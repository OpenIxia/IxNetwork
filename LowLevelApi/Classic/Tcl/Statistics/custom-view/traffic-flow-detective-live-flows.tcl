################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2012 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    26/03/2012 - Mircea Dan Gheorghe - created sample                         #
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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to create a custom view            #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    OS        Linux Fedora Core 12 (32 bit)                                   #
#    IxOS      6.40 EA (6.40.900.4)                                            #
#    IxNetwork 7.0  EA (7.0.801.20)                                            #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.200.115.204
    set ixTclPort   8009
    set ports       {{10.200.115.151 3 11} {10.200.115.151 3 12}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 6.30 –setAttribute strict

puts "Load the IxNetwork config"
ixNet exec loadConfig [ixNet readFrom config.custom-views.ixncfg]
set vPorts [ixNet getList [ixNet getRoot] vport]

puts "Assigning virtual ports to real ports"
::ixTclNet::AssignPorts $::ixia::ports {} $vPorts force

puts "Starting all protocols"
ixNet exec startAllProtocols

puts "Waiting for 30 sec"
after 30000

puts "Applying the traffic"
ixNet setAttr [ixNet getRoot]/traffic -refreshLearnedInfoBeforeApply true
ixNet exec apply [ixNet getRoot]/traffic

puts -nonewline "Starting the traffic "
ixNet exec start [ixNet getRoot]/traffic

set count 0
while { [ixNet getAttr [ixNet getRoot]/traffic -state] != "started" } {
    puts -nonewline "."
    after 1000
    incr count
    if { $count > 90 } {
        error "Waited for 90 sec, Traffic still not in started state !"
    }
}
puts "."

puts "Leting the traffic run for 30 sec"
after 30000

puts "Add the custom view"
set custom_view [ixNet add [ixNet getRoot]/statistics view]
ixNet setAttr $custom_view -caption "traffic-flow-detective-live-flows"
ixNet setAttr $custom_view -type layer23TrafficFlowDetective
ixNet setAttr $custom_view -visible true
ixNet commit
set custom_view [lindex [ixNet remapIds $custom_view] 0]

puts "Retrieve relevant filters for the view"
set availablePortFilter        [ixNet getList $custom_view availablePortFilter]
set availableTrackingFilter    [ixNet getList $custom_view availableTrackingFilter]
set availableTrafficItemFilter [ixNet getList $custom_view availableTrafficItemFilter]
set availableStatisticFilter   [ixNet getList $custom_view availableStatisticFilter]

puts "Configure the filter selection area"
ixNet setAttr $custom_view/layer23TrafficFlowDetectiveFilter -flowFilterType        liveFlows
ixNet setAttr $custom_view/layer23TrafficFlowDetectiveFilter -portFilterIds         $availablePortFilter
ixNet setAttr $custom_view/layer23TrafficFlowDetectiveFilter -trafficItemFilterIds  $availableTrafficItemFilter
ixNet commit

puts "Configure the stats filter"
set rxFramesStatisticFilter [lindex $availableStatisticFilter [lsearch -regexp $availableStatisticFilter "Rx Frames"]]
set statFilter [ixNet add  $custom_view/layer23TrafficFlowDetectiveFilter statisticFilter]
ixNet setAttr $statFilter -statisticFilterId $rxFramesStatisticFilter
ixNet setAttr $statFilter -operator          isEqualOrGreater
ixNet setAttr $statFilter -value             10
ixNet commit

puts "Configure the liveFlows filter"
ixNet setAttr $custom_view/layer23TrafficFlowDetectiveFilter/liveFlowsFilter -numberOfResults    20
ixNet setAttr $custom_view/layer23TrafficFlowDetectiveFilter/liveFlowsFilter -sortByStatisticId  $rxFramesStatisticFilter
ixNet setAttr $custom_view/layer23TrafficFlowDetectiveFilter/liveFlowsFilter -sortingCondition   worstPerformers
ixNet commit

puts "Enable the stats columns to be disaplyed"
set statsList [ixNet getList $custom_view statistic]
foreach stat $statsList {
    ixNet setAttr $stat -enabled true
}
ixNet commit

puts "Get the custom view going and start retrieveing stats"
ixNet setAttribute $custom_view -enabled true
ixNet commit

puts "TEST END ."

puts " "
puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view"
puts "[ixNet help ::ixNet::OBJ-/statistics/view]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/layer23TrafficFlowDetectiveFilter"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/layer23TrafficFlowDetectiveFilter]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/layer23TrafficFlowDetectiveFilter/liveFlowsFilter"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/layer23TrafficFlowDetectiveFilter/liveFlowsFilter]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/layer23TrafficFlowDetectiveFilter/statisticFilter"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/layer23TrafficFlowDetectiveFilter/statisticFilter]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/statistic"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/statistic]"
