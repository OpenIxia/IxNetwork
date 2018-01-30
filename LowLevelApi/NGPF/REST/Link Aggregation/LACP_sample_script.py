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
#    This script intends to demonstrate how to use NGPF OSPFv2 API.            #
#	 Script uses four ports to demonstrate LAG properties					   #
#                                                                              #
#    1. It will create 2 LACP topologies, each having an two port which are    #
#       LAG members. It will then modify the ActorSystemId and ActorKey	for	   # 
#       both the LAG systems                                                   #
#    2. Start the LACP protocol                                                #
#    3. Retrieve protocol statistics and LACP per port statistics              #
#	 4. Disable Synchronization flag on port1 in System1-LACP-LHS              # 
#	 5. Retrieve protocol statistics and LACP per port statistics              #
#	 6. Re-enable Synchronization flag on port1 in System1-LACP-LHS            # 
#	 7. Retrieve protocol statistics and LACP per port statistics              #
#	 8. Perform StopPDU on port1 in System1-LACP-LHS                		   #
#	 9. Retrieve LACP global learned info              			   			   #
#	 10. Perform StopPDU on port1 in System1-LACP-LHS                          # 
#	 11. Retrieve LACP global learned info                                     #
#	 12. Stop All protocols                                                    # 
#                                                                              #
# 	Ixia Software:                                                             #
#    IxOS      6.90 EA                                                         #
#    IxNetwork 7.50 EA                                                         #
#                                                                              #
################################################################################
if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports        = [('10.200.113.7', '8', '7'), ('10.200.113.7', '8', '8')]
    py.ixTclServer  =  "10.200.225.53"
    py.ixRestPort    =  '11020'
    py.ixTclPort     =  8020
# END HARNESS VARS ************************************************************

import time
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import httplib
import sys
import pprint
debug=0
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



#proc to generate drill-down global learned info view for LACP
def gererateLacpLearnedInfoView ( viewName ):
    viewCaption = viewName
    protocol = 'LACP'
    drillDownType = 'Global Learned Info'
    root    = ixNet.getRoot()
    statistics = root + '/statistics'
    statsViewList = ixNet.getList(statistics, 'view')
	
   # Add a StatsView
    view = ixNet.add(statistics, 'view')
    ixNet.setAttribute(view, '-caption', viewCaption)
    ixNet.setAttribute(view, '-type', 'layer23NextGenProtocol')
    ixNet.setAttribute(view, '-visible', 'true')
    ixNet.commit()
    view = ixNet.remapIds(view)[0]

   # Set Filters        
    trackingFilter = ixNet.add(view, 'advancedCVFilters')
    ixNet.setAttribute(trackingFilter, '-protocol', protocol)
    ixNet.commit()
    #ixNet getAttr $trackingFilter -availableGroupingOptions        
    ixNet.setAttribute(trackingFilter, '-grouping', drillDownType)
    ixNet.commit()
    layer23NextGenProtocolFilter = view + '/' + 'layer23NextGenProtocolFilter'        
    ixNet.setAttribute(layer23NextGenProtocolFilter, '-advancedCVFilter', trackingFilter)
    ixNet.commit()

    # Enable Stats Columns to be displayed
    statsList = ixNet.getList(view, 'statistic')
    for stat in statsList :
        ixNet.setAttribute(stat, '-enabled', 'true')

    ixNet.commit()

    # Enable Statsview
    ixNet.setAttribute(view, '-enabled', 'true')
    ixNet.commit()
	
################################################################################
# Connect to IxNet client
################################################################################

ixNet = IxNet(py.ixTclServer, int(py.ixTclPort)+3000)
ixNet.connect()
root = ixNet.getRoot()

################################################################################
# Cleaning up IxNetwork
################################################################################

print "Cleaning up IxNetwork..."
ixNet.execute('newConfig')

################################################################################
# Adding ports to configuration
################################################################################
print "Adding ports to configuration"
root = ixNet.getRoot()
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.commit()

root    = ixNet.getRoot()
vportTx1 = ixNet.getList(root, 'vport')[0]
vportRx1 = ixNet.getList(root, 'vport')[1]
vportTx2 = ixNet.getList(root, 'vport')[2]
vportRx2 = ixNet.getList(root, 'vport')[3]
vportListLAG1 = [vportTx1, vportTx2]
vportListLAG2 = [vportRx1, vportRx2]

################################################################################
# Assign ports 
################################################################################
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print "Assigning ports to " + str(vports) + " ..."
assignPorts=ixNet.execute('assignPorts',py.ports,[],vports,True )
time.sleep(10)

print("Adding topologies")
ixNet.add(root, 'topology')
ixNet.add(root, 'topology')
ixNet.commit()

topologies = ixNet.getList(ixNet.getRoot(), 'topology')
topo1 = topologies[0]
topo2 = topologies[1]
ixNet.setAttribute( topo1,'-vports', vportListLAG1)
ixNet.setAttribute( topo2,'-vports', vportListLAG2)

print "Adding 2 device groups"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

t1devices = ixNet.getList(topo1, 'deviceGroup')
t2devices = ixNet.getList(topo2, 'deviceGroup')

t1dev1 = t1devices[0]
t2dev1 = t2devices[0]

print("Configuring the multipliers (number of sessions)")
ixNet.setAttribute(t1dev1, '-multiplier', '1')
ixNet.setAttribute(t2dev1, '-multiplier', '1')
ixNet.commit()

print("Adding ethernet/mac endpoints")
ixNet.add(t1dev1, 'ethernet')
ixNet.add(t2dev1, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(t1dev1, 'ethernet')[0]
mac2 = ixNet.getList(t2dev1, 'ethernet')[0]

print("Configuring the mac addresses %s" % (mac1))
ixNet.setMultiAttribute(ixNet.getAttribute(mac1, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '00:11:01:00:00:01',
    '-step',      '00:00:01:00:00:00')

ixNet.setMultiAttribute(ixNet.getAttribute(mac2, '-mac') + '/counter',
    '-direction', 'increment',
    '-start',     '00:12:01:00:00:01',
    '-step',      '00:00:01:00:00:00')
ixNet.commit()

print("Adding LACP over Ethernet stacks")
ixNet.add(mac1, 'lacp')
ixNet.add(mac2, 'lacp')
ixNet.commit()

lacp1 = ixNet.getList(mac1, 'lacp')[0]
lacp2 = ixNet.getList(mac2, 'lacp')[0]

print("Renaming the topologies and the device groups")
ixNet.setAttribute(topo1, '-name', 'LAG1-LHS')
ixNet.setAttribute(topo2, '-name', 'LAG1-RHS')

ixNet.setAttribute(t1dev1, '-name', 'SYSTEM1-LACP-LHS')
ixNet.setAttribute(t2dev1, '-name', 'SYSTEM1-LACP-RHS')
ixNet.commit()


print("Modifying ActorSystemID and ActorKey to user defined values")
sys1LagLHS = ixNet.getList(mac1, 'lacp')[0]
sys1LagRHS = ixNet.getList(mac2, 'lacp')[0]

sys1LagLHSport1 = ixNet.getList(sys1LagLHS, 'port')[0]
sys1LagLHSport2 = ixNet.getList(sys1LagLHS, 'port')[1]
sys1LagRHSport1 = ixNet.getList(sys1LagRHS, 'port')[0]
sys1LagRHSport2 = ixNet.getList(sys1LagRHS, 'port')[1]

sys1LagLHSport1ActKey = ixNet.getAttribute(sys1LagLHSport1, '-actorKey')
sys1LagLHSport2ActKey = ixNet.getAttribute(sys1LagLHSport2, '-actorKey')
sys1LagRHSport1ActKey = ixNet.getAttribute(sys1LagRHSport1, '-actorKey')
sys1LagRHSport2ActKey = ixNet.getAttribute(sys1LagRHSport2, '-actorKey')

sys1LagLHSport1SysId = ixNet.getAttribute(sys1LagLHSport1, '-actorSystemId')
sys1LagLHSport2SysId = ixNet.getAttribute(sys1LagLHSport2, '-actorSystemId')
sys1LagRHSport1SysId = ixNet.getAttribute(sys1LagRHSport1, '-actorSystemId')
sys1LagRHSport2SysId = ixNet.getAttribute(sys1LagRHSport2, '-actorSystemId')

ixNet.setMultiAttribute(sys1LagLHSport1ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(sys1LagLHSport2ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(sys1LagRHSport1ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(sys1LagRHSport2ActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()

ixNet.setMultiAttribute(sys1LagLHSport1ActKey + '/singleValue', '-value', '666')
ixNet.setMultiAttribute(sys1LagLHSport2ActKey + '/singleValue', '-value', '666')
ixNet.setMultiAttribute(sys1LagRHSport1ActKey + '/singleValue', '-value', '777')
ixNet.setMultiAttribute(sys1LagRHSport2ActKey + '/singleValue', '-value', '777')
ixNet.commit()

ixNet.setMultiAttribute(sys1LagLHSport1SysId, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(sys1LagLHSport2SysId, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(sys1LagRHSport1SysId, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(sys1LagRHSport2SysId, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()

ixNet.setMultiAttribute(sys1LagLHSport1SysId + '/singleValue', '-value', '666')
ixNet.setMultiAttribute(sys1LagLHSport2SysId + '/singleValue', '-value', '666')
ixNet.setMultiAttribute(sys1LagRHSport1SysId + '/singleValue', '-value', '777')
ixNet.setMultiAttribute(sys1LagRHSport2SysId + '/singleValue', '-value', '777')
ixNet.commit()

################################################################################
# Start LACP protocol and wait for 60 seconds                                  #
################################################################################
print("Starting LACP and waiting for 60 seconds for sessions to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)


################################################################################
# Disable Synchronization flag on port1 in System1-LACP-LHS                    #
################################################################################
print ("\n\nDisable Synchronization flag on port1 in System1-LACP-LHS")
sys1LagLHSport1SyncFlag = ixNet.getAttribute(sys1LagLHSport1, '-synchronizationFlag')
ixNet.setMultiAttribute(sys1LagLHSport1SyncFlag, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(sys1LagLHSport1SyncFlag + '/singleValue', '-value', 'false')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
ixNet.execute('applyOnTheFly', topology)

time.sleep(5)

################################################################################
# Re-enable Synchronization flag on port1 in System1-LACP-LHS                  #
################################################################################
print ("\n\n Re-enable Synchronization flag on port1 in System1-LACP-LHS")
sys1LagLHSport1SyncFlag = ixNet.getAttribute(sys1LagLHSport1, '-synchronizationFlag')
ixNet.setMultiAttribute(sys1LagLHSport1SyncFlag, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(sys1LagLHSport1SyncFlag + '/singleValue', '-value', 'true')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
ixNet.execute('applyOnTheFly', topology)
time.sleep(5)



################################################################################
# Stop all protocols                                                           #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')
