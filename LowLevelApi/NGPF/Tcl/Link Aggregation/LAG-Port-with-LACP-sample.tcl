#!/usr/bin/tclsh
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

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF LAG API.               #
#	 Script uses four ports for demonstration.                                 #
#                                                                              #
#    1. It will create 2 LAGs as RED-LAG & BLUE-LAG with LACP as LAG protocol, # 
#       each LAG having two member ports . It will then modify  the            #
#       ActorSystemId and ActorKey for both the LAG systems.                   #
#    2. Start the LAG.                                                         #
#    3. Retrieve protocol statistics and LACP per port statistics.             #
#	 4. Disable Synchronization flag on RED-LAG-port1 in RED-LAG.              # 
#	 5. Retrieve protocol statistics and LACP per port statistics.             #
#	 6. Re-enable Synchronization flag on RED-LAG-port1 in RED-LAG.            # 
#	 7. Retrieve protocol statistics and LACP per port statistics.             #
#	 8. Perform StopPDU on RED-LAG-port1 in RED-LAG.                           # 
#	 9. Retrieve LACP global learned info.                                     #
#	 10. Perform StartPDU on RED-LAG-port1 in RED-LAG.                         # 
#	 11. Retrieve LACP global learned info.                                    #
#	 12. Stop All protocols.                                                   #
################################################################################

# Script Starts
puts "!!! Test Script Starts !!!"
#procedure to generate drill-down global learned info view for LACP
proc gererateLacpLearnedInfoView { viewName } {
variable currentStatView
	set viewCaption $viewName
	set protocol "LACP"
	set drillDownType "Global Learned Info"
	set root [ixNet getRoot]
	set statsViewList [ixNet getList $root/statistics view]
	
	# Add a StatsView
	
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
    set ixTclServer 10.39.50.102
    set ixTclPort   5555
    set ports       {{10.39.50.96 10 1} {10.39.50.96 10 3} {10.39.50.96 10 5} {10.39.50.96 10 7}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::ixia::ixTclServer -port $::ixia::ixTclPort -version 8.50 –setAttributeibute strict

puts "Create a new config"
ixNet exec newConfig

################################################################################
# 1. Protocol configuration section. Configure LACP as per the description     #
################################################################################ 
puts "Add 4 virtual ports"
set root [ixNet getRoot]
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet add $root vport
ixNet commit

set vPorts [ixNet getList $root vport]
set vportTx1 [lindex $vPorts 0]
set vportRx1 [lindex $vPorts 1]
set vportTx2 [lindex $vPorts 2]
set vportRx2 [lindex $vPorts 3]
set vportListLAG1 [list $vportTx1 $vportTx2]
set vportListLAG2 [list $vportRx1 $vportRx2]


puts "Assign Real ports to virtula ports the ports"
::ixTclNet::AssignPorts $ixia::ports {} $vPorts force

# ADD LAG-1 named RED-LAG
set lag1 [ixNet add $root lag]
ixNet commit
ixNet setMultiAttr $lag1 -name "RED-LAG" -vports $vportListLAG1
ixNet commit

# ADD LAG-2 named BLUE-LAG
set lag2 [ixNet add $root lag]
ixNet commit
ixNet setMultiAttr $lag2 -name "BLUE-LAG" -vports $vportListLAG2
ixNet commit


# Add LACP in RED-LAG
set lag1Stack [ixNet add $lag1 protocolStack]
ixNet setMultiAttribute $lag1Stack -name "LAG1-stack"
ixNet commit
set lag1eth [ixNet add $lag1Stack "ethernet"]
ixNet setMultiAttribute $lag1eth -stackedLayers [list ] -name "Ethernet-RED-LAG"
ixNet commit
set lag1lacp [ixNet add $lag1eth "lagportlacp"]

# To add StaticLag as LAG protocol
# Command - set lag1static [ixNet add $lag1eth "lagportstaticlag"]

ixNet setMultiAttribute $lag1lacp -stackedLayers [list ] -name "LACP-RED-LAG"
ixNet commit

# # Add LACP in BLUE-LAG
set lag2Stack [ixNet add $lag2 protocolStack]
ixNet setMultiAttribute $lag2Stack -name "LAG2-stack"
ixNet commit
set lag2eth [ixNet add $lag2Stack "ethernet"]
ixNet setMultiAttribute $lag2eth -stackedLayers [list ] -name "Ethernet-BLUE-LAG"
ixNet commit
set lag2lacp [ixNet add $lag2eth "lagportlacp"]

# To add StaticLag as LAG protocol
# Command - set lag2static [ixNet add $lag2eth "lagportstaticlag"]

ixNet setMultiAttribute $lag2lacp -stackedLayers [list ] -name "LACP-BLUE-LAG"
ixNet commit

# configure LACP ActorSystemID and ActorKey to user defined values

puts "Configure LACP ActorSystemID and ActorKey to user defined values"
set RedLAGlacp [lindex $lag1lacp 0]
set BlueLAGlacp [lindex $lag2lacp 0]

set RedLAGlacpActKey [ixNet getA $RedLAGlacp -actorKey]
set BlueLAGlacpActKey [ixNet getA $BlueLAGlacp -actorKey]

set RedLAGlacpSysId [ixNet getA $RedLAGlacp -actorSystemId]
set BlueLAGlacpSysId [ixNet getA $BlueLAGlacp -actorSystemId]

ixNet setMultiAttr $RedLAGlacpActKey -pattern singleValue -clearOverlays False
ixNet setMultiAttr $BlueLAGlacpActKey -pattern singleValue -clearOverlays False
ixNet commit

ixNet setMultiAttr $RedLAGlacpSysId -pattern singleValue -clearOverlays False
ixNet setMultiAttr $BlueLAGlacpSysId -pattern singleValue -clearOverlays False
ixNet commit

ixNet setMultiAttribute $RedLAGlacpActKey/singleValue -value "6677"
ixNet setMultiAttribute $BlueLAGlacpActKey/singleValue -value "8899"
ixNet commit

ixNet setMultiAttribute $RedLAGlacpSysId/singleValue -value "016677"
ixNet setMultiAttribute $BlueLAGlacpSysId/singleValue -value "018899"
ixNet commit

################################################################################
# 2. Start LAG protocol and wait for 60 seconds                               #
################################################################################
puts "\nStarting LAG and waiting for 60 seconds for sessions to come up"
ixNet exec startAllProtocols
after 60000

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
# 4. Disable Synchronization flag on port1 in RED-LAG						#
################################################################################
puts "\n\nDisable Synchronization flag on port1 in RED-LAG"
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
set RedLAGlacpPort1SyncFlag [ixNet getA $RedLAGlacpPort1 -synchronizationFlag]
ixNet setMultiAttr $RedLAGlacpPort1SyncFlag -pattern singleValue -clearOverlays false
ixNet commit
ixNet setMultiAttribute $RedLAGlacpPort1SyncFlag/singleValue -value false
ixNet commit

#Applying changes on the fly
set globals $root/globals
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
# 6. Re-enable Synchronization flag on port1 in RED-LAG               #
################################################################################
puts "\n\nRe-enable Synchronization flag on port1 in RED-LAG"
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
set RedLAGlacpPort1SyncFlag [ixNet getA $RedLAGlacpPort1 -synchronizationFlag]
ixNet setMultiAttr $RedLAGlacpPort1SyncFlag -pattern singleValue -clearOverlays false
ixNet commit
ixNet setMultiAttribute $RedLAGlacpPort1SyncFlag/singleValue -value true
ixNet commit

#Applying changes on the fly
set globals $root/globals
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
# 8. Perform LACPDU stop on RED-LAG-LACP                                   #
################################################################################
puts "\n\nPerform LACPDU stop on RED-LAG-LACP - port1 "
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
ixNet exec lacpStopPDU $RedLAGlacpPort1
# wait 90 secs for LACP timeout
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
# 10. Perform LACPDU start on RED-LAG-LACP                                 # 
################################################################################
puts "\n\nPerform LACPDU start on RED-LAG-LACP-Port1"
set RedLAGlacpPort1 [lindex [ixNet getList $RedLAGlacp port] 0]
ixNet exec lacpStartPDU $RedLAGlacpPort1
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
