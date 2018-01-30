#------------------------------------------------------------------------------
# Name          : test.SampleScript_QuickStreams_UDFs.tcl
# Author        : Deepak Kumar Singh
# Purpose       : Verifying UDFs for Quick Streams in various mode.
# Code Flow     : 1. Configure IXIA Ports
#                 2. Apply Traffic
#                 3. Verify Traffic Config in IxNetwork/IxExplorer
#                 4. Start Traffic and Wait for sometime
#                 5. Stop Traffic and verify Traffic Stats
#                 6. Disable Ingress Tracking and enable Capture Mode
#                 7. Apply Traffic and Start Capture
#                 8. Start Traffic and Wait for sometime
#                 9. Stop Traffic and Stop Capture
#		          10. Verify UDF Patterns in Captured Packets
#		          11. Clean IXIA Ports
# Test Setup    : B2B
# ixncfg used   : Yes (config.SampleScript_QuickStreams_UDFs.ixncfg)
# Scriptgen used: No
#------------------------------------------------------------------------------

source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/TestRun/config.tcl

#-------------------------------------------------------------------------------
# PROCEDURE  : checkDetailTrafficConfiguration
# PURPOSE    : Checking Traffic Wizard Configuration in IxNetwork
# PARAMETERS : None
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkDetailTrafficConfiguration {} {
    set error 1

	# Checking various attributes of QFG 1
    set top [ixNet getRoot]	
	set trafficItemList [ixNet getList $top/traffic trafficItem]
    set trafficItem1 [lindex $trafficItemList 0]
    set hltList [ixNet getList $trafficItem1 highLevelStream] 

	log "Verifying various attributes of QFG 1" 	
    set hlt1 [lindex $hltList 0]
    set udfList [ixNet getList $hlt1 udf]
	
	# Checking UDF1 attributes of QFG 1
	log "Verifying UDF1 attributes of QFG 1 ....."
    set udf1 [lindex $udfList 0]  
    if {[checkAttributeValue $udf1 {enabled True \
	                                byteOffset 32 \
									chainedFromUdf none \
                                    type counter}] == 1} {
		log "UDF1 attributes for QFG 1 are not proper !!!"
        return $error
    }
    if {[checkAttributeValue $udf1/counter {width 32 \
	                                        bitOffset 0 \
	                                        startValue 286331153 \
	                                        count 10 \
											stepValue 2 \
											direction increment}] == 1} {
		log "UDF1 attributes for QFG 1 are not proper !!!"
        return $error
    }
    log "UDF1 attributes for QFG 1 are proper !!!"
	
	# Checking UDF2 attributes of QFG 1
	log "Verifying UDF2 attributes of QFG 1 ....."
    set udf2 [lindex $udfList 1]  
    if {[checkAttributeValue $udf2 {enabled True \
	                                byteOffset 36 \
									type valueList}] == 1} {
		log "UDF2 attributes for QFG-1 are not proper !!!"
        return $error
    }
    if {[checkAttributeValue $udf2/valueList {width 32 \
	                                          startValueList "2863311530 3149642683 3435973836"}] == 1} {
		log "UDF2 attributes for QFG 1 are not proper !!!"
        return $error
    }
    log "UDF2 attributes for QFG 1 are proper !!!"
	
	# Checking UDF3 attributes of QFG 1
	log "Verifying UDF3 attributes of QFG 1 ....."
    set udf3 [lindex $udfList 2]  
    if {[checkAttributeValue $udf3 {enabled True \
	                                byteOffset 40 \
                                    type rangeList}] == 1} {
		log "UDF3 attributes for QFG-1 are not proper !!!"
        return $error
    }
    if {[checkAttributeValue $udf3/rangeList {width 32 \
	                                          startValueCountStepList "286331153 3 4 572662306 4 3"}] == 1} {
		log "UDF3: Rangelist attributes for QFG 1 are not proper !!!"
        return $error
    }
    log "UDF3 attributes for QFG 1 are proper !!!"
	
	# Checking UDF4 attributes of QFG 1
	log "Verifying UDF4 attributes of QFG 1 ....."
    set udf4 [lindex $udfList 3]  
    if {[checkAttributeValue $udf4 {enabled True \
	                                byteOffset 44 \
                                    type nestedCounter}] == 1} {
		log "UDF4 attributes for QFG-1 are not proper !!!"
        return $error
    }
    if {[checkAttributeValue $udf4/nestedCounter {width 32 \
	                                              startValue 286331153 \
												  innerLoopRepeatValue 2 \
												  innerLoopIncrementBy 2 \
	                                              innerLoopLoopCount 2 \
												  outerLoopIncrementBy 2 \
                                                  outerLoopLoopCount 3}] == 1} {
		log "UDF4: Nested Counter attributes for QFG 1 are not proper !!!"
        return $error
    }
    log "UDF4 attributes for QFG 1 are proper !!!"
	
	# Checking UDF5 attributes of QFG 1
	log "Verifying UDF5 attributes of QFG 1 ....."
    set udf5 [lindex $udfList 4]  
    if {[checkAttributeValue $udf5 {enabled True \
	                                byteOffset 52 \
                                    type ipv4}] == 1} {
		log "UDF4 attributes for QFG-1 are not proper !!!"
        return $error
    }
    if {[checkAttributeValue $udf5/ipv4 {width 32 \
	                                     startValue 286331153 \
										 skipValues False \
	                                     innerLoopLoopCount 2 \
                                         innerLoopIncrementBy 2 \
                                         outerLoopLoopCount 5}] == 1} {
		log "UDF5: IPv4 attributes for QFG 1 are not proper !!!"
        return $error
    }
    log "UDF5 attributes for QFG 1 are proper !!!"
	
	# Checking Table UDF attributes of QFG 1
	log "Verifying Table UDF attributes of QFG 1 ....."   
    if {[checkAttributeValue $hlt1/tableUdf {enabled True}] == 1} {
		log "Table UDF attributes for QFG 1 are not proper !!!"
        return $error
    }
	set columnList [ixNet getList $hlt1/tableUdf column] 
	set column1 [lindex $columnList 0]
    if {[checkAttributeValue $column1 {offset 448 \
									   size 4 \
									   format hex \
									   values "aaaaaaaa bbbbbbbb cccccccc"}] == 1} {
		log "Table UDF: Column1 attributes for QFG 1 are not proper !!!"
        return $error
    }
	set column2 [lindex $columnList 1]
    if {[checkAttributeValue $column2 {offset 480 \
									   size 6 \
									   format mac \
									   values "111111111111 222222222222 333333333333"}] == 1} {
		log "Table UDF: Column2 attributes for QFG 1 are not proper !!!"
        return $error
    }
    log "Table UDF attributes for QFG 1 are proper !!!"
	
	# Checking various attributes of QFG 2     
	log "Verifying various attributes of QFG 2" 	
    set hlt2 [lindex $hltList 1]
    set udfList [ixNet getList $hlt2 udf]
	
	# Checking UDF1 attributes of QFG 2
	log "Verifying UDF1 attributes of QFG 2 ....."
    set udf1 [lindex $udfList 0]  
    if {[checkAttributeValue $udf1 {enabled True \
	                                byteOffset 48 \
                                    type random}] == 1} {
		log "UDF1 attributes for QFG 2 are not proper !!!"
        return $error
    }
    if {[checkAttributeValue $udf1/random {width 32}] == 1} {
		log "UDF1: Random attributes for QFG 2 are not proper !!!"
        return $error
    }
    log "UDF1 attributes for QFG 2 are proper !!!"	
}

#-------------------------------------------------------------------------------
# PROCEDURE  : checkDetailTrafficConfigurationInIxExplorer
# PURPOSE    : Proc for checking Traffic Wizard Configuration in IxExplorer
# PARAMETERS : None
# RETURN     : (BOOL)    - 0 for Pass ~ 1 for Fail
#-------------------------------------------------------------------------------
proc checkDetailTrafficConfigurationInIxExplorer {chassisIp card port numStream} {
    set error 1
	
	log "Connecting to the Chassis $chassisIp ....."
    if {[ixExplorerConnectChassis $chassisIp $card $port] == 1} {        
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }
    log "Connect to the Chassis $chassisIp successfully !!!"

    if {[chassis get $chassisIp]} {
        log "Not able to get the chassis object of IxOS !!!"
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }
    set chassisId [chassis cget -id]

    # Verifying IxExplorer port attributes configured from IxNetwork Quick Stream
    log "Verifying IxExplorer port attributes configured from IxNetwork Quick Stream ....."
    if {[port get $chassisId $card $port]} {
        log "Not able to get the port object through IxTclHal !!!"
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }

    # Enum value for Tx Mode- Sequential (Packet Streams) is 0
    if {[ixExplorerCheckAttributeValue port {transmitMode 0}] == 1} {
        log "Traffic Config is not correct !!!"
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }

    # Verifying IxExplorer stream attributes configured from IxNetwork Quick Stream
    log "Verifying number of IxExplorer stream configured from IxNetwork Quick Stream ....."
    set streamId 1
    while {$streamId <= $numStream} {
        if {[stream get $chassisId $card $port $streamId]} {
            break
        }
        incr streamId
    }
    log "IxExplorer :: Stream  Count [expr $streamId -1] (Expected : $numStream)"
    if {[expr $streamId -1] != $numStream} {
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }

    log "Verifying configurations for stream 1 ....."

    set streamId 1
    if {[stream get $chassisId $card $port $streamId]} {
        log "Not able to get the stream object of IxOS !!!"
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }

    # Enum value for Frame Size- Fixed is 0
    # Enum value for Payload Type (Data Pattern)- Increment Byte is 0
    if {[ixExplorerCheckAttributeValue stream {framesize 100 \
											   frameSizeType 0 \
											   patternType 0}] == 1} {
        log "Traffic Config is not correct"
        ixExplorerDisconnectChassis $chassisIp
        return $error
    }

    log "IxExplorer stream attributes configured from IxNetwork Quick Stream are correct !!!"  

    ixExplorerDisconnectChassis $chassisIp

    set error 0
    return $error
}

proc Action {portData1 portData2} {
    # Initialize return value
    set FAILED 1
    set PASSED 0
	
	# Get IXIA Ports Info     
    set chassisIp1 [lindex $portData1 0]
    set card1      [lindex $portData1 1]
    set port1      [lindex $portData1 2]
    set client1    [lindex $portData1 3]
    set tcpPort1   [lindex $portData1 4]
    
    set chassisIp2 [lindex $portData2 0]
    set card2      [lindex $portData2 1]
    set port2      [lindex $portData2 2]
    set client2    [lindex $portData2 3]
    set tcpPort2   [lindex $portData2 4]
	
	set version "5.40"

    # Connect to IxNetwork TCL-Server/Client
    if {$client1 == $client2} {  
        log "Connecting to client $client1"
        if {[ixNet connect $client1 -port $tcpPort1 -version $version] != "::ixNet::OK"} {
            log "Unable to connect to IxNetwork Tcl Server !!!"
			ixNetCleanUp
			return $FAILED
        }
    } else {
        log "Use the same client !!!"
	    ixNetCleanUp
	    return $FAILED
    }
    log "Connection to the Client successful !!!"

    # Clean up all the existing configurations from the client
    log "Cleaning up the Client ....."
    ixNetCleanUp    
	log "Client is cleaned up successfully !!!"
	after 5000

    # Load the Test Config
    log "Now we configure the Ixia ports from the config file !!!"    
    log "Loading ixncfg file ....."
	set configFileName "config.SampleScript_QuickStreams_UDFs.ixncfg"
	set configFile [ixNet readFrom "$::pwd/$configFileName"]
    if {[ixNet exec loadConfig $configFile] != "::ixNet::OK"} {
        log "Loading IxNetwork config file : FAILED"
        ixNetCleanUp
        return $FAILED
    } 
    log "Loading IxNetwork config file : PASSED" 

    # Get Real Port List
    set realPortsList [list [list $chassisIp1 $card1 $port1] \
                            [list $chassisIp2 $card2 $port2]]
	log "Real Ports are = $realPortsList"

    # Get Virtual Ports
    log "Getting virtual ports ....."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    log "Virtual ports are = $vPorts"

    # Assign virtual ports to real ports
    log "Assigning virtual ports to real ports ....."    
    set assignStatus [ixTclNet::AssignPorts $realPortsList {} $vPorts force]
    log "Assigned: $assignStatus"
    if {[string equal [lindex $assignStatus 0] $vPort1] != 1 || \
        [string equal [lindex $assignStatus 1] $vPort2] != 1} {
		log "Ports are not assigned !!!"
        ixNetCleanUp
        return $FAILED
    } 
    log "Ports are assigned successfully !!!"	
	
	# Check if the ports are assigned; if un-assigned re-assign them   
	if {[ifUnassignedConnectAgain] == 1} {
		log "Not able to re-assign the ports !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Ports are in assigned state !!!"
	
	# Check Ports Link Status
    log "Checking Port Link Status ....."
    if {[ixTclNet::CheckLinkState $vPorts doneList]} {  
        log "Ports Link is down !!!"	
        ixNetCleanUp
        return $FAILED
    }   
    log "Ports Link is Up !!!"	
	after 5000

    # Start Test Execution	
	log "Test execution Starts !!!"		
	
    # Generate and Apply  Traffic 
    if {[generateApplyTraffic] == 1} {
        log "Failed to start traffic !!!"
        #ixNetCleanUp
        return $FAILED
    }
    log "Traffic applied successfully !!!"	

	#--------------------------------------------#
	#  Verification of Traffic Configuration
	#--------------------------------------------# 
	log "Verifying Traffic configuration ....."
	
	# Check High Level Stream or Flow Groups Count
	log "Verifying no. of HL Streams ....."
	if {[checkHighLevelSteamCountForAllTrafficItem 1 {0 2}] == 1} {
		log "Traffic Config is not correct"
		ixNetCleanUp
		return $FAILED
	}
	log "No. of HL Streams generated is correct !!!"		
	
	# Check Traffic Config in IxNetwork
	log "Verifying Traffic Configuration in IxNetwork ....."
	if {[checkDetailTrafficConfiguration] == 1} {
		log "Traffic Config is not correct in IxNetwork !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic Config in IxNetwork is correct !!!"

	# Check Traffic Config in IxExplorer
	log "Verifying Traffic configuration from IxExplorer ....."
	if {[checkDetailTrafficConfigurationInIxExplorer $chassisIp1 $card1 $port1 2] == 1} {
		log "Traffic Config is not correct in IxExplorer !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic configuration in IxExplorer is correct !!!"

	#-------------------------------------------------#
	#  Test Part 4: Verification of Traffic Stats
	#-------------------------------------------------#  
	# Start Traffic
	log "Starting Traffic ....."
	set traffic [ixNet getRoot]/traffic
	if {[startTraffic $traffic] == 1} {
		log "Failed to start Traffic"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic started successfully !!!"

	log "Waiting for 15 secs for the traffic to flow ....."
	after 15000

	# Stop Traffic
	log "Stopping Traffic ....."
	if {[stopTraffic $traffic] == 1} {
		log "Failed to stop traffic"
		ixNetCleanUp
		return $FAILED
	}		
	log "Traffic stopped successfully !!!"	
	after 5000	
	
	set tolerance 5
	
	# Check Data Plane Port Statistics
	log "Verifying Data Plane Port Statistics ....."        
	set txPortList [subst {{[ixNet getAttr $vPort1 -name]} }]
	set rxPortList [subst {{[ixNet getAttr $vPort2 -name]} }]		
	if {[checkAllPortTrafficStats "Data Plane Port Statistics" $txPortList $rxPortList $tolerance] == 1} {
		log "Did not get the expected value for Data Plane Port Statistics !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Data Plane Port Statistics is correct !!!"
   
	# Check Traffic Item Statistics
	log "Verifying Traffic Item Statistics ....."
	if {[checkAllTrafficStats "Traffic Item Statistics" $tolerance] == 1} {
		log "Did not get the expected value for Traffic Item Statistics !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic Item Statistics is correct !!!"

	# Check Flow Statistics
	log "Verifying Flow Statistics ....."
	if {[checkAllTrafficStats "Flow Statistics" $tolerance] == 1} {
		log "Did not get the expected value for Flow Statistics !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Flow Statistics is correct !!!"   
	
	#-------------------------------------------------#
	#  Test Part 5: Verification of Packet Structure
	#-------------------------------------------------#     
	log "Verifying Captured Packets ....."
	
	# Disable Ingress Tracking
	log "Disabling ingress tracking ....."
	set top [ixNet getRoot]
	set traffic $top/traffic 		
	set trafficItemList [ixNet getList $traffic trafficItem]
	set trafficItem1 [lindex $trafficItemList 0]	
	if {[setAndCheckAttributeValue $trafficItem1/tracking trackBy {"" y}] == 1} {
		ixNetCleanUp
		return $FAILED
	}
	log "Disabled Ingress Tracking successfully !!!"
	
	# Enable Capture Mode
	log "Enabling Capture Mode ....."
	if {[enableCaptureMode $vPort2] == 1} {
		log "Failed to enable Capture Mode !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Capture Mode enabled successfully !!!"
	after 5000
	
	# Traffic Apply	        
	if {[generateApplyTraffic] == 1} {
		log "Failed to apply traffic !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic applied successfully !!!"
	after 5000

	# Start Capture
	log "Starting the capture"
	if {[ixNet exec startCapture] != "::ixNet::OK"} {
		log "Failed to start packet capture !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Capture started successfully !!!"
	after 5000
	
	# Start Traffic        
	log "Starting Traffic ....."
	if {[startTraffic $traffic] == 1} {
		log "Failed to start the traffic"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic started successfully !!!"
	
	log "Waiting for 15 secs for the traffic to flow ....."
	after 15000
	
	# Stop Traffic
	log "Stopping Traffic ....."		
	if {[stopTraffic $traffic] == 1} {
		log "Failed to stop the traffic"
		ixNetCleanUp
		return $FAILED
	}
	log "Traffic stopped successfully !!!"
	after 5000
	
	# Stop Capture
	log "Stopping the capture"
	if {[ixNet exec stopCapture] != "::ixNet::OK"} {
		log "Failed to stop packet capture !!!"
		ixNetCleanUp
		return $FAILED
	}
	log "Capture stopped successfully !!!"
	after 5000
	
	#---------------------------------------#
	#       Verify Counter UDF
	#---------------------------------------#
	log "Verifying Counter UDF ....."
	
	# Get Timestamps of desired Captured Packets		
	set j 17; # Decimal Value of Hex 11
	for {set i 1} {$i <= 10} {incr i} {
		set pattern [list 32 35 "11 11 11 [format %0.2X $j]"]
		incr j 2
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern]
	}        

	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 9} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			log "Counter UDF Patterns not in correct sequence !!!"
			ixNetCleanUp
			return $FAILED
		}
	}	

	log "Counter UDF is working properly !!!"

	#---------------------------------------#
	#       Verify Valuelist UDF
	#---------------------------------------#		
	log "Verifying Valuelist UDF ....."
	
	# Get Timestamps of desired Captured Packets	
	set j 170; # Decimal Value of Hex AA
	for {set i 1} {$i <= 3} {incr i} {
		set pattern [list 36 39 "[format %0.2X $j] [format %0.2X $j] [format %0.2X $j] [format %0.2X $j]"]
		incr j 17; # Decimal Value of Hex 11
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern]
	}        

	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 2} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			log "Valuelist UDF Patterns not in correct sequence !!!"
			ixNetCleanUp
			return $FAILED
		}
	}	

	log "Valuelist UDF is working properly !!!"

	#---------------------------------------#
	#       Verify Rangelist UDF
	#---------------------------------------#		
	log "Verifying Rangelist UDF ....."
	
	# Verify the 1st List
	# Get Timestamps of desired Captured Packets		
	set j 17; # Decimal Value of Hex 11
	for {set i 1} {$i <= 3} {incr i} {
		set pattern [list 40 43 "11 11 11 [format %0.2X $j]"]
		incr j 4
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern]
	}        

	# Verify Sequence of UDF Patterns
	for {set i 1} {$i <= 2} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			log "Rangelist UDF Patterns not in correct sequence !!!"
			ixNetCleanUp
			return $FAILED
		}
	}        
	
	# Verify the 2nd List
	# Get Timestamps of desired Captured Packets	
	set j 34; # Decimal Value of Hex 22
	for {set i 1} {$i <= 4} {incr i} {
		set pattern [list 40 43 "22 22 22 [format %0.2X $j]"]
		incr j 3
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern]
	}        

	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 3} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			log "Rangelist UDF Patterns not in correct sequence !!!"
			ixNetCleanUp
			return $FAILED
		}
	}	

	log "Rangelist UDF is working properly !!!"	       

	#---------------------------------------#
	#       Verify Nested Counter UDF
	#---------------------------------------#		
	log "Verifying Nested Counter UDF ....."
	
	# Get Timestamps of desired Captured Packets		
	set j 17; # Decimal Value of Hex 11
	for {set i 1} {$i <= 6} {incr i} {
		set pattern [list 44 47 "11 11 11 [format %0.2X $j]"]
		incr j 2
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern 2]
	}        

	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 5} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			log "Nested Counter UDF Patterns not in correct sequence !!!"
			ixNetCleanUp
			return $FAILED
		}
	}	

	log "Nested Counter UDF is working properly !!!"

	#---------------------------------------#
	#          Verify IPv4 UDF
	#---------------------------------------#		
	log "Verifying IPv4 UDF ....."
	
	# Get Timestamps of desired Captured Packets		
	set j 17; # Decimal Value of Hex 11
	for {set i 1} {$i <= 5} {incr i} {
		set pattern [list 52 55 "11 11 11 [format %0.2X $j]"]
		incr j 2
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern 2]
	}        

	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 4} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			log "IPv4 UDF Patterns not in correct sequence !!!"
			ixNetCleanUp
			return $FAILED				 
		}
	}	

	log "IPv4 UDF is working properly !!!"

	#---------------------------------------#
	#          Verify Table UDF
	#---------------------------------------#			
	log "Verifying Table UDF ....."
	
	# Verify 1st Column of Table UDF
	# Get Timestamps of desired Captured Packets		
	set j 170; # Decimal Value of Hex AA
	for {set i 1} {$i <= 3} {incr i} {
		set pattern [list 56 59 "[format %0.2X $j] [format %0.2X $j] [format %0.2X $j] [format %0.2X $j]"]
		incr j 17; # Decimal Value of Hex 11
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern]
	}
	
	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 2} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			 puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			 ixNetCleanUp
			 log "Table UDF Patterns not in correct sequence !!!"
			 break
		}
	}

	# Verify 2nd Column Table UDF
	# Get Timestamps of desired Captured Packets		
	set j 11
	for {set i 1} {$i <= 3} {incr i} {
		set pattern [list 60 65 "$j $j $j $j $j $j"]
		incr j 11
		set timeStamp($i) [ReturnTimestamp $chassisIp2 $card2 $port2 $pattern]
	}
	
	# Verify Sequence of Captured Packets
	for {set i 1} {$i <= 2} {incr i} {
		set j [expr $i+1]
		if {$timeStamp($i) >= $timeStamp($j)}  {
			 puts "break timeStamp($j) = $timeStamp($j) timeStamp($i) = $timeStamp($i)"
			 break
			 ixNetCleanUp
			 log "Table UDF Patterns not in correct sequence !!!"
		}
	}		

	log "Table UDF is working properly !!!"	
	
	#---------------------------------------#
	#          Verify Random UDF
	#---------------------------------------#		
	log "Verifying Random UDF ....."
	
	set pattern {48 48 "AB"}        
	if {[verifyCapturedPackets $chassisIp2 $card2 $port2 $pattern] == 1} {
		log "Random UDF is not working properly !!!"
		ixNetCleanUp
		return $FAILED
	}        

	log "Random UDF is working properly !!!"    

	# End Test Execution
	log "Various UDF Modes for Quick Streams are working fine !!!"	
	log "Test execution Ends !!!"  

    ixNetCleanUp
    return $PASSED
}

#------------------------------------------------------------------------------#
# Execute the Action procedure defined above                                   #
#------------------------------------------------------------------------------#
Execute_Action
