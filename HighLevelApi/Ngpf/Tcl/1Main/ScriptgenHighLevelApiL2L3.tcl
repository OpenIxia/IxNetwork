# IxNetwork version: 8.10.1046.6
# time of scriptgen: 11/8/2016, 10:05 AM

package require Ixia; # ixia hlt package
# ixNet connect localhost -version 8.10

# if not already defined, define logging and errorhandler
# callbacks
if {![info exists ::ixnHLT_log]} {
    proc ::my_ixnhlt_logger {s} {
        puts $s; flush stderr; update; update idletasks
    }
    set ::ixnHLT_log ::my_ixnhlt_logger
}
if {![info exists ::ixnHLT_errorHandler]} {
    proc ::my_ixnhlt_errorhandler {module status} {
        set msg "FAIL - $module - [keylget status log]"
        $::ixnHLT_log $msg
        return -code error $msg
    }
    set ::ixnHLT_errorHandler ::my_ixnhlt_errorhandler
}
            

proc ixnHLT_connectedPathList {ixnHLT_N} {
    upvar $ixnHLT_N ixnHLT
    set path_list [ixnHLT_vportPathList ixnHLT "connected"]
    # consider the topology connected
    # if at least one of the vports for the topology is connected 
    set connected_vpaths $path_list
    foreach {t v} [ixnHLT_collectTopologyVports ixnHLT] {
        foreach v_item $v {
            if {[lsearch $connected_vpaths $v_item] != -1} {
                if {[lsearch $path_list $t] == -1} {lappend path_list $t}
            }
        }
    }
    return $path_list
}
proc ixnHLT_vportPathList {ixnHLT_N {type all}} {
    upvar $ixnHLT_N ixnHLT
    set path_list {}
    set source_data {}
    if {[info exists ixnHLT(path_list)]} { set source_data $ixnHLT(path_list) }
    foreach path_elem_0 $source_data {
        foreach path_elem_1 $path_elem_0 {
            if {$type == "all"} {
                lappend path_list $path_elem_1
            } elseif {$type == "connected"} {
                if {![info exists ixnHLT(unconnected_path_list)]} {
                    lappend path_list $path_elem_1
                } elseif {[info exists ixnHLT(unconnected_path_list)] &&  [lsearch $ixnHLT(unconnected_path_list) $path_elem_1] == -1} {
                    lappend path_list $path_elem_1
                }
            }
        }
    }
    return $path_list
}
proc ixnHLT_collectTopologyVports {ixnHLT_N} {
    upvar $ixnHLT_N ixnHLT
    # clear out exists topology-vports.* elements
    array set rval {}
    set r [ixNet getRoot]
    set failed [catch {
        set t_list [ixNet getList $r topology]
    }] 
    if {$failed} {
        # no topology present in this configuration
        return {}
    }
    foreach t $t_list {
        # convert to ixnet style path from internal format path
        # - remove the ::ixNet::OBJ- cruft
        # - convert :NN indexes to :<NN> indexes
        # - use leading double slash instead of single slash
        # eg .. convert ::ixNet::OBJ-/topology:1 to //topology:<1>
        set p_list [ixNet getList $t port]
        foreach p $p_list {
            set a [ixNet getAttribute $p -vport]
            set aa //[join [lrange [split $a "/"] 1 end] "/"]
            set tt //[join [lrange [split $t "/"] 1 end] "/"]
            set tt [regsub -all {:([0-9]+)} $tt {:<\1>}]
            set aa [regsub -all {:([0-9]+)} $aa {:<\1>}]
            lappend rval($tt) $aa
        }
    }
    array get rval
}
proc ixnHLT_endpointMatch {ixnHLT_N ixnpattern_list {handle_type "HANDLE"}} {
    upvar $ixnHLT_N ixnHLT
    
    set traffic_ep_ignore_list {
        {^::ixNet::OBJ-/vport:\d+/protocols/mld/host:\d+$}
        {^::ixNet::OBJ-/vport:\d+/protocolStack/ethernet:[^/]+/ipEndpoint:[^/]+/range:[^/]+/ptpRangeOverIp:1$}
    }
    
    set rval [list]
    foreach {cpat} $ixnpattern_list {
        set pat $cpat
        if {[string range $pat 0 0] != "^"}     { set pat "^$pat" }
        if {[string range $pat end end] != "$"} { set pat "$pat\$" }
        foreach {n} [lsort -dictionary [array names ixnHLT "$handle_type,*"]] {
            # note there could be stuff after the path so use 1, not end
            set ixn_path        [lindex [split $n ","] 1]
            set parent_ixn_path [join [lrange  [split $ixn_path /] 0 end-1] /]
            if {[info exists ixnHLT($handle_type,$parent_ixn_path)] && [llength $rval] > 0} {
                set rval_list $rval
                if {[llength $rval] == 1} {
                    set rval_list [list $rval]
                }
                set parent_ixn_index_list [lsearch -regexp -all $rval_list \
                    "^[set ixnHLT($handle_type,$parent_ixn_path)]\$"]
            } else {
                set parent_ixn_index_list ""
            }
            if {[llength $parent_ixn_index_list] == 0 && \
                [regexp $pat $ixn_path] && [string length $ixnHLT($n)] > 0 \
            } {
                if {![regexp $traffic_ep_ignore_list $ixnHLT($n)]} {
                    lappend rval $ixnHLT($n)
                }
            }
        }
    }
    return $rval
}


# ----------------------------------------------------------------
# Configuration procedure
# 

proc ixnHLT_Scriptgen_Configure {ixnHLTVarName} {
    upvar 1 $ixnHLTVarName ixnHLT
    
    # //vport
    $::ixnHLT_log interface_config://vport:<1>...
    set _result_ [::ixia::interface_config  \
        -mode config \
        -port_handle $ixnHLT(PORT-HANDLE,//vport:<1>) \
        -transmit_clock_source external \
        -tx_gap_control_mode average \
        -transmit_mode advanced \
        -port_rx_mode capture_and_measure \
        -flow_control_directed_addr 0180.c200.0001 \
        -enable_flow_control 1 \
        -internal_ppm_adjust 0 \
        -enable_data_center_shared_stats 0 \
        -data_integrity 1 \
        -additional_fcoe_stat_2 fcoe_invalid_frames \
        -ignore_link 0 \
        -additional_fcoe_stat_1 fcoe_invalid_delimiter \
        -intf_mode ethernet \
        -speed ether100 \
        -duplex full \
        -autonegotiation 1 \
        -auto_detect_instrumentation_type floating \
        -phy_mode copper \
        -master_slave_mode auto \
        -arp_refresh_interval 60 \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    # The last configure command did not scriptgen the following attributes:
    # [//vport:<1>]
    # n kBool -isConnected True
    # n kString -ixnClientVersion 8.10.1046.6
    # n kString -connectionInfo {chassis="10.219.117.101" card="1" port="1" portip="10.0.1.1"}
    # n kEnumValue -stateDetail idle
    # n kInteger -actualSpeed 1000
    # n kBool -isDirectConfigModeEnabled False
    # n kInteger -internalId 1
    # n kString -licenses {obsolete, do not use}
    # n kString -connectionStatus {10.219.117.101:01:01 }
    # n kEnumValue -state up
    # n kBool -isVMPort False
    # n kString -assignedTo 10.219.117.101:1:1
    # n kObjref -connectedTo {$ixNetSG_ref(18)}
    # n kBool -isPullOnly False
    # n kBool -isAvailable True
    # n kString -ixosChassisVersion {ixos 8.10.1250.8 ea-patch1}
    # n kString -ixnChassisVersion 8.10.1046.6
    # n kBool -isMapped True
    # n kString -name 1/1/1
    
    catch { 
        set ixnHLT(HANDLE,//vport:<1>) [keylget _result_ interface_handle] 
        lappend ixnHLT(VPORT-CONFIG-HANDLES,//vport:<1>,interface_config) \
            $ixnHLT(HANDLE,//vport:<1>)
    }
    $::ixnHLT_log {COMPLETED: interface_config}
    
    # //vport
    $::ixnHLT_log interface_config://vport:<2>...
    set _result_ [::ixia::interface_config  \
        -mode config \
        -port_handle $ixnHLT(PORT-HANDLE,//vport:<2>) \
        -transmit_clock_source external \
        -tx_gap_control_mode average \
        -transmit_mode advanced \
        -port_rx_mode capture_and_measure \
        -flow_control_directed_addr 0180.c200.0001 \
        -enable_flow_control 1 \
        -internal_ppm_adjust 0 \
        -enable_data_center_shared_stats 0 \
        -data_integrity 1 \
        -additional_fcoe_stat_2 fcoe_invalid_frames \
        -ignore_link 0 \
        -additional_fcoe_stat_1 fcoe_invalid_delimiter \
        -intf_mode ethernet \
        -speed ether100 \
        -duplex full \
        -autonegotiation 1 \
        -auto_detect_instrumentation_type floating \
        -phy_mode copper \
        -master_slave_mode auto \
        -arp_refresh_interval 60 \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    # The last configure command did not scriptgen the following attributes:
    # [//vport:<2>]
    # n kBool -isConnected True
    # n kString -ixnClientVersion 8.10.1046.6
    # n kString -connectionInfo {chassis="10.219.117.101" card="1" port="2" portip="10.0.1.2"}
    # n kEnumValue -stateDetail idle
    # n kInteger -actualSpeed 1000
    # n kBool -isDirectConfigModeEnabled False
    # n kInteger -internalId 2
    # n kString -licenses {obsolete, do not use}
    # n kString -connectionStatus {10.219.117.101:01:02 }
    # n kEnumValue -state up
    # n kBool -isVMPort False
    # n kString -assignedTo 10.219.117.101:1:2
    # n kObjref -connectedTo {$ixNetSG_ref(19)}
    # n kBool -isPullOnly False
    # n kBool -isAvailable True
    # n kString -ixosChassisVersion {ixos 8.10.1250.8 ea-patch1}
    # n kString -ixnChassisVersion 8.10.1046.6
    # n kBool -isMapped True
    # n kString -name 1/1/2
    
    catch { 
        set ixnHLT(HANDLE,//vport:<2>) [keylget _result_ interface_handle] 
        lappend ixnHLT(VPORT-CONFIG-HANDLES,//vport:<2>,interface_config) \
            $ixnHLT(HANDLE,//vport:<2>)
    }
    $::ixnHLT_log {COMPLETED: interface_config}
    
    # //vport/l1Config/rxFilters/filterPalette
    $::ixnHLT_log uds_config://vport:<1>/l1Config/rxFilters/filterPalette...
    set _result_ [::ixia::uds_config  \
        -port_handle $ixnHLT(PORT-HANDLE,//vport:<1>) \
        -uds1 1 \
        -uds1_SA any \
        -uds1_DA any \
        -uds1_error errAnyFrame \
        -uds1_framesize any \
        -uds1_framesize_from 0 \
        -uds1_framesize_to 0 \
        -uds1_pattern any \
        -uds2 1 \
        -uds2_SA any \
        -uds2_DA any \
        -uds2_error errAnyFrame \
        -uds2_framesize any \
        -uds2_framesize_from 0 \
        -uds2_framesize_to 0 \
        -uds2_pattern any \
        -uds3 1 \
        -uds3_SA any \
        -uds3_DA any \
        -uds3_error errAnyFrame \
        -uds3_framesize any \
        -uds3_framesize_from 0 \
        -uds3_framesize_to 0 \
        -uds3_pattern any \
        -uds4 1 \
        -uds4_SA any \
        -uds4_DA any \
        -uds4_error errAnyFrame \
        -uds4_framesize any \
        -uds4_framesize_from 0 \
        -uds4_framesize_to 0 \
        -uds4_pattern any \
        -uds5 1 \
        -uds5_SA any \
        -uds5_DA any \
        -uds5_error errAnyFrame \
        -uds5_framesize any \
        -uds5_framesize_from 0 \
        -uds5_framesize_to 0 \
        -uds5_pattern any \
        -uds6 1 \
        -uds6_SA any \
        -uds6_DA any \
        -uds6_error errAnyFrame \
        -uds6_framesize any \
        -uds6_framesize_from 0 \
        -uds6_framesize_to 0 \
        -uds6_pattern any \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    # The last configure command did not scriptgen the following attributes:
    # [//vport:<1>/l1Config/rxFilters/filterPalette]
    # n kString -sourceAddress1Mask 00:00:00:00:00:00
    # n kString -destinationAddress1Mask 00:00:00:00:00:00
    # n kString -sourceAddress2 00:00:00:00:00:00
    # n kEnumValue -pattern2OffsetType fromStartOfFrame
    # n kInteger -pattern2Offset 20
    # n kString -sourceAddress2Mask 00:00:00:00:00:00
    # n kString -destinationAddress2 00:00:00:00:00:00
    # n kString -destinationAddress1 00:00:00:00:00:00
    # n kString -sourceAddress1 00:00:00:00:00:00
    # n kString -pattern1 00
    # n kString -destinationAddress2Mask 00:00:00:00:00:00
    # n kInteger -pattern1Offset 20
    # n kString -pattern2 00
    # n kString -pattern2Mask 00
    # n kEnumValue -pattern1OffsetType fromStartOfFrame
    # n kString -pattern1Mask 00
    
    $::ixnHLT_log {COMPLETED: uds_config}
    
    # //vport/l1Config/rxFilters/filterPalette
    $::ixnHLT_log uds_config://vport:<2>/l1Config/rxFilters/filterPalette...
    set _result_ [::ixia::uds_config  \
        -port_handle $ixnHLT(PORT-HANDLE,//vport:<2>) \
        -uds1 1 \
        -uds1_SA any \
        -uds1_DA any \
        -uds1_error errAnyFrame \
        -uds1_framesize any \
        -uds1_framesize_from 0 \
        -uds1_framesize_to 0 \
        -uds1_pattern any \
        -uds2 1 \
        -uds2_SA any \
        -uds2_DA any \
        -uds2_error errAnyFrame \
        -uds2_framesize any \
        -uds2_framesize_from 0 \
        -uds2_framesize_to 0 \
        -uds2_pattern any \
        -uds3 1 \
        -uds3_SA any \
        -uds3_DA any \
        -uds3_error errAnyFrame \
        -uds3_framesize any \
        -uds3_framesize_from 0 \
        -uds3_framesize_to 0 \
        -uds3_pattern any \
        -uds4 1 \
        -uds4_SA any \
        -uds4_DA any \
        -uds4_error errAnyFrame \
        -uds4_framesize any \
        -uds4_framesize_from 0 \
        -uds4_framesize_to 0 \
        -uds4_pattern any \
        -uds5 1 \
        -uds5_SA any \
        -uds5_DA any \
        -uds5_error errAnyFrame \
        -uds5_framesize any \
        -uds5_framesize_from 0 \
        -uds5_framesize_to 0 \
        -uds5_pattern any \
        -uds6 1 \
        -uds6_SA any \
        -uds6_DA any \
        -uds6_error errAnyFrame \
        -uds6_framesize any \
        -uds6_framesize_from 0 \
        -uds6_framesize_to 0 \
        -uds6_pattern any \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    # The last configure command did not scriptgen the following attributes:
    # [//vport:<2>/l1Config/rxFilters/filterPalette]
    # n kString -sourceAddress1Mask 00:00:00:00:00:00
    # n kString -destinationAddress1Mask 00:00:00:00:00:00
    # n kString -sourceAddress2 00:00:00:00:00:00
    # n kEnumValue -pattern2OffsetType fromStartOfFrame
    # n kInteger -pattern2Offset 20
    # n kString -sourceAddress2Mask 00:00:00:00:00:00
    # n kString -destinationAddress2 00:00:00:00:00:00
    # n kString -destinationAddress1 00:00:00:00:00:00
    # n kString -sourceAddress1 00:00:00:00:00:00
    # n kString -pattern1 00
    # n kString -destinationAddress2Mask 00:00:00:00:00:00
    # n kInteger -pattern1Offset 20
    # n kString -pattern2 00
    # n kString -pattern2Mask 00
    # n kEnumValue -pattern1OffsetType fromStartOfFrame
    # n kString -pattern1Mask 00
    
    $::ixnHLT_log {COMPLETED: uds_config}
    
    # //vport/l1Config/rxFilters/filterPalette
    $::ixnHLT_log uds_filter_pallette_config://vport:<1>/l1Config/rxFilters/filterPalette...
    set _result_ [::ixia::uds_filter_pallette_config  \
        -port_handle $ixnHLT(PORT-HANDLE,//vport:<1>) \
        -DA1 00:00:00:00:00:00 \
        -DA2 00:00:00:00:00:00 \
        -DA_mask1 00:00:00:00:00:00 \
        -DA_mask2 00:00:00:00:00:00 \
        -pattern1 00 \
        -pattern2 00 \
        -pattern_mask1 00 \
        -pattern_mask2 00 \
        -pattern_offset1 20 \
        -pattern_offset2 20 \
        -SA1 00:00:00:00:00:00 \
        -SA2 00:00:00:00:00:00 \
        -SA_mask1 00:00:00:00:00:00 \
        -SA_mask2 00:00:00:00:00:00 \
        -pattern_offset_type1 startOfFrame \
        -pattern_offset_type2 startOfFrame \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    $::ixnHLT_log {COMPLETED: uds_filter_pallette_config}
    
    # //vport/l1Config/rxFilters/filterPalette
    $::ixnHLT_log uds_filter_pallette_config://vport:<2>/l1Config/rxFilters/filterPalette...
    set _result_ [::ixia::uds_filter_pallette_config  \
        -port_handle $ixnHLT(PORT-HANDLE,//vport:<2>) \
        -DA1 00:00:00:00:00:00 \
        -DA2 00:00:00:00:00:00 \
        -DA_mask1 00:00:00:00:00:00 \
        -DA_mask2 00:00:00:00:00:00 \
        -pattern1 00 \
        -pattern2 00 \
        -pattern_mask1 00 \
        -pattern_mask2 00 \
        -pattern_offset1 20 \
        -pattern_offset2 20 \
        -SA1 00:00:00:00:00:00 \
        -SA2 00:00:00:00:00:00 \
        -SA_mask1 00:00:00:00:00:00 \
        -SA_mask2 00:00:00:00:00:00 \
        -pattern_offset_type1 startOfFrame \
        -pattern_offset_type2 startOfFrame \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    $::ixnHLT_log {COMPLETED: uds_filter_pallette_config}
    
    # The following objects had no attributes that were scriptgenned:
    # n //globals/interfaces
    # n //statistics/measurementMode
    # n //vport:<1>/l1Config/ethernet/fcoe
    # n //vport:<1>/capture/trigger
    # n //vport:<1>/capture/filter
    # n //vport:<1>/capture/filterPallette
    # n //vport:<2>/l1Config/ethernet/fcoe
    # n //vport:<2>/capture/trigger
    # n //vport:<2>/capture/filter
    # n //vport:<2>/capture/filterPallette
    # n //globals/testInspector
    # n //globals/preferences
    # n //reporter
    # n //reporter/testParameters
    # n //reporter/generate
    # n //reporter/saveResults
    # n //statistics/rawData
    # n //statistics/autoRefresh
    # n //impairment
    # n //impairment/defaultProfile
    # n //impairment/defaultProfile/checksums
    # n //impairment/defaultProfile/rxRateLimit
    # n //impairment/defaultProfile/drop
    # n //impairment/defaultProfile/reorder
    # n //impairment/defaultProfile/duplicate
    # n //impairment/defaultProfile/bitError
    # n //impairment/defaultProfile/delay
    # n //impairment/defaultProfile/delayVariation
    # n //impairment/defaultProfile/customDelayVariation
    # n //quickTest
    # n //quickTest/globals
    # n //vport:<1>/l1Config/ethernet/oam
    # n //vport:<1>/l1Config/OAM
    # n //vport:<1>/protocols
    # n //vport:<1>/protocols/openFlow
    # n //vport:<1>/protocols/openFlow/hostTopologyLearnedInformation/switchHostRangeLearnedInfoTriggerAttributes
    # n //vport:<1>/protocolStack/options
    # n //vport:<2>/l1Config/ethernet/oam
    # n //vport:<2>/l1Config/OAM
    # n //vport:<2>/protocols
    # n //vport:<2>/protocols/openFlow
    # n //vport:<2>/protocols/openFlow/hostTopologyLearnedInformation/switchHostRangeLearnedInfoTriggerAttributes
    # n //vport:<2>/protocolStack/options
    # n //globals/testInspector/statistic:<1>
    # n //globals/testInspector/statistic:<2>
    # n //globals/testInspector/statistic:<3>
    # n //globals/testInspector/statistic:<4>
    # n //globals/testInspector/statistic:<5>
    # n //globals/testInspector/statistic:<6>
    # n //globals/testInspector/statistic:<7>
    # n //globals/testInspector/statistic:<8>
    # n {//statistics/rawData/statistic:"Tx Frames"}
    # n {//statistics/rawData/statistic:"Rx Frames"}
    # n {//statistics/rawData/statistic:"Frames Delta"}
    # n {//statistics/rawData/statistic:"Tx Frame Rate"}
    # n {//statistics/rawData/statistic:"Rx Frames Rate"}
    # n {//statistics/rawData/statistic:"Avg Latency (us)"}
    # n {//statistics/rawData/statistic:"Min Latency (us)"}
    # n {//statistics/rawData/statistic:"Max Latency (us)"}
    # n {//statistics/rawData/statistic:"Minimum Delay Variation"}
    # n {//statistics/rawData/statistic:"Maximum Delay Variation"}
    # n {//statistics/rawData/statistic:"Avg Delay Variation"}
    # n {//statistics/rawData/statistic:"Reordered Packets"}
    # n {//statistics/rawData/statistic:"Lost Packets"}
    # end of list
    
    return 0
}

proc ixnCPF_Scriptgen_Configure {ixnHLTVarName} {
    upvar 1 $ixnHLTVarName ixnHLT
    
    set topology_1_status [::ixiangpf::topology_config \
        -topology_name      {Topology 1}                            \
        -port_handle        "$ixnHLT(PORT-HANDLE,//vport:<1>)"      \
    ]
    if {[keylget topology_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $topology_1_status
    }
    set topology_1_handle [keylget topology_1_status topology_handle]
    set ixnHLT(HANDLE,//topology:<1>) $topology_1_handle
    
    set device_group_1_status [::ixiangpf::topology_config \
        -topology_handle              $topology_1_handle      \
        -device_group_name            {Basic L3-1}            \
        -device_group_multiplier      3                       \
        -device_group_enabled         1                       \
    ]
    if {[keylget device_group_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $device_group_1_status
    }
    set deviceGroup_1_handle [keylget device_group_1_status device_group_handle]
    set ixnHLT(HANDLE,//topology:<1>/deviceGroup:<1>) $deviceGroup_1_handle
    
    set ethernet_1_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 1}               \
        -protocol_handle              $deviceGroup_1_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 00.01.01.01.00.01          \
        -src_mac_addr_step            00.00.00.00.00.01          \
        -vlan                         0                          \
        -vlan_id                      101                        \
        -vlan_id_step                 1                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    # n The attribute: useVlans with the value: False is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    # n Node: pbbEVpnParameter is not supported for scriptgen.
    if {[keylget ethernet_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ethernet_1_status
    }
    set ethernet_1_handle [keylget ethernet_1_status ethernet_handle]
    set ixnHLT(HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>) $ethernet_1_handle
    
    set ipv4_1_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv4 1}                \
        -protocol_handle                   $ethernet_1_handle      \
        -ipv4_resolve_gateway              1                       \
        -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
        -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
        -gateway                           1.1.1.4                 \
        -gateway_step                      0.0.0.0                 \
        -intf_ip_addr                      1.1.1.1                 \
        -intf_ip_addr_step                 0.0.0.1                 \
        -netmask                           255.255.255.0           \
    ]
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    if {[keylget ipv4_1_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ipv4_1_status
    }
    set ipv4_1_handle [keylget ipv4_1_status ipv4_handle]
    set ixnHLT(HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>) $ipv4_1_handle
    
    set topology_2_status [::ixiangpf::topology_config \
        -topology_name      {Topology 2}                            \
        -port_handle        "$ixnHLT(PORT-HANDLE,//vport:<2>)"      \
    ]
    if {[keylget topology_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $topology_2_status
    }
    set topology_2_handle [keylget topology_2_status topology_handle]
    set ixnHLT(HANDLE,//topology:<2>) $topology_2_handle
    
    set device_group_2_status [::ixiangpf::topology_config \
        -topology_handle              $topology_2_handle      \
        -device_group_name            {Basic L3-2}            \
        -device_group_multiplier      3                       \
        -device_group_enabled         1                       \
    ]
    if {[keylget device_group_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $device_group_2_status
    }
    set deviceGroup_2_handle [keylget device_group_2_status device_group_handle]
    set ixnHLT(HANDLE,//topology:<2>/deviceGroup:<1>) $deviceGroup_2_handle
    
    set ethernet_2_status [::ixiangpf::interface_config \
        -protocol_name                {Ethernet 2}               \
        -protocol_handle              $deviceGroup_2_handle      \
        -mtu                          1500                       \
        -src_mac_addr                 00.01.01.02.00.01          \
        -src_mac_addr_step            00.00.00.00.00.01          \
        -vlan                         0                          \
        -vlan_id                      101                        \
        -vlan_id_step                 1                          \
        -vlan_id_count                1                          \
        -vlan_tpid                    0x8100                     \
        -vlan_user_priority           0                          \
        -vlan_user_priority_step      0                          \
        -use_vpn_parameters           0                          \
        -site_id                      0                          \
    ]
    # n The attribute: useVlans with the value: False is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    # n Node: pbbEVpnParameter is not supported for scriptgen.
    if {[keylget ethernet_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ethernet_2_status
    }
    set ethernet_2_handle [keylget ethernet_2_status ethernet_handle]
    set ixnHLT(HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>) $ethernet_2_handle
    
    set ipv4_2_status [::ixiangpf::interface_config \
        -protocol_name                     {IPv4 2}                \
        -protocol_handle                   $ethernet_2_handle      \
        -ipv4_resolve_gateway              1                       \
        -ipv4_manual_gateway_mac           00.00.00.00.00.01       \
        -ipv4_manual_gateway_mac_step      00.00.00.00.00.00       \
        -gateway                           1.1.1.1                 \
        -gateway_step                      0.0.0.0                 \
        -intf_ip_addr                      1.1.1.4                 \
        -intf_ip_addr_step                 0.0.0.1                 \
        -netmask                           255.255.255.0           \
    ]
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    if {[keylget ipv4_2_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ipv4_2_status
    }
    set ipv4_2_handle [keylget ipv4_2_status ipv4_handle]
    set ixnHLT(HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>) $ipv4_2_handle
    
    # n Node: /globals/topology/ipv6Autoconfiguration does not have global settings.
    # n Node: /globals/topology/ipv6 does not have global settings.
    # n Node: /globals/topology/bfdRouter does not have global settings.
    # n Node: /globals/topology/ospfv2Router does not have global settings.
    # n Node: /globals/topology/ospfv3Router does not have global settings.
    # n Node: /globals/topology/pimRouter does not have global settings.
    # n Node: /globals/topology/rsvpteIf does not have global settings.
    # n Node: /globals/topology/rsvpteLsps does not have global settings.
    # n Node: /globals/topology/isisFabricPathRouter does not have global settings.
    # n Node: /globals/topology/isisL3Router does not have global settings.
    # n Node: /globals/topology/isisSpbRouter does not have global settings.
    # n Node: /globals/topology/isisTrillRouter does not have global settings.
    # n Node: /globals/topology/igmpHost does not have global settings.
    # n Node: /globals/topology/mldHost does not have global settings.
    # n Node: /globals/topology/ldpBasicRouterV6 does not have global settings.
    # n Node: /globals/topology/ldpBasicRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouterV6 does not have global settings.
    # n Node: /globals/topology/msrpListener does not have global settings.
    # n Node: /globals/topology/msrpTalker does not have global settings.
    # n Node: /globals/topology/bgpIpv4Peer does not have global settings.
    # n Node: /globals/topology/bgpIpv6Peer does not have global settings.
    # n Node: /globals/topology/igmpQuerier does not have global settings.
    # n Node: /globals/topology/mldQuerier does not have global settings.
    # n Node: /globals/topology/dhcpv4client does not have global settings.
    # n Node: /globals/topology/dhcpv6client does not have global settings.
    # n Node: /globals/topology/dhcpv4server does not have global settings.
    # n Node: /globals/topology/dhcpv6server does not have global settings.
    # n Node: /globals/topology/dhcpv4relayAgent does not have global settings.
    # n Node: /globals/topology/lightweightDhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/dhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/pppoxclient does not have global settings.
    # n Node: /globals/topology/pppoxserver does not have global settings.
    # n Node: /globals/topology/lac does not have global settings.
    # n Node: /globals/topology/lns does not have global settings.
    # n Node: /globals/topology/vxlan does not have global settings.
    # n Node: /globals/topology/greoipv4 does not have global settings.
    # n Node: /globals/topology/greoipv6 does not have global settings.
    # n Node: /globals/topology/ptp does not have global settings.
    # n Node: /globals/topology/ancp does not have global settings.
    # n Node: /globals/topology/lacp does not have global settings.
    # n Node: /globals/topology/staticLag does not have global settings.
    # n Node: /globals/topology/openFlowChannel does not have global settings.
    # n Node: /globals/topology/openFlowController does not have global settings.
    # n Node: /globals/topology/ovsdbserver does not have global settings.
    
    set ipv4_3_status [::ixiangpf::interface_config \
        -protocol_handle                    /globals      \
        -arp_on_linkup                      0             \
        -single_arp_per_gateway             1             \
        -ipv4_send_arp_rate                 200           \
        -ipv4_send_arp_interval             1000          \
        -ipv4_send_arp_max_outstanding      400           \
        -ipv4_send_arp_scale_mode           port          \
        -ipv4_attempt_enabled               0             \
        -ipv4_attempt_rate                  200           \
        -ipv4_attempt_interval              1000          \
        -ipv4_attempt_scale_mode            port          \
        -ipv4_diconnect_enabled             0             \
        -ipv4_disconnect_rate               200           \
        -ipv4_disconnect_interval           1000          \
        -ipv4_disconnect_scale_mode         port          \
        -ipv4_re_send_arp_on_link_up        true          \
    ]
    if {[keylget ipv4_3_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ipv4_3_status
    }
    
    set ethernet_3_status [::ixiangpf::interface_config \
        -protocol_handle                     /globals      \
        -ethernet_attempt_enabled            0             \
        -ethernet_attempt_rate               200           \
        -ethernet_attempt_interval           1000          \
        -ethernet_attempt_scale_mode         port          \
        -ethernet_diconnect_enabled          0             \
        -ethernet_disconnect_rate            200           \
        -ethernet_disconnect_interval        1000          \
        -ethernet_disconnect_scale_mode      port          \
    ]
    if {[keylget ethernet_3_status status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $ethernet_3_status
    }
    
    # n Node: /globals/topology/ipv6Autoconfiguration does not have global settings.
    # n Node: /globals/topology/ipv6 does not have global settings.
    # n Node: /globals/topology/bfdRouter does not have global settings.
    # n Node: /globals/topology/ospfv2Router does not have global settings.
    # n Node: /globals/topology/ospfv3Router does not have global settings.
    # n Node: /globals/topology/pimRouter does not have global settings.
    # n Node: /globals/topology/rsvpteIf does not have global settings.
    # n Node: /globals/topology/rsvpteLsps does not have global settings.
    # n Node: /globals/topology/isisFabricPathRouter does not have global settings.
    # n Node: /globals/topology/isisL3Router does not have global settings.
    # n Node: /globals/topology/isisSpbRouter does not have global settings.
    # n Node: /globals/topology/isisTrillRouter does not have global settings.
    # n Node: /globals/topology/igmpHost does not have global settings.
    # n Node: /globals/topology/mldHost does not have global settings.
    # n Node: /globals/topology/ldpBasicRouterV6 does not have global settings.
    # n Node: /globals/topology/ldpBasicRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouterV6 does not have global settings.
    # n Node: /globals/topology/msrpListener does not have global settings.
    # n Node: /globals/topology/msrpTalker does not have global settings.
    # n Node: /globals/topology/bgpIpv4Peer does not have global settings.
    # n Node: /globals/topology/bgpIpv6Peer does not have global settings.
    # n Node: /globals/topology/igmpQuerier does not have global settings.
    # n Node: /globals/topology/mldQuerier does not have global settings.
    # n Node: /globals/topology/dhcpv4client does not have global settings.
    # n Node: /globals/topology/dhcpv6client does not have global settings.
    # n Node: /globals/topology/dhcpv4server does not have global settings.
    # n Node: /globals/topology/dhcpv6server does not have global settings.
    # n Node: /globals/topology/dhcpv4relayAgent does not have global settings.
    # n Node: /globals/topology/lightweightDhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/dhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/pppoxclient does not have global settings.
    # n Node: /globals/topology/pppoxserver does not have global settings.
    # n Node: /globals/topology/lac does not have global settings.
    # n Node: /globals/topology/lns does not have global settings.
    # n Node: /globals/topology/vxlan does not have global settings.
    # n Node: /globals/topology/greoipv4 does not have global settings.
    # n Node: /globals/topology/greoipv6 does not have global settings.
    # n Node: /globals/topology/ptp does not have global settings.
    # n Node: /globals/topology/ancp does not have global settings.
    # n Node: /globals/topology/lacp does not have global settings.
    # n Node: /globals/topology/staticLag does not have global settings.
    # n Node: /globals/topology/openFlowChannel does not have global settings.
    # n Node: /globals/topology/openFlowController does not have global settings.
    # n Node: /globals/topology/ovsdbserver does not have global settings.
}

proc ixnHLT_Scriptgen_RunTest {ixnHLTVarName} {
    upvar 1 $ixnHLTVarName ixnHLT
    
    # #######################
    # start phase of the test
    # #######################
    $::ixnHLT_log {Waiting 60 seconds before starting protocol(s) ...}
    after 60000
    
    $::ixnHLT_log {Starting all protocol(s) ...}
    set r [::ixia::test_control -action start_all_protocols]
    if {[keylget r status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $r
    }
    
    after 30000


    
                    
    # 
    #  Reset traffic
    # 
    $::ixnHLT_log {Resetting traffic...}
    set _result_ [::ixia::traffic_control  \
        -action reset \
        -traffic_generator ixnetwork_540 \
        -cpdp_convergence_enable 0 \
        -l1_rate_stats_enable  1 \
        -misdirected_per_flow  0 \
        -delay_variation_enable 0 \
        -packet_loss_duration_enable 0 \
        -latency_bins enabled \
        -latency_control store_and_forward \
        -instantaneous_stats_enable 0 \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    set port_handles_for_traffic_stats {}
    #
    # Collect port_handles_for_traffic_stats
    #
    foreach {t v} [array get ixnHLT PORT-HANDLE,*] {
        lappend port_handles_for_traffic_stats $v
    }
    set port_handles_for_traffic_stats [lsort -unique $port_handles_for_traffic_stats]
                    
    # 
    #  Configure traffic for all configuration elements
    # 
    #  -- Traffic item //traffic/trafficItem:<1>
    $::ixnHLT_log {Configuring traffic for traffic item: //traffic/trafficItem:<1>}
    set ti_srcs(EndpointSet-1) [ixnHLT_endpointMatch ixnHLT [list //topology:<1>] HANDLE]
    if {[llength $ti_srcs(EndpointSet-1)] == 0} {
        error "Cannot find any src endpoints for elem EndpointSet-1"
    }
    set ti_dsts(EndpointSet-1) [ixnHLT_endpointMatch ixnHLT [list //topology:<2>] HANDLE]
    if {[llength $ti_dsts(EndpointSet-1)] == 0} {
        error "Cannot find any dst endpoints for elem EndpointSet-1"
    }
    
    set _result_ [::ixia::traffic_config  \
        -mode create \
        -traffic_generator ixnetwork_540 \
        -endpointset_count 1 \
        -emulation_src_handle [list [list $ti_srcs(EndpointSet-1)]] \
        -emulation_dst_handle [list [list $ti_dsts(EndpointSet-1)]] \
        -emulation_multicast_dst_handle [list [list]] \
        -emulation_multicast_dst_handle_type [list [list]] \
        -global_dest_mac_retry_count 1 \
        -global_dest_mac_retry_delay 5 \
        -enable_data_integrity 1 \
        -global_enable_dest_mac_retry 1 \
        -global_enable_min_frame_size 0 \
        -global_enable_staggered_transmit 0 \
        -global_enable_stream_ordering 0 \
        -global_stream_control continuous \
        -global_stream_control_iterations 1 \
        -global_large_error_threshhold 2 \
        -global_enable_mac_change_on_fly 0 \
        -global_max_traffic_generation_queries 500 \
        -global_mpls_label_learning_timeout 30 \
        -global_refresh_learned_info_before_apply 0 \
        -global_use_tx_rx_sync 1 \
        -global_wait_time 1 \
        -global_display_mpls_current_label_value 0 \
        -global_detect_misdirected_packets 0 \
        -global_frame_ordering none \
        -frame_sequencing disable \
        -frame_sequencing_mode rx_threshold \
        -src_dest_mesh one_to_one \
        -route_mesh one_to_one \
        -bidirectional 0 \
        -allow_self_destined 0 \
        -use_cp_rate 1 \
        -use_cp_size 1 \
        -enable_dynamic_mpls_labels 0 \
        -hosts_per_net 1 \
        -name TI0-Traffic_Item_1 \
        -source_filter all \
        -destination_filter all \
        -tag_filter [list [list]] \
        -merge_destinations 1 \
        -circuit_endpoint_type ipv4 \
        -pending_operations_timeout 30 \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    #  -- All current config elements
    set config_elements [keylget _result_ traffic_item]
    
    #  -- Config Element //traffic/trafficItem:<1>/configElement:<1>
    $::ixnHLT_log {Configuring options for config elem: //traffic/trafficItem:<1>/configElement:<1>}
    set _result_ [::ixia::traffic_config  \
        -mode modify \
        -traffic_generator ixnetwork_540 \
        -stream_id [lindex $config_elements 0] \
        -preamble_size_mode auto \
        -preamble_custom_size 8 \
        -data_pattern {} \
        -data_pattern_mode incr_byte \
        -enforce_min_gap 0 \
        -rate_percent 100 \
        -frame_rate_distribution_port split_evenly \
        -frame_rate_distribution_stream split_evenly \
        -frame_size 256 \
        -length_mode fixed \
        -tx_mode advanced \
        -transmit_mode single_burst \
        -burst_loop_count 1 \
        -pkts_per_burst 50000 \
        -tx_delay 0 \
        -tx_delay_unit bytes \
        -number_of_packets_per_stream 50000 \
        -loop_count 1 \
        -min_gap_bytes 12 \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    #  -- Endpoint set EndpointSet-1
    $::ixnHLT_log {Configuring traffic for config elem: //traffic/trafficItem:<1>/configElement:<1>}
    $::ixnHLT_log {Configuring traffic for endpoint set: EndpointSet-1}
    
    #  -- Stack //traffic/trafficItem:<1>/configElement:<1>/stack:"ethernet-1"
    set _result_ [::ixia::traffic_config  \
        -mode modify_or_insert \
        -traffic_generator ixnetwork_540 \
        -stream_id [lindex $config_elements 0] \
        -stack_index 1 \
        -l2_encap ethernet_ii \
        -mac_src_mode fixed \
        -mac_src_tracking 0 \
        -mac_src 00:00:00:00:00:00 \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    #  -- Stack //traffic/trafficItem:<1>/configElement:<1>/stack:"ipv4-2"
    set _result_ [::ixia::traffic_config  \
        -mode modify_or_insert \
        -traffic_generator ixnetwork_540 \
        -stream_id [lindex $config_elements 0] \
        -stack_index 2 \
        -l3_protocol ipv4 \
        -qos_type_ixn tos \
        -ip_precedence_mode fixed \
        -ip_precedence 0 \
        -ip_precedence_tracking 0 \
        -ip_delay_mode fixed \
        -ip_delay 0 \
        -ip_delay_tracking 0 \
        -ip_throughput_mode fixed \
        -ip_throughput 0 \
        -ip_throughput_tracking 0 \
        -ip_reliability_mode fixed \
        -ip_reliability 0 \
        -ip_reliability_tracking 0 \
        -ip_cost_mode fixed \
        -ip_cost 0 \
        -ip_cost_tracking 0 \
        -ip_cu_mode fixed \
        -ip_cu 0 \
        -ip_cu_tracking 0 \
        -ip_id_mode fixed \
        -ip_id 0 \
        -ip_id_tracking 0 \
        -ip_reserved_mode fixed \
        -ip_reserved 0 \
        -ip_reserved_tracking 0 \
        -ip_fragment_mode fixed \
        -ip_fragment 1 \
        -ip_fragment_tracking 0 \
        -ip_fragment_last_mode fixed \
        -ip_fragment_last 1 \
        -ip_fragment_last_tracking 0 \
        -ip_fragment_offset_mode fixed \
        -ip_fragment_offset 0 \
        -ip_fragment_offset_tracking 0 \
        -ip_ttl_mode fixed \
        -ip_ttl 64 \
        -ip_ttl_tracking 0 \
        -track_by {sourceDestValuePair0 flowGroup0 trackingenabled0} \
        -egress_tracking none \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    #  -- Post Options
    $::ixnHLT_log {Configuring post options for config elem: //traffic/trafficItem:<1>/configElement:<1>}
    set _result_ [::ixia::traffic_config  \
        -mode modify \
        -traffic_generator ixnetwork_540 \
        -stream_id [lindex $config_elements 0] \
        -transmit_distribution none \
    ]
    # Check status
    if {[keylget _result_ status] != $::SUCCESS} {
      $::ixnHLT_errorHandler [info script] $_result_
    }
    
    

    # 
    # Configure traffic for Layer 4-7 AppLibrary Profile
    # 
    

    #
    # Start traffic configured earlier
    #
    $::ixnHLT_log "Running Traffic..."
    set r [::ixia::traffic_control \
        -action run \
        -traffic_generator ixnetwork_540 \
        -type l23 \
    ]
    if {[keylget r status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $r
    }
                
    after 30000
    
    # ################################
    # protocol stats phase of the test
    # ################################
    
    #  stats for:
    #  packet_config_buffers handles
    $::ixnHLT_log {getting stats for packet_config_buffers configuration elements}
    after [expr 5*1000]
                    
    foreach {vport_path} [ixnHLT_vportPathList ixnHLT "connected"] {
        set port_handle $ixnHLT(PORT-HANDLE,$vport_path)
        if {![info exists ixnHLT(VPORT-CONFIG-HANDLES,$vport_path,packet_config_buffers)]} {
            continue
        }
        set items $ixnHLT(VPORT-CONFIG-HANDLES,$vport_path,packet_config_buffers)
        if {![llength $items]} {
            continue
        }
        $::ixnHLT_log "$vport_path..."
        set r [::ixia::packet_stats -port_handle $port_handle -stop 1]
        if {[keylget r status] != $::SUCCESS} {
            $::ixnHLT_errorHandler [info script] $r
        }
        if {[info exists ixnHLT(processstats)] &&
            [llength [info commands $ixnHLT(processstats)]]} {
            #catch {$ixnHLT(processstats) packet_config_buffers $port_handle $r}"
            $ixnHLT(processstats) packet_config_buffers $port_handle $r
        } else {
            $::ixnHLT_log "-----------------------------------"
            $::ixnHLT_log ::ixia::packet_stats
            foreach {stat} [keylkeys r $port_handle.aggregate] {
                set v [keylget r $port_handle.aggregate.$stat]
                $::ixnHLT_log [format {%40s = %s} $stat $v]
            }
            $::ixnHLT_log ""
        }
    }
                
    # ######################
    # stop phase of the test
    # ######################
    #
    # Stop traffic started earlier
    #
    $::ixnHLT_log "Stopping Traffic..."
    set r [::ixia::traffic_control \
        -action stop \
        -traffic_generator ixnetwork_540 \
        -type l23 ]
    if {[keylget r status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $r
    }
    
    # ###############################
    # traffic stats phase of the test
    # ###############################
    after 30000
                    
    #
    # print stats for all ports that are involved w/ 
    # ixnHLT(TRAFFIC-ENDPOINT-HANDLES)
    #
    $::ixnHLT_log "Traffic stats"
    for {set traffic_stats_retry 0} {$traffic_stats_retry < 120} {incr traffic_stats_retry} {
        set r [::ixia::traffic_stats \
            -mode aggregate \
            -traffic_generator ixnetwork_540 \
            -measure_mode mixed \
        ]
        if {[keylget r status] != $::SUCCESS} {
            $::ixnHLT_errorHandler [info script] $r
        }
                        
        if {![keylget r waiting_for_stats]} {
            break
        }
                        
        $::ixnHLT_log "Traffic waiting_for_stats flag is 1. Trial $traffic_stats_retry"
        after 1000
    }
                    
    if {[keylget r waiting_for_stats]} {
        keylset r log "Traffic statistics are not ready after 120 seconds. waiting_for_stats is 1"
        $::ixnHLT_errorHandler [info script] $r
    }
                    
    foreach {port_handle} $port_handles_for_traffic_stats {
        $::ixnHLT_log ""
        $::ixnHLT_log "port $port_handle"
        $::ixnHLT_log -----------------------------------
        $::ixnHLT_log TX
        set statlist [keylkeys r $port_handle.aggregate.tx]
        foreach {stat} $statlist {
            set v [keylget r $port_handle.aggregate.tx.$stat]
            $::ixnHLT_log [format {%40s = %s} $stat $v]
        }
        $::ixnHLT_log RX
        set statlist [keylkeys r $port_handle.aggregate.rx]
        foreach {stat} $statlist {
            set v [keylget r $port_handle.aggregate.rx.$stat]
            $::ixnHLT_log [format {%40s = %s} $stat $v]
        }
        $::ixnHLT_log ""
    }
    
    $::ixnHLT_log {Stopping all protocol(s) ...}
    set r [::ixia::test_control -action stop_all_protocols]
    if {[keylget r status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $r
    }
                    
}
#  reset ixnHLT
catch {unset ixnHLT}; array set ixnHLT {}

# ----------------------------------------------------------------
#  chassis, card, port configuration
# 
#  port_list needs to match up with path_list below
# 
set chassis {10.219.117.101}
set tcl_server 10.219.117.101
set port_list {{1/1 1/2}}
set vport_name_list {{1/1/1 1/1/2}}
set guard_rail none
# 
#  this should match up w/ your port_list above
# 
set ixnHLT(path_list) {{//vport:<1> //vport:<2>}}
# 
# 
set _result_ [::ixiangpf::connect  \
    -reset 1 \
    -device $chassis \
    -port_list $port_list \
    -ixnetwork_tcl_server localhost \
    -tcl_server $tcl_server \
    -guard_rail $guard_rail \
    -return_detailed_handles 0 \
]
# Check status
if {[keylget _result_ status] != $::SUCCESS} {
  $::ixnHLT_errorHandler [info script] $_result_
}
foreach {port_list_elem} $port_list         \
        {name_list_elem} $vport_name_list   \
        {path_list_elem} $ixnHLT(path_list) \
        {chassis_elem}   $chassis {

    set ch_vport_list [list]
    foreach {port} $port_list_elem {path} $path_list_elem {
        if {[catch {keylget _result_ port_handle.$chassis_elem.$port} _port_handle]} {
            error "connection status: $_result_: $_port_handle"
        }
        set ixnHLT(PORT-HANDLE,$path) $_port_handle
        lappend ch_vport_list $_port_handle
    }

    set vpinfo_rval [::ixia::vport_info     \
        -mode set_info                      \
        -port_list $ch_vport_list           \
        -port_name_list $name_list_elem     \
    ]
    if {[keylget vpinfo_rval status] != $::SUCCESS} {
        $::ixnHLT_errorHandler [info script] $vpinfo_rval
    }
}
            

# 
if {[llength [info commands obj_config_placeholder]]==0} {
    proc obj_config_placeholder {args} {}
}

# ----------------------------------------------------------------

#call the procedure that configures legacy implementation
ixnHLT_Scriptgen_Configure ixnHLT

#call the procedure that configures CPF
#this should be called after the call to legacy implementation
ixnCPF_Scriptgen_Configure ixnHLT

ixnHLT_Scriptgen_RunTest ixnHLT
