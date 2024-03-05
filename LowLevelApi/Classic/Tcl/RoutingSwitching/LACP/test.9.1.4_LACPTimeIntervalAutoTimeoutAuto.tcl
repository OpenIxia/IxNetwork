################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################
################################################################################
# File Name  : test.9.1.4_LACPTimeIntervalAutoTimeoutAuto.tcl
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
