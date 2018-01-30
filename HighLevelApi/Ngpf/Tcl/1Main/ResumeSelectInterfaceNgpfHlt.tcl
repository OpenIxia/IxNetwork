#!/opt/ActiveTcl-8.5/bin/tclsh


package req Ixia

set ixiaChassisIp 10.219.117.102
set ixNetworkTclServerIp 10.219.16.219

set userName hgee

source /home/hgee/Dropbox/MyIxiaWork/IxNet_tclApi.tcl

proc KeylPrint {keylist {space ""}} {
    upvar $keylist kl
    set result ""
    foreach key [keylkeys kl] {
	set value [keylget kl $key]
	if {[catch {keylkeys value}]} {
	    append result "$space$key: $value\n"
	} else {
	    set newspace "$space "
	    append result "$space$key:\n[KeylPrint value $newspace]"
	}
    }
    return $result
}

puts "\nConnecting to $ixNetworkTclServerIp ..."

EnableHltDebug myIxiaDebug.txt

set status [::ixiangpf::connect \
		-ixnetwork_tcl_server $ixNetworkTclServerIp \
		-tcl_server $ixiaChassisIp \
		-username $userName \
		-session_resume_keys 1 \
	       ]

puts [KeylPrint status]


# First, the followings are the acceptable handles to send or receive from "all" interfaces.
# You do NOT use the -scalable parameters for all interfaces.
# Scalable parameters are ONLY to select interfaces:
#
#   -/topology:1
#   -/topology:1/deviceGroup:1
#   -/topology:1/deviceGroup:1/ethernet:1/ipv4:1

#----------------------------------------------------------------------------------------

set ipv4Handle_src /topology:1/deviceGroup:1/ethernet:1/ipv4:1 
set ipv4Handle_dst /topology:2/deviceGroup:1/ethernet:1/ipv4:1


if 0 {
#----- Example 1 -------#
#   src endpoints interface #1 to #5 
# /topology:1/deviceGroup:1/ethernet:1/ipv4:1
set srcPortHandle(EndpointSet-1) [list $ipv4Handle_src]
set srcPortStart(EndpointSet-1)  [list 1]
set srcPortCount(EndpointSet-1)  [list 1]
set srcIntStart(EndpointSet-1)   [list 1]
set srcIntCount(EndpointSet-1)   [list 5]

#  dst endpoints interface #6 to #10
# /topology:2/deviceGroup:1/ethernet:1/ipv4:1
set dstPortHandle(EndpointSet-1)  [list $ipv4Handle_dst]
set dstPortStart(EndpointSet-1)   [list 1]
set dstPortCount(EndpointSet-1)   [list 1]
set dstIntStart(EndpointSet-1)    [list 6]
set dstIntCount(EndpointSet-1)    [list 5]
#-----------------------#
}

#----- Example 2 -------#
#   src endpoints interface #2, #4, #6, #8, #10 
# /topology:1/deviceGroup:1/ethernet:1/ipv4:1
#
# As you can see, I'm sending from 5 different interfaces from the same ipv4 stack.
# To do this, I'm using the same handle and a list containing 5 same handles.
# For each index on the handle list, they correlate to the index on each of the array list.
# Meaning that they are aligned accordingly to the index number on every list. 
# Now go look at the photo below for an understanding.
set srcPortHandle(EndpointSet-1) [list $ipv4Handle_src $ipv4Handle_src $ipv4Handle_src $ipv4Handle_src $ipv4Handle_src]
set srcPortStart(EndpointSet-1)  [list 1 1 1 1 1]
set srcPortCount(EndpointSet-1)  [list 1 1 1 1 1]
set srcIntStart(EndpointSet-1)   [list 2 4 6 8 10]
set srcIntCount(EndpointSet-1)   [list 1 1 1 1 1]

#  dst endpoints interface #6 to #10
# /topology:2/deviceGroup:1/ethernet:1/ipv4:1
set dstPortHandle(EndpointSet-1)  [list $ipv4Handle_dst]
set dstPortStart(EndpointSet-1)   [list 1]
set dstPortCount(EndpointSet-1)   [list 1]
set dstIntStart(EndpointSet-1)    [list 6]
set dstIntCount(EndpointSet-1)    [list 5]
#-----------------------#


# Traffic Item Notes:
# NOTE 1: 
#       - Notice that there is no dollar sign for the variables.  
#       - Even though we are using only scalable parameters, we still need to include the parameters -emulation_src_handle and -emulation_dst_handle.
#           For those two -emulation handles, you have to pass in an empty list.
#           But if you are going to create, say 3 endpoints on this Traffic Itrem, then you have to pass in 3 empty list like this: [list  [list]  [list] [list] ]  or {{  {}  {}  {}  }}
# 
# NOTE 2:
#         - Let say our src endpoint are selective.  Then you must use the -scalable parameters.
#          - But if you destination endpoints are not selective, you MUST remove all of the dest -scalable parameters and use the parameter -emulation_dst_handle

if 0 {
set trafficItemStatus [::ixia::traffic_config \
			   -mode create \
			   -name Traffic_Item_1 \
			   -endpointset_count 1 \
			   -circuit_endpoint_type ipv4 \
			   -l3_protocol ipv4 \
			   -bidirectional 0 \
			   -route_mesh one_to_one \
			   -src_dest_mesh one_to_one \
			   -track_by {trackingenabled0 sourceDestValuePair0} \
			   -allow_self_destined 0 \
			   -emulation_src_handle [list [list]] \
			   -emulation_dst_handle [list [list /topology:1/deviceGroup:1]] \
			   -emulation_scalable_src_handle     srcPortHandle \
			   -emulation_scalable_src_intf_start srcIntStart \
			   -emulation_scalable_src_intf_count srcIntCount \
			   -emulation_scalable_dst_handle     dstPortHandle \
			   -emulation_scalable_dst_intf_start dstIntStart \
			   -emulation_scalable_dst_intf_count dstIntCount \
 			   -emulation_scalable_src_port_start srcPortStart \
			   -emulation_scalable_src_port_count srcPortCount \
			   -emulation_scalable_dst_port_count dstPortCount \
			   -emulation_scalable_dst_port_start dstPortStart \
			  ]
}

set trafficItemStatus [::ixia::traffic_config \
			   -mode create \
			   -name Traffic_Item_1 \
			   -endpointset_count 1 \
			   -circuit_endpoint_type ipv4 \
			   -l3_protocol ipv4 \
			   -bidirectional 0 \
			   -route_mesh one_to_one \
			   -src_dest_mesh one_to_one \
			   -track_by {trackingenabled0 sourceDestValuePair0} \
			   -allow_self_destined 0 \
			   -emulation_src_handle [list [list]] \
			   -emulation_dst_handle [list [list /topology:2/deviceGroup:1/ethernet:1/ipv4:1]] \
			   -emulation_scalable_src_handle     srcPortHandle \
			   -emulation_scalable_src_intf_start srcIntStart \
			   -emulation_scalable_src_intf_count srcIntCount \
 			   -emulation_scalable_src_port_start srcPortStart \
			   -emulation_scalable_src_port_count srcPortCount \
			  ]

if {[keylget trafficItemStatus status] != $::SUCCESS} {
    puts "\nError: Traffic Item config failed: $trafficItemStatus\n"
    exit
}


