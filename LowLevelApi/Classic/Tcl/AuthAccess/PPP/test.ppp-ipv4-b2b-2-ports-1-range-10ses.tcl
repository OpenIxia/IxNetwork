# TCL script modified by TCL Script Doctor on 10/29/2008 5:40:51 PM
#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shws how to run a SM test case, and how to verify the some SM
# statistics
#
# Sequence of events being carried out by the script
#     1) Configure pppox protocol by sourcing the script gen file
#     2) Start protocol pppox
#     3) Check the the server and client sessions up
#
# SCRIPT-GEN USED : Yes
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

#------------------------------------------------------------------------------
# PROCEDURE    : GetIxStatValue
# PURPOSE      : Retriving the PPPoX stat values for from the stat view browser
# INPUT        : (1) Stat View Caption
#                (2) Array of the expected stat Name.
# OUTPUT       : The stat values
# RETURN VALUE : The stat value array
#------------------------------------------------------------------------------
proc GetIxStatValue {viewCaption statName} {

    set statValue 0
    set statViewList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    set statViewObjRef ""
    foreach statView $statViewList {
        if {[ixNet getAttribute $statView -name] == $viewCaption} {
            if {[ixNet getAttribute $statView -enabled] == "false"} {
                ixNet setAttribute $statView -enabled true
                ixNet commit
            }
            set statViewObjRef $statView
            break
        }
    }

    if {[info exists statValueArray]} {
        unset statValueArray
    }
    after 1000

    set timeout 10
    while {$timeout > 0} {
        if {[ixNet getAttribute $statViewObjRef -isReady] == true} {
            break
        }
        after 500
        incr timeout -1
    }

    if {[ixNet getAttribute $statViewObjRef -isReady] != true} {
        puts "Error: Data is not available."
        return 0
    }

    if {[ixNet getAttribute $statViewObjRef -isReady] != true} {
        puts "Error: Data is not available."
        return 0
    }

    set rowList [ixNet getList $statViewObjRef row]
    foreach row $rowList {
        set cellList [ixNet getList $row cell]
        foreach cell $cellList {
            if {[ixNet getAttribute $cell -catalogStatName] == $statName} {
                set statValue [ixNet getAttribute $cell -statValue]
                break
            }
        }
    }

    puts " GetIxStatValue value = ($statValue)"
    return $statValue
}


#------------------------------------------------------------------------------
# PROCEDURE    : Action
# PURPOSE      : Encapsulating all of your testing actions
# INPUT        : (1) [list $chassis1 $card1 $port1 $client1 $tcpPort1]
#                (2) [list $chassis2 $card2 $port2 $client2 $tcpPort2]
#                (3) home; (the current directory)
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {
    # initialize return value
    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set client1    [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]

    # get port info 2
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set client2    [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]

    if {$client1 == $client2} {
        set status ""
        puts "Connecting to client $client1"
        if {[catch {set status [ixNet connect $client1 -port \
            $tcpPort1]} error]} {
            puts "Unable to connect to ixNetwork"
            return $FAILED
        }

        if {[string equal $status "::ixNet::OK"] != 1} {
            puts "connection to client unsuccessfill"
            return $FAILED
        }

    } else {

        puts "Try to use the same client"
        return $FAILED
    }

    # clean up all the existing configurations from client
    puts "cleaning up the client"
    ixNetCleanUp
    puts "Executing from [pwd]"

    # Now we configure the first Ixia port
    puts "Now we configure the first Ixia port from the script-gen file"
    if {[catch {source "$::pwd/config.ppp-ipv4-b2b-2-ports-1-range-10ses.tcl"} \
        error] } {
        puts "Error in sourcing the file ./config.ethernet-l2-vpn-15.3.tcl"
        puts "$error"
        return $FAILED
    }

    # get the virtual port list
    puts "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    puts "Virtual ports are = $vPorts"

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1]\
         [list $chassisIp2 $card2 $port2] ]

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    puts "Assigned: $status"
    ixNet commit
    if {[string equal [lindex $status 0] $vPort1] != 1 ||\
        [string equal [lindex $status 1] $vPort2] != 1} {
        ixNetCleanUp
        return $FAILED
    }

    puts "getting ppp plugin from port 1"
    set p1 [lindex $vPorts 0]
    set l2eth1 [lindex [ixNet getList $p1/protocolStack ethernet] 0]
    set myppp1 [lindex [ixNet getList $l2eth1 pppoxEndpoint] 0]
    puts "got ppp pluging from port 1 successfully"

    puts "getting ppp plugin from port 2"
    set p2 [lindex $vPorts 1]
    set l2eth2 [lindex [ixNet getList $p2/protocolStack ethernet] 0]
    set myppp2 [lindex [ixNet getList $l2eth2 pppoxEndpoint] 0]
    puts "got ppp pluging from port 2 successfully"

    puts "Starting PPPoX on the ports"
    ixNet exec start $myppp2
    ixNet exec start $myppp1
    puts "PPPoX started on the ports"

    puts "Wait for 30 seconds"
    after 30000

    set viewName       "PPP Setup Statistics - All Ports"
    set statNameClient "Client Interfaces Up"
    set statNameServer "Server Interfaces Up"

    set expectedValue 10
    set timeout       10

    set statList [ixNet getList [ixNet getRoot]/statistics statViewBrowser]
    foreach stat $statList {
       if { [regexp $viewName $stat] } {
            if { [regexp -nocase [ixNet getAtt $stat -enabled] false] } {
                 puts "Eanbling stats $stat"
                 ixNet setAtt $stat -enabled true
                 ixNet commit
                 after 2000
                 break
            }
        }
    }

    set sval 0
    set cval 0
    set sval [GetIxStatValue $viewName $statNameServer]
    set cval [GetIxStatValue $viewName $statNameClient]

    puts "The no of interfaces up on server is $sval"
    puts "The no of interfaces up on client is $cval"

    if { ($sval != $expectedValue) || ($cval != $expectedValue) } {
        puts "The values are not equal to expected value $expectedValue"
        ixNetCleanUp
        return $FAILED
    }


    if { [catch {ixNet exec stopAllProtocols} err] } {
        puts "Error: $err while stopping protocols"
        ixNetCleanUp
        return $FAILED
    }

    ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
