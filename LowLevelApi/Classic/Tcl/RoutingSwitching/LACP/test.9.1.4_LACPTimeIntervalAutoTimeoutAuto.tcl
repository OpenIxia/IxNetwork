
################################################################################
# File Name  : test.9.1.4_LACPTimeIntervalAutoTimeoutAuto.tcl
# Author     : Darshan T
# Purpose    : This test case verifies that if Time out set to auto and time
#              interval set to auto for both the ports and if stop protocol on
#              port 2 then after 90 sec port1 goes in to Expiry set and after 3
#              sec of expiry it will move to defaulted state.
# Return     : 0 - PASS
#              1 - FAIL
################################################################################
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl


proc Action {portData1 portData2} {

    source $::pwd/LACP_Utils.tcl
    # initialize return value
    set PASSED 0
    set FAILED 1
    global lacpGlobalParams

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
    #ixNetCleanUp
    puts "Executing from [pwd]"

    set configFileName "config.9.1.4_LACPTimeIntervalAutoTimeoutAuto.ixncfg"

    puts "Loading the config file......"
    if  {[ixNet exec loadConfig [ixNet readFrom $::pwd/$configFileName]] != \
          $lacpGlobalParams(ixNetOk)} {
        puts "Loading IxNetwork config file FAILED "
        #ixNetCleanUp
        return $FAILED
    }

    puts "Configuration of the ports Successful"
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # Assign virtual ports to real ports

    puts "Assign virtual ports to real ports ..."
    set root   [ixNet getRoot]
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts]
    ixNet commit

    puts "Assigned: $status"
    set vport1 [lindex $vPorts 0]
    set vport2 [lindex $vPorts 1]

    set proto [ixNet getList $vport1 protocols]
    set proto [ixNet getList $proto lacp]

    set proto1 [ixNet getList $vport2 protocols]
    set proto1 [ixNet getList $proto1 lacp]

    set linkList1 [ixNet getList $proto link]
    set link1     [lindex $linkList1 0]

    # Start LACP Protocol
    puts "Start LACP Protocol on both ports"

    if {[startLacpOnPorts $proto $proto1] ==1} {
      puts "Error In Starting LACP protocol"
      #ixNetCleanUp
      return $FAILED
    }

    puts "Wait for $lacpGlobalParams(pktCaptureDurShort) sec...."
    after $lacpGlobalParams(pktCaptureDurShortInMilisec)

    #Enabling Capture on ports

    if {[enableAndStartCapture [lindex $vPorts 0] [lindex $vPorts 1]] == 1} {
        puts "Error In Enable and Starting of capture on ports"
        ixNetCleanUp
        return $FAILED
    }

	
    puts "Wait for 35sec. so that atleast one lacpdu is captured from each port"
    after 35000

    # Stop LACP on Port2
    puts "Stop LACP Protocol on port2"
    if {[stopLacpOnPorts $proto1] ==1} {

        puts "Error In Starting LACP protocol on port2"
            
        return $FAILED
    }
    puts "Wait for $lacpGlobalParams(pktCaptureDurLong) sec"

    after $lacpGlobalParams(pktCaptureDurLongInMilisec)

    # Stop Capture
    puts "Stopping the capture"
    if {[catch {ixNet exec stopCapture} err] == 1} {
        puts "Failed to stop packet capture "
            
        return $FAILED
    }

	
    # Stop LACP on Port1
    puts "Stop LACP Protocol on port1"
    if {[stopLacpOnPorts $proto] ==1} {
        puts "Error In Starting LACP protocol on port1"
            
        return $FAILED
    }

    puts "Checking for time stamp of last LACP packet sent by port2"

    set lastPacketTimeStamp [getTimeValueOfLacpPacket $chassisIp1 \
                                 $card1 $port1 1]

    if {$lastPacketTimeStamp == 1 || $lastPacketTimeStamp == 0} {

        puts "Error In getting time stamp last LACP packet sent by port2..."
            
        return $FAILED
    }

    puts "Checking for time stamp of first LACP packet in which expiry \
          bit set  sent by port1"

    set firstExpbitSetPckTimestamp [getTimeValueOfLacpPacket $chassisIp2 \
                                        $card2 $port2 2]

    if {$firstExpbitSetPckTimestamp == 1 || $firstExpbitSetPckTimestamp == 0} {
        puts "Error In getting time stamp of first LACP packet in \
              which expiry bit set  sent by port1..."
            
        return $FAILED
    }

    set obsLacpTimeout [expr [expr $firstExpbitSetPckTimestamp - $lastPacketTimeStamp]\
                                   /$lacpGlobalParams(devideValue)]

    puts "The last pdu time stamp is <$lastPacketTimeStamp>"
    puts "The First Exp bit set time stamp is <$firstExpbitSetPckTimestamp>"
    puts "The Observed LACP Timeout value is <$obsLacpTimeout>"
    if {$obsLacpTimeout > 90 || \
        $obsLacpTimeout < 89} {

        puts "FAILURE : Observed Lacp Timeout is <$obsLacpTimeout>sec. \
              should have been 90sec for long."
            
        return $FAILED
    }

    set firstDefbitSetPckTimestamp [getTimeValueOfLacpPacket $chassisIp2 \
                                        $card2 $port2 4]

    if {$firstDefbitSetPckTimestamp == 1 || $firstDefbitSetPckTimestamp == 0} {

        puts "Error In getting time stamp..."
            
        return $FAILED
    }


    puts "The First Default bit set time stamp is <$firstDefbitSetPckTimestamp>"
    set defTimeout [expr [expr $firstDefbitSetPckTimestamp - $firstExpbitSetPckTimestamp]\
                               /$lacpGlobalParams(devideValue)]

    puts "Time taken to go to defaulted state : <$defTimeout>"
    if {$defTimeout < $lacpGlobalParams(shortTimeoutLowerlimit) || \
        $defTimeout > $lacpGlobalParams(shortTimeoutUpperlimit)} {

        puts "FAILURE: Time taken to go to defaulted state from expiry state is \
             <$defTimeout>sec. should have been 3sec."
            
        return $FAILED
    }

        
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
