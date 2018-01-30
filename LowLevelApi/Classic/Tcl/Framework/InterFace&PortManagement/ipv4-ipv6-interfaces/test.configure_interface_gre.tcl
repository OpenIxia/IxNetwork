#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to Add and modify an IPv4 GRE interface,
# connected via an ipv4 interface.
#
# Sequence of events being carried out by the script
#     1) Adds one IPv4 intrface per port
#     2) Adds one IPv4 GRE interface connected via IPv4 interface.
#     3) Modifies the added GRE interfaces
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

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
proc AddIp4Int {p1 ip gateway } {
    set i1 [ixNet add $p1 interface]
    ixNet commit

    set i1 [ixNet remapIds $i1]
    set ip1 [ixNet add $i1 ipv4]

    ixNet setAttr $ip1 -ip $ip
    ixNet setAttr $ip1 -gateway $gateway
    ixNet setAttr $ip1 -maskWidth 24
    ixNet setAttr $i1 -enabled true
    ixNet commit

    set i1 [ixNet remapIds $i1]
    return $i1
}


#------------------------------------------------------------------------------
# PROCEDURE    : AddIp6Int
# PURPOSR      : Adding IPv6 interface (connected)
# INPUT        : (1) object referance of the port on which ip6 interface
#                    "object" to be added
#                (2) The IPv6 address
# OUTPUT       : IPv6 Interface will be added in the IxNetwork GUI.
# RETURN VALUE : ref to added interface
#------------------------------------------------------------------------------
proc AddIp6Int { p1 ip } {
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
# PROCEDURE    : AddGREInt
# PURPOSR      : Adding GRE interface
# INPUT        : (1) object referance of the port on which GRE interface
#                    "object" to be added
#                (2) object referance of the interface which will be "source IP"
#                (3) Destination IP of the GRE interface
#                (4) IP address of the GRE Interface
# OUTPUT       : GRE Interface will be added in the IxNetwork GUI.
# RETURN VALUE : ref to added interface
#------------------------------------------------------------------------------
proc AddGREInt { p1 int dst ip } {
     set i1 [ixNet add $p1 interface]
     ixNet setAttr $i1 -type gre
     ixNet setAttr $i1 -enabled true
     ixNet commit

     set ip1 [ixNet add $i1 ipv4]
     ixNet setAttr $ip1 -ip $ip
     ixNet commit

     set i1 [ixNet remapIds $i1]

     set g1 [ixNet add $i1 gre]
     ixNet setAttr $g1 -dest $dst
     ixNet setAttr $g1 -inKey 5
     ixNet setAttr $g1 -outKey 0
     ixNet setAttr $g1 -useChecksum true
     ixNet setAttr $g1 -useSequence true
     ixNet setAttr $g1 -useKey       true
     ixNet setAttr $g1 -source       $int/ipv4
     ixNet setAttr $i1 -enabled true
     ixNet commit

     set g1 [ixNet remapIds $g1]
     return $g1
}


#------------------------------------------------------------------------------
# PROCEDURE    : ModifyGREInt
# PURPOSR      : Modifying the properties of the GRE interface
# INPUT        : (1) object referance of the interface which will be "source IP"
#                (2) object referance of the port on which GRE interface
#                    "object" is added
#                (3) object referance of the GRE interface to be modified.
#                (4) A flag indicating if it is a ipv4 gre interface
#                   (1 == ipv4) any other value stands for Ipv6
# OUTPUT       : GRE Interface properties will be modified as specified in
#                this procedure.
# RETURN VALUE : ref to added interface
#------------------------------------------------------------------------------
proc ModifyGREInt { int p1 g1 ipv4} {
     set flag 0

    set inKey               36
    set outKey              63
    set useChecksum         false
    set useSequence         false
    set useKey              true

    if {$ipv4 == 1} {
        set source      $int/ipv4
        set dest        3.3.3.3
    } else {
        set source      $int/ipv6:1
        set dest        2001:0:0:0:0:0:0:1
    }

    set enable true

    puts "Changing the initial parameters of the GRE interface"
    ixNet setAttr $g1  -dest         $dest
    ixNet setAttr $g1  -inKey        $inKey
    ixNet setAttr $g1  -outKey       $outKey
    ixNet setAttr $g1  -useChecksum  $useChecksum
    ixNet setAttr $g1  -useSequence  $useSequence
    ixNet setAttr $g1  -useKey       $useKey
    ixNet setAttr $g1  -source       $source
    ixNet setAttr $int -enabled     $enable
    ixNet commit
    puts "Changing parameters done !"

    if {$inKey  !=  [ixNet getAttr $g1 -inKey]} {
        puts "** Get Attribute on inKey failed"
        set flag 1
    }

    if {$outKey  !=  [ixNet getAttr $g1 -outKey]} {
        puts "Get Attribute failed on outKey"
        set flag 1
    }

    if {$useChecksum != [ixNet getAttr $g1 -useChecksum]} {
        puts "** Get Attribute on useChecksum failed"
        set flag 1
    }

    if {$useSequence  !=  [ixNet getAttr $g1 -useSequence]} {
        puts "** Get Attribute on useSequence failed"
        set flag 1
    }

    if {$useKey != [ixNet getAttr $g1 -useKey]} {
        puts "** Get Attribute on useKey failed"
        set flag 1
    }

    if {$source  !=  [ixNet getAttr $g1 -source]} {
        puts "** Get Attribute on source failed"
        set flag 1
    }

    if {$enable  !=  [ixNet getAttr $int -enabled]} {
        puts "Get Attribute failed on enable"
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
    set pList [getPortList $portData1 $portData2]

    set port1 [lindex $pList 0]
    set port2 [lindex $pList 1]
    puts "vitrual ports are port1 = $port1"
    puts "vitrual ports are port1 = $port1"

    set ipv4 1
    if {$ipv4 == 1} {
        puts "Configuring for IPv4 interface ..."
        set i1 [AddIp4Int $port1 20.20.20.1 20.20.20.2]
        set i2 [AddIp4Int $port2 20.20.20.2 20.20.20.1]
    } else {
        puts "Configuring for IPv6..."
        set i1 [AddIp6Int $port1 2004:0:0:0:0:0:0:1]
        set i1 [AddIp6Int $port1 2004:0:0:0:0:0:0:2]
        set i1 [AddIp6Int $port1 2004:0:0:0:0:0:0:3]
        set i1 [AddIp6Int $port1 2004:0:0:0:0:0:0:4]
        set i1 [AddIp6Int $port1 2004:0:0:0:0:0:0:5]
        set i2 [AddIp6Int $port2 2004:0:0:0:0:0:0:6]
    }

    set ilist1 [ixNet getList $port1 interface]
    set i1     [lindex $ilist1 [expr {[llength $ilist1] - 1}]]
    set ilist2 [ixNet getList $port2 interface]
    set i2     [lindex $ilist2 [expr {[llength $ilist2] - 1}]]

    # Add GRE Interface
    puts "Adding GRE interface ..."
    set g1 [AddGREInt $port1 $i1 1.1.1.1 5.5.5.5]
    set g2 [AddGREInt $port2 $i2 2.2.2.2 6.6.6.6]
    puts "Interface adding complete !!"

    set int $port1/interface:2
    set gre $int/gre

    puts "Modifying gre interface ...."
    set modify [ModifyGREInt $i1 $port1 $gre 1]
    if {$modify == 1} {
       puts "GRE Interface test Failed"
       ixNetCleanUp
       return $FAILED
    } else {
       puts "GRE Interface test Passed !!"
    }
    puts "Gre interface Modification done !!"

    ## Needs to remove assigned ports after test
    ixNetCleanUp
    return $PASSED
}

#-----------------------------------------------------------------------------#
# Execute the Action procedure defined above                                  #
#-----------------------------------------------------------------------------#
Execute_Action

