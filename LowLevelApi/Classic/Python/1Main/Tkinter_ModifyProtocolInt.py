#!/usr/local/python2.7.6/bin/python2.7

# By Hubert Gee
#
# Description:
#   A sample script using Tkinter to call TCL APIs.
#   This script sources an API file and the APIs are a combination
#   of low level and high level APIs.
#   
#   This script can load a saved config file or resume from an existing
#   configuration.
#   
#   This script was created to test ModifyProtocolInterfaces.

import Tkinter
import sys
import time

tcl = Tkinter.Tcl()
tcl.eval('package req Ixia')
tcl.eval('source tclApi2.tcl')

tcl.eval('set connect(-tcl_server) "10.219.117.101"')
tcl.eval('set connect(-ixnetwork_tcl_server) "10.219.117.103"')
tcl.eval('set connect(-username) "hgee"')
tcl.eval('set connect(-session_resume_keys) 1')

tcl.eval('set ixiaChassisIp "10.219.117.101"')
tcl.eval('set ixNetworkTclServerIp "10.219.117.103"')
tcl.eval('set userName) "hgee"')
tcl.eval('set portList "1/1 1/2"')
tcl.eval('set port1 "1/1/1"')
tcl.eval('set port2 "1/1/2"')
tcl.eval('set ixncfgFile "/home/hgee/Dropbox/MyIxiaWork/Temp/l2l3_8.10.ixncfg"')


# Uncomment this to load a saved config file
#if tcl.eval('LoadConfigFile') == 1:
#    sys.exit()

# Uncomment this to connect to an existing configuration
status = tcl.eval('ResumeHlt ::connect')


#if tcl.eval('VerifyPortState') == 1:
#    sys.exit()


'''
tcl.eval('ModifyProtocolInterfaces -port $port1 -ipv4 10.10.10.1 -ipv4MaskWidth 24 \
-ipv4Step 0.0.0.1 -gatewayIpv4 10.10.10.11 -gatewayIpv4Step 0.0.0.1 -name {{1 myInt1} {3 myInt3} {5 myInt6}} \
-disable all -vlanId 3 -vlanPriority 5 -vlanEnable false -vlanTpId 0x8200 -vlanCount 10')
'''

#tcl.eval('ModifyProtocolInterfaces -port $port1 -disable all -mac 00:01:01:01:00:253 -macStep 00:00:00:00:00:02')

#tcl.eval('ModifyProtocolInterfaces -port $port1 -delete {11 12 13 14 15 16 17 18 19 20 21}')

# QinQ
#tcl.eval('ModifyProtocolInterfaces -port $port1 -vlanId {88,108} -vlanPriority {7,3}')
#tcl.eval('ModifyProtocolInterfaces -port $port1 -vlanIdList {{1 78,103} {3 78,103}} -vlanPriorityList {{1 7,5} {3 6,3}}')


#tcl.eval('ModifyProtocolInterfaces -port $port1 -delete all')

#tcl.eval('ModifyProtocolInterfaces -port $port1 -vlanDisableList {1 3 5 7 9}')

#tcl.eval('ModifyProtocolInterfaces -port $port1 -vlanId 3 -vlanPriority 5 -vlanEnable true')

#tcl.eval('ModifyProtocolInterfaces -port $port1 -vlanIdList {{1 101} {2 102} {3 103} {4 104} {5 105}} \
#-vlanPriorityList {{1 1} {2 2} {3 3} {4 4} {5 5}} -vlanEnableList {1 2 3 4 5} -vlanDisableList {6 7 8 9}')

#tcl.eval('ModifyProtocolInterfaces -port $port1 -mac 00:01:01:03:00:01 -macStep 00:00:01:00:00:00')


#tcl.eval('ModifyProtocolInterfaces -port $port1 -ipv4List {{"myInt1" 188.188.10.1} {"myInt3" 208.208.2.1}} -ipv4GatewayList {{1 2.2.2.1} {2 2.2.2.2} {3 2.2.2.3}}')

#tcl.eval('ModifyProtocolInterfaces -port $port1 -ipv4List {{"myInt1" 100.100.10.1} {"myInt3" 200.200.2.1}} -ipv4GatewayList {{1 2.2.2.1} {2 2.2.2.2} {3 2.2.2.3}} -name {{1 myInt1} {3 myInt3}}')


'''
ports = []
ipList = []
gatewayList = []
vlanList = []
port1 = '1/1/1'

vlanId = 100
for x in range(1,11):
    ports.append(port1)
    ipList.append('1.1.1.%d' % x)
    #vlanList.append(str(100))
    vlanList.append('%s %s' % (str(100),  str(88)))
    vlanId += 1

for x in range(11,21):
    gatewayList.append('1.1.1.%d' % x)

# Create new interfaces on a port. This will also append to existing interfaces
# Two ways to create interfaces:
#    1> Enter one value and let step do the incrementings.
#    2> Provide a list of values. 
#      
#       ports       = {1/1/1    1/1/1    1/1/1}
#       ipList      = {1.1.1.1  1.1.1.2  1.1.1.3}
#       gatewayList = {1.1.1.4  1.1.1.5  1.1.1.6}
#       vlanList    = {1001     1002     1003}
#       macList     = {align with above}

# This example shows how to pass in a list custom list of 
# IP, Macs, vlan IDs
tcl.eval('set portConfig($port1,-mode) config')
tcl.eval('set portConfig($port1,-port_handle) {%s}' % ' '.join(ports))
tcl.eval('set portConfig($port1,-intf_ip_addr) {%s}' % ' '.join(ipList))
tcl.eval('set portConfig($port1,-connected_count) 1')
tcl.eval('set portConfig($port1,-gateway) {%s}' % ' '.join(gatewayList))
tcl.eval('set portConfig($port1,-gateway_step) 0.0.0.1')
tcl.eval('set portConfig($port1,-netmask) 255.255.255.0')
tcl.eval('set portConfig($port1,-src_mac_addr) "0001.0101.0001"')
tcl.eval('set portConfig($port1,-src_mac_addr_step) 0000.0000.0001')
tcl.eval('set portConfig($port1,-mtu) 1500')
tcl.eval('set portConfig($port1,-vlan_id) {%s}' % ' '.join(vlanList) ) ;# Ex: A list of Vlan IDs
tcl.eval('set portConfig($port1,-vlan_id) {100,88}') ;# QinQ
tcl.eval('set portConfig($port1,-vlan_id_count) 1') ;# Ignore this if you are doing QinQ
tcl.eval('set portConfig($port1,-vlan) 1') ;# 1 means to enable vlan. 0 to disable vlan.
tcl.eval('set portConfig($port1,-vlan_id_step) 0')
tcl.eval('set portConfig($port1,-vlan_user_priority) {3,7}') ;# QinQ
tcl.eval('set endpoint($port1) [PortConfigProtocolIntHlt $port1 ::portConfig]')


# This example shows that it will autogenerate MAC addresses,
# create 10 incremental interfaces.
tcl.eval('set portConfig($port2,-mode) config')
tcl.eval('set portConfig($port2,-port_handle) $port2')
tcl.eval('set portConfig($port2,-intf_ip_addr) 1.1.1.11')
tcl.eval('set portConfig($port2,-connected_count) 10')
tcl.eval('set portConfig($port2,-gateway) 1.1.1.1')
tcl.eval('set portConfig($port2,-gateway_step) 0.0.0.1')
tcl.eval('set portConfig($port2,-netmask) 255.255.255.0')
#tcl.eval('set portConfig($port2,-src_mac_addr) "0001.0202.0001"')
#tcl.eval('set portConfig($port2,-src_mac_addr_step) 0000.0000.0001')
tcl.eval('set portConfig($port2,-mtu) 1500')
tcl.eval('set portConfig($port2,-vlan_id) 100')
tcl.eval('set portConfig($port2,-vlan_id_count) 1')
tcl.eval('set portConfig($port2,-vlan) 1')
tcl.eval('set portConfig($port2,-vlan_id_step) 1')
tcl.eval('set portConfig($port2,-vlan_user_priority) 7')
tcl.eval('set endpoint($port2) [PortConfigProtocolIntHlt $port2 ::portConfig]')
'''
