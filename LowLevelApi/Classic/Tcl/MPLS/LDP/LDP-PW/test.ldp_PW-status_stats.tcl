source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#------------------------------------------------------------------------------
# PROCEDURE    : Action
# PURPOSE      : Encapsulating all of your testing actions
# INPUT        : (1) [list $chassis1 $card1 $port1 $client1 $tcpPort1]
#                (2) [list $chassis2 $card2 $port2 $client2 $tcpPort2]
#                (3) home; (the current directory)
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {
    source $::pwd/ldpUtilsQa.tcl

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
        if {[catch {set status [ixNet connect $client1 -port $tcpPort1]} error]} {
            puts "Unable to connect to ixNetwork"
            return $FAILED
        }

        if {[string equal $status "::ixNet::OK"] != 1} {
            puts "connection to client unsuccessful"
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

    #Creating New Config
    ixNet exec newConfig

    puts "loading ixncfg file ..."
    # load config files
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/config.ldp_PW-status_stats.ixncfg"]] != "::ixNet::OK"} {
        puts "Error in sourcing the file config.refreshCfmCcmLearnedInfo.ixncfg"
        return $FAILED

    } else {
        # For stand alone test
        puts "Loading IxNetwork config file : passed"
    }

    # Assign real ports to virtual ports
    puts "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    puts "Virtual ports are = $vPorts"


    set realPortsList [list [list $chassisIp1 $card1 $port1]\
            [list $chassisIp2 $card2 $port2]]

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    puts "Assigned: $status"
    ixNet commit
    if {[string equal [lindex $status 0]  $vPort1] != 1 || \
        [string equal [lindex $status 1]  $vPort2] != 1} {
        ixNetCleanUp
        return $flag
    }

    # get ldp from protocol management

    set portList1 [list [list $chassisIp1 $card1 $port1]]


    set ldpProtocolMgmt1 "$vPort1/protocols/ldp"
    set ldpProtocolMgmt2 "$vPort2/protocols/ldp"

    set l2Vcrange1 [lindex [ixNet getList [lindex [ixNet getList \
        [lindex [ixNet getList $ldpProtocolMgmt1 router] 0] l2Interface] 0] l2VcRange] 0]

    set l2Vcrange2 [lindex [ixNet getList [lindex [ixNet getList \
        [lindex [ixNet getList $ldpProtocolMgmt2 router] 0] l2Interface] 0] l2VcRange] 0]

    set pwstatustlvoption1 [ixNet getAtt $l2Vcrange1 -enablePwStatusTlv]
    set pwstatustlvoption2 [ixNet getAtt $l2Vcrange2 -enablePwStatusTlv]

    if {$pwstatustlvoption1 && $pwstatustlvoption2 == "true"} {
        ixNet exec start $ldpProtocolMgmt1
        ixNet exec start $ldpProtocolMgmt2

        puts "LDP started"
        puts "LDP started"

        puts "waiting for 35 seconds for down interval"
        after 35000

         set expectedStat {"LDP Basic Sessions Up"                     1 \
                           "LDP Targeted Sessions Up"                  1 \
                           "LDP Targeted Sessions Configured"          1 \
                           "LDP PW Status Down"                        1 \
                           "LDP Aggregated PW Status Notification Tx"  1 \
                           "LDP Aggregated PW Status Notification Rx"  1}

        set status [checkAllLdpStats $portList1  $expectedStat]

        if {$status != 0} {
            ixNetCleanUp
            set flag 1
            return $flag
        }

        puts "waiting for 40 seconds for up interval"
        after 40000

        set expectedStat {"LDP Basic Sessions Up"                    1 \
                          "LDP Targeted Sessions Up"                 1 \
                          "LDP Targeted Sessions Configured"         1 \
                          "LDP PW Status Down"                       0 \
                          "LDP Aggregated PW Status Notification Tx" 1 \
                          "LDP Aggregated PW Status Notification Rx" 1 \
                          "LDP Aggregated PW Status Cleared Tx"      1 \
                          "LDP Aggregated PW Status Cleared Rx"      1}

        set status [checkAllLdpStats $portList1  $expectedStat]

        if {$status != 0} {
            ixNetCleanUp
            set flag 1
            return $flag
        }
    }  else {
        puts "PW-Status is not enabled: FAILED "
        ixNetCleanUp
        return $flag
    }

    ixNetCleanUp
    set flag 0
    return $flag
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
