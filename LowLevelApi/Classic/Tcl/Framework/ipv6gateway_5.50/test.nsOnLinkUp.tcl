source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#-----------------------------------------------------------------------------#
# Name  : test.2.1_Enable_LinkOnUp_check_Stats_DiscoNeigh.tcl                 #
# Steps : 1. Add 2 virual ports                                               #
#         2. Add muliple IPv6 Interfaces and assign IPv6 Gateway to them.     #
#         3. Enable the 'NS on Link Up' option."                              #
#         4. Assign 2 B2B real ports to virtual ports.                        #
#         5. Check in Statistics if Neighbor solicitation are sent.           #
#         6. Discovered info will be displayed in the                         #
#           'Discovered Neighbors' tab.                                       #
#-----------------------------------------------------------------------------#

proc configureIxNetworkGui {} {

    set port1Interface1Ipv6Addr1 "1234:0:0:0:0:0:0:1"
    set port1Interface2Ipv6Addr2 "4321:0:0:0:0:0:0:1"

    set port2Interface1Ipv6Addr1 "1234:0:0:0:0:0:0:2"
    set port2Interface2Ipv6Addr2 "4321:0:0:0:0:0:0:2"

    set port1Interface1Ipv6Gateway1 $port2Interface1Ipv6Addr1
    set port1Interface2Ipv6Gateway2 $port2Interface2Ipv6Addr2

    set port2Interface1Ipv6Gateway1 $port1Interface1Ipv6Addr1
    set port2Interface2Ipv6Gateway2 $port1Interface2Ipv6Addr2

    # get Root object
    set root [ixNet getRoot]

    # Add virual port1
    set vport1 [ixNet add $root vport]
    ixNet commit
    set vport1  [lindex [ixNet remapIds $vport1] 0]

    # Add virual port2
    set vport2 [ixNet add $root vport]
    ixNet commit
    set vport2  [lindex [ixNet remapIds $vport2] 0]

    # Add two connected interface on virtual port 1
    set interface11 [ixNet add $vport1 interface]
    ixNet commit
    set interface11 [lindex [ixNet remapIds $interface11] 0]

    set interface12 [ixNet add $vport1 interface]
    ixNet commit
    set interface12 [lindex [ixNet remapIds $interface12] 0]

    # add 1 Ipv6 address and corresponding gateway on each interface.
    ixNet setAttr $interface11 -enabled true
    ixNet commit

    set ipv6addr11 [ixNet add $interface11 ipv6]
    ixNet setAttr $ipv6addr11 -ip $port1Interface1Ipv6Addr1
    ixNet setAttr $ipv6addr11 -gateway $port1Interface1Ipv6Gateway1
    ixNet setAttr $ipv6addr11 -prefixLength 64
    ixNet commit

    ixNet setAttr $interface12 -enabled true
    ixNet commit

    set ipv6addr12 [ixNet add $interface12 ipv6]
    ixNet setAttr $ipv6addr12 -ip $port1Interface2Ipv6Addr2
    ixNet setAttr $ipv6addr12 -gateway $port1Interface2Ipv6Gateway2
    ixNet setAttr $ipv6addr12 -prefixLength 64
    ixNet commit

    # Add two connected interface on virtual port 2
    set interface21 [ixNet add $vport2 interface]
    ixNet commit
    set interface21 [lindex [ixNet remapIds $interface21] 0]

    set interface22 [ixNet add $vport2 interface]
    ixNet commit
    set interface22 [lindex [ixNet remapIds $interface22] 0]


    # add 1 Ipv6 address and corresponding gateway on each interface.
    ixNet setAttr $interface21 -enabled true
    ixNet commit

    set ipv6addr21 [ixNet add $interface21 ipv6]
    ixNet setAttr $ipv6addr21 -ip $port2Interface1Ipv6Addr1
    ixNet setAttr $ipv6addr21 -gateway $port2Interface1Ipv6Gateway1
    ixNet setAttr $ipv6addr21 -prefixLength 64
    ixNet commit

    ixNet setAttr $interface22 -enabled true
    ixNet commit

    set ipv6addr22 [ixNet add $interface22 ipv6]
    ixNet setAttr $ipv6addr22 -ip $port2Interface2Ipv6Addr2
    ixNet setAttr $ipv6addr22 -gateway $port2Interface2Ipv6Gateway2
    ixNet setAttr $ipv6addr22 -prefixLength 64
    ixNet commit

    # turn nsOnLinkup off
    set globals $root/globals
    set interfaces $globals/interfaces
    ixNet setAttr $interfaces -nsOnLinkup false
    ixNet commit
}


proc checkDiscoverNeighbor {port NeighborList} {
    set totalNeigborsFound 0
    set neighbors [ixNet getList $port discoveredNeighbor]
    set totalNeighbors [llength $neighbors]

    for {set count 0} {$count < [llength $NeighborList]} {incr count} {
        set expectedNeig [lindex $NeighborList $count]
        puts "expected Neighbor is $expectedNeig"

        for {set count1 0} {$count1 < $totalNeighbors} {incr count1} {
            set discoveredNeighbor1 [lindex $neighbors $count1]
            set neighborIp [ixNet getAttr $discoveredNeighbor1 -neighborIp]
            puts "Obtained Neighbor is $neighborIp"

            if {$neighborIp == $expectedNeig} {
               puts "Neigbor $expectedNeig is obtained"
               incr totalNeigborsFound
               break
            }
        }
    }

    if {$totalNeigborsFound >= [llength $NeighborList]} {
        return 0
    } else {
        return 1
    }
}


proc Action {portData1 portData2} {

    set FAILED 1
    set PASSED 0

    # get port info 1
    set chassisIp1 [getChassisIp $portData1]
    set card1      [getCardNumber $portData1]
    set port1      [getPortNumber $portData1]

    # get port info 2
    set chassisIp2 [getChassisIp  $portData2]
    set card2      [getCardNumber $portData2]
    set port2      [getPortNumber $portData2]

    # Hostname, where IxNetwork TCL-Server client runs
    set hostName [lindex [getHostName $portData1] 0]

    # Version Number (IxNetwork Major version No i.e. 5.50)
    set version "5.50"

    # connect to client
    if {[ixNet connect $hostName -version 5.50] != "::ixNet::OK"} {
        puts "Test case failed unable to connect to IxNetwork"
        return $FAILED
    }

    # clean up config
    ixNet exec newConfig

    # Configure IxNetwork GUI
    configureIxNetworkGui

    # getting the real port list
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]

    # get root object
    set root [ixNet getRoot]

    # Assign real ports to virtual ports
    puts "getting virtual ports ...."
    set vPorts [ixNet getList $root vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]

    # enable NS on Link Up option
    set globals $root/globals
    set interfaces $globals/interfaces
    ixNet setAttr $interfaces -nsOnLinkup true
    ixNet commit

    # Assign virtual ports to real ports
    puts "Assign virtual ports to real ports ..."
    if {[catch {ixTclNet::AssignPorts $realPortsList {} $vPorts}]} {
        puts "Error in assigning ports"
        ixNet exec newConfig
    }

    puts "Clearing stats"
    ixNet exec clearStats
    after 3000

    puts "Clearing Neighbor Table"
    ixNet exec clearNeighborTable $vPort1
    ixNet exec clearNeighborTable $vPort2
    after 5000

    puts "Clearing Neighbor Table"
    ixNet exec clearNeighborTable $vPort1
    ixNet exec clearNeighborTable $vPort2
    after 5000

    puts "Release ports"
    ixNet exec releasePort $vPort1
    ixNet exec releasePort $vPort2

    puts "Connecting ports"
    ixNet exec connectPort $vPort1
    ixNet exec connectPort $vPort2

    puts "wait for 10 second"
    after 10000

    puts "Checking Discoved Neighbors on port1"
    set neighborsExpectedListP1 {1234:0:0:0:0:0:0:2 4321:0:0:0:0:0:0:2}
    set neighborsExpectedListP2 {1234:0:0:0:0:0:0:1 4321:0:0:0:0:0:0:1}

    set checkNeigbors [checkDiscoverNeighbor $vPort1 $neighborsExpectedListP1]
    if {$checkNeigbors == 1} {
        ixNetCleanUp
        return $FAILED
    }

    set completeStats {"Neighbor Solicitation Tx."  2 \
                       "Neighbor Solicitation Rx."  2 \
                       "Neighbor Advertisement Tx." 2 \
                       "Neighbor Advertisement Rx." 2}

    if {[checkAllProtocolStats $realPortsList "Global Protocol Statistics" \
        $completeStats]} {
        puts "Failure: In checking stats"
        ixNet exec newConfig
        return $FAILED
    } else {
        puts "Success: In checking stats"
    }

    #-------------------------------------------------------------------------#
    # PHASE 2: Neighbor solicitation also send during simulate link up/down   #
    #-------------------------------------------------------------------------#
    puts "Clearing stats"
    ixNet exec clearStats

    puts "Clearing Neighbor Table"
    ixNet exec clearNeighborTable $vPort1
    ixNet exec clearNeighborTable $vPort2
    after 5000

    puts "Simulating link Down"
    ixNet exec linkUpDn $vPort1 down
    ixNet exec linkUpDn $vPort2 down
    after 3000

    puts "Simulating link Up"
    ixNet exec linkUpDn $vPort1 up
    ixNet exec linkUpDn $vPort2 up

    log "Waiting for 20 seconds"
    after 20000

    puts "Checkiing neighbor on port 1"
    set checkNeigbors [checkDiscoverNeighbor $vPort1 \
                           $neighborsExpectedListP1]

    if {$checkNeigbors == 1} {
        ixNet exec newConfig
        return $FAILED
    }

    puts "Checkiing neighbor on port 2"
    set checkNeigbors [checkDiscoverNeighbor $vPort2 \
                           $neighborsExpectedListP2]

    if {$checkNeigbors == 1} {
        ixNet exec newConfig
        return $FAILED
    }

    set completeStats {"Neighbor Solicitation Tx."  2 \
                       "Neighbor Solicitation Rx."  2 \
                       "Neighbor Advertisement Tx." 2 \
                       "Neighbor Advertisement Rx." 2}

    if {[checkAllProtocolStats $realPortsList "Global Protocol Statistics" \
        $completeStats]} {
        puts "Failure: In checking stats"
        ixNet exec newConfig
        return $FAILED
    }

    ixNet exec newConfig
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action
