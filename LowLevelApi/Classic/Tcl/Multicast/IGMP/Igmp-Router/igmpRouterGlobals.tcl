################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

#-----------------------------------------------------------------------------------
# Name : igmp_router_global.tcl
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
