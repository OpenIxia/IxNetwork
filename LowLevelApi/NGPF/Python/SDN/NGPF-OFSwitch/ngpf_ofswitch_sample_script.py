# -*- coding: cp1252 -*-
#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    05/02/2016 - Sarabjeet Kaur - created sample                              #
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
#    This script intends to demonstrate how to use NGPF OpenFlow Controller API#
#    It will create 1 topology of OpenFlow Controller, it will start the 
#    emulation and then it will retrieve and display few statistics 
#    It will also check detailed learned info and learned info after sending on#
#    demand message                                                            #
# Ixia Software:                                                               #
#    IxOS      8.200 EA                                                         #
#    IxNetwork 8.20 EA                                                         #
#                                                                              #
################################################################################
import sys
import time

################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the  #
# IxNetwork.py file somewhere else where we python can autoload it             #
# "IxNetwork.py" is available in <IxNetwork_installer_path>\API\Python         #
################################################################################
sys.path.append('C:\Program Files (x86)\Ixia\IxNetwork\8.10-EA\API\Python')
import IxNetwork
print("loaded successfully")

#from lib import IxNetwork
#import time

class NgpfOpenFlowSwitch(object):
    ################################################################################
    # Connecting to IxTCl server and cretaing new config                           #
    ################################################################################
    def __init__(self, ix_tcl_server, ix_tcl_port, ix_version="8.10"):
        ixNet = IxNetwork.IxNet()
        print("connecting to IxNetwork client")
        ixNet.connect(ix_tcl_server, '-port', ix_tcl_port, '-version', ix_version,
                      '-setAttribute', 'strict')

        # cleaning up the old configfile, and creating an empty config
        print("cleaning up the old configfile, and creating an empty config")
        ixNet.execute('newConfig')
        self.ixNet = ixNet
        self.root = ixNet.getRoot()

    def assignPorts(self, realPort1):
        chassis1 = realPort1[0]
        card1 = realPort1[1]
        port1 = realPort1[2]
        root = self.ixNet.getRoot()
        vport1 = self.ixNet.add(root, 'vport')
        self.ixNet.commit()
        vport1 = self.ixNet.remapIds(vport1)[0]
        chassisObj1 = self.ixNet.add(root + '/availableHardware', 'chassis')
        self.ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
        self.ixNet.commit()
        chassisObj1 = self.ixNet.remapIds(chassisObj1)[0]

        cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1, port1)
        self.ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
                                     '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
        self.ixNet.commit()

        ################################################################################
        # Start protocol and check statistics                                          #
        ################################################################################
    def start_protocol_check_stats(self):

        print("Starting protocols and waiting for 45 seconds for protocols to come up")
        self.ixNet.execute('startAllProtocols')
        time.sleep(45)
        print ("Fetching all Protocol Summary Stats\n")
        viewPage = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
        statcap = self.ixNet.getAttribute(viewPage, '-columnCaptions')
        for statValList in self.ixNet.getAttribute(viewPage, '-rowValues'):
            for statVal in statValList:
                print("***************************************************")
                index = 0
                for satIndv in statVal:
                    print("%-30s:%s" % (statcap[index], satIndv))
                    index = index + 1
        print("***************************************************")

        print ("Verifying OpenFlow Switch Per Port stats\n")
        viewPage = '::ixNet::OBJ-/statistics/view:"OF Switch Per Port"/page'
        statcap = self.ixNet.getAttribute(viewPage, '-columnCaptions')
        for statValList in self.ixNet.getAttribute(viewPage, '-rowValues'):
            for statVal in statValList:
                print("***************************************************")
                index = 0
                for satIndv in statVal:
                    print("%-30s:%s" % (statcap[index], satIndv))
                    index = index + 1
        print("***************************************************")

    def on_the_fly(self, switch_disable_enable):
        for i in switch_disable_enable:
            ofSwitchActive = self.ixNet.getAttribute(switch_disable_enable, '-active')
            swActive = self.ixNet.add(ofSwitchActive, 'overlay')
            self.ixNet.setMultiAttribute(swActive, '-value', 'false')
            self.ixNet.commit()
        globalObj = self.ixNet.getRoot() + '/globals'
        topology = globalObj + '/topology'
        print ("Applying changes on the fly")
        try:
            self.ixNet.execute('applyOnTheFly', topology)
        except:
            print("error in applying on the fly change")
        time.sleep(10)
        
        for i in switch_disable_enable:
            ofSwitchActive = self.ixNet.getAttribute(switch_disable_enable, '-active')
            swActive = self.ixNet.add(ofSwitchActive, 'overlay')
            self.ixNet.setMultiAttribute(swActive, '-value', 'true')
            self.ixNet.commit()
        globalObj = self.ixNet.getRoot() + '/globals'
        topology = globalObj + '/topology'
        print ("Applying changes on the fly")
        try:
            self.ixNet.execute('applyOnTheFly', topology)
        except:
            print("error in applying on the fly change")
        time.sleep(10)
    def on_the_fly_port_number_ethernetaddress(self, sw_port):
        EthernetDestVal = self.ixNet.getAttribute(sw_port, '-etherAddr')
        print EthernetDestVal
        val = self.ixNet.getAttribute(EthernetDestVal, '-values')[0]
        print val
        self.ixNet.setMultiAttribute(EthernetDestVal, '-clearOverlays', 'false')
        self.ixNet.commit()
        EthernetDestValues = self.ixNet.add(EthernetDestVal, 'singleValue')
        self.ixNet.setMultiAttribute(EthernetDestValues, '-value', '56:00:00:00:00:1')
        self.ixNet.commit()
        time.sleep(20)
        PortVal = self.ixNet.getAttribute(sw_port, '-portNumber')
        self.ixNet.setMultiAttribute(PortVal, '-clearOverlays', 'false')
        self.ixNet.commit()
        PortSetValues = self.ixNet.add(PortVal, 'singleValue')
        self.ixNet.setMultiAttribute(PortSetValues, '-value', '5677888')
        self.ixNet.commit()
        globalObj = self.ixNet.getRoot() + '/globals'
        topology = globalObj + '/topology'
        print ("Applying changes on the fly")
        try:
            self.ixNet.execute('applyOnTheFly', topology)
        except:
            print("error in applying on the fly change")
        time.sleep(10)

    ###############################################################################
    # print learned info                                                          #
    ###############################################################################
    def print_learned_info(self, openFlowSwitch):
        self.ixNet.execute('getOFChannelLearnedInfo', openFlowSwitch, '1')
        time.sleep(5)
        print("Print OFSwitch Learned Info")
        linfo = self.ixNet.getList(openFlowSwitch, 'learnedInfo')[0]
        linfoList = self.ixNet.getList(linfo, 'table')
        print("***************************************************")
        for table in linfoList:
            tableType = self.ixNet.getAttribute(table, '-type')
            print(tableType)
            print("=================================================")
            columns = self.ixNet.getAttribute(table, '-columns')
            print(columns)
            values = self.ixNet.getAttribute(table, '-values')
            for value in values:
                for word in values:
                    print(word)
        time.sleep(15)
        self.ixNet.execute('getOFSwitchFlowStatLearnedInfo', openFlowSwitch, '1')
        time.sleep(5)
        print ("Print OFswitch Flow Learned info")
        linfo = self.ixNet.getList(openFlowSwitch, 'learnedInfo')[0]
        linfoList = self.ixNet.getList(linfo, 'table')
        print("***************************************************")
        for table in linfoList:
            tableType = self.ixNet.getAttribute(table, '-type')
            print(tableType)
            print("=================================================")
            columns = self.ixNet.getAttribute(table, '-columns')
            print(columns)
            values = self.ixNet.getAttribute(table, '-values')
            for value in values:
                for word in values:
                    print(word)
        time.sleep(15)
        print ('Stopping protocols')
        self.ixNet.execute('stopAllProtocols')

    ################################################################################
    # protocol configuration section                                               #
    ################################################################################
    def main(self):
        self.assignPorts(ports[0])
        root = self.ixNet.getRoot()
        vportTx = self.ixNet.getList(root, 'vport')[0]

        print("adding topologies")
        self.ixNet.add(root, 'topology', '-vports', vportTx)
        self.ixNet.commit()
        topologies = self.ixNet.getList(self.ixNet.getRoot(), 'topology')
        topo1 = topologies[0]

        print "Adding 2 device groups"
        deviceGroup1 = self.ixNet.add(topo1, 'deviceGroup')
        self.ixNet.commit()
        t1devices = self.ixNet.getList(topo1, 'deviceGroup')
        t1dev1 = t1devices[0]

        print("Configuring the multipliers (number of sessions)")
        self.ixNet.setAttribute(t1dev1, '-multiplier', '1')
        self.ixNet.commit()

        print("Adding ethernet/mac endpoints")
        self.ixNet.add(t1dev1, 'ethernet')
        self.ixNet.commit()

        mac1 = self.ixNet.getList(t1dev1, 'ethernet')[0]
        print ('ixNet.help(\'::ixNet::OBJ-/topology/deviceGroup/ethernet\')')

        print("Add ipv4")
        self.ixNet.add(mac1, 'ipv4')
        self.ixNet.commit()

        ip1 = self.ixNet.getList(mac1, 'ipv4')[0]
        mvAdd1 = self.ixNet.getAttribute(ip1, '-address')
        mvGw1 = self.ixNet.getAttribute(ip1, '-gatewayIp')

        print("configuring ipv4 addresses")
        self.ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '1.1.1.2')
        self.ixNet.commit()
        self.ixNet.setAttribute(mvGw1 + '/singleValue', '-value', '1.1.1.1')
        self.ixNet.commit()

        self.ixNet.setAttribute(self.ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
        self.ixNet.commit()
        self.ixNet.setMultiAttribute(self.ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
        self.ixNet.commit()
        time.sleep(5)

        print (self.ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

        print("Adding Openflow Switch over IP4 stacks")
        self.ixNet.add(ip1, 'openFlowSwitch')
        self.ixNet.commit()

        openFlowSwitch1 = self.ixNet.getList(ip1, 'openFlowSwitch')[0]
        print openFlowSwitch1
        time.sleep(5)

        openflowSwitchchannels = self.ixNet.add(openFlowSwitch1, 'OFSwitchChannel')
        self.ixNet.commit()
        time.sleep(5)

        openflowchannellist = self.ixNet.getList(openFlowSwitch1, 'OFSwitchChannel')[0]
        self.ixNet.setMultiAttribute(openflowSwitchchannels, '-auxConnectionsPerChannel', '1')
        self.ixNet.commit()
        time.sleep(5)

        #openflowTablelist = self.ixNet.getList(ip1, 'switchTablesList')[0]
        self.ixNet.setMultiAttribute(openFlowSwitch1, '-numberOfTableRanges', '3')
        self.ixNet.commit()
        time.sleep(5)

        switchTableList = self.ixNet.getList(openFlowSwitch1, 'switchTablesList')[0]
        print switchTableList

        networkTopologyObj = self.ixNet.add(deviceGroup1, 'networkTopology')
        self.ixNet.commit()
        networkTopologyObjRing = self.ixNet.add(networkTopologyObj, 'netTopologyRing')
        self.ixNet.commit()

        self.start_protocol_check_stats()

        swtopology = self.ixNet.getList(self.ixNet.getRoot(), 'topology')[0]
        print swtopology
        deviceGroupSW = self.ixNet.getList(swtopology, 'deviceGroup')[0]
        ethernetSw = self.ixNet.getList(deviceGroupSW, 'ethernet')[0]
        ipv4Sw = self.ixNet.getList(ethernetSw, 'ipv4')[0]
        ofSw = self.ixNet.getList(ipv4Sw, 'openFlowSwitch')[0]
        print "Now disable/Enable of switch on the fly"
        self.on_the_fly(ofSw)

        print "Changing Ethernet Address, Port number on the fly!!!!!"
        swPortActive = self.ixNet.getList(ofSw, 'ofSwitchPorts')[0]
        print swPortActive
        self.on_the_fly_port_number_ethernetaddress(swPortActive)

        print "Fetching Switch Learned info !!!!!"
        self.print_learned_info(ofSw)

        print ('!!! Test Script Ends !!!')

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
if __name__ == "__main__":
    ixTclServer = '10.214.101.141'
    ixTclPort = '8558'
    ports = [('12.0.1.253', '5', '10',)]
    version = '8.10'
    switch = NgpfOpenFlowSwitch(ixTclServer, ixTclPort, version)
    switch.main()

