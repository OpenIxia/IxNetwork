#py> TOPOLOGY: b2b-1G
#py> TIMEOUT: 900
# HARNESS VARS ****************************************************************
# comment out these lines when harness runs this test
#


namespace eval ::cfg {}
set ::cfg::hltapi_p2no_hltset HLTSET142
set env(IXIA_VERSION) $::cfg::hltapi_p2no_hltset 

namespace eval ::py {
    set ixTclServer {localhost}
    set ixTclPort   8009
    set ports       {{10.205.15.88 1 1} {10.205.15.88 1 2} {10.205.15.88 2 1} {10.205.15.88 2 2}}
}

if {[catch {package require Ixia} retCode]} {
    puts "FAIL - [info script] - $retCode"
    return 0
}

set PASSED 0
set FAILED 1

proc log {a} {puts $a}

# Procedure for comparing Protocols Summary Statistics
proc checkStats {statList expList} {
    proc logPass {expStName stVal op expStVal {tlr "-"}} {
        set fmt "%-35s %10.2f %2s %10.2f %5s ...Passed"
        log [format $fmt $expStName $stVal $op $expStVal $tlr]
        update idletasks
    }

    proc logFail {expStName stVal op expStVal {tlr "-"}} {
        set fmt "%-35s %10.2f %2s %10.2f %5s ...FAILED"
        log [format $fmt $expStName $stVal $op $expStVal $tlr]
        update idletasks
    }

    set retFlag 1
    if {[llength $statList] == 0} {
        return -code error "Empty Statistics list!"
    }

    set someFail false
    foreach stItem $statList expItem $expList {
        if {$expItem == ""} {continue}        ;# skip if exp list is shorter than stat list 

        set fmt "%-35s %10s %2s %10s %5s"
        set header [format $fmt [lindex $expItem 0] "RETURNED" "" "EXPECTED" "TOL"] 
        log $header
        log "[string repeat "-" [expr [string length $header] + 10]]"
        array set tmpVal [lindex $stItem 1]
        set missingStats {}
        foreach {expStName op expStVal} [lindex $expItem 1] {
            unset -nocomplain tolerance                         ;# reset any prev tolerance
            if {[llength $expStVal] == 2} {                     ;# for tolerance
                foreach {expStVal tolerance} $expStVal break    ;# idiomatic form instead of 2 lindex ops
            }
            if {![string is double -strict $expStVal]} {continue} ;# skip strings values
            if {[catch {
                if {![string is double -strict $tmpVal($expStName)]} {
                    set tmpVal($expStName) -1        ;# set to something bad if empty
                }}]} {lappend missingStats $expStName; continue}

            switch -- $op {
                "=" {if {$tmpVal($expStName) == $expStVal} {
                        logPass $expStName $tmpVal($expStName) $op $expStVal
                        set retFlag 0
                    } elseif {[info exists tolerance] && $tolerance != ""} {    ;# tolerance case
                        set minExp [expr $expStVal - abs($expStVal) * $tolerance]
                        set maxExp [expr $expStVal + abs($expStVal) * $tolerance]

                        if {$tmpVal($expStName) >= $minExp && $tmpVal($expStName) <= $maxExp} {
                            logPass $expStName $tmpVal($expStName) $op $expStVal $tolerance
                            set retFlag 0
                        } else {
                            logFail $expStName $tmpVal($expStName) $op $expStVal $tolerance
                            set someFail true
                        }
                    } else {
                        logFail $expStName $tmpVal($expStName) $op $expStVal
                        set someFail true
                    }}
                "<" {if {$tmpVal($expStName) < $expStVal} {
                        logPass $expStName $tmpVal($expStName) $op $expStVal
                        set retFlag 0
                    } else {
                        logFail $expStName $tmpVal($expStName) $op $expStVal
                        set someFail true
                    }}
                ">" {if {$tmpVal($expStName) > $expStVal} {
                        logPass $expStName $tmpVal($expStName) $op $expStVal
                        set retFlag 0
                    } else {
                        logFail $expStName $tmpVal($expStName) $op $expStVal
                        set someFail true
                    }}
                ">=" {if {$tmpVal($expStName) >= $expStVal} {
                        logPass $expStName $tmpVal($expStName) $op $expStVal
                        set retFlag 0
                    } else {
                        logFail $expStName $tmpVal($expStName) $op $expStVal
                        set someFail true
                    }}
                "<=" {if {$tmpVal($expStName) <= $expStVal} {
                        logPass $expStName $tmpVal($expStName) $op $expStVal
                        set retFlag 0
                    } else {
                        logFail $expStName $tmpVal($expStName) $op $expStVal
                        set someFail true
                    }}
                "<>" {if {$tmpVal($expStName) >= $expStVal && $tmpVal($expStName) <= $tolerance} {  ;# use $expStVal as lower limit and
                        logPass $expStName $tmpVal($expStName) $op $expStVal $tolerance             ;# $tolerance as interval upper limit
                        set retFlag 0
                    } else {
                        logFail $expStName $tmpVal($expStName) $op $expStVal $tolerance
                        set someFail true
                    }}
                default {
                    set fmt "%-35s %10.2f %2s %10.2f %5s ...Ignored"
                    puts [format $fmt $expStName $tmpVal($expStName) $op $expStVal "-"]
                    set retFlag 0
                }
            }
        }

        if {[llength $missingStats] > 0} {
            return -code error "\nStatistics:\n[join $missingStats '\n']\nmissing from stat view!"
        }
        log "\n"
    }
    if {$someFail} {
        set retFlag 1            ;# some value hasn't matched
        return $retFlag            ;# this way we can see all mismatched stats in one pass
    } else {
        return $retFlag
    }
}

set test_name [info script]

set chassis_ip [lindex $::py::ports 0 0]
set port1 "[lindex $::py::ports 0 1]/[lindex $::py::ports 0 2]"
set port2 "[lindex $::py::ports 1 1]/[lindex $::py::ports 1 2]"
set port3 "[lindex $::py::ports 2 1]/[lindex $::py::ports 2 2]"
set port4 "[lindex $::py::ports 3 1]/[lindex $::py::ports 3 2]"
set port_list [list $port1 $port2 $port3 $port4]
set ixnetwork_tcl_server $::py::ixTclServer

# Connect to the chassis.
# When using P2NO HLTSET, for loading the IxTclNetwork package please 
# provide –ixnetwork_tcl_server parameter to ::ixia::connect
set connect_status [::ixiangpf::connect \
		-reset   \
		-interactive 			1  \
        -device                 $chassis_ip \
        -port_list              $port_list  \
		-ixnetwork_tcl_server   $ixnetwork_tcl_server  ]
if {[keylget connect_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget connect_status log]"
	return $FAILED
}

set port_handle [list]
foreach port $port_list {
    if {![catch {keylget connect_status port_handle.$chassis_ip.$port} \
            temp_port]} {
        lappend port_handle $temp_port
	}
}
set port_1 [lindex $port_handle 0]
set port_2 [lindex $port_handle 1]
set port_3 [lindex $port_handle 2]
set port_4 [lindex $port_handle 3]

puts "Wait 5 seconds ..."
after 5000
puts "Rebooting port(s)..."
set ret [::ixia::reboot_port_cpu \
    -port_list [list $port_handle]  \
]
if {[keylget ret status] != $::SUCCESS} {
    puts "FAIL - $test_name - Error while rebooting port: [keylget ret log]"
	return $FAILED
}

# Create Topologies
# # Topology 1 with Device Group 1 and Device Group 2
puts "Create Topology 1 with Device Group 1 and Device Group 2"
set topology1_status [::ixiangpf::topology_config 	\
	-topology_name            	"DHCPv4Server"     \
	-port_handle               	[list $port_1 $port_3]    	\
	-device_group_multiplier 	 	1		\
	]
	
# Verify that topology 1 with DG1 is created	
puts "Verify that topology 1 with DG1 is created"
if {[keylget topology1_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget topology1_status log]"
	return $FAILED
}

set deviceGroup_first_handle [keylget topology1_status device_group_handle]
set topology_first_handle [keylget topology1_status topology_handle]

set topology1_status [::ixiangpf::topology_config 	\
	-mode 						config   \
	-topology_handle   $topology_first_handle     \
	-device_group_multiplier 	 	1		\
	]	
	
# Verify that topology 1 with DG2 is created	
puts "Verify that topology 1 with DG2 is created"
if {[keylget topology1_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget topology1_status log]"
	return $FAILED
}

set deviceGroup_second_handle [keylget topology1_status device_group_handle]

# # Topology 2 with Device Group 3 and Device Group 4
puts "Create Topology 2 with Device Group 3 and Device Group 4"
set topology2_status [::ixiangpf::topology_config 	\
	-topology_name            	"DHCPv4Client"     \
	-port_handle               	[list $port_2 $port_4] 	\
	-device_group_multiplier 	 	15		\
	]
	
# Verify that topology 2 with DG3 is created	
puts "Verify that topology 2 with DG3 is created"
if {[keylget topology2_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget topology2_status log]"
	return $FAILED
}

set deviceGroup_third_handle [keylget topology2_status device_group_handle]
set topology_second_handle [keylget topology2_status topology_handle]

set topology2_status [::ixiangpf::topology_config 	\
	-mode 						config   \
	-topology_handle   $topology_second_handle     \
	-device_group_multiplier 	 	8		\
	]	

# Verify that topology 2 with DG4 is created	
puts "Verify that topology 2 with DG4 is created"
if {[keylget topology2_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget topology2_status log]"
	return $FAILED
}	

set deviceGroup_fourth_handle [keylget topology2_status device_group_handle]


# # Create DHCPv4 Server
puts "Create DHCPv4 Server 1"
set dhcp_server_status [::ixiangpf::emulation_dhcp_server_config 	\
		-handle					$deviceGroup_first_handle 	\
		-lease_time                 			86400   	     		\
		-ipaddress_count			15			\
		-ip_dns1				10.10.10.10		\
		-ip_dns1_step				0.0.0.1			\
		-ip_dns2				20.20.20.20		\
		-ip_dns2_step				0.0.1.0			\
		-ipaddress_pool				154.1.0.2	\
		-ipaddress_pool_step			0.0.0.1			\
		-ipaddress_pool_prefix_length 		16			\
		-ip_address					154.1.0.1 \
		-ip_prefix_length			16 \
		-vlan_id						100			\
		-protocol_name				"DHCPv4Server1" \
	]

# Verify that DHCPv4 Server 1 is created
puts "Verify that DHCPv4 Server 1 is created"
if {[keylget dhcp_server_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_server_status log]"
	return $FAILED
}	 

set dhcp_server1 [keylget dhcp_server_status dhcpv4server_handle]

puts "Create DHCPv4 Server 2"
set dhcp_server_status [::ixiangpf::emulation_dhcp_server_config 	\
		-handle					$deviceGroup_second_handle 	\
		-lease_time                 			86400   	     		\
		-ipaddress_count			10			\
		-ip_dns1				30.30.30.30		\
		-ip_dns1_step				0.0.0.1			\
		-ip_dns2				40.40.40.40		\
		-ip_dns2_step				0.0.1.0			\
		-ipaddress_pool				134.1.0.2	\
		-ipaddress_pool_step			0.0.0.1			\
		-ipaddress_pool_prefix_length 		16			\
		-ip_address					134.1.0.1 \
		-ip_prefix_length			16 \
		-vlan_id						200			\
		-protocol_name				"DHCPv4Server2" \
	]

# Verify that DHCPv4 Server 2 is created
puts "Verify that DHCPv4 Server 2 is created"
if {[keylget dhcp_server_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_server_status log]"
	return $FAILED
}	 
	
set dhcp_server2 [keylget dhcp_server_status dhcpv4server_handle]

# # Create DHCPv4 Client
puts "Create DHCPv4 Client 1"
set dhcp_client_status [::ixiangpf::emulation_dhcp_group_config 	\
		-handle						$deviceGroup_third_handle	\
		-dhcp_range_ip_type				ipv4			\
		-dhcp_range_renew_timer			10			\
		-dhcp_range_use_first_server			1			\
		-use_rapid_commit				1			\
		-vlan_id						100			\
		-protocol_name				"DHCPv4Client1"		\
	]

# Verify that DHCPv4 Client 1 is created
puts "Verify that DHCPv4 Client 1 is created"
if {[keylget dhcp_client_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_client_status log]"
	return $FAILED
}

set dhcp_client1 [keylget dhcp_client_status dhcpv4client_handle]
puts "Create DHCPv4 Client 2"
set dhcp_client_status [::ixiangpf::emulation_dhcp_group_config 	\
		-handle						$deviceGroup_fourth_handle	\
		-dhcp_range_ip_type				ipv4			\
		-dhcp_range_renew_timer			10			\
		-dhcp_range_use_first_server			1			\
		-use_rapid_commit				1			\
		-vlan_id						200			\
		-protocol_name				"DHCPv4Client2"		\
	]

# Verify that DHCPv4 Client 2 is created
puts "Verify that DHCPv4 Client 2 is created"
if {[keylget dhcp_client_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_client_status log]"
	return $FAILED
}

set dhcp_client2 [keylget dhcp_client_status dhcpv4client_handle]

# Start Protocols
# # Start the Servers first
puts "Start the Servers first"
set control_status [::ixiangpf::emulation_dhcp_server_control \
	-dhcp_handle      $dhcp_server1\
	-action           collect\
	]
	
# Verify the start command on DHCPv4 Server 1
puts "Verify the start command on DHCPv4 Server 1"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

set control_status [::ixiangpf::emulation_dhcp_server_control \
	-dhcp_handle      $dhcp_server2\
	-action           collect\
	]
	
# Verify the start command on DHCPv4 Server 2
puts "Verify the start command on DHCPv4 Server 2"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

puts "Wait 15 seconds before the Servers are up..."
after 15000
# # Start the Clients second
puts "Start the Clients second"
set control_status [::ixiangpf::emulation_dhcp_control \
	-handle     $dhcp_client1 \
	-action           bind\
	]

# Verify the start command on DHCPv4 Client 1
puts "Verify the start command on DHCPv4 Client 1"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

set control_status [::ixiangpf::emulation_dhcp_control \
	-handle     $dhcp_client2 \
	-action           bind\
	]

# Verify the start command on DHCPv4 Client 2
puts "Verify the start command on DHCPv4 Client 2"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

puts "Wait 30 seconds before the Clients are up..."
after 30000

# Stats
# DHCPv4 Server Stats
set dhcp_server_stats [::ixiangpf::emulation_dhcp_server_stats 	\
        -port_handle   [list $port_1 $port_3] \
		-action 	collect			 \
	]	

# Verify Statistics from Server are retrieved	
puts "Verify Statistics from Server are retrieved"
if {[keylget dhcp_server_stats status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_server_stats log]"
	return $FAILED
}

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "port_name"]
set dhcpServer1Port                 [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "sessions_up"]
set dchpServer1SessionsUp           [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "sessions_down"]
set dhcpServer1SessionsDown         [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "sessions_not_started"]
set dhcpServer1SessionsNotStarted   [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "session_total"]
set dhcpServer1SessionsTotal		[lindex $dhcp_server_stats 1 1 0 1 $index 1]


set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "port_name"]
set dhcpServer2Port                 [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "sessions_up"]
set dchpServer2SessionsUp           [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "sessions_down"]
set dhcpServer2SessionsDown         [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "sessions_not_started"]
set dhcpServer2SessionsNotStarted   [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "session_total"]
set dhcpServer2SessionsTotal		[lindex $dhcp_server_stats 2 1 0 1 $index 1]



set DHCPv4ServerStats [list                                     \
	[list {"Port $dhcpServer1Port"}                             \
	[list   "Sessions Up"                                 		$dchpServer1SessionsUp\
			"Sessions Down"                                		$dhcpServer1SessionsDown\
			"Sessions Not Started"                           	$dhcpServer1SessionsNotStarted\
			"Sessions Total"                                	$dhcpServer1SessionsTotal]]\
	[list {"Port $dhcpServer2Port"}			\
	[list   "Sessions Up"                                 		$dchpServer2SessionsUp\
			"Sessions Down"                                		$dhcpServer2SessionsDown\
			"Sessions Not Started"                          	$dhcpServer2SessionsNotStarted\
			"Sessions Total"                                	$dhcpServer2SessionsTotal ]]]

set Expected.DHCPv4ServerStats [list                                     \
	[list {"Port $dhcpServer1Port"}                             \
	[list   "Sessions Up"                                 	=	2\
			"Sessions Down"                                	=	0\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	2]]\
	[list {"Port $dhcpServer2Port"}			\
	[list   "Sessions Up"                                 	=	2\
			"Sessions Down"                                	=	0\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	2 ]]]
			
puts "Check Server Statistics"
if {[checkStats ${DHCPv4ServerStats} ${Expected.DHCPv4ServerStats}] == 1} {
    puts "Expected DHCPv4 Server Statistics do not match !!!"
    return $FAILED
}			
	
# DHCPv4 Client Stats
set dhcp_client_stats [::ixiangpf::emulation_dhcp_stats 	\
        -port_handle   [list $port_2 $port_4] \
		-mode 	aggregate_stats			 \
		-dhcp_version dhcp4\
	]	

# Verify Statistics from Client are retrieved
puts "Verify Statistics from Client are retrieved"
if {[keylget dhcp_client_stats status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_client_stats log]"
	return $FAILED
}

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "port_name"]
set dhcpClient1Port                 [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "setup_success"]
set dchpClient1SessionsUp           [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "total_failed"]
set dhcpClient1SessionsDown         [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "sessions_not_started"]
set dhcpClient1SessionsNotStarted   [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "sessions_total"]
set dhcpClient1SessionsTotal		[lindex $dhcp_client_stats 1 1 0 1 $index 1]


set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "port_name"]
set dhcpClient2Port                 [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "setup_success"]
set dchpClient2SessionsUp           [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "total_failed"]
set dhcpClient2SessionsDown         [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "sessions_not_started"]
set dhcpClient2SessionsNotStarted   [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "sessions_total"]
set dhcpClient2SessionsTotal		[lindex $dhcp_client_stats 2 1 0 1 $index 1]


set DHCPv4ClientStats [list                                     \
	[list "Port $dhcpClient1Port"                             \
	[list   "Sessions Up"                                 		$dchpClient1SessionsUp\
			"Sessions Down"                                		$dhcpClient1SessionsDown\
			"Sessions Not Started"                          	$dhcpClient1SessionsNotStarted\
			"Sessions Total"                                	$dhcpClient1SessionsTotal]]\
	[list "Port $dhcpClient2Port"		\
	[list   "Sessions Up"                                 		$dchpClient2SessionsUp\
			"Sessions Down"                                		$dhcpClient2SessionsDown\
			"Sessions Not Started"                          	$dhcpClient2SessionsNotStarted\
			"Sessions Total"                                	$dhcpClient2SessionsTotal ]]]

set Expected.DHCPv4ClientStats [list                                     \
	[list {"Port $dhcpClient1Port"}                             \
	[list   "Sessions Up"                                 	=	23\
			"Sessions Down"                                	=	0\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	23]]\
	[list {"Port $dhcpClient2Port"}			\
	[list   "Sessions Up"                                 	=	23\
			"Sessions Down"                                	=	0\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	23 ]]]

puts "Check Server Statistics"
if {[checkStats ${DHCPv4ClientStats} ${Expected.DHCPv4ClientStats}] == 1} {
    puts "Expected DHCPv4 Client Statistics do not match !!!"
    return $FAILED
}				

# Stop Protocols
# # Stop DHCPv4 Servers
puts "Stop DHCPv4 Servers"
set control_status [::ixiangpf::emulation_dhcp_server_control \
	-dhcp_handle      $dhcp_server1\
	-action           reset\
	]
	
# Verify the stop command on DHCPv4 Server 1
puts "Verify the stop command on DHCPv4 Server 1"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

set control_status [::ixiangpf::emulation_dhcp_server_control \
	-dhcp_handle      $dhcp_server2\
	-action           reset\
	]
	
# Verify the stop command on DHCPv4 Server 2
puts "Verify the stop command on DHCPv4 Server 2"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

# # Stop DHCPv4 Clients
puts "Stop DHCPv4 Clients"
set control_status [::ixiangpf::emulation_dhcp_control \
	-handle     $dhcp_client1 \
	-action           release\
	]

# Verify the stop command on DHCPv4 Client 1
puts "Verify the stop command on DHCPv4 Client 1"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

set control_status [::ixiangpf::emulation_dhcp_control \
	-handle     $dhcp_client2 \
	-action           release\
	]

# Verify the stop command on DHCPv4 Client 2
puts "Verify the stop command on DHCPv4 Client 2"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}
puts "Wait for DHCPv4 Protocol to stop..."
after 10000

# Modify some of the protocol specific parameters
# # Create DHCPv4 Server
puts "Modify DHCPv4 Server 1"
set dhcp_server_status [::ixiangpf::emulation_dhcp_server_config 	\
		-mode modify                                      \
		-handle					$dhcp_server1 	\
		-lease_time                 			86400   	     		\
		-ipaddress_count			15			\
		-ip_dns1				70.70.70.70	\
		-ip_dns1_step				0.0.0.1			\
		-ip_dns2				21.21.21.21		\
		-ip_dns2_step				0.0.1.0			\
		-ipaddress_pool				154.1.0.2	\
		-ipaddress_pool_step			0.0.0.1			\
		-ipaddress_pool_prefix_length 		16			\
		-ip_address					154.1.0.1 \
		-ip_prefix_length			16 \
		-vlan_id						200			\
		-protocol_name				"DHCPv4Server1" \
	]

# Verify that DHCPv4 Server 1 is modified
puts "Verify that DHCPv4 Server 1 is modified"
if {[keylget dhcp_server_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_server_status log]"
	return $FAILED
}	 

puts "Modify DHCPv4 Server 2"
set dhcp_server_status [::ixiangpf::emulation_dhcp_server_config 	\
		-mode modify                                           \
		-handle					$dhcp_server2 	\
		-lease_time                 			86400   	     		\
		-ipaddress_count			10			\
		-ip_dns1				80.80.80.80		\
		-ip_dns1_step				0.0.0.1			\
		-ip_dns2				41.41.41.41		\
		-ip_dns2_step				0.0.1.0			\
		-ipaddress_pool				134.1.0.2	\
		-ipaddress_pool_step			0.0.0.1			\
		-ipaddress_pool_prefix_length 		16			\
		-ip_address					134.1.0.1 \
		-ip_prefix_length			16 \
		-vlan_id						101			\
		-protocol_name				"DHCPv4Server2" \
	]

# Verify that DHCPv4 Server 2 is modified
puts "Verify that DHCPv4 Server 2 is modified"
if {[keylget dhcp_server_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_server_status log]"
	return $FAILED
}	 

puts "Apply on the fly changes"
set apply_on_the_fly_status [::ixiangpf::test_control\
       -action	   apply_on_the_fly_changes]
# Verify that apply on the fly changes command is succeded
puts "Verify that apply on the fly changes command is succeded"
if {[keylget apply_on_the_fly_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget apply_on_the_fly_status log]"
	return $FAILED
}
puts "Wait 5 seconds ..."		
after 5000

# Start Protocols
# # Start the Servers first
puts "Start the Servers first"
set control_status [::ixiangpf::emulation_dhcp_server_control \
	-dhcp_handle      $dhcp_server1\
	-action           collect\
	]
	
# Verify the start command on DHCPv4 Server 1
puts "Verify the start command on DHCPv4 Server 1"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

set control_status [::ixiangpf::emulation_dhcp_server_control \
	-dhcp_handle      $dhcp_server2\
	-action           collect\
	]
	
# Verify the start command on DHCPv4 Server 2
puts "Verify the start command on DHCPv4 Server 2"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

puts "Wait 15 seconds before the Servers are up..."
after 15000
# # Start the Clients second
puts "Start the Clients second"
set control_status [::ixiangpf::emulation_dhcp_control \
	-handle     $dhcp_client1 \
	-action           bind\
	]

# Verify the start command on DHCPv4 Client 1
puts "Verify the start command on DHCPv4 Client 1"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

set control_status [::ixiangpf::emulation_dhcp_control \
	-handle     $dhcp_client2 \
	-action           bind\
	]

# Verify the start command on DHCPv4 Client 2
puts "Verify the start command on DHCPv4 Client 2"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}

puts "Wait 30 seconds before the Clients are up..."
after 30000

# Stats
# DHCPv4 Server Stats
# Stats
# DHCPv4 Server Stats
set dhcp_server_stats [::ixiangpf::emulation_dhcp_server_stats 	\
        -port_handle   [list $port_1 $port_3] \
		-action 	collect			 \
	]	

# Verify Statistics from Server are retrieved	
puts "Verify Statistics from Server are retrieved"
if {[keylget dhcp_server_stats status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_server_stats log]"
	return $FAILED
}

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "port_name"]
set dhcpServer1Port                 [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "sessions_up"]
set dchpServer1SessionsUp           [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "sessions_down"]
set dhcpServer1SessionsDown         [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "sessions_not_started"]
set dhcpServer1SessionsNotStarted   [lindex $dhcp_server_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 1 1 0 1] "session_total"]
set dhcpServer1SessionsTotal		[lindex $dhcp_server_stats 1 1 0 1 $index 1]


set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "port_name"]
set dhcpServer2Port                 [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "sessions_up"]
set dchpServer2SessionsUp           [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "sessions_down"]
set dhcpServer2SessionsDown         [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "sessions_not_started"]
set dhcpServer2SessionsNotStarted   [lindex $dhcp_server_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_server_stats 2 1 0 1] "session_total"]
set dhcpServer2SessionsTotal		[lindex $dhcp_server_stats 2 1 0 1 $index 1]



set DHCPv4ServerStats [list                                     \
	[list {"Port $dhcpServer1Port"}                             \
	[list   "Sessions Up"                                 		$dchpServer1SessionsUp\
			"Sessions Down"                                		$dhcpServer1SessionsDown\
			"Sessions Not Started"                           	$dhcpServer1SessionsNotStarted\
			"Sessions Total"                                	$dhcpServer1SessionsTotal]]\
	[list {"Port $dhcpServer2Port"}			\
	[list   "Sessions Up"                                 		$dchpServer2SessionsUp\
			"Sessions Down"                                		$dhcpServer2SessionsDown\
			"Sessions Not Started"                          	$dhcpServer2SessionsNotStarted\
			"Sessions Total"                                	$dhcpServer2SessionsTotal ]]]

set Expected.DHCPv4ServerStats [list                                     \
	[list {"Port $dhcpServer1Port"}                             \
	[list   "Sessions Up"                                 	=	2\
			"Sessions Down"                                	=	0\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	2]]\
	[list {"Port $dhcpServer2Port"}			\
	[list   "Sessions Up"                                 	=	2\
			"Sessions Down"                                	=	0\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	2 ]]]
			
puts "Check Server Statistics"
if {[checkStats ${DHCPv4ServerStats} ${Expected.DHCPv4ServerStats}] == 1} {
    puts "Expected DHCPv4 Server Statistics do not match !!!"
    return $FAILED
}			
	
# DHCPv4 Client Stats
set dhcp_client_stats [::ixiangpf::emulation_dhcp_stats 	\
        -port_handle   [list $port_2 $port_4] \
		-mode 	aggregate_stats			 \
		-dhcp_version dhcp4\
	]	

# Verify Statistics from Client are retrieved
puts "Verify Statistics from Client are retrieved"
if {[keylget dhcp_client_stats status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget dhcp_client_stats log]"
	return $FAILED
}

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "port_name"]
set dhcpClient1Port                 [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "setup_success"]
set dchpClient1SessionsUp           [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "total_failed"]
set dhcpClient1SessionsDown         [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "sessions_not_started"]
set dhcpClient1SessionsNotStarted   [lindex $dhcp_client_stats 1 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 1 1 0 1] "sessions_total"]
set dhcpClient1SessionsTotal		[lindex $dhcp_client_stats 1 1 0 1 $index 1]


set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "port_name"]
set dhcpClient2Port                 [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "setup_success"]
set dchpClient2SessionsUp           [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "total_failed"]
set dhcpClient2SessionsDown         [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "sessions_not_started"]
set dhcpClient2SessionsNotStarted   [lindex $dhcp_client_stats 2 1 0 1 $index 1]

set index [lsearch -regexp [lindex $dhcp_client_stats 2 1 0 1] "sessions_total"]
set dhcpClient2SessionsTotal		[lindex $dhcp_client_stats 2 1 0 1 $index 1]


set DHCPv4ClientStats [list                                     \
	[list "Port $dhcpClient1Port"                             \
	[list   "Sessions Up"                                 		$dchpClient1SessionsUp\
			"Sessions Down"                                		$dhcpClient1SessionsDown\
			"Sessions Not Started"                          	$dhcpClient1SessionsNotStarted\
			"Sessions Total"                                	$dhcpClient1SessionsTotal]]\
	[list "Port $dhcpClient2Port"		\
	[list   "Sessions Up"                                 		$dchpClient2SessionsUp\
			"Sessions Down"                                		$dhcpClient2SessionsDown\
			"Sessions Not Started"                          	$dhcpClient2SessionsNotStarted\
			"Sessions Total"                                	$dhcpClient2SessionsTotal ]]]

set Expected.DHCPv4ClientStats [list                                     \
	[list {"Port $dhcpClient1Port"}                             \
	[list   "Sessions Up"                                 	=	8\
			"Sessions Down"                                	=	15\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	23]]\
	[list {"Port $dhcpClient2Port"}			\
	[list   "Sessions Up"                                 	=	8\
			"Sessions Down"                                	=	15\
			"Sessions Not Started"                          =	0\
			"Sessions Total"                                =	23 ]]]

puts "Check Server Statistics"
if {[checkStats ${DHCPv4ClientStats} ${Expected.DHCPv4ClientStats}] == 1} {
    puts "Expected DHCPv4 Client Statistics do not match !!!"
    return $FAILED
}				



# # Stop All Protocols
puts "Stop All Protocols"
set control_status [::ixiangpf::test_control \
	-action           stop_all_protocols\
	]
# Verify the stop all protocols command
puts "Verify the stop all protocols command"
if {[keylget control_status status] == $::FAILURE } {
    puts "FAIL - $test_name - [keylget control_status log]"
	return $FAILED
}
puts "Wait 10 seconds for Protocols to stop..."
after 10000
puts "Done... IxNetwork session is closed..."
puts ""
puts "!!! PASSED !!!"
