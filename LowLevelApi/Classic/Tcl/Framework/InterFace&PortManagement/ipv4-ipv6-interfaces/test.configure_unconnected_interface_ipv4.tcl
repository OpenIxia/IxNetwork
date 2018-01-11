#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to Add and modify and remove and IPv4 unconnected,
# interface connected via an connected interface.
#
# Sequence of events being carried out by the script
#    1) Adds 11 IPv4 connected interfaces on a port
#    2) Adds 11 Ipv4 un-connected interfaces via the connected interfaces
#    3) Modifies the properties of the 11 un-connected interfaces
#    4) Removes all the un-connected interfaces
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#------------------------------------------------------------------------------
# PROCEDURE    : AddInterface
# PURPOSE      : Adding an interface to the GUI
# INPUT        : Virtual port info
# OUTPUT       : one virtual port will be added
# ASSUMPTION   : This is just an blank interface, no IPv4/IPv6 object is there
#------------------------------------------------------------------------------
proc AddInterface {port} {
    set i1 [ixNet add $port interface]
    ixNet commit
    set i1 [ixNet remapIds $i1]
    puts "new interface global id: $i1"

    return $i1
}


#------------------------------------------------------------------------------
# PROCEDURE    : AAddIPv4Add
# PURPOSE      : Adding an IPv4 address object to an existing interface object
# INPUT        : ref to the interface object, ip address of the interface,
#                gateway
# OUTPUT       : one Ipv4 interface will be added.
#------------------------------------------------------------------------------
proc AddIPv4Add {i1 ip gateway} {

    set ip1 [ixNet add $i1 ipv4]
    #set i1 [ixNet add $p1 interface]
    ixNet commit
    set i1 [ixNet remapIds $i1]

    ixNet setAttr $ip1 -ip $ip
    ixNet setAttr $ip1 -gateway $gateway
    ixNet setAttr $ip1 -maskWidth 24
    ixNet setAttr $i1 -enabled true
    ixNet commit
    set i1 [ixNet remapIds $ip1]

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
proc ModifyIp4UnconnectedInt {p1 ip} {
    set flag 0
    set maskWidth 16
    ixNet commit

    ixNet setAttr $p1 -ip $ip
    ixNet setAttr $p1 -maskWidth $maskWidth
    ixNet commit

    if {$ip != [ixNet getAttr $p1 -ip]} {
        puts "** Get Attribute on ip failed"
        set flag 1
    }

    if {$maskWidth != [ixNet getAttr $p1 -maskWidth]} {
        puts "Get Attribute failed on maskWidth"
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

    puts "Configuring for connected IPv4 interface..."
    set a1 [AddInterface $port1]
    set b1 [AddIPv4Add $a1 "1.1.1.1" "2.2.2.2"]
    ixNet commit

    puts "Configuring 10  IPv4 Unconnected Interface "
    for {set i 1} {$i < 11} {incr i} {
        set unconnIntf($i) [AddUnconnectedInt $port1 $a1]
        set unconn1($i) [ixNet add $unconnIntf($i) ipv4]
        ixNet setAttr $unconn1($i) -ip 4.4.4.$i
        ixNet commit

        # Checking If the Unconnected Interface is Created or not
        set index [lsearch [ixNet getList $port1 interface] $unconnIntf($i)]
        if {$index >= 0} {
            puts "Unconnected Interface ceated "
        } else {
            puts "Unconnected Interface ceation failed "
            ixNetCleanUp
            return $FAILED
        }
    }

    # Checking for Modifying Unconnected IPv4 Interface
    for {set i 1} {$i < 11} {incr i} {
    puts "Modifying IPv4 Unconnected Interface unconn1($i)"
        set modify [ModifyIp4UnconnectedInt $unconn1($i) 3.3.3.$i ]
        if {$modify == 1} {
            puts "IPv4 Unconnected Interface Modification test Failed"
            ixNetCleanUp
            return $FAILED
        } else {
            puts "IPv4 Unconnected Interface Modification test Passed"
        }
    }

    # Checking for removing Unconnected IPv4 Interface
    for {set i 1} {$i < 11} {incr i} {

        puts " Removing the Unconnecter Interface unconn1($i)"
        ixNet remove $unconnIntf($i)
        ixNet commit

        set index [lsearch [ixNet getList $port1 interface] $unconnIntf($i)]
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

