#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    Load a saved .ixncfg config file
#       - This script could use the ports from the saved config file.
#       - If you want to use different ports, then set portList [list [$ixChassisIp, $cardId, $portId] ...]
#         and the APIs will use your $portList for ReleasePorts, ClearPortOwnership and AssignPorts
#
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
#    - TCL must have Tclx package
#      If you could, install ActiveState TCL. 
#
# Suports Windows API server and Linux API server
#

package req Tclx
source api.tcl

set osPlatform windows ;# windows|linux

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
set portList [list "$ixChassisIp 1 1" "$ixChassisIp 2 1"]
set configFile bgpNgpf_8.40.ixncfg

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

ConnectToIxChassis $ixChassisIp

if {[ReleasePorts $portList]} {
    exit
}

if {[ClearPortOwnership $portList]} {
    exit
}

# Configuring the license server details are optional. If you need to configure them,
# this is the spot to do it.  You need to release the ports before you could configure them.
if {[ConfigLicenseServer $licenseServerIp $licenseMode $licenseTier]} {
    exit
}

if {[LoadConfigFile $configFile]} {
    exit
}

if {[AssignPorts $ixChassisIp $portList]} {
    exit
}

if {[VerifyPortState]} {
    exit
}

StartAllProtocols

if {[VerifyAllProtocolSessionsNgpf]} {
    exit
}

set trafficItemObjectList [GetTrafficItemObjects "Topo1 to Topo2"]
set trafficItemObj [lindex $trafficItemObjectList 0]
set configElementObj [lindex $trafficItemObjectList 1]

#ConfigFrameSize -configElementObj $configElementObj -type fixed -frameSize 256
#ConfigFrameSize -configElementObj $configElementObj -type increment -randomMin 127 -randomMax 1514
ConfigFrameSize -configElementObj $configElementObj -type increment -incrementFrom 68 -incrementTo 512 -incrementStep 1

ConfigFrameRate -configElementObj $configElementObj -type percentLineRate -rate 25
ConfigFramePayload -configElementObj $configElementObj -type custom -customRepeat True -customPattern ff

ConfigTrafficTransmissionControl -configElementObj ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1 -type fixedFrameCount -frameCount 80000
#ConfigTrafficTransmissionControl -configElementObj ::ixNet::OBJ-/traffic/trafficItem:1/configElement:1 -type continuous

RegenerateAllTrafficItems

if {[StartTraffic]} {
    exit
}

set stats [GetStats]
puts [KeylPrint stats]

set txFrames [keylget stats flow.1.Tx_Frames]
set rxFrames [keylget stats flow.1.Rx_Frames]
set delta [expr $txFrames - $rxFrames]
puts "\nTxFrames: $txFrames  RxFrames: $rxFrames  Delta: $delta"

ixNet disconnect


