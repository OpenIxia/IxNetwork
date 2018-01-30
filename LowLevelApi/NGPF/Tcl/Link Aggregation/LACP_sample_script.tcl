#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    06/04/2015 - Sumit Deb - created sample                                   #
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
#    This script intends to demonstrate how to use NGPF LACP API.              #
#	 Script uses four ports to demonstrate LAG properties.                     #
#                                                                              #
#    1. It will create 2 LACP topologies, each having an two port which are    #
#       LAG members. It will then modify the ActorSystemId and ActorKey	for    # 
#       both the LAG systems.                                                  #
#    2. Start the LACP protocol.                                               #
#    3. Retrieve protocol statistics and LACP per port statistics.             #
#	 4. Disable Synchronization flag on port1 in System1-LACP-LHS.             # 
#	 5. Retrieve protocol statistics and LACP per port statistics.             #
#	 6. Re-enable Synchronization flag on port1 in System1-LACP-LHS.           # 
#	 7. Retrieve protocol statistics and LACP per port statistics.             #
#	 8. Perform StopPDU on port1 in System1-LACP-LHS.                          # 
#	 9. Retrieve LACP global learned info.                                     #
#	 10. Perform StopPDU on port1 in System1-LACP-LHS.                         # 
#	 11. Retrieve LACP global learned info.                                    #
#	 12. Stop All protocols.                                                   #
#                                                                              # 
# 	Ixia Software:                                                             #
#    IxOS      6.90 EA                                                         #
#    IxNetwork 7.50 EA                                                         #
#                                                                              #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"
#proc to generate drill-down global learned info view for LACP
proc gererateLacpLearnedInfoView { viewName } {
variable currentStatView
	set viewCaption $viewName
	set protocol "LACP"
	set drillDownType "Global Learned Info"
	set statsViewList [ixNet getList [ixNet getRoot]/statistics view]
	
	# Add a StatsView
	set root [ixNet getRoot]
	set statistics $root/statistics
    set view [ixNet add $statistics view]
    ixNet setAttribute $view -caption $viewCaption
	ixNet setAttribute $view -type layer23NextGenProtocol
    ixNet setAttribute $view -visible true
	ixNet commit
	set view [ixNet remapIds $view]

	# Set Filters        
    set trackingFilter [ixNet add $view advancedCVFilters]
    ixNet setAttribute $trackingFilter -protocol $protocol
	ixNet commit
	#ixNet getAttr $trackingFilter -availableGroupingOptions        
	ixNet setAttribute $trackingFilter -grouping $drillDownType
	ixNet commit
	set layer23NextGenProtocolFilter $view/layer23NextGenProtocolFilter        
	ixNet setAttribute $layer23NextGenProtocolFilter -advancedCVFilter $trackingFilter
	ixNet commit

	# Enable Stats Columns to be displayed
	set statsList [ixNet getList $view statistic]
	foreach stat $statsList {
		ixNet setAttribute $stat -enabled true
	}
	ixNet commit

	# Enable Statsview
	ixNet setAttribute $view -enabled true
	ixNet commit
}
# Edit this variables values to match your setup
namespace eval ::ixia {
    set ixTclServer 10.205.28.122
    set ixTclPort   8987
    set ports       {{10.205.28.173 1 1} {10.205.28.173 1 2} {10.205.28.173 1 3} {10.205.28.173 1 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 7.50\
    –setAttributeibute strict

puts "Creating a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure LACP as per the description     #
################################################################################ 
puts "Adding 4 vports"
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet add [ixNet getRoot] vport
ixNet commit

set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx1 [lindex $vPorts 0]
set vportRx1 [lindex $vPorts 1]
set vportTx2 [lindex $vPorts 2]
set vportRx2 [lindex $vPorts 3]
set vportListLAG1 [list $vportTx1 $vportTx2]
set vportListLAG2 [list $vportRx1 $vportRx2]


puts "Assigning the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

puts "Adding 2 topologies"
ixNet add [ixNet getRoot] topology -vports $vportListLAG1
ixNet add [ixNet getRoot] topology -vports $vportListLAG2
ixNet commit

set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]
set topo2 [lindex $topologies 1]

puts "Adding 2 device groups"
ixNet add $topo1 deviceGroup
ixNet add $topo2 deviceGroup
ixNet commit

set t1devices [ixNet getList $topo1 deviceGroup]
set t2devices [ixNet getList $topo2 deviceGroup]

set t1dev1 [lindex $t1devices 0]
set t2dev1 [lindex $t2devices 0]

puts "Configuring the multipliers (number of sessions)"
ixNet setAttribute $t1dev1 -multiplier 1
ixNet setAttribute $t2dev1 -multiplier 1
ixNet commit

puts "Adding ethernet/mac endpoints"
ixNet add $t1dev1 ethernet
ixNet add $t2dev1 ethernet
ixNet commit

set mac1 [ixNet getList $t1dev1 ethernet]
set mac2 [ixNet getList $t2dev1 ethernet]

puts "Configuring the mac addresses"
ixNet setMultiAttr [ixNet getAttr $mac1 -mac]/counter\
        -direction  increment                        \
        -start      {00:11:01:00:00:01}              \
        -step       {00:00:00:00:00:01}

ixNet setMultiAttr [ixNet getAttr $mac2 -mac]/counter\
        -direction  increment                        \
        -start      {00:12:01:00:00:01}              \
        -step       {00:00:00:00:00:01}
ixNet commit

puts "Adding LACP over Ethernet stacks"
ixNet add $mac1 lacp
ixNet add $mac2 lacp
ixNet commit

set lacp1 [ixNet getList $mac1 lacp]
set lacp2 [ixNet getList $mac2 lacp]

puts "Renaming the topologies and the device groups"
ixNet setAttribute $topo1  -name "LAG1-LHS"
ixNet setAttribute $topo2  -name "LAG1-RHS"

ixNet setAttribute $t1dev1 -name "SYSTEM1-LACP-LHS"
ixNet setAttribute $t2dev1 -name "SYSTEM1-LACP-RHS"
ixNet commit


puts "Modifying ActorSystemID and ActorKey to user defined values"
set sys1LagLHS [lindex $lacp1 0]
set sys1LagRHS [lindex $lacp2 0]
set sys1LagLHSport1 [lindex [ixNet getList $sys1LagLHS port] 0]
set sys1LagLHSport2 [lindex [ixNet getList $sys1LagLHS port] 1]
set sys1LagRHSport1 [lindex [ixNet getList $sys1LagRHS port] 0]
set sys1LagRHSport2 [lindex [ixNet getList $sys1LagRHS port] 1]

set sys1LagLHSport1ActKey [ixNet getA $sys1LagLHSport1 -actorKey]
set sys1LagLHSport2ActKey [ixNet getA $sys1LagLHSport2 -actorKey]
set sys1LagRHSport1ActKey [ixNet getA $sys1LagRHSport1 -actorKey]
set sys1LagRHSport2ActKey [ixNet getA $sys1LagRHSport2 -actorKey]

set sys1LagLHSport1SysId [ixNet getA $sys1LagLHSport1 -actorSystemId]
set sys1LagLHSport2SysId [ixNet getA $sys1LagLHSport2 -actorSystemId]
set sys1LagRHSport1SysId [ixNet getA $sys1LagRHSport1 -actorSystemId]
set sys1LagRHSport2SysId [ixNet getA $sys1LagRHSport2 -actorSystemId]

ixNet setMultiAttr $sys1LagLHSport1ActKey -pattern singleValue -clearOverlays False
ixNet setMultiAttr $sys1LagLHSport2ActKey -pattern singleValue -clearOverlays False
ixNet setMultiAttr $sys1LagRHSport1ActKey -pattern singleValue -clearOverlays False
ixNet setMultiAttr $sys1LagRHSport2ActKey -pattern singleValue -clearOverlays False
ixNet commit

ixNet setMultiAttr $sys1LagLHSport1SysId -pattern singleValue -clearOverlays False
ixNet setMultiAttr $sys1LagLHSport2SysId -pattern singleValue -clearOverlays False
ixNet setMultiAttr $sys1LagRHSport1SysId -pattern singleValue -clearOverlays False
ixNet setMultiAttr $sys1LagRHSport2SysId -pattern singleValue -clearOverlays False
ixNet commit

ixNet setMultiAttribute $sys1LagLHSport1ActKey/singleValue -value "666"
ixNet setMultiAttribute $sys1LagLHSport2ActKey/singleValue -value "666"
ixNet setMultiAttribute $sys1LagRHSport1ActKey/singleValue -value "777"
ixNet setMultiAttribute $sys1LagRHSport2ActKey/singleValue -value "777"
ixNet commit

ixNet setMultiAttribute $sys1LagLHSport1SysId/singleValue -value "666"
ixNet setMultiAttribute $sys1LagLHSport2SysId/singleValue -value "666"
ixNet setMultiAttribute $sys1LagRHSport1SysId/singleValue -value "777"
ixNet setMultiAttribute $sys1LagRHSport2SysId/singleValue -value "777"
ixNet commit

################################################################################
# 2. Start LACP protocol and wait for 60 seconds                               #
################################################################################
puts "\nStarting LACP and waiting for 60 seconds for sessions to come up"
ixNet exec startAllProtocols
after 30000

################################################################################
# 3. Retrieve protocol statistics and LACP per port statistics                 #
################################################################################
puts "\nFetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "\nFetching all LACP per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}

after 5000
################################################################################
# 4. Disable Synchronization flag on port1 in System1-LACP-LHS                 #
################################################################################
puts "\n\nDisable Synchronization flag on port1 in System1-LACP-LHS"
set sys1LagLHSport1SyncFlag [ixNet getA $sys1LagLHSport1 -synchronizationFlag]
ixNet setMultiAttr $sys1LagLHSport1SyncFlag -pattern singleValue -clearOverlays False
ixNet commit
ixNet setMultiAttribute $sys1LagLHSport1SyncFlag/singleValue -value false
ixNet commit

#Applying changes on the fly
set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
ixNet exec applyOnTheFly $topology

after 5000

################################################################################
# 5. Retrieve protocol statistics and LACP per port statistics                 #
################################################################################
puts "\nFetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "\nFetching all LACP per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}

after 5000
################################################################################
# 6. Re-enable Synchronization flag on port1 in System1-LACP-LHS               #
################################################################################
puts "\n\nRe-enable Synchronization flag on port1 in System1-LACP-LHS"
ixNet setMultiAttr $sys1LagLHSport1SyncFlag -pattern singleValue -clearOverlays False
ixNet commit
ixNet setMultiAttribute $sys1LagLHSport1SyncFlag/singleValue -value true
ixNet commit

#Applying changes on the fly
set globals [ixNet getRoot]/globals
set topology $globals/topology
puts "Applying changes on the fly"
ixNet exec applyOnTheFly $topology

after 5000

################################################################################
# 7. Retrieve protocol statistics and LACP per port statistics                 #
################################################################################
puts "\nFetching all Protocol Summary Stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"Protocols Summary"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}
puts "\nFetching all LACP per-port statistics\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP Per Port"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}

after 5000

################################################################################
# 8. Perform LACPDU stop on System1-LACP-LHS                                   #
################################################################################
puts "\n\nPerform LACPDU stop on System1-LACP-LHS "
ixNet exec lacpStopPDU $sys1LagLHS
after 90000

################################################################################
# 9. Retrieve LACP global Learned Info                                         #
################################################################################
puts "\n\n Retrieve LACP global Learned Info"
set viewName "LACP-global-learned-Info-TCLview"
gererateLacpLearnedInfoView $viewName
ixNet exec refresh ::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"
after 10000
puts "\nFetching all Global Learned Info\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}

after 5000

################################################################################
# 10. Perform LACPDU start on System1-LACP-LHS                                 # 
################################################################################
puts "\n\nPerform LACPDU start on System1-LACP-LHS "
ixNet exec lacpStartPDU $sys1LagLHS
after 90000

################################################################################
# 11. Retrieve LACP global Learned Info                                        #
################################################################################
ixNet exec refresh ::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"
after 10000
puts "\nFetching all Global Learned Info\n"
set viewPage {::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page}
set statcap [ixNet getAttr $viewPage -columnCaptions]
foreach statValList [ixNet getAttr $viewPage -rowValues] {
    foreach statVal $statValList  {
        puts "***************************************************"
        set index 0
        foreach satIndv $statVal {
            puts [format "%*s:%*s" -30 [lindex $statcap $index]\
                -10 $satIndv]
            incr index
        }
    }
}

after 5000
################################################################################
# 12. Stop all protocols                                                       #
################################################################################
puts "Stopping all protocols"
ixNet exec stopAllProtocols
puts "\n\n!!! Test Script Ends !!!"
