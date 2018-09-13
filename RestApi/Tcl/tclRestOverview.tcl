#!/usr/local/ActiveTcl-8.6/bin/tclsh

# Notes:
#   set jsonData [json::json2dict $jsonStuff]
#   TLS: http://wiki.tcl.tk/1475

package req rest
package req json

set apiServer 192.168.70.3
set apiServerPort 11009
set ixChassisIp 192.168.70.11
set port1 "$ixChassisIp 1 1"
set port2 "$ixChassisIp 2 1"
set portList [list $port1 $port2]
set httpHeader "http://$apiServer:$apiServerPort"

proc get {url} {
    puts "\nGET: $url"
    set header [list Content-type application/json]
    set config [list method get format json headers $header]
    set response [::rest::simple $url {} $config]
    return $response
    #set currentState [dict get $response state]
}

proc post {url jsonData} {
    puts "POST: $url"
    puts "DATA: $jsonData"
    set header [list Content-type application/json]
    set config [list method post format json headers $header result json]
    set response [::rest::simple $url {} $config $jsonData]
    return $response
}

proc patch {url jsonData} {
    puts "PATCH: $url"
    puts "DATA: $jsonData"
    set header [list Content-type application/json]
    set config [list method patch format json headers $header]
    set response [::rest::simple $url {} $config $jsonData]
    return $response
}

# GET
set url $httpHeader/api/v1/sessions/1/ixnetwork/topology
set response [get $url]
puts "\nGET response: $response"

# POST
set url $httpHeader/api/v1/sessions/1/ixnetwork/topology
set response [post $url {{"name": "BGP_Topology", "vports": ["/api/v1/sessions/1/ixnetwork/vport/1"]}}]
set state [dict get $response links]

# PATCH
set url $httpHeader/api/v1/sessions/1/ixnetwork/topology/1
set result [patch $url {{"name": "OSPF_Topology"}}]





