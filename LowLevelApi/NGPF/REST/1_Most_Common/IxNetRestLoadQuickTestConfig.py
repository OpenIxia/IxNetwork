#!/usr/local/python2.7.6/bin/python2.7

# By Hubert Gee
# June 20,2016
#
# Requirement:
# ------------
#    IxNetwork 8.0
# 
# Description:
# ------------
#
#    Using REST API to connect to an existing Quick Test configuration.
#    If the variable userSelectQuickTestList is 'all', then execute all
#    the configured Quick Tests. Else, execute the list provided by 
#    the user from the commandline. 
#
#    Each Quick Test will retrieve its AggregateResults.csv file and 
#    includes a timestamp on it.
#
# Usage:
# ------
# 
#    Enter: python IxNetRestLoadQuickTestConfig.py -help
#

import time
import requests
import json
import httplib
import sys
import pprint
import re
import datetime
import os

# Set parameters with default values
class configs():
    #ixNetworkApiServer = '10.219.117.103'
    ixNetworkApiServer = '192.168.70.127'
    ixNetworkPort = '8009'
    userSelectQuickTestList = 'all'
    copyResultFileToLocalLinuxPath = '/home/hgee'
    quickTestCsvResultFile = 'AggregateResults.csv'
    quickTestConfigFile = '/home/hgee/Dropbox/MyIxiaWork/Temp/QuickTest_vm8.20.ixncfg'

debug=1

class TestFailedError(Exception): pass

class IxNet:
	def __init__(self,server,port,version='v1'):
		self.urlHeadersJson = {'content-type': 'application/json'}
		self.urlHeadersData = {'content-type': 'application/octet-stream'}
		self.server = server
		self.port = port
		self.version=version
		self.baseUrl = "http://%s:%s/api/%s" % (server,str(port),version)
		self.srvUrl = "http://%s:%s" % (self.server,self.port)
		self.sessionId=None
		self.response = None

	def connect(self,timeout=60):
		#http = httplib.HTTPConnection(self.server+":"+str(self.port))
		res = self.getIxNetSessions()
		self.sessionId = str(res[0]['id'])
		self.ixNetUrl = "%s/sessions/%s/ixnetwork" % (self.baseUrl,self.sessionId)
		self._root     = self.ixNetUrl
		self.execDict = self.getOptions(self.ixNetUrl,'operations')
		self.execstatisticsViewDict = self.getOptions(self.ixNetUrl+"/statistics/view",'operations')


	def waitForComplete(self,sessionUrl, timeout=90):
		if self.response.json().has_key('errors'):
			print self.response.json()["errors"][0]#.replace("\r","")
			raise Exception('FAIL : need To Exit ')
		print "\tState","\t",self.response.json()["state"]
		while self.response.json()["state"] == "IN_PROGRESS":
			if timeout == 0:break
			time.sleep(1)
			state = self.getAttribute(self.response.json()["url"], "state" )
			print "\t\t",state
			timeout = timeout - 1

	def getRoot(self):return self._root
	def commit(self):pass
	def remapIds(self, localIdList):
		if type(localIdList)==list:return localIdList
		else:return [localIdList]
	
	def checkError(self):
		if not self.response.ok:TestFailedError(self.response.text)
	def getList(self, objRef, child):
		if debug:print "GetList: %s/%s/" % (objRef,child)
		baseUrl = objRef
		if self.srvUrl not in objRef:baseUrl = self.srvUrl+objRef
		try:self.response = requests.get("%s/%s/" % (baseUrl,child), headers=self.urlHeadersJson)
		except Exception, e:raise Exception('Got an error code: ', e)
		self.checkError()
		objs = ["%s/%s/%s" % (objRef,child,str(i['id'])) for i in self.response.json()]
		return objs
	
		
	def getIxNetSessions(self):
		if debug:print self.baseUrl +"/sessions"
		try:self.response = requests.get(self.baseUrl +"/sessions", headers=self.urlHeadersJson)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		sessions = [i for i in self.response.json() if i['state']=='ACTIVE']
		return sessions

	def add(self, objRef, child, *args):
		try:data=args[0]
		except:data=[{}]
		if debug:print "ADD:","%s/%s/" % (objRef,child),data
		try:self.response = requests.post("%s/%s/" % (objRef,child), data=json.dumps(data),headers=self.urlHeadersJson)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		return ["http://%s:%s%s" % (self.server,self.port,i['href']) for i in self.response.json()['links']]

	def remove(self, objRef):
		try:self.response = requests.delete(objRef)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		return self.response.json()

		
	def execute(self, *args):
		args=list(args)
		if debug:print "EXECUTE ARGS:",args
		execName = args[0]
		posturl=''
		#posturl = self.execDict[execName]
		print "Exec: ",execName
		try:posturl = self.srvUrl+self.execDict[execName]
		except:pass
		if debug:print "INITIAL POST URL",posturl

		if execName=="loadConfig" and self._loadConfig(args[1]):
			data={'filename': self.ixncfgname}
			try:self.response = requests.post(url=posturl, data=json.dumps(data),headers=self.urlHeadersJson)
			except Exception, e:raise Exception('Got an error code: ', e)
			self.waitForComplete(posturl)
			self.checkError()
			return self.response.json()
			
		elif execName=="importBgpRoutes":
			argx = ['arg%d' % (i+1,) for i in range(len(args[1:]))]
			tmp =[]
			for i in args[1:]:
				try:tmp.append(i.replace(self.srvUrl,""))
				except:tmp.append(i)
				
			data = dict(zip(argx,tmp))
			posturl = self.srvUrl+data['arg1']
			
		else:
			argx = ['arg%d' % (i+1,) for i in range(len(args[1:]))]
			argsv = args[1:]
			tmp_values=[]
			for val in argsv:
				if type(val)==list or type(val)==tuple:
					if all(isinstance(elem, list) for elem in val) or all(isinstance(elem, tuple) for elem in val):
						kstruct=[]
						for elm in val:
							if debug:print "UUUUUUUUUUUUU",elm
							argxy = ['arg%d' % (i+1,) for i in range(len(elm))]
							v = dict(zip(argxy,elm))
							kstruct.append(v)
						tmp_values.append(kstruct[:])
					else:tmp_values.append([v for v in val])
				else:tmp_values.append(val)
			if debug:print "Temp Values:",tmp_values
			data = dict(zip(argx,tmp_values))
		if data:
			if type(data['arg1']) == list:
				if type(data['arg1'][0]) == dict:
					pass
				else:
					obj = data['arg1'][0].replace(self.srvUrl,"")
					posturl = self.srvUrl+obj + "/operations/"+execName
			else:
				obj=data['arg1'].replace(self.srvUrl,"") 
				posturl = self.srvUrl+obj + "/operations/"+execName
		print "POST:->",posturl
		print "DATA:->",data
		
		
		#self.response = requests.post(url=posturl, data=json.dumps(data),headers=self.urlHeadersJson)
		print '\nEXECUTE:', posturl, data
		try:self.response = requests.post(url=posturl, data=json.dumps(data),headers=self.urlHeadersJson)
		except Exception, e:raise Exception('Got an error code: ', e)
		self.waitForComplete(posturl)
		self.checkError()
		return self.response.json()


	def setAttribute(self,objRef,name,value):
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		name=name.lstrip("-")
		if debug:print "SET ATTRIBUTE DATA",{name:value}
		try:self.response = requests.patch(url=objRef, data=json.dumps({name:value}), headers=self.urlHeadersJson)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()

	
	def getOptions(self,objRef,nodetype="attributes",editable=True):
		
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		try:self.response = requests.options(url=objRef)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		#if debug:pprint.pprint(self.response.json())
		childrenList       = self.response.json()['custom']['children']
		attributes = self.response.json()['custom']['attributes']
		operationsList = self.response.json()['custom']['operations']
		attributesList=[]
		for attr in attributes:
			if attr['type']['name']=="href":attributesList.append(attr)
			elif attr['readOnly']==False:attributesList.append(attr)
			if editable:attributesList.append(attr)
			
				
		operationsDict = {}
		for attr in operationsList:operationsDict[attr['operation']] = attr['href']
		if nodetype=="children":returnvalues = childrenList
		elif nodetype=="operations":returnvalues = operationsDict
		else:returnvalues = attributesList
		return returnvalues

	def setMultiAttribute(self,objRef,*args):
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		names = [name.lstrip("-") for name in args[0::2]]
		values = args[1::2]
		data = dict(zip(names,values))
		if debug:
			print "setMultiAttribute:url",objRef
			pprint.pprint(data)
		try:self.response = requests.patch(url=objRef, data=json.dumps(data), headers=self.urlHeadersJson)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()

	def getAttribute(self, objRef, name):
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		name=name.lstrip("-")
                #print '\nGET:', objRef, name
		try:self.response = requests.get(objRef)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		if name=="all":
                    return self.response.json()
		else:
                    #print '\nGET Response:', pprint.pprint(self.response.json())
                    return self.response.json()[name]

		
	def getIxNetSessionUrl(self, sessionId=None):
		if sessionId:return 
		else:return "/%s/sessions/%s/ixnetwork" % (self.baseUrl,str(self.sessionId))

	def readFrom(self,filename, *args):
		# read the config as binary
		self.ixncfgname=filename
		with open(filename, mode='rb') as file:
			configContent = file.read()
		return configContent

	def _assignPorts(self,*args):
		realPorts = args[0]
		vports = args[2]
		from copy import deepcopy
		data = {"arg1":[],"arg2":[],"arg3":[],"arg4":True}
		try:[data["arg1"].append({"arg1": chassis, "arg2": str(card), "arg3": str(port)}) for chassis,card,port in realPorts]
		except Exception, e:raise Exception(str(e))
		data["arg3"] = vports
		return data
		
	def ixNetExec(objUrl, execName, payload=None):
		try:
			stateURL_ = objUrl + "/operations/"+execName
			_stateURL=stateURL_.replace('//','/')
			urlString=_stateURL.replace('http:/','http://')
			urlHeadersJson = {'content-type': 'application/json'}
			if payload == None:
				print "POST: " + urlString
				response = requests.post(url=urlString, headers=urlHeadersJson)
			else: 
				print "POST: " + urlString + "  <-- Payload: " + str(payload)
				response = requests.post(url=urlString, headers=urlHeadersJson, data=json.dumps(payload))
			a = response.json()
			if a["id"]!="":waitForComplete(objUrl, response)
			else : return response
		except Exception, e:
			raise Exception('Got an error code: ', e)  
		if not response.ok:
			raise TestFailedError(response.text)
		return response


def loadConfigFile(sessionUrl, configFile):
    # Load a saved config file from a Linux filesystem
    # 
    # sessionUrl = http://10.219.x.x:11009/api/v1/sessions/1/ixnetwork
    # configFile = The full path including the saved config file
    # 
    # Returns 0 if success
    # Returns 1 if failed

    urlHeadersJson = {'content-type': 'application/json'}
    urlHeadersData = {'content-type': 'application/octet-stream'}

    # 1> Read the config file
    print '\nReading saved config file'
    with open(configFile, mode='rb') as file:
        configContents = file.read()

    fileName = configFile.split('/')[-1]

    # 2> Upload it to the server and give it any name you want for the filename
    uploadFile = sessionUrl+'/files?filename='+fileName
    print '\nUploading file to server:', uploadFile
    response = requests.post(uploadFile, data=configContents, headers=urlHeadersData)
    if response.status_code != 201:
        return 1

    # 3> Set the payload to load the given filename:  /api/v1/sessions/1/ixnetwork/files/ospfNgpf_8.10.ixncfg
    payload = {'arg1': '/api/v1/sessions/1/ixnetwork/files/%s' % fileName}

    loadConfigUrl = sessionUrl+'/operations/loadconfig'

    # 4> Tell the server to load the config file
    print '\nLoad config:', loadConfigUrl
    print 'Payload', payload
    response = requests.post(url=loadConfigUrl, data=json.dumps(payload), headers=urlHeadersJson)
    if response.status_code != 202:
        return 1

    if waitForComplete(response, loadConfigUrl+'/'+response.json()['id']) == 1:
        return 1
    else:
        return 0

def VerifyPortState( portList='all', expectedPortState='up' ):
    # portList format = 1/2.  Not 1/1/2

    print '\nVerifyPortState ...',
    allVports = ixNet.getList(ixNet.getRoot(), 'vport')
    if portList == 'all':
        vportList = allVports

    if portList != 'all':
        vPortList = []
        for vport in allVports:
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
            connectedTo = ixNet.getAttribute(vport, 'connectedTo')
            connectedTo = connectedTo.split('/')[-2:]
            card = connectedTo[0].split(':')[-1]
            port = connectedTo[1].split(':')[-1]
            port = card+'/'+port

            if port in portList:
                vPortList.append(vport)
                
    portsAllUpFlag = 0

    for vport in vPortList:
        for timer in xrange(60+1):
	    # ::ixNet::OBJ-/availableHardware/chassis:"10.205.4.35"/card:1/port:1
            connectedTo = ixNet.getAttribute(vport, 'connectedTo')
            connectedTo = connectedTo.split('/')[-2:]
            card = connectedTo[0].split(':')[-1]
            port = connectedTo[1].split(':')[-1]
            port = card+'/'+port
            portState = ixNet.getAttribute(vport, 'state')

            if expectedPortState == 'up':
                if portState != 'up' and timer != 60:
                    print '\nVerifyPortState: %s is still %s. Expecting port up. %s/60 seconds.' % (port, portState, timer)
                    time.sleep(2)
                    continue

                if portState != 'up' and timer == 60:
                    print '\nError VerifyPortState: %s seem to be stuck on %s state. Expecting port up.\n' % port
                    portsAllUpFlag = 1

                if portState == 'up':
                    print '\nVerifyPortState: %s state is %s' % (port, portState)
                    break

            if expectedPortState == 'down':
                if portState != 'down' and timer != 60:
                    print '\nVerifyPortState: %s is still %s. Expecting port down. %s/60 seconds.' % (port, portState, timer)
                    time.sleep(2)
                    continue
                
                if portState == 'up' and timer != 60:
                    print '\nError VerifyPortState: %s seem to be stuck on the %s state. Expecting port down' % (port, portState)
                    portsAllUpFlag = 1

                if portState == 'down':
                    print '\nVerifyPortState: %s state is %s as expected' % (port, portState)
                    break

    if portsAllUpFlag == 1:
        return 1
    else:
        time.sleep(3)
        return 0


def GetConfiguredQuickTests():
    allConfiguredQuickTestNames = []
    allConfiguredQuickTestHandles = ixNet.getAttribute(ixNet.getRoot()+'/quickTest', 'testIds')
    for qtHandle in allConfiguredQuickTestHandles:
        allConfiguredQuickTestNames.append(ixNet.getAttribute(qtHandle, 'name'))
    return allConfiguredQuickTestNames


def VerifyAllQuickTestNames( quickTestNameList ):
    noSuchQuickTestName = []
    allConfiguredQuickTestNames = []
    allConfiguredQuickTestHandles = ixNet.getAttribute(ixNet.getRoot()+'/quickTest', 'testIds')
    for qtHandle in allConfiguredQuickTestHandles:
        allConfiguredQuickTestNames.append(ixNet.getAttribute(qtHandle, 'name'))

    print '\nAll configured QT test names:', allConfiguredQuickTestNames, 

    for userDefinedQuickTestName in quickTestNameList:
        if userDefinedQuickTestName not in allConfiguredQuickTestNames:
            noSuchQuickTestName.append(userDefinedQuickTestName)

    if noSuchQuickTestName != '':
        for noSuchTestName in noSuchQuickTestName:
            print '\nError: No such Quick Test name:', noSuchTestName
    else:
        return 0

    return 1


def GetAllQuickTestHandles():
    return ixNet.getAttribute(ixNet.getRoot()+'/quickTest', 'testIds')

def ApplyQuickTestHandle( quickTestHandle ):
    print '\nApplying Quick Test handle:', quickTestHandle
    ixNet.execute('apply', quickTestHandle)

def VerifyQuickTestApply( quickTestHandle ):
    currentAction = GetQuickTestCurrentAction(quickTestHandle).strip(' ')
    print '\nVerifyQuickTestApply currentAction:', currentAction
    if currentAction == 'TestEnded' or currentAction == 'None':
        for timer in xrange(1,20+1):
            currentAction = GetQuickTestCurrentAction(quickTestHandle).strip(' ')
            if currentAction == 'TestEnded' or currentAction == 'None':
                print '\nCurrent state = %s : Waiting %s/20 seconds to change states' % (currentAction, timer)
                time.sleep(1)
                continue
            else:
                break

    ixNetworkVersion = ixNet.getAttribute(ixNet.getRoot()+'/globals', 'buildNumber')
    ixNetworkVersionNumber = re.match('^[^ ]+ *([0-9]+)\.[^ ]+ *', ixNetworkVersion)
    applyQuickTestCounter = 300
    for counter in xrange(1,applyQuickTestCounter+1):
        quickTestApplyStates = ['InitializingTest', 'ApplyFlowGroups', 'SetupStatisticsCollection']
        currentAction = GetQuickTestCurrentAction(quickTestHandle).strip(' ')
        if currentAction == None:
            currentAction = 'ApplyingAndInitializing'
            
        print '\nVerifyQuickTestApply: %s : Waiting %s/%s seconds' % (currentAction, counter, applyQuickTestCounter)
        if ixNetworkVersionNumber >= 8:
            if counter < applyQuickTestCounter and currentAction != 'TransmittingFrames':
                time.sleep(1)
                continue

        if ixNetworkVersionNumber < 8:
            if counter < applyQuickTestCounter and currentAction == 'ApplyingAndInitializing':
                time.sleep(1)
                continue

        if ixNetworkVersionNumber >= 8:
            if counter < applyQuickTestCounter and currentAction == 'TransmittingFrames':
                print '\nVerifyQuickTestApply is done applying configuration and has started transmitting frames'
                break
            break

        if ixNetworkVersionNumber < 8:
            if counter < applyQuickTestCounter and currentAction == 'ApplyingAndInitializing':
                print '\nVerifyQuickTestApply is done applying configuration and has started transmitting frames'
                break
            break
        
        if counter == applyQuickTestCounter:
            if ixNetworkVersionNumber >= 8 & currentAction != 'TransmittingFrames':
                print '\nVerifyQuickTestApply is stuck on %s. Waited %s/%s seconds' % (
			currentAction, counter, applyQuickTestCounter)
                return 1
            if ixNetworkVersion < 8 and currentAction != 'Trial':
                print '\nVerifyQuickTestApply is stuck on %s. Waited %s/%s seconds' % (
			currentAction, counter, applyQuickTestCounter)
                return 1

    return 0

def StartQuickTest( quickTestHandle ):
    print '\nStartQuickTest\n'
    ixNet.execute('start', quickTestHandle)

def GetQuickTestHandleByName( quickTestName ):
    for quickTestHandle in GetAllQuickTestHandles():
        currentQtName = ixNet.getAttribute(quickTestHandle, 'name')
        if (bool(re.match(quickTestName, currentQtName, re.I))):
            return quickTestHandle

    return 0

def GetQuickTestDuration( quickTestHandle ):
    return ixNet.getAttribute(quickTestHandle+'/testConfig', 'duration')

def GetQuickTestTotalFrameSizesToTest( quickTestHandle ):
    return len(ixNet.getAttribute(quickTestHandle+'/testConfig', 'framesizeList'))

def GetQuickTestCurrentAction(quickTestHandle):
    ixNetworkVersion = ixNet.getAttribute(ixNet.getRoot()+'/globals', 'buildNumber')

    match = re.match('^[^ ]+ *([0-9]+)\.[^ ]+ *', ixNetworkVersion)
    if match.group(1) >= 8:
        return ixNet.getAttribute(quickTestHandle+'/results', 'currentAction')
    else:
        return ixNet.getAttribute(quickTestHandle+'/results', 'progress')

def CopyFileWindowsToLocalLinux( currentQtTestName, windowsPath, localPath ):
    fileName = windowsPath.split('\\')[-1]
    print '\nCopyFileWindowsToLocalLinux: From: %s to %s\n' % (windowsPath, localPath)
    destinationPath = '/api/v1/sessions/1/ixnetwork/files/'+fileName
    currentTimestamp = datetime.datetime.utcnow().strftime('%s')
    
    requests.post('http://%s:%s/api/v1/sessions/1/ixnetwork/operations/copyfile' % (
		    configs.ixNetworkApiServer, 
		    int(configs.ixNetworkPort)+3000), 
		  data=json.dumps({"arg1": windowsPath, "arg2": destinationPath}), 
		  headers={'content-type': 'application/json'})

    # curl http://10.219.117.103:11009/api/v1/sessions/1/ixnetwork/files/AggregateResults.csv -O -H "Content-Type: application/octet-stream" -output /home/hgee/AggregateResults.csv

    requestStatus = requests.get('http://%s:%s/api/v1/sessions/1/ixnetwork/files/%s' % (
		    configs.ixNetworkApiServer, 
		    int(configs.ixNetworkPort)+3000, fileName), 
				 stream=True)
    if requestStatus.status_code == 200:
        contents = requestStatus.raw.read()
	localPath = localPath+'/'+currentQtTestName.replace(' ', '_')+'_'+fileName+'_'+currentTimestamp 
	with open(localPath, 'wb') as downloadedFileContents:
            downloadedFileContents.write(contents)
    else:
        print '\nError: Failed to get %s from %s' % (fileName, configs.ixNetworkApiServer)

def MonitorQuickTestRunProgress( quickTestHandle ):
    counter = 1
    while True:
        isRunning = ixNet.getAttribute(quickTestHandle+'/results', 'isRunning')

        if isRunning == True:
            currentRunningProgress = ixNet.getAttribute(quickTestHandle+'/results', 'progress')
            print '\n%s seconds: %s' % (counter, currentRunningProgress)
            counter += 1
            time.sleep(10)
            continue
        else:
            break

    time.sleep(2)

def help():
    os.system('clear')
    print '\n\nUsage:'
    print '-'*50, '\n'
    
    print '-ixNetworkApiServerIp:   The IxNetwork Windows PC'
    print '-ixNetworkPort:          The IxNetwork socket port number'
    print '-quickTestListToRun:     All the Quick Test names to run wrapped inside double quotes'
    print '                         Example: \'broadcast 2544, throughput\''
    print '-copyResultsToLinuxPath: The full path and file name to save the Quick Test results on'
    print '                         your local Linux.'
    print '                         Example: /automation/resultFolder'
    print '-quickTestCsvResultFile: The statistic result file to get when test is done'
    sys.exit()


parameters = sys.argv[1:]
argIndex = 0
while argIndex < len(parameters):
    currentArg = parameters[argIndex]
    if currentArg == '-ixNetworkApiServerIp':
        configs.ixNetworkApiServerIp = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-ixNetworkPort':
        configs.ixNetworkPort = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-quickTestListToRun':
        # -quickTestListToRun 'broadcast Copy_1, broadcast'
        params = parameters[argIndex + 1]
        configs.userSelectQuickTestList = [x.strip() for x in params.split(',')]
        argIndex += 2
    elif currentArg == '-copyResultsToLinuxPath':
        configs.copyResultFileToLocalLinux = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-quickTestCsvResultFile':
        configs.quickTestCsvResultFile = parameters[argIndex + 1]
	argIndex += 2
    elif currentArg == '-help':
        help()
    else:
        sys.exit('No such parameter: %s' % currentArg) 


ixNet = IxNet(configs.ixNetworkApiServer, int(configs.ixNetworkPort)+3000)
ixNet.connect()

if os.path.exists(configs.quickTestConfigFile) == False:
    sys.exit('\nNo such config file: {0}'.format(configs.quickTestConfigFile))

if loadConfigFile(sessionUrl, configs.quickTestConfigFile) == 1:
    sys.exit()

if configs.userSelectQuickTestList == 'all':
    configuredQuickTestList = GetConfiguredQuickTests()
    if configuredQuickTestList:
        quickTestNameList = configuredQuickTestList
    else:
        sys.exit('\nError: No Quick Test configured found')
else:
    # Verify user selected Quick Test to run
    if VerifyAllQuickTestNames(configs.userSelectQuickTestList) == 0:
        sys.exit()
    quickTestNameList = configs.userSelectQuickTestList

sys.exit()

print '\nList of Quick Test to run ...'
for quickTestToRun in quickTestNameList:
    print '\t', quickTestToRun

for quickTestName in quickTestNameList:
    quickTestHandle = GetQuickTestHandleByName(quickTestName)
    currentQuickTestName = ixNet.getAttribute(quickTestHandle, 'name')
    print '\nStarting QuickTest name:', currentQuickTestName

    # Get test duration
    testDuration = GetQuickTestDuration(quickTestHandle)
    totalFrameSizesToTest = GetQuickTestTotalFrameSizesToTest(quickTestHandle)
    ApplyQuickTestHandle(quickTestHandle)

    # Must wait 8 seconds for applying to sync before moving forward
    print '\nWait 8 seconds for Quick Test to apply to hardware ...'
    time.sleep(8)
    
    if StartQuickTest(quickTestHandle) == 1:
        sys.exit()

    if VerifyQuickTestApply(quickTestHandle) == 1:
        sys.exit()

    MonitorQuickTestRunProgress(quickTestHandle)
    resultPath = ixNet.getAttribute(quickTestHandle+'/results', 'resultPath')
    resultPath = resultPath+'\\'+configs.quickTestCsvResultFile

    if configs.copyResultFileToLocalLinuxPath.split('/')[:-1] == '/':
        configs.copyResultFileToLocalLinuxPath = configs.copyResultFileToLocalLinuxPath[:-1]

    CopyFileWindowsToLocalLinux(currentQuickTestName, resultPath, configs.copyResultFileToLocalLinuxPath)

sys.exit()

