#!/usr/bin/tclsh
################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################

################################################################################
# Description:                                                                 
#    This script intends to demonstrate how to use IEEE 802.1x API
#    It will do the  following :
#1.    Add topology and devicegroup 
#2.    Configure ethernet and dot1x Layer.
#3.    Change protocol type to PEAPV0
#4.    Change few global parameters
#5.    Start of Device group
#6.    Check for session info and stats
#7.    Stop of Device group
################################################################################

namespace eval ::py {
    set ixTclServer 10.39.65.1
    set ixTclPort   8009
    set ports       {{10.39.65.187 1 4}}
}

puts "Load ixNetwork Tcl API package"
package req IxTclNetwork

puts "Connect to IxNetwork Tcl server"
ixNet connect $::py::ixTclServer -port $::py::ixTclPort -version 8.50\
    –setAttribute strict

puts "Creating a new config"
ixNet exec newConfig

##############################################################################
# Connecting to IxTCl server and cretaing new config                           
##############################################################################
puts "Adding 1 vport"
ixNet add [ixNet getRoot] vport
ixNet commit
set vPorts [ixNet getList [ixNet getRoot] vport]
set vportTx [lindex $vPorts 0]

puts "Assigning the ports"
::ixTclNet::AssignPorts $py::ports {} $vPorts force

puts "Adding topology"
ixNet add [ixNet getRoot] topology -vports $vportTx
ixNet commit
set topologies [ixNet getList [ixNet getRoot] topology]
set topo1 [lindex $topologies 0]

####################### Adding Dot1x Device Group  ##########################

puts "Adding dot1x device group"
ixNet add $topo1 deviceGroup
ixNet commit
set dot1x_dg [ixNet getList $topo1 deviceGroup]

puts "Configuring the multipliers "
ixNet setAttr $dot1x_dg -multiplier 1
ixNet setAttr $dot1x_dg -name "Dot1x DG"
ixNet commit

#############################################################################
############## Configuring Dot1x layer and change of protcol    #############
#############################################################################
puts "Add Ethernet layer"
set ethernet [ixNet add $dot1x_dg "ethernet"]
ixNet setMultiAttribute $ethernet -name "Ethernet"
ixNet commit

puts "Add Dot1x layer"
set dot1x [ixNet add $ethernet "dotOneX"]
ixNet setMultiAttribute $dot1x -name "Dot1x"
ixNet commit

puts "Change prtocol type to PEAPV0"
set dot1x_protocol [ixNet getAttribute $dot1x -protocol]
set dot1x_protocol_single_val [ixNet add $dot1x_protocol "singleValue"]
ixNet setMultiAttribute $dot1x_protocol_single_val -value eappeapv0
ixNet commit

#############################################################################   
################## Change few global parameters #############################
#############################################################################
 
puts " Change few global parameters "
set glob [ixNet getList [ixNet getRoot] "globals"]
set glob_topo [ixNet getList $glob "topology"]
set dot1x_glob [ixNet getList $glob_topo "dotOneX"]

puts "Enable Don't Logoff global parameter"
set disable_logoff [ixNet getAttribute $dot1x_glob -disableLogoff]
set disable_logoff_single_val [ixNet add $disable_logoff "singleValue"]
ixNet setMultiAttribute $disable_logoff_single_val -value true
ixNet commit

puts "Change the DUT Test mode to single host"
set dut_mode [ixNet getAttribute $dot1x_glob -dutTestMode]
set dut_mode_single_val [ixNet add $dut_mode "singleValue"]
ixNet setMultiAttribute $dut_mode_single_val -value "singlehost"
ixNet commit

puts "Change the Wait before run value"
set wait_before_run [ixNet getAttribute $dot1x_glob -waitBeforeRun]
set wait_before_run_single_val [ixNet add $wait_before_run "singleValue"]
ixNet setMultiAttribute $wait_before_run_single_val -value 10
ixNet commit

puts "Change the EAPOL Version"
set eapol_version [ixNet getAttribute $dot1x -eapolVersion]
set eapol_version_single_val [ixNet add $eapol_version "singleValue"]
ixNet setMultiAttribute $eapol_version_single_val -value "eapolver2020"
ixNet commit

puts "Enable Ignore Authenticator EAPOL Version" 
set ignore_auth_eapol_ver [ixNet getAttribute $dot1x -ignoreAuthEapolVer]
set ignore_auth_eapol_ver_single_val [ixNet add $ignore_auth_eapol_ver "singleValue"]
ixNet setMultiAttribute $ignore_auth_eapol_ver_single_val -value "true"
ixNet commit

############################################################################
################## Starting Protocols and Dispalying Statistics ############
############################################################################

puts "Starting Dot1x DeviceGroup"
ixNet exec start $dot1x_dg
after 30000

puts "Fetch the session info "
set dot1x_session_info [ixNet getAttr $dot1x -sessionInfo]
after 3000
puts "Session info - $dot1x_session_info"

puts "Fetching the Protocol stats\n"
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
puts "***************************************************"

puts "Fetching Dot1x per port stats\n"
set viewPage {::ixNet::OBJ-/statistics/view:"IEEE 802.1X Per Port"/page}
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
puts "***************************************************"

puts "Stopping Dot1x DG"
ixNet exec stop $dot1x_dg
after 30000

puts "For more info please refer to the user manual or the built-in help"
puts "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1"
puts "ixNet help ::ixNet::OBJ-/topology:1/deviceGroup:1/ethernet:1/dotOneX:1"

puts "*****************END************************"





