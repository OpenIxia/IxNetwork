from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MplsTrafficEndPoint(Base):
	"""The MplsTrafficEndPoint class encapsulates a user managed mplsTrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MplsTrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'mplsTrafficEndPoint'

	def __init__(self, parent):
		super(MplsTrafficEndPoint, self).__init__(parent)

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
		"""The Gateway MAC address of the destination traffic endpoint. The default value is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('gatewayMac')
	@GatewayMac.setter
	def GatewayMac(self, value):
		self._set_attribute('gatewayMac', value)

	@property
	def IpAddress(self):
		"""Specify the IP address of the Source Traffic Endpoint. The default value is 0.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpMask(self):
		"""Specify the Mask value. The default value is 24.

		Returns:
			number
		"""
		return self._get_attribute('ipMask')
	@IpMask.setter
	def IpMask(self, value):
		self._set_attribute('ipMask', value)

	@property
	def Ipv4Dscp(self):
		"""The priority specified for the IP address. The default value is 0.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Dscp')
	@Ipv4Dscp.setter
	def Ipv4Dscp(self, value):
		self._set_attribute('ipv4Dscp', value)

	@property
	def Ipv4Ecn(self):
		"""The ECN value specified for the IP address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Ecn')
	@Ipv4Ecn.setter
	def Ipv4Ecn(self, value):
		self._set_attribute('ipv4Ecn', value)

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
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('ipv6AddressMask')
	@Ipv6AddressMask.setter
	def Ipv6AddressMask(self, value):
		self._set_attribute('ipv6AddressMask', value)

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
	def MplsInnerMacSource(self):
		"""The MPLS Inner Source MAC value.

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerMacSource')
	@MplsInnerMacSource.setter
	def MplsInnerMacSource(self, value):
		self._set_attribute('mplsInnerMacSource', value)

	@property
	def MplsInnerVlanId(self):
		"""The MPLS Inner VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerVlanId')
	@MplsInnerVlanId.setter
	def MplsInnerVlanId(self, value):
		self._set_attribute('mplsInnerVlanId', value)

	@property
	def MplsInnerVlanPriority(self):
		"""The MPLS Inner VLAN Priority value.

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerVlanPriority')
	@MplsInnerVlanPriority.setter
	def MplsInnerVlanPriority(self, value):
		self._set_attribute('mplsInnerVlanPriority', value)

	@property
	def MplsLabel(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsLabelStackSize(self):
		"""The size of the MPLS label stack.

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelStackSize')
	@MplsLabelStackSize.setter
	def MplsLabelStackSize(self, value):
		self._set_attribute('mplsLabelStackSize', value)

	@property
	def MplsPayloadType(self):
		"""Specify the MPLS Payload Type.

		Returns:
			str(ethernet|ipv4|ipv6)
		"""
		return self._get_attribute('mplsPayloadType')
	@MplsPayloadType.setter
	def MplsPayloadType(self, value):
		self._set_attribute('mplsPayloadType', value)

	@property
	def MplsTrafficClass(self):
		"""The MPLS Traffic Class value.

		Returns:
			str
		"""
		return self._get_attribute('mplsTrafficClass')
	@MplsTrafficClass.setter
	def MplsTrafficClass(self, value):
		self._set_attribute('mplsTrafficClass', value)

	@property
	def Name(self):
		"""The name of the Traffic Source Endpoint.

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
		"""Specify the size of the Range.

		Returns:
			number
		"""
		return self._get_attribute('rangeSize')
	@RangeSize.setter
	def RangeSize(self, value):
		self._set_attribute('rangeSize', value)

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

	def add(self, ArpViaInterface=None, EnableVlan=None, GatewayMac=None, IpAddress=None, IpMask=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new mplsTrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): If selected, ARP request is conveyed through an Interface.
			EnableVlan (bool): Select this check box to make VLAN available.
			GatewayMac (str): The Gateway MAC address of the destination traffic endpoint. The default value is 00 00 00 00 00 00.
			IpAddress (str): Specify the IP address of the Source Traffic Endpoint. The default value is 0.
			IpMask (number): Specify the Mask value. The default value is 24.
			Ipv4Dscp (str): The priority specified for the IP address. The default value is 0.
			Ipv4Ecn (str): The ECN value specified for the IP address.
			Ipv6Address (str): Specify the IPv6 address of the Source Traffic Endpoint. The default value is 0.0.0.0.0.0.0.0
			Ipv6AddressMask (number): NOT DEFINED
			Ipv6Dscp (str): The priority specified for the IP address. The default value is 0.
			Ipv6Ecn (str): The ECN value specified for the IP address.
			Ipv6FlowLabel (str): The IPv6 Flow Label value.
			MacAddress (str): The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			MplsInnerMacSource (str): The MPLS Inner Source MAC value.
			MplsInnerVlanId (str): The MPLS Inner VLAN identifier.
			MplsInnerVlanPriority (str): The MPLS Inner VLAN Priority value.
			MplsLabel (str): NOT DEFINED
			MplsLabelStackSize (number): The size of the MPLS label stack.
			MplsPayloadType (str(ethernet|ipv4|ipv6)): Specify the MPLS Payload Type.
			MplsTrafficClass (str): The MPLS Traffic Class value.
			Name (str): The name of the Traffic Source Endpoint.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): NOT DEFINED
			RangeSize (number): Specify the size of the Range.
			VlanCount (number): Specify the VLAN count. The default value is 1.
			VlanId (str): Specify the VLAN ID (Outer and Inner).
			VlanPriority (str): Specify the VLAN Priority (Outer and Inner).

		Returns:
			self: This instance with all currently retrieved mplsTrafficEndPoint data using find and the newly added mplsTrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the mplsTrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, EnableVlan=None, GatewayMac=None, IpAddress=None, IpMask=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves mplsTrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve mplsTrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all mplsTrafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): If selected, ARP request is conveyed through an Interface.
			EnableVlan (bool): Select this check box to make VLAN available.
			GatewayMac (str): The Gateway MAC address of the destination traffic endpoint. The default value is 00 00 00 00 00 00.
			IpAddress (str): Specify the IP address of the Source Traffic Endpoint. The default value is 0.
			IpMask (number): Specify the Mask value. The default value is 24.
			Ipv4Dscp (str): The priority specified for the IP address. The default value is 0.
			Ipv4Ecn (str): The ECN value specified for the IP address.
			Ipv6Address (str): Specify the IPv6 address of the Source Traffic Endpoint. The default value is 0.0.0.0.0.0.0.0
			Ipv6AddressMask (number): NOT DEFINED
			Ipv6Dscp (str): The priority specified for the IP address. The default value is 0.
			Ipv6Ecn (str): The ECN value specified for the IP address.
			Ipv6FlowLabel (str): The IPv6 Flow Label value.
			MacAddress (str): The MAC Address of the source traffic endpoint. The default value is 00 00 00 00 00 00.
			MplsInnerMacSource (str): The MPLS Inner Source MAC value.
			MplsInnerVlanId (str): The MPLS Inner VLAN identifier.
			MplsInnerVlanPriority (str): The MPLS Inner VLAN Priority value.
			MplsLabel (str): NOT DEFINED
			MplsLabelStackSize (number): The size of the MPLS label stack.
			MplsPayloadType (str(ethernet|ipv4|ipv6)): Specify the MPLS Payload Type.
			MplsTrafficClass (str): The MPLS Traffic Class value.
			Name (str): The name of the Traffic Source Endpoint.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): NOT DEFINED
			RangeSize (number): Specify the size of the Range.
			VlanCount (number): Specify the VLAN count. The default value is 1.
			VlanId (str): Specify the VLAN ID (Outer and Inner).
			VlanPriority (str): Specify the VLAN Priority (Outer and Inner).

		Returns:
			self: This instance with matching mplsTrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of mplsTrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the mplsTrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
