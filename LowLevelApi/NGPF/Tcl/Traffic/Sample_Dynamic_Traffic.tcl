################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mario Dicu $
#
#    Copyright © 1997 - 2015 by IXIA
#    All Rights Reserved.
#
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

#****************************************************************
namespace eval ::py {
       set ixTclServer 10.205.11.28
       set ixTclPort   8027
       set ports       {{10.205.11.84 9 1} {10.205.11.84 9 2}}
  }

************************************************************

package req IxTclNetwork

set config_file "config.IPv4_IPv6.ixncfg"

set PASSED 0
set FAILED 1
set SKIPPED 99

ixNet setSessionParameter setAttribute strict

proc waitForTrafficState {state {timeout 90}} {
    set traffic [ixNet getRoot]/traffic
    set count 0

    # all this if == started code is a half baked solution to prevent invalid behaviours when the traffic is
    # ment to stop by itself after few packets and the started state will never be noticed.
    if  {$state == "started"} {
        set tiList [ixNet getList $traffic trafficItem]
        foreach trItem $tiList {
            set confElList [ixNet getList $trItem configElement]
            foreach confEl $confElList {
                set trType [ixNet getAttr $confEl/transmissionControl -type]
                switch $trType {
                    "continuous"  {  }
                    "auto"    {  }
                    default   {
                        puts "$trType traffic type detected waiting a predefined 90 sec for traffic to start"
                        after 90000
                        return 0
                    }
                }
            }
        }
    }
}

proc printTrafficWarningsAndErrors {{tiList "Unused for now"}} {
    set traffic [ixNet getRoot]/traffic
    set it 0
    foreach trafficItem [ixNet getList $traffic trafficItem] {
        if {[ixNet getAttr $trafficItem -errors] != ""} {
            puts "$trafficItem > ERR > [ixNet getAttr $trafficItem -errors]"
            incr it
        }
        if {[ixNet getAttr $trafficItem -warnings] != ""} {
            puts "$trafficItem > WARN > [ixNet getAttr $trafficItem -warnings]"
            incr it
        }
    }
    if {$it == 0} {puts "Traffic had no errors nor warnings."}
    return 0
}
	
proc generateApplyTraffic {} {
    puts "using the procedure from 5.40TrafficCommonUtils.tcl"
    set flag 1
    set traffic [ixNet getRoot]/traffic
    
	# Generating Traffic
	puts "Generating the traffic..."
	foreach TI traffic {
		if {[::ixNet exec generate $TI] ne "::ixNet::OK"} {
			puts "Not able to generate the traffic.."
			printTrafficWarningsAndErrors
			return $flag
		}
    }
	
	ixNet setAttribute ::ixNet::OBJ-//traffic -refreshLearnedInfoBeforeApply false
	ixNet commit

    # Apply Traffic
    puts "Applying the traffic ...."
    if {[::ixNet exec apply $traffic] ne "::ixNet::OK"} {
        puts "Not able to apply the traffic.."
        printTrafficWarningsAndErrors
        return $flag
    }

    waitForTrafficState stopped

    puts "Traffic applied successfully ..."
    printTrafficWarningsAndErrors

    set flag 0
    return $flag
}


    #---------------------------------------------------------------------------
    # Connecting to client
    #---------------------------------------------------------------------------
    ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 7.20
    puts "connectToClient Successful"
    
    #---------------------------------------------------------------------------
    #Cleaning up all the existing configurations from client
    #---------------------------------------------------------------------------

    puts "Performing Client cleanup"
    if {[catch {ixNet exec newConfig} err] != 0} {
    error "Clean-up Failed: $err"
    }
    after 2000

    #---------------------------------------------------------------------------
    # load the ixncfg config file
    #---------------------------------------------------------------------------
    puts "\t- Loading ixncfg file ..."
    if  {[ixNet exec loadConfig [ixNet readFrom $config_file ]] != "::ixNet::OK"} {
    error "Loading IxNetwork config file FAILED "
    }
    
    #---------------------------------------------------------------------------
    # Remove the last used chassis in the config
    #---------------------------------------------------------------------------
    set chassis_list [ixNet getL [ixNet getRoot]/availableHardware chassis]
    if {[llength $chassis_list] != 0} {
        puts "Removing the chassis from the config"
        foreach chassis $chassis_list {
            ixNet remove $chassis
        }
        if {[catch {ixNet commit} err] != 0} {
            error "Commit Failed: $err"
        }
    }    
    
    #--------------------------------------------------------------------------- 
    # get the virtual port list and real port list
    #---------------------------------------------------------------------------
    # Assign real ports to virtual ports
    puts "Getting virtual ports ...."
    set vPorts [ixNet getList [ixNet getRoot] vport]
    set vPort1 [lindex $vPorts 0]
    set vPort2 [lindex $vPorts 1]
    
    puts "Assign virtual ports to real ports"
    set status [::ixTclNet::AssignPorts $::py::ports {} $vPorts force]
    puts "Assigned: $status"
        
    # Check if port assign was ok
    puts "Checking if Ports were assigned correctly"
    foreach port $vPorts {
        set vport_state [ixNet getAttribute $port -isAvailable]
        if {$vport_state != "true"} {
            if {[::ixNet exec connectPort $port] != "::ixNet::OK"} {
               error "Unable to connect $port"
            }
        }        
    }
    puts "Ports assigned."
    
	# #---------------------------------------------------------------------------
    # # Starting protocols and wait for protocols to be started
    # #---------------------------------------------------------------------------

	puts "Starting protocols"
    catch {ixNet exec startAllProtocols} result1
    if {$result1 != "::ixNet::OK"} {
       error "FAILED : Starting Protocol"
    }
	after 60000
	
	# #---------------------------------------------------------------------------
    # # Marking the fields for on the fly change
    # #---------------------------------------------------------------------------
	
	set TI [ixNet getL [ixNet getRoot]/traffic trafficItem]
	set Traffic [ixNet getL / traffic]
	set i 1
	foreach IndTI $TI {
		set TIname [ixNet getA $IndTI -name] 
		set stream [ixNet getL $IndTI highLevelStream]
		foreach Indstream $stream {
			set streamname [ixNet getA $Indstream -name]
			set stck [ixNet getL $Indstream stack]
			foreach Indstck $stck {
				set stackname [ixNet getA $Indstck -displayName]
				if {$stackname == "Ethernet II"} {
					set fld [ixNet getL $Indstck field]
					set DstMAC [lindex $fld 0]
					ixNet setA $DstMAC -onTheFlyMask ffffffffffff
				}
				if {[string match *IPv4* $stackname] == 1} {
					set fld [ixNet getL $Indstck field]
					set Identification [lindex $fld 18]
					set DstIP [lindex $fld 27]
					ixNet setA $Identification -onTheFlyMask ffff
					ixNet setA $DstIP -onTheFlyMask 100000000
				}
				if {[string match *IPv6* $stackname] == 1} {
					set fld [ixNet getL $Indstck field]
					set HopLimit [lindex $fld 5]
					set DstIP6 [lindex $fld 7]
					ixNet setA $HopLimit -onTheFlyMask ff
					ixNet setA $DstIP6 -onTheFlyMask ffffffffffffffffffffffffffffffff
				}
				
				puts "\n"
			} 
		}
	}
	ixNet commit
	ixNet exec applyOnTheFlyTrafficChanges $Traffic	
	
		
	# #---------------------------------------------------------------------------
	# # Generate and Apply traffic                                               #
	# #---------------------------------------------------------------------------
	
	set root [ixNet getRoot]
	set traffic $root/traffic

	if {[generateApplyTraffic]} {
		error "Failed to Generate and Apply traffic"
	}
	
	after 30000
	
	
	#---------------------------------------------------------------------------
	# Start traffic
	#---------------------------------------------------------------------------
	
	puts "Starting Traffic ..."
	set startTraffic [catch {::ixNet exec startStatelessTraffic $traffic} errMsg]
	if {$startTraffic} {
		catch returned 1 if error in starting traffic.
		error "$errMsg"
		return $flag
	}
	puts "Traffic started successfully !!!"
	
	set count 0
	puts "Waiting for traffic to start (Checking Traffic State) ..."
	while { [ixNet getAttr $traffic -state] != "started" } {
		puts "isStarted --> [ixNet getAttr $traffic -state]"
		after 1000
		incr count
		if { $count > 60 } {
			error "Waited for 1 min, Traffic still not started.. "
		}
	}
	puts "Traffic started successfully ...(in $count sec)"

	after 15000	
	
	#################################################################################
	#   Changing Header Fields On The Fly                                           #
	#################################################################################
	
	set TI [ixNet getL [ixNet getRoot]/traffic trafficItem]
	set Traffic [ixNet getL / traffic]
	set i 1
	foreach IndTI $TI {
		set TIname [ixNet getA $IndTI -name] 
		set stream [ixNet getL $IndTI highLevelStream]
		foreach Indstream $stream {
			set streamname [ixNet getA $Indstream -name]
			set stck [ixNet getL $Indstream stack]
			foreach Indstck $stck {
				set stackname [ixNet getA $Indstck -displayName]
				if {$stackname == "Ethernet II"} {
					set fld [ixNet getL $Indstck field]
					set DstMAC [lindex $fld 0]
					ixNet setA $DstMAC -valueList [list 10:00:$i:00:00:01  10:00:[expr $i+1]:00:00:01]
				}
				if {[string match *IPv4* $stackname] == 1} {
					set fld [ixNet getL $Indstck field]
					set Identification [lindex $fld 18]
					set DstIP [lindex $fld 27]
					ixNet setA $Identification -singleValue 120
					ixNet setA $DstIP -valueList [list 30.0.$i.1  30.0.[expr $i+1].1]
				}
				if {[string match *IPv6* $stackname] == 1} {
					set fld [ixNet getL $Indstck field]
					set HopLimit [lindex $fld 5]
					set DstIP6 [lindex $fld 7]
					ixNet setA $HopLimit -singleValue 120
					ixNet setA $DstIP6 -valueList [list 9000:0:$i:0:0:0:0:1  9000:0:[expr $i+1]:0:0:0:0:1]
				}
				
				puts "\n"
			} 
		}
	}
	ixNet commit
	ixNet exec applyOnTheFlyTrafficChanges $Traffic
	
	
	#################################################################################
	#   Verification of changed fields on the fly                                   #
	#################################################################################
	
	set TI [ixNet getL [ixNet getRoot]/traffic trafficItem]
	set Traffic [ixNet getL / traffic]
	set i 1
	foreach IndTI $TI {
		set TIname [ixNet getA $IndTI -name] 
		set stream [ixNet getL $IndTI highLevelStream]
		foreach Indstream $stream {
			set streamname [ixNet getA $Indstream -name]
			set stck [ixNet getL $Indstream stack]
			foreach Indstck $stck {
				set stackname [ixNet getA $Indstck -displayName]
				if {$stackname == "Ethernet II"} {
					set fld [ixNet getL $Indstck field]
					set DstMAC [lindex $fld 0]
					set Destination [ixNet exec getLearntInfo $DstMAC]
					puts "Destination address after OTF changes are ... $Destination"
				}
				if {[string match *IPv4* $stackname] == 1} {
					set fld [ixNet getL $Indstck field]
					set Identification [lindex $fld 18]
					set DstIP [lindex $fld 27]
					set Ident [ixNet getA $Identification -fieldValue]
					set DestinationIP [ixNet exec getLearntInfo $DstIP] 
					puts "Identification value after OTF is ... $Ident"
					puts "Destination IP's after OTF changes are ... $DestinationIP"
				}
				if {[string match *IPv6* $stackname] == 1} {
					set fld [ixNet getL $Indstck field]
					set HopLimit [lindex $fld 5]
					set DstIP6 [lindex $fld 7]
					set hoplimit [ixNet getA $HopLimit -fieldValue]
					set DestinationIP6 [ixNet exec getLearntInfo $DstIP6]
					puts "Hoplimit after OTF change is ... $hoplimit"
					puts "Destination IP after OTF changes are ... $DestinationIP6"
				}
				
				puts "\n"
			} 
		}
	}
	
	
########################
####### TEST BODY END
########################    

puts "Cleaning up the client: "

puts "    2. Stopping protocols"
catch {ixNet exec stopAllProtocols} result2
if {$result2 != "::ixNet::OK"} {
   error "FAILED : Stopping Protocol"
}
after 5000

puts "    3. Performing New Config"
if {[catch {ixNet exec newConfig} err] != 0} {
    error "Clean-up Failed: $err"
}
after 2000    
    
puts "DONE"
        
return $PASSED