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
import httplib
import sys
import pprint
debug=1
class TestFailedError(Exception): pass
class returnItem():
    def __init__(self,res):
	    self.responseString = res
    def json(self,):
        return json.loads(self.responseString)
    def ok(self,):
        return True

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
		if 'error' in str(self.response):TestFailedError(self.response)
	def getList(self, objRef, child):
		if debug:print "GetList: %s/%s/" % (objRef,child)
		baseUrl = objRef
		if self.srvUrl not in objRef:baseUrl = self.srvUrl+objRef
		try:self.response = requests().get("%s/%s/" % (baseUrl,child))
		except Exception, e:raise Exception('Got an error code: ', e)
		#for i in self.response.json():print i
		self.checkError()
		objs = ["%s/%s/%s" % (objRef,child,str(i['id'])) for i in self.response.json()]
		return objs

		
		
	def getIxNetSessions(self):
		if debug:print self.baseUrl +"/sessions"
		try:self.response = requests().get(self.baseUrl +"/sessions")
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		sessions = [i for i in self.response.json() if i['state']=='ACTIVE']
		return sessions

	def add(self, objRef, child, *args):
		try:data=args[0]
		except:data=[{}]
		if debug:print "ADD:","%s/%s/" % (objRef,child),data
		try:self.response = requests().post("%s/%s/" % (objRef,child), json.dumps(data))
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		return ["http://%s:%s%s" % (self.server,self.port,i['href']) for i in self.response.json()['links']]

	def remove(self, objRef):
		try:self.response = requests().delete(objRef)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		return self.response.json()

	def help(self, urlObj):
		try:self.response = requests().options(urlObj)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		return self.response.json()
	
	def getHelpUrl(self,items):
		tmp={}
		import re
		for item in items:
			item = item.split("/api/v1/sessions/%s/ixnetwork/" % (self.sessionId,))[-1]
			tstr = "/api/v1/sessions/%s/ixnetwork/" % (self.sessionId,) + re.sub(r"/[0-9]+","",item)
			tmp[tstr]=None
		if len(tmp.keys())>1:raise Exception("Two different nodes given")
		retr = "http://%s:%s%s" % (self.server,self.port,tmp.keys()[0])
		return retr
		
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
			try:self.response = requests().post(posturl, json.dumps(data))
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
		
		
		#self.response = requests().post(posturl, json.dumps(data))
		try:self.response = requests().post(posturl, json.dumps(data))
		except Exception, e:raise Exception('Got an error code: ', e)
		self.waitForComplete(posturl)
		self.checkError()
		return self.response.json()

	def setAttribute(self,objRef,name,value):
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		name=name.lstrip("-")
		if debug:print "SET ATTRIBUTE DATA",{name:value}
		try:self.response = requests().patch(objRef, json.dumps({name:value}))
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()

	def getNode(self,objRef,deepchild="*",skip=0,take=30,filter=None):
		tmpurl = objRef+"?deepchild=%s&skip=%d&take=%d" % (deepchild,skip,take)
		try:self.response = requests().get(tmpurl)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		nodes = [node['links'][0]['href'] for node in self.response.json()['data']]
		return nodes
	
	def getOptions(self,objRef,nodetype="attributes",editable=True):
		
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		try:self.response = requests().options(objRef)
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
		try:self.response = requests().patch(objRef, json.dumps(data))
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()

	def getAttribute(self, objRef, name):
		if self.srvUrl not in objRef:
			objRef = self.srvUrl + objRef
		name=name.lstrip("-")
		try:self.response = requests().get(objRef)
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		if name=="all":return self.response.json()
		else:return self.response.json()[name]

		
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

	def getFilteredList(self, objRef, child, name, value):
		tmp_objRef = objRef
		name=name.lstrip("-")
		if debug:print "getFilteredList:",objRef,child
		#objRef = self._convert2Url(objRef)
		try:self.response = requests().get("%s/%s/" % (objRef,child))
		except Exception, e:raise Exception('Got an error code: ', e)  
		self.checkError()
		#HACK Need to return the URL , we need to make it.
		objs = ["%s/%s/%s" % (objRef,child,str(i['id'])) for i in self.response.json() if str(i[name])==str(value)]
		if debug:print "\t",objs
		return objs
	


	def _loadConfig(self,binaryconfig):
		# send the config to server files location
		r = requests().post(self.ixNetUrl + "/files/"+ self.ixncfgname,binaryconfig)
		if self.ixncfgname in r:return True
		else:raise Exception("Load Config Failed")

	def setAndCheckAttributeValue(self,node,attr,value):
		#print '\tSet node %s attrib:value "%s:%s"' % (str(node),attr,str(value))
		isError = 1
		retVal  = str(value)
		try:
			self.setAttribute(node,"-%s" %(attr),value)
			self.commit()
		except Exception,ex:
			print "\t\t\tError while setting %s node attribute %s value %s" %(node,attr,value)
			print str(ex)
			return isError
		
		retAttrVal = self.getAttribute(node,"-%s" %(attr))
		if retVal!=retAttrVal:
			print "\t\t\tgetAttribute value (%s) doesnt match with expected value (%s)" % (retAttrVal,retVal)
		return 0

	def waitForThreeTimeStampPeriods(self,viewtocheck):
		timStpChgCount=0
		while timStpChgCount<4:
			timeStamp1 = self.getAttribute(viewtocheck+"/page",'-timestamp')
			time.sleep(1)
			timeStamp2 = self.getAttribute(viewtocheck+"/page",'-timestamp')
			if timeStamp1 != timeStamp2:
				timStpChgCount+=1
				print  "Timestamp change count: ",timStpChgCount
		print "Waited until 3 timestamp changes seen for %s",viewtocheck

	def isViewReady(self,view,timeout=10,refresh=False):
		print "Check if %s is ready" % (view,)
		startTime = time.time()

		while self.getFilteredList(self.getRoot()+'/statistics', 'view', '-caption', view)==[] or 'rue' not in str(self.getAttribute( self.getFilteredList(self.getRoot()+'/statistics', 'view', '-caption', view)[0]+"/page","-isReady")):
			print 'sssssssssssssss',self.getAttribute( self.getFilteredList(self.getRoot()+'/statistics', 'view', '-caption', view)[0]+"/page","-isReady")
			endTime = time.time()
			diff = endTime - startTime
			if (diff > timeout):
				print "View ( %s )is not available in %d secs." % (view,timeout)
				return False
			print "\tStats from %s/page are not ready yet..." % (view,),
			print "\tWait 5 seconds, verify again"
			time.sleep(5)
		print "\t%s view is available!" %(view,)
		retViewObj = self.getFilteredList(self.getRoot()+'/statistics', 'view', '-caption', view)[0]
		if not refresh:
			self.waitForThreeTimeStampPeriods(self.getFilteredList(self.getRoot()+'/statistics', 'view', '-caption', view)[0])
			
		return retViewObj

	def waitForTrafficState(self,state,timeout=90):
		traffic=self.ixNetUrl+"/traffic"
		count = 0

		if state=="started":
			tiList = self.getList(traffic,"trafficItem")
			for trItem in tiList:
				confElList = self.getList(trItem,"configElement")
				for confEl in confElList:
					trType = self.getAttribute(confEl+"/transmissionControl","-type")
					if trType not in ["continuous","auto"]:
						print "%s traffic type detected waiting a predefined 90 sec for traffic to start" % (trType,)
						time.sleep(90)
						return 0
				

		print "\tChecking Traffic State: %s for: %s sec" %(state,str(timeout))
		
		while self.getAttribute(traffic,"-state")!=state:
			print "\t\t\t%d: Traffic state --> %s" % (count,self.getAttribute(traffic,"-state"))
			time.sleep(1)
			count+=1
			if count > timeout:
				#printTrafficWarningsAndErrors()
				raise Exception("Waited for %s sec, Traffic still not in %s state... " % (count,state))
		print "\tTraffic reached %s state in %s sec" % (state,count)
		return 0


	def generateApplyStartTraffic(self,refreshBeforeApply=False,timeOut=90):
		print "Generate Apply Start Traffic..."
		error = 0
		traffic = self.ixNetUrl+"/traffic"
		print "\tSet refreshLearnedInfoBeforeApply for Traffic to %s" % (str(refreshBeforeApply),)
		if refreshBeforeApply:
			if self.setAndCheckAttributeValue(traffic,"refreshLearnedInfoBeforeApply", 'true'):return 1
		else:
			if self.setAndCheckAttributeValue(traffic,"refreshLearnedInfoBeforeApply", 'false'):return 1

		# Apply Traffic
		tt="/api/v1/sessions/1/ixnetwork/traffic"
		print "\tApplying the traffic ...."
		self.execute("apply",tt)
		self.waitForTrafficState("stopped")
		print "\tTraffic applied successfully ..."
		#printTrafficWarningsAndErrors()
		self.setAndCheckAttributeValue(traffic,"refreshLearnedInfoBeforeApply", 'false')
		#Start Traffic
		print "\tStarting the traffic..."
		self.execute('startStatelessTraffic',[tt])
		self.waitForTrafficState('started',timeOut)
		#printTrafficWarningsAndErrors()
		print "SUCCESS:Generate Apply Start Traffic..."
		return 0


	def getViewPageSnapshotForPandas(self,view,nRandomPages=0,retType=[],timeOut=90,refresh=False):
		viewObj = self.isViewReady(view,timeOut,refresh)
		if not viewObj:raise Exception("View is not Ready")
		print viewObj
		
		statUrl = self.getFilteredList(self.getRoot()+'/statistics', 'view', '-caption', view)
		if statUrl==[]:raise Exception("FAIL - need to exit the caption ",view," does not exists ")
		stats=statUrl[0]+'/page'

		cols = self.getAttribute(stats, '-columnCaptions')
		i = int(self.getAttribute(stats, '-currentPage'))
		total = int(self.getAttribute(stats, '-totalPages'))

		retList=[]
		def getRowData(cols,rows):
			retList=[]
			for row in rows.values():
				a = []
				appnd2a = a.append
				for stat,val in zip(cols, row[0]):appnd2a((stat, val))
				if type(retType)==list:retList.append(a[:])
				else:retList.append(dict(a))
			return retList[:]
		
		if nRandomPages and total>nRandomPages:
			for pageNumber in sample(set(range(1,total)), nRandomPages):
				self.setAndCheckAttributeValue(stats,'currentPage', pageNumber)
				if not self.isViewReady(view,timeOut,refresh):raise Exception("View is not Ready")
				rows = self.getAttribute(stats, '-rowValues')
				retList+= (cols,getRowData(rows))
		else:
			while i <= total:
				if total>1:
					self.setAndCheckAttributeValue(stats,'currentPage', i)
					if not self.isViewReady(view,timeOut,refresh):raise Exception("View is not Ready")
				i+=1
				rows = self.getAttribute(stats, '-rowValues')
				retList+= getRowData(cols,rows)
		
		return retList
'''
def singleValue(ixNet,url,count,value=[],format=None):
	#return
	print "\tIn singleValue",value
	ixNet.setAttribute(url,"-pattern","singleValue")
	ixNet.setAttribute(url+"/singleValue","-value",value[0])
	j=ixNet.getAttribute(url+"/singleValue","-value")
	print "FFF",j,value[0]
	if str(value[0])!=j:raise Exception("FAIL singleValue:SetAndGet attribute verification failed")
	
def counter(ixNet,url,count,value=[],format=None):
	#return
	print "\tIn counter",value
	ixNet.setAttribute(url,"-pattern","counter")
	ixNet.setMultiAttribute(url+"/counter","-start",str(value[0]),"-step",'3',"-direction","increment")
	j=ixNet.getAttribute(url+"/counter","start")
	print j, value
	if str(value[0])!=j:raise Exception("FAIL COUNTER:SetAndGet attribute verification failed")
def custom(ixNet,url,count,value=[],format=None):
	#return
	print "\tIn custom",value
	ixNet.setAttribute(url,"-pattern","custom")
	
def random(ixNet,url,count,value=[],format=None):
	#return
	print "\tIn random",value
	ixNet.setAttribute(url,"-pattern","random")
	j=ixNet.getAttribute(url,"-values")
	print "-------->",j,count,len(list(set(j)))
	if format=="bool":
		if len(list(set(j)))!=2:raise Exception("FAIL:Random:SetAndGet attribute verification failed")
	else:
		if len(list(set(j)))!=count:raise Exception("FAIL:Random:SetAndGet attribute verification failed")
def repeatableRandom(ixNet,url,count,value=[],format=None):
	print "\tIn repeatableRandom",value
	ixNet.setAttribute(url,"-pattern","repeatableRandom")
	ixNet.setMultiAttribute(url+"/repeatableRandom","-mask",str(value[0]),"-count",count,"-seed","2")
	j=ixNet.getAttribute(url+"/repeatableRandom","-seed")
	print type(j)
	if str(j)!=str("2"):raise Exception("FAIL:repeatableRandom:SetAndGet attribute verification failed")

def valueList(ixNet,url,count,value,format=None):
	#return
	print "\tIn valueList",value
	ixNet.setAttribute(url,"-pattern","valueList")
	#print "\t",url,enum,"Doesnt Work"
	ixNet.setAttribute(url+"/valueList","-values",value*count)
	#ixNet.setMultiAttribute(url,"-pattern","valueList","-value",[enum]*10)

def alternate(ixNet,url,count,value,format=None):
	print "\tIn alternate",value
	

def subset(ixNet,url,count,value,format=None):print "\tIn subset"
def customDistributed(ixNet,url,count,value,format=None):print "\tIn customDistributed"

	
def setAndCheckAttributeValue(ixNet,url,attributes):
	fd={"alternate":alternate,"customDistributed":customDistributed,"subset":subset,"singleValue":singleValue,"valueList":valueList,"counter":counter,"custom":custom,"random":random,"repeatableRandom":repeatableRandom}
	def verifyEnums(ixNet,url,attribdict):
		for i in attribdict['type']['enums']:
			ixNet.setAttribute(url,attribdict['name'],i)
			j=ixNet.getAttribute(url,attribdict['name'])
			if i!=j:raise Exception("FAIL verifyEnums:SetAndGet attribute verification failed")
		
	def verifyHrefs(ixNet,url,attribdict):
		url = "http://%s:%s" % (ixNet.server,ixNet.port) + ixNet.getAttribute(url,attribdict['name'])
		allAttributes     = ixNet.getAttribute(url,"all")
		#pprint.pprint(allAttributes)
		
		print "SSSSS:",allAttributes["pattern"],allAttributes["values"]
		availablePatterns = allAttributes['availablePatterns']
		enums             = allAttributes['enums']
		format            = allAttributes['format']#decimal,enum,ipv4,mac
		count             = int(allAttributes['count'])
		if format=="decimal":
			if enums:value=[enums[-3]]
			else:value=[5]
		elif format=='ipv4':value=["11.11.11.1"]
		elif format=="mac":value=["00:11:01:00:00:01"]
		elif format=="enum":value=[enums[-2]]
		elif format=="bool":value=['true']
		else:print format
		print url,attribdict['name']
		#print "\t",availablePatterns,enums,format,count
		for pattern in availablePatterns:
			fd[pattern](ixNet,url,count,value,format)
			

	def verifyInteger(ixNet,url,attribdict,setvalue='7'):
		url = "http://%s:%s" % (ixNet.server,ixNet.port) + url
		print "verifyInteger",url,attribdict['name'],setvalue
		ixNet.setAttribute(url,attribdict['name'],setvalue)
		j=ixNet.getAttribute(url,attribdict['name'])
		if setvalue!=j:raise Exception("FAIL:SetAndGet attribute (%s ) verification failed" % (attribdict['name']))

	def verifyString(ixNet,url,attribdict,setvalue='7'):
		url = "http://%s:%s" % (ixNet.server,ixNet.port) + url
		ixNet.setAttribute(url,attribdict['name'],setvalue)
		j=ixNet.getAttribute(url,attribdict['name'])
		if setvalue!=j:raise Exception("FAIL:SetAndGet attribute (%s ) verification failed" % (attribdict['name']))
		
	for attribdict in attributes:
		print attribdict['name'],attribdict['type']['name']
		if attribdict['type']['name']   == "string":verifyString(ixNet,url,attribdict)
		elif attribdict['type']['name'] == "int":pass#verifyInteger(ixNet,url,attribdict)
		elif attribdict['type']['name'] == "enum":verifyEnums(ixNet,url,attribdict)
		elif attribdict['type']['name'] == "href":verifyHrefs(ixNet,url,attribdict)
		else:print "NEED TO ADD THIS TYPE",attribdict['type']['name']
			

#ixNet = IxNet('10.200.115.204', 12345)
#ixNet.connect()
#root = ixNet.getRoot()
#vports = ixNet.add(root,'vport',[{}]*2)
#vports = ixNet.getList(root,'vport')
#print vports
#print ixNet.getAttribute(vports[0],'name')
#ixNet.setAttribute(vports[0],"-name","Vinod")
#ixNet.setMultiAttribute(vports[0],"-name","Vinodddddwwwwww","-type","ethernetvm")
#print ixNet.getAttribute(vports[0],'-name')
ipv4obj = ["/api/v1/sessions/2/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1","/api/v1/sessions/2/ixnetwork/topology/2/deviceGroup/1/ethernet/1/ipv4/1"]
opr = "http://10.200.115.204:12345/api/v1/sessions/2/ixnetwork/topology/deviceGroup/ethernet/ipv4"

print "Starting ipv4only"
ixNet.execute('start',opr,ipv4obj)
print "Stopping all protocols"
ixNet.execute("stopAllProtocols")
print "Starting ipv4only again"
ixNet.execute('start',opr,ipv4obj)
print "stopping ipv4only again"
ixNet.execute('stop',opr,ipv4obj)
ixNet.execute('stop',["topology/1/deviceGroup/1/ethernet/1/ipv4/1"])
#ixNet.assignPorts([('10.200.115.147', '7', '9'), ('10.200.115.147', '7', '10')])
#ixNet.execute('assignports',[('10.200.115.147', '7', '9'), ('10.200.115.147', '7', '10')])
#self.a
#ixNet.execute('loadConfig',ixNet.readFrom('test2.ixncfg'))
ethNode = ixNet.getNode(ixNet.getList(root,"topology")[0],"ethernet")[0]
#vlan = ixNet.getList(ethNode,'vlan')[0]
#vlan_attributes = ixNet.getOptions(vlan, "attributes")
#setAndCheckAttributeValue(ixNet,vlan,vlan_attributes)

ipv4Node = ixNet.getNode(ixNet.getList(root,"topology")[0],"ipv4")[0]
ipv4_attributes = ixNet.getOptions(ipv4Node, "attributes")
setAndCheckAttributeValue(ixNet,ipv4Node,ipv4_attributes)
'''
