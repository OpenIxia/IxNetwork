from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv6TrafficEndPoint(Base):
	"""The Ipv6TrafficEndPoint class encapsulates a user managed ipv6TrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv6TrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ipv6TrafficEndPoint'

	def __init__(self, parent):
		super(Ipv6TrafficEndPoint, self).__init__(parent)

	@property
	def ArpViaInterface(self):
		"""If selected, ARP request is conveyed through an Interface.

		Returns:
			bool
		"""
		return self._get_attribute('arpViaInterface')
	@ArpViaInterface.setter
	def ArpViaInterface(self, value):
		self._set_attribute('arpViaInterface', value)

	@property
	def DestinationPort(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationPort')
	@DestinationPort.setter
	def DestinationPort(self, value):
		self._set_attribute('destinationPort', value)

	@property
	def EnableVlan(self):
		"""Select this check box to make VLAN available.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def GatewayMac(self):
		"""The Gateway MAC address of the source traffic endpoint. The default value is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('gatewayMac')
	@GatewayMac.setter
	def GatewayMac(self, value):
		self._set_attribute('gatewayMac', value)

	@property
	def Ipv6Address(self):
		"""Specify the IPv6 address of the Source Traffic Endpoint. The default value is 0.0.0.0.0.0.0.0

		Returns:
			str
		"""
		return self._get_attribute('ipv6Address')
	@Ipv6Address.setter
	def Ipv6Address(self, value):
		self._set_attribute('ipv6Address', value)

	@property
	def Ipv6AddressMask(self):
		"""Specify the Mask value. The default value is 64.

		Returns:
			number
		"""
		return self._get_attribute('ipv6AddressMask')
	@Ipv6AddressMask.setter
	def Ipv6AddressMask(self, value):
		self._set_attribute('ipv6AddressMask', value)

	@property
	def Ipv6CustomHeaderLength(self):
		"""The Custom IPv6 Header Length value. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('ipv6CustomHeaderLength')
	@Ipv6CustomHeaderLength.setter
	def Ipv6CustomHeaderLength(self, value):
		self._set_attribute('ipv6CustomHeaderLength', value)

	@property
	def Ipv6CustomHeaderValue(self):
		"""The Custom IPv6 Header Value. The default value is 00.

		Returns:
			str
		"""
		return self._get_attribute('ipv6CustomHeaderValue')
	@Ipv6CustomHeaderValue.setter
	def Ipv6CustomHeaderValue(self, value):
		self._set_attribute('ipv6CustomHeaderValue', value)

	@property
	def Ipv6CustomNextHeader(self):
		"""The Custom IPv6 Next Header value. The default value is 1.

		Returns:
			str
		"""
		return self._get_attribute('ipv6CustomNextHeader')
	@Ipv6CustomNextHeader.setter
	def Ipv6CustomNextHeader(self, value):
		self._set_attribute('ipv6CustomNextHeader', value)

	@property
	def Ipv6Dscp(self):
		"""The priority specified for the IP address. The default value is 0.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Dscp')
	@Ipv6Dscp.setter
	def Ipv6Dscp(self, value):
		self._set_attribute('ipv6Dscp', value)

	@property
	def Ipv6Ecn(self):
		"""The ECN value specified for the IP address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Ecn')
	@Ipv6Ecn.setter
	def Ipv6Ecn(self, value):
		self._set_attribute('ipv6Ecn', value)

	@property
	def Ipv6FlowLabel(self):
		"""The IPv6 Flow Label value.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NextHeader(self):
		"""The IPv6 Next Header value.

		Returns:
			str(custom|tcp|udp)
		"""
		return self._get_attribute('ipv6NextHeader')
	@Ipv6NextHeader.setter
	def Ipv6NextHeader(self, value):
		self._set_attribute('ipv6NextHeader', value)

	@property
	def MacAddress(self):
		"""The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def Name(self):
		"""The name of the Traffic endpoint. It is an auto-populated field but can be customized for convenience.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def ProtocolInterface(self):
		"""NOT DEFINED

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def RangeSize(self):
		"""Specify the size of the traffic range.

		Returns:
			number
		"""
		return self._get_attribute('rangeSize')
	@RangeSize.setter
	def RangeSize(self, value):
		self._set_attribute('rangeSize', value)

	@property
	def SourcePort(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('sourcePort')
	@SourcePort.setter
	def SourcePort(self, value):
		self._set_attribute('sourcePort', value)

	@property
	def UdpDestination(self):
		"""Specify the UDP Destination. The default value is 1.

		Returns:
			str
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""Specify the UDP Source. The default value is 1.

		Returns:
			str
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanCount(self):
		"""Specify the VLAN count. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""Specify the VLAN ID (Outer and Inner).

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Specify the VLAN Priority (Outer and Inner).

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, ArpViaInterface=None, DestinationPort=None, EnableVlan=None, GatewayMac=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6CustomHeaderLength=None, Ipv6CustomHeaderValue=None, Ipv6CustomNextHeader=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, Ipv6NextHeader=None, MacAddress=None, Name=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new ipv6TrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): If selected, ARP request is conveyed through an Interface.
			DestinationPort (str): NOT DEFINED
			EnableVlan (bool): Select this check box to make VLAN available.
			GatewayMac (str): The Gateway MAC address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			Ipv6Address (str): Specify the IPv6 address of the Source Traffic Endpoint. The default value is 0.0.0.0.0.0.0.0
			Ipv6AddressMask (number): Specify the Mask value. The default value is 64.
			Ipv6CustomHeaderLength (number): The Custom IPv6 Header Length value. The default value is 1.
			Ipv6CustomHeaderValue (str): The Custom IPv6 Header Value. The default value is 00.
			Ipv6CustomNextHeader (str): The Custom IPv6 Next Header value. The default value is 1.
			Ipv6Dscp (str): The priority specified for the IP address. The default value is 0.
			Ipv6Ecn (str): The ECN value specified for the IP address.
			Ipv6FlowLabel (str): The IPv6 Flow Label value.
			Ipv6NextHeader (str(custom|tcp|udp)): The IPv6 Next Header value.
			MacAddress (str): The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			Name (str): The name of the Traffic endpoint. It is an auto-populated field but can be customized for convenience.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): NOT DEFINED
			RangeSize (number): Specify the size of the traffic range.
			SourcePort (str): NOT DEFINED
			UdpDestination (str): Specify the UDP Destination. The default value is 1.
			UdpSource (str): Specify the UDP Source. The default value is 1.
			VlanCount (number): Specify the VLAN count. The default value is 1.
			VlanId (str): Specify the VLAN ID (Outer and Inner).
			VlanPriority (str): Specify the VLAN Priority (Outer and Inner).

		Returns:
			self: This instance with all currently retrieved ipv6TrafficEndPoint data using find and the newly added ipv6TrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ipv6TrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, DestinationPort=None, EnableVlan=None, GatewayMac=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6CustomHeaderLength=None, Ipv6CustomHeaderValue=None, Ipv6CustomNextHeader=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, Ipv6NextHeader=None, MacAddress=None, Name=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves ipv6TrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv6TrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all ipv6TrafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): If selected, ARP request is conveyed through an Interface.
			DestinationPort (str): NOT DEFINED
			EnableVlan (bool): Select this check box to make VLAN available.
			GatewayMac (str): The Gateway MAC address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			Ipv6Address (str): Specify the IPv6 address of the Source Traffic Endpoint. The default value is 0.0.0.0.0.0.0.0
			Ipv6AddressMask (number): Specify the Mask value. The default value is 64.
			Ipv6CustomHeaderLength (number): The Custom IPv6 Header Length value. The default value is 1.
			Ipv6CustomHeaderValue (str): The Custom IPv6 Header Value. The default value is 00.
			Ipv6CustomNextHeader (str): The Custom IPv6 Next Header value. The default value is 1.
			Ipv6Dscp (str): The priority specified for the IP address. The default value is 0.
			Ipv6Ecn (str): The ECN value specified for the IP address.
			Ipv6FlowLabel (str): The IPv6 Flow Label value.
			Ipv6NextHeader (str(custom|tcp|udp)): The IPv6 Next Header value.
			MacAddress (str): The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			Name (str): The name of the Traffic endpoint. It is an auto-populated field but can be customized for convenience.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): NOT DEFINED
			RangeSize (number): Specify the size of the traffic range.
			SourcePort (str): NOT DEFINED
			UdpDestination (str): Specify the UDP Destination. The default value is 1.
			UdpSource (str): Specify the UDP Source. The default value is 1.
			VlanCount (number): Specify the VLAN count. The default value is 1.
			VlanId (str): Specify the VLAN ID (Outer and Inner).
			VlanPriority (str): Specify the VLAN Priority (Outer and Inner).

		Returns:
			self: This instance with matching ipv6TrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv6TrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv6TrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
