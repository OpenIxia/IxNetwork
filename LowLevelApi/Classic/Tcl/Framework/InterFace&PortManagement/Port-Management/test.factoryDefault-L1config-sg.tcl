#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to manipulate the L1 config options and how do
# reset factory default operation to a port. This test cases
#
# Sequence of events being carried out by the script
#    1) Loads a tcl config file
#    2) Checks the L1 config parameters
#    3) Reset factory defaults
#    4) Checks the L1 config again
#
# SCRIPT-GEN USED : Yes
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#---------------------------------------------------------------------------
# PROCEDURE    : verifyL1ConfigProperties
# PURPOSE      : Checking L1 config properties.
# RETURN VALUE : bool
#---------------------------------------------------------------------------
proc verifyL1ConfigProperties {vPort1 matchMode} {
    set isError 0
    set L1config [ixNet getList $vPort1 l1Config]

    #ixNet setAttribute $ixNetSG_curObj/l1Config -currentType ethernet
    if {[ixNet getAttr $L1config -currentType] != "ethernet"} {
        puts "This proc intended to check L1 config for type Ethernet"
        set isError 1
        return $isError
    }

    set L1configEth  [ixNet getList $L1config ethernet]
    puts "This os tje match $L1configEth"

    if {$matchMode == "FactoryDefault"} {
        array set expectProp {autoNegotiate true \
                              speed speed100fd   \
                              loopback false     \
                              media copper}
    } else {
        array set expectProp {autoNegotiate false\
                              speed speed10fd    \
                              loopback true      \
                              media copper}
    }

    puts "[parray expectProp]"
    puts "Now checking ethernet attributes of L1Config ........."

    foreach attr [array names expectProp] {
        set attVal [ixNet getAttr $L1configEth -$attr]
        set val $expectProp($attr)
        puts "attVal = $attVal (-$attr) expectProp = $val"

        if {$attVal != $val} {
            puts "attVal = $attVal expectProp = $val --> did not match!"
            set isError 1
            return $isError
        }
    }
    return $isError
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
    if {[catch {source "$::pwd/config.factoryDefault-L1config-sg.tcl"} \
         error] } {
         puts "Error in sourcing the file ./config.factoryDefault-L1config-sg.tcl"
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
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2] ]

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    puts "Assigned: $status"
    ixNet commit
    if {[string equal [lindex $status 0] $vPort1] != 1 } {
        ixNetCleanUp
        return $FAILED
    }


    if {[verifyL1ConfigProperties $vPort1 "sgConfig"] == 1} {
        # Error Occured :: Start cleanup
        cleanupConfigurationFromPorts
        return $FAILED
    }

    # Sg configuration is properly applied to the port
    puts "Apply config to port was successful"

    if {[setPortPropertiesToFactoryDefaults $vPort1] == 1} {
        # Error Occured :: Start cleanup
        cleanupConfigurationFromPorts
        return $FAILED
    }

    puts "Wait for 10 secomds"
    after 10000

    if {[verifyL1ConfigProperties $vPort1 "FactoryDefault"] == 1} {
        # Error Occured :: Start cleanup
        cleanupConfigurationFromPorts
        return $FAILED
    }
    puts "Clening up configurations ..."

    ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
