#!/usr/local/python2.7.6/bin/python2.7

# Written by: Hubert Gee
# Date: 1/4/17

# Description:
#
#    Assuming that you already created vChassis and vLoadModules Virtual
#    machines and you know the mgmt IP addresses to vChassis's and all the vLM.
#
#    This script will:
#       - Connect to the IxNetwork API Server.
#       - Connect to the vChassis IP.
#       - Rebuild chassis topology and discover all the load module appliances.
#       - Add IxVM card/port based on all the discovered appliances.
#       - Verify all the IxVM card and port status.
#
# Requirements:
#    
#    IxNetwork API Server
#    vChassis and vLM are reachable from the IxNetwork API Server (Windows Client).

import IxNetwork
import sys

ixNetworkTclServer = '192.168.70.127'
vChassisIp = '192.168.70.140'
ixNetworkVersion = '8.30'
ixNetworkPort = '8009'
vLoadModuleType = 'vmware' ;# vmware or qemu

if float(ixNetworkVersion) < 8.2:
    vLoadModuleLogin = 'root'
    vLoadModulePassword = 'root123'
if float(ixNetworkVersion) == 8.2:
    vLoadModuleLogin = 'ixia'
    vLoadModulePassword = 'H8WWQsqPqs2oNVIc'
if float(ixNetworkVersion) >= 8.3:
    vLoadModuleLogin = 'admin'
    vLoadModulePassword = 'admin'

def ConnectToServer(ixNet, ixNetworkTclServer, ixNetworkPort, ixNetworkVersion):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    connectStatus = ixNet.connect(ixNetworkTclServer, 'port', ixNetworkPort, '-version', ixNetworkVersion)
    if connectStatus != '::ixNet::OK':
        print '\nFailed to connect to IxNetwork Windows Client IP: %s\n' % ixNetworkTclServer
        return 1
    return 0

def AddIxiaChassisPy( ixChassisIp ):
    print '\nAdding chassis: ', ixChassisIp
    ixChassisObj = ixNet.add(ixNet.getRoot()+'availableHardware', 'chassis', '-hostname', ixChassisIp)
    ixNet.commit()

    #::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"
    ixChassisObj = ixNet.remapIds(ixChassisObj)[0]
    return ixChassisObj

def RemoveIxiaChassisPy( ixChassisIp ):
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    chassisList = ixNet.getList(availableHardware, 'chassis')
    for eachIxChassis in chassisList:
        currentChassisIp = ixNet.getAttribute(eachIxChassis, '-ip')
        if currentChassisIp == ixChassisIp:
            print 'RemoveIxiaChassisPy: ', eachIxChassis
            ixNet.remove(eachIxChassis)
            ixNet.commit()

def ReleaseAllPortsPy(ixNet):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    print '\nReleaseAllPortsPy'
    ixNet.execute('releaseAllPorts')

def IxVmConnectToVChassisPy(vChassisIp):
    # Besides connecting to ixNet, you must also connect to the 
    # virtual chassis to configure IxVM ports.

    ixvmChassisStatus = ixNet.execute('connectToChassis', vChassisIp)
    if ixvmChassisStatus != '::ixNet::OK':
        print '\nFailed to connect to virtual chassis IP: %s\n' % vChassisIp
        return 1
    else:
        return 0

def IxVmAddHypervisor(ixNet, vChassisIp, vLoadModuleLogin, vLoadModulePassword, vLoadModuleType):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    availableHardwareObj = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardwareObj, 'virtualChassis')[0]

    try:
        hypervisor = ixNet.add(vChassisObj, 'hypervisor')
        ixNet.setAttribute(hypervisor, '-enable', '%s' % 'true')
        ixNet.setAttribute(hypervisor, '-serverIp', '%s' % vChassisIp)
        ixNet.setAttribute(hypervisor, '-user', '%s' % vLoadModuleLogin)
        ixNet.setAttribute(hypervisor, '-password', '%s' % vLoadModulePassword)
        ixNet.setAttribute(hypervisor, '-type', '%s' % vLoadModuleType)
        ixNet.commit()
    except:
        #hypervisor = '::ixNet::OBJ-/availableHardware/virtualChassis/hypervisor:"192.168.70.10"'
        hypervisor = ixNet.getList(vChassisObj, 'hypervisor')[0]

    if len(hypervisor) != 0:
        print 'Hypervisor:', hypervisor
        return hypervisor
    else:
        return 0

def IxVmDiscoverAppliancesPy(ixNet):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    availableHardwareObj = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardwareObj, 'virtualChassis')[0]

    # Load Modules
    # ['::ixNet::OBJ-/availableHardware/virtualChassis/discoveredAppliance:"192.168.70.130"', 
    #   '::ixNet::OBJ-/availableHardware/virtualChassis/discoveredAppliance:"192.168.70.131"']
    discoveredApplianceList = ixNet.getList(vChassisObj, 'discoveredAppliance')
    for eachDiscoveredAppliance in discoveredApplianceList:
        print 'DiscoveredAppliances:', eachDiscoveredAppliance
    return discoveredApplianceList

def IxVmRemoveAllHypervisorsPy( ixNet ):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    hypervisorList = ixNet.getList(vChassisObj, 'hypervisor')

    for eachHypervisor in hypervisorList:
        print 'Removing hypervisor:', eachHypervisor
        ixNet.remove(eachHypervisor)
        ixNet.commit()

    hypervisorList = ixNet.getList(vChassisObj, 'hypervisor')
    if len(hypervisorList) == 0:
        print 'removeAllHypervisors: verified good'
        return 1
    else:
        print 'removeAllHypervisors: verified failed'
        return 0

def IxVmCreateVmCardsAndPortsPy(ixNet):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    # This API will go discover all created IxVM Load Modules and bring them up
    # as cards/ports for usage.
    # This API will assume that each virtual load module has one eth1 interface created
    # as test port.

    # This API requires calling APIs:
    #    - ixVmRediscoverAppliances()
    #    - ixVmDiscoverAppliances()

    # Returns an XML format of discovered load module management IP addresses
    rediscoverStatus = IxVmRediscoverAppliancesPy(ixNet)
    discoveredAppliances = IxVmDiscoverAppliancesPy(ixNet)

    availableHardwareObj = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardwareObj, 'virtualChassis')[0]

    cardNumber = 1
    for eachAppliance in discoveredAppliances:
        mgmtIp =ixNet.getAttribute(eachAppliance, '-managementIp')
        print 'Adding new ixVmCard %d/%s: %s' % (cardNumber, '1', eachAppliance)
        # ::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:L6
        ixVmCardObj = ixNet.add(vChassisObj, 'ixVmCard')

        ixNet.setMultiAttribute(ixVmCardObj, '-managementIp', mgmtIp, '-cardId', str(cardNumber))
        ixNet.commit()

        # ::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"/ixVmPort:L7
        ixVmPortObj = ixNet.add(ixVmCardObj, 'ixVmPort')
        ixNet.setMultiAttribute(ixVmPortObj,
                                '-portId', '1',
                                '-interface', 'eth1',
                                '-promiscuous', 'false',
                                '-mtu', '1500')
        ixNet.commit()
        cardNumber += 1

def IxVmRemoveCardIdPy(ixNet, vmCardId):
    # This API will remove the specified vm card ID.
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    import re
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    vmCardList = ixNet.getList(vChassisObj, 'ixVmCard')
    ReleaseAllPortsPy(ixNet)

    for eachVmCardId in vmCardList:
        # '::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"'
        currentCardIdMatch = re.match('::ixNet.*ixVmCard.*Card([0-9]+)', eachVmCardId)
        if currentCardIdMatch:
            if int(currentCardIdMatch.group(1)) == vmCardId:
                print '\nremoveCardId:', eachVmCardId
                ixNet.remove(eachVmCardId)
                ixNet.commit()
                return 0
    return 1

def IxVmRemoveAllCardsPy(ixNet):
    # This API will remove all vm cards.
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    vmCardList = ixNet.getList(vChassisObj, 'ixVmCard')
    ReleaseAllPortsPy(ixNet)

    for eachVmCardId in vmCardList:
        # '::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"'
        print '\nremoveCardId:', eachVmCardId
        ixNet.remove(eachVmCardId)
        ixNet.commit()

def IxVmRemovePortIdPy(ixNet, vmCardId, vmPortId):
    # This API will remove the specified vmCardId/vmPortId
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    # Example: ixNet = IxNetwork.IxNet() & ixNet.connect(apiServer)

    import re
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    vmCardList = ixNet.getList(vChassisObj, 'ixVmCard')

    for eachVmCardId in vmCardList:
        # '::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1"'
        currentCardIdMatch = re.match('::ixNet.*ixVmCard.*Card([0-9]+)', eachVmCardId)
        if currentCardIdMatch:
            if int(currentCardIdMatch.group(1)) == vmCardId:
                vmPortIdList = ixNet.getList(eachVmCardId, 'ixVmPort')

                for eachVmPortId in vmPortIdList:
                    currentPortIdMatch = re.match('::ixNet.*ixVmPort.*Port([0-9]+)', eachVmPortId)
                    if int(currentPortIdMatch.group(1)) == vmPortId:
                        print '\nremoveCardIdPortId: Removing:', eachVmPortId
                        ixNet.remove(eachVmPortId)
                        ixNet.commit()
                        return 0
    return 1

def IxVmRediscoverAppliancesPy(ixNet):
    # Returns an XML data:
    #    <ApplianceInfo>
    #    <ApplianceName>port1</ApplianceName>
    #    <ApplianceType>VMware</ApplianceType>
    #    <ManagementIP>192.168.70.130</ManagementIP>
    #    <RODiskVersion />
    #    <InterfaceName>eth0</InterfaceName>
    #    <State>Assigned</State>
    #    </ApplianceInfo>
    print '\nIxVmRediscoverAppliancesPy'
    return ixNet.execute('rediscoverAppliances')

def IxVmRefreshChassisTopologyPy(ixNet):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    ixNet.execute('ixVmRefreshChassisTopology')

def IxVmRemoveAllVmConfigPy(ixNet):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    IxVmRemoveAllCardsPy(ixNet)
    IxVmRemoveAllHypervisorsPy(ixNet)

def IxVmRebuildChassisTopologyPy(ixNet, ixNetworkVersion):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    print '\nRebuilding chassis topology ...'
    #rebuildChassisTopology (kString - ixnVersion ,kBool - usePrevSlotID ,kBool - promiscMode)
    ixNet.execute('rebuildChassisTopology', ixNetworkVersion, 'false', 'false')

def IxVmRebootVirtualChassis(ixNet, vChassisIp):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()
    # This API will reboot the virtual chassis and it will not return
    # until the virtual chassis comes back up.
    print '\nIxVmRebootVirtualChassis:', vChassisIp
    ixNet.execute('connectToChassis', vChassisIp)
    ixNet.execute('rebootVirtualChassis')

def IxVmChangeLicenseServer(ixNet, vChassisObj, licenseServerIp):
    print '\nIxVmChangeLicenseServer', licenseServerIp
    ixNet.setAttribute(vChassisObj, '-licenseServer', licenseServerIp)
    ixNet.commit()

def IxVmCheckCardStatus(ixNet):
    # ixNet = The IxNetwork connection object. For example: ixNet = IxNetwork.IxNet()

    # Checks all IxVM cards and its ports for cardOK and portOK.
    # If any card or port is not ok, return 1.
    # Returns 0 if all cards and ports are ok.

    import re, time
    ixNet.execute('refreshChassisTopology')
    availableHardware = ixNet.getList(ixNet.getRoot(), 'availableHardware')[0]
    vChassisObj = ixNet.getList(availableHardware, 'virtualChassis')[0]
    ixVmCardList = ixNet.getList(vChassisObj, 'ixVmCard')
    for card in ixVmCardList:
        print '\n',
        for counter in range(1,11):
            cardStatus = ixNet.getAttribute(card, '-cardState')
            # ::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card1 (VMware: port1)": cardOK
            cardIdMatch = re.match('::ixNet::OBJ.*(Card[0-9]+)', card)
            if cardIdMatch:
                print 'VM %s status: %s' % (cardIdMatch.group(1), cardStatus)
                if counter < 10 and cardStatus != 'cardOK':
                    print '\tWait %s/10 seconds' % counter
                    time.sleep(1)
                if counter < 10 and cardStatus == 'cardOK':
                    break
                if counter == 10 and cardStatus != 'cardOK':
                    return 1

        ixVmPortList = ixNet.getList(card, 'ixVmPort')
        for port in ixVmPortList:
            for counter in range(1,11):
                portStatus = ixNet.getAttribute(port, '-portState')
                # ::ixNet::OBJ-/availableHardware/virtualChassis/ixVmCard:"Card2 (VMware: port2)"/ixVmPort:"Port1": portOK
                portIdMatch = re.match('::ixNet::OBJ.*ixVmPort:\"(Port[0-9]+).*', port)
                if portIdMatch:
                    print '\t%s status: %s' % (portIdMatch.group(1), portStatus)
                    if counter < 10 and portStatus != 'portOK':
                        print '\t\tWait %s/10 seconds' % counter
                        time.sleep(1)
                    if counter < 10 and portStatus == 'portOK':
                        break
                    if counter == 10 and portStatus != 'portOK':
                        return 1
    # Return 0. All good.
    return 0

def SetLicenseUtility(**kwargs):
    for key,value in kwargs.items():
        print '%s: %s' % (key,value)

    print kwargs['tier']
    print kwargs['mode']

    '''
    argIndex = 0
    while argIndex < len(parameters):
        currentArg = parameters[argIndex]
        if currentArg == '-jobfile':
            self.jobFile = parameters[argIndex+1]
            argIndex+=2
        elif currentArg == '-resourcefile':
            self.globalResourceFile = parameters[argIndex+1]
            self.resourceFile = parameters[argIndex+1]
            self.globalResourceFile = True
            argIndex+=2                
    '''

    # ::ixNet::OBJ-/globals
    ixNetGlobals = ixNet.getList(ixNet.getRoot(), 'globals')[0]

    # ::ixNet::OBJ-/globals/licensing
    license = ixNet.getList(ixNetGlobals, 'licensing')[0]
    #Attributes:
    #        -licensingServers (readOnly=False, type=kArray[kString])
    #        -mode (readOnly=False, type=kEnumValue=mixed,perpetual,subscription)
    #        -tier (readOnly=False, type=kString) tier3, tier2, tier1 or tier0
    ixNet.setMultiAttribute(kwargs['ixNetObj'])



ixNet = IxNetwork.IxNet()

if ConnectToServer(ixNet, ixNetworkTclServer, ixNetworkPort, ixNetworkVersion) == 1:
    sys.exit()

# Remove all IxVM configurations first
IxVmRemoveAllVmConfigPy(ixNet)
RemoveIxiaChassisPy(vChassisIp)
#ixNet.disconnect()
#sys.exit()

#SetLicenseUtility(ixNetObj=ixNet, tier='2', mode='perpetual')
#sys.exit()

if IxVmConnectToVChassisPy(vChassisIp) == 1:
    sys.exit()

IxVmRebuildChassisTopologyPy(ixNet, ixNetworkVersion)

if IxVmAddHypervisor(ixNet, vChassisIp, vLoadModuleLogin, vLoadModulePassword, vLoadModuleType) == 0:
    sys.exit()

IxVmCreateVmCardsAndPortsPy(ixNet)
AddIxiaChassisPy(vChassisIp)

if IxVmCheckCardStatus(ixNet) == 1:
    print '\nIxVM Card/port failed to come up\n'
    sys.exit()

'''
# Miscellaneous APIs
IxVmRemovePortIdPy(ixNet, 2, 1)
IxVmRemoveCardIdPy(ixNet, 1)
IxVmRefreshChassisTopologyPy(ixNet)
IxVmDiscoverAppliancesPy(ixNet)
IxVmRebootVirtualChassis(ixNet, vChassisIp)
'''

ixNet.disconnect()
