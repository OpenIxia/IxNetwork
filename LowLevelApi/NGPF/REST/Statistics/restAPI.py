################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


# Needed for REST API
import time
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import sys
import zipfile

class TestFailedError(Exception): pass
class returnItem():
    def __init__(self,res):
	    self.responseString = res
    def json(self,):
        return json.loads(self.responseString)

class requests():
    def __init__(self,):pass
    
    def get(self,sessionsUrl):
        request = urllib2.Request(sessionsUrl)
        request.get_method = lambda: 'GET'
        return returnItem(urllib2.urlopen(request).read())
	
    def post(self,sessionsUrl,data=None):
        request = urllib2.Request(sessionsUrl)
        request.get_method = lambda: 'POST'
        if data==None:return urllib2.urlopen(request).read()
        else:return returnItem(urllib2.urlopen(request,data).read())
	
    def patch(self,sessionsUrl,data):
        request = urllib2.Request(sessionsUrl)
        request.get_method = lambda: 'PATCH'
        return returnItem(urllib2.urlopen(request,data).read())

    def options(self,sessionsUrl):
        request = urllib2.Request(sessionsUrl)
        request.get_method = lambda: 'OPTIONS'
        return returnItem(urllib2.urlopen(request).read())
		
    def delete(self,sessionsUrl):
        request = urllib2.Request(sessionsUrl)
        request.get_method = lambda: 'DELETE'
        return returnItem(urllib2.urlopen(request).read())
	
#######################################################
# Get the current url IxNetwork Sessions in a List form
# Ex usage: allSessions = getIxNetSessionsList(ixnetUrl)
#######################################################
def getIxNetSessionsList(ixnetUrl):
    try:
        sessionsUrl = ixnetUrl+"sessions"
        print "GET: " + sessionsUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests().get(sessionsUrl)
        responseList = json.loads(response)
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return responseList

#######################################################
# Get the current url IxNetwork Sessions in a requests form
# Ex usage: allSessions = getIxNetSessions(ixnetUrl)
#######################################################
def getIxNetSessions(ixnetUrl):
    try:
        sessionsUrl = ixnetUrl+"sessions"
        print "GET: " + sessionsUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests().get(sessionsUrl)
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response

#######################################################
# Add new list to IxNetwork session, returns response in requests form
# Ex: addIxNetObject(sessionUrl, "vport")
#######################################################
def addIxNetObject(sessionUrl, obj):
    try:
        addPortUrl = sessionUrl + obj
        print "POST: " + addPortUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests().post(addPortUrl)
        checkForComplete(sessionUrl, response)
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response

#######################################################
# ixNet delete objects/sessions/lists
# Ex: removeIxNetObject(ixnetUrl, 1, "vport/1")
#######################################################
def removeIxNetObject(sessionUrl, obj):
    try:
        deleteUrl = sessionUrl + obj
        response = requests().delete(deleteUrl)
        print "DELETE: " + deleteUrl
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response

#######################################################
# Get ixnet ports, returns response in requests form
# Ex: aa = getIxNetPorts(ixnetUrl, 1)
#######################################################

def getIxNetPorts(sessionUrl):
    try:
        getPortsUrl = sessionUrl + "vport"
        response = requests().get(getPortsUrl)
        print "GET: " + getPortsUrl
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response  

#######################################################
# Add new port to Ixnetwork session, returns response in requests form
# Ex: ixNetAddNewPort(ixnetUrl, 1)
#######################################################
def ixNetAddNewPort(sessionUrl):
    try:
        addPortUrl = sessionUrl+ "vport"
        print "POST: " + addPortUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests().post(addPortUrl)
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response

#######################################################
# ixNet help, returns response in requests form
# Ex: aa =  getIxNetHelp(ixnetUrl, 1, "/newConfig")
#######################################################
def getIxNetHelp(ixnetUrl, sessionId, urlObj):
    try:
        response = requests().option(ixnetUrl+"sessions/"+str(sessionId)+"/ixnetwork" + urlObj)
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response



#######################################################
# ixNet exec with no arguments, returns response in requests form
# Ex: aa =  ixNetExec(ixnetUrl, 1, "newConfig")
#######################################################
def ixNetExec(objUrl, execName, payload=None):
    try:
        stateURL_ = objUrl + "/operations/"+execName
        _stateURL=stateURL_.replace('//','/')
        urlString=_stateURL.replace('http:/','http://')
        urlHeadersJson = {'content-type': 'application/json'}
        if payload == None:
            print "POST: " + urlString
            response = requests().post(urlString)
        else: 
            print "POST: " + urlString + "  <-- Payload: " + str(payload)
            response = requests().post(urlString,json.dumps(payload))
        a = json.loads(response)
        print '------',type(a)
        if a["id"]!="":waitForComplete(objUrl, response)
        else : return response
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    return response

#######################################################
# wait for the current operation to complete
# Ex: waitForComplete(sessionUrl, response)
#######################################################
def waitForComplete(sessionUrl, requestSess, timeout=120):
    a = json.loads(requestSess)
    for key in a:
       if "errors" in key:
            raise Exception('FAIL : need To Exit ',a["errors"])
    state = a["state"]
    if state != "COMPLETED":
        print "WAIT FOR ACTION TO COMPLETE"
        url = a["url"].split("operations/")[1]
        print "Current state: " + state
        it = 0
        while state == "IN_PROGRESS":
            if timeout == it:
                raise TestFailedError ("Operation is still in progress after : " + str(timeout) + " seconds")
            time.sleep(1)
            stateURL_=sessionUrl + "operations/" + url
            _stateURL=stateURL_.replace('//','/')
            stateURL=_stateURL.replace('http:/','http://')
            state = ixNetGetAtt(stateURL, "state", False)
            print "Current state: " + state + " after " + str(it) + " seconds"
            it = it + 1
    if state == "ERROR": raise TestFailedError('FAIL : process did not went to Completed state')
#######################################################
# wait for the current operation to complete
# Ex: waitForComplete(sessionUrl, response)
#######################################################
def checkForComplete(sessionUrl, requestSess, timeout=90):
    print "WAIT FOR ACTION TO COMPLETE"
    if str(200) not in str(requestSess): 
        print "Retrieved :",str(requestSess)
        raise Exception("FAIL")
    a = json.loads(requestSess)
    print 'The newly created object is :',a.get('links')[0].get('href')
    

#######################################################
# ixNet assign ports
# Ex: ixNetAssignPorts(ixnetUrl, 1, py.ports)
#######################################################
# py.ports        = [('10.205.11.22', '3', '15'), ('10.205.11.22', '3', '16')]
def ixNetAssignPorts(sessionUrl, realPorts):
    try:
        print "Assign Multiple Ports at once"
        urlString = sessionUrl+ "operations/assignports"
        urlHeadersJson = {'content-type': 'application/json'}
        sessionId = sessionUrl.split("sessions/")[1].split("/ixnet")[0]
        chassisPorts = realPorts
        # get the vports in current session
        vportIds = []
        vports = getIxNetPorts(sessionUrl)
        for v in json.loads(vports):
            vportIds.append(str(v['id']))
        datas = []
        portIds = []
        # create data and post foreach real port
        for vport, rport in zip(vportIds, chassisPorts):
            chassis = rport[0]
            card = rport[1]
            port = rport[2]
            portid = vport
            # data = { "arg1": [{"arg1": chassis, "arg2": str(card), "arg3": str(port)}], \
                     # "arg2": [], \
                     # "arg3": ["/api/v1/sessions/"+str(sessionId)+"/ixnetwork/vport/" + str(portid)], \
                     # "arg4": "true"}
            # print data
            data = {"arg1": chassis, "arg2": str(card), "arg3": str(port)}
            portIds.append(sessionUrl+'vport/'+portid)
            datas.append(data)
        payload = {'arg1': datas, 'arg2': [], 'arg3': portIds, 'arg4': True} 
        print "POST: " + urlString + " <--- DATA: " + str(payload)
        response = requests().post(urlString, json.dumps(payload))
        # print response.text
        waitForComplete(sessionUrl, response)
        print ""
    except Exception, e:
        print str(e)
    return response    
#######################################################
# Add new list to IxNetwork session, returns the url of the object created
# Ex: deleteIxNetObject(sessionUrl, "vport", payload)
#######################################################
def deleteIxNetObject(inputUrl, obj, payload=None):
    print json.dumps(payload)
    try:
        rawUrl = inputUrl + "/" + obj
        print "DELETE: " + rawUrl
        urlHeadersJson = {'content-type': 'application/json'}
        if payload == None:
            response = requests().delete(rawUrl)
        else:
            response = requests().delete(rawUrl, json.dumps(payload))
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    if "[200]" not in str(response):
        raise TestFailedError(json.loads(response)['errors'])
#######################################################
# ixNet assign ports
# Ex: ixNetAssignPort(ixnetUrl, 1, py.ports[0])
#######################################################
def ixNetAssignPort(sessionUrl, vportId, realPort):
    try:
        urlString = sessionUrl + "operations/assignports"
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
        response = requests().post(urlString, json.dumps(dataJson))
        waitForComplete(sessionUrl, response)
        return response
    except Exception, e:
        print str(e)
    return response    

#######################################################
# ixNet setAttribute 
# Example: 
#        attribute = {"name":"PortCreatedFromRest"}
#        aaa = ixNetSetAtt(ixnetUrl, 1, "vport/1", attribute)
#        print aaa
#######################################################
def ixNetSetAtt(urlString, att):
    try:
        print "PATCH: " + urlString + " <-- Attribute: " + str(att)
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests().patch(urlString, json.dumps(att))
    except Exception, e:
        raise Exception('Got an error code: ', e)
    if "[200]" not in str(response):
        raise TestFailedError(json.loads(response)['errors'])
    return response


#######################################################
# ixNet getA method, return result in text mode
# aa = ixNetGetAtt(ixnetUrl,1,"vport/1", "name")
#######################################################
def ixNetGetAtt(getAttUrl, att, logging=True ):
    try:
        if logging:
            print "GET: " + getAttUrl
        response = requests().get(getAttUrl)
        res = json.loads(response)
        # return res[att]
    except Exception, e:
        raise Exception('Got an error code: ', e)  
#    if "[200]" not in str(response):
#        raise TestFailedError(json.loads(response)['errors'])
    attUrl = res[att]
    return attUrl

#######################################################
# Returns the session url of ixnetwork instance
# Example: 
#        sessionUrl = getIxNetSessionUrl(ixnetUrl, sessionId)
#######################################################
def getIxNetSessionUrl(ixnetUrl, sessionId):
    return ixnetUrl+"sessions/"+str(sessionId)+"/ixnetwork/"


#######################################################
# ixNet exec loadConfig 
# Example: 
#        configName = "config.configName.ixncfg"
#        ixNetLoadConfig(ixNetSessionUrl, configName)
#####################################################
def ixNetLoadConfig(ixNetSessionUrl, configName):
    urlHeadersJson = {'content-type': 'application/json'}
    urlHeadersData = {'content-type': 'application/octet-stream'}
    print "Uploading IxNetwork config to server"
    uploadUrl = ixNetSessionUrl + "files/"+ configName
	# read the config as binary
    with open(configName, mode='rb') as file:
        configContent = file.read()
	# send the config to server files location
    r = requests().post(uploadUrl,  configContent)
    if configName in r: 
        print "IxNetwork config uploaded Correctly, now loading the config"
        dataJson = {'filename': configName}
        loadConfigUrl = ixNetSessionUrl + '/operations/loadConfig'
        r = requests().post(loadConfigUrl, json.dumps(dataJson))
        responseCode = str(r)
        if "Response [200]" not in responseCode:
            print r
            return False
        else: 
            return True
        waitForComplete(ixNetSessionUrl, r)
    else:
        print "Config Not uploaded correctly to server"
        return False
##############################################################
# Retrieve Stats
# Example:
#         ixNetGetStats(ixNetSessionUrl, "Protocols Summary",\
#       	["Sessions Up","Sessions Total","Sessions Down"])
##############################################################
def ixNetGetStats(ixNetSessionUrl, viewname,colList):
    dict_data={}
    urlHeadersJson = {'content-type': 'application/json'}
    urlHeadersData = {'content-type': 'application/octet-stream'}
    getUrl = ixNetSessionUrl + "statistics/view/"
    print "GET: " + getUrl
    response = requests().get(getUrl)
    res = json.loads(response)
    for view in res:
        if str(view.get('caption'))==str(viewname):
            print 'Checking for the stat  : ',viewname
            view_id = str(view.get('id'))
            #print 'view_id is :',view_id
            break
        else:continue
    if view_id == "" :print "FAIL - need to exit the caption ",viewname," does not exists "
    print "GET: " + getUrl+view_id+'/page/'
    page = requests().get(getUrl+view_id+'/page/')
    p = json.loads(page)
    #statValue = p.get('pageValues')
    statValue = p.get('rowValues').get('arg1')[0]
    statCap = p.get('columnCaptions')
    print '--Validating for ',statCap[0],'----> ',statValue[0]
    for cap,val in zip(statCap, statValue):
        if cap in colList:
            print cap,'::',val
            dict_data.update({cap:val,})
    return dict_data
##############################################################
# Retrieve Stat : similer to the above slight modifications
# Example:
#         ixNetGetStat(ixNetSessionUrl, "Protocols Summary",\
#       	["Sessions Up","Sessions Total","Sessions Down"])
##############################################################
def ixNetGetStat(ixNetSessionUrl, viewname,colList,timeout=90):
    dict_data={}
    dict_dataFinal={}
    urlHeadersJson = {'content-type': 'application/json'}
    urlHeadersData = {'content-type': 'application/octet-stream'}
    getUrl = ixNetSessionUrl + "statistics/view/"
    print "GET: " + getUrl
    response = requests().get(getUrl)
    res = json.loads(response)
    for view in res:
        if str(view.get('caption'))==str(viewname):
            print 'Checking for the stat  : ',viewname
            view_id = str(view.get('id'))
            break
        else:continue
    if view_id == "" :print "FAIL - need to exit the caption ",viewname," does not exists "
    print "GET: " + getUrl+view_id+'/page/'
    page = requests().get(getUrl+view_id+'/page/')
    p = json.loads(page)
    trial = 0
    print getUrl+view_id+'/page/ -isReady = ',p["isReady"]
    print '----------------- This 1 - p',p
    while str(p["isReady"])!=str("True"):
        p = json.loads(requests().get(getUrl+view_id+'/page/'))
        print '------------ This 2',p["isReady"]
        print getUrl+view_id+'/page/ -isReady = ',p["isReady"]
        time.sleep(1)
        trial+=1
        if trial==timeout:
            print 'FAIL- View is not reday !! waited for :'+trial+' seconds'
            raise Exception('View is not Ready !!')
    statValueList = p.get('rowValues').get('arg1')
    statCap = p.get('columnCaptions')
    for statValue in statValueList:
        print '---------Validating for ',statCap[0],'----> ',statValue[0]
        for cap,val in zip(statCap, statValue):
            if cap in colList:
                print cap,'::',val
                dict_data.update({cap:val,})
		dict_dataFinal.update({statValue[0]:dict_data},)
    return dict_dataFinal
##############################################################
# verifyStatsForUP
# Example:
#         verifyStatsForUP()	
##############################################################
def verifyStatsForUP(ixNetSessionUrl):
    viewList = ["Sessions Up","Sessions Total","Sessions Down"]
    data = ixNetGetStat(ixNetSessionUrl, "Protocols Summary",viewList)
    for key, value in data.iteritems():
	    if str(value["Sessions Total"])!=str(value["Sessions Up"]):
		    raise Exception("FAIL - Expected Session Total=Session Up :: Retrieved :: Sessions Total : ",value["Sessions Total"],"!=Session Up :",value["Sessions Up"])
    return True
##############################################################
# fetchLearnedInfo
# Example:
#         fetchLearnedInfo(ixNetSessionUrl)	
##############################################################
def fetchLearnedInfo(ixNetSessionUrl,opr_type='getlearnedinfo',itemlist=[1,2]):
    dict_data={}
    dict_dataFinal={}
    try:
        print "GET: " + ixNetSessionUrl
        urlHeadersJson = {'content-type': 'application/json'}
        response = requests().get(ixNetSessionUrl)
    except Exception, e:
        raise Exception('Got an error code: ', e)  
    res = json.loads(response)
    #node=res["links"][-1]["href"]
    node=ixNetSessionUrl
    for item in itemlist:
        data ={"arg1":[node],"arg2" :[item]}
        ixNetExec(ixNetSessionUrl,opr_type,data)
    learnedInfoURL=ixNetSessionUrl+'/learnedInfo'
    print "GET: " + learnedInfoURL
    response = requests().get(learnedInfoURL)
    res = json.loads(response)
    for learnedinfo in res:
        print "---Checking the Learned Info for the node -- ",learnedinfo["__id__"][-1]
        for valuesList in learnedinfo["values"]:
            for name,val in zip(learnedinfo["columns"],valuesList):
                dict_data.update({name:val,})
                print name,"=",val
            dict_dataFinal.update({learnedinfo["__id__"][-1]:dict_data},)
    return dict_dataFinal

     
#        for key, value in learnedinfo.iteritems():
#      	    print key,value  
#	    if str(value["Sessions Total"])!=str(value["Sessions Up"]):
#		    raise Exception("FAIL - Expected Session Total=Session Up :: Retrieved :: Sessions Total : ",value["Sessions Total"],"!=Session Up :",value["Sessions Up"])
#    return True
##############################################################
# verifyStateForUP
# Example: ixNetSessionUrl_ipv4 =  ixNetSessionUrl+'topology/1/deviceGroup/1/ethernet/1/ipv4/'
#         verifyStateForUP(ixNetSessionUrl_ipv4,"1")	
##############################################################
def verifyStateForUP(ixNetSessionUrl):
    att_Status = 'sessionStatus'
    att_statCount ='stateCounts'
    att_count = 'count'
    data_Status = ixNetGetAtt(ixNetSessionUrl, att_Status )
    data_statCount = ixNetGetAtt(ixNetSessionUrl, att_statCount )
    data_count = ixNetGetAtt(ixNetSessionUrl, att_count )
    print data_Status,data_statCount,data_count
    if data_Status.count('up')!=data_count or data_Status.count('up')!=data_statCount["arg4"]:
        raise Exception("FAIL -- Not all sessions are UP data_count,data_statCount,data_Status -> ",data_count,data_statCount,data_Status)
    return True
	
################################################################################
# Procedure : generateApplyStartTraffic
# Purpose   : To Generate and Apply Traffic
# Example   : generateApplyStartTraffic(ixNetSessionUrl,refreshBeforeApply=False,timeOut=90)
################################################################################
def generateApplyStartTraffic(ixNetSessionUrl,refreshBeforeApply=False,timeOut=90):
    print "Generate Apply Start Traffic..."
    error = 0
    urlHeadersJson = {'content-type': 'application/json'}
    trafficURL = ixNetSessionUrl+"traffic/"
    print "Set refreshLearnedInfoBeforeApply for Traffic to %s" % (str(refreshBeforeApply),)
    if refreshBeforeApply:
        if setAndCheckAttributeValue(trafficURL,"refreshLearnedInfoBeforeApply", 'true'):return 1
    else:
        if setAndCheckAttributeValue(trafficURL,"refreshLearnedInfoBeforeApply", 'false'):return 1
    # Apply Traffic
    print "Applying the traffic ...."
    response = requests().get(trafficURL)
    res = json.loads(response)
    node=res["links"][-1]["href"]
    data ={"arg1":node}
    ixNetExec(trafficURL,"apply",data)
    print "Starting the traffic..."
    data ={"arg1":[node]}
    ixNetExec(trafficURL,"startStatelessTraffic",data)
    print "SUCCESS:Generate Apply Start Traffic..."
    return 0
	
################################################################################
# Procedure : setAndCheckAttributeValue
# Purpose   : set and verify the value
# Example   : setAndCheckAttributeValue(ixNetSessionUrl,attr,value)
#			: setAndCheckAttributeValue(trafficURL,"refreshLearnedInfoBeforeApply",'false')
################################################################################
def setAndCheckAttributeValue(ixNetSessionUrl,attr,value):
    print "Verifying for the node :",ixNetSessionUrl
    isError = 1
    retVal  = str(value.lower())
    setVal = {attr:value}
    try:
        ixNetSetAtt(ixNetSessionUrl,setVal)
    except Exception,e:
        print "Error while setting %s node attribute %s value %s" %(ixNetSessionUrl,attr,value)
        print str(e)
        return isError
    retAttrVal = str(ixNetGetAtt(ixNetSessionUrl,attr))
    if retVal!=str(retAttrVal.lower()):
        print "FAIL:getAttribute value (%s) does not match with expected value (%s)" % (retAttrVal,retVal)
        return isError		
    return 0
##############################################################
# Drilldown Stats : similer to the above slight modifications
# Example:
#         ixNetGetStat(ixNetSessionUrl, "Protocols Summary",\
#       	["Sessions Up","Sessions Total","Sessions Down"])
##############################################################
def Drilldown(ixNetSessionUrl, viewname,drill_down_option,drill_down_agg="0"):
    dict_data={}
    dict_dataFinal={}
    urlHeadersJson = {'content-type': 'application/json'}
    urlHeadersData = {'content-type': 'application/octet-stream'}
    getUrl = ixNetSessionUrl + "statistics/view/"
    print "GET: " + getUrl
    response = requests().get(getUrl)
    res = json.loads(response)
    for view in res:
        if str(view.get('caption'))==str(viewname):
            print 'Checking for the stat  : ',viewname
            view_id = str(view.get('id'))
            break
        else:continue
    if view_id == "" :print "FAIL - need to exit the caption ",viewname," does not exists "
    print "Performing drill down for the ",drill_down_option," Drill Down view"
    drillDown = getUrl+view_id+'/drillDown/'
    setAndCheckAttributeValue(drillDown,"targetDrillDownOption",drill_down_option)
    setAndCheckAttributeValue(drillDown,"targetRowIndex",drill_down_agg)
    data ={"arg1":ixNetSessionUrl+'/statistics/view/'+view_id+'/drillDown'}
    ixNetExec(drillDown,"doDrillDown",data)
