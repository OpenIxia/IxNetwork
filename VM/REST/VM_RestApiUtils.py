#!/usr/bin/python
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
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample script                                                        #
#    - Contains function definitions for IxVM REST specific operations         #
#                                                                              #
################################################################################

from FW_RestApiUtils import *

class RestCB:

    @staticmethod
    def getHypervisorIP():
        return '10.215.191.229'
        #return '10.215.191.219'

    #######################################################
    # get the Url from a multivalue url for a specific pattern
    # a = getMultiValueFromUrl(baseUrl, "counter")
    #######################################################
    @staticmethod
    def ixNetGetList(getAttUrl, child, logging=True):
        try:
            h = httplib2.Http()
            getUrl = getAttUrl+"/"+child
            if logging:
                print ("GET: " + getUrl + " <-- Child: " + str(child))
            # response = requests.get(getUrl)
            response, content = h.request(getUrl,'GET')
            res = json.loads(content)
        except Exception as e:
            raise Exception('Got an error code: ', e)
        if response.status != 200 :
            raise TestFailedError(json.loads(content)['errors'])
        return res

    @staticmethod
    def rediscovery(sessionUrl):
        print ("* [rediscovery] :")
        print ("\t - Triggering rediscovery... (ixNet exec rediscoverAppliances)")
        ixNetExec(sessionUrl,'rediscoverAppliances')

    @staticmethod
    def getIP_list(sessionUrl , string_match = "newFeatures_" ):
        print ("* [getIP_list] :")
        print ("\t - string_match : " + str(string_match))
        ip_list = []
        RestCB.rediscovery(sessionUrl)

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        disApp = RestCB.ixNetGetList(vChassisUrl,"discoveredAppliance",True)
        for da in disApp:
            if string_match in str(da['applianceName']):
                ip_list.append(str(da['managementIp']))

        return ip_list

    #KB Added
    # Will retrun list of card IPs which are already connected to the chassis
    @staticmethod
    def getIP_list_chassis(sessionUrl):
        print ("* [getIP_list_chassis] :")
        ip_list = []

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        disApp = RestCB.ixNetGetList(vChassisUrl,"ixVmCard")
        for da in disApp:
            ip_list.append(str(da['managementIp']))
        return ip_list


    #KB Added
    # Will retrun list of card status which are already connected to the chassis
    @staticmethod
    def getCardStatus_list_chassis(sessionUrl):
        print ("* [getCardStatus_list_chassis] :")
        card_list = []

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        disApp = RestCB.ixNetGetList(vChassisUrl,"ixVmCard")
        for da in disApp:
            card_list.append(str(da['cardState']))
        return card_list


    @staticmethod
    def addDefaultHypervisor(sessionUrl):
        print ("* [addDefaultHypervisor] :")
        hypervisorIp = RestCB.getHypervisorIP()

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)
        hyp_ips = []
        print ('- hypervisors list :')
        for hypervisor in hypervisorsList:
            print ("\t - type : " + str(hypervisor['type']) +" ; IP :" + str(hypervisor['serverIp']))

            # Enable the default hypervisor ..if it is needed
            if str(hypervisor['serverIp']) == hypervisorIp and str(hypervisor['enabled']) != "true" and str(hypervisor['type']) != "qemu":
                ed = {'enabled': 'true' , 'type':'qemu'}
                vChassisUrlEd = vChassisUrl + "/hypervisor/" + str(hypervisor['id'])
                ixNetSetAttFromSession(vChassisUrlEd,"",ed)

            hyp_ips.append(str(hypervisor['serverIp']))

        if hypervisorIp not in hyp_ips:
            print ("\t -> add new hypervisor : type : qemu ; IP : " + str(hypervisorIp))
            paylod = {"enabled" : "true",  "serverIp" : hypervisorIp,  "type" : "qemu", "user" : "root", "password" : "ixia123"}
            cardTest1 = addIxNetObject(vChassisUrl,"hypervisor",paylod)

        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)

    # KB/Tarak
    # Adding hypervisor
    @staticmethod
    def addHypervisor(sessionUrl, enabled, hypervisorIp, type, user, password):
        print ("* [add Hypervisor] :")
        print ("\t - enabled : " + str(enabled))
        print ("\t - hypervisorIp : " + str(hypervisorIp))
        print ("\t - type : " + str(type))
        print ("\t - user : " + str(user))
        print ("\t - password : " + str(password))
        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)
        hyp_ips = []
        print ('- hypervisors list :')
        for hypervisor in hypervisorsList:
            print ("\t - type : " + str(hypervisor['type']) +" ; IP :" + str(hypervisor['serverIp']))
            hyp_ips.append(str(hypervisor['serverIp']))

        if hypervisorIp not in hyp_ips:
            print ("\t -> add new hypervisor : type :" + str(type) + " ; IP : " + str(hypervisorIp))
            paylod = {"enabled" : enabled,  "serverIp" : hypervisorIp,  "type" : type, "user" : user, "password" : password}
            cardTest1 = addIxNetObject(vChassisUrl,"hypervisor",paylod)
        else:
            print ("\t -> Hypervisor already added")
        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)

    # KB/Tarak
    # Deleting hypervisor
    @staticmethod
    def deleteHypervisor(sessionUrl, hypervisorIp):
        print ("* [delete Hypervisor] :")
        print ("\t - hypervisorIp : " + str(hypervisorIp))
        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)
        hyp_ips = []
        print ('- hypervisors list :')
        for hypervisor in hypervisorsList:
            hyp_ips.append(str(hypervisor['serverIp']))
            if hypervisorIp == str(hypervisor['serverIp']) :
                print ("\t - type : " + str(hypervisor['type']) +" ; IP :" + str(hypervisor['serverIp']) + " ID : " + str(hypervisor['id']))
                vChassisUrlDel = vChassisUrl + "/hypervisor/" + str(hypervisor['id'])
                print ("delete URL" + str(vChassisUrlDel))
                removeIxNetObject(vChassisUrlDel)

        if hypervisorIp not in hyp_ips:
            print ("Nothing to delete")

        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)


    # KB/Tarak
    # Enable/Disable hypervisor
    @staticmethod
    def enableDisableHyp(sessionUrl, enabled, hypervisorIp):
        print ("* [enable/disable Hypervisor] :")
        print ("\t - enabled : " + str(enabled))
        print ("\t - hypervisorIp : " + str(hypervisorIp))
        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)
        hyp_ips = []
        print ('- hypervisors list :')
        for hypervisor in hypervisorsList:
            hyp_ips.append(str(hypervisor['serverIp']))
            if hypervisorIp == str(hypervisor['serverIp']) :
                print ("\t - type : " + str(hypervisor['type']) +" ; IP :" + str(hypervisor['serverIp']) + " enabled : " + str(hypervisor['enabled']))
                if str(hypervisor['enabled']) != enabled:
                    ed = {'enabled': enabled}
                    vChassisUrlEd = vChassisUrl + "/hypervisor/" + str(hypervisor['id'])
                    setEd = ixNetSetAttFromSession(vChassisUrlEd,"",ed)

        if hypervisorIp not in hyp_ips:
            print ("\t -> add new hypervisor : type :" + str(type) + " ; IP : " + str(hypervisorIp))
            paylod = {"enabled" : enabled,  "serverIp" : hypervisorIp,  "type" : type, "user" : user, "password" : password}
            cardTest1 = addIxNetObject(vChassisUrl,"hypervisor",paylod)

        hypervisorsList = RestCB.ixNetGetList(vChassisUrl, 'hypervisor', False)

    @staticmethod
    def clear_topology(sessionUrl):
        print ("* [Clear topology] :")
        print ("\t - Collecting card list...")
        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        card_list = RestCB.ixNetGetList(vChassisUrl,'ixVmCard')
        print ("\t - Removing all existing cards... if any...")
        for card in card_list:
            cardId = str(card['cardId'])
            cardUrl = sessionUrl.split('/api')[0]+str(card['links'][-1]['href'])
            arg = {"arg1" : cardId}
            ixNetExec(sessionUrl,'clearCardOwnershipById',arg)
            removeIxNetObject(cardUrl)
        print ("\t - Checking that cards were deleted...")
        card_list = RestCB.ixNetGetList(vChassisUrl,'ixVmCard')
        if len(card_list) != 0:
            raise TestFailedError("Card list not cleared... check your configuration!")
        print ("\t - Card list cleared!")


    @staticmethod
    def addIxvmCard(sessionUrl, mngtIP, cardId="", keepalive=""):
        print ("* [addIxvmCard] :")
        print ("\t - mngtIP : " + str(mngtIP))
        print ("\t - cardId : " + str(cardId))
        print ("\t - keepalive : " + str(keepalive))

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        payload = { 'managementIp' : str(mngtIP) }
        if cardId != "":
            payload = { 'managementIp' : str(mngtIP) , 'cardId' : cardId}
        if keepalive != "":
            payload = { 'managementIp' : str(mngtIP) , 'cardId' : cardId , 'keepAliveTimeout' : str(keepalive)}
        if cardId == "" and keepalive != "":
            payload = { 'managementIp' : str(mngtIP) , 'keepAliveTimeout' : str(keepalive)}

        cardTest1 = addIxNetObject(vChassisUrl,"ixVmCard",payload)

        #Find the new URL :
        cardUrl = ""
        card_list = RestCB.ixNetGetList(vChassisUrl,'ixVmCard')
        for card in card_list:
            if card['managementIp'] == mngtIP:
                cardUrl = sessionUrl.split('/api')[0]+str(card['links'][-1]['href'])

        return cardUrl

    @staticmethod
    def addIxvmPort(cardUrl , interface , portId = "" , promisc = "", mtu = ""):
        print ("* [addIxvmPort] :")
        print ("\t - cardUrl : " + str(cardUrl))
        print ("\t - interface : " + str(interface))
        print ("\t - portId : " + str(portId))
        print ("\t - promisc : " + str(promisc))
        print ("\t - mtu : " + str(mtu))

        payload = { 'interface' : str(interface) }
        if portId != "":
            payload = { 'interface' : str(interface) , 'portId' : portId}
        if promisc != "":
            payload = { 'interface' : str(interface) , 'portId' : portId , 'promiscMode' : str(promisc)}
        if portId == "" and promisc != "":
            payload = { 'interface' : str(interface) , 'promiscMode' : str(promisc)}
        if mtu != "":
            payload["mtu"] = str(mtu)

        newPort = addIxNetObject(cardUrl,"ixVmPort",payload)

        #Find the new URL :
        portUrl = ""
        port_list = RestCB.ixNetGetList(cardUrl,'ixVmPort')
        for port in port_list:
            if port['interface'] == interface:
                portUrl = cardUrl.split('/api')[0]+str(port['links'][-1]['href'])

        return portUrl

    @staticmethod
    def split_port(port):
        splitted = port[1:-1].split(";")
        return splitted

    @staticmethod
    def getChassisTopology (sessionUrl) :
        print ("* [getChassisTopology] :")
        headers = ['Card ID', 'Card IP', 'KeepAlive', 'Port ID', 'Interface Name', 'Promisc', 'MAC Address', 'MTU', 'Speed']

        refCH = ixNetExec(sessionUrl,"refreshChassisTopology")
        print ("refCH = " + str(refCH))
        topology = json.loads(refCH)["result"]

        resulted_topo = []
        expected_row = []
        expected_port = []
        for port in topology:
            portx = RestCB.split_port(port)
            expected_port.append('Port')
            for i in range(0,len(headers)):
                row = (headers[i],portx[i])
                expected_row.append(row)
            expected_port.append(expected_row)
            expected_row = []
            resulted_topo.append(expected_port)
            expected_port = []
        return resulted_topo


    @staticmethod
    def create_toplogy(sessionUrl,ip_list,card_count,ports_per_card):
        print ("* [create_toplogy] :")
        print ("\t - ip_list : " + str(ip_list))
        print ("\t - card_count : " + str(card_count))
        print ("\t - ports_per_card : " + str(ports_per_card))

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"

        print("Adding %s cards..." % str(card_count))
        for i in range(0,card_count):
            newCard = RestCB.addIxvmCard(sessionUrl,ip_list[i])
            for j in range(1,ports_per_card+1):
                newPort = RestCB.addIxvmPort(newCard,"eth"+str(j))


        card_list = RestCB.ixNetGetList(vChassisUrl,'ixVmCard')

        print("Checking that we now have %s cards in our configuration..." % str(card_count))
        if len(card_list) != card_count:
            raise TestFailedError("Card list not cleared... check your configuration!")
        print ("Card list contains %s cards!" % card_count)

        return 0

    @staticmethod
    def getCardStatus(sessionUrl,card_id, logging= True , withRefresh = True):
        if logging:
            print ("* [getCardStatus] :")
            print ("\t - card_id : " + str(card_id))

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        card_list=[]
        if withRefresh == True:
            ixNetExec(sessionUrl,"refreshChassisTopology")

        card_list = RestCB.ixNetGetList(vChassisUrl,'ixVmCard',False)

        for card in card_list:
            if card['cardId'] == str(card_id):
                return card['cardState']
        if logging:
            print ("Card %s ID does not exist!" % card_id)


    @staticmethod
    def getPortStatus(sessionUrl,card_id,port_id):
        print ("* [getPortStatus] :")
        print ("\t - card_id : " + str(card_id))
        print ("\t - port_id : " + str(port_id))

        vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"
        ixNetExec(sessionUrl,"refreshChassisTopology")
        card_list = RestCB.ixNetGetList(vChassisUrl,'ixVmCard')

        cardUrl = ""

        for card in card_list:
            if card['cardId'] == str(card_id):
                cardUrl = sessionUrl.split('/api')[0]+str(card['links'][-1]['href'])

        if cardUrl == "":
            print ("The specified card does not exist")
            return

        port_list = RestCB.ixNetGetList(cardUrl,'ixVmPort')
        for port in port_list:
            if port['portId'] == str(port_id):
                return port['portState']
        print ("Port %s from card %s does not exist!" % (str(port_id),str(card_id)))


    @staticmethod
    def card_reboot (sessionUrl,chassis_ip,card_id) :
        print ("Card Reboot")
        print ("Chassis IP: " + str(chassis_ip))
        print ("Card ID: " + str(card_id))

        timeout = 300
        print ("Connecting to VM Chassis: " + str(chassis_ip))

        arg1 = {"arg1":chassis_ip}
        connectChassis = ixNetExec(sessionUrl,"connectToChassis",arg1)

        print ("Rebooting Card" + str(card_id))
        arg1 = {"arg1":card_id}
        reboot = ixNetExec(sessionUrl,"hwrebootcardbyids",arg1)

        Card_Status = RestCB.checkCard_disconnect_Connect (sessionUrl,card_id)

        print ("Success: Rebooting card " + str(card_id))

    @staticmethod
    def chassis_reboot (sessionUrl) :
        print ("Chassis Reboot")
        reboot = ixNetExec(sessionUrl,"rebootvirtualchassis")
        print ("Success: Rebooting chassis ")



    @staticmethod
    def checkCard_disconnect_Connect (sessionUrl,card_id,timeout=120) :
        print ("* Check if card was disconnected")
        cardStatus = RestCB.getCardStatus(sessionUrl,card_id)
        i = 0
        while (cardStatus != "cardDisconnected" and i < 35) :
            print ("cardStatus is: " + str(cardStatus))
            print ("Wait for 5 sec; Expected card status: cardDisconnected ... (" + str(i) + ")")
            time.sleep(5)
            cardStatus = RestCB.getCardStatus (sessionUrl,card_id)
            i = i + 5
        if i >= timeout :
            print ("The card was not disconnected after (sec) " + str(i))
        else :
            print ("The card was disconnected after (sec) " + str(i))

        print ("Wait for card to be reconnected")
        cardStatus = RestCB.getCardStatus (sessionUrl,card_id)
        i = 0
        while (cardStatus != "cardOK" and i < timeout) :
            print ("cardStatus is: " + str(cardStatus))
            print ("Wait for 5 sec; Expected card status: cardOK ... (" + str(i) + ")")
            time.sleep(5)
            cardStatus = RestCB.getCardStatus (sessionUrl,card_id)
            i = i + 5
        if i >= timeout :
            print ("The card was not reconnected after (sec) " + str(i))
            raise TestFailedError("The card was not reconnected... check your configuration!")
        else :
            print ("The card was reconnected after (sec) " + str(i))

    @staticmethod
    def checkPortsAvailable (sessionUrl) :
        print ("Checking that the ports are available..")
        ports = RestCB.ixNetGetList(sessionUrl, "vport")
        portStates = []
        portDictionary = {}
        for port in ports:
            portLink = port['links'][-1]['href']
            portLink2 = sessionUrl.split('/api/v1')[0] + port['links'][-1]['href']
            portID = port['links'][-1]['href'].split('vport/')[1]
            portState = ixNetGetAtt(portLink2, "state")
            portStates.append(portState)
            portDictionary[str(portID)] = str(portState)

        sep = '+' + '-' * 25 + '+' + '-' * 65 + '+'
        print (sep)
        print ('| {0:23} | {1:63} |'.format('Ports ID:', 'Cause of problem:'))
        print (sep)
        for i in range(1, len(ports) + 1):
            print ('| {0:23} | {1:63} |'.format(i, portDictionary[str(i)]))
        print (sep)

    @staticmethod
    def matchInCapturedPkt(ixNet, currentPkt, matchFieldList):
        #initilize return value
        PASSED = 0
        FAILED = 1

        for stack, fieldList in matchFieldList:
            print(fieldList)
            isStackFound = 0
            #stackList = (currentPkt + "/stack")
            stackList = RestCB.ixNetGetList(currentPkt, 'stack')
            print(stackList)
            #print ("***** STACKLIST: $stackList *****"
            for pktStack in stackList:
                print(pktStack)
                if (pktStack['displayName'] != stack):
                    continue
                else:
                    isStackFound = 1
                    #print ("Browing $stack to match $fieldList"
                    print ("Check")
                    for fieldName, fieldValue in fieldList:
                        print ("Aici %s  %s"%(fieldName,fieldValue))
                        isFound = 0
                        fldList = RestCB.ixNetGetList(sessionUrl.split('/api/v1')[0] + pktStack['links'][0]['href'], '')
                        print(fldList)
                        #print ("----- FIELDLIST: $fldList -----"
                        for pktStackField in fldList:
                            print(pktStackField)
                            if str(pktStackField['displayName']) != str(fieldName):
                                continue
                            else:
                                isFound = 1
                                if str(pktStackField['fieldValue']) != str(fieldValue):
                                    print("%s: %s (obtained) %s (expected)" %(fieldName, str(pktStackField['fieldValue']), fieldValue))
                                    return FAILED
                                else:
                                    print("%s: %s (obtained)  %s (expected)" %(fieldName, str(pktStackField['fieldValue']), fieldValue))
                                    break
                            if (isFound == 0):
                                print("No match found for %s" %fieldName)
                                isStackFound = 0
                                break
                        if (isFound == 1) and (isStackFound == 1):
                            print("All fields matched...")
                            break

                if isStackFound == 0:
                    #puts "No matching $stack found to match $fieldList"
                    return FAILED
            print("All Field Patterns Matched for this packet")
            return PASSED



    @staticmethod
    def card_reboot (sessionUrl,chassis_ip,card_id,timeoutReconnect=120) :
        print ("Card Reboot")
        print ("Chassis IP: " + str(chassis_ip))
        print ("Card ID: " + str(card_id))

        timeout = 300
        print ("Connecting to VM Chassis: " + str(chassis_ip))

        arg1 = {"arg1":chassis_ip}
        connectChassis = ixNetExec(sessionUrl,"connecttochassis",arg1)

        cardIdList = []
        cardIdList.append(card_id)

        print ("Rebooting Card " + str(card_id))

        #reboot = ixNetExec(sessionUrl,"hwrebootcardbyids",arg1)

        cardDiscOK = 0
        cardStatus = RestCB.getCardStatus(sessionUrl,card_id,False,False)

        print ("Current cardStatus : " + str(cardStatus))
        print ("")
        try:
            h = httplib2.Http()
            urlString = sessionUrl + "/operations/hwrebootcardbyids"
            urlHeadersJson = {'content-type': 'application/json'}
            arg1 = {"arg1":cardIdList}
            print (arg1)
            # response = requests.post(url=urlString, headers=urlHeadersJson,data=json.dumps(arg1))
            response, content = h.request(urlString,'POST',json.dumps(arg1),urlHeadersJson)
            a = json.loads(content)
            for key in a:
               if "errors" in key:
                    raise Exception('FAIL : need To Exit ',a["errors"])
            state = a["state"]
            url = a["url"]

            if state == "SUCCESS" and url == "":
                print ("Exec is SUCCESS")
            elif state == "ERROR":
                raise Exception('FAIL : need To Exit ',a["result"])
            else:
                if state != "COMPLETED":
                    print ("WAIT FOR ACTION TO COMPLETE")
                    url = a["url"].split("operations/")[1]
                    print ("Current state: " + state)
                    it = 0
                    while state == "IN_PROGRESS":
                        if timeout == it:
                            raise TestFailedError ("Operation is still in progress after : " + str(timeout) + " seconds")
                        time.sleep(1)
                        state = ixNetGetAtt(sessionUrl + "/operations/" + url, "state", False)
                        response, content = h.request(sessionUrl + "/operations/" + url, 'GET', json.dumps(arg1), urlHeadersJson)
                        cardStatus = RestCB.getCardStatus(sessionUrl,card_id,False,False)
                        print ("Current EXEC state: " + state + "; cardStatus :" + str(cardStatus) + " after (" + str(it) + ") seconds")
                        if cardStatus == "cardDisconnected":
                            cardDiscOK = 1
                        it = it + 1
        except Exception as e:
            raise Exception('Got an error code: ', e)
        if response.status != 200 :
            raise TestFailedError(json.loads(content)['errors'])

        if cardDiscOK == 0:
            raise TestFailedError(" The card was not disconnect from ixE ... maybe the reboot doesn't work properly")

        i = 0
        print ("Wait for card to be reconnected")
        while (cardStatus != "cardOK" and i < timeoutReconnect) :
            print ("cardStatus is: " + str(cardStatus))
            print ("Wait for 5 sec; Expected card status: cardOK ... (" + str(i) + ")")
            time.sleep(5)
            cardStatus = RestCB.getCardStatus (sessionUrl,card_id)
            i = i + 5
        if i >= timeout :
            print ("The card was not reconnected after (sec) " + str(i))
            raise TestFailedError("The card was not reconnected... check your configuration!")
        else :
            print ("The card was reconnected after (sec) " + str(i))

        print ("Success: Rebooting card " + str(card_id))

class VM:

#######################################################
# getPortMacs returns a list of the port mac addresses used in the config
# Note: This procedure is used by updateTrafficForKVM in order to set the mac addresses for raw flows
# Example: getPortMacs(http://10.215.191.227:12345/api/v1/sessions/1/ixnetwork)
#######################################################
    @staticmethod
    def getPortMacs(ixNetSessUrl):
        print ("Getting the MAC addresses for the VMs' test ports...")
        macs = []

        vports = ixNetGetList(ixNetSessUrl, "vport")

        for port in vports:
            portID = port["id"]
            ifgPerPort = []
            portInfo = {}
            connInfo = ixNetGetAtt(ixNetSessUrl + "/vport/" + str(portID), "connectionInfo")
            for elem in connInfo.split(" ", 4):
                key, val = elem.split("=",1)
                portInfo.update({key: val[1:-1]})

            args = {'arg': str(portInfo["chassis"])}
            ixNetExec(ixNetSessUrl, "connectToChassis", args)
            chassisUrl  = ixNetSessUrl + "/availableHardware"
            ixNetGetList(chassisUrl, "virtualChassis")
            chassisUrl  = chassisUrl + "/virtualChassis"
            ixNetGetList(chassisUrl, "ixVmCard")
            cardUrl      = chassisUrl + "/ixVmCard/" + str(portInfo["card"])
            ixNetGetList(cardUrl, "ixVmPort")
            macUrl      = cardUrl + "/ixVmPort/" + str(portInfo["port"])
            macs.append(str(ixNetGetAtt(macUrl, "macAddress")))
        return macs

#######################################################
# updateTrafficForKVM changes RAW flows macs to the actual mac addresses of the vports in use
# Note: This is to be used for KVM and Ubuntu setups, in which 00::...::00 mac addresses are not supported
# Example: updateTrafficForKVM(http://10.215.191.227:12345/api/v1/sessions/1/ixnetwork)
#######################################################
    @staticmethod
    def updateTrafficForKVM(ixNetSessUrl):

        # Get all the available flows
        url = ixNetSessUrl
        ixNetGetList(url, "traffic")
        url = url + "/traffic"
        trList = ixNetGetList(url, "trafficItem")

        macs = VM.getPortMacs(ixNetSessUrl)

        # Change the mac addresses used in all the raw flows to the mac addresses of the actual test ports
        # #1 iterate through traffic items
        for trItem in trList:
            trUrl = url + "/trafficItem/" + str(trItem["id"])
            # Only raw ones need to be changed
            if "RAW" in str(ixNetGetAtt(trUrl, "trafficType")).upper():
                hlsList = ixNetGetList(trUrl, "highLevelStream")
                # #2 iterate through the flows
                for hls in hlsList:
                    hlUrl = trUrl + "/highLevelStream/" + str(hls["id"])
                    # Retrieve the tx and rx port ids
                    txIds = ixNetGetAtt(hlUrl, "txPortId")
                    tx = txIds.split("/")[-1]
                    # There might be multiple rx ports, need to set all of them
                    rxIds = ixNetGetAtt(hlUrl, "rxPortIds")
                    rx = []
                    for rxS in rxIds:
                        rx.append(rxS.split("/")[-1])

                    # #3 iterate through the stacks (ethernet is the one to be changed)
                    stackList = ixNetGetList(hlUrl, "stack")
                    for stackEl in stackList:
                        stackUrl = hlUrl + "/stack/" + str(stackEl["id"])
                        if "ETHERNET" in str(ixNetGetAtt(stackUrl, "displayName")).upper():
                            for field in ixNetGetList(stackUrl, "field"):
                                fieldUrl       = stackUrl + "/field/" + str(field["id"])
                                fieldName   = str(ixNetGetAtt(fieldUrl, "name"))

                                if "SOURCE" in fieldName.upper():
                                        ixNetSetAtt(fieldUrl, {"valueType": "singleValue"})
                                        ixNetSetAtt(fieldUrl, {"singleValue": macs[int(tx)-1]})

                                if "DESTINATION" in fieldName.upper():
                                        destMacs = []
                                        for rxPort in rx:
                                            destMacs.append(macs[int(rxPort)-1])
                                        # Value list for multiple rx ports
                                        if len(destMacs) > 1:
                                            ixNetSetAtt(fieldUrl, {"valueType": "valueList"})
                                            ixNetSetAtt(fieldUrl, {"valueList": destMacs})
                                        # Single value for 1 rx port
                                        else:
                                            ixNetSetAtt(fieldUrl, {"valueType": "singleValue"})
                                            ixNetSetAtt(fieldUrl, {"singleValue": destMacs[0]})
        print ("Successfully updated raw flows macs!")
