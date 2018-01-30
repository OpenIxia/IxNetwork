from __future__ import absolute_import, print_function
import os, sys, time, traceback

from ixnetwork.IxnHttp import IxnHttp
from ixnetwork.IxnConfigManagement import IxnConfigManagement
from ixnetwork.IxnPortManagement import IxnPortManagement
from ixnetwork.IxnStatManagement import IxnStatManagement
from ixnetwork.IxnQuery import IxnQuery
from ixnetwork.IxnEmulationHosts import IxnIpv4Emulation, IxnBgpIpv4PeerEmulation

# Default connecting to windows:
#    Options: linux | windows | windowsConnectionMgr
api_server_type = 'windows'

# Accepting command line parameter: windows or linux
if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    api_server_type = sys.argv[1]

#------------ User Settings ------------#
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
    delete_session_when_done = True

enable_trace = True
release_ports_when_done = False
force_take_port_ownership = True
port_1_name = 'Port_1'
port_2_name = 'Port_2'
chassis_ip = '192.168.70.11'
port_list = [['Port_1', chassis_ip, '1', '1'],
             ['Port_2', chassis_ip, '2', '1']]

#-------------- User Settings End ----------------#

def release_ports(ixnhttp):
    query_vport = IxnQuery(ixnhttp, '/').node('vport', properties=['name']).go()
    for vport in query_vport.vport:
        vport_name = vport.attributes.name.value
        print('\nReleasing port name:', vport_name)
        print('\t', vport.href)
        vport.operations.releaseport({'arg1': [vport.href]})

try:
    # CONNECT TO API SERVER
    ixnhttp = IxnHttp(api_server_ip, api_server_rest_port)
    if enable_trace: ixnhttp.trace = True

    if api_server_type in ['windows', 'windowsConnectionMgr']:
        sessions = ixnhttp.sessions()
        ixnhttp.current_session = sessions[0]

    if api_server_type == 'linux':
        print('\nCreating new session on Linux API server:', api_server_ip)
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

    # CREATE A BLANK CONFIG
    config_mgmt = IxnConfigManagement(ixnhttp)
    config_mgmt.new_config()

    # CONNECT CHASSIS: 
    #     Query for the chassis IP to get the chassis state value.
    query_result = ixnhttp.root.query.node('availableHardware').go()
    query_result.availableHardware.create_chassis(payload={'hostname': chassis_ip})
    query_result = IxnQuery(ixnhttp, '/') \
        .node('availableHardware') \
        .node('chassis', properties=['state', 'ip'], where=[{'property': 'ip', 'regex':chassis_ip}])

    # WAIT FOR CHASSIS TO CONNECT
    timeout = 60
    start_time = int(time.time())
    while True:
        counter = int(time.time()) - start_time
        print('connect_chassis: {0} Connecting...'.format(chassis_ip))
        print('\tWaiting {0}/{1} seconds'.format(counter, timeout))
        query_chassis = query_result.go()
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
    #   Verify if ports are owned.  If not owned, ports are released and available.
    #                               If owned, ports are connected. You could verify port ownership.
    print('\nVerifying if ports are available for usage')
    if force_take_port_ownership is False:
        query_chassis = IxnQuery(ixnhttp, '/').node('availableHardware') \
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

    # CREATE VIRTUAL PORTS and ASSIGM PORTS
    port_mgmt = IxnPortManagement(ixnhttp)
    for port in port_list:
        # CREATE A VIRTUAL PORT FIRST
        ixnhttp.root.create_vport(count=1, payload={'name': port[0]})
        # Now map the physical port to the virtual port by the port name.
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

    # Get a list of all the configure vports for Topology Group configurations.
    query_vport = IxnQuery(ixnhttp, '/').node('vport').go()
    vport_list = [vport.href for vport in query_vport.vport]

    # CREATE TOPOLOGY GROUP 1 using port1
    topology_1 = ixnhttp.root.create_topology(payload={'name': 'Topo1'})
    topology_1.attributes.vports.value = [vport_list[0]]
    topology_1.attributes.name.value = 'BGP Topo1'
    topology_1.update()

    # CREATE DEVICE GROUP and SET MULTIPLIER
    device_group_1 = topology_1.create_deviceGroup()
    device_group_1.attributes.multiplier.value = '1'
    device_group_1.update()
  
    # CREATE ETHERNET STACK
    ethernet_1 = device_group_1.create_ethernet()

    # ENABLE VLAN
    ethernet_1.attributes.enableVlans.value.single_value = 'true'

    # CONFIGURE VLAN ID and PRIORITY
    vlan_1 = ethernet_1.query.node('vlan', properties=['vlanId', 'priority']).go().vlan[0]
    vlan_1.attributes.vlanId.value.single_value = '108'
    vlan_1.attributes.priority.value.single_value = '2'

    # CREATE IPV4
    ipv4_1 = ethernet_1.create_ipv4()
    ipv4_1.attributes.address.value.single_value = '1.1.1.1'
    ipv4_1.attributes.gatewayIp.value.single_value = '1.1.1.2'

    # CREATE BGP
    bgp_1 = ipv4_1.create_bgpIpv4Peer()
    bgp_1.attributes.holdTimer.value.single_value = '90'
    bgp_1.attributes.dutIp.value.single_value = '1.1.1.2'
    bgp_1.attributes.enableGracefulRestart.value.single_value = 'false'
    bgp_1.attributes.restartTime.value.single_value = '45'
    bgp_1.attributes.type.value.single_value = 'internal'
    bgp_1.attributes.enableBgpIdSameasRouterId.value.single_value = 'true'
    bgp_1.attributes.flap.value.value_list = ['true', 'true']
    bgp_1.attributes.uptimeInSec.value.single_value = '30'
    bgp_1.attributes.downtimeInSec.value.single_value = '10'

    # CREATE TOPOLOGY 2 Using port2
    topology_2 = ixnhttp.root.create_topology(payload={'name': 'Topo2'})
    topology_2.attributes.vports.value = [vport_list[1]]
    topology_2.attributes.name.value = 'BGP Topo2'
    topology_2.update()

    # CREATE DEVICE GROUP and SET MULTIPLIER
    device_group_2 = topology_2.create_deviceGroup()
    device_group_2.attributes.multiplier.value = '1'
    device_group_2.update()
  
    # CREATE ETHERNET STACK
    ethernet_2 = device_group_2.create_ethernet()

    # ENABLE VLAN
    ethernet_2.attributes.enableVlans.value.single_value = 'true'

    # CONFIGURE VLAN ID and PRIORITY
    vlan_2 = ethernet_2.query.node('vlan', properties=['vlanId', 'priority']).go().vlan[0]
    vlan_2.attributes.vlanId.value.single_value = '108'
    vlan_2.attributes.priority.value.single_value = '2'

    # CREATE IPV4
    ipv4_2 = ethernet_2.create_ipv4()
    ipv4_2.attributes.address.value.single_value = '1.1.1.2'
    ipv4_2.attributes.gatewayIp.value.single_value = '1.1.1.1'

    # CREATE BGP
    bgp_2 = ipv4_2.create_bgpIpv4Peer()
    bgp_2.attributes.holdTimer.value.single_value = '90'
    bgp_2.attributes.dutIp.value.single_value = '1.1.1.1'
    bgp_2.attributes.enableGracefulRestart.value.single_value = 'false'
    bgp_2.attributes.restartTime.value.single_value = '45'
    bgp_2.attributes.type.value.single_value = 'internal'
    bgp_2.attributes.enableBgpIdSameasRouterId.value.single_value = 'true'
    bgp_2.attributes.flap.value.value_list = ['false', 'false']
    bgp_2.attributes.uptimeInSec.value.single_value = '60'
    bgp_2.attributes.downtimeInSec.value.single_value = '20'

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

    # CREATE TRAFFIC ITEM
    #    1> Query for the traffic object
    # query_traffic = ixnhttp.root.query.node('traffic').go()
    #    2> Using traffic object to create a Traffic Item
    query_traffic = IxnQuery(ixnhttp, '/traffic').go()
    traffic_item_obj = query_traffic.create_trafficItem(payload={'name': 'Topo1 to Topo2',
                                                                    'trafficType': 'ipv4',
                                                                    'biDirectional': True,
                                                                    'srcDestMesh':' one-to-one',
                                                                    'routeMesh':' oneToOne',
                                                                    'allowSelfDestined': False})
    # 3> Add source and destination Endpoints
    #    QUERY FOR ALL CONFIGURED TOPOLOGY GROUPS 
    #        To use the topology groups as src/dst endpoints
    query_topology = IxnQuery(ixnhttp, '/').node('topology').go()
    topology_1_obj = query_topology.topology[0].href
    topology_2_obj = query_topology.topology[1].href
    endpoing_obj = traffic_item_obj.create_endpointSet(payload={'sources': [topology_1_obj],
                                                                'destinations': [topology_2_obj]})
    
    query_config_elements = IxnQuery(ixnhttp, '/traffic') \
        .node('trafficItem', properties=['name'], where=[{'property': 'name', 'regex': 'Topo1 to Topo2'}]) \
        .node('tracking', properties=['trackBy']) \
        .node('configElement') \
        .node('frameSize', properties=['type', 'fixedSize']) \
        .node('frameRate', properties=['type', 'rate']) \
        .node('transmissionControl', properties=['type', 'frameCount']) \
        .go()

    frame_size = query_config_elements.trafficItem[0].configElement[0].frameSize
    frame_size.attributes.type.value = 'fixed'
    frame_size.attributes.fixedSize.value = '127'
    frame_size.update()

    frame_rate = query_config_elements.trafficItem[0].configElement[0].frameRate
    frame_rate.attributes.type.value = 'percentLineRate'
    frame_rate.attributes.rate.value = '25'
    frame_rate.update()

    frame_count = query_config_elements.trafficItem[0].configElement[0].transmissionControl
    frame_count.attributes.type.value = 'fixedFrameCount'
    frame_count.attributes.frameCount.value = '28000'
    frame_count.update()

    track_by = query_config_elements.trafficItem[0].tracking[0]
    track_by.attributes.trackBy.value = ['flowGroup0']
    track_by.update()
    
    # REGENERATE:  All Traffic Items
    query_traffic = IxnQuery(ixnhttp, '/traffic').node('trafficItem', properties=['name']).go()
    for each_traffic_item in query_traffic.trafficItem:
        print('\nRegenerating Traffic Item:', each_traffic_item.attributes.name.value)
        # arg1: /api/v1/sessions/1/ixnetwork/traffic/trafficItem/1
        each_traffic_item.operations.generate({'arg1': each_traffic_item.href})
  
    # APPLY TRAFFIC
    print('\nApplying traffic')
    # arg1: /api/v1/sessions/1/ixnetwork/traffic
    query_traffic.operations.apply({'arg1': query_traffic.href})

    # START TRAFFIC
    print('\nStarting traffic')
    # arg1: /api/v1/sessions/1/ixnetwork/traffic
    query_traffic.operations.start({'arg1': query_traffic.href})

    # CHECK TRAFFIC STATE:  
    #   To ensure traffic stats are shown before checking statistics.
    #   Options: started | stopped | startedWaitingForStats | stoppedWaitingForStats
    #       For continuous traffic, set expected_state=['started', 'startedWaitingForStats']
    #       For fixed frame count, set expected_state=['stopped', 'stoppedWaitingForStats']
    expected_state = ['stopped', 'stoppedWaitingForStats']
    start_time = int(time.time())
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
    time.sleep(5)

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
        tx_frames = flow_stats_row[4]
        rx_frames = flow_stats_row[5]
        frames_delta = flow_stats_row[6]
        if tx_frames != rx_frames:
            print('Failed: Frame loss delta:', frames_delta)
        else:
            print('TxPort:{0} RxPort:{1} TxFrames:{2} RxFrames:{3} = No loss'.format(
                    tx_port, rx_port, tx_frames, rx_frames))
    print()
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
