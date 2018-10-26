#!/usr/bin/tclsh

# Description
#    Sample to demonstrate how to use TCL to send ReST APIs.

# Requirements
#     - rest, json and tdom
#     - yum install tcllib, tcltls, tcl-devel
#     - Get and install tdom package:
#          - https://centos.pkgs.org/6/puias-computational-i386/tdom-0.8.2-11.sdl6.i686.rpm.html
#          - rpm -Uvh <tdom file>
#
# Notes:
#   set jsonData [json::json2dict $jsonStuff]
#   TLS: http://wiki.tcl.tk/1475
#   ActiveStateTCL 8.6 has all the required packages. Use ActiveStateTCL if you are having problems with your native TCL.
#   
package req rest
package req json

# Uncomment this if using HTTPS
#package req tls
#http::register https 443 ::tls::socket

set apiServer 192.168.70.3
set apiServerPort 11009
set ixChassisIp 192.168.70.128
set port1 "$ixChassisIp 1 1"
set port2 "$ixChassisIp 1 2"
set portList [list $port1 $port2]

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

set httpHeader "https://$apiServer:$apiServerPort"

# POST
set url $httpHeader/api/v1/sessions/1/ixnetwork/topology
set response [post $url {{"name": "BGP_Topology", "vports": ["/api/v1/sessions/1/ixnetwork/vport/1"]}}]
set state [dict get $response links]

# GET
set url $httpHeader/api/v1/sessions/1/ixnetwork/topology
set response [get $url]
puts "\nGET response: $response"

# PATCH
set url $httpHeader/api/v1/sessions/1/ixnetwork/topology/1
set result [patch $url {{"name": "OSPF_Topology"}}]





