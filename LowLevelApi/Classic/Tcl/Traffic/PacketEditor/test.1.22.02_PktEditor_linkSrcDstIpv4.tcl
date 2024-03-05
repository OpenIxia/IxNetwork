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


#-------------------------------------------------------------------------------
# Name      : test.Packet_Editor_1.22.02.tcl
# Purpose   : To Automate a test case which checks linking between src and
#                 dst ipv4 address
# Description   : The loaded config file has the follwoing configurations:
#                     a) A raw IPv4 traffic
#                     b) The raw traffic has a LINK between srcIp and destIp
#                     c) Source IP has the count 4
#                     d) Dest IP has the count 4
#                     e) So there suppose to be 4 * 4 = 16 <sourceIP destIP>
#                        tuple
#                     f) Transmission mode is Fixed Iteration Count (1). So
#                        expection is if the stream contains 16 packets, only
#                        16 packets will be transmitted, and transmission will
#                        be stopped after that.
#                     g) Transmission rate is 1 packet prsecond
#
# Steps         :  1) Load the above config
#                  2) Start transmitting
#                  3) Wait for 20 seconds (give enough time to transmit all the
#                     packets)
#                  4) Stop transmit. There shall be exactly 16 packets in the
#                     captute buffer.
#                  5) Those packets will have uniques <sourceIP destIP>
#                     combination (as specified in the raw packet configuration)
#-------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc Action {portData1 portData2} {
    #---------------------------------------------------------------------------
    # initialize return values
    #---------------------------------------------------------------------------
    set PASSED 0
    set FAILED 1

    #---------------------------------------------------------------------------
    # get port info 1
    #---------------------------------------------------------------------------
    set chassisIp1 [getChassisIp  $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    #---------------------------------------------------------------------------
    # get port info 2
    #---------------------------------------------------------------------------
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    #---------------------------------------------------------------------------
    # Connecting to client
    #---------------------------------------------------------------------------
    set connection_Result [connectToClient $portData1 $portData2 5.40]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessfill"
        return $FAILED
    }
    log "connectToClient Successful"

    #---------------------------------------------------------------------------
    # clean up all the existing configurations from client
    #---------------------------------------------------------------------------
    log "cleaning up the client"
    ixNetCleanUp

    #---------------------------------------------------------------------------
    # load the ixncfg config file
    #---------------------------------------------------------------------------
    set configFileName config.[getTestId].ixncfg
    if {[catch {ixNet exec loadConfig [ixNet readFrom \
         "$::pwd/$configFileName"]} errorMsg]} {
       log "Error in loading Config file: $errorMsg"
       ixNetCleanUp
       return $FAILED
    }

    #---------------------------------------------------------------------------
    # get the virtual port list and real port list
    #---------------------------------------------------------------------------
    log "getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
        [list $chassisIp2 $card2 $port2] ]

    #---------------------------------------------------------------------------
    # Assign virtual ports to real ports
    #---------------------------------------------------------------------------
    log "Assign virtual ports to real ports ..."
    set force true
    set status [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $status"
    ixTclNet::CheckLinkState $vPorts doneList

    #---------------------------------------------------------------------------
    # Check if the ports are assigned if un assigned re-assign them
    #---------------------------------------------------------------------------
    after 5000
    ifUnassignedConnectAgain

    #---------------------------------------------------------------------------
    # Forcefully make the port mode "capture"
    #---------------------------------------------------------------------------
    if {[enableCaptureMode $vPorts]} {
        log "unable to make port mode capture"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # generte the traffic
    #---------------------------------------------------------------------------
    generateApplyTraffic

    #---------------------------------------------------------------------------
    # Start packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec startCapture} errorMsg]} {
        log "error in starting capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }
    after 1000

    #---------------------------------------------------------------------------
    # start the traffic
    #---------------------------------------------------------------------------
    set traffic [ixNet getRoot]/traffic
    startTraffic $traffic

    #---------------------------------------------------------------------------
    # wait for desired amount of time
    #---------------------------------------------------------------------------
    set waitTime 60000
    log "wait for $waitTime ms"
    after $waitTime

    #---------------------------------------------------------------------------
    # Stop the traffic
    #---------------------------------------------------------------------------
    stopTraffic $traffic

    #---------------------------------------------------------------------------
    # stop packet capture
    #---------------------------------------------------------------------------
    if {[catch {ixNet exec stopCapture} errorMsg]} {
        log "error in stopping capture $errorMsg"
        ixNetCleanUp
        return $FAILED
    }

    #---------------------------------------------------------------------------
    # verify capture
    #---------------------------------------------------------------------------
    set expectedPktCount 16
    set numPackets [numberOfPacketCapturedInBuffer $chassisIp2 $card2 $port2]
    if {$numPackets != $expectedPktCount} {
        log "Expected $expectedPktCount packets will be present in the buffer"
        log "The number of packet present is $numPackets"
        ixNetCleanUp
        return $FAILED
    }

    # create the source address and dest address array
    for {set i 1} {$i <= 4} {incr i} {
        set srcAddr($i) "0C 00 00 0$i"
        set dstAddr($i) "0E 00 00 0$i"
    }

    # for each source address and destination address pair verify that packet
    # is present
    set isFound 1
    set startIndexSrc 26
    set endIndexSrc   29
    set startIndexDst 30
    set endIndexDst   33
    for {set i 1} {$i <= 4} {incr i} {
        for {set j 1} {$j <= 4} {incr j} {
            set src $srcAddr($i)
            set dst $dstAddr($j)
            set expetedList [subst {$startIndexSrc $endIndexSrc "$src" \
                                    $startIndexDst $endIndexDst "$dst"}]

            if {[verifyCapturedPackets $chassisIp2 $card2 $port2 \
                $expetedList]} {
                log "Src/Dst pair $src/$dst not found"
                set isFound 0
            }
        }
    }

    #---------------------------------------------------------------------------
    # clean up and exit
    #---------------------------------------------------------------------------
    ixNetCleanUp

    if {$isFound == 0} {
        return $FAILED
    }

    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
