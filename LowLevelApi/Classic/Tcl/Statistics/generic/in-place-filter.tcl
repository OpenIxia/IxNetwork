################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2012 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    13/06/2012 - Vicentiu Zamfirescu - created sample                         #
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
#    This script intends to demonstrate how to create a in place filter		   #
#	 for a on demand view.													   #
# Module:                                                                      #
#    The sample was tested on an XMVDC16 module.                               #
# Software:                                                                    #
#    OS        Linux Fedora Core 12 (32 bit)                                   #
#    IxOS      6.50 EA (6.50.950.4)                                            #
#    IxNetwork 7.10  EA (7.10.840.14)                                          #
#                                                                              #
################################################################################

# edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 127.0.0.1
    set ixTclPort   8009
    set ports       {{10.215.170.111 1 11} {10.215.170.111 1 12}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 6.30 –setAttribute strict

puts "Load the IxNetwork config"
ixNet exec loadConfig [ixNet readFrom config.dhcpv4-basic.ixncfg]
set vPorts [ixNet getList [ixNet getRoot] vport]

puts "Assigning virtual ports to real ports"
::ixTclNet::AssignPorts $::ixia::ports {} $vPorts force

puts "Starting all protocols"
ixNet exec startAllProtocols

puts "Waiting for 30 sec"
after 30000

proc executeDrillDown {ddOption  rowN  view} {
	puts "Creating  DD  $ddOption  ON  $view  view"
	set root [ixNet getRoot]
	set index [lsearch -regexp [ixNet getL $root/statistics view] "$view"]	
	if {$index== -1} {
		puts "Cannot find $view in view tree !"
		return 1
	}
	set usedView [lindex [ixNet getL $root/statistics view] $index]
	
	ixNet setA $usedView/drillDown -targetRowIndex $rowN
	ixNet commit

	set targets [ixNet getA $usedView/drillDown -availableDrillDownOptions]
	puts "Available Drill Down Options: $targets"

	set index [lsearch -regexp $targets "$ddOption"]	
	if {$index== -1} {
		puts "DD option $ddOption is not available for $view view !"
		return 1
	}
	
	set target [lindex $targets $index]
	puts "Drill down option used: $target"
	
	ixNet setA $usedView/drillDown -targetDrillDownOption $target
	ixNet commit

	ixNet exec doDrillDown $usedView/drillDown
	puts "Finished creating  DD  $ddOption  ON  $view  view"
	return 0
}

puts "Refreshing CPF views."
if {[ixNet exec refresh __allNextGenViews] != "::ixNet::OK"} {
	error "Failed to refresh CPF views !!!"
}
after 5000

if { [executeDrillDown "Per Port" 1 "Protocols Summary"] != 0 } {
	error "Cannot perform the given DD option !"
}

if { [executeDrillDown "Per Lease" 0 "DHCPv4 Server Drill Down"] != 0 } {
	error "Cannot perform the given DD option !"
}

# Set the view on which the filter will be applied, the filter name, the filter expression and sorting
set viewName "DHCPv4 Server Drill Down"
set filName "1_New_Filter"
set filExpr {Equals([Lease#], '2') Or Equals([Lease#], '4') Or Equals([Lease#], '6') Or Equals([Lease#], '8')}
set sortExpr {[Lease#] = desc}

puts "Creating filter $filName for $viewName view"
set index [lsearch -regexp [ixNet getL [ixNet getRoot]/statistics view] $viewName]	
if {$index== -1} {
	error "Cannot find $viewName in view tree !"
}
set usedView [lindex [ixNet getL [ixNet getRoot]/statistics view] $index]	

set filters [ixNet getA $usedView/layer23NextGenProtocolFilter -allAdvancedFilters]
puts "All advanced filters: "
foreach item $filters {
	puts "** $item"
}	

set index [lsearch -regexp $filters $filName]	
if {$index== -1} {
	puts "Cannot find the expected filter in the filter list, the filter will be created"	
	set trackingFilter [ixNet add $usedView/layer23NextGenProtocolFilter advancedFilter]

	puts "Set the name of the tracking filter"
	ixNet setA $trackingFilter -name $filName

	puts "Set the expression of the tracking filter"
	ixNet setA $trackingFilter -expression $filExpr

	puts "Set the sort option of the tracking filter"
	ixNet setA $trackingFilter -sortingStats $sortExpr
	ixNet commit

	puts "Get the ID of the tracking filter"
	set id_1 [ixNet getA $trackingFilter -trackingFilterId]

	puts "Apply the filter id to the target view"
	ixNet exec addAdvancedFilter $usedView/layer23NextGenProtocolFilter $id_1
	puts "Finished creating the filter"		
} else {
	puts "Filter already exists, applying the filter"
	set usedFilter [lindex $filters $index]
	puts "Used filter: $usedFilter"	

	ixNet exec addAdvancedFilter $usedView/layer23NextGenProtocolFilter $usedFilter
	puts "Finished applying the filter"
}

# Delete the filter
# ixNet exec removeAdvancedFilter $usedView/layer23NextGenProtocolFilter $usedFilter

# set filters [ixNet getA $usedView/layer23NextGenProtocolFilter -allAdvancedFilters]	

# set index [lsearch -regexp $filters $filName]	
# if {$index != -1} {
	# error "The filter was found in the filter list although it has been deleted !"
# }
# puts "Finished deleting the filter"
	
puts "TEST END ."

puts " "
puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view"
puts "[ixNet help ::ixNet::OBJ-/statistics/view]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/layer23NextGenProtocolFilter"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/layer23NextGenProtocolFilter]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/drillDown"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/drillDown]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/statistic"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/statistic]"
