#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    Load a saved .ixncfg config file
#    Verify port state
#    Start all protocols
#    TODO: Verify protocol sessions
#    Start traffic
#    Get stats

package req IxTclNetwork
package req Tclx

source api.tcl

set apiServerIp 192.168.70.3
set ixChassisIp 192.168.70.11
set ixNetworkVersion 8.40
set portList [list "$ixChassisIp 1 1" "$ixChassisIp 2 1"]

set configFile /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/SampleScripts/bgp_ngpf_8.30.ixncfg

if {[Connect $apiServerIp $ixNetworkVersion]} {
    exit
}

ReleaseAllPorts

#ReleasePorts "$ixChassisIp 1 1"

ClearPortOwnership $portList

if {[LoadConfigFile $configFile]} {
    exit
}

if {[VerifyPortState]} {
    exit
}

StartAllProtocols

if {[VerifyAllProtocolSessionsNgpf]} {
    exit
}

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


