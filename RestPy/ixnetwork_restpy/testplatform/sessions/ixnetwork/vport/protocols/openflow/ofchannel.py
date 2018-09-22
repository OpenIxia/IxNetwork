from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfChannel(Base):
	"""The OfChannel class encapsulates a user managed ofChannel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ofChannel'

	def __init__(self, parent):
		super(OfChannel, self).__init__(parent)

	@property
	def Capabilities(self):
		"""An instance of the Capabilities class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.capabilities.Capabilities)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.capabilities import Capabilities
		return Capabilities(self)._select()

	@property
	def ControllerTables(self):
		"""An instance of the ControllerTables class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllertables.ControllerTables)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllertables import ControllerTables
		return ControllerTables(self)

	@property
	def FlowRange(self):
		"""An instance of the FlowRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrange.FlowRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrange import FlowRange
		return FlowRange(self)

	@property
	def Group(self):
		"""An instance of the Group class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.group.Group)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.group import Group
		return Group(self)

	@property
	def Meter(self):
		"""An instance of the Meter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meter.Meter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meter import Meter
		return Meter(self)

	@property
	def SupportedActions(self):
		"""An instance of the SupportedActions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.supportedactions.SupportedActions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.supportedactions import SupportedActions
		return SupportedActions(self)._select()

	@property
	def SwitchPacketIn(self):
		"""An instance of the SwitchPacketIn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchpacketin.SwitchPacketIn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchpacketin import SwitchPacketIn
		return SwitchPacketIn(self)

	@property
	def SwitchPorts(self):
		"""An instance of the SwitchPorts class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchports.SwitchPorts)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchports import SwitchPorts
		return SwitchPorts(self)

	@property
	def SwitchTables(self):
		"""An instance of the SwitchTables class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchtables.SwitchTables)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchtables import SwitchTables
		return SwitchTables(self)

	@property
	def CalculateFlows(self):
		"""If true, calculates the rate at which flows are transmitted by the controller.

		Returns:
			bool
		"""
		return self._get_attribute('calculateFlows')
	@CalculateFlows.setter
	def CalculateFlows(self, value):
		self._set_attribute('calculateFlows', value)

	@property
	def CalculatePacketInReplyDelay(self):
		"""If true, calculates delay between Packet-In sent from Switch and reply received from Controller.

		Returns:
			bool
		"""
		return self._get_attribute('calculatePacketInReplyDelay')
	@CalculatePacketInReplyDelay.setter
	def CalculatePacketInReplyDelay(self, value):
		self._set_attribute('calculatePacketInReplyDelay', value)

	@property
	def DataPathId(self):
		"""Indicates the Datapath ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')
	@DataPathId.setter
	def DataPathId(self, value):
		self._set_attribute('dataPathId', value)

	@property
	def DataPathIdInHex(self):
		"""Indicates the Datapath ID in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdInHex')
	@DataPathIdInHex.setter
	def DataPathIdInHex(self, value):
		self._set_attribute('dataPathIdInHex', value)

	@property
	def DatapathDescritpion(self):
		"""Indicates a description of the datapath.

		Returns:
			str
		"""
		return self._get_attribute('datapathDescritpion')
	@DatapathDescritpion.setter
	def DatapathDescritpion(self, value):
		self._set_attribute('datapathDescritpion', value)

	@property
	def Description(self):
		"""A description of the OF Channel used to identify it.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def EnableCalculateFlowsPerSecondUsingBarrierReq(self):
		"""If true, enables flow rate Calculation using Barrier request message.

		Returns:
			bool
		"""
		return self._get_attribute('enableCalculateFlowsPerSecondUsingBarrierReq')
	@EnableCalculateFlowsPerSecondUsingBarrierReq.setter
	def EnableCalculateFlowsPerSecondUsingBarrierReq(self, value):
		self._set_attribute('enableCalculateFlowsPerSecondUsingBarrierReq', value)

	@property
	def EnableHelloElement(self):
		"""Enables Hello element for version negotiation.

		Returns:
			bool
		"""
		return self._get_attribute('enableHelloElement')
	@EnableHelloElement.setter
	def EnableHelloElement(self, value):
		self._set_attribute('enableHelloElement', value)

	@property
	def EnableStartupEmptyTableFeatureRequest(self):
		"""If true, the Table Feature Request is sent at start up. The default value is false

		Returns:
			bool
		"""
		return self._get_attribute('enableStartupEmptyTableFeatureRequest')
	@EnableStartupEmptyTableFeatureRequest.setter
	def EnableStartupEmptyTableFeatureRequest(self, value):
		self._set_attribute('enableStartupEmptyTableFeatureRequest', value)

	@property
	def Enabled(self):
		"""If true, the OF Channel is used in the OpenFlow configuration.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FlowTxBurstSize(self):
		"""Indicates the number of flows sent in a single burst.

		Returns:
			number
		"""
		return self._get_attribute('flowTxBurstSize')
	@FlowTxBurstSize.setter
	def FlowTxBurstSize(self, value):
		self._set_attribute('flowTxBurstSize', value)

	@property
	def HardwareDescription(self):
		"""Indicates the hardware description of the switch.

		Returns:
			str
		"""
		return self._get_attribute('hardwareDescription')
	@HardwareDescription.setter
	def HardwareDescription(self, value):
		self._set_attribute('hardwareDescription', value)

	@property
	def InterFlowBurstGap(self):
		"""Indicates the duration, in milliseconds, to wait between successive flow bursts.

		Returns:
			number
		"""
		return self._get_attribute('interFlowBurstGap')
	@InterFlowBurstGap.setter
	def InterFlowBurstGap(self, value):
		self._set_attribute('interFlowBurstGap', value)

	@property
	def InterPacketInBurstGap(self):
		"""Indicates the duration, in milliseconds, to wait between successive Packet-In bursts.

		Returns:
			number
		"""
		return self._get_attribute('interPacketInBurstGap')
	@InterPacketInBurstGap.setter
	def InterPacketInBurstGap(self, value):
		self._set_attribute('interPacketInBurstGap', value)

	@property
	def LocalIp(self):
		"""Indicates the local IP address of the interface. This field is auto-populated and cannot be changed.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def ManufacturerDescription(self):
		"""Indicates the description of the switch manufacturer.

		Returns:
			str
		"""
		return self._get_attribute('manufacturerDescription')
	@ManufacturerDescription.setter
	def ManufacturerDescription(self, value):
		self._set_attribute('manufacturerDescription', value)

	@property
	def MaximumNumberOfFlowsProcessed(self):
		"""Indicates the maximum number of flows that the controller can advertise before backing off.

		Returns:
			number
		"""
		return self._get_attribute('maximumNumberOfFlowsProcessed')
	@MaximumNumberOfFlowsProcessed.setter
	def MaximumNumberOfFlowsProcessed(self, value):
		self._set_attribute('maximumNumberOfFlowsProcessed', value)

	@property
	def MaximumPacketInBytes(self):
		"""Indicates the maximum size of data in a Packet-In a message.

		Returns:
			number
		"""
		return self._get_attribute('maximumPacketInBytes')
	@MaximumPacketInBytes.setter
	def MaximumPacketInBytes(self, value):
		self._set_attribute('maximumPacketInBytes', value)

	@property
	def NumberOfBuffers(self):
		"""Indicates the maximum number of packets that can be stored in the buffered at a time.

		Returns:
			number
		"""
		return self._get_attribute('numberOfBuffers')
	@NumberOfBuffers.setter
	def NumberOfBuffers(self, value):
		self._set_attribute('numberOfBuffers', value)

	@property
	def PacketInReplyTimeout(self):
		"""Indicates the duration for which the Switch should wait for Packet-in-reply before freeing the buffer.

		Returns:
			number
		"""
		return self._get_attribute('packetInReplyTimeout')
	@PacketInReplyTimeout.setter
	def PacketInReplyTimeout(self, value):
		self._set_attribute('packetInReplyTimeout', value)

	@property
	def PacketInTxBurstSize(self):
		"""Indicates the number of packets in messages sent in a single burst.

		Returns:
			number
		"""
		return self._get_attribute('packetInTxBurstSize')
	@PacketInTxBurstSize.setter
	def PacketInTxBurstSize(self, value):
		self._set_attribute('packetInTxBurstSize', value)

	@property
	def RemoteIp(self):
		"""Indicates the IP address of the DUT at the other end of OF channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')
	@RemoteIp.setter
	def RemoteIp(self, value):
		self._set_attribute('remoteIp', value)

	@property
	def SerialNumber(self):
		"""Indicates the Serial Number of the switch.

		Returns:
			str
		"""
		return self._get_attribute('serialNumber')
	@SerialNumber.setter
	def SerialNumber(self, value):
		self._set_attribute('serialNumber', value)

	@property
	def SoftwareDescription(self):
		"""Indicates the description of the software installed on the switch.

		Returns:
			str
		"""
		return self._get_attribute('softwareDescription')
	@SoftwareDescription.setter
	def SoftwareDescription(self, value):
		self._set_attribute('softwareDescription', value)

	@property
	def StartUpGenerationId(self):
		"""A 64-bit sequence number field that identifies a given mastership view. A new incremented Generation ID is assigned each time the mastership view changes, for instance, when a new master is designated. On receiving a role change request, the switch compares the Generation ID in the message against the largest Generation ID seen so far. A message with a Generation ID smaller than a previously seen Generation ID is discarded.

		Returns:
			str
		"""
		return self._get_attribute('startUpGenerationId')
	@StartUpGenerationId.setter
	def StartUpGenerationId(self, value):
		self._set_attribute('startUpGenerationId', value)

	@property
	def StartUpRoleRequest(self):
		"""If selected, the controller sends a Role Request message when connection is established to change its role as per the option selected.

		Returns:
			str(noRoleRequest|master|slave)
		"""
		return self._get_attribute('startUpRoleRequest')
	@StartUpRoleRequest.setter
	def StartUpRoleRequest(self, value):
		self._set_attribute('startUpRoleRequest', value)

	@property
	def StartupFeatureRequest(self):
		"""If true, a feature request is sent at startup.

		Returns:
			bool
		"""
		return self._get_attribute('startupFeatureRequest')
	@StartupFeatureRequest.setter
	def StartupFeatureRequest(self, value):
		self._set_attribute('startupFeatureRequest', value)

	@property
	def StoreFlows(self):
		"""If true, the switch will store the flows advertised by the controller in its tables.

		Returns:
			bool
		"""
		return self._get_attribute('storeFlows')
	@StoreFlows.setter
	def StoreFlows(self, value):
		self._set_attribute('storeFlows', value)

	@property
	def UseDataPathIdAsChannelIdentifier(self):
		"""If true, the Datapath ID of the switch is used.

		Returns:
			bool
		"""
		return self._get_attribute('useDataPathIdAsChannelIdentifier')
	@UseDataPathIdAsChannelIdentifier.setter
	def UseDataPathIdAsChannelIdentifier(self, value):
		self._set_attribute('useDataPathIdAsChannelIdentifier', value)

	@property
	def UseDatapathId(self):
		"""Use datapath Id that is configured.

		Returns:
			bool
		"""
		return self._get_attribute('useDatapathId')
	@UseDatapathId.setter
	def UseDatapathId(self, value):
		self._set_attribute('useDatapathId', value)

	def add(self, CalculateFlows=None, CalculatePacketInReplyDelay=None, DataPathId=None, DataPathIdInHex=None, DatapathDescritpion=None, Description=None, EnableCalculateFlowsPerSecondUsingBarrierReq=None, EnableHelloElement=None, EnableStartupEmptyTableFeatureRequest=None, Enabled=None, FlowTxBurstSize=None, HardwareDescription=None, InterFlowBurstGap=None, InterPacketInBurstGap=None, ManufacturerDescription=None, MaximumNumberOfFlowsProcessed=None, MaximumPacketInBytes=None, NumberOfBuffers=None, PacketInReplyTimeout=None, PacketInTxBurstSize=None, RemoteIp=None, SerialNumber=None, SoftwareDescription=None, StartUpGenerationId=None, StartUpRoleRequest=None, StartupFeatureRequest=None, StoreFlows=None, UseDataPathIdAsChannelIdentifier=None, UseDatapathId=None):
		"""Adds a new ofChannel node on the server and retrieves it in this instance.

		Args:
			CalculateFlows (bool): If true, calculates the rate at which flows are transmitted by the controller.
			CalculatePacketInReplyDelay (bool): If true, calculates delay between Packet-In sent from Switch and reply received from Controller.
			DataPathId (str): Indicates the Datapath ID of the OpenFlow switch.
			DataPathIdInHex (str): Indicates the Datapath ID in hexadecimal format.
			DatapathDescritpion (str): Indicates a description of the datapath.
			Description (str): A description of the OF Channel used to identify it.
			EnableCalculateFlowsPerSecondUsingBarrierReq (bool): If true, enables flow rate Calculation using Barrier request message.
			EnableHelloElement (bool): Enables Hello element for version negotiation.
			EnableStartupEmptyTableFeatureRequest (bool): If true, the Table Feature Request is sent at start up. The default value is false
			Enabled (bool): If true, the OF Channel is used in the OpenFlow configuration.
			FlowTxBurstSize (number): Indicates the number of flows sent in a single burst.
			HardwareDescription (str): Indicates the hardware description of the switch.
			InterFlowBurstGap (number): Indicates the duration, in milliseconds, to wait between successive flow bursts.
			InterPacketInBurstGap (number): Indicates the duration, in milliseconds, to wait between successive Packet-In bursts.
			ManufacturerDescription (str): Indicates the description of the switch manufacturer.
			MaximumNumberOfFlowsProcessed (number): Indicates the maximum number of flows that the controller can advertise before backing off.
			MaximumPacketInBytes (number): Indicates the maximum size of data in a Packet-In a message.
			NumberOfBuffers (number): Indicates the maximum number of packets that can be stored in the buffered at a time.
			PacketInReplyTimeout (number): Indicates the duration for which the Switch should wait for Packet-in-reply before freeing the buffer.
			PacketInTxBurstSize (number): Indicates the number of packets in messages sent in a single burst.
			RemoteIp (str): Indicates the IP address of the DUT at the other end of OF channel.
			SerialNumber (str): Indicates the Serial Number of the switch.
			SoftwareDescription (str): Indicates the description of the software installed on the switch.
			StartUpGenerationId (str): A 64-bit sequence number field that identifies a given mastership view. A new incremented Generation ID is assigned each time the mastership view changes, for instance, when a new master is designated. On receiving a role change request, the switch compares the Generation ID in the message against the largest Generation ID seen so far. A message with a Generation ID smaller than a previously seen Generation ID is discarded.
			StartUpRoleRequest (str(noRoleRequest|master|slave)): If selected, the controller sends a Role Request message when connection is established to change its role as per the option selected.
			StartupFeatureRequest (bool): If true, a feature request is sent at startup.
			StoreFlows (bool): If true, the switch will store the flows advertised by the controller in its tables.
			UseDataPathIdAsChannelIdentifier (bool): If true, the Datapath ID of the switch is used.
			UseDatapathId (bool): Use datapath Id that is configured.

		Returns:
			self: This instance with all currently retrieved ofChannel data using find and the newly added ofChannel data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ofChannel data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CalculateFlows=None, CalculatePacketInReplyDelay=None, DataPathId=None, DataPathIdInHex=None, DatapathDescritpion=None, Description=None, EnableCalculateFlowsPerSecondUsingBarrierReq=None, EnableHelloElement=None, EnableStartupEmptyTableFeatureRequest=None, Enabled=None, FlowTxBurstSize=None, HardwareDescription=None, InterFlowBurstGap=None, InterPacketInBurstGap=None, LocalIp=None, ManufacturerDescription=None, MaximumNumberOfFlowsProcessed=None, MaximumPacketInBytes=None, NumberOfBuffers=None, PacketInReplyTimeout=None, PacketInTxBurstSize=None, RemoteIp=None, SerialNumber=None, SoftwareDescription=None, StartUpGenerationId=None, StartUpRoleRequest=None, StartupFeatureRequest=None, StoreFlows=None, UseDataPathIdAsChannelIdentifier=None, UseDatapathId=None):
		"""Finds and retrieves ofChannel data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannel data from the server.
		By default the find method takes no parameters and will retrieve all ofChannel data from the server.

		Args:
			CalculateFlows (bool): If true, calculates the rate at which flows are transmitted by the controller.
			CalculatePacketInReplyDelay (bool): If true, calculates delay between Packet-In sent from Switch and reply received from Controller.
			DataPathId (str): Indicates the Datapath ID of the OpenFlow switch.
			DataPathIdInHex (str): Indicates the Datapath ID in hexadecimal format.
			DatapathDescritpion (str): Indicates a description of the datapath.
			Description (str): A description of the OF Channel used to identify it.
			EnableCalculateFlowsPerSecondUsingBarrierReq (bool): If true, enables flow rate Calculation using Barrier request message.
			EnableHelloElement (bool): Enables Hello element for version negotiation.
			EnableStartupEmptyTableFeatureRequest (bool): If true, the Table Feature Request is sent at start up. The default value is false
			Enabled (bool): If true, the OF Channel is used in the OpenFlow configuration.
			FlowTxBurstSize (number): Indicates the number of flows sent in a single burst.
			HardwareDescription (str): Indicates the hardware description of the switch.
			InterFlowBurstGap (number): Indicates the duration, in milliseconds, to wait between successive flow bursts.
			InterPacketInBurstGap (number): Indicates the duration, in milliseconds, to wait between successive Packet-In bursts.
			LocalIp (str): Indicates the local IP address of the interface. This field is auto-populated and cannot be changed.
			ManufacturerDescription (str): Indicates the description of the switch manufacturer.
			MaximumNumberOfFlowsProcessed (number): Indicates the maximum number of flows that the controller can advertise before backing off.
			MaximumPacketInBytes (number): Indicates the maximum size of data in a Packet-In a message.
			NumberOfBuffers (number): Indicates the maximum number of packets that can be stored in the buffered at a time.
			PacketInReplyTimeout (number): Indicates the duration for which the Switch should wait for Packet-in-reply before freeing the buffer.
			PacketInTxBurstSize (number): Indicates the number of packets in messages sent in a single burst.
			RemoteIp (str): Indicates the IP address of the DUT at the other end of OF channel.
			SerialNumber (str): Indicates the Serial Number of the switch.
			SoftwareDescription (str): Indicates the description of the software installed on the switch.
			StartUpGenerationId (str): A 64-bit sequence number field that identifies a given mastership view. A new incremented Generation ID is assigned each time the mastership view changes, for instance, when a new master is designated. On receiving a role change request, the switch compares the Generation ID in the message against the largest Generation ID seen so far. A message with a Generation ID smaller than a previously seen Generation ID is discarded.
			StartUpRoleRequest (str(noRoleRequest|master|slave)): If selected, the controller sends a Role Request message when connection is established to change its role as per the option selected.
			StartupFeatureRequest (bool): If true, a feature request is sent at startup.
			StoreFlows (bool): If true, the switch will store the flows advertised by the controller in its tables.
			UseDataPathIdAsChannelIdentifier (bool): If true, the Datapath ID of the switch is used.
			UseDatapathId (bool): Use datapath Id that is configured.

		Returns:
			self: This instance with matching ofChannel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateRole(self):
		"""Executes the updateRole operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannel)): The method internally set Arg1 to the current href for this instance

		Returns:
			number: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateRole', payload=locals(), response_object=None)
