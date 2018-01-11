package req Ixia

set ixnHLT(path_list) {{//vport:<1> //vport:<2>}}
set guard_rail statistics
# 
# 
set _result_ [::ixia::connect  \
    -reset 1 \
    -vport_count 2 \
    -ixnetwork_tcl_server localhost \
    -tcl_server localhost \
    -guard_rail $guard_rail \
]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
  $::ixnHLT_errorHandler [info script] $_result_
}
if {[catch {keylget _result_ vport_list} _port_handle]} {
    error "connection status: $_result_: $_port_handle"
}
set i 0
foreach _unconnected_port $_port_handle {
    set port_${i} $_unconnected_port
    incr i
}

# method 1
# using interface_config for the ethernetRange

set chassis [format %02x [lindex [split $port_0 "/"] 0]]
set card    [format %02x [lindex [split $port_0 "/"] 1]]
set port    [format %02x [lindex [split $port_0 "/"] 2]]
set src_mac_addr 00${chassis}.00${card}.${port}01
set interface_status [::ixia::interface_config                   \
    -port_handle            $port_0                          \
    -mode                   config                           \
    -connected_count        1                                \
    -src_mac_addr           $src_mac_addr                    \
    -l23_config_type        static_endpoint                  \
]

set ethRange [keylget interface_status interface_handle]

set _result_ [::ixia::esmc_config  \
    -mode create \
    -parent_handle $ethRange \
    -style //vport/protocolStack/ethernetEndpoint/range \
    -wait_id False \
    -ql QL-PRS \
    -rate 2 \
    -flag_mode Auto \
    -enabled True \
    -name direct-esmc-range \
]
puts $_result_

# method 2
# using ethernetrange_config for the ethernetRange

set _result_ [::ixia::ethernetrange_config  \
    -mode create \
    -parent_handle $port_1 \
    -style //vport/protocolStack/ethernetEndpoint/range \
    -mac_range_enabled True \
    -mac_range_count 1 \
    -mac_range_mtu 1500 \
    -mac_range_increment_by 00:00:00:00:00:01 \
    -mac_range_mac 4C:FB:AA:6C:00:00 \
    -mac_range_name MAC-R1 \
    -vlan_range_id_incr_mode 2 \
    -vlan_range_enabled False \
    -vlan_range_name VLAN-R1 \
]

set codegen_ethrange_handle [keylget _result_ handles]

set _result_ [::ixia::esmc_config  \
    -mode create \
    -parent_handle $codegen_ethrange_handle \
    -style //vport/protocolStack/ethernetEndpoint/range \
    -wait_id False \
    -ql QL-PRS \
    -rate 1 \
    -flag_mode Auto \
    -enabled True \
    -name ethernetrange_config-esmc \
]

puts $_result_