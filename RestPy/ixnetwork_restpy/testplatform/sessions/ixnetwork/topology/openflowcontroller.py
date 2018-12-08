
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


class OpenFlowController(Base):
	"""The OpenFlowController class encapsulates a user managed openFlowController node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpenFlowController property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'openFlowController'

	def __init__(self, parent):
		super(OpenFlowController, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)

	@property
	def LearnedInfoUpdate(self):
		"""An instance of the LearnedInfoUpdate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfoupdate.LearnedInfoUpdate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfoupdate import LearnedInfoUpdate
		return LearnedInfoUpdate(self)

	@property
	def OpenFlowChannel(self):
		"""An instance of the OpenFlowChannel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.openflowchannel.OpenFlowChannel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.openflowchannel import OpenFlowChannel
		return OpenFlowChannel(self)

	@property
	def AcceptUnconfiguredChannel(self):
		"""If selected, un-configured channels are accepted for this interface.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('acceptUnconfiguredChannel')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AuxConnTimeout(self):
		"""The inactive time in milliseconds after which the auxiliary connection will timeout and close.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxConnTimeout')

	@property
	def AuxNonHelloStartupOption(self):
		"""Specify the action from the following options for non-hello message when connection is established. The options are: 1) Accept Connection 2) Return Error

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxNonHelloStartupOption')

	@property
	def BadVersionErrorAction(self):
		"""Specify the action to be performed when an invalid version error occurs. The options are: 1) Re-send Hello 2) Terminate Connection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('badVersionErrorAction')

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
	def ControllerLocalIp(self):
		"""The local IP address of the interface. This field is auto-populated and cannot be changed.

		Returns:
			list(str)
		"""
		return self._get_attribute('controllerLocalIp')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DelFlowsAtStartup(self):
		"""If selected, Controller sends an OpenFlow delete message (for all wild card entries) at start-up. This deletes all existing flows in the DUT.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delFlowsAtStartup')

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
	def EchoInterval(self):
		"""The periodic interval in seconds at which the Interface sends Echo Request Packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoInterval')

	@property
	def EchoTimeOut(self):
		"""If selected, the echo request times out when they have been sent for a specified number of times, or when the time value specified has lapsed, but no response is received

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoTimeOut')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FeatRequestTimeout(self):
		"""The inactive time in milliseconds after which the feature request will timeout.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('featRequestTimeout')

	@property
	def FeatureRquestTimeoutAction(self):
		"""Specify the action to be performed when a feature request times out. The options are: 1) Re-send Feature Request 2) Terminate Connection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('featureRquestTimeoutAction')

	@property
	def FileCaCertificate(self):
		"""Browse and upload a CA Certificate file for TLS session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCaCertificate')

	@property
	def FileCertificate(self):
		"""Browse and upload the certificate file for TLS session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fileCertificate')

	@property
	def FilePrivKey(self):
		"""Browse and upload the private key file for TLS session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filePrivKey')

	@property
	def InstallFlowForLLDP(self):
		"""If selected, the controller sends add flow to each connected switch in such a way that each switch forwards LLDP packet to all other connected switches.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('installFlowForLLDP')

	@property
	def InstallLLDPFlow(self):
		"""If selected, LLDP Flow is installed.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('installLLDPFlow')

	@property
	def LLDPDestinactionMac(self):
		"""Specify the LLDP Destination MAC address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lLDPDestinactionMac')

	@property
	def LldpDstMacAddress(self):
		"""The destination MAC Address for the LLDP packet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lldpDstMacAddress')

	@property
	def ModeOfConnection(self):
		"""The mode of connection used for the Interface. Options include: 1) Active 2) Passive 3) Mixed

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('modeOfConnection')

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
	def NumberOfChannels(self):
		"""Total number of OpenFlow channels to be added for this protocol interface.

		Returns:
			number
		"""
		return self._get_attribute('numberOfChannels')
	@NumberOfChannels.setter
	def NumberOfChannels(self, value):
		self._set_attribute('numberOfChannels', value)

	@property
	def PeriodicEcho(self):
		"""If selected, the Interface sends echo requests periodically to keep the OpenFlow session connected.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicEcho')

	@property
	def PeriodicLLDP(self):
		"""If selected, the interface sends LLDP packets periodically to discover new links.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicLLDP')

	@property
	def PeriodicLLDPInterval(self):
		"""The periodic interval in milliseconds at which the Interface sends LLDP packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicLLDPInterval')

	@property
	def ResponseTimeout(self):
		"""The time in milliseconds after which the trigger request times out, if no response is received

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('responseTimeout')

	@property
	def SendPortFeatureAtStartup(self):
		"""If selected, port Description request is sent when the connection is established

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendPortFeatureAtStartup')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SetAsyncConfig(self):
		"""Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters

		Returns:
			bool
		"""
		return self._get_attribute('setAsyncConfig')
	@SetAsyncConfig.setter
	def SetAsyncConfig(self, value):
		self._set_attribute('setAsyncConfig', value)

	@property
	def SetSwitchConfig(self):
		"""Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters

		Returns:
			bool
		"""
		return self._get_attribute('setSwitchConfig')
	@SetSwitchConfig.setter
	def SetSwitchConfig(self, value):
		self._set_attribute('setSwitchConfig', value)

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
	def StartupEmptyTableFeatureRequest(self):
		"""If selected, the Table Feature Request is sent at start up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startupEmptyTableFeatureRequest')

	@property
	def StartupFeatureRequest(self):
		"""If selected, port feature request is sent when the connection is established.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startupFeatureRequest')

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
	def TcpPort(self):
		"""Specify the TCP port for this interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tcpPort')

	@property
	def TimeoutOption(self):
		"""The types of timeout options supported. Choose one of the following: 1) Multiplier 2) Timeout Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutOption')

	@property
	def TimeoutOptionValue(self):
		"""The value specified for the selected Timeout option.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutOptionValue')

	@property
	def TlsVersion(self):
		"""TLS version selection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tlsVersion')

	@property
	def TriggerLldp(self):
		"""If selected, LLDP is triggered

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('triggerLldp')

	@property
	def TypeOfConnection(self):
		"""The type of connection used for the Interface. Options include: 1) TCP 2) TLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('typeOfConnection')

	@property
	def Version(self):
		"""Implementation Version

		Returns:
			number
		"""
		return self._get_attribute('version')

	@property
	def VersionSupported(self):
		"""Indicates the supported OpenFlow version number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('versionSupported')

	def add(self, ConnectedVia=None, Multiplier=None, Name=None, NumberOfChannels=None, SetAsyncConfig=None, SetSwitchConfig=None, StackedLayers=None):
		"""Adds a new openFlowController node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfChannels (number): Total number of OpenFlow channels to be added for this protocol interface.
			SetAsyncConfig (bool): Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters
			SetSwitchConfig (bool): Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved openFlowController data using find and the newly added openFlowController data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the openFlowController data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, ControllerLocalIp=None, Count=None, DescriptiveName=None, Errors=None, Multiplier=None, Name=None, NumberOfChannels=None, SessionStatus=None, SetAsyncConfig=None, SetSwitchConfig=None, StackedLayers=None, StateCounts=None, Status=None, Version=None):
		"""Finds and retrieves openFlowController data from the server.

		All named parameters support regex and can be used to selectively retrieve openFlowController data from the server.
		By default the find method takes no parameters and will retrieve all openFlowController data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			ControllerLocalIp (list(str)): The local IP address of the interface. This field is auto-populated and cannot be changed.
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfChannels (number): Total number of OpenFlow channels to be added for this protocol interface.
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			SetAsyncConfig (bool): Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters
			SetSwitchConfig (bool): Un-checked state means getting the async config, Checked means setting asynchronous config with available parameters
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
			Version (number): Implementation Version

		Returns:
			self: This instance with matching openFlowController data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of openFlowController data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the openFlowController data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, AcceptUnconfiguredChannel=None, Active=None, AuxConnTimeout=None, AuxNonHelloStartupOption=None, BadVersionErrorAction=None, DelFlowsAtStartup=None, DirectoryName=None, EchoInterval=None, EchoTimeOut=None, FeatRequestTimeout=None, FeatureRquestTimeoutAction=None, FileCaCertificate=None, FileCertificate=None, FilePrivKey=None, InstallFlowForLLDP=None, InstallLLDPFlow=None, LLDPDestinactionMac=None, LldpDstMacAddress=None, ModeOfConnection=None, PeriodicEcho=None, PeriodicLLDP=None, PeriodicLLDPInterval=None, ResponseTimeout=None, SendPortFeatureAtStartup=None, StartupEmptyTableFeatureRequest=None, StartupFeatureRequest=None, TcpPort=None, TimeoutOption=None, TimeoutOptionValue=None, TlsVersion=None, TriggerLldp=None, TypeOfConnection=None, VersionSupported=None):
		"""Base class infrastructure that gets a list of openFlowController device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AcceptUnconfiguredChannel (str): optional regex of acceptUnconfiguredChannel
			Active (str): optional regex of active
			AuxConnTimeout (str): optional regex of auxConnTimeout
			AuxNonHelloStartupOption (str): optional regex of auxNonHelloStartupOption
			BadVersionErrorAction (str): optional regex of badVersionErrorAction
			DelFlowsAtStartup (str): optional regex of delFlowsAtStartup
			DirectoryName (str): optional regex of directoryName
			EchoInterval (str): optional regex of echoInterval
			EchoTimeOut (str): optional regex of echoTimeOut
			FeatRequestTimeout (str): optional regex of featRequestTimeout
			FeatureRquestTimeoutAction (str): optional regex of featureRquestTimeoutAction
			FileCaCertificate (str): optional regex of fileCaCertificate
			FileCertificate (str): optional regex of fileCertificate
			FilePrivKey (str): optional regex of filePrivKey
			InstallFlowForLLDP (str): optional regex of installFlowForLLDP
			InstallLLDPFlow (str): optional regex of installLLDPFlow
			LLDPDestinactionMac (str): optional regex of lLDPDestinactionMac
			LldpDstMacAddress (str): optional regex of lldpDstMacAddress
			ModeOfConnection (str): optional regex of modeOfConnection
			PeriodicEcho (str): optional regex of periodicEcho
			PeriodicLLDP (str): optional regex of periodicLLDP
			PeriodicLLDPInterval (str): optional regex of periodicLLDPInterval
			ResponseTimeout (str): optional regex of responseTimeout
			SendPortFeatureAtStartup (str): optional regex of sendPortFeatureAtStartup
			StartupEmptyTableFeatureRequest (str): optional regex of startupEmptyTableFeatureRequest
			StartupFeatureRequest (str): optional regex of startupFeatureRequest
			TcpPort (str): optional regex of tcpPort
			TimeoutOption (str): optional regex of timeoutOption
			TimeoutOptionValue (str): optional regex of timeoutOptionValue
			TlsVersion (str): optional regex of tlsVersion
			TriggerLldp (str): optional regex of triggerLldp
			TypeOfConnection (str): optional regex of typeOfConnection
			VersionSupported (str): optional regex of versionSupported

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def ClearAllLearnedInfo(self):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, Arg2):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear OF Channels learnt by this Controller.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Channel into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Get OF Channel Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, SessionIndices):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Get OF Channel Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, SessionIndices):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Get OF Channel Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, Arg2):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Gets OF Channels learnt by this Controller.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Channel into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Get OF Topology Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, SessionIndices):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Get OF Topology Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, SessionIndices):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Get OF Topology Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetOFTopologyLearnedInfo', payload=locals(), response_object=None)

	def GetOFTopologyLearnedInfo(self, Arg2):
		"""Executes the getOFTopologyLearnedInfo operation on the server.

		Gets OF Topology learnt by this Controller.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF session into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetOFTopologyLearnedInfo', payload=locals(), response_object=None)

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

	def SendLLDPPacketOut(self, LldpDestination, EnableLldpFlowAdd, LldpTimeoutVal):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			LldpDestination (str): This parameter requires a lldpDestination of type kString
			EnableLldpFlowAdd (bool): This parameter requires a enableLldpFlowAdd of type kBool
			LldpTimeoutVal (number): This parameter requires a lldpTimeoutVal of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SendLLDPPacketOut', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, LldpDestination, EnableLldpFlowAdd, LldpTimeoutVal, SessionIndices):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			LldpDestination (str): This parameter requires a lldpDestination of type kString
			EnableLldpFlowAdd (bool): This parameter requires a enableLldpFlowAdd of type kBool
			LldpTimeoutVal (number): This parameter requires a lldpTimeoutVal of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SendLLDPPacketOut', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, SessionIndices, LldpDestination, EnableLldpFlowAdd, LldpTimeoutVal):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a lldpDestination of type kString
			LldpDestination (str): This parameter requires a enableLldpFlowAdd of type kBool
			EnableLldpFlowAdd (bool): This parameter requires a lldpTimeoutVal of type kInteger
			LldpTimeoutVal (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SendLLDPPacketOut', payload=locals(), response_object=None)

	def SendLLDPPacketOut(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the sendLLDPPacketOut operation on the server.

		Send LLDP Packet Out to all Switches.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (str): LLDP Destination MAC
			Arg4 (bool): Enable LLDP Flow Add in Switch
			Arg5 (number): LLDP Timeout Value

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendLLDPPacketOut', payload=locals(), response_object=None)

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

	def StartController(self):
		"""Executes the startController operation on the server.

		Start OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartController', payload=locals(), response_object=None)

	def StartController(self, SessionIndices):
		"""Executes the startController operation on the server.

		Start OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartController', payload=locals(), response_object=None)

	def StartController(self, SessionIndices):
		"""Executes the startController operation on the server.

		Start OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartController', payload=locals(), response_object=None)

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

	def StopController(self):
		"""Executes the stopController operation on the server.

		Stop OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopController', payload=locals(), response_object=None)

	def StopController(self, SessionIndices):
		"""Executes the stopController operation on the server.

		Stop OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopController', payload=locals(), response_object=None)

	def StopController(self, SessionIndices):
		"""Executes the stopController operation on the server.

		Stop OpenFlow Controller

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopController', payload=locals(), response_object=None)
