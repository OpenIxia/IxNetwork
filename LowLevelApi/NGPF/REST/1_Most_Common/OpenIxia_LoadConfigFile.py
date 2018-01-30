
"""Load a saved BGP config file.
    - Using two back-2-back Ixia ports to test this script
    - Connect to chassis
    - Verify if ports are available
    - Reassign ports (If needed)
    - Verify port state
    - Start all protocols
    - Verify protocol sessions
    - Start traffic
    - Modify BGP configs
    - Modify Traffic
    - Get statistics

- Allows you to remap physical ports so the config file works on any testbed.
- Supports Windows API server and Linux API server.
- CLI input:
        python LoadConfigFile.py windows  (To connect to Windows API server)
        python LoadConfigFile.py linux    (To connect to Linux API server)
"""

from __future__ import absolute_import, print_function
import os, sys, time, traceback

# Get these modules from http://github.com/openixia/ixnetwork_client_python
# or do a pip install ixnetwork
from ixnetwork.IxnHttp import IxnHttp
from ixnetwork.IxnConfigManagement import IxnConfigManagement
from ixnetwork.IxnPortManagement import IxnPortManagement
from ixnetwork.IxnStatManagement import IxnStatManagement
from ixnetwork.IxnQuery import IxnQuery
from ixnetwork.IxnEmulationHosts import IxnIpv4Emulation, IxnBgpIpv4PeerEmulation

# Default connecting to windows:
#    Options: linux | windows | windowsConnectionMgr
api_server_type = 'windows'

# Accepting command line parameter: windows, windowsConnectionMgr or linux
if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    api_server_type = sys.argv[1]

#------------ User Preferences ------------#
if api_server_type == 'windows':
    api_server_ip = '192.168.70.127'
    api_server_rest_port = 11009

if api_server_type == 'linux':
    api_server_ip = '192.168.70.144'
    api_server_rest_port = 443
    username = 'admin'
    password = 'admin'
    license_server_ip = '192.168.70.127'
    license_mode = 'subscription'
    license_tier = 'tier3'
    delete_session_when_done = False

enable_trace = True
config_file = '/home/hgee/Dropbox/MyIxiaWork/Temp/bgp_ngpf_8.30.ixncfg'

release_ports_when_done = False
force_take_port_ownership = True
port_1_name = 'Port_1'

# REMAP CHASSIS/PORTS.
#     Comment this out if you want to use the saved config chassis/ports.
chassis_ip = '10.219.116.72'
port_list = [['Port_1', chassis_ip, '1', '1'],
             ['Port_2', chassis_ip, '1', '2']]

#-------------- User Preferences Ends ----------------#

def release_ports(ixnhttp):
    query_vport = IxnQuery(ixnhttp, '/').node('vport', properties=['name']).go()
    for vport in query_vport.vport:
        vport_name = vport.attributes.name.value
        print('\nReleasing port name:', vport_name)
        print('\t', vport.href)
        vport.operations.releaseport({'arg1': [vport.href]})

try:
    if api_server_type in ['windows', 'windowsConnectionMgr']:
        ixnhttp = IxnHttp(api_server_ip, api_server_rest_port, secure=False)
        sessions = ixnhttp.sessions()
        ixnhttp.current_session = sessions[0]

    if api_server_type == 'linux':
        ixnhttp = IxnHttp(api_server_ip, api_server_rest_port, secure=True)
        ixnhttp.auth(username, password)
        ixnhttp.create_session()

        # CONFIG LICENSE SERVER
        #    New session needs to know where the license server is located.
        query_license = IxnQuery(ixnhttp, '/') \
            .node('globals') \
            .node('licensing', properties=['licensingServers', 'tier', 'mode']) \
            .go()
        print('\nConfigure license server:', license_server_ip, license_mode, license_tier)
        query_license.globals.licensing.attributes.licensingServers.value = [license_server_ip]
        query_license.globals.licensing.attributes.mode.value = license_mode
        query_license.globals.licensing.attributes.tier.value = license_tier
        query_license.globals.licensing.update()

    if enable_trace: ixnhttp.trace = True

    # LOAD CONFIG FILE
    config_mgmt = IxnConfigManagement(ixnhttp)
    if os.path.exists(config_file) is False:
        raise Exception('Error: No such config file found: {0}'.format(config_file))
    print('\nloading config file:', config_file)
    config_mgmt.load_config(config_file, upload=True)

    # CONNECT CHASSIS:
    if 'port_list' in locals():
        # If user includes port_list for reassigning ports, then connect to user defined chassis_ip.
        query_result = ixnhttp.root.query.node('availableHardware').go()
        query_result.availableHardware.create_chassis(payload={'hostname': chassis_ip})
    else:
        # Get the saved config's chassis IP address.
        query_result = IxnQuery(ixnhttp, '/') \
            .node('availableHardware') \
            .node('chassis', properties=['ip']).go()
        chassis_ip = query_result.availableHardware.chassis[0].attributes.ip.value

    # WAIT FOR CHASSIS TO CONNECT
    query_chassis_ip = IxnQuery(ixnhttp, '/') \
    .node('availableHardware') \
    .node('chassis', properties=['state', 'ip'], where=[{'property': 'ip', 'regex':chassis_ip}])

    timeout = 60
    start_time = int(time.time())
    while True:
        counter = int(time.time()) - start_time
        print('connect_chassis: {0} Connecting...'.format(chassis_ip))
        print('\tWaiting {0}/{1} seconds'.format(counter, timeout))
        query_chassis = query_chassis_ip.go()
        if query_chassis.availableHardware.chassis == []:
            time.sleep(1)
            continue
        current_status = query_chassis.availableHardware.chassis[0].attributes.state.value
        print('\tStatus: {0}'.format(current_status))
        if current_status != 'ready' and counter < timeout:
            time.sleep(1)
        if current_status != 'ready' and counter == timeout:
            raise Exception('connect_chassis: {0} failed'.format(chassis_ip))
        if current_status == 'ready' and counter < timeout:
            break

    # ARE PORTS AVAILABLE?
    print('\nVerifying if ports are available for usage')
    # Check for port ownership
    if 'port_list' in locals() and force_take_port_ownership is False:
        query_chassis = IxnQuery(ixnhttp, '/') \
        .node('availableHardware') \
        .node('chassis', properties=['ip'], where=[{'property': 'ip', 'regex': chassis_ip}]) \
        .node('card', properties=['cardId']) \
        .node('port', properties=['portId', 'owner']) \
        .go()

        print()
        is_port_owned = False
        for each_card in query_chassis.availableHardware.chassis[0].card:
            card_id = each_card.attributes.cardId.value
            port_id = each_card.port[0].attributes.portId.value
            port_owner = each_card.port[0].attributes.owner.value
            # Verify against user defined ports
            for port in port_list:
                defined_card_id = int(port[2])
                defined_port_id = int(port[3])
                if card_id == defined_card_id and port_id == defined_port_id:
                    if port_owner != '':
                        is_port_owned = True
                    if port_owner == '':
                        port_owner = 'PortIsReleased/Available'
                    print('\t{0}:{1}:{2} Owner: {3}'.format(chassis_ip, card_id, port_id, port_owner))
        if is_port_owned:
            raise Exception('force_take_port_ownership = False. Ports are not avialable for usage.')

    # REMAP PORTS
    #     Only remap ports if user included port_list. Otherwise, use the ports in the saved config file.
    if 'port_list' in locals():
        port_mgmt = IxnPortManagement(ixnhttp)
        for port in port_list:
            # port_mgmt.map(port_name, chassis_ip, card_id, port_id)
            port_mgmt.map(port[0], port[1], port[2], port[3])
        port_mgmt.apply()

    # VERIFY PORT STATE
    start = int(time.time())
    # Get the total number of vports
    query_vport = IxnQuery(ixnhttp, '/').node('vport', properties=['assignedTo']).go()
    vport_count = len(query_vport.vport)
    # Setup the port state query
    port_state_query = IxnQuery(ixnhttp, '/').node('vport',
        properties=['state', 'assignedTo'],
        where=[{'property':'state', 'regex':'up'}])
    timeout = 90
    while True:
        # Execute the state query
        query_port = port_state_query.go()
        counter = int(time.time()) - start
        # Show the current vport status
        print('\nVerify port state')
        try:
            for index in range(0,vport_count):
                if query_port.vport[index]:
                    state = query_port.vport[index].attributes.state.value
                    assignedTo = query_port.vport[index].attributes.assignedTo.value
                    print('\t{0} is {1}'.format(assignedTo, state))
        except:
            # Get the down state ports
            down_state_query = IxnQuery(ixnhttp, '/').node('vport',
                properties=['state', 'assignedTo'],
                where=[{'property':'state', 'regex':'down'}]) \
                .go()
            for x in range(0,len(down_state_query.vport)):
                print('\t{0} is down'.format(down_state_query.vport[x].attributes.assignedTo.value))

        print('\tWaiting %s/%s seconds' % (counter, timeout))
        # If the state_query on any vport object is 'up', the vport will get listed.
        if len(query_port.vport) == vport_count:
            break
        if int(time.time()) - start > timeout:
            raise Exception('%s vport objects did not reach state ip in %s seconds' % (vport_count, timeout))
        time.sleep(1)
    time.sleep(5)

    # EXAMPLE: MODIFY BGP PROPERTIES
    query_bgp = IxnQuery(ixnhttp, '/') \
        .node('topology', properties=['name'], where=[{'property': 'name', 'regex': 'Topo1'}]) \
        .node('deviceGroup') \
        .node('ethernet') \
        .node('ipv4') \
        .node('bgpIpv4Peer', properties=['flap']) \
        .go()

    bgp_host = query_bgp.topology[0].deviceGroup[0].ethernet[0].ipv4[0].bgpIpv4Peer[0]
    bgp_host_flap = bgp_host.attributes.flap
    bgp_host_flap.value.value_list = ['false', 'false']
    bgp_host_flap.value.dump()

    # START ALL PROTOCOLS
    ixnhttp.root.operations.startallprotocols()

    print('\nVerify IPv4 ARP')
    ipv4 = IxnIpv4Emulation(ixnhttp)
    ipv4.find(vport_name=port_1_name)
    ipv4.wait_until(IxnIpv4Emulation.STATE_UP, timeout=60)

    print('\nVerify BGP protocol sessions')
    bgp = IxnBgpIpv4PeerEmulation(ixnhttp)
    bgp.find(vport_name=port_1_name)
    bgp.wait_until(IxnBgpIpv4PeerEmulation.STATE_UP, timeout=90)

    # EXAMPLE: MODIFY TRAFFIC ITEM
    #     Get Traffic Item properties that you want to modify.
    query_traffic_item = IxnQuery(ixnhttp, '/') \
        .node('traffic') \
        .node('trafficItem', properties=['name'], where=[{'property': 'name', 'regex': 'Topo1 to Topo2'}]) \
        .node('configElement') \
        .node('frameRate', properties=['type', 'rate']) \
        .node('frameSize', properties=['fixedSize']) \
        .node('transmissionControl', properties=['type', 'frameCount']) \
        .go()

    frame_rate = query_traffic_item.traffic.trafficItem[0].configElement[0].frameRate
    frame_rate.attributes.type.value = 'percentLineRate'
    frame_rate.attributes.rate.value = '25'
    frame_rate.update()

    frame_size = query_traffic_item.traffic.trafficItem[0].configElement[0].frameSize
    frame_size.attributes.fixedSize.value = '256'
    frame_size.update()

    transmission_control = query_traffic_item.traffic.trafficItem[0].configElement[0].transmissionControl
    # transmissionControl options: continuous | auto | custom | fixedDuration | fixedFrameCount | fixedIterationCount
    transmission_control.attributes.type.value = 'fixedFrameCount'
    transmission_control.attributes.frameCount.value = '20000'
    transmission_control.update()

    # REGENERATE:  All Traffic Items
    for each_traffic_item in query_traffic_item.traffic.trafficItem:
        print('\nRegenerating Traffic Item:', each_traffic_item.attributes.name.value)
        # arg1: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1
        each_traffic_item.operations.generate({'arg1': each_traffic_item.href})

    # APPLY TRAFFIC
    print('\nApplying traffic')
    # arg1: /api/v1/sessions/1/ixnetwork/traffic
    query_traffic_item.traffic.operations.apply({'arg1': query_traffic_item.traffic.href})

    # START TRAFFIC
    print('\nStarting traffic')
    # arg1: /api/v1/sessions/1/ixnetwork/traffic
    query_traffic_item.traffic.operations.start({'arg1': query_traffic_item.traffic.href})

    # CHECK TRAFFIC STATE:
    #   To ensure traffic stats are shown before checking statistics.
    #   Options: started | stopped | startedWaitingForStats | stoppedWaitingForStats
    #       For CONTINUOUS traffic, set expected_state=['started', 'startedWaitingForStats']
    #       For FIXED frame count, set expected_state=['stopped', 'stoppedWaitingForStats']
    expected_state = ['started', 'startedWaitingForStats']
    start_time = int(time.time())
    timeout = 25
    print('\nExpecting traffic state:', expected_state)
    while True:
        query_traffic = IxnQuery(ixnhttp, '/').node('traffic', properties=['state']).go()
        current_traffic_state = query_traffic.traffic.attributes.state.value
        counter = int(time.time()) - start_time
        print('\ncheck_traffic_state:\n\tCurrent state: {traffic_state}\n\tExpecting state: {expecting}\n\tWaiting {counter}/{timeout} seconds'.format(
            traffic_state=current_traffic_state,
            expecting = expected_state,
            counter=counter,
            timeout=timeout))
        if counter < timeout and current_traffic_state not in expected_state:
            time.sleep(1)
            continue
        if counter < timeout and current_traffic_state in expected_state:
            break
        if counter == timeout and current_traffic_state not in expected_state:
            raise Exception('check_traffic_state: Traffic state did not reach the expected state(s):', expected_state)

    # GET AND PRINT STATISTICS
    stat_mgmt = IxnStatManagement(ixnhttp)
    views = stat_mgmt.get_views()
    print()

    flow_statistics_page = stat_mgmt.get_view_page('Flow Statistics')
    stat_mgmt.print_view_page(flow_statistics_page, column_captions=[
        'Tx Port', 'Rx Port', 'Tx Frames', 'Rx Frames', 'Frames Delta'])
    print()
    # flow_statistics_page is a list containing:
    #    1tem #1:     Statistic column names
    #    item #2-end: Statistics corresponding to the column names
    for flow_stats_row in flow_statistics_page[1:]:
        tx_port = flow_stats_row[0]
        rx_port = flow_stats_row[1]
        vlan = flow_stats_row[3]
        tx_frames = flow_stats_row[5]
        rx_frames = flow_stats_row[6]
        frames_delta = flow_stats_row[7]
        if tx_frames != rx_frames:
            print('Failed: Frame loss delta:', frames_delta)
        else:
            print('TxPort:{0} RxPort:{1} TxFrames:{2} RxFrames:{3} = No loss'.format(
                    tx_port, rx_port, tx_frames, rx_frames))
    print()
    stat_mgmt = IxnStatManagement(ixnhttp)
    views = stat_mgmt.get_views()
    print()

    flow_statistics_page = stat_mgmt.get_view_page('Flow Statistics')
    stat_mgmt.print_view_page(flow_statistics_page, column_captions=[
        'Tx Port', 'Rx Port', 'Tx Frames', 'Rx Frames', 'Frames Delta'])
    print()
    # flow_statistics_page is a list containing:
    #    1tem #1:     Statistic column names
    #

    traffic_item_page = stat_mgmt.get_view_page('Traffic Item Statistics')
    stat_mgmt.print_view_page(traffic_item_page, column_captions=[
        'Traffic Item', 'Tx Frames', 'Rx Frames', 'Frames Delta', 'loss %'])

    print()
    protocols_summary_page = stat_mgmt.get_view_page('Protocols Summary')
    stat_mgmt.print_view_page(protocols_summary_page, column_captions=[
        'Protocol Type', 'Sessions Total', 'Sessions Up', 'Sessions Down', 'Sessions Not Started'])

    if release_ports_when_done:
        release_ports(ixnhttp)

    if api_server_type == 'linux':
        ixnhttp.delete_session()

    if api_server_type == 'windowsConnectionMgr':
        ixnhttp.delete_session()

except (KeyboardInterrupt, Exception) as err_msg:
    if enable_trace:
        print('\n%s' % traceback.format_exc())
    print('\nIxNetException_Error:', err_msg)

    if release_ports_when_done:
        release_ports(ixnhttp)

    if api_server_type in ['linux', 'windowsConnectionMgr'] and delete_session_when_done:
        print('\nDeleteing session...')
        ixnhttp.delete_session()
