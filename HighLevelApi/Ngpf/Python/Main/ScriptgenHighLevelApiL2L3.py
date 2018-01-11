# IxNetwork version: 8.10.1046.6
# time of scriptgen: 11/8/2016, 10:02 AM
import sys, os
import time, re
# sys.path.append('/path/to/hltapi/library/common/ixiangpf/python')
# sys.path.append('/path/to/ixnetwork/api/python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

if os.name == 'nt':
	ixiatcl = IxiaTcl()
else:
	# unix dependencies
	tcl_dependencies = [
		'/home/user/ixia/ixos/lib',
		'/home/user/ixia/ixnet/IxTclProtocol',
		'/home/user/ixia/ixnet/IxTclNetwork'
	]
	ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)

ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)
			
def ixnHLT_endpointMatch(ixnHLT, ixnpattern_list, handle_type='HANDLE'):
	traffic_ep_ignore_list = [
		'^::ixNet::OBJ-/vport:\d+/protocols/mld/host:\d+$',
		'^::ixNet::OBJ-/vport:\d+/protocolStack/ethernet:[^/]+/ipEndpoint:[^/]+/range:[^/]+/ptpRangeOverIp:1$'
	]

	rval = []
	for pat in ixnpattern_list:
		if pat[ 0] != '^': pat = '^' + pat
		if pat[-1] != '$': pat = pat + '$'

		for path in set(x for x in ixnHLT if x.startswith(handle_type)):
			ixn_path = path.split(',')[1]
			parent_ixn_path = '/'.join(ixn_path.split('/')[:-1])
			parent_path = '%s,%s' % (handle_type, parent_ixn_path)

			parent_found = False
			if len(rval) > 0 and parent_path in ixnHLT and parent_path in rval:
				parent_found = True

			if not parent_found and re.match(pat, ixn_path) and len(ixnHLT[path]) > 0:
				if not any(re.match(x, ixnHLT[path]) for x in traffic_ep_ignore_list):
					rval.append(ixnHLT[path])

	return rval
			
# ----------------------------------------------------------------
# Configuration procedure

try:
	ixnHLT_logger('')
except (NameError,):
	def ixnHLT_logger(msg):
		print(msg)

try:
	ixnHLT_errorHandler('', {})
except (NameError,):
	def ixnHLT_errorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)
			
def ixnHLT_Scriptgen_Configure(ixiahlt, ixnHLT):
	ixiatcl = ixiahlt.ixiatcl
	# //vport
	ixnHLT_logger('interface_config://vport:<1>...')
	_result_ = ixiahlt.interface_config(
		mode='config',
		port_handle=ixnHLT['PORT-HANDLE,//vport:<1>'],
		transmit_clock_source='external',
		tx_gap_control_mode='average',
		transmit_mode='advanced',
		port_rx_mode='capture_and_measure',
		flow_control_directed_addr='0180.c200.0001',
		enable_flow_control='1',
		internal_ppm_adjust='0',
		enable_data_center_shared_stats='0',
		data_integrity='1',
		additional_fcoe_stat_2='fcoe_invalid_frames',
		ignore_link='0',
		additional_fcoe_stat_1='fcoe_invalid_delimiter',
		intf_mode='ethernet',
		speed='ether100',
		duplex='full',
		autonegotiation=1,
		auto_detect_instrumentation_type='floating',
		phy_mode='copper',
		master_slave_mode='auto',
		arp_refresh_interval='60'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	# The last configure command did not scriptgen the following attributes:
	# [//vport:<1>]
	# n kBool -isConnected 'True'
	# n kString -ixnClientVersion '8.10.1046.6'
	# n kString -connectionInfo 'chassis="10.219.117.101" card="1" port="1" portip="10.0.1.1"'
	# n kEnumValue -stateDetail 'idle'
	# n kInteger -actualSpeed '1000'
	# n kBool -isDirectConfigModeEnabled 'False'
	# n kInteger -internalId '1'
	# n kString -licenses 'obsolete, do not use'
	# n kString -connectionStatus '10.219.117.101:01:01 '
	# n kEnumValue -state 'up'
	# n kBool -isVMPort 'False'
	# n kString -assignedTo '10.219.117.101:1:1'
	# n kObjref -connectedTo '$ixNetSG_ref(18)'
	# n kBool -isPullOnly 'False'
	# n kBool -isAvailable 'True'
	# n kString -ixosChassisVersion 'ixos 8.10.1250.8 ea-patch1'
	# n kString -ixnChassisVersion '8.10.1046.6'
	# n kBool -isMapped 'True'
	# n kString -name '1/1/1'
	
	try:
		ixnHLT['HANDLE,//vport:<1>'] = _result_['interface_handle']
		config_handles = ixnHLT.setdefault('VPORT-CONFIG-HANDLES,//vport:<1>,interface_config', [])
		config_handles.append(_result_['interface_handle'])
	except:
		pass
	ixnHLT_logger('COMPLETED: interface_config')
	
	# //vport
	ixnHLT_logger('interface_config://vport:<2>...')
	_result_ = ixiahlt.interface_config(
		mode='config',
		port_handle=ixnHLT['PORT-HANDLE,//vport:<2>'],
		transmit_clock_source='external',
		tx_gap_control_mode='average',
		transmit_mode='advanced',
		port_rx_mode='capture_and_measure',
		flow_control_directed_addr='0180.c200.0001',
		enable_flow_control='1',
		internal_ppm_adjust='0',
		enable_data_center_shared_stats='0',
		data_integrity='1',
		additional_fcoe_stat_2='fcoe_invalid_frames',
		ignore_link='0',
		additional_fcoe_stat_1='fcoe_invalid_delimiter',
		intf_mode='ethernet',
		speed='ether100',
		duplex='full',
		autonegotiation=1,
		auto_detect_instrumentation_type='floating',
		phy_mode='copper',
		master_slave_mode='auto',
		arp_refresh_interval='60'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	# The last configure command did not scriptgen the following attributes:
	# [//vport:<2>]
	# n kBool -isConnected 'True'
	# n kString -ixnClientVersion '8.10.1046.6'
	# n kString -connectionInfo 'chassis="10.219.117.101" card="1" port="2" portip="10.0.1.2"'
	# n kEnumValue -stateDetail 'idle'
	# n kInteger -actualSpeed '1000'
	# n kBool -isDirectConfigModeEnabled 'False'
	# n kInteger -internalId '2'
	# n kString -licenses 'obsolete, do not use'
	# n kString -connectionStatus '10.219.117.101:01:02 '
	# n kEnumValue -state 'up'
	# n kBool -isVMPort 'False'
	# n kString -assignedTo '10.219.117.101:1:2'
	# n kObjref -connectedTo '$ixNetSG_ref(19)'
	# n kBool -isPullOnly 'False'
	# n kBool -isAvailable 'True'
	# n kString -ixosChassisVersion 'ixos 8.10.1250.8 ea-patch1'
	# n kString -ixnChassisVersion '8.10.1046.6'
	# n kBool -isMapped 'True'
	# n kString -name '1/1/2'
	
	try:
		ixnHLT['HANDLE,//vport:<2>'] = _result_['interface_handle']
		config_handles = ixnHLT.setdefault('VPORT-CONFIG-HANDLES,//vport:<2>,interface_config', [])
		config_handles.append(_result_['interface_handle'])
	except:
		pass
	ixnHLT_logger('COMPLETED: interface_config')
	
	# //vport/l1Config/rxFilters/filterPalette
	ixnHLT_logger('uds_config://vport:<1>/l1Config/rxFilters/filterPalette...')
	_result_ = ixiahlt.uds_config(
		port_handle=ixnHLT['PORT-HANDLE,//vport:<1>'],
		uds1='1',
		uds1_SA='any',
		uds1_DA='any',
		uds1_error='errAnyFrame',
		uds1_framesize='any',
		uds1_framesize_from='0',
		uds1_framesize_to='0',
		uds1_pattern='any',
		uds2='1',
		uds2_SA='any',
		uds2_DA='any',
		uds2_error='errAnyFrame',
		uds2_framesize='any',
		uds2_framesize_from='0',
		uds2_framesize_to='0',
		uds2_pattern='any',
		uds3='1',
		uds3_SA='any',
		uds3_DA='any',
		uds3_error='errAnyFrame',
		uds3_framesize='any',
		uds3_framesize_from='0',
		uds3_framesize_to='0',
		uds3_pattern='any',
		uds4='1',
		uds4_SA='any',
		uds4_DA='any',
		uds4_error='errAnyFrame',
		uds4_framesize='any',
		uds4_framesize_from='0',
		uds4_framesize_to='0',
		uds4_pattern='any',
		uds5='1',
		uds5_SA='any',
		uds5_DA='any',
		uds5_error='errAnyFrame',
		uds5_framesize='any',
		uds5_framesize_from='0',
		uds5_framesize_to='0',
		uds5_pattern='any',
		uds6='1',
		uds6_SA='any',
		uds6_DA='any',
		uds6_error='errAnyFrame',
		uds6_framesize='any',
		uds6_framesize_from='0',
		uds6_framesize_to='0',
		uds6_pattern='any'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('uds_config', _result_)
	# The last configure command did not scriptgen the following attributes:
	# [//vport:<1>/l1Config/rxFilters/filterPalette]
	# n kString -sourceAddress1Mask '00:00:00:00:00:00'
	# n kString -destinationAddress1Mask '00:00:00:00:00:00'
	# n kString -sourceAddress2 '00:00:00:00:00:00'
	# n kEnumValue -pattern2OffsetType 'fromStartOfFrame'
	# n kInteger -pattern2Offset '20'
	# n kString -sourceAddress2Mask '00:00:00:00:00:00'
	# n kString -destinationAddress2 '00:00:00:00:00:00'
	# n kString -destinationAddress1 '00:00:00:00:00:00'
	# n kString -sourceAddress1 '00:00:00:00:00:00'
	# n kString -pattern1 '00'
	# n kString -destinationAddress2Mask '00:00:00:00:00:00'
	# n kInteger -pattern1Offset '20'
	# n kString -pattern2 '00'
	# n kString -pattern2Mask '00'
	# n kEnumValue -pattern1OffsetType 'fromStartOfFrame'
	# n kString -pattern1Mask '00'
	
	ixnHLT_logger('COMPLETED: uds_config')
	
	# //vport/l1Config/rxFilters/filterPalette
	ixnHLT_logger('uds_config://vport:<2>/l1Config/rxFilters/filterPalette...')
	_result_ = ixiahlt.uds_config(
		port_handle=ixnHLT['PORT-HANDLE,//vport:<2>'],
		uds1='1',
		uds1_SA='any',
		uds1_DA='any',
		uds1_error='errAnyFrame',
		uds1_framesize='any',
		uds1_framesize_from='0',
		uds1_framesize_to='0',
		uds1_pattern='any',
		uds2='1',
		uds2_SA='any',
		uds2_DA='any',
		uds2_error='errAnyFrame',
		uds2_framesize='any',
		uds2_framesize_from='0',
		uds2_framesize_to='0',
		uds2_pattern='any',
		uds3='1',
		uds3_SA='any',
		uds3_DA='any',
		uds3_error='errAnyFrame',
		uds3_framesize='any',
		uds3_framesize_from='0',
		uds3_framesize_to='0',
		uds3_pattern='any',
		uds4='1',
		uds4_SA='any',
		uds4_DA='any',
		uds4_error='errAnyFrame',
		uds4_framesize='any',
		uds4_framesize_from='0',
		uds4_framesize_to='0',
		uds4_pattern='any',
		uds5='1',
		uds5_SA='any',
		uds5_DA='any',
		uds5_error='errAnyFrame',
		uds5_framesize='any',
		uds5_framesize_from='0',
		uds5_framesize_to='0',
		uds5_pattern='any',
		uds6='1',
		uds6_SA='any',
		uds6_DA='any',
		uds6_error='errAnyFrame',
		uds6_framesize='any',
		uds6_framesize_from='0',
		uds6_framesize_to='0',
		uds6_pattern='any'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('uds_config', _result_)
	# The last configure command did not scriptgen the following attributes:
	# [//vport:<2>/l1Config/rxFilters/filterPalette]
	# n kString -sourceAddress1Mask '00:00:00:00:00:00'
	# n kString -destinationAddress1Mask '00:00:00:00:00:00'
	# n kString -sourceAddress2 '00:00:00:00:00:00'
	# n kEnumValue -pattern2OffsetType 'fromStartOfFrame'
	# n kInteger -pattern2Offset '20'
	# n kString -sourceAddress2Mask '00:00:00:00:00:00'
	# n kString -destinationAddress2 '00:00:00:00:00:00'
	# n kString -destinationAddress1 '00:00:00:00:00:00'
	# n kString -sourceAddress1 '00:00:00:00:00:00'
	# n kString -pattern1 '00'
	# n kString -destinationAddress2Mask '00:00:00:00:00:00'
	# n kInteger -pattern1Offset '20'
	# n kString -pattern2 '00'
	# n kString -pattern2Mask '00'
	# n kEnumValue -pattern1OffsetType 'fromStartOfFrame'
	# n kString -pattern1Mask '00'
	
	ixnHLT_logger('COMPLETED: uds_config')
	
	# //vport/l1Config/rxFilters/filterPalette
	ixnHLT_logger('uds_filter_pallette_config://vport:<1>/l1Config/rxFilters/filterPalette...')
	_result_ = ixiahlt.uds_filter_pallette_config(
		port_handle=ixnHLT['PORT-HANDLE,//vport:<1>'],
		DA1='00:00:00:00:00:00',
		DA2='00:00:00:00:00:00',
		DA_mask1='00:00:00:00:00:00',
		DA_mask2='00:00:00:00:00:00',
		pattern1='0',
		pattern2='0',
		pattern_mask1='0',
		pattern_mask2='0',
		pattern_offset1='20',
		pattern_offset2='20',
		SA1='00:00:00:00:00:00',
		SA2='00:00:00:00:00:00',
		SA_mask1='00:00:00:00:00:00',
		SA_mask2='00:00:00:00:00:00',
		pattern_offset_type1='startOfFrame',
		pattern_offset_type2='startOfFrame'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('uds_filter_pallette_config', _result_)
	
	ixnHLT_logger('COMPLETED: uds_filter_pallette_config')
	
	# //vport/l1Config/rxFilters/filterPalette
	ixnHLT_logger('uds_filter_pallette_config://vport:<2>/l1Config/rxFilters/filterPalette...')
	_result_ = ixiahlt.uds_filter_pallette_config(
		port_handle=ixnHLT['PORT-HANDLE,//vport:<2>'],
		DA1='00:00:00:00:00:00',
		DA2='00:00:00:00:00:00',
		DA_mask1='00:00:00:00:00:00',
		DA_mask2='00:00:00:00:00:00',
		pattern1='0',
		pattern2='0',
		pattern_mask1='0',
		pattern_mask2='0',
		pattern_offset1='20',
		pattern_offset2='20',
		SA1='00:00:00:00:00:00',
		SA2='00:00:00:00:00:00',
		SA_mask1='00:00:00:00:00:00',
		SA_mask2='00:00:00:00:00:00',
		pattern_offset_type1='startOfFrame',
		pattern_offset_type2='startOfFrame'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('uds_filter_pallette_config', _result_)
	
	ixnHLT_logger('COMPLETED: uds_filter_pallette_config')
	
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
	
def ixnCPF_Scriptgen_Configure(ixiangpf, ixnHLT):
	ixiatcl = ixiangpf.ixiahlt.ixiatcl
	
	_result_ = ixiangpf.topology_config(
		topology_name      = """Topology 1""",
		port_handle        = [ixnHLT['PORT-HANDLE,//vport:<1>']],
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('topology_config', _result_)
	
	topology_1_handle = _result_['topology_handle']
	ixnHLT['HANDLE,//topology:<1>'] = topology_1_handle
	
	_result_ = ixiangpf.topology_config(
		topology_handle              = topology_1_handle,
		device_group_name            = """Basic L3-1""",
		device_group_multiplier      = "3",
		device_group_enabled         = "1",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('topology_config', _result_)
	
	deviceGroup_1_handle = _result_['device_group_handle']
	ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>'] = deviceGroup_1_handle
	
	_result_ = ixiangpf.interface_config(
		protocol_name                = """Ethernet 1""",
		protocol_handle              = deviceGroup_1_handle,
		mtu                          = "1500",
		src_mac_addr                 = "00.01.01.01.00.01",
		src_mac_addr_step            = "00.00.00.00.00.01",
		vlan                         = "0",
		vlan_id                      = '%s' % ("101"),
		vlan_id_step                 = '%s' % ("1"),
		vlan_id_count                = '%s' % ("1"),
		vlan_tpid                    = '%s' % ("0x8100"),
		vlan_user_priority           = '%s' % ("0"),
		vlan_user_priority_step      = '%s' % ("0"),
		use_vpn_parameters           = "0",
		site_id                      = "0",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	
	# n The attribute: useVlans with the value: False is not supported by scriptgen.
	# n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
	# n The attribute: connectedVia with the value: {} is not supported by scriptgen.
	# n Node: pbbEVpnParameter is not supported for scriptgen.
	ethernet_1_handle = _result_['ethernet_handle']
	ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>'] = ethernet_1_handle
	
	_result_ = ixiangpf.interface_config(
		protocol_name                     = """IPv4 1""",
		protocol_handle                   = ethernet_1_handle,
		ipv4_resolve_gateway              = "1",
		ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
		ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
		gateway                           = "1.1.1.4",
		gateway_step                      = "0.0.0.0",
		intf_ip_addr                      = "1.1.1.1",
		intf_ip_addr_step                 = "0.0.0.1",
		netmask                           = "255.255.255.0",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	
	# n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
	# n The attribute: connectedVia with the value: {} is not supported by scriptgen.
	ipv4_1_handle = _result_['ipv4_handle']
	ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'] = ipv4_1_handle
	
	_result_ = ixiangpf.topology_config(
		topology_name      = """Topology 2""",
		port_handle        = [ixnHLT['PORT-HANDLE,//vport:<2>']],
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('topology_config', _result_)
	
	topology_2_handle = _result_['topology_handle']
	ixnHLT['HANDLE,//topology:<2>'] = topology_2_handle
	
	_result_ = ixiangpf.topology_config(
		topology_handle              = topology_2_handle,
		device_group_name            = """Basic L3-2""",
		device_group_multiplier      = "3",
		device_group_enabled         = "1",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('topology_config', _result_)
	
	deviceGroup_2_handle = _result_['device_group_handle']
	ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>'] = deviceGroup_2_handle
	
	_result_ = ixiangpf.interface_config(
		protocol_name                = """Ethernet 2""",
		protocol_handle              = deviceGroup_2_handle,
		mtu                          = "1500",
		src_mac_addr                 = "00.01.01.02.00.01",
		src_mac_addr_step            = "00.00.00.00.00.01",
		vlan                         = "0",
		vlan_id                      = '%s' % ("101"),
		vlan_id_step                 = '%s' % ("1"),
		vlan_id_count                = '%s' % ("1"),
		vlan_tpid                    = '%s' % ("0x8100"),
		vlan_user_priority           = '%s' % ("0"),
		vlan_user_priority_step      = '%s' % ("0"),
		use_vpn_parameters           = "0",
		site_id                      = "0",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	
	# n The attribute: useVlans with the value: False is not supported by scriptgen.
	# n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
	# n The attribute: connectedVia with the value: {} is not supported by scriptgen.
	# n Node: pbbEVpnParameter is not supported for scriptgen.
	ethernet_2_handle = _result_['ethernet_handle']
	ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>'] = ethernet_2_handle
	
	_result_ = ixiangpf.interface_config(
		protocol_name                     = """IPv4 2""",
		protocol_handle                   = ethernet_2_handle,
		ipv4_resolve_gateway              = "1",
		ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
		ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
		gateway                           = "1.1.1.1",
		gateway_step                      = "0.0.0.0",
		intf_ip_addr                      = "1.1.1.4",
		intf_ip_addr_step                 = "0.0.0.1",
		netmask                           = "255.255.255.0",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	
	# n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
	# n The attribute: connectedVia with the value: {} is not supported by scriptgen.
	ipv4_2_handle = _result_['ipv4_handle']
	ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'] = ipv4_2_handle
	
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
	
	_result_ = ixiangpf.interface_config(
		protocol_handle                    = "/globals",
		arp_on_linkup                      = "0",
		single_arp_per_gateway             = "1",
		ipv4_send_arp_rate                 = "200",
		ipv4_send_arp_interval             = "1000",
		ipv4_send_arp_max_outstanding      = "400",
		ipv4_send_arp_scale_mode           = "port",
		ipv4_attempt_enabled               = "0",
		ipv4_attempt_rate                  = "200",
		ipv4_attempt_interval              = "1000",
		ipv4_attempt_scale_mode            = "port",
		ipv4_diconnect_enabled             = "0",
		ipv4_disconnect_rate               = "200",
		ipv4_disconnect_interval           = "1000",
		ipv4_disconnect_scale_mode         = "port",
		ipv4_re_send_arp_on_link_up        = "true",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	
	
	_result_ = ixiangpf.interface_config(
		protocol_handle                     = "/globals",
		ethernet_attempt_enabled            = "0",
		ethernet_attempt_rate               = "200",
		ethernet_attempt_interval           = "1000",
		ethernet_attempt_scale_mode         = "port",
		ethernet_diconnect_enabled          = "0",
		ethernet_disconnect_rate            = "200",
		ethernet_disconnect_interval        = "1000",
		ethernet_disconnect_scale_mode      = "port",
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('interface_config', _result_)
	
	
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


def ixnHLT_Scriptgen_RunTest(ixiahlt, ixnHLT):
	ixiatcl = ixiahlt.ixiatcl
	# #######################
	# start phase of the test
	# #######################
	ixnHLT_logger('Waiting 60 seconds before starting protocol(s) ...')
	time.sleep(60)
	
	ixnHLT_logger('Starting all protocol(s) ...')
	
	_result_ = ixiahlt.test_control(action='start_all_protocols')
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('ixiahlt::traffic_control', _result_)
	
	time.sleep(30)


					
	# 
	#  Reset traffic
	# 
	ixnHLT_logger('Resetting traffic...')
	_result_ = ixiahlt.traffic_control(
		action='reset',
		traffic_generator='ixnetwork_540',
		cpdp_convergence_enable='0',
		l1_rate_stats_enable ='1',
		misdirected_per_flow ='0',
		delay_variation_enable='0',
		packet_loss_duration_enable='0',
		latency_bins='enabled',
		latency_control='store_and_forward',
		instantaneous_stats_enable='0'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_control', _result_)
	#
	# Collect port_handles for traffic_stats
	#
	traffic_stats_ph = set()
	for (k, v) in ixnHLT.iteritems():
		if k.startswith('PORT-HANDLE,'):
			traffic_stats_ph.add(v)
					
	# 
	#  Configure traffic for all configuration elements
	# 
	#  -- Traffic item//traffic/trafficItem:<1>
	ixnHLT_logger('Configuring traffic for traffic item: //traffic/trafficItem:<1>')
	
	ti_srcs, ti_dsts = {}, {}
	ti_mcast_rcvr_handle, ti_mcast_rcvr_port_index, ti_mcast_rcvr_host_index, ti_mcast_rcvr_mcast_index = {}, {}, {}, {}
	
	ti_srcs['EndpointSet-1'] = ixnHLT_endpointMatch(ixnHLT, ['//topology:<1>'], 'HANDLE')
	if len(ti_srcs) == 0:
		match_err = {'log': 'Cannot find any src endpoints for EndpointSet-1'}
		ixnHLT_errorHandler('ixnHLT_endpointMatch', match_err)
	
	ti_dsts['EndpointSet-1'] = ixnHLT_endpointMatch(ixnHLT, ['//topology:<2>'], 'HANDLE')
	if len(ti_dsts) == 0:
		match_err = {'log': 'Cannot find any dst endpoints for elem EndpointSet-1'}
		ixnHLT_errorHandler('ixnHLT_endpointMatch', match_err)
	
	
	_result_ = ixiahlt.traffic_config(
		mode='create',
		traffic_generator='ixnetwork_540',
		endpointset_count=1,
		emulation_src_handle=[[ti_srcs['EndpointSet-1']]],
		emulation_dst_handle=[[ti_dsts['EndpointSet-1']]],
		emulation_multicast_dst_handle=[[]],
		emulation_multicast_dst_handle_type=[[]],
		global_dest_mac_retry_count='1',
		global_dest_mac_retry_delay='5',
		enable_data_integrity='1',
		global_enable_dest_mac_retry='1',
		global_enable_min_frame_size='0',
		global_enable_staggered_transmit='0',
		global_enable_stream_ordering='0',
		global_stream_control='continuous',
		global_stream_control_iterations='1',
		global_large_error_threshhold='2',
		global_enable_mac_change_on_fly='0',
		global_max_traffic_generation_queries='500',
		global_mpls_label_learning_timeout='30',
		global_refresh_learned_info_before_apply='0',
		global_use_tx_rx_sync='1',
		global_wait_time='1',
		global_display_mpls_current_label_value='0',
		global_detect_misdirected_packets='0',
		global_frame_ordering='none',
		frame_sequencing='disable',
		frame_sequencing_mode='rx_threshold',
		src_dest_mesh='one_to_one',
		route_mesh='one_to_one',
		bidirectional='0',
		allow_self_destined='0',
		use_cp_rate='1',
		use_cp_size='1',
		enable_dynamic_mpls_labels='0',
		hosts_per_net='1',
		name='TI0-Traffic_Item_1',
		source_filter='all',
		destination_filter='all',
		tag_filter=[[]],
		merge_destinations='1',
		circuit_endpoint_type='ipv4',
		pending_operations_timeout='30'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_config', _result_)
	
	#  -- All current config elements
	config_elements = ixiatcl.convert_tcl_list(_result_['traffic_item'])
	
	#  -- Config Element //traffic/trafficItem:<1>/configElement:<1>
	ixnHLT_logger('Configuring options for config elem: //traffic/trafficItem:<1>/configElement:<1>')
	_result_ = ixiahlt.traffic_config(
		mode='modify',
		traffic_generator='ixnetwork_540',
		stream_id=config_elements[0],
		preamble_size_mode='auto',
		preamble_custom_size='8',
		data_pattern='',
		data_pattern_mode='incr_byte',
		enforce_min_gap='0',
		rate_percent='100',
		frame_rate_distribution_port='split_evenly',
		frame_rate_distribution_stream='split_evenly',
		frame_size='256',
		length_mode='fixed',
		tx_mode='advanced',
		transmit_mode='single_burst',
		burst_loop_count='1',
		pkts_per_burst='50000',
		tx_delay='0',
		tx_delay_unit='bytes',
		number_of_packets_per_stream='50000',
		loop_count='1',
		min_gap_bytes='12'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_config', _result_)
	
	#  -- Endpoint set EndpointSet-1
	ixnHLT_logger('Configuring traffic for config elem: //traffic/trafficItem:<1>/configElement:<1>')
	ixnHLT_logger('Configuring traffic for endpoint set: EndpointSet-1')
	#  -- Stack //traffic/trafficItem:<1>/configElement:<1>/stack:"ethernet-1"
	_result_ = ixiahlt.traffic_config(
		mode='modify_or_insert',
		traffic_generator='ixnetwork_540',
		stream_id=config_elements[0],
		stack_index='1',
		l2_encap='ethernet_ii',
		mac_src_mode='fixed',
		mac_src_tracking='0',
		mac_src='00:00:00:00:00:00'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_config', _result_)
	
	#  -- Stack //traffic/trafficItem:<1>/configElement:<1>/stack:"ipv4-2"
	_result_ = ixiahlt.traffic_config(
		mode='modify_or_insert',
		traffic_generator='ixnetwork_540',
		stream_id=config_elements[0],
		stack_index='2',
		l3_protocol='ipv4',
		qos_type_ixn='tos',
		ip_precedence_mode='fixed',
		ip_precedence='0',
		ip_precedence_tracking='0',
		ip_delay_mode='fixed',
		ip_delay='0',
		ip_delay_tracking='0',
		ip_throughput_mode='fixed',
		ip_throughput='0',
		ip_throughput_tracking='0',
		ip_reliability_mode='fixed',
		ip_reliability='0',
		ip_reliability_tracking='0',
		ip_cost_mode='fixed',
		ip_cost='0',
		ip_cost_tracking='0',
		ip_cu_mode='fixed',
		ip_cu='0',
		ip_cu_tracking='0',
		ip_id_mode='fixed',
		ip_id='0',
		ip_id_tracking='0',
		ip_reserved_mode='fixed',
		ip_reserved='0',
		ip_reserved_tracking='0',
		ip_fragment_mode='fixed',
		ip_fragment='1',
		ip_fragment_tracking='0',
		ip_fragment_last_mode='fixed',
		ip_fragment_last='1',
		ip_fragment_last_tracking='0',
		ip_fragment_offset_mode='fixed',
		ip_fragment_offset='0',
		ip_fragment_offset_tracking='0',
		ip_ttl_mode='fixed',
		ip_ttl='64',
		ip_ttl_tracking='0',
		track_by='sourceDestValuePair0 flowGroup0 trackingenabled0',
		egress_tracking='none'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_config', _result_)
	
	#  -- Post Options
	ixnHLT_logger('Configuring post options for config elem: //traffic/trafficItem:<1>/configElement:<1>')
	_result_ = ixiahlt.traffic_config(
		mode='modify',
		traffic_generator='ixnetwork_540',
		stream_id=config_elements[0],
		transmit_distribution='none'	
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_config', _result_)
	# 
	# Configure traffic for Layer 4-7 AppLibrary Profile
	# 
	


	
	#
	# Start traffic configured earlier
	#
	ixnHLT_logger('Running Traffic...')
	_result_ = ixiahlt.traffic_control(
		action='run',
		traffic_generator='ixnetwork_540',
		type='l23'
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_control', _result_)
				  
	time.sleep(30)
	
	# ################################
	# protocol stats phase of the test
	# ################################
	
	#  stats for:
	#  packet_config_buffers handles
	ixnHLT_logger('getting stats for packet_config_buffers configuration elements')
	# ######################
	# stop phase of the test
	# ######################
	#
	# Stop traffic started earlier
	#
	ixnHLT_logger('Stopping Traffic...')
	_result_ = ixiahlt.traffic_control(
		action='stop',
		traffic_generator='ixnetwork_540',
		type='l23',
	)
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('traffic_control', _result_)
	
	# ###############################
	# traffic stats phase of the test
	# ###############################
	time.sleep(30)
				  
	#
	# print stats for all ports that are involved w/ 
	# ixnHLT(TRAFFIC-ENDPOINT-HANDLES)
	#
	ixnHLT_logger('Traffic stats')
	for traffic_stats_retry in range(120):
		_result_ = ixiahlt.traffic_stats(
			mode='aggregate',
			traffic_generator='ixnetwork_540',
			measure_mode='mixed'
		)
		if _result_['status'] != IxiaHlt.SUCCESS:
			ixnHLT_errorHandler('traffic_stats', _result_)
		
		if _result_['waiting_for_stats'] == '0':
			break
		
		ixnHLT_logger('Traffic waiting_for_stats flag is 1. Trial %d' % traffic_stats_retry)
		time.sleep(1)
				  
	if _result_['waiting_for_stats'] != '0':
		add_info = 'Traffic statistics are not ready after 120 seconds. waiting_for_stats is 1'
		raise IxiaError(IxiaError.COMMAND_FAIL, add_info)
				  
	for port_handle in traffic_stats_ph:
		ixnHLT_logger('')
		ixnHLT_logger('port %s' % port_handle)
		ixnHLT_logger('-----------------------------------')
	
		ixnHLT_logger('TX')
		for (k, v) in _result_[port_handle]['aggregate']['tx'].iteritems():
			ixnHLT_logger('{0:40s} = {1}'.format(k, v))
	
		ixnHLT_logger('RX')
		for (k, v) in _result_[port_handle]['aggregate']['rx'].iteritems():
			ixnHLT_logger('{0:40s} = {1}'.format(k, v))
	
		ixnHLT_logger('')
	
	ixnHLT_logger('Stopping all protocol(s) ...')
	
	_result_ = ixiahlt.test_control(action='stop_all_protocols')
	# Check status
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('ixiahlt::traffic_control', _result_)
					
# ----------------------------------------------------------------
# This dict keeps all generated handles and other info
ixnHLT = {}

# ----------------------------------------------------------------
#  chassis, card, port configuration
# 
#  port_list needs to match up with path_list below
# 
chassis = ['10.219.117.101']
tcl_server = '10.219.117.101'
port_list = [['1/1', '1/2']]
vport_name_list = [['1/1/1', '1/1/2']]
guard_rail = 'none'
# 
#  this should match up w/ your port_list above
# 
ixnHLT['path_list'] = [['//vport:<1>', '//vport:<2>']]
# 
# 
_result_ = ixiangpf.connect(
	reset=1,
	device=chassis,
	port_list=port_list,
	ixnetwork_tcl_server='localhost',
	tcl_server=tcl_server,
	guard_rail=guard_rail,
	return_detailed_handles=0
)
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('connect', _result_)
porthandles = []
for (ch, ch_ports, ch_vport_paths) in zip(chassis, port_list, ixnHLT['path_list']):
	ch_porthandles = []
	for (port, path) in zip(ch_ports, ch_vport_paths):
		try:
			ch_key = _result_['port_handle']
			for ch_p in ch.split('.'):
				ch_key = ch_key[ch_p]
			porthandle = ch_key[port]
		except:
			errdict = {'log': 'could not connect to chassis=%s,port=<%s>' % (ch, port)}
			ixnHLT_errorHandler('connect', errdict)

		ixnHLT['PORT-HANDLE,%s' % path] = porthandle
		ch_porthandles.append(porthandle)
	porthandles.append(ch_porthandles)

for (ch_porthandles, ch_vport_names) in zip(porthandles, vport_name_list):
	_result_ = ixiahlt.vport_info(
		mode='set_info',
		port_list=[ch_porthandles],
		port_name_list=[ch_vport_names]
	)
	if _result_['status'] != IxiaHlt.SUCCESS:
		ixnHLT_errorHandler('vport_info', _result_)
			

# ----------------------------------------------------------------

#call the procedure that configures legacy implementation
ixnHLT_Scriptgen_Configure(ixiahlt, ixnHLT)

#call the procedure that configures CPF
#this should be called after the call to legacy implementation
ixnCPF_Scriptgen_Configure(ixiangpf, ixnHLT)

ixnHLT_Scriptgen_RunTest(ixiahlt, ixnHLT)
