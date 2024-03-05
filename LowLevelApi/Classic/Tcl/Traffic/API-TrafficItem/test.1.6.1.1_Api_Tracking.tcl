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
# File Name - test.1.6.1.1_Api_Tracking.tcl
# Description:
#            1) Load the scriptgen file using Tcl
#            2) Verify the configuration
#            3) Maipulate the attributes and verify its value again what was set
# Topology  - B2B
################################################################################
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

proc verifyEgressAttributes {egress} {
    set isError 1

    set offsetsAvail [list {Outer VLAN Priority (3 bits)}         \
                           {Outer VLAN ID (4 bits)}               \
                           {Outer VLAN ID (6 bits)}               \
                           {Outer VLAN ID (8 bits)}               \
                           {Outer VLAN ID (10 bits)}              \
                           {Outer VLAN ID (12 bits)}              \
                           {Inner VLAN Priority (3 bits)}         \
                           {Inner VLAN ID (4 bits)}               \
                           {Inner VLAN ID (6 bits)}               \
                           {Inner VLAN ID (8 bits)}               \
                           {Inner VLAN ID (10 bits)}              \
                           {Inner VLAN ID (12 bits)}              \
                           {MPLS Exp (3 bits)}                    \
                           {IPv4 TOS Precedence (3 bits)}         \
                           {IPv4 DSCP (6 bits)}                   \
                           {IPv6 Traffic Class (8 bits)}          \
                           {IPv6 Traffic Class Bits 0-2 (3 bits)} \
                           {IPv6 Traffic Class Bits 0-5 (6 bits) } ]

    set enacapsulationsAvail [ixNet getAttr $egress -availableEncapsulations]

    if {[setAndCheckAttributeValue $egress "enabled" \
           {"True" y}] == 1} {
           return $isError
    }

    foreach encap $enacapsulationsAvail {
        if {[setAndCheckAttributeValue $egress "encapsulation" \
            [list $encap y]] == 1} {
             error "1"
            return $isError
        }
    }

    # Assumption enacapsulation = {POS: Cisco Frame Relay} is set as result
    # of the previous foreach
    if {[setAndCheckAttributeValue $egress "offset" \
        [list {MPLS Exp (3 bits)} y]] == 1} {
            error "2"
        return $isError

    }

    # set encapsulatipn custom first ...
    if {[setAndCheckAttributeValue $egress "encapsulation" \
        [list {Any: Use Custom Settings} y]] == 1} {
            error "3"
        return $isError
    }

    # then set custom bits
    if {[setAndCheckAttributeValue $egress "customOffsetBits" \
        {"100" y}] == 1} {
            error "4"
        return $isError
    }

    if {[setAndCheckAttributeValue $egress "customWidthBits" \
        {"2" y}] == 1} {
            error "5"
        return $isError
    }

    set isError 0
    return $isError
}


proc verifyLatencyBinAttributes {latencyBin} {
    set isError 1
    # Set valid value & verify

    if {[setAndCheckAttributeValue $latencyBin "numberOfBins" \
        {"15" y}] == 1} {
        return $isError
    }

    set letValList [list 1.000000   1.420000 \
                         2.000000   2.820000 \
                         4.000000   5.660000 \
                         8.000000  11.320000 \
                         16.000000 22.620000 \
                         32.000000 45.260000 \
                         64.000000 90.500000 \
                         128.000000]

    if {[setAndCheckAttributeValue $latencyBin "binLimits" \
        [list $letValList y]] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $latencyBin "enabled" \
        {"True" y}] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


proc verifyTrafficItemTrackingAttributes {ttracking} {

    set isError 1
    set availableTrackBy [list customOverride \
                               trackingenabled0 \
                               sourceDestEndpointPair0 \
                               sourceDestValuePair0 \
                               sourceDestPortPair0 \
                               sourceEndpoint0 \
                               destEndpoint0 \
                               sourcePort0 \
                               trafficGroup0 \
                               ethernetIiDestinationaddress0 \
                               ethernetIiSourceaddress0 \
                               ethernetIiEtherType0 \
                               ethernetIiPfcQueue0 \
                               ipv4Precedence0 \
                               ipv4SourceIp0 \
                               ipv4DestIp0]

    set listOfTrackBy [list {trackingenabled0} \
                            {ethernetIiDestinationaddress0}  \
                            {ethernetIiSourceaddress0} \
                            {ipv4SourceIp0} \
                            {ipv4DestIp0} \
                            {customOverride}]


    ixNet setAttr $ttracking -trackBy $listOfTrackBy
    ixNet commit

    if {[setAndCheckAttributeValue $ttracking "offset" \
        {"100" y}] == 1} {
        return $isError
    }

    if {[setAndCheckAttributeValue $ttracking "values" \
        [list [list 99 ] y]] == 1} {
         return $isError
    }

    if {[setAndCheckAttributeValue $ttracking "fieldWidth" \
        {"thirtyTwoBits" y}] == 1} {
         return $isError
    }

    if {[setAndCheckAttributeValue $ttracking "oneToOneMesh" \
        {"True" y}] == 1} {
        return $isError
    }

    set isError 0
    return $isError
}


proc Action {portData1 portData2} {
    set FAILED 1
    set PASSED 0

    set ASSIGN_PORT 0

    # get port info 1
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # get port info 2
    set chassisIp2 [getChassisIp $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.40)
    set version "5.40"

    # connect to the chassis
    set connection_Result [connectToClient $portData1 $portData2 $version]
    log "Connection Result: $connection_Result"
    if {[string equal $connection_Result "::ixNet::OK"] != 1} {
        log "connection to client unsuccessful"
        return $FAILED
    }
    log "connectToClient Successful"

    # clean up all the existing configurations from client
    log "cleaning up the client"
    ixNetCleanUp

    after 2000

    # load config files
    set configFileName config.[getTestId].ixncfg
    if  {[ixNet exec loadConfig [ixNet readFrom "$::pwd/$configFileName"]] != \
         "::ixNet::OK"} {
        log "Loading IxNetwork config file : Failed "
        ixNetCleanUp
        return $FAILED
    }
    log "Loading IxNetwork config file : Passed"


    if {$ASSIGN_PORT} {
        # getting the real port list
        set realPortsList [list [list $chassisIp1 $card1 $port1] \
                                [list $chassisIp2 $card2 $port2]]

        # Assign real ports to virtual ports
        log "getting virtual ports ...."
        set vPorts [ixNet getList [ixNet getRoot] vport]
        set vPort1 [lindex $vPorts 0]
        set vPort2 [lindex $vPorts 1]
        log "Virtual ports are = $vPorts"

        # Assign virtual ports to real ports
        log "Assign virtual ports to real ports ..."
        set force true
        set status      [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
        log "Assigned: $status"
        ixNet commit
        if {[string equal [lindex $status 0]  $vPort1] != 1 || \
            [string equal [lindex $status 1]  $vPort2] != 1} {
            ixNetCleanUp
            return $FAILED
        }
        ixTclNet::CheckLinkState $vPorts doneList
    }

    # Verify configurations
    set Root [ixNet getRoot]
    set traffic $Root/traffic
    set tracking $traffic/tracking
    set ti1 [lindex [ixNet getList $traffic trafficItem] 0]
    set tt1 [lindex [ixNet getList $ti1 tracking] 0]
    set eg1 [lindex [ixNet getList $tt1 egress] 0]
    set lb1 [lindex [ixNet getList $tt1 latencyBin] 0]
    after 100

    #-------------------------------------------------------------------------
    # EGRESS
    #-------------------------------------------------------------------------
    if {[verifyEgressAttributes $eg1] == 1} {
        after 1000000
        ixNetCleanUp
        return $FAILED
    }
    log "Egress Attributes verification successful"

    after 100
    #-------------------------------------------------------------------------
    # LATENCY BIN
    #-------------------------------------------------------------------------
    if {[verifyLatencyBinAttributes $lb1] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "Latency Bin Attributes verification successful"

    after 100
    #--------------------------------------------------------------------------
    # TRACKING (TRAFFIC ITEM TRACKING, NOT TRAFFIC)
    #--------------------------------------------------------------------------
    if {[verifyTrafficItemTrackingAttributes $tt1] == 1} {
        ixNetCleanUp
        return $FAILED
    }
    log "Traffic Item Tracking Attributes verification successful"

    ixNetCleanUp
    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
