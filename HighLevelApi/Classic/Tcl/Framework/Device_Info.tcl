package require Ixia

set test_name [info script]

set chassis_ip [list 10.205.19.228 10.205.19.232]
set port_list [list [list 4/1] [list 2/3]]

# Connect to the chassis, reset to factory defaults and take ownership
set connect_status [::ixia::connect \
        -reset                    \
        -device    $chassis_ip     \
        -port_list $port_list     \
        -username  ixiaApiUser    ]
if {[keylget connect_status status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget connect_status log]"
}

set port_0 [keylget connect_status port_handle.[lindex $chassis_ip 0].4/1]
set port_1 [keylget connect_status port_handle.[lindex $chassis_ip 1].2/3]

set port_list_info {1/3/1 1/3/2 1/4/1 1/4/2 1/4/3 1/4/4 1/7/1 1/8/1 2/2/1 2/2/2 2/2/3 2/2/4}

# Getting information about the specified ports
set device_stat [::ixia::device_info                \
        -ports              $port_list_info         \
        -fspec_version                              \
        ]
if {[keylget device_stat status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_stat log]"
}

foreach port $port_list_info {
    if {[regexp -- {^(\d+)/\d+/\d+$} $port {} chassis] == 0} {
        keylset returnList status $::FAILURE
        keylset returnList log "ERROR on $test_name: invalid port list specified."
        return $returnList
    }
    puts "Port $port information:"
    if {$chassis == 1} {
        set chassis [lindex $chassis_ip 0]
    } else {
        set chassis [lindex $chassis_ip 1]
    }
    puts "in chassis $chassis"
    catch {unset available_type}
    catch {set available_type [keylget device_stat $chassis.available.$port.type]}
    if {[info exists available_type]} {
        puts "port available\ntype=$available_type"
    }
    catch {unset inuse_owner}
    catch {set inuse_owner [keylget device_stat $chassis.inuse.$port.owner]} 
    if {[info exists inuse_owner]} {
        puts "port in use by $inuse_owner\ntype [keylget device_stat $chassis.inuse.$port.type]"
    }
    puts "--------------------------"
}

# Getting ports' names
set device_stat [::ixia::device_info                \
        -port_handle        $port_list_info         \
        -fspec_version                              \
        ]
if {[keylget device_stat status] != $::SUCCESS} {
    return "FAIL - $test_name - [keylget device_stat log]"
}

foreach port $port_list_info {
    if {[regexp -- {^(\d+)/\d+/\d+$} $port {} chassis] == 0} {
        keylset returnList status $::FAILURE
        keylset returnList log "ERROR on $test_name: invalid port list specified."
        return $returnList
    }
    puts "Port handle $port information:"
    if {$chassis == 1} {
        set chassis [lindex $chassis_ip 0]
    } else {
        set chassis [lindex $chassis_ip 1]
    }
    puts "in chassis $chassis"
    puts "port name=[keylget device_stat port_handle.$port.port_name]"
    puts "--------------------------"
}
