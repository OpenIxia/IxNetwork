#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    A sample script to show how to create two Topology Groups with multiple
#    ports in each Topology Group.
#    Verify port state
#    Create an IPv4 BGP configuration from scratch.
#    Start all protocols
#    Verify protocol
#    Start traffic
#    Get stats
#
# Prerequisites
#    - If connecting to a Linux API server:
#        - The Linux API server is a secured access device.
#        - Uses SSL (HTTPS).
#        - You must install:
#             - OpenSSL for your Linux OS if running this script from Linux.
#             - TLS for TCL in order to connect to a Linux API server.
#               Download from: https://sourceforge.net/projects/tls/files/tls
#
#    - Open README_LinuxApiServer file to download IxTclNetwork.
#    - TCL must have Tclx package
#      If you could, install and use ActiveState TCL.
#
# This script is compatible on Windows API server and Linux API server.
#

package req Tclx
source api.tcl

set osPlatform windows;# windows|linux

if {$osPlatform == "windows"} {
    set apiServerIp 192.168.70.3
 }
if {$osPlatform == "linux"} {
    set apiServerIp 192.168.70.108
}

set ixChassisIp 192.168.70.11
set ixNetworkVersion 8.40

set licenseServerIp 192.168.70.3 ;# This could be on an ixChassisIp or a remote Windows PC.
set licenseMode subscription 
set licenseTier tier3

set portList [list "$ixChassisIp 1 1" "$ixChassisIp 2 1" "$ixChassisIp 3 1" "$ixChassisIp 4 1"]
set topology1Ports [list "$ixChassisIp 1 1" "$ixChassisIp 3 1"]
set topology2Ports [list "$ixChassisIp 2 1" "$ixChassisIp 4 1"]

if {$osPlatform == "linux"} {
    package req IxTclNetworkLinuxApiServer 
   if {[Connect -apiServerIp $apiServerIp -ixNetworkVersion $ixNetworkVersion -osPlatform linux -username admin -password admin]} {
	exit
    }
    set sessions [ixNet getSessionInfo]
    puts "\nSessionId: $sessions"
}

if {$osPlatform == "windows"} {
    package req IxTclNetwork
    if {[Connect -apiServerIp $apiServerIp -ixNetworkVersion $ixNetworkVersion -osPlatform windows]} {
	exit
    }
}

if {[NewBlankConfig]} {
    exit
}

# Pass in a list of ixia chassis IP address if you have multiple chassis's.
ConnectToIxChassis $ixChassisIp

if {[ReleasePorts $portList]} {
    exit
}

if {[ClearPortOwnership $portList]} {
    exit
}

# Configuring the license server details are optional. If you need to configure them,
# this is the spot to do it.  NOte: You need to release the ports before you could configure them
# which is done above.
if {[ConfigLicenseServer $licenseServerIp $licenseMode $licenseTier]} {
    exit
}

if {[AssignPorts $ixChassisIp $portList]} {
    exit
}

if {[VerifyPortState]} {
    exit
}

set topology1Obj [CreateTopology -name Topo-1 -portList $topology1Ports]
set topology2Obj [CreateTopology -name Topo-2 -portList $topology2Ports]

set deviceGroup1Obj [CreateDeviceGroup -topologyObj $topology1Obj -name DG-1 -multiplier 1]
set deviceGroup2Obj [CreateDeviceGroup -topologyObj $topology2Obj -name DG-2 -multiplier 1]

set ethernet1Obj [CreateEthernetNgpf \
		      -deviceGroupObj $deviceGroup1Obj \
		      -name Eth-1 \
		      -macAddress 00:01:01:01:00:01 -direction increment -step 00:00:00:00:00:01 \
		      -macAddressPortStep 00:00:00:00:00:01 \
		      -enableVlan false \
		     ]

set ethernet2Obj [CreateEthernetNgpf \
		      -deviceGroupObj $deviceGroup2Obj \
		      -name Eth-2 \
		      -macAddress 00:01:02:01:00:01 -direction increment -step 00:00:00:00:00:01 \
		      -macAddressPortStep 00:00:00:00:00:01 \
		      -enableVlan false \
		     ]

ConfigVlanIdNgpf -ethernetObj $ethernet1Obj -start 101 -step 0 -direction increment
ConfigVlanIdNgpf -ethernetObj $ethernet2Obj -start 101 -step 0 -direction increment

set ipv4Obj1 [CreateIpv4Ngpf -ethernetObj $ethernet1Obj -name IPv4-1 \
		  -ipAddress 1.1.1.1 -direction inrement -step 0.0.0.1 -ipv4PortStep 0.0.0.1 \
		 ]

set ipv4Obj2 [CreateIpv4Ngpf -ethernetObj $ethernet2Obj -name IPv4-2 \
		  -ipAddress 1.1.1.3 -direction inrement -step 0.0.0.1 -ipv4PortStep 0.0.0.1 \
	     ]

ConfigIpv4GatewayIpNgpf -ipv4Obj $ipv4Obj1 -gatewayIp 1.1.1.3 \
    -direction increment -step 0.0.0.1 -ipv4GatewayPortStep 0.0.0.1 

ConfigIpv4GatewayIpNgpf -ipv4Obj $ipv4Obj2 -gatewayIp 1.1.1.1 \
    -direction increment -step 0.0.0.1  -ipv4GatewayPortStep 0.0.0.1

ConfigBgpNgpf -ipv4Obj $ipv4Obj1 -dutIp 1.1.1.3  -direction increment -step 0.0.0.1
ConfigBgpNgpf -ipv4Obj $ipv4Obj2 -dutIp 1.1.1.1  -direction increment -step 0.0.0.1

StartAllProtocols

if {[VerifyAllProtocolSessionsNgpf]} {
    exit
}

set trafficItemObj [CreateTrafficItem \
			-name bgpTraffic \
			-trafficType ipv4 \
			-biDirection True \
			-trackBy {trackingenabled0} \
		       ]

CreateEndpoints -trafficItemObj $trafficItemObj -name flowGroup-1 -srcEndpoint $topology1Obj -dstEndpoint $topology2Obj

set configElementObj [GetConfigElementObj $trafficItemObj]
ConfigFrameSize -configElementObj $configElementObj -type increment -incrementFrom 68 -incrementTo 512 -incrementStep 1
ConfigFrameRate -configElementObj $configElementObj -type percentLineRate -rate 25
ConfigFramePayload -configElementObj $configElementObj -type custom -customRepeat True -customPattern ff

ConfigTrafficTransmissionControl -configElementObj ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1 -type fixedFrameCount -frameCount 80000

# For continuous traffic
#ConfigTrafficTransmissionControl -configElementObj ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1 -type continuous

RegenerateAllTrafficItems

if {[StartTraffic]} {
    exit
}

set stats [GetStats "Port Statistics"]
puts [KeylPrint stats]

set stats [GetStats "Flow Statistics"]
puts [KeylPrint stats]

set stats [GetStats "Traffic Item Statistics"]
puts [KeylPrint stats]

set txFrames [keylget stats flow.1.Tx_Frames]
set rxFrames [keylget stats flow.1.Rx_Frames]
set delta [expr $txFrames - $rxFrames]
puts "\nTxFrames: $txFrames  RxFrames: $rxFrames  Delta: $delta"

ixNet disconnect
