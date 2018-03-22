#!/opt/ActiveTcl-8.5/bin/tclsh

# Description
#    This sample script shows how to prepare and use ixNet low level TCL API with the Linux API server.
#
#    Load a saved .ixncfg config file 
#    Verify port state
#    Start all protocols
#    TODO: Verify protocol sessions
#    Start traffic
#    Get stats

# To support ixNet low level API against the Linux API server:
#
#   
#   - Version from 8.0 up to 8.40, you need to download the IxTclNetwork package from the Linux API server.
#   - The problem is that the IxTclNetwork in it is the same file name as the installed IxNetwork file in the lib directory.
#   - This is one way to handle the filename conflict.
#
#   - Untar it.
#   - Put it in the Ixia installation folder: /ixia/ixnetwork/8.40.1124.8/lib/IxTclNetwork and rename it to LinuxApiServer:
#          Example: /ixia/ixnetwork/8.40.1124.8/lib/IxTclNetwork/LinuxApiServer
#   - Go into the LinuxApiServer folder and:
#       - Rename IxTclNetwork to IxTclNetworkLinuxApiServer.tcl
#       - Edit pkgIndex.tcl
#       
#           set env(IXTCLNETWORK_8.40.1124.8) [file dirname [info script]]
# 
#           package ifneeded IxTclNetworkLinuxApiServer 8.40.1124.8 {
#           package provide IxTclNetworkLinuxApiServer 8.40.1124.8
#           source [file join $env(IXTCLNETWORK_8.40.1124.8) LinuxApiServer/IxTclNetworkLinuxApiServer.tcl]
#           source [file join $env(IXTCLNETWORK_8.40.1124.8) LinuxApiServer/HighLevelAPI.tcl]
#
#    - Install ActiveTcl to get the tls and http packages because the Linux API server requires it.
#    - Add tls and http paths to TCLLIBPATH:
#
#         export linuxApiServer=${ixTclNetwork}/LinuxApiServer
#         export tclTls=/opt/ActiveTcl-8.5/./lib/teapot/package/linux-glibc2.3-x86_64/lib/tls1.6.4
#         export tclHttp=/opt/ActiveTcl-8.5/lib/tcl8.5/http1.0
#         export TCLLIBPATH="$IXOS_API_HOME $HLT_HOME $HLT_LIBRARY ${IXLOAD_HOME}/lib $ixLoadComm $ixTclNetwork $linuxApiServer $tclTls $tclHttp"
# 
#    - Add ActiveTcl to .bashrc PATH
#         export PATH="/opt/ActiveTcl-8.5/bin:/usr/local/git-2.15.1/libexec/git-core:/usr/local/python3.6.3/bin:$PATH"
#
#    - In the scripts, package req IxTclNetworkLinuxApiServer


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
set portList [list "$ixChassisIp 1 1" "$ixChassisIp 2 1"]

# For the Linux API server, the config file has to be in the same directory as the script.
set configFile bgp_ngpf_8.30.ixncfg

set apiKey [GetApiKey $apiServerIp $username $password]
if {$apiKey == 1} {
    exit
}

Connect $apiServerIp $ixNetworkVersion $apiKey

set sessions [ixNet getSessionInfo]
puts "\nSessionId: $sessions"

ConfigLicenseServer $licenseServerIp $licenseMode $licenseTier

if {[LoadConfigFile $configFile]} {
    exit
}


ReleasePorts $portList
ClearPortOwnership $portList
GetPortsAndAssignPorts $ixChassisIp

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


