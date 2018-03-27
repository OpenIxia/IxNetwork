#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    Load a saved .ixncfg config file
#       - This script will use the ports from the saved config file.
#       - If you want to use different ports, then set portList [list [$ixChassisIp, $cardId, $portId] ...]
#    Verify port state
#    Start all protocols
#    Start traffic
#    Get stats

package req IxTclNetwork
package req Tclx

source api.tcl

set apiServerIp 192.168.70.3
set ixChassisIp 192.168.70.11
set ixNetworkVersion 8.40
#set portList []
set configFile /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/SampleScripts/bgp_ngpf_8.30.ixncfg

if {[Connect -apiServerIp $apiServerIp -ixNetworkVersion $ixNetworkVersion -osPlatform windows]} {
    exit
}

ConnectToIxChassis $ixChassisIp

if {[ReleasePorts]} {
    exit
}

if {[ClearPortOwnership]} {
    exit
}

if {[LoadConfigFile $configFile]} {
    exit
}

if {[AssignPorts $ixChassisIp]} {
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


