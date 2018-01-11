#!/opt/ActiveTcl-8.5/bin/tclsh

package req IxTclNetwork

set IxNserver 10.205.1.42
set IxNport   8009
set ixNetVersion 7.12

#make sure you have the ixncfg(the same as the one attached to the bug) loaded, then assign your ports, start IGMP protocol, apply traffic and start traffic

ixNet connect $IxNserver -port $IxNport -version $ixNetVersion


#You can create a TCL custom view that have -egressLatencyBinDisplayOption set to „showEgressRows” value.
#Afterwards you can set the same attribute to „showEgressFlatView” value.
#
#Here is an example:

#To Create Custom Views....

set root [ixNet getRoot]

set view [ixNet add [ixNet getRoot]/statistics view]

set caption_name "EgressView"
ixNet setAttribute $view -caption "$caption_name"
ixNet setAttribute $view -type layer23TrafficFlow
ixNet commit

set view [lindex [ixNet remapIds $view] 0]

#setting Attributes to make it visible, setting Port filter ID and Traffic Filter ID 
ixNet setAttr $view -visible true
ixNet commit

set av_port_Filter [ixNet getList $view availablePortFilter]
ixNet setAttr $view/layer23TrafficFlowFilter -portFilterIds $av_port_Filter
ixNet commit

set av_port_Filter [ixNet getAttr $view/layer23TrafficFlowFilter -portFilterIds]
set av_Traffic_Item_Filter [ixNet getList $view availableTrafficItemFilter]
ixNet setAttr $view/layer23TrafficItemFilter -trafficItemFilterIds $av_Traffic_Item_Filter
ixNet commit

set av_Traffic_Item_Filter [ixNet getAttr $view/layer23TrafficItemFilter -trafficItemFilterIds] 


#Adding the column to the created view 
ixNet setAttr "$view/statistic:\"Tx Frames\"" -enabled true
ixNet setAttr "$view/statistic:\"Rx Frames\"" -enabled true
ixNet setAttr "$view/statistic:\"Loss %\"" -enabled true
ixNet setAttr "$view/statistic:\"Frames Delta\"" -enabled true

#setting the view type as the Flat View
ixNet setAttr $view/layer23TrafficFlowFilter -egressLatencyBinDisplayOption showEgressRows  
if {[catch {set status [ixNet commit]} error]} {
     log "unable to create Flat View"
     ixNetCleanUp
     return $flag
     }

#setting the enumeration field to track by means of the VLAN ID 
set enumerationFilter [ixNet add $view/layer23TrafficFlowFilter enumerationFilter]
ixNet setAttribute $enumerationFilter -trackingFilterId [lindex [ixNet getList \
                   $view availableTrackingFilter] [lsearch [ixNet getList $view \
                   availableTrackingFilter] {::ixNet::OBJ-/statistics/view:"EgressFlatView"/availableTrackingFilter:"Ethernet:Outer VLAN ID (10 bits) at offset 118"}]]

#seting the sorting order 

set sort_order "ascending"
ixNet setAttribute $enumerationFilter -sortDirection $sort_order
ixNet commit

#sets the view to be enabled to collect the data 
ixNet setAttr $view -enabled true
ixNet commit

#Move to the flatview
if {[catch {set status [ixNet setAttr $view/layer23TrafficFlowFilter –egressLatencyBinDisplayOption showEgressFlatView]} error]} {
    log "Unable to set the attribute to showEgressRows"
    ixNetCleanUp
    return $flag
}

#Config file and full version of script you can find in perforce:
#//protocols/regression-suites/ixN-test-cases/b2b/5.40Traffic/customer/test.FlatEgressChange.tcl
#//protocols/regression-suites/ixN-test-cases/b2b/5.40Traffic/customer/FlatView_Egress_Tracking.ixncfg
#
#Regards,
#Cosmin
