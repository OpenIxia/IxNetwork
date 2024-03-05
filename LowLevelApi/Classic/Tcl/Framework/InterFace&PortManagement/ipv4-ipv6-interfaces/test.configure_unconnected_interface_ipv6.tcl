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

#-----------------------------------------------------------------------------
# This script shows how to Add and modify and remove and IPv6 unconnected,
# interface connected via an connected interface.
#
# Sequence of events being carried out by the script
#    1) Adds 6 IPv6 connected interfaces on a port
#    2) Adds 6 Ipv6 un-connected interfaces via the connected interfaces
#    3) Modifies the properties of the 6 un-connected interfaces
#    4) Removes all the un-connected interfaces
# SCRIPT-GEN USED : No
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl
#-------------------------------------------------------------------------------
# PROCEDURE    : AddIp6Int
# PURPOSE      : Adding a Ipv6 connected interface.
# INPUT        : (1) Object ref to the virtual port
#                (2) Ipv6 address
# RETURN VALUE : Referance to the added interface
#-------------------------------------------------------------------------------
proc AddIp6Int {p1 ip} {
    set i1 [ixNet add $p1 interface]
    ixNet commit
    set i1 [ixNet remapIds $i1]
    puts "new interface global id: $i1"

    set ip1 [ixNet add $i1 ipv6]
    ixNet commit

    set ip1 [ixNet remapIds $ip1]
    puts "new ip6 global id: $ip1"
    ixNet setAttr $ip1 -ip $ip
    ixNet setAttr $ip1 -prefixLength 24
    ixNet commit

    ixNet setAttr $i1 -enabled true
    ixNet commit
    return $i1
}


#------------------------------------------------------------------------------
# PROCEDURE    : AddUnconnectedInt
# PURPOSE      : Adding an unconnected interface object via a connected
#                interface
# INPUT        : ref to the virtual port object and connected interface object.
# OUTPUT       : One unconnected interface will be added
#------------------------------------------------------------------------------
proc AddUnconnectedInt {p1 int} {

    set uc1 [ixNet add $p1 interface]
    ixNet setAttr $uc1 -type routed
    ixNet setAttr $uc1 -enabled true
    ixNet commit

    set uc1 [ixNet remapIds $uc1]
    ixNet setAttr $uc1/unconnected -connectedVia $int
    ixNet commit
    return $uc1
}


#------------------------------------------------------------------------------
# PROCEDURE    : ModifyIp4UnconnectedInt
# PURPOSE      : Modifying the property of the unconnected interface object.
# INPUT        : ref to the unconnected interface object, and ip address
# OUTPUT       : Modify the added unconnected interface as specified in this
#                proc
#------------------------------------------------------------------------------
proc ModifyIp6UnconnectedInt {p1 ip} {
    set flag 0
    ixNet setAttr $p1 -ip $ip
    ixNet commit

    if {$ip != [ixNet getAttr $p1 -ip]} {
       puts "** Get Attribute on ip failed"
       set flag 1
    }

    return $flag
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
    set pList [addVport $portData1 $portData2]
    set port1 [lindex $pList 0]
    set port2 [lindex $pList 1]

    puts "Configuring for 5 IPv6 interface ..."
    for {set i 1} {$i < 6} {incr i} {
        set i1($i) [AddIp6Int $port1 2004:0:0:0:0:0:0:$i]
        set i2($i) [AddIp6Int $port2 2005:0:0:0:0:0:0:$i]
    }

    # creating 6 ipv6 unconnected interface
    for {set i 1} {$i < 6} {incr i} {
        set unconn1($i) [AddUnconnectedInt $port1 $i1($i)]
        set unconn2($i) [AddUnconnectedInt $port2 $i2($i)]

        set ipv61($i) [ixNet add $unconn1($i) ipv6]
        set ipv62($i) [ixNet add $unconn2($i) ipv6]

        ixNet setAttr $ipv61($i) -ip 20:0:0:0:0:0:0:$i
        ixNet setAttr $ipv62($i) -ip 30:0:0:0:0:0:0:$i
        ixNet commit

        # Checking If the Unconnected Interface is Created or not
        # for first port only
        set index [lsearch [ixNet getList $port1 interface] $unconn1($i)]
        if {$index >= 0} {
            puts "Unconnected Interface ceated "
        } else {
            puts " Unconnected Interface ceation failed "
            ixNetCleanUp
            return $FAILED
        }
    }

    # Checking for the unconnected interface modification:
    for {set j 1} {$j < 6} {incr j} {

        set modify [ModifyIp6UnconnectedInt $ipv61($j) "40:0:0:0:0:0:0:1"]

        if {$modify == 1} {
           puts "IPv4 Unconnected Interface Modification test Failed"
           ixNetCleanUp
           return $FAILED
        } else {
           puts "IPv4 Unconnected Interface Modification test Passed"
        }
    }

    #Checking for removing Unconnected IPv6 Interface
    for {set j 1} {$j < 6} {incr j} {

        puts "Removing the Unconnecter Interface"
        ixNet remove $unconn1($j)
        ixNet commit

        set index [lsearch [ixNet getList $port1 interface] $unconn1(1)]

        if {$index >= 0} {
           puts "interface Remove : FAILED"
           ixNetCleanUp
           return $FAILED
        } else {
           puts "interface Remove : passed"
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

