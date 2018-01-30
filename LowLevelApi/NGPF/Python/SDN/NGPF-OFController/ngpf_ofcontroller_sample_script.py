# -*- coding: cp1252 -*-
#!/usr/bin/tclsh
################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright © 1997 - 2015 by IXIA                                           #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    13/07/2016 - Sarabjeet Kaur - created sample                              #
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
#    IxOS      8.10 EA                                                         #
#    IxNetwork 8.10 EA                                                         #
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

class NgpfOpenFlowController(object):
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

    def assignPorts (self, realPort1) :
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

        cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1,port1)
        self.ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
                                '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
        self.ixNet.commit()
    ################################################################################
    # Method for enabling  and set values for match criteria & Instruction Actions                                          #
    ################################################################################
    def enablematchesinstructions (self, flow_profile, required_match_criteria_list, required_instruction, required_action):
        global1 = self.ixNet.getList(self.root, 'globals')[0]
        topo1 = self.ixNet.getList(global1, 'topology')[0]
        ofcontroller1 = self.ixNet.getList(topo1, 'openFlowController')[0]
        flowtemp = self.ixNet.getList(ofcontroller1, 'flowSetTemplate')[0]
        predefined_template = self.ixNet.add(flowtemp, 'predefined')
        flow_template = self.ixNet.add(predefined_template, 'flowTemplate')
        self.ixNet.commit()
        time.sleep(5)
        matchactionlist = self.ixNet.getList(flow_template, 'matchAction')
        for i in matchactionlist:
            print i
            print self.ixNet.getAttribute(i, '-name')
            if (self.ixNet.getAttribute(i, '-name') == "[1] Blank Template"):
                print "success"
                self.ixNet.execute('addFromTemplate', flow_profile, i)
                self.ixNet.commit()
                time.sleep(5)

        flow_profile_matchAction = self.ixNet.getList(flow_profile, 'matchAction')[0]
        flow_profilematch_criteria = self.ixNet.getList(flow_profile_matchAction, 'matchCriteria')[0]
        match_criteria_list = self.ixNet.getList(flow_profilematch_criteria, 'matchCriteria')

        for matchCriteria in match_criteria_list:
            if self.ixNet.getAttribute(matchCriteria, '-name') == "Ethernet":
                print "Match criteria is ethernet"
                self.ixNet.setMultiAttribute(matchCriteria, '-isEnabled', 'true')
                self.ixNet.commit()
                ethernetmatchCriteria = self.ixNet.getList(matchCriteria, 'matchCriteria')
                print ethernetmatchCriteria
                for ethernetmatchlist in ethernetmatchCriteria:
                    if self.ixNet.getAttribute(ethernetmatchlist, '-name') == "Ethernet Source":
                        ethernetsourcefield = self.ixNet.getList(ethernetmatchlist, 'field')[0]
                        print ethernetsourcefield
                        valuemulti = self.ixNet.getAttribute(ethernetsourcefield, '-value')
                        print valuemulti
                        self.ixNet.setAttribute(valuemulti + '/singleValue', '-value', '44:0:0:0:0:77')
                        self.ixNet.commit()
                        time.sleep(5)
                    else:
                        ethernetdestinationfield = self.ixNet.getList(ethernetmatchlist, 'field')[0]
                        print ethernetdestinationfield
                        valuemulti = self.ixNet.getAttribute(ethernetdestinationfield, '-value')
                        print valuemulti
                        self.ixNet.setAttribute(valuemulti + '/singleValue', '-value', '11:0:0:0:0:77')
                        self.ixNet.commit()
                        time.sleep(5)

            if self.ixNet.getAttribute(matchCriteria, '-name') == "IP":
                print "Match criteria is IP"
                self.ixNet.setMultiAttribute(matchCriteria, '-isEnabled', 'true')
                self.ixNet.commit()
                ipmatchCriteria = self.ixNet.getList(matchCriteria, 'matchCriteria')[0]
                print ipmatchCriteria
                ipv4list = self.ixNet.getList(ipmatchCriteria, 'matchCriteria')
                for ipv4names in ipv4list:
                    if self.ixNet.getAttribute(ipv4names, '-name') == "IPv4 Source":
                        ipsourcefield = self.ixNet.getList(ipv4names, 'field')[0]
                        print ipsourcefield
                        valuemulti = self.ixNet.getAttribute(ipsourcefield, '-value')
                        print valuemulti
                        self.ixNet.setAttribute(valuemulti + '/singleValue', '-value', '67.1.1.1')
                        self.ixNet.commit()
                        time.sleep(5)
                    else:
                        ipdestinationfield = self.ixNet.getList(ipv4names, 'field')[0]
                        print ipdestinationfield
                        valuemulti = self.ixNet.getAttribute(ipdestinationfield, '-value')
                        print valuemulti
                        self.ixNet.setAttribute(valuemulti + '/singleValue', '-value', '4.1.1.1')
                        self.ixNet.commit()
                        time.sleep(5)

        flowProfileMatchAction = self.ixNet.getList(flow_profile, 'matchAction')[0]
        flowProfileInstruction = self.ixNet.getList(flowProfileMatchAction, 'instructions')[0]
        print "Adding instruction"
        self.ixNet.execute('addInstruction', flowProfileInstruction, "Apply Actions")
        self.ixNet.commit()
        flowProfileInstructionAdded = self.ixNet.getList(flowProfileInstruction, 'instruction')[0]
        print flowProfileInstructionAdded
        print "Adding 2 action"
        for action in required_action:
            self.ixNet.execute('addAction', flowProfileInstructionAdded, action)
            self.ixNet.commit()

        actionsAdded = self.ixNet.getList(flowProfileInstructionAdded, 'actions')[0]
        actionList = self.ixNet.getList(actionsAdded, 'action')
        print actionList
        for action in actionList:
            if (self.ixNet.getAttribute(action, '-name')) == "Set Ethernet Source":
                print "action is Set Ethernet Source"
                val = "4:6:0:0:0:0"
                print val
            else:
                print "action is Set Ethernet Destination"
                val = "7:7:4:8:1:7"
                print val
            field = self.ixNet.getList(action, 'field')[0]
            print field
            actionValue = self.ixNet.getAttribute(field, '-value')
            print actionValue
            self.ixNet.setAttribute(actionValue + '/singleValue', '-value', val)
            self.ixNet.commit()

    ################################################################################
    # Start protocol and check statistics                                          #
    ################################################################################
    def start_protocol_check_stats(self):

        print("Starting protocols and waiting for 45 seconds for protocols to come up")
        self.ixNet.execute('startAllProtocols')
        time.sleep(45)
        print ("Fetching all Protocol Summary Stats\n")
        viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
        statcap   = self.ixNet.getAttribute(viewPage, '-columnCaptions')
        for statValList in self.ixNet.getAttribute(viewPage, '-rowValues') :
            for  statVal in statValList :
                print("***************************************************")
                index = 0
                for satIndv in statVal :
                    print("%-30s:%s" % (statcap[index], satIndv))
                    index = index + 1
        print("***************************************************")

        print ("Verifying OpenFlow Controller Per Port stats\n")
        viewPage  = '::ixNet::OBJ-/statistics/view:"OpenFlow Controller Per Port"/page'
        statcap   = self.ixNet.getAttribute(viewPage, '-columnCaptions')
        for statValList in self.ixNet.getAttribute(viewPage, '-rowValues') :
            for  statVal in statValList :
                print("***************************************************")
                index = 0
                for satIndv in statVal :
                    print("%-30s:%s" % (statcap[index], satIndv))
                    index = index + 1
        print("***************************************************")

    ################################################################################
    # On the fly section                                                           #
    ################################################################################
    def on_the_fly(self, flow_profile):
        flowProfileMatchAction = self.ixNet.getList(flow_profile, 'matchAction')[0]
        print flowProfileMatchAction
        flowProfileInstruction = self.ixNet.getList(flowProfileMatchAction, 'instructions')[0]
        flowProfileInstructionAdded = self.ixNet.getList(flowProfileInstruction, 'instruction')[0]
        actionsAdded = self.ixNet.getList(flowProfileInstructionAdded, 'actions')[0]
        actionList = self.ixNet.getList(actionsAdded, 'action')[0]
        print actionList
        if (self.ixNet.getAttribute(actionList, '-name')) == "Set Ethernet Source":
            print "Modifying Set Ethernet Source  Value OTF to 16:44:33:2:1:1"
            val = "16:44:33:2:1:1"
        Ethernetfield = self.ixNet.getList(actionList, 'field')[0]
        actionValue = self.ixNet.getAttribute(Ethernetfield, '-value')
        self.ixNet.setAttribute(actionValue + '/singleValue', '-value', val)
        self.ixNet.commit()

        globalObj = self.ixNet.getRoot() + '/globals'
        topology  = globalObj + '/topology'
        print ("Applying changes on the fly")
        try:
            self.ixNet.execute('applyOnTheFly', topology)
        except:
            print("error in applying on the fly change")
        time.sleep(10)

    ###############################################################################
    # print learned info                                                          #
    ###############################################################################
    def print_learned_info(self, openFlowController1):
        self.ixNet.execute('getOFChannelLearnedInfo', openFlowController1, '1')
        time.sleep(5)
        print("Print OFController Learned Info")
        linfo  = self.ixNet.getList(openFlowController1, 'learnedInfo')[0]
        linfoList = self.ixNet.getList(linfo, 'table')
        print("***************************************************")
        for table in linfoList :
            tableType = self.ixNet.getAttribute(table, '-type')
            print(tableType)
            print("=================================================")
            columns = self.ixNet.getAttribute(table, '-columns')
            print(columns)
            values = self.ixNet.getAttribute(table, '-values')
            for value in values :
                for word in values :
                    print(word)
        time.sleep(15)
        print "Set on demand message for flow stat!!!!"
        OfChanneLearnedinfoList = self.ixNet.getList(openFlowController1, 'ofChannelLearnedInfoList')[0]
        OnDemandMessage = self.ixNet.getAttribute(OfChanneLearnedinfoList, '-onDemandMessages')
        values1 = self.ixNet.getAttribute(OnDemandMessage, '-values')[0]
        self.ixNet.setAttribute(OnDemandMessage + '/singleValue', '-value', "flowstat")
        print "sending on demand message on the fly for flow stat learned info"
        self.ixNet.execute('sendOnDemandMessage', OfChanneLearnedinfoList, 1)


        print ('Stopping protocols')
        self.ixNet.execute('stopAllProtocols')

    ################################################################################
    # protocol configuration section                                               #
    ################################################################################
    def main(self):
        self.assignPorts(ports[0])
        root    = self.ixNet.getRoot()
        vportTx = self.ixNet.getList(root, 'vport')[0]

        print("adding topologies")
        self.ixNet.add(root, 'topology', '-vports', vportTx)
        self.ixNet.commit()
        topologies = self.ixNet.getList(self.ixNet.getRoot(), 'topology')
        topo1 = topologies[0]

        print "Adding 2 device groups"
        self.ixNet.add(topo1, 'deviceGroup')
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
        mvGw1  = self.ixNet.getAttribute(ip1, '-gatewayIp')

        print("configuring ipv4 addresses")
        self.ixNet.setAttribute(mvAdd1 + '/singleValue', '-value', '1.1.1.2')
        self.ixNet.commit()
        self.ixNet.setAttribute(mvGw1  + '/singleValue', '-value', '1.1.1.1')
        self.ixNet.commit()

        self.ixNet.setAttribute(self.ixNet.getAttribute(ip1, '-prefix') + '/singleValue', '-value', '24')
        self.ixNet.commit()
        self.ixNet.setMultiAttribute(self.ixNet.getAttribute(ip1, '-resolveGateway') + '/singleValue', '-value', 'true')
        self.ixNet.commit()
        time.sleep(5)

        print (self.ixNet.help('::ixNet::OBJ-/topology/deviceGroup/ethernet/ipv4'))

        print("Adding Openflow Controller over IP4 stacks")
        self.ixNet.add(ip1, 'openFlowController')
        self.ixNet.commit()

        openFlowController1 = self.ixNet.getList(ip1, 'openFlowController')[0]
        print openFlowController1
        time.sleep(5)

        openflowchannels = self.ixNet.add(openFlowController1, 'openFlowChannel')
        self.ixNet.commit()
        time.sleep(5)

        openflowchannellist = self.ixNet.getList(openFlowController1, 'openFlowChannel')[0]
        self.ixNet.setMultiAttribute(openflowchannels, '-groupsPerChannel', '1')
        self.ixNet.commit()
        time.sleep(5)

        self.ixNet.setMultiAttribute(openflowchannels, '-metersPerChannel', '1')
        self.ixNet.commit()
        time.sleep(5)

        table1 = self.ixNet.getList(openflowchannellist, 'tables')[0]
        flowset = self.ixNet.getList(table1, 'flowSet')[0]
        flowprofile = self.ixNet.getList(flowset, 'flowProfile')[0]
        requiredMatchCriteriaList = ["Ethernet", "IP"]
        requiredInstruction = ["Apply Actions"]
        requiredaction = ["Set Ethernet Source", "Set Ethernet Destination"]
        self.enablematchesinstructions(flowprofile, requiredMatchCriteriaList, requiredInstruction, requiredaction)

        self.start_protocol_check_stats()
        self.on_the_fly(flowprofile)
        self.print_learned_info(openFlowController1)
        print ('!!! Test Script Ends !!!')


#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information   #
# below                                                                         #
#################################################################################
if __name__ == "__main__":
    ixTclServer = '10.214.101.141'
    ixTclPort = '8564'
    ports = [('12.0.1.253', '5', '10',)]
    version = '8.10'
    controller = NgpfOpenFlowController(ixTclServer, ixTclPort, version)
    controller.main()

