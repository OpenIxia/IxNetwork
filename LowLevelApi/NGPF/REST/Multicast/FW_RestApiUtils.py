################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Indranil Acharya $
#
#    Copyright © 1997 - 2015 by IXIA
#    All Rights Reserved.
#
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
#    This contains required definitions for restAPI sample scripts             # 
#                                                                              #
################################################################################
# Needed for REST API
import time
#import requests
import json
import httplib2
from urllib import urlencode

import sys
import zipfile

class TestFailedError(Exception): pass

#######################################################
# Get the current url IxNetwork Sessions in a List form
# Ex usage: allSessions = getIxNetSessionsList(ixnetUrl)
#######################################################
def getIxNetSessionsList(ixnetUrl):
    try:
        sessionsUrl = ixnetUrl+"sessions"
        print "GET: " + sessionsUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests.get(sessionsUrl, headers=urlHeadersJson)
        responseList = response.json()
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    return responseList

#######################################################
# Get the current url IxNetwork Sessions in a requests form
# Ex usage: allSessions = getIxNetSessions(ixnetUrl)
#######################################################
def getIxNetSessions(ixnetUrl):
    print "[getIxNetSessions] + " + ixnetUrl
        
    try:
        h = httplib2.Http()
        sessionsUrl = ixnetUrl+"sessions"
        print "GET: " + sessionsUrl
        urlHeadersJson = {'content-type': 'application/json'}
        #response = requests.get(sessionsUrl, headers=urlHeadersJson)
        response, content = h.request(sessionsUrl,'GET','',urlHeadersJson)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(content.json()['errors'])
    return json.loads(content)
    

#######################################################
# Add new list to IxNetwork session, returns response in requests form
# Ex: addIxNetObjectFromSession(sessionUrl, "vport")
#######################################################
def addIxNetObjectFromSession(sessionUrl, obj, waitComplete=False):
    try:
        addPortUrl = sessionUrl + obj
        print "POST: " + addPortUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests.post(addPortUrl, headers=urlHeadersJson)
        if waitComplete:
            waitForComplete(sessionUrl, response)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    objLists = response.json()
    objUrl = sessionUrl.split("/api/v1/sessions/")[0] + objLists['links'][0]['href']
    return objUrl

#######################################################
# Add new list to IxNetwork session, returns the url of the object created
# Ex: addIxNetObject(sessionUrl, "vport", payload)
#######################################################
def addIxNetObject(inputUrl, obj, payload=None):
    try:
        h = httplib2.Http()
        rawUrl = inputUrl + "/" + obj
        print "POST: " + rawUrl
        urlHeadersJson = {'content-type': 'application/json'}
        if payload == None:
            response, content = h.request(rawUrl,'POST','',urlHeadersJson)
        else:
            response, content = h.request(rawUrl,'POST',json.dumps(payload),urlHeadersJson)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
        
    objLists = json.loads(content)
    objUrl =  inputUrl.split("/api/v1/sessions/")[0] + objLists['links'][0]['href']
    return objUrl

#######################################################
# ixNet delete objects/sessions/lists
# Ex: removeIxNetObject(deleteUrl)
#######################################################
def removeIxNetObject(deleteUrl):
    try:
        h = httplib2.Http()
        #response = requests.delete(deleteUrl)
        response, content = h.request(deleteUrl,'DELETE')
        print "DELETE: " + deleteUrl
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    return content

#######################################################
# Get ixnet ports, returns response in requests form
# Ex: aa = getIxNetPorts(ixnetUrl, 1)
#######################################################
def getIxNetPorts(sessionUrl):
    try:
        h = httplib2.Http()
        getPortsUrl = sessionUrl + "/vport"
        print "GET: " + getPortsUrl
        # response = requests.get(getPortsUrl)
        response, content = h.request(getPortsUrl,'GET')
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    return content

#######################################################
# Add new port to Ixnetwork session, returns response in requests form
# Ex: ixNetAddNewPort(ixnetUrl, 1)
#######################################################
def ixNetAddNewPort(sessionUrl):
    try:
        addPortUrl = sessionUrl+ "/vport"
        print "POST: " + addPortUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests.post(addPortUrl, headers=urlHeadersJson)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    return response

#######################################################
# ixNet help, returns response in requests form
# Ex: aa =  getIxNetHelp(ixnetUrl, 1, "/newConfig")
#######################################################
def getIxNetHelp(ixnetUrl, sessionId, urlObj):
    try:
        response = requests.options(ixnetUrl+"sessions/"+str(sessionId)+"/ixnetwork" + urlObj)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    return response


#######################################################
# ixNet exec with direct ulr added to obj session url
# Ex: aa =  ixNetDirectExec(ixnetUrl, 1, "quickTest/operations/apply")
#######################################################
def ixNetDirectExec(objUrl, execName, payload=None):
    try:
        h = httplib2.Http()
        urlString = objUrl + "/"+execName
        urlHeadersJson = {'content-type': 'application/json'}
        if payload == None:
            print "POST: " + urlString
            #response = requests.post(url=urlString, headers=urlHeadersJson)
            response, content = h.request(urlString,'POST','',urlHeadersJson)
        else:
            print "POST: " + urlString + "  <-- Payload: " + str(payload)
            # response = requests.post(url=urlString, headers=urlHeadersJson, data=json.dumps(payload))
            response, content = h.request(urlString,'POST',json.dumps(payload),urlHeadersJson)
        waitForComplete(objUrl, content)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    return content

#######################################################
# ixNet exec with no arguments, returns response in requests form
# Ex: aa =  ixNetExec(ixnetUrl, 1, "newConfig")
#######################################################
def ixNetExec(objUrl, execName, payload=None):
    try:
        h = httplib2.Http()
        urlString = objUrl + "/operations/"+execName
        urlHeadersJson = {'content-type': 'application/json'}
        if payload == None:
            print "POST: " + urlString
            #response = requests.post(url=urlString, headers=urlHeadersJson)
            response, content = h.request(urlString,'POST','',urlHeadersJson)
        else:
            print "POST: " + urlString + "  <-- Payload: " + str(payload)
            #response = requests.post(url=urlString, headers=urlHeadersJson, data=json.dumps(payload))
            response, content = h.request(urlString,'POST',json.dumps(payload),urlHeadersJson)
        waitForComplete(objUrl, content)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(response.json()['errors'])
    return content
    
#######################################################
# wait for the current operation to complete
# Ex: waitForComplete(sessionUrl, response)
#######################################################
def waitForComplete(sessionUrl, requestSess, timeout=180):
    a = json.loads(requestSess)
    for key in a:
       if "errors" in key:
            raise Exception('FAIL : need To Exit ',a["errors"])
    state = a["state"]
    url = a["url"]
    if state == "SUCCESS" and url == "":
        print "Exec is SUCCESS"
    elif state == "ERROR":
        raise Exception('FAIL : need To Exit ',a["result"])
    else:
        if state != "COMPLETED":
            print "WAIT FOR ACTION TO COMPLETE"
            url = a["url"].split("operations/")[1]
            print "Current state: " + state
            it = 0
            while state == "IN_PROGRESS":
                if timeout == it:
                    raise TestFailedError ("Operation is still in progress after : " + str(timeout) + " seconds")
                time.sleep(1)
                state = ixNetGetAtt(sessionUrl + "/operations/" + url, "state", False)
                print "Current state: " + state + " after " + str(it) + " seconds"
                it = it + 1


#######################################################
# ixNet assign ports
# Ex: ixNetAssignPorts(ixnetUrl, 1, py.ports)
#######################################################
# py.ports        = [('10.205.11.22', '3', '15'), ('10.205.11.22', '3', '16')]
def ixNetAssignPorts(sessionUrl, realPorts):
    try:
        h = httplib2.Http()
        print "Assign Multiple Ports at once"
        urlString = sessionUrl+ "/operations/assignports"
        urlHeadersJson = {'content-type': 'application/json'}
        sessionId = sessionUrl.split("sessions/")[1].split("/ixnet")[0]
        chassisPorts = realPorts
        # get the vports in current session
        vportIds = []
        vports = getIxNetPorts(sessionUrl)
        for v in json.loads(vports):
            vportIds.append(str(v['id']))
        realPortData = []
        vportData = []
        # create data and post foreach real port
        for vportId, rport in zip(vportIds, chassisPorts):
            chassis = rport[0]
            card = rport[1]
            port = rport[2]
            realPortData.append({'arg1': chassis, 'arg2': str(card), 'arg3': str(port)})
            vportData.append("/api/v1/sessions/"+str(sessionId)+"/ixnetwork/vport/" + str(vportId))
        # print "realPortData: " + str(realPortData)
        # print "vportData: " + str(vportData)
        datas = { "arg1": realPortData, \
                 "arg2": [], \
                 "arg3": vportData, \
                 "arg4": "true"}
        # print datas
        print "POST: " + urlString + " <--- DATA: " + str(datas)
        # response = requests.post(url=urlString, data=json.dumps(datas), headers=urlHeadersJson)
        
        response, content = h.request(urlString,'POST',json.dumps(datas),urlHeadersJson)
        # wait for COMPLETE
        waitForComplete(sessionUrl, content)
        print ""
    except Exception, e:
        raise TestFailedError (str(e))
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    print "Ports Assign Complete"

#######################################################
# ixNet assign ports
# Ex: ixNetAssignPort(ixnetUrl, 1, py.ports[0])
#######################################################
def ixNetAssignPort(sessionUrl, vportId, realPort):
    try:
        urlString = sessionUrl + "/operations/assignports"
        urlHeadersJson = {'content-type': 'application/json'}
        sessionId = sessionUrl.split("sessions/")[1].split("/ixnet")[0]
        chassis = realPort[0]
        card = realPort[1]
        port = realPort[2]
        dataJson = {    "arg1": [{"arg1": chassis, "arg2": card, "arg3": port}], \
                        "arg2": [], \
                        "arg3": ["/api/v1/sessions/"+str(sessionId)+"/ixnetwork/vport/" + str(vportId)], \
                        "arg4": "true"}
        print "POST: " + urlString + " <--- DATA: " + str(dataJson)
        response = requests.post(url=urlString, data=json.dumps(dataJson), headers=urlHeadersJson)
        waitForComplete(sessionUrl, response)
        return response
    except Exception, e:
        print str(e)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    print "Port Assign Complete"

#######################################################
# ixNet setAttribute
# Example:
#        attribute = {"name":"PortCreatedFromRest"}
#        aaa = ixNetSetAttFromSession(sessionUrl, "vport/1", attribute)
#        print aaa
#######################################################
def ixNetSetAttFromSession(sessionUrl, obj, att):
    try:
        h = httplib2.Http()
        urlString = sessionUrl + obj
        print "POST: " + urlString + " <-- Attribute: " + str(att)
        urlHeadersJson = {'content-type': 'application/json'}
        response, content = h.request(urlString,'PATCH',json.dumps(att),urlHeadersJson)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    return response

#######################################################
# ixNet setAttribute
# Example:
#        attribute = {"name":"PortCreatedFromRest"}
#        aaa = ixNetSetAtt(urlString, attribute)
#        print aaa
#######################################################
def ixNetSetAtt(urlString, att):
    try:
        h = httplib2.Http()
        print "PATCH: " + urlString + " <-- Attribute: " + str(att)
        urlHeadersJson = {'content-type': 'application/json'}
        response, content = h.request(urlString,'PATCH',json.dumps(att),urlHeadersJson)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    return response

#######################################################
# ixNet checkAttribute
# Example:
#        attribute = {"name":"PortCreatedFromRest"}
#        ixNetCheckAtt(urlString, attribute)
#######################################################
def ixNetCheckAtt(urlString, atts):
    try:
        h = httplib2.Http()
        print "GET: " + urlString + " <-- Attributes to check: " + str(atts)
        urlHeadersJson = {'content-type': 'application/json'}
        # response = requests.get(url=urlString, headers=urlHeadersJson)
        response, content = h.request(urlString,'GET','',urlHeadersJson)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    reqAtt = json.loads(content)
    
    for attrib in atts:
        if str(reqAtt[attrib]).lower() != str(atts[attrib]).lower():
            raise TestFailedError("Attribute was not set correctly: "  + attrib + "=" + reqAtt[attrib] + ", should be: " + atts[attrib])
    print "All Attributes set correctly"

#######################################################
# ixNet getA method, return result in text mode
# aa = ixNetGetAttFromSession(sessionUrl, "vport/1", "name")
#######################################################
def ixNetGetAttFromSession(sessionUrl, obj, att ):
    try:
        h = httplib2.Http()
        getAttUrl = sessionUrl + obj
        print "GET: " + getAttUrl
        response, content = h.request(getAttUrl,'GET')
        res = json.loads(content)
        return res[att]
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    return res[att]

#######################################################
# ixNet getA method for raw url, return result in text mode
# aa = ixNetGetAtt(getAttUrl, "name")
#######################################################
def ixNetGetAtt(getAttUrl, att, logging=True ):
    try:
        h = httplib2.Http()
        if logging:
            print "GET: " + getAttUrl
        #response = requests.get(getAttUrl)
        response, content = h.request(getAttUrl,'GET')
        res = json.loads(content)
        # return res[att]
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    attUrl = res[att]
    return attUrl
    

#######################################################
# ixNet get List in requests form
# aa = ixNetGetList(ixNetSessionUrl, "vport")
#######################################################
def ixNetGetList(ixNetSessionUrl, list):
    try:
        listUrl = ixNetSessionUrl + "/" + list
        print "GET: " + listUrl
        response = requests.get(listUrl)
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    return response

#######################################################
# ixNet get att by using the list position
# aa = getAttByListPos(vports, 0, "id")
#######################################################
def getAttByListPos(jsonObj, pos, attName):
    list = jsonObj.json()
    if len(list) < pos:
        raise TestFailedError("The json object list is shorter than desired pos")
    if len(list) > 0:
        return list[pos][attName]
    else:
        raise TestFailedError("The json object list is 0")

#######################################################
# ixNet get all ports in requests form
# aa = getVports(ixNetSessionUrl)
#######################################################
def getVports(ixNetSessionUrl):
    try:
        portsUrl = ixNetSessionUrl + "/vport"
        print "GET: " + portsUrl
        response = requests.get(portsUrl)
        res = response.json()
        # return res[att]
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if not response.ok:
        raise TestFailedError(response.text)
    if "[200]" not in str(response):
        raise TestFailedError(response.json()['errors'])
    return response

#######################################################
# ixNet getA method for raw url, return result in text mode
# aa = ixNetGetAttUrl(getAttUrl, "name")
#######################################################
def ixNetGetAttUrl(getAttUrl, att ):
    try:
        h = httplib2.Http()
        print "GET: " + getAttUrl
        # response = requests.get(getAttUrl)
        response, content = h.request(getAttUrl,'GET')
        res = json.loads(content)
        # return res[att]
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    attUrl = getAttUrl.split("/api/v1/")[0] + res[att]
    return attUrl

#######################################################
# get the Url from a multivalue url for a specific pattern
# a = getMultiValueFromUrl(baseUrl, "counter")
#######################################################
def getMultiValueFromUrl(baseUrl, pattern):
    try:
        h = httplib2.Http()
        print "GET: " + baseUrl
        ixnetUrl = baseUrl.split("/api/v1/")[0]
        # response = requests.get(baseUrl)
        response, content = h.request(baseUrl,'GET')
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if response.status != 200 :
        raise TestFailedError(json.loads(content)['errors'])
    links = json.loads(content)
    for link in links["links"]:
        lhref = link["href"]
        if pattern in lhref:
            retUrl = ixnetUrl + lhref
            print retUrl
            return retUrl

#######################################################
# Returns the session url of ixnetwork instance
# Example:
#        sessionUrl = getIxNetSessionUrl(ixnetUrl, sessionId)
#######################################################
def getIxNetSessionUrl(ixnetUrl, sessionId):
    return ixnetUrl+"sessions/"+str(sessionId)+"/ixnetwork"

#######################################################
# Returns the full url using ixNet url and rest port
# Example:
#        sessionUrl = getIxNetSessionUrl(ixnetUrl, sessionId)
#######################################################
def fixUrl(clientIP, clientRestPort, url):
    return "http://" + str(clientIP) + ":" + str(clientRestPort) + url

#######################################################
# Returns the Attribute from an existing request response
# Example:
#        att = getAttFromResponse(response, "url")
#######################################################
def getAttFromResponse(response, att):
    return response.json()[att]

#######################################################
# ixNet exec loadConfig
# Example:
#        configName = "config.configName.ixncfg"
#        ixNetLoadConfig(ixNetSessionUrl, configName)
#####################################################
def ixNetLoadConfig(ixNetSessionUrl, configName):
    import requests
    urlHeadersJson = {'content-type': 'application/json'}
    print "Uploading IxNetwork config to server"

    # read the config as binary
    with open(configName, mode='rb') as file:
        configContent = file.read()

    # get the file name
    if '\\' in configName:
        configName = configName.split('\\')[-1]

    uploadUrl = ixNetSessionUrl + "/files/"+ configName

    urlHeadersData = {'content-type': 'application/octet-stream','content-length': len(configContent)}

    # send the config to server files location
    r = requests.post(uploadUrl, headers=urlHeadersData, data=configContent)

    if configName in r.text:
        print "IxNetwork config uploaded Correctly, now loading the config"
        dataJson = {'filename': configName}
        loadConfigUrl = ixNetSessionUrl + '/operations/loadConfig'
        r = requests.post(url=loadConfigUrl, data=json.dumps(dataJson), headers=urlHeadersJson)
        responseCode = str(r)
        if "Response [200]" not in responseCode:
            print r.text
            return False
        else:
            return True
        waitForComplete(ixNetSessionUrl, r)
    else:
        print "Config Not uploaded correctly to server"
        return False

#######################################################
# Protocols specific stuff
#####################################################
class RestProtocols:

    @staticmethod
    def waitForUpCount(getAttUrl, **kwargs):
        # ixNetGetAtt(getAttUrl, att )
        if kwargs:
            if 'upCount' in kwargs: totalCount = kwargs['upCount']
            else: totalCount = len(ixNetGetAtt(getAttUrl, "sessionStatus" ))
            if 'timeout' in kwargs: timeout = kwargs['timeout']
            else: timeout = 90
        else:
            timeout = 90
            totalCount = len(ixNetGetAtt(getAttUrl, "sessionStatus" ))
        print "--- Wait for all sessions to become Up for maximum: " + str(timeout) + " seconds"
        it = 0
        while it < timeout:
            upCount = 0
            sessionStatus = ixNetGetAtt(getAttUrl, "sessionStatus" )
            for status in sessionStatus:
                if status == "up":
                    upCount = upCount + 1
            if upCount == totalCount:
                print "Reached " + str(upCount) + " sessions in: " + str(it) + " seconds"
                break
            else:
                print "Still not " + str(upCount) + " sessions Up after " + str(it) + " seconds"
                it = it + 1
                time.sleep(1)

    @staticmethod
    def setDeviceGroupMultiplier(dgUrl, multiplier):
        print "Set the DG multiplier to " + str(multiplier) + " for " + dgUrl
        attributes = {"multiplier": multiplier}
        ixNetSetAtt(dgUrl, attributes)

class RestTraffic:

    @staticmethod
    def generateTrafficItem(sessionUrl, trafficItem):
        print "-- Generate the traffic item"
        trafficUrl = sessionUrl+"/traffic"
        trafficAtt = {"arg1":trafficItem}
        result = ixNetExec(sessionUrl,"generate", trafficAtt)
        # result = ixNetExec(trafficItem,"generate")
        print result

    @staticmethod
    def setTrafficRegenerate(sessionUrl):
        print "-- Set the Regenerate Learned Info Before Apply for traffic"
        trafficURL = sessionUrl+"/traffic"
        trafficAtt = {"refreshLearnedInfoBeforeApply":"true"}
        ixNetSetAtt(trafficURL, trafficAtt)

    @staticmethod
    def applyAndStartTraffic(sessionUrl):
        trafficUrl = sessionUrl+"/traffic"
        print "-- Apply the traffic"
        trafficAtt = {"arg1":trafficUrl}
        result = ixNetExec(trafficUrl,"apply", trafficAtt)
        print result
        print "-- Start the traffic"
        ixNetExec(trafficUrl,"start",trafficAtt)

    @staticmethod
    def waitTrafficState ( sessionUrl ,state, timeout=60 ) :
        availableStates = { "locked" ,"started" ,"startedWaitingForStats" ,"startedWaitingForStreams" ,"stopped" ,"stoppedWaitingForStats", "txStopWatchExpected", "unapplied"}

        if state not in availableStates :
            print "Please use any of the available state: $availableStates"
            return 1

        print "- Waiting for maximum "+ str(timeout)+" seconds for traffic to be in "+ str(state)+" state..."
        i = 0
        newState = ixNetGetAtt(sessionUrl + "/traffic", "state", False)
        while (newState != state and i < timeout) :
            time.sleep(1)
            i = i + 1
            print str(i) + ", state : " + str(newState)
            newState = ixNetGetAtt(sessionUrl + "/traffic", "state",False)

        if i == timeout :
            print "Traffic wasn't in "+str(state)+" state after "+str(i)+" seconds of waiting."
            return 1
        else:
            print "Traffic is in "+str(state)+" state. ("+str(i)+" sec)"
            return 0



class RestQuickTest:

    @staticmethod
    def applyQT(qtTypeUrl, testUrl):
        print "-- Apply the QuickTest"
        qtUrl = qtTypeUrl
        qtAtt = {"arg1":testUrl}
        result = ixNetDirectExec(qtTypeUrl, "quickTest/operations/apply", qtAtt)
        print result

    @staticmethod
    def startQT(sessionUrl, tesName=None):
        print "-- Start the QuickTest"
        qtUrl = sessionUrl
        if tesName ==None:
            result = ixNetExec(sessionUrl, "startTestConfiguration")
        else:
            qtAtt = {"arg1":tesName}
            result = ixNetExec(sessionUrl, "startTestConfiguration", qtAtt)
        print result

    @staticmethod
    def checkProgress(testUrl, timeout=90):
        print "-- Check the QT Progress"
        progress = ixNetGetAtt(testUrl + "/results", "progress")
        isRunning = ixNetGetAtt(testUrl + "/results", "isRunning")
        it = 0
        print "Check the isRunning status every 10 seconds"
        while it < timeout:
            time.sleep(10)
            it = it + 1
            progress = ixNetGetAtt(testUrl + "/results", "progress", False)
            isRunning = ixNetGetAtt(testUrl + "/results", "isRunning", False)
            if isRunning == "true":
                print "Progress Check : " + str(it) + "/" + str(timeout) + " progress: " + progress
            else:
                print "Progress Check : " + str(it) + "/" + str(timeout) + " COMPLETE"
                break
            # print "Iteration : " + str(it) + " isRunning: " + isRunning

    @staticmethod
    def getTestResult(testUrl, timeout=90):
        print "-- Check QT Result"
        result = ixNetGetAtt(testUrl + "/results", "result")
        print "QT Result is: " + result
        return result

    @staticmethod
    def createTest(sessionUrl, qtType, trafficType):
        print "-- Create QuickTest"
        qtAtt = {"arg1":"/timeline", "arg2":qtType, "arg3":trafficType }
        result = ixNetDirectExec(sessionUrl, "timeline/operations/createTest", qtAtt)
        # print result
        return result

    @staticmethod
    def getQTBasedOnTimeLine(sessionUrl, timeLineUrl):
        print "-- Get QT ID based on the timeline"
        timeLines = ixNetGetList(sessionUrl + "/timeline", "test")
        timeLines = timeLines.json()
        for timeLine in timeLines:
            if timeLineUrl in str(timeLine["links"]):
                splitChar = "/api/v1/sessions"
                qt = timeLine["quickTestId"].split(splitChar)[1]
                baseUrl = sessionUrl.split(splitChar)[0]
                qtFullUrl = baseUrl + splitChar + qt
                return qtFullUrl
                # return timeLine["quickTestId"]
        raise TestFailedError("Specified timeLine URL was not found, timeLineUrl:" + timeLineUrl)

