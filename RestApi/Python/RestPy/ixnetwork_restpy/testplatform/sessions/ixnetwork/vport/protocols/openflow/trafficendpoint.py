from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrafficEndPoint(Base):
	"""The TrafficEndPoint class encapsulates a user managed trafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'trafficEndPoint'

	def __init__(self, parent):
		super(TrafficEndPoint, self).__init__(parent)

	@property
	def ArpViaInterface(self):
		"""If true, ARP request is conveyed through an Interface.

		Returns:
			bool
		"""
		return self._get_attribute('arpViaInterface')
	@ArpViaInterface.setter
	def ArpViaInterface(self, value):
		self._set_attribute('arpViaInterface', value)

	@property
	def CustomEtherHeaderLength(self):
		"""Specifies the Custom Header length in bytes.

		Returns:
			number
		"""
		return self._get_attribute('customEtherHeaderLength')
	@CustomEtherHeaderLength.setter
	def CustomEtherHeaderLength(self, value):
		self._set_attribute('customEtherHeaderLength', value)

	@property
	def CustomEtherHeaderValue(self):
		"""Specifies the Custom ether Header value.

		Returns:
			str
		"""
		return self._get_attribute('customEtherHeaderValue')
	@CustomEtherHeaderValue.setter
	def CustomEtherHeaderValue(self, value):
		self._set_attribute('customEtherHeaderValue', value)

	@property
	def CustomEtherType(self):
		"""Specifies the custom Ether Type. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('customEtherType')
	@CustomEtherType.setter
	def CustomEtherType(self, value):
		self._set_attribute('customEtherType', value)

	@property
	def CustomIpHeaderLength(self):
		"""Specifies the custom Header length in bytes.

		Returns:
			number
		"""
		return self._get_attribute('customIpHeaderLength')
	@CustomIpHeaderLength.setter
	def CustomIpHeaderLength(self, value):
		self._set_attribute('customIpHeaderLength', value)

	@property
	def CustomIpHeaderValue(self):
		"""Specifies the Custom Header value.

		Returns:
			str
		"""
		return self._get_attribute('customIpHeaderValue')
	@CustomIpHeaderValue.setter
	def CustomIpHeaderValue(self, value):
		self._set_attribute('customIpHeaderValue', value)

	@property
	def CustomIpProtocol(self):
		"""Specifies the custom IP Protocol for the Source Traffic Endpoints. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('customIpProtocol')
	@CustomIpProtocol.setter
	def CustomIpProtocol(self, value):
		self._set_attribute('customIpProtocol', value)

	@property
	def DestinationPort(self):
		"""Specifies the transport destination port. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('destinationPort')
	@DestinationPort.setter
	def DestinationPort(self, value):
		self._set_attribute('destinationPort', value)

	@property
	def EnableMacInMac(self):
		"""Enables the PBB-specific fields.

		Returns:
			bool
		"""
		return self._get_attribute('enableMacInMac')
	@EnableMacInMac.setter
	def EnableMacInMac(self, value):
		self._set_attribute('enableMacInMac', value)

	@property
	def EnableVlan(self):
		"""If enabled, VLAN is available.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def EtherType(self):
		"""Specifies the Ether Type to be used.

		Returns:
			str(custom|ipv4|ipv6|mplsUnicast)
		"""
		return self._get_attribute('etherType')
	@EtherType.setter
	def EtherType(self, value):
		self._set_attribute('etherType', value)

	@property
	def GatewayMac(self):
		"""Specifies the Gateway MAC address of the source traffic endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('gatewayMac')
	@GatewayMac.setter
	def GatewayMac(self, value):
		self._set_attribute('gatewayMac', value)

	@property
	def IpAddress(self):
		"""Specifies the IPv4 address of the Source Traffic Endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpMask(self):
		"""Specifies the Mask value.

		Returns:
			number
		"""
		return self._get_attribute('ipMask')
	@IpMask.setter
	def IpMask(self, value):
		self._set_attribute('ipMask', value)

	@property
	def IpProtocol(self):
		"""Specifies the IP Protocol to be used.

		Returns:
			str(custom|tcp|udp)
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def IpTos(self):
		"""Specifies the Terms of Service of the IP Protocol. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('ipTos')
	@IpTos.setter
	def IpTos(self, value):
		self._set_attribute('ipTos', value)

	@property
	def Ipv4Dscp(self):
		"""Specifies value of Ipv4 DSCP field.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Dscp')
	@Ipv4Dscp.setter
	def Ipv4Dscp(self, value):
		self._set_attribute('ipv4Dscp', value)

	@property
	def Ipv4Ecn(self):
		"""Specifies the IPv4 ECN field, which is actually the last 2 bits of ToS field.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Ecn')
	@Ipv4Ecn.setter
	def Ipv4Ecn(self, value):
		self._set_attribute('ipv4Ecn', value)

	@property
	def Ipv6Address(self):
		"""Specifies the IPv6 address to be used in the traffic endpoint.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Address')
	@Ipv6Address.setter
	def Ipv6Address(self, value):
		self._set_attribute('ipv6Address', value)

	@property
	def Ipv6AddressMask(self):
		"""Specifies the mask of IPv6 address

		Returns:
			number
		"""
		return self._get_attribute('ipv6AddressMask')
	@Ipv6AddressMask.setter
	def Ipv6AddressMask(self, value):
		self._set_attribute('ipv6AddressMask', value)

	@property
	def Ipv6CustomHeaderLength(self):
		"""Specifies the IPv6 custom header length. This indicates the number of bytes in the field IPv6 custom header Value.

		Returns:
			number
		"""
		return self._get_attribute('ipv6CustomHeaderLength')
	@Ipv6CustomHeaderLength.setter
	def Ipv6CustomHeaderLength(self, value):
		self._set_attribute('ipv6CustomHeaderLength', value)

	@property
	def Ipv6CustomHeaderValue(self):
		"""Specifies the IPv6 custom header value. This is populated with hexadecimal byte string containing the protocol header content.

		Returns:
			str
		"""
		return self._get_attribute('ipv6CustomHeaderValue')
	@Ipv6CustomHeaderValue.setter
	def Ipv6CustomHeaderValue(self, value):
		self._set_attribute('ipv6CustomHeaderValue', value)

	@property
	def Ipv6CustomNextHeader(self):
		"""Specifies the custom IPv6 Next header. This has dependency on the field IPv6 Next Header which should be set to custom. It actually specifies the protocol type of header, the actual content and length of protocol header is specified in other fields. Using this custom header, user can send any other protocol header except TCP/UDP.

		Returns:
			str
		"""
		return self._get_attribute('ipv6CustomNextHeader')
	@Ipv6CustomNextHeader.setter
	def Ipv6CustomNextHeader(self, value):
		self._set_attribute('ipv6CustomNextHeader', value)

	@property
	def Ipv6Dscp(self):
		"""Specifies the IPv6 DSCP field. This is the set of first 6 bits of the ToS field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Dscp')
	@Ipv6Dscp.setter
	def Ipv6Dscp(self, value):
		self._set_attribute('ipv6Dscp', value)

	@property
	def Ipv6Ecn(self):
		"""Specifies the IPv6 ECN field, which is actually the last 2 bits of ToS field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Ecn')
	@Ipv6Ecn.setter
	def Ipv6Ecn(self, value):
		self._set_attribute('ipv6Ecn', value)

	@property
	def Ipv6FlowLabel(self):
		"""Specifies the IPv6 flow label field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NextHeader(self):
		"""Specifies the IPv6 Next header. It can be TCP, UDP or a custom header.

		Returns:
			str(custom|tcp|udp)
		"""
		return self._get_attribute('ipv6NextHeader')
	@Ipv6NextHeader.setter
	def Ipv6NextHeader(self, value):
		self._set_attribute('ipv6NextHeader', value)

	@property
	def MacAddress(self):
		"""Specifies the MAC Address of the source traffic endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MplsInnerMacSource(self):
		"""Specifies the Inner MAC source of MPLS. Applicable when the MPLS payload type is ethernet.

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerMacSource')
	@MplsInnerMacSource.setter
	def MplsInnerMacSource(self, value):
		self._set_attribute('mplsInnerMacSource', value)

	@property
	def MplsInnerVlanId(self):
		"""Specifies the inner VLAN ID. Applicable when the MPLS payload type is ethernet.

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerVlanId')
	@MplsInnerVlanId.setter
	def MplsInnerVlanId(self, value):
		self._set_attribute('mplsInnerVlanId', value)

	@property
	def MplsInnerVlanPriority(self):
		"""Specifies the Inner VLAN priority. Applicable when the MPLS payload type is ethernet.

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerVlanPriority')
	@MplsInnerVlanPriority.setter
	def MplsInnerVlanPriority(self, value):
		self._set_attribute('mplsInnerVlanPriority', value)

	@property
	def MplsLabel(self):
		"""Value of the MPLS label field.

		Returns:
			str
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsLabelStackSize(self):
		"""Specifies the MPLS label stack size. Indicates the number of MPLS tage that are appended. Can take a max of 3.

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelStackSize')
	@MplsLabelStackSize.setter
	def MplsLabelStackSize(self, value):
		self._set_attribute('mplsLabelStackSize', value)

	@property
	def MplsPayloadType(self):
		"""Specifies the payload type in MPLS. Can be IPv4/IPv6 (L3) or Ethernet (L2).

		Returns:
			str(ethernet|ipv4|ipv6)
		"""
		return self._get_attribute('mplsPayloadType')
	@MplsPayloadType.setter
	def MplsPayloadType(self, value):
		self._set_attribute('mplsPayloadType', value)

	@property
	def MplsTrafficClass(self):
		"""Specifies the MPLS traffic class.

		Returns:
			str
		"""
		return self._get_attribute('mplsTrafficClass')
	@MplsTrafficClass.setter
	def MplsTrafficClass(self, value):
		self._set_attribute('mplsTrafficClass', value)

	@property
	def Name(self):
		"""Specifies the name of the Traffic endpoint.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PbbDestinamtionMac(self):
		"""Specifies the B-Destination MAC.

		Returns:
			str
		"""
		return self._get_attribute('pbbDestinamtionMac')
	@PbbDestinamtionMac.setter
	def PbbDestinamtionMac(self, value):
		self._set_attribute('pbbDestinamtionMac', value)

	@property
	def PbbEtherType(self):
		"""Specifies the B-Ether Type.

		Returns:
			str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)
		"""
		return self._get_attribute('pbbEtherType')
	@PbbEtherType.setter
	def PbbEtherType(self, value):
		self._set_attribute('pbbEtherType', value)

	@property
	def PbbIsId(self):
		"""Value of the PBB I-SID field.

		Returns:
			str
		"""
		return self._get_attribute('pbbIsId')
	@PbbIsId.setter
	def PbbIsId(self, value):
		self._set_attribute('pbbIsId', value)

	@property
	def PbbSourceMac(self):
		"""Specifies the B-Source MAC.

		Returns:
			str
		"""
		return self._get_attribute('pbbSourceMac')
	@PbbSourceMac.setter
	def PbbSourceMac(self, value):
		self._set_attribute('pbbSourceMac', value)

	@property
	def PbbVlanId(self):
		"""Specifies the B-VLAN ID.

		Returns:
			str
		"""
		return self._get_attribute('pbbVlanId')
	@PbbVlanId.setter
	def PbbVlanId(self, value):
		self._set_attribute('pbbVlanId', value)

	@property
	def PbbVlanPcp(self):
		"""Specifies the B-VLAN priority.

		Returns:
			str
		"""
		return self._get_attribute('pbbVlanPcp')
	@PbbVlanPcp.setter
	def PbbVlanPcp(self, value):
		self._set_attribute('pbbVlanPcp', value)

	@property
	def ProtocolInterface(self):
		"""Specifies the name of the protocol interface being used for this OpenFlow configuration.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def RangeSize(self):
		"""Specifies the size of the traffic range.

		Returns:
			number
		"""
		return self._get_attribute('rangeSize')
	@RangeSize.setter
	def RangeSize(self, value):
		self._set_attribute('rangeSize', value)

	@property
	def SourcePort(self):
		"""Specifies the transport source port. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('sourcePort')
	@SourcePort.setter
	def SourcePort(self, value):
		self._set_attribute('sourcePort', value)

	@property
	def UdpDestination(self):
		"""Value of the UDP destination field.

		Returns:
			str
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""Value of the UDP source field.

		Returns:
			str
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanCount(self):
		"""Specifies the VLAN Count.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""Specifies the VLAN ID. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""Specifies the VLAN Priority. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, CustomIpHeaderLength=None, CustomIpHeaderValue=None, CustomIpProtocol=None, DestinationPort=None, EnableMacInMac=None, EnableVlan=None, EtherType=None, GatewayMac=None, IpAddress=None, IpMask=None, IpProtocol=None, IpTos=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6CustomHeaderLength=None, Ipv6CustomHeaderValue=None, Ipv6CustomNextHeader=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, Ipv6NextHeader=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new trafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): If true, ARP request is conveyed through an Interface.
			CustomEtherHeaderLength (number): Specifies the Custom Header length in bytes.
			CustomEtherHeaderValue (str): Specifies the Custom ether Header value.
			CustomEtherType (str): Specifies the custom Ether Type. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			CustomIpHeaderLength (number): Specifies the custom Header length in bytes.
			CustomIpHeaderValue (str): Specifies the Custom Header value.
			CustomIpProtocol (str): Specifies the custom IP Protocol for the Source Traffic Endpoints. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			DestinationPort (str): Specifies the transport destination port. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			EnableMacInMac (bool): Enables the PBB-specific fields.
			EnableVlan (bool): If enabled, VLAN is available.
			EtherType (str(custom|ipv4|ipv6|mplsUnicast)): Specifies the Ether Type to be used.
			GatewayMac (str): Specifies the Gateway MAC address of the source traffic endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpAddress (str): Specifies the IPv4 address of the Source Traffic Endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpMask (number): Specifies the Mask value.
			IpProtocol (str(custom|tcp|udp)): Specifies the IP Protocol to be used.
			IpTos (str): Specifies the Terms of Service of the IP Protocol. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			Ipv4Dscp (str): Specifies value of Ipv4 DSCP field.
			Ipv4Ecn (str): Specifies the IPv4 ECN field, which is actually the last 2 bits of ToS field.
			Ipv6Address (str): Specifies the IPv6 address to be used in the traffic endpoint.
			Ipv6AddressMask (number): Specifies the mask of IPv6 address
			Ipv6CustomHeaderLength (number): Specifies the IPv6 custom header length. This indicates the number of bytes in the field IPv6 custom header Value.
			Ipv6CustomHeaderValue (str): Specifies the IPv6 custom header value. This is populated with hexadecimal byte string containing the protocol header content.
			Ipv6CustomNextHeader (str): Specifies the custom IPv6 Next header. This has dependency on the field IPv6 Next Header which should be set to custom. It actually specifies the protocol type of header, the actual content and length of protocol header is specified in other fields. Using this custom header, user can send any other protocol header except TCP/UDP.
			Ipv6Dscp (str): Specifies the IPv6 DSCP field. This is the set of first 6 bits of the ToS field.
			Ipv6Ecn (str): Specifies the IPv6 ECN field, which is actually the last 2 bits of ToS field.
			Ipv6FlowLabel (str): Specifies the IPv6 flow label field.
			Ipv6NextHeader (str(custom|tcp|udp)): Specifies the IPv6 Next header. It can be TCP, UDP or a custom header.
			MacAddress (str): Specifies the MAC Address of the source traffic endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			MplsInnerMacSource (str): Specifies the Inner MAC source of MPLS. Applicable when the MPLS payload type is ethernet.
			MplsInnerVlanId (str): Specifies the inner VLAN ID. Applicable when the MPLS payload type is ethernet.
			MplsInnerVlanPriority (str): Specifies the Inner VLAN priority. Applicable when the MPLS payload type is ethernet.
			MplsLabel (str): Value of the MPLS label field.
			MplsLabelStackSize (number): Specifies the MPLS label stack size. Indicates the number of MPLS tage that are appended. Can take a max of 3.
			MplsPayloadType (str(ethernet|ipv4|ipv6)): Specifies the payload type in MPLS. Can be IPv4/IPv6 (L3) or Ethernet (L2).
			MplsTrafficClass (str): Specifies the MPLS traffic class.
			Name (str): Specifies the name of the Traffic endpoint.
			PbbDestinamtionMac (str): Specifies the B-Destination MAC.
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): Specifies the B-Ether Type.
			PbbIsId (str): Value of the PBB I-SID field.
			PbbSourceMac (str): Specifies the B-Source MAC.
			PbbVlanId (str): Specifies the B-VLAN ID.
			PbbVlanPcp (str): Specifies the B-VLAN priority.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): Specifies the name of the protocol interface being used for this OpenFlow configuration.
			RangeSize (number): Specifies the size of the traffic range.
			SourcePort (str): Specifies the transport source port. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			UdpDestination (str): Value of the UDP destination field.
			UdpSource (str): Value of the UDP source field.
			VlanCount (number): Specifies the VLAN Count.
			VlanId (str): Specifies the VLAN ID. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			VlanPriority (str): Specifies the VLAN Priority. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			self: This instance with all currently retrieved trafficEndPoint data using find and the newly added trafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the trafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, CustomIpHeaderLength=None, CustomIpHeaderValue=None, CustomIpProtocol=None, DestinationPort=None, EnableMacInMac=None, EnableVlan=None, EtherType=None, GatewayMac=None, IpAddress=None, IpMask=None, IpProtocol=None, IpTos=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6CustomHeaderLength=None, Ipv6CustomHeaderValue=None, Ipv6CustomNextHeader=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, Ipv6NextHeader=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves trafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve trafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all trafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): If true, ARP request is conveyed through an Interface.
			CustomEtherHeaderLength (number): Specifies the Custom Header length in bytes.
			CustomEtherHeaderValue (str): Specifies the Custom ether Header value.
			CustomEtherType (str): Specifies the custom Ether Type. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			CustomIpHeaderLength (number): Specifies the custom Header length in bytes.
			CustomIpHeaderValue (str): Specifies the Custom Header value.
			CustomIpProtocol (str): Specifies the custom IP Protocol for the Source Traffic Endpoints. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			DestinationPort (str): Specifies the transport destination port. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			EnableMacInMac (bool): Enables the PBB-specific fields.
			EnableVlan (bool): If enabled, VLAN is available.
			EtherType (str(custom|ipv4|ipv6|mplsUnicast)): Specifies the Ether Type to be used.
			GatewayMac (str): Specifies the Gateway MAC address of the source traffic endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpAddress (str): Specifies the IPv4 address of the Source Traffic Endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			IpMask (number): Specifies the Mask value.
			IpProtocol (str(custom|tcp|udp)): Specifies the IP Protocol to be used.
			IpTos (str): Specifies the Terms of Service of the IP Protocol. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			Ipv4Dscp (str): Specifies value of Ipv4 DSCP field.
			Ipv4Ecn (str): Specifies the IPv4 ECN field, which is actually the last 2 bits of ToS field.
			Ipv6Address (str): Specifies the IPv6 address to be used in the traffic endpoint.
			Ipv6AddressMask (number): Specifies the mask of IPv6 address
			Ipv6CustomHeaderLength (number): Specifies the IPv6 custom header length. This indicates the number of bytes in the field IPv6 custom header Value.
			Ipv6CustomHeaderValue (str): Specifies the IPv6 custom header value. This is populated with hexadecimal byte string containing the protocol header content.
			Ipv6CustomNextHeader (str): Specifies the custom IPv6 Next header. This has dependency on the field IPv6 Next Header which should be set to custom. It actually specifies the protocol type of header, the actual content and length of protocol header is specified in other fields. Using this custom header, user can send any other protocol header except TCP/UDP.
			Ipv6Dscp (str): Specifies the IPv6 DSCP field. This is the set of first 6 bits of the ToS field.
			Ipv6Ecn (str): Specifies the IPv6 ECN field, which is actually the last 2 bits of ToS field.
			Ipv6FlowLabel (str): Specifies the IPv6 flow label field.
			Ipv6NextHeader (str(custom|tcp|udp)): Specifies the IPv6 Next header. It can be TCP, UDP or a custom header.
			MacAddress (str): Specifies the MAC Address of the source traffic endpoint. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			MplsInnerMacSource (str): Specifies the Inner MAC source of MPLS. Applicable when the MPLS payload type is ethernet.
			MplsInnerVlanId (str): Specifies the inner VLAN ID. Applicable when the MPLS payload type is ethernet.
			MplsInnerVlanPriority (str): Specifies the Inner VLAN priority. Applicable when the MPLS payload type is ethernet.
			MplsLabel (str): Value of the MPLS label field.
			MplsLabelStackSize (number): Specifies the MPLS label stack size. Indicates the number of MPLS tage that are appended. Can take a max of 3.
			MplsPayloadType (str(ethernet|ipv4|ipv6)): Specifies the payload type in MPLS. Can be IPv4/IPv6 (L3) or Ethernet (L2).
			MplsTrafficClass (str): Specifies the MPLS traffic class.
			Name (str): Specifies the name of the Traffic endpoint.
			PbbDestinamtionMac (str): Specifies the B-Destination MAC.
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): Specifies the B-Ether Type.
			PbbIsId (str): Value of the PBB I-SID field.
			PbbSourceMac (str): Specifies the B-Source MAC.
			PbbVlanId (str): Specifies the B-VLAN ID.
			PbbVlanPcp (str): Specifies the B-VLAN priority.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): Specifies the name of the protocol interface being used for this OpenFlow configuration.
			RangeSize (number): Specifies the size of the traffic range.
			SourcePort (str): Specifies the transport source port. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			UdpDestination (str): Value of the UDP destination field.
			UdpSource (str): Value of the UDP source field.
			VlanCount (number): Specifies the VLAN Count.
			VlanId (str): Specifies the VLAN ID. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.
			VlanPriority (str): Specifies the VLAN Priority. This attribute is of range kind and can take wildcard as input. It is composed of sub-attributes like, startValue, stepValue, repeatCount, wrapCount, and incrementMode.

		Returns:
			self: This instance with matching trafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
