#-----------------------------------------------------------------------------------
# Name : igmp_router_global.tcl
# Author : Suvendu M
# Purpose : Global variables needed for scripting and common to most of the
#           test cases are defined in this file. This will facilitate in
#           incorporating changes in variable names easily.
#
#------------------------------------------------------------------------------------
global topologyGlobals igmpGlobals
set topologyGlobals(b2b) 2
set igmpGlobals(s0) "0.0.0.0"
set cnt 1

# Creating 508 group and source IPs
for {set 3rdByte 1} {$3rdByte <= 2} {incr 3rdByte} {
    for {set 4thByte 1} {$4thByte <= 254} {incr 4thByte} {
        set igmpGlobals(s$cnt) "1.1.$3rdByte.$4thByte"

        set igmpGlobals(hexS$cnt) "01 01 [format %02x $3rdByte] \
            [format %02x $4thByte]"

        set igmpGlobals(g$cnt) "224.1.$3rdByte.$4thByte"

        set igmpGlobals(hexG$cnt) "e0 01 [format %02x $3rdByte] \
            [format %02x $4thByte]"
        incr cnt
    }
}

set igmpGlobals(defRV)            2
set igmpGlobals(defQI)            125
set igmpGlobals(defQRI)           10
set igmpGlobals(qi1)              60
set igmpGlobals(ohpi1)            [expr $igmpGlobals(defRV) * $igmpGlobals(qi1) + \
                                        $igmpGlobals(defQRI)]
set igmpGlobals(lmqc)             4
set igmpGlobals(lmqi)             5
set igmpGlobals(lmqt)             [expr $igmpGlobals(lmqc)*$igmpGlobals(lmqi)]
set igmpGlobals(v1)               "igmpv1"
set igmpGlobals(v2)               "igmpv2"
set igmpGlobals(v3)               "igmpv3"
set igmpGlobals(ex)               "exclude"
set igmpGlobals(in)               "include"
set igmpGlobals(protocolWaitTime) 10
set igmpGlobals(maxGrpCount)      400
set igmpGlobals(maxQurCount)      100
set igmpGlobals(hexRtrIp1)        "0b 01 01 01"
set igmpGlobals(hexRtrIp2)        "0b 01 01 02"
