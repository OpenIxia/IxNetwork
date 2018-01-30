#!/opt/Python-2.7.6/bin/python2.7

import Tkinter
import sys
import time

ixChassisIp = '10.219.117.102'
ixNetworkTclServer = '10.219.16.219'
user_name = 'hgee'
port_list = '1/1 1/2'
port1 = '1/1/1'
port2 = '1/1/2'

tcl = Tkinter.Tcl()

tcl.eval('package req Ixia')

tcl.eval('source tclApi.tcl')

tcl.eval('puts "\nHello World\n"')

connect_status = tcl.eval('ConnectToIxia "-reset -port_list %s -device %s -ixnetwork_tcl_server %s -tcl_server %s -username %s"' % \
                              (port_list, ixChassisIp, ixNetworkTclServer, ixChassisIp, user_name))

port1_handle = tcl.eval('PortConfigProtocolInt "-mode config -port_handle %s -intf_ip_addr 1.1.1.1 -gateway 1.1.1.2 -netmask 255.255.255.0 -src_mac_addr 0001.0101.0001 -l23_config_type protocol_interface"' % port1)

# ::ixNet::OBJ-/vport:1/interface:1
print '\nport1_handle: ', port1_handle

port2_handle = tcl.eval('PortConfigProtocolInt "-mode config -port_handle %s -intf_ip_addr 1.1.1.2 -gateway 1.1.1.1 -netmask 255.255.255.0 -src_mac_addr 0001.0102.0001 -l23_config_type protocol_interface"' % port2)

# ::ixNet::OBJ-/vport:2/interface:1
print '\nport2_handle: ', port2_handle

traffic_config_sttatus = tcl.eval('CreateTrafficItem "-mode create -name Traffic_Item_1 -emulation_src_handle %s -emulation_dst_handle %s -src_dest_mesh one_to_one -route_mesh one_to_one -bidirectional 0 -circuit_endpoint_type ipv4 -rate_percent 50 -frame_size 80 -transmit_mode continuous -pkts_per_burst 50000 -track_by flowGroup0"' % (port1_handle, port2_handle))

tcl.eval('StartTrafficHlt')
print '\nSleep 10 seconds for traffic to run ...'
time.sleep(10)
flow_stats = tcl.eval('set stats [GetStatsHlt flow]')

tcl.eval('puts "\nkeylprint: [KeylPrint stats]"')

print '\nflow_stats: ', flow_stats
tcl.eval('puts "\nFramesSent: [keylget stats flow.1.rx total_pkts]"')

