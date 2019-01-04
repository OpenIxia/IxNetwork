#!/usr/bin/tclsh

# Description
#     This script assumes that a configuration exists.
#      
#     - Connect to an existing configuration
#     - Set capture port to capture software and hardware
#     - Set traffic type to continuous mode.
#     - Start traffic
#     - Start capture
#     - Stop capture
#     - save the capture file on the server
#     - Copy the .cap file off the API server to local filesystem

package req IxTclNetwork

# For Linux API server.
# These packages comes with IxTclNetwork starting with IxNetwork 8.50
package require http
package require json
package require tls
::http::register https 443 ::tls::socket

# Use some procs from the api.tcl library in the same directory.
source api.tcl

set osPlatform linux;# windows|linux

if {$osPlatform == "windows"} {
    set apiServerIp 192.168.70.3
}

if {$osPlatform == "linux"} {
    set apiServerIp 192.168.70.12
}

set ixNetworkVersion 8.50
#set licenseServerIp 192.168.70.3 ;# This could be on an ixChassisIp or a remote Windows PC.
#set licenseMode subscription
#set licenseTier tier3

set ixChassisIp 192.168.70.128
set portList [list "$ixChassisIp 1 1" "$ixChassisIp 1 2"]
set port1 [list $ixChassisIp 1 1]
set port2 [list $ixChassisIp 1 2]

set apiKey [ixNet getApiKey $apiServerIp -username admin -password admin]
puts "\napiKey: $apiKey"

puts "Connecting to Linux API server ..."
if {[Connect -osPlatform linux -apiServerIp 192.168.70.12 -port 443 -ixNetworkVersion 8.50 -sessionId 1 -apiKey $apiKey -closeServerOnDisconnect 0] == 1} {
    exit
}

set sessions [ixNet getSessionInfo]
puts "\nSessionId: $sessions"

# Connect to Windows
#ixNet connect 192.168.70.3 -port 8009 -version 8.50 -setAttribute strict

# For this sample, vport2 is the capturing port
set vportList [ixNet getList [ixNet getRoot] vport]
set vport2 [lindex $vportList 1]
set vportName [ixNet getAttribute $vport2 -name]

set trafficItem [ixNet getList [ixNet getRoot]/traffic trafficItem]
set configElement [ixNet getList $trafficItem configElement]

ixNet setAttribute $vport2 -rxMode captureAndMeasure
ixNet setMultiAttribute $vport2/capture -softwareEnabled true -hardwareEnabled true
ixNet setAttribute $configElement/transmissionControl -type continuous
ixNet commit

RegenerateAllTrafficItems
StartTraffic
StartCapture

puts "Letting traffic run for 10 seconds ..."
after 10000

StopCapture
StopTraffic

set serverFileLocation packetCapture ;# For Linux

set capturedFile [SaveCaptureFiles $serverFileLocation]

# Just get one captured file for this example
set capturedFile [lindex $capturedFile 0]
puts "\nCaptured file: $capturedFile"

# For Windows. Copy the .cap file out of the API server
#catch {ixNet exec copyFile [ixNet readFrom "c:\\Results\\Port2_HW.cap" -ixNetRelative] [ixNet writeTo ./port2_cap.cap -overwrite]} errMsg

CopyFileFromLinuxApiServer \
    -apiServerIp $apiServerIp \
    -sessionId 1 \
    -apiKey $apiKey \
    -pathExtension /captures/packetCapture \
    -srcFile port2_HW.cap \
    -dstFilePath ./port2_Hw.cap




