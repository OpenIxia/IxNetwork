#!/usr/bin/tclsh

package req IxTclNetwork

set ixNetworkTclServer 10.219.16.219
set ixNetworkVersion 7.31

ixNet connect $ixNetworkTclServer -version $ixNetworkVersion

proc createView {name type } {

    # View: ::ixNet::OBJ-/statistics/view:L7
    set view [ixNet add [ixNet getRoot]statistics view]

    ixNet setAttribute $view -caption $name
    ixNet setAttribute $view -visible true
    ixNet setAttribute $view -type $type
    ixNet commit
    return $view 
}

proc enableView {view {enable true}} {
    ixNet setAttribute $view -enabled $enable
    ixNet setAttribute $view -visible $enable
    ixNet commit
}

proc GetDrillDownStats {} {
    # Remove all existing TCL Views first.
    ixNet execute removeAllTclViews

    # View: ::ixNet::OBJ-/statistics/view:L7
    set view [ixNet add [ixNet getRoot]statistics view]

    ixNet setAttribute $view -caption "Dhcp Sessions"
    ixNet setAttribute $view -visible true
    ixNet commit

    set view [lindex [ixNet remapids $view] 0]
    puts "\nview: $view"
    # view: ::ixNet::OBJ-/statistics/view:"Dhcp Sessions"

    puts "\nhelp: [ixNet help $view]"
    # type=kEnumValue=layer23NextGenProtocol,layer23ProtocolAuthAccess,layer23ProtocolPort,layer23ProtocolRouting,layer23ProtocolStack,layer23TrafficFlow,layer23TrafficFlowDetective,layer23TrafficItem,layer23TrafficPort,layer47AppLibraryTraffic,sVReadOnly
    ixNet setAttribute $view -type layer23ProtocolAuthAccess
    ixNet commit
    
    set protocolFilters [ixNet getList ${view} availableProtocolFilter]
    puts "\nprotocolFilters: $protocolFilters"

}

GetDrillDownStats
ixNet disconnect
