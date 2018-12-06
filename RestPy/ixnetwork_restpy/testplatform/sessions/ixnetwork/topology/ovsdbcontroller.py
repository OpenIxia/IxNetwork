
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ovsdbcontroller(Base):
	"""The Ovsdbcontroller class encapsulates a user managed ovsdbcontroller node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ovsdbcontroller property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ovsdbcontroller'

	def __init__(self, parent):
		super(Ovsdbcontroller, self).__init__(parent)

	@property
	def ClusterData(self):
		"""An instance of the ClusterData class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.clusterdata.ClusterData)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.clusterdata import ClusterData
		return ClusterData(self)._select()

	@property
	def Connector(self):
		"""An instance of the Connector class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return Connector(self)

	@property
	def ClearDumpDbFiles(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clearDumpDbFiles')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

	@property
	def ConnectionType(self):
		"""Connection should use TCP or TLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('connectionType')

	@property
	def ControllerTcpPort(self):
		"""Specify the TCP port for the Controller

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('controllerTcpPort')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DirectoryName(self):
		"""Location of Directory in Client where the Certificate and Key Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('directoryName')

	@property
	def DumpdbDirectoryName(self):
		"""Location of Directory in Client where the DumpDb Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dumpdbDirectoryName')

	@property
	def EnableLogging(self):
		"""If true, Port debug logs will be recorded, Maximum recording will be upto 500 MB .

		Returns:
			bool
		"""
		return self._get_attribute('enableLogging')
	@EnableLogging.setter
	def EnableLogging(self, value):
		self._set_attribute('enableLogging', value)

	@property
	def EnableOvsdbServerIp(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableOvsdbServerIp')

	@property
	def ErrorCode(self):
		"""Error Code

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorDesc(self):
		"""Description of Error occured

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorDesc')

	@property
	def ErrorLogDirectoryName(self):
		"""Location of Directory in Client where the ErrorLog Files are available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorLogDirectoryName')

	@property
	def ErrorLogicalSwitchName(self):
		"""Error occured for this Logical Switch Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorLogicalSwitchName')

	@property
	def ErrorPhysicalSwitchName(self):
		"""Error occured for this Physical Switch Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorPhysicalSwitchName')

	@property
	def ErrorTimeStamp(self):
		"""Time Stamp at which Last Error occurred

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('errorTimeStamp')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FileCaCertificate(self):
		"""CA Certificate File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCaCertificate')

	@property
	def FileCertificate(self):
		"""Certificate File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCertificate')

	@property
	def FileHWGatewayCertificate(self):
		"""HW Gateway Certificate File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileHWGatewayCertificate')

	@property
	def FilePrivKey(self):
		"""Private Key File

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filePrivKey')

	@property
	def HSCConfiguration(self):
		"""Each VTEP has its own Hardware Switch Controller.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hSCConfiguration')

	@property
	def LatestDumpDbFileNames(self):
		"""Api to fetch latest DumpDb Files

		Returns:
			str
		"""
		return self._get_attribute('latestDumpDbFileNames')
	@LatestDumpDbFileNames.setter
	def LatestDumpDbFileNames(self, value):
		self._set_attribute('latestDumpDbFileNames', value)

	@property
	def LatestErrorFileNames(self):
		"""Api to fetch latest Error Files

		Returns:
			str
		"""
		return self._get_attribute('latestErrorFileNames')
	@LatestErrorFileNames.setter
	def LatestErrorFileNames(self, value):
		self._set_attribute('latestErrorFileNames', value)

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def OvsdbSchema(self):
		"""Database schema

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ovsdbSchema')

	@property
	def OvsdbServerIp(self):
		"""The IP address of the DUT or Ovs Server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ovsdbServerIp')

	@property
	def PseudoConnectedTo(self):
		"""GUI-only connection

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('pseudoConnectedTo')
	@PseudoConnectedTo.setter
	def PseudoConnectedTo(self, value):
		self._set_attribute('pseudoConnectedTo', value)

	@property
	def PseudoConnectedToBfd(self):
		"""GUI-only connection

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('pseudoConnectedToBfd')
	@PseudoConnectedToBfd.setter
	def PseudoConnectedToBfd(self, value):
		self._set_attribute('pseudoConnectedToBfd', value)

	@property
	def PseudoConnectedToVxlanReplicator(self):
		"""GUI-only connection

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('pseudoConnectedToVxlanReplicator')
	@PseudoConnectedToVxlanReplicator.setter
	def PseudoConnectedToVxlanReplicator(self, value):
		self._set_attribute('pseudoConnectedToVxlanReplicator', value)

	@property
	def PseudoMultiplier(self):
		"""Multiplier for GUI-only connection

		Returns:
			number
		"""
		return self._get_attribute('pseudoMultiplier')

	@property
	def PseudoMultiplierBfd(self):
		"""Multiplier for GUI-only connection

		Returns:
			number
		"""
		return self._get_attribute('pseudoMultiplierBfd')

	@property
	def PseudoMultiplierVxlanReplicator(self):
		"""Multiplier for GUI-only connection

		Returns:
			number
		"""
		return self._get_attribute('pseudoMultiplierVxlanReplicator')

	@property
	def Role(self):
		"""The role of the OVSDB Controller.

		Returns:
			list(str[master|none|slave])
		"""
		return self._get_attribute('role')

	@property
	def ServerAddDeleteConnectionError(self):
		"""API to retrieve error occured while Adding/ Deleting Server

		Returns:
			str
		"""
		return self._get_attribute('serverAddDeleteConnectionError')
	@ServerAddDeleteConnectionError.setter
	def ServerAddDeleteConnectionError(self, value):
		self._set_attribute('serverAddDeleteConnectionError', value)

	@property
	def ServerAddDeleteStatus(self):
		"""Status of all servers Added/Deleted to Controller. Use Get Server Add/Delete Status, right click action to get current status

		Returns:
			str
		"""
		return self._get_attribute('serverAddDeleteStatus')

	@property
	def ServerConnectionIp(self):
		"""The IP address of the DUT or Ovs Server which needs to be Added/Deleted.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serverConnectionIp')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def TableNames(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableNames')

	@property
	def TimeOut(self):
		"""Transact request Time Out in seconds. For scale scenarios increase this Timeout value.

		Returns:
			number
		"""
		return self._get_attribute('timeOut')
	@TimeOut.setter
	def TimeOut(self, value):
		self._set_attribute('timeOut', value)

	@property
	def VerifyHWGatewayCertificate(self):
		"""Verify HW Gateway Certificate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('verifyHWGatewayCertificate')

	@property
	def VerifyPeerCertificate(self):
		"""Verify Peer Certificate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('verifyPeerCertificate')

	@property
	def Vxlan(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('vxlan')
	@Vxlan.setter
	def Vxlan(self, value):
		self._set_attribute('vxlan', value)

	@property
	def VxlanReplicator(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('vxlanReplicator')
	@VxlanReplicator.setter
	def VxlanReplicator(self, value):
		self._set_attribute('vxlanReplicator', value)

	def add(self, ConnectedVia=None, EnableLogging=None, LatestDumpDbFileNames=None, LatestErrorFileNames=None, Multiplier=None, Name=None, PseudoConnectedTo=None, PseudoConnectedToBfd=None, PseudoConnectedToVxlanReplicator=None, ServerAddDeleteConnectionError=None, StackedLayers=None, TimeOut=None, Vxlan=None, VxlanReplicator=None):
		"""Adds a new ovsdbcontroller node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableLogging (bool): If true, Port debug logs will be recorded, Maximum recording will be upto 500 MB .
			LatestDumpDbFileNames (str): Api to fetch latest DumpDb Files
			LatestErrorFileNames (str): Api to fetch latest Error Files
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			PseudoConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): GUI-only connection
			PseudoConnectedToBfd (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): GUI-only connection
			PseudoConnectedToVxlanReplicator (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): GUI-only connection
			ServerAddDeleteConnectionError (str): API to retrieve error occured while Adding/ Deleting Server
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			TimeOut (number): Transact request Time Out in seconds. For scale scenarios increase this Timeout value.
			Vxlan (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): 
			VxlanReplicator (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): 

		Returns:
			self: This instance with all currently retrieved ovsdbcontroller data using find and the newly added ovsdbcontroller data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ovsdbcontroller data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, EnableLogging=None, Errors=None, LatestDumpDbFileNames=None, LatestErrorFileNames=None, Multiplier=None, Name=None, PseudoConnectedTo=None, PseudoConnectedToBfd=None, PseudoConnectedToVxlanReplicator=None, PseudoMultiplier=None, PseudoMultiplierBfd=None, PseudoMultiplierVxlanReplicator=None, Role=None, ServerAddDeleteConnectionError=None, ServerAddDeleteStatus=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None, TimeOut=None, Vxlan=None, VxlanReplicator=None):
		"""Finds and retrieves ovsdbcontroller data from the server.

		All named parameters support regex and can be used to selectively retrieve ovsdbcontroller data from the server.
		By default the find method takes no parameters and will retrieve all ovsdbcontroller data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableLogging (bool): If true, Port debug logs will be recorded, Maximum recording will be upto 500 MB .
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			LatestDumpDbFileNames (str): Api to fetch latest DumpDb Files
			LatestErrorFileNames (str): Api to fetch latest Error Files
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			PseudoConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): GUI-only connection
			PseudoConnectedToBfd (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): GUI-only connection
			PseudoConnectedToVxlanReplicator (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): GUI-only connection
			PseudoMultiplier (number): Multiplier for GUI-only connection
			PseudoMultiplierBfd (number): Multiplier for GUI-only connection
			PseudoMultiplierVxlanReplicator (number): Multiplier for GUI-only connection
			Role (list(str[master|none|slave])): The role of the OVSDB Controller.
			ServerAddDeleteConnectionError (str): API to retrieve error occured while Adding/ Deleting Server
			ServerAddDeleteStatus (str): Status of all servers Added/Deleted to Controller. Use Get Server Add/Delete Status, right click action to get current status
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
			TimeOut (number): Transact request Time Out in seconds. For scale scenarios increase this Timeout value.
			Vxlan (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): 
			VxlanReplicator (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): 

		Returns:
			self: This instance with matching ovsdbcontroller data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ovsdbcontroller data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ovsdbcontroller data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, ClearDumpDbFiles=None, ConnectionType=None, ControllerTcpPort=None, DirectoryName=None, DumpdbDirectoryName=None, EnableOvsdbServerIp=None, ErrorCode=None, ErrorDesc=None, ErrorLogDirectoryName=None, ErrorLogicalSwitchName=None, ErrorPhysicalSwitchName=None, ErrorTimeStamp=None, FileCaCertificate=None, FileCertificate=None, FileHWGatewayCertificate=None, FilePrivKey=None, HSCConfiguration=None, OvsdbSchema=None, OvsdbServerIp=None, ServerConnectionIp=None, TableNames=None, VerifyHWGatewayCertificate=None, VerifyPeerCertificate=None):
		"""Base class infrastructure that gets a list of ovsdbcontroller device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ClearDumpDbFiles (str): optional regex of clearDumpDbFiles
			ConnectionType (str): optional regex of connectionType
			ControllerTcpPort (str): optional regex of controllerTcpPort
			DirectoryName (str): optional regex of directoryName
			DumpdbDirectoryName (str): optional regex of dumpdbDirectoryName
			EnableOvsdbServerIp (str): optional regex of enableOvsdbServerIp
			ErrorCode (str): optional regex of errorCode
			ErrorDesc (str): optional regex of errorDesc
			ErrorLogDirectoryName (str): optional regex of errorLogDirectoryName
			ErrorLogicalSwitchName (str): optional regex of errorLogicalSwitchName
			ErrorPhysicalSwitchName (str): optional regex of errorPhysicalSwitchName
			ErrorTimeStamp (str): optional regex of errorTimeStamp
			FileCaCertificate (str): optional regex of fileCaCertificate
			FileCertificate (str): optional regex of fileCertificate
			FileHWGatewayCertificate (str): optional regex of fileHWGatewayCertificate
			FilePrivKey (str): optional regex of filePrivKey
			HSCConfiguration (str): optional regex of hSCConfiguration
			OvsdbSchema (str): optional regex of ovsdbSchema
			OvsdbServerIp (str): optional regex of ovsdbServerIp
			ServerConnectionIp (str): optional regex of serverConnectionIp
			TableNames (str): optional regex of tableNames
			VerifyHWGatewayCertificate (str): optional regex of verifyHWGatewayCertificate
			VerifyPeerCertificate (str): optional regex of verifyPeerCertificate

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def AddServer(self, Arg2):
		"""Executes the addServer operation on the server.

		Add Server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Add Server.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddServer', payload=locals(), response_object=None)

	def ClearLastErrors(self, Arg2):
		"""Executes the clearLastErrors operation on the server.

		Clear Error Messages reported due to Last Action.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to clear last reported error messages.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearLastErrors', payload=locals(), response_object=None)

	def ClearPortLogs(self, Arg2):
		"""Executes the clearPortLogs operation on the server.

		Add Server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Add Server.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearPortLogs', payload=locals(), response_object=None)

	def ControllerDumpDB(self, Arg2):
		"""Executes the controllerDumpDB operation on the server.

		Command to fetch Tor Information stored internally.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ControllerDumpDB', payload=locals(), response_object=None)

	def DeleteServer(self, Arg2):
		"""Executes the deleteServer operation on the server.

		Delete Server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Delete Server.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DeleteServer', payload=locals(), response_object=None)

	def DumpDB(self, Arg2):
		"""Executes the dumpDB operation on the server.

		Attach.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DumpDB', payload=locals(), response_object=None)

	def GetServerAddDeleteStatus(self, Arg2):
		"""Executes the getServerAddDeleteStatus operation on the server.

		Get Server Status.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to get Server Status.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetServerAddDeleteStatus', payload=locals(), response_object=None)

	def RestartDown(self):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
