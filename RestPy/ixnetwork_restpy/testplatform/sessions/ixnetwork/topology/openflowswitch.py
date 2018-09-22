from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpenFlowSwitch(Base):
	"""The OpenFlowSwitch class encapsulates a user managed openFlowSwitch node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpenFlowSwitch property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'openFlowSwitch'

	def __init__(self, parent):
		super(OpenFlowSwitch, self).__init__(parent)

	@property
	def OFSwitchChannel(self):
		"""An instance of the OFSwitchChannel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchchannel.OFSwitchChannel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchchannel import OFSwitchChannel
		return OFSwitchChannel(self)

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
	def OFSwitchLearnedInfoConfig(self):
		"""An instance of the OFSwitchLearnedInfoConfig class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchlearnedinfoconfig.OFSwitchLearnedInfoConfig)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchlearnedinfoconfig import OFSwitchLearnedInfoConfig
		return OFSwitchLearnedInfoConfig(self)._select()

	@property
	def OfSwitchPorts(self):
		"""An instance of the OfSwitchPorts class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchports.OfSwitchPorts)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchports import OfSwitchPorts
		return OfSwitchPorts(self)._select()

	@property
	def PacketInList(self):
		"""An instance of the PacketInList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.packetinlist.PacketInList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.packetinlist import PacketInList
		return PacketInList(self)

	@property
	def SwitchGroupsList(self):
		"""An instance of the SwitchGroupsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.switchgroupslist.SwitchGroupsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.switchgroupslist import SwitchGroupsList
		return SwitchGroupsList(self)

	@property
	def SwitchTablesList(self):
		"""An instance of the SwitchTablesList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.switchtableslist.SwitchTablesList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.switchtableslist import SwitchTablesList
		return SwitchTablesList(self)

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
	def BandTypes(self):
		"""Select meter band types from the list

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandTypes')

	@property
	def BarrierReplyDelayType(self):
		"""Select the Barrier Reply Delay Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('barrierReplyDelayType')

	@property
	def BarrierReplyMaxDelay(self):
		"""Configure Barrier Reply Max Delay in milli seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('barrierReplyMaxDelay')

	@property
	def Capabilities(self):
		"""Capabilities

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilities')

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
	def ControllerFlowTxRate(self):
		"""If selected, statistics is published showing the rate at which Flows are transmitted per second, by the Controller

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('controllerFlowTxRate')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DatapathDesc(self):
		"""The description of the Data Path used.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('datapathDesc')

	@property
	def DatapathId(self):
		"""The Datapath ID of the OF Channel.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('datapathId')

	@property
	def DatapathIdHex(self):
		"""The Datapath ID in Hex of the OF Channel.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('datapathIdHex')

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
	def EnableHelloElement(self):
		"""Enable Hello Element

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHelloElement')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

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
	def FlowRemovedMask(self):
		"""Specify the flow removed message types that will not be received when the controller has the Master role

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowRemovedMask')

	@property
	def FlowRemovedMaskSlave(self):
		"""Specify the flow removed message types that will not be received when the controller has the Slave role

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowRemovedMaskSlave')

	@property
	def GroupCapabilities(self):
		"""Group configuration flags: Weight:Support weight for select groups. Liveness:Support liveness for select groups. Chaining:Support chaining groups. Check Loops:Check chaining for loops and delete.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCapabilities')

	@property
	def GroupType(self):
		"""Can be of the following types per switch: 1)All: Execute all buckets in the group. 2)Select:Execute one bucket in the group. 3)Indirect:Execute the one defined bucket in this group. 4)Fast Failover:Execute the first live bucket.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupType')

	@property
	def HardwareDesc(self):
		"""The description of the hardware used.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hardwareDesc')

	@property
	def InterPacketInBurstGap(self):
		"""Specify the duration (in milliseconds) for which the switch waits between successive packet-in bursts.The default value is 1,000 milliseconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interPacketInBurstGap')

	@property
	def ManufacturerDesc(self):
		"""The description of the manufacturer. The default value is Ixia.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('manufacturerDesc')

	@property
	def MaxBandPerMeter(self):
		"""Maximum number of bands per meter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxBandPerMeter')

	@property
	def MaxColorValue(self):
		"""Maximum Color Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxColorValue')

	@property
	def MaxNumberOfBucketsPerGroups(self):
		"""To specify the maximum number of group buckets each group can have.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxNumberOfBucketsPerGroups')

	@property
	def MaxPacketInBytes(self):
		"""The maximum length of the Packet-in messages in bytes.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxPacketInBytes')

	@property
	def MeterCapabilities(self):
		"""Select meter capabilities from the list

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('meterCapabilities')

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
	def NumMeter(self):
		"""Maximum number of Openflow meters configured for the switch

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numMeter')

	@property
	def NumberOfBuffers(self):
		"""Specify the maximum number of packets the switch can buffer when sending packets to the controller using packet-in messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfBuffers')

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
	def NumberOfHostPorts(self):
		"""Number of Host Ports per Switch

		Returns:
			number
		"""
		return self._get_attribute('numberOfHostPorts')

	@property
	def NumberOfPacketIn(self):
		"""Specify the number of packet-in ranges supported by the switch.The maximum allowed value is 10 ranges.

		Returns:
			number
		"""
		return self._get_attribute('numberOfPacketIn')
	@NumberOfPacketIn.setter
	def NumberOfPacketIn(self, value):
		self._set_attribute('numberOfPacketIn', value)

	@property
	def NumberOfPorts(self):
		"""Number of Ports per Switch

		Returns:
			number
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def NumberOfTableRanges(self):
		"""Number of Tables per Switch

		Returns:
			number
		"""
		return self._get_attribute('numberOfTableRanges')
	@NumberOfTableRanges.setter
	def NumberOfTableRanges(self, value):
		self._set_attribute('numberOfTableRanges', value)

	@property
	def NumberOfTopologyPorts(self):
		"""Number of Topology Ports per Switch

		Returns:
			number
		"""
		return self._get_attribute('numberOfTopologyPorts')

	@property
	def NumberOfUnconnectedPorts(self):
		"""Number of Unconnected Ports per Switch

		Returns:
			number
		"""
		return self._get_attribute('numberOfUnconnectedPorts')
	@NumberOfUnconnectedPorts.setter
	def NumberOfUnconnectedPorts(self, value):
		self._set_attribute('numberOfUnconnectedPorts', value)

	@property
	def PacketInMaskMaster(self):
		"""Packet In Mask Master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInMaskMaster')

	@property
	def PacketInMaskSlave(self):
		"""Packet In Mask Slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInMaskSlave')

	@property
	def PacketInReplyDelay(self):
		"""If selected, delay between packet-in and the corresponding packet-out or flow mod is published.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInReplyDelay')

	@property
	def PacketInReplyTimeout(self):
		"""The amount of time, in seconds, that the switch keeps the packet-in message in buffer, if it does not receive any corresponding packet-out or flow mod.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInReplyTimeout')

	@property
	def PacketInTxBurst(self):
		"""Specify the number of packet-in transmitting packets that can be sent in a single burst within the time frame specified by the Inter PacketIn Burst Gap value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInTxBurst')

	@property
	def PacketOutRxRate(self):
		"""If selected, packet_out rx rate and packet_in tx rate is calculated for the switch.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetOutRxRate')

	@property
	def PeriodicEcho(self):
		"""If selected, the Interface sends echo requests periodically to keep the OpenFlow session connected.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicEcho')

	@property
	def PortStatusMaskMaster(self):
		"""Port Status Mask Master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portStatusMaskMaster')

	@property
	def PortStatusMaskSlave(self):
		"""Port Status Mask Slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portStatusMaskSlave')

	@property
	def SerialNumber(self):
		"""The serial number used.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serialNumber')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SoftwareDesc(self):
		"""The description of the software used.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('softwareDesc')

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
	def StoreFlows(self):
		"""If selected, the flow information sent by the Controller are learned by the Switch.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('storeFlows')

	@property
	def SwitchDesc(self):
		"""A description of the Switch

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('switchDesc')

	@property
	def SwitchLocalIp(self):
		"""The local IP address of the interface. This field is auto-populated and cannot be changed.

		Returns:
			list(str)
		"""
		return self._get_attribute('switchLocalIp')

	@property
	def TableMissAction(self):
		"""Specify what the Switch should do when there is no match for the packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableMissAction')

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
	def TransactionID(self):
		"""If selected, PacketIn Delay Calculation will be done by matching transaction ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('transactionID')

	@property
	def TypeOfConnection(self):
		"""The type of connection used for the Interface. Options include: 1) TCP 2) TLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('typeOfConnection')

	@property
	def VersionSupported(self):
		"""Indicates the supported OpenFlow version number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('versionSupported')

	def add(self, ConnectedVia=None, Multiplier=None, Name=None, NumberOfChannels=None, NumberOfPacketIn=None, NumberOfTableRanges=None, NumberOfUnconnectedPorts=None, StackedLayers=None):
		"""Adds a new openFlowSwitch node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfChannels (number): Total number of OpenFlow channels to be added for this protocol interface.
			NumberOfPacketIn (number): Specify the number of packet-in ranges supported by the switch.The maximum allowed value is 10 ranges.
			NumberOfTableRanges (number): Number of Tables per Switch
			NumberOfUnconnectedPorts (number): Number of Unconnected Ports per Switch
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved openFlowSwitch data using find and the newly added openFlowSwitch data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the openFlowSwitch data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, Multiplier=None, Name=None, NumberOfChannels=None, NumberOfHostPorts=None, NumberOfPacketIn=None, NumberOfPorts=None, NumberOfTableRanges=None, NumberOfTopologyPorts=None, NumberOfUnconnectedPorts=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None, SwitchLocalIp=None):
		"""Finds and retrieves openFlowSwitch data from the server.

		All named parameters support regex and can be used to selectively retrieve openFlowSwitch data from the server.
		By default the find method takes no parameters and will retrieve all openFlowSwitch data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfChannels (number): Total number of OpenFlow channels to be added for this protocol interface.
			NumberOfHostPorts (number): Number of Host Ports per Switch
			NumberOfPacketIn (number): Specify the number of packet-in ranges supported by the switch.The maximum allowed value is 10 ranges.
			NumberOfPorts (number): Number of Ports per Switch
			NumberOfTableRanges (number): Number of Tables per Switch
			NumberOfTopologyPorts (number): Number of Topology Ports per Switch
			NumberOfUnconnectedPorts (number): Number of Unconnected Ports per Switch
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
			SwitchLocalIp (list(str)): The local IP address of the interface. This field is auto-populated and cannot be changed.

		Returns:
			self: This instance with matching openFlowSwitch data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of openFlowSwitch data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the openFlowSwitch data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ClearAllLearnedInfo(self, Arg2):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear OF Channels learnt by this Switch.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Channel into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def GetOFChannelLearnedInfo(self, Arg2):
		"""Executes the getOFChannelLearnedInfo operation on the server.

		Gets OF Channels learnt by this switch.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Channel into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetOFChannelLearnedInfo', payload=locals(), response_object=None)

	def GetOFSwitchFlowStatLearnedInfo(self, Arg2):
		"""Executes the getOFSwitchFlowStatLearnedInfo operation on the server.

		Gets OF Switch Flows learnt by this switch.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Switch Flows into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetOFSwitchFlowStatLearnedInfo', payload=locals(), response_object=None)

	def GetOFSwitchGroupLearnedInfo(self, Arg2):
		"""Executes the getOFSwitchGroupLearnedInfo operation on the server.

		Gets OF Switch Groups learnt by this switch.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Switch Flows into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetOFSwitchGroupLearnedInfo', payload=locals(), response_object=None)

	def GetOFSwitchMeterLearnedInfo(self, Arg2):
		"""Executes the getOFSwitchMeterLearnedInfo operation on the server.

		Gets OF Switch Meter learned info for this switch.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of OF Switch Flows into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetOFSwitchMeterLearnedInfo', payload=locals(), response_object=None)

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
