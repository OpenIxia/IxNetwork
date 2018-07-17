#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    Load a saved .ixncfg config file
#       - If you want to use different ports, then set portList [list [$ixChassisIp, $cardId, $portId] ...]
#    Verify port state
#    Start all protocols
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
# Suports Windows API server and Linux API server
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

set ixNetworkVersion 8.40
set licenseServerIp 192.168.70.3 ;# This could be on an ixChassisIp or a remote Windows PC.
set licenseMode subscription 
set licenseTier tier3

set ixChassisIp 192.168.70.11
set portList [list "$ixChassisIp 1 1" "$ixChassisIp 2 1"]
set port1 [list $ixChassisIp 1 1]
set port2 [list $ixChassisIp 2 1]

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

set topology1Obj [CreateTopology -name Topo-1 -portList [list $port1]]
set topology2Obj [CreateTopology -name Topo-2 -portList [list $port2]]

set deviceGroup1Obj [CreateDeviceGroup -topologyObj $topology1Obj -name DG-1 -multiplier 3]
set deviceGroup2Obj [CreateDeviceGroup -topologyObj $topology2Obj -name DG-2 -multiplier 3]

set ethernet1Obj [CreateEthernetNgpf \
		      -deviceGroupObj $deviceGroup1Obj \
		      -name Eth-1 \
		      -macAddress 00:01:01:01:00:01 -direction increment -step 00:00:00:00:00:01 \
		     ]

set ethernet2Obj [CreateEthernetNgpf \
		      -deviceGroupObj $deviceGroup2Obj \
		      -name Eth-2 \
		      -macAddress 00:01:02:01:00:01 -direction increment -step 00:00:00:00:00:01 \
		     ]

set ipv4Obj1 [CreateIpv4Ngpf -ethernetObj $ethernet1Obj -name IPv4-1 -ipAddress 1.1.1.1 -direction inrement -step 0.0.0.1]
set ipv4Obj2 [CreateIpv4Ngpf -ethernetObj $ethernet2Obj -name IPv4-2 -ipAddress 1.1.1.4 -direction inrement -step 0.0.0.1]

ConfigIpv4GatewayIpNgpf -ipv4Obj $ipv4Obj1 -gatewayIp 1.1.1.4 -direction increment -step 0.0.0.1
ConfigIpv4GatewayIpNgpf -ipv4Obj $ipv4Obj2 -gatewayIp 1.1.1.1 -direction increment -step 0.0.0.1

ConfigBgpNgpf -ipv4Obj $ipv4Obj1 -dutIp 1.1.1.4  -direction increment -step 0.0.0.1
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
#ConfigTrafficTransmissionControl -configElementObj ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1 -type continuous

RegenerateAllTrafficItems

if {[StartTraffic]} {
    exit
}

set stats [GetStats "Port Statistics"]
puts [KeylPrint stats]

set stats [GetStats]
puts [KeylPrint stats]

set txFrames [keylget stats flow.1.Tx_Frames]
set rxFrames [keylget stats flow.1.Rx_Frames]
set delta [expr $txFrames - $rxFrames]
puts "\nTxFrames: $txFrames  RxFrames: $rxFrames  Delta: $delta"


ixNet disconnect


