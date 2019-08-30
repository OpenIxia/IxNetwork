
# Description
#    - This sample script shows how to prepare and use ixNet low level TCL API with the Linux API server.
#    
#    Load a saved .ixncfg config file 
#       - This script will automatically get the ports from the saved config file.
#       - If you want to use different ports, then set portList [list [chassisIp, cardId, portId] ...]
#    Verify port state
#    Start all protocols
#    TODO: Verify protocol sessions
#    Start traffic
#    Get stats
#
# Requirements
#    - TCL pacakges: tls, json, http, 
# To support ixNet low level API against the Linux API server:
#
#   Get IxTclNetwork.tcl:   
#       - Version from 8.0 up to 8.40, you need to download the IxTclNetwork package from the Linux API server.
#       - On a web browser, enter the IP address of your Linux API server.
#       - Login admin/admin.
#       - Click on "Download A Client"
#
#   - The problem is that the IxTclNetwork is the same file name as the installed IxNetwork file in the lib directory.
#   - You don't want to overwrite the existing file.  Ixia is addressing this issue on the next release.
#   - We are going to rename IxTclNetwork to IxTclNetworkLinuxApiServer in order to support both Windows and Linux.
#   - Below is a way to handle the filename conflict.
#
#   - After you downloaded the IxTclNetwork.py file, untar it.
#
#   - Put it in the Ixia installation folder: /path_to_ixia_installation/ixia/ixnetwork/8.40.1124.8/lib/IxTclNetwork/LinuxApiServer and rename it to LinuxApiServer:
#
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
# Optional:
#
#   Install ActiveTcl to get the tls and http packages because the Linux API server requires it.
#     - Add tls and http paths to TCLLIBPATH:
#
#         export linuxApiServer=${ixTclNetwork}/LinuxApiServer
#         export tclTls=/opt/ActiveTcl-8.5/./lib/teapot/package/linux-glibc2.3-x86_64/lib/tls1.6.4
#         export tclHttp=/opt/ActiveTcl-8.5/lib/tcl8.5/http1.0
#         export TCLLIBPATH="$IXOS_API_HOME $HLT_HOME $HLT_LIBRARY ${IXLOAD_HOME}/lib $ixLoadComm $ixTclNetwork $linuxApiServer $tclTls $tclHttp"
# 
#     - Add ActiveTcl to .bashrc PATH
#         export PATH="/opt/ActiveTcl-8.5/bin:/usr/local/git-2.15.1/libexec/git-core:/usr/local/python3.6.3/bin:$PATH"
#
#     - In the scripts, add: package req IxTclNetworkLinuxApiServer

# For ixNetwork version prior to 9.0
#package req IxTclNetworkLinuxApiServer
#package req Tclx

# For ixNetwork version 9.0+
package req IxTclNetwork
source api.tcl

set apiServerIp 192.168.70.12

set ixNetworkVersion 9.00
set username admin
set password admin
set licenseServerIp 192.168.70.3
set licenseMode subscription
set licenseTier tier3

set ixChassisIp 192.168.70.128
set portList [list "$ixChassisIp 1 1" "$ixChassisIp 2 1"]

set configFile bgp_ngpf_8.30.ixncfg

if {[Connect -apiServerIp $apiServerIp -ixNetworkVersion $ixNetworkVersion -osPlatform linux -username admin -password admin]} {
    exit
}

set sessions [ixNet getSessionInfo]
puts "\nSessionId: $sessions"

ConfigLicenseServer $licenseServerIp $licenseMode $licenseTier

if {[LoadConfigFile $configFile]} {
    exit
}

if {[ReleasePorts]} {
    exit
}

if {[ClearPortOwnership]} {
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

#ixNet disconnect


