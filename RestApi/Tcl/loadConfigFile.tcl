#!/usr/local/ActiveTcl-8.6/bin/tclsh

# This is a sample script to show how to use the TCL rest.tcl package to execute ReST APIs.
# This script will connect to an IxNetwork API server and perform the followings:
# 
#    - Connect to an IxNetwork API server
#    - Load a saved JSON config file
#    - Reassign ports
#    - Start all protocols
#    - Start traffic
#    - Stop traffic
#    - Get stats
# 
# Requirements
#    - rest.tcl
#    - json.tcl
#    - tclRestLib.tcl
#    - ospf_ngpf_8.40.json

source tclRestLib.tcl
package require rest
package require json

set apiServer 192.168.70.3
set ixChassisIp 192.168.70.120
set port1 "$ixChassisIp,1,1"
set port2 "$ixChassisIp,1,2"
set portList [list ${port1} ${port2}]
set jsonFileName "ospf_ngpf_8.40.json"

if {[catch {
    set sessionUrl [connect -apiServerIp $apiServer -serverOs "windows"]
    importJsonConfigFile -jsonFileName $jsonFileName -option "newConfig" -sessionUrl $sessionUrl
    assignPorts -portList $portList -sessionUrl $sessionUrl
    startAllProtocols -sessionUrl $sessionUrl
    after 25000

    startTraffic -sessionUrl $sessionUrl
    after 30000

    stopTraffic -sessionUrl $sessionUrl
    after 5000

    set stats [getStats -viewName "Traffic Item Statistics" -sessionUrl $sessionUrl]
    foreach stat $stats {
        foreach {key value} $stat {
            puts "$key: $value"
        }
    }

    stopAllProtocols -sessionUrl $sessionUrl

} errMsg]} {
    puts "\nerrMsg: $errMsg"
}
