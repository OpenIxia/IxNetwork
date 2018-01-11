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
#    This script intends to demonstrate how to create a custom view with	   #
#	 advanced filtering														   #	
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

puts "Refreshing CPF views."
if {[ixNet exec refresh __allNextGenViews] != "::ixNet::OK"} {
	error "Failed to refresh CPF views !!!"
}
after 5000

# Set the custom view name, protocol used, grouping level, filter expression, filter sorting expression and what stats to be added in the custom view
set viewName "DHCPv4Server-PerLease"
set protocol "DHCPv4 Server"
set grLevel "Per Lease" 
set filExpr {Equals([Lease#], '2') Or Equals([Lease#], '4') Or Equals([Lease#], '6') Or Equals([Lease#], '8')}
set sortExpr {[Lease#] = desc}  
set cvStats "all"

puts "Creating advanced filtering custom view $viewName"

set mv [ixNet add [ixNet getRoot]/statistics view]
ixNet setAttr $mv -caption "$viewName"
ixNet setAttr $mv -type layer23NextGenProtocol
ixNet setAttr $mv -visible true
ixNet commit
set mv [lindex [ixNet remapIds $mv] 0]

puts "Add advanced filtering filter in $viewName"
set trackingFilter [ixNet add $mv advancedCVFilters]

puts "Verify protocol $protocol is available"		
set fil [ixNet getL $mv layer23NextGenProtocolFilter]
set afil [ixNet getL $mv availableProtocolFilter]
# ixNet commit

set index [lsearch -regexp $afil $protocol]
if {$index == -1} {
	error "Cannot find $protocol in the available protocol filters list"
}

puts "Protocol $protocol is available, selecting it for the filter"	
ixNet setA $trackingFilter -protocol $protocol
ixNet commit

puts "Verify grouping level $grLevel is available"

set avGrLev [ixNet getA $trackingFilter -availableGroupingOptions]

set index [lsearch -regexp $avGrLev "$grLevel"]
if {$index == -1} {
	error "Cannot find $grLevel in the available grouping level list"
}	

puts "Grouping level $grLevel is available, selecting it for the filter"	
ixNet setA $trackingFilter -grouping $grLevel
ixNet commit

puts "Adding filter expression and filter sorting stats"
ixNet setA $trackingFilter -expression $filExpr
ixNet setA $trackingFilter -sortingStats $sortExpr
ixNet commit

puts "Setting the filter"
ixNet setAttr $mv/layer23NextGenProtocolFilter -advancedCVFilter $trackingFilter
ixNet commit

puts "Enable the stats columns to be disaplyed for $viewName"
set statsList [ixNet getList $mv statistic]

if {$cvStats == "all"} {
	foreach stat $statsList {
		ixNet setAttr $stat -enabled true
	}	
} else {
	foreach stat $cvStats {
		set index [lsearch -regexp $statsList $stat]	
		if {$index== -1} {
			error "Cannot find $stat statistic !"
		}	
		ixNet setAttr [lindex $statsList $index] -enabled true
	}
}	
ixNet commit	

puts "Get the $viewName view going and start retrieveing stats"
ixNet setAttribute $mv -enabled true
ixNet commit

puts "TEST END ."

puts " "
puts " "
puts "For more info please refer to the user manual or the built-in help"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view"
puts "[ixNet help ::ixNet::OBJ-/statistics/view]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/advancedCVFilters"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/advancedCVFilters]"
puts " "
puts "ixNet help ::ixNet::OBJ-/statistics/view/statistic"
puts "[ixNet help ::ixNet::OBJ-/statistics/view/statistic]"
