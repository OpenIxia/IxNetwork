from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowRange(Base):
	"""The FlowRange class encapsulates a user managed flowRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowRange'

	def __init__(self, parent):
		super(FlowRange, self).__init__(parent)

	@property
	def FlowRangeAction(self):
		"""An instance of the FlowRangeAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrangeaction.FlowRangeAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flowrangeaction import FlowRangeAction
		return FlowRangeAction(self)

	@property
	def CheckOverlap(self):
		"""If true, Ixia enables the Check Overlap flag while sending OpenFlow flow modification messages.

		Returns:
			bool
		"""
		return self._get_attribute('checkOverlap')
	@CheckOverlap.setter
	def CheckOverlap(self, value):
		self._set_attribute('checkOverlap', value)

	@property
	def Description(self):
		"""A name that describes the Flow Range.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DontAddOnChannelUp(self):
		"""If true, no flow add or delete packet is sent out when OpenFlow channel comes up or when flow entry is enabled/disabled in the IxNetwork GUI. This facility is useful to send flow add,delete, and modify for ad-hoc flows through Test Composer.

		Returns:
			bool
		"""
		return self._get_attribute('dontAddOnChannelUp')
	@DontAddOnChannelUp.setter
	def DontAddOnChannelUp(self, value):
		self._set_attribute('dontAddOnChannelUp', value)

	@property
	def EmergencyFlow(self):
		"""If true, Ixia enables the Emergency flag while sending OpenFlow flow modification messages.

		Returns:
			bool
		"""
		return self._get_attribute('emergencyFlow')
	@EmergencyFlow.setter
	def EmergencyFlow(self, value):
		self._set_attribute('emergencyFlow', value)

	@property
	def Enabled(self):
		"""If true, enables the flow Range object in the protocol.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EthernetDestination(self):
		"""Indicates the Ethernet destination address for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""Indicates the Ethernet source address for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""Indicates the type of Ethernet to be used. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def FlowModStatus(self):
		"""Reflects the status of the selected flow range which is modified at runtime.

		Returns:
			str
		"""
		return self._get_attribute('flowModStatus')

	@property
	def HardTimeout(self):
		"""Indicates the inactive time in seconds after which the Flow range will hard timeout and close.

		Returns:
			number
		"""
		return self._get_attribute('hardTimeout')
	@HardTimeout.setter
	def HardTimeout(self, value):
		self._set_attribute('hardTimeout', value)

	@property
	def IdleTimeout(self):
		"""Indicates the inactive time in seconds after which the Flow range will timeout and become idle.

		Returns:
			number
		"""
		return self._get_attribute('idleTimeout')
	@IdleTimeout.setter
	def IdleTimeout(self, value):
		self._set_attribute('idleTimeout', value)

	@property
	def InPort(self):
		"""Indicates the In port value for flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""Specifies the IP DSCP value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpProtocol(self):
		"""Specifies the IP Protocol to be used for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""Indicates the IPv4 destination address mask value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""Indicates the IPv4 source address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def MatchType(self):
		"""Indicates the type of match to be configured.

		Returns:
			str(strict|loose)
		"""
		return self._get_attribute('matchType')
	@MatchType.setter
	def MatchType(self, value):
		self._set_attribute('matchType', value)

	@property
	def Priority(self):
		"""Indicates the priority level for the Flow Range.

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def SendFlowRemoved(self):
		"""If true, Ixia enables the Send Flow Removed flag while sending OpenFlow flow modification messages.

		Returns:
			bool
		"""
		return self._get_attribute('sendFlowRemoved')
	@SendFlowRemoved.setter
	def SendFlowRemoved(self, value):
		self._set_attribute('sendFlowRemoved', value)

	@property
	def TotalFlowCount(self):
		"""Specifies the number of flows.

		Returns:
			number
		"""
		return self._get_attribute('totalFlowCount')
	@TotalFlowCount.setter
	def TotalFlowCount(self, value):
		self._set_attribute('totalFlowCount', value)

	@property
	def TransportDestinationIcmpCode(self):
		"""Specifies the Transport destination address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('transportDestinationIcmpCode')
	@TransportDestinationIcmpCode.setter
	def TransportDestinationIcmpCode(self, value):
		self._set_attribute('transportDestinationIcmpCode', value)

	@property
	def TransportSourceIcmpType(self):
		"""Specifies the Transport Source address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('transportSourceIcmpType')
	@TransportSourceIcmpType.setter
	def TransportSourceIcmpType(self, value):
		self._set_attribute('transportSourceIcmpType', value)

	@property
	def VlanId(self):
		"""Indicates the VLAN identifier value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Indicates the VLAN priority value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, CheckOverlap=None, Description=None, DontAddOnChannelUp=None, EmergencyFlow=None, Enabled=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, HardTimeout=None, IdleTimeout=None, InPort=None, IpDscp=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, MatchType=None, Priority=None, SendFlowRemoved=None, TotalFlowCount=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, VlanId=None, VlanPriority=None):
		"""Adds a new flowRange node on the server and retrieves it in this instance.

		Args:
			CheckOverlap (bool): If true, Ixia enables the Check Overlap flag while sending OpenFlow flow modification messages.
			Description (str): A name that describes the Flow Range.
			DontAddOnChannelUp (bool): If true, no flow add or delete packet is sent out when OpenFlow channel comes up or when flow entry is enabled/disabled in the IxNetwork GUI. This facility is useful to send flow add,delete, and modify for ad-hoc flows through Test Composer.
			EmergencyFlow (bool): If true, Ixia enables the Emergency flag while sending OpenFlow flow modification messages.
			Enabled (bool): If true, enables the flow Range object in the protocol.
			EthernetDestination (str): Indicates the Ethernet destination address for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			EthernetSource (str): Indicates the Ethernet source address for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			EthernetType (str): Indicates the type of Ethernet to be used. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			HardTimeout (number): Indicates the inactive time in seconds after which the Flow range will hard timeout and close.
			IdleTimeout (number): Indicates the inactive time in seconds after which the Flow range will timeout and become idle.
			InPort (str): Indicates the In port value for flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpDscp (str): Specifies the IP DSCP value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpProtocol (str): Specifies the IP Protocol to be used for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			Ipv4Destination (str): Indicates the IPv4 destination address mask value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			Ipv4Source (str): Indicates the IPv4 source address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			MatchType (str(strict|loose)): Indicates the type of match to be configured.
			Priority (number): Indicates the priority level for the Flow Range.
			SendFlowRemoved (bool): If true, Ixia enables the Send Flow Removed flag while sending OpenFlow flow modification messages.
			TotalFlowCount (number): Specifies the number of flows.
			TransportDestinationIcmpCode (str): Specifies the Transport destination address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			TransportSourceIcmpType (str): Specifies the Transport Source address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			VlanId (str): Indicates the VLAN identifier value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			VlanPriority (str): Indicates the VLAN priority value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			self: This instance with all currently retrieved flowRange data using find and the newly added flowRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CheckOverlap=None, Description=None, DontAddOnChannelUp=None, EmergencyFlow=None, Enabled=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, FlowModStatus=None, HardTimeout=None, IdleTimeout=None, InPort=None, IpDscp=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, MatchType=None, Priority=None, SendFlowRemoved=None, TotalFlowCount=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves flowRange data from the server.

		All named parameters support regex and can be used to selectively retrieve flowRange data from the server.
		By default the find method takes no parameters and will retrieve all flowRange data from the server.

		Args:
			CheckOverlap (bool): If true, Ixia enables the Check Overlap flag while sending OpenFlow flow modification messages.
			Description (str): A name that describes the Flow Range.
			DontAddOnChannelUp (bool): If true, no flow add or delete packet is sent out when OpenFlow channel comes up or when flow entry is enabled/disabled in the IxNetwork GUI. This facility is useful to send flow add,delete, and modify for ad-hoc flows through Test Composer.
			EmergencyFlow (bool): If true, Ixia enables the Emergency flag while sending OpenFlow flow modification messages.
			Enabled (bool): If true, enables the flow Range object in the protocol.
			EthernetDestination (str): Indicates the Ethernet destination address for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			EthernetSource (str): Indicates the Ethernet source address for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			EthernetType (str): Indicates the type of Ethernet to be used. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			FlowModStatus (str): Reflects the status of the selected flow range which is modified at runtime.
			HardTimeout (number): Indicates the inactive time in seconds after which the Flow range will hard timeout and close.
			IdleTimeout (number): Indicates the inactive time in seconds after which the Flow range will timeout and become idle.
			InPort (str): Indicates the In port value for flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpDscp (str): Specifies the IP DSCP value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpProtocol (str): Specifies the IP Protocol to be used for the flow range. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			Ipv4Destination (str): Indicates the IPv4 destination address mask value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			Ipv4Source (str): Indicates the IPv4 source address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			MatchType (str(strict|loose)): Indicates the type of match to be configured.
			Priority (number): Indicates the priority level for the Flow Range.
			SendFlowRemoved (bool): If true, Ixia enables the Send Flow Removed flag while sending OpenFlow flow modification messages.
			TotalFlowCount (number): Specifies the number of flows.
			TransportDestinationIcmpCode (str): Specifies the Transport destination address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			TransportSourceIcmpType (str): Specifies the Transport Source address. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			VlanId (str): Indicates the VLAN identifier value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			VlanPriority (str): Indicates the VLAN priority value. This attribute is of string type and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			self: This instance with matching flowRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateFlowMod(self, Arg2):
		"""Executes the updateFlowMod operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=flowRange)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(sendFlowAdd|sendFlowModify|sendFlowRemove)): NOT DEFINED

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateFlowMod', payload=locals(), response_object=None)
