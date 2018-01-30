#!/bin/tclsh

# Description
#
# 1> Load a config file
# 2> Do a scriptgen on the config
#       You could generate a tcl, perl or python file.
# 
# The script of our entire configuration will be saved on the path
# where you executed the script.  You could change the filename and path
# as well.
#

package req IxTclNetwork

set ixNetworkWindows 10.219.117.103
set ixNetworkVersion 8.10

# tcl, perl or python
set language tcl
set extension tcl

puts "Connect to IxNetwork"
ixNet connect $ixNetworkWindows -port 8009 -version $ixNetworkVersion -setAttribute strict

# Uncomment this if you want to load a saved config file first
if 0 {
set confName intf_b2b_traf_flow.cfg

puts "Loading $confName"
ixNet exec loadConfig [ixNet readFrom $confName]
}


set random [clock clicks -milliseconds]

set testName [file tail [info script]]
set testName intf_b2b_traf_flow
set scriptGenFileName "[string map {"test." "tmp."} $testName].$random.${extension}"

ixNet setMultiAttribute /globals/scriptgen \
    -serializationType      ixNet          \
    -language               $language      \
    -linePerAttribute       true           \
    -includeConnect         true           \
    -includeTestComposer    false
#-connectHostname        
#-connectPort            
#-connectVersion  
       
ixNet setMultiAttribute /globals/scriptgen/ixNetCodeOptions \
    -includeTrafficStack       true                         \
    -includeTrafficFlowGroup   true                         \
    -includeTraffic            true                         \
    -includeStatistic          true                         \
    -includeQuickTest          true                         \
    -includeDefaultValues      true                         \
    -includeStatistic          true                         \
    -includeTestComposer       false                        \
    -includeAvailableHardware  true
ixNet commit

puts "Create the low level scriptgen for $language '$scriptGenFileName'"
ixNet exec generate /globals/scriptgen [ixNet writeTo $scriptGenFileName -overwrite]
