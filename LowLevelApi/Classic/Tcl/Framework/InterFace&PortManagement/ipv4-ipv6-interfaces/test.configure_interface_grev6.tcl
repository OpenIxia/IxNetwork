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
#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to Add and remove an IPv6 GRE interface,
# connected via an ipv4 interface.
#
# Sequence of events being carried out by the script
#    1) Add one IPv4 interface per port
#    2) Add six IPv6 GRE interface connected via the IPv4 interface
#    3) Remove all the IPv6 GRE interface.
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#------------------------------------------------------------------------------
# PROCEDURE    : AddGREIntv6
# PURPOSR      : Adding IPv6 GRE interface
# INPUT        : (1) object referance to the port where ipv4 GRE interface
#                    is added
#                (2) object referance of the interface on which GRE interface
#                    to be added
#                (3) The destination IPv6 address
#                (4) The interface IPv6 address
# OUTPUT       : IPv4 Interface will be added in the IxNetwork GUI.
# RETURN VALUE : ref to added interface
#------------------------------------------------------------------------------
proc AddGREIntv6 {p1 int dst ip6} {
    set i1 [ixNet add $p1 interface]
    ixNet setAttr $i1 -type gre
    ixNet setAttr $i1 -enabled true
    ixNet commit

    set ip [ixNet add $i1 ipv6]
    ixNet setAttr $ip -ip $ip6
    ixNet commit

    set i1 [ixNet remapIds $i1]

    set g1 [ixNet add $int gre]
    ixNet setAttr $g1 -dest $dst
    ixNet setAttr $g1 -inKey 5
    ixNet setAttr $g1 -outKey 0
    ixNet setAttr $g1 -useChecksum true
    ixNet setAttr $g1 -useSequence true
    ixNet setAttr $g1 -useKey true
    ixNet setAttr $g1 -source $ip
    ixNet commit

    ixNet setAttr $i1 -enabled true
    ixNet commit

    set i1 [ixNet remapIds $i1]
    return $i1
}


#------------------------------------------------------------------------------
# PROCEDURE    : AddIp4Int
# PURPOSR      : Adding IPv4 interface (connected)
# INPUT        : (1) object referance of the port on which ip4 interface
#                    "object" to be added
#                (2) The IPv4 address
#                (3) The concerned gateway
# OUTPUT       : IPv4 Interface will be added in the IxNetwork GUI.
# RETURN VALUE : ref to added interface
#------------------------------------------------------------------------------
proc AddIp4Int {p1 ip gateway} {
    set i1 [ixNet add $p1 interface]
    ixNet commit
    set i1 [ixNet remapIds $i1]
    set ip1 [ixNet add $i1 ipv4]
    ixNet setAttr $ip1 -ip $ip
    ixNet setAttr $ip1 -gateway $gateway
    ixNet setAttr $ip1 -maskWidth 24
    ixNet setAttr $i1 -enabled true
    ixNet commit
    set i1 [ixNet remapIds $ip1]
    return $i1
}


#------------------------------------------------------------------------------
# PROCEDURE    : Action
# PURPOSE      : Encapsulating all of your testing actions
# INPUT        : (1) [list $chassis1 $card1 $port1 $client1 $tcpPort1]
#                (2) [list $chassis2 $card2 $port2 $client2 $tcpPort2]
#                (3) home; (the current directory)
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc Action {portData1 portData2} {

    # initialize return value
    set FAILED 1
    set PASSED 0

    puts "Executing from [pwd]"
    puts "connecting to client"
    set pList [getPortList $portData1 $portData2]
    set port1 [lindex $pList 0]
    set port2 [lindex $pList 1]

    puts " Configuring for IPv4..."
    set i1 [AddIp4Int $port1 20.20.20.1 20.20.20.2]
    set i2 [AddIp4Int $port2 20.20.20.2 20.20.20.1]

    set ilist1 [ixNet getList $port1 interface]
    set int1   $i1
    set int2   $i2
    set i1     [lindex $ilist1 [expr {[llength $ilist1] - 1}]]
    set ilist2 [ixNet getList $port2 interface]
    set i2     [lindex $ilist2 [expr {[llength $ilist1] - 1}]]

    puts "Add GRE interface"
    set b 5
    set c 55

    for {set a 1} {$a<6} {incr a} {
        set  g1($a) [AddGREIntv6 $port1 $i1  "20.20.20.2" \
                                 "$b:$b:$b:$b:$b:$b:$b:$b"]

        set  g2($a) [AddGREIntv6 $port2 $i2  "20.20.20.1" \
                                 "$c:$c:$c:$c:$c:$c:$c:$c"]

        set  ilist1 [ixNet getList $port1 interface]
        set  g [lindex $ilist1 [expr {[llength $ilist1] - 1}]]

        incr b
        incr c

        puts "Checking if the GRE interfaces are created or not"
        set x [split $g ":"]
        set y [lindex $x 6]

        if { $y == [expr $a + 1] } {
            puts " No $a GRE IPv6 interfaces is created in the First port "

        } else {
            puts " The No $a GRE interfaces is not created in th First port"
            ixNetCleanUp
            return $FAILED
        }
    }

    puts "Removing and checking if the GRE interface is removed or not"
    for {set a 1} {$a<6} {incr a} {
        ixNet remove $g2($a)
        ixNet commit
        set index [lsearch [ixNet getList $port1 interface] $g2($a)]
        if {$index >= 0} {
            puts " IPv6 GRE interface Remove : FAILED"
            ixNetCleanUp
            return $FAILED
        } else {
            puts " IPv6 GRE interface Remove in the 2ed Port: passed"
        }
    }

    ## Needs to remove assigned ports after test
    ixNetCleanUp
    return $PASSED
}


#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action

