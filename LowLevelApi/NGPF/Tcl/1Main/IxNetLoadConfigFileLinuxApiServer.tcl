#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    Load a saved .ixncfg config file
#    Verify port state
#    Start all protocols
#    TODO: Verify protocol sessions
#    Start traffic
#    Get stats

#package req IxTclNetwork
package req IxTclNetworkLinuxApiServer
package req Tclx

source api.tcl

set apiServerIp 192.168.70.108
set ixChassisIp 192.168.70.11
set ixNetworkVersion 8.40
set username admin
set password admin
set licenseServerIp 192.168.70.3
set licenseMode subscription
set licenseTier tier3

# For the Linux API server, the config file has to be in the same directory as the script.
set configFile bgp_ngpf_8.30.ixncfg

set apiKey [GetApiKey $apiServerIp $username $password]
if {$apiKey == 1} {
    exit
}
puts "\napiKey: $apiKey"

Connect $apiServerIp $ixNetworkVersion $apiKey

set sessions [ixNet getSessionInfo]
puts "\nSessionId: $sessions"

if {[LoadConfigFile $configFile]} {
    exit
}

ReleaseAllPorts
#ClearPortOwnership [list "$ixChassisIp 1 1" "$ixChassisIp 2 1"] 
ConfigLicenseServer $licenseServerIp $licenseMode $licenseTier

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




if 0 {
if {[Connect $apiServerIp $ixNetworkVersion]} {
    exit
}

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
}

ixNet disconnect


