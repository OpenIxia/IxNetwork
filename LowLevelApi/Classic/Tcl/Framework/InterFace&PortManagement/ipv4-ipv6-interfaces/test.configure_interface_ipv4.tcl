#------------------------------------------------------------------------------
# PURPOSE OF THE SCRIPT:
# This script shows how to Add, modify the interface properties
# and remove an IPv4 interface.
#
# Sequence of events being carried out by the script
#     1) Adds 6 IPv4 interface per port
#     2) Modifies properties of all the added interfaces
#     3) Removes all the 6 interfaces
#
# SCRIPT-GEN USED : No
# IXNCFG USED     : No
#------------------------------------------------------------------------------
source $env(IXNETWORK_SAMPLE_SCRIPT_DIR)/IxNetwork/Classic/Tcl/TestRun/config.tcl

#------------------------------------------------------------------------------
# PROCEDURE    : AddInterfaceIPv4
# PURPOSE      : Adding IPV4 connected interface
# INPUT        : (1) Object reference to the virtual port on which ipv4
#                    interface object to be added.
#                (2) ip address
#                (3) gateway
# OUTPUT       : An IPv4 interface will be added
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc AddInterfaceIPv4 {port {ip 1.1.1.1} {gateway 2.2.2.2}} {
    set i1 [ixNet add $port interface]
    ixNet commit
    set ip1 [ixNet add $i1 ipv4]
    ixNet setAttr $ip1 -ip $ip
    ixNet setAttr $ip1 -gateway $gateway
    ixNet setAttr $ip1 -maskWidth 24
    ixNet setAttr $i1 -enabled true
    ixNet commit
    return $i1
}


#------------------------------------------------------------------------------
# PROCEDURE    : ModifyIp4Int
# PURPOSE      : Modifying IPV4 connected interface
# INPUT        : (1) Object reference to the ipv4 interface object.
#                (2) ip address
#                (3) gateway
# OUTPUT       : IPv4 interface object will be modified as specified in this
#                proc
# RETURN VALUE : FAILED (1) or PASSED (0)
#------------------------------------------------------------------------------
proc ModifyIp4Int {p1 ip gateway} {
    set flag 0
    set maskWidth 16
    ixNet commit
    ixNet setAttr $p1 -ip $ip
    ixNet setAttr $p1 -gateway $gateway
    ixNet setAttr $p1 -maskWidth $maskWidth
    ixNet commit
    if {$gateway != [ixNet getAttr $p1 -gateway]} {
        puts "** Get Attribute on gateway failed"
        set flag 1
    }
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
    set pList [getPortList $portData1 $portData2]
    set port1 [lindex $pList 0]
    set port2 [lindex $pList 1]

    # create 6 ipv4 interfaces on port 1 and port 2
    puts "Configuring for IPv4 creating 6 interfaces ..."
    set c 20
    set d 20
    for {set a 1} {$a <6} {incr a} {
        set i1($a) [AddInterfaceIPv4 $port1 "20.20.$c.2" "20.20.$c.1"]
        set i2($a) [AddInterfaceIPv4 $port2 "20.20.$d.1" "20.20.$d.2"]

        set ilist1 [ixNet getList $port1 interface]
        set j1 [lindex $ilist1 [expr {[llength $ilist1] - 1}]]
        set ilist2 [ixNet getList $port2 interface]
        set j2 [lindex $ilist2 [expr {[llength $ilist1] - 1}]]

        incr c
        incr d
    }
    ixNet commit

    # Check If all the Interfaces are created or not
    puts "Check If all the Interfaces are created or not (port1)"
    set x [split $j1 ":"]
    set y [lindex $x 6]

    if { $y == [expr $a - 1 ] } {
        puts "$y interfaces are created in the First port "
    } else {
        puts "All the interfaces are not created in th First port"
        ixNetCleanUp
        return $FAILED
    }

    # Check If all the Interfaces are created or not
    puts "Check If all the Interfaces are created or not (port2)"
    set x [split $j2 ":"]
    set y [lindex $x 6]

    if { $y == [expr $a - 1]} {
        puts "$y interfaces are created in the Second port "
    } else {
        puts "All the interfaces are not created in th Second port"
        ixNetCleanUp
        return $FAILED
    }

    #  Modify Connected Ipv4 Interface
    puts "Success : configured ip address.."
    set c 30
    set d 30
    for {set a 1} {$a <6} {incr a} {
        set ip1 [lindex [ixNet getList $i1($a) ipv4] 0]
        set ip2 [lindex [ixNet getList $i2($a) ipv4] 0]

        set modify [ModifyIp4Int $ip1 "20.20.$c.2" "20.20.$c.1"]
        set modify [ModifyIp4Int $ip2 "20.20.$d.1" "20.20.$d.2"]

        incr c
        incr d
        if {$modify == 1} {
            puts "IPv4 Interface modification test Failed"
            ixNetCleanUp
            return $FAILED
        } else {
            puts "IPv4 Interface modification test Passed"
        }
    }

    # Deleting Ipv4 connected interface in the fly
    for {set a 2} {$a < 5} {incr a} {
        ixNet remove $i1($a)
        ixNet commit
        set index [lsearch [ixNet getList $port1 interface] $i1($a)]
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


