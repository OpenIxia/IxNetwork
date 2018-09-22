from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchActionV131LearnedInfo(Base):
	"""The SwitchActionV131LearnedInfo class encapsulates a system managed switchActionV131LearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchActionV131LearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchActionV131LearnedInfo'

	def __init__(self, parent):
		super(SwitchActionV131LearnedInfo, self).__init__(parent)

	@property
	def ActionType(self):
		"""This describes the action associated with the flow entry.

		Returns:
			str
		"""
		return self._get_attribute('actionType')

	@property
	def ArpDstHwAddress(self):
		"""This describes the target hardware address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddress')

	@property
	def ArpDstIpv4Address(self):
		"""This describes the target IPv4 address in the ARP payload.

		Returns:
			number
		"""
		return self._get_attribute('arpDstIpv4Address')

	@property
	def ArpOpcode(self):
		"""This describes the ARP opcode.

		Returns:
			number
		"""
		return self._get_attribute('arpOpcode')

	@property
	def ArpSrcHwAddress(self):
		"""This describes the source hardware address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddress')

	@property
	def ArpSrcIpv4Address(self):
		"""This describes the source IPv4 address in the ARP payload.

		Returns:
			number
		"""
		return self._get_attribute('arpSrcIpv4Address')

	@property
	def EthernetDestination(self):
		"""This describes the destination address of the Ethernet port.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetSource(self):
		"""This describes the source address of the Ethernet port.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def EthernetType(self):
		"""This describes the Ethernet type of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def Experimenter(self):
		"""This describes the unique Experimenter identifier. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('experimenter')

	@property
	def ExperimenterData(self):
		"""This describes the data of the Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDatalength(self):
		"""This describes the data length of the Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDatalength')

	@property
	def GroupId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def Icmpv4Code(self):
		"""This describes the ICMP code.

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Code')

	@property
	def Icmpv4Type(self):
		"""This describes the ICMP type.

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Type')

	@property
	def Icmpv6Code(self):
		"""This describes the ICMPv6 code.

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Code')

	@property
	def Icmpv6Type(self):
		"""This describes the ICMPv6 type.

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Type')

	@property
	def IpDscp(self):
		"""This describes the IP DSCP value for advertising.

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def IpEcn(self):
		"""This describes the ECN bits of the IP header.

		Returns:
			number
		"""
		return self._get_attribute('ipEcn')

	@property
	def IpProtocol(self):
		"""This describes the IP Protocol used.

		Returns:
			number
		"""
		return self._get_attribute('ipProtocol')

	@property
	def Ipv4Destination(self):
		"""This describes the IPv4 destination address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""This describes the IPv4 source address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')

	@property
	def Ipv6Destination(self):
		"""This describes the IPv6 destination address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Destination')

	@property
	def Ipv6ExtHeader(self):
		"""This describes the IPv6 Extension Header pseudo-field.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6FlowLabel(self):
		"""This describes the IPv6 Flow label.

		Returns:
			number
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6NdSll(self):
		"""This describes the source link-layer address option in an IPv6 Neighbor Discovery message.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')

	@property
	def Ipv6NdTarget(self):
		"""This describes the target address in an IPv6 Neighbor Discovery message.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTarget')

	@property
	def Ipv6NdTll(self):
		"""This describes the target link-layer address option in an IPv6 Neighbor Discovery message

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTll')

	@property
	def Ipv6Source(self):
		"""This describes the IPv6 source address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')

	@property
	def MaxByteLength(self):
		"""This describes the maximum amount of data from a packet that should be sent when the port is OFPP_CONTROLLER.

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')

	@property
	def MplsBos(self):
		"""This describes the BoS bit in the first MPLS shim header.

		Returns:
			number
		"""
		return self._get_attribute('mplsBos')

	@property
	def MplsLabel(self):
		"""This describes the LABEL in the first MPLS shim header.

		Returns:
			number
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsTc(self):
		"""This describes the TC in the first MPLS shim header.

		Returns:
			number
		"""
		return self._get_attribute('mplsTc')

	@property
	def MplsTtl(self):
		"""This replaces the existing MPLS TTL. Only applies to packets with an existing MPLS shim header.

		Returns:
			number
		"""
		return self._get_attribute('mplsTtl')

	@property
	def NetworkTtl(self):
		"""This describes the IP TTL.

		Returns:
			number
		"""
		return self._get_attribute('networkTtl')

	@property
	def OutputPort(self):
		"""This describes the out port value. It requires matching entries to include this as an output port.

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def OutputPortType(self):
		"""This describes the Output Port Type for this Flow Range

		Returns:
			str
		"""
		return self._get_attribute('outputPortType')

	@property
	def PbbIsid(self):
		"""This describes the I-SID in the first PBB service instance tag.

		Returns:
			number
		"""
		return self._get_attribute('pbbIsid')

	@property
	def QueueId(self):
		"""This describes the queue of the port in which the packet should be enqueued.

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def SctpDestination(self):
		"""This describes the SCTP target port.

		Returns:
			number
		"""
		return self._get_attribute('sctpDestination')

	@property
	def SctpSource(self):
		"""This describes the SCTP source port.

		Returns:
			number
		"""
		return self._get_attribute('sctpSource')

	@property
	def TcpDestination(self):
		"""This describes the TCP destination address.

		Returns:
			number
		"""
		return self._get_attribute('tcpDestination')

	@property
	def TcpSource(self):
		"""This describes the TCP source address.

		Returns:
			number
		"""
		return self._get_attribute('tcpSource')

	@property
	def TunnelId(self):
		"""This describes the unique identifier used for the Tunnel.

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')

	@property
	def UdpDestination(self):
		"""This describes the UDP destination port.

		Returns:
			number
		"""
		return self._get_attribute('udpDestination')

	@property
	def UdpSource(self):
		"""This describes the UDP source port.

		Returns:
			number
		"""
		return self._get_attribute('udpSource')

	@property
	def VlanId(self):
		"""This describes the unique VLAN Identifier.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""This describes the User Priority for this VLAN.

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ActionType=None, ArpDstHwAddress=None, ArpDstIpv4Address=None, ArpOpcode=None, ArpSrcHwAddress=None, ArpSrcIpv4Address=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, Experimenter=None, ExperimenterData=None, ExperimenterDatalength=None, GroupId=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6ExtHeader=None, Ipv6FlowLabel=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6NdTll=None, Ipv6Source=None, MaxByteLength=None, MplsBos=None, MplsLabel=None, MplsTc=None, MplsTtl=None, NetworkTtl=None, OutputPort=None, OutputPortType=None, PbbIsid=None, QueueId=None, SctpDestination=None, SctpSource=None, TcpDestination=None, TcpSource=None, TunnelId=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves switchActionV131LearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchActionV131LearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchActionV131LearnedInfo data from the server.

		Args:
			ActionType (str): This describes the action associated with the flow entry.
			ArpDstHwAddress (str): This describes the target hardware address in the ARP payload.
			ArpDstIpv4Address (number): This describes the target IPv4 address in the ARP payload.
			ArpOpcode (number): This describes the ARP opcode.
			ArpSrcHwAddress (str): This describes the source hardware address in the ARP payload.
			ArpSrcIpv4Address (number): This describes the source IPv4 address in the ARP payload.
			EthernetDestination (str): This describes the destination address of the Ethernet port.
			EthernetSource (str): This describes the source address of the Ethernet port.
			EthernetType (str): This describes the Ethernet type of the flow match.
			Experimenter (number): This describes the unique Experimenter identifier. The default value is 1.
			ExperimenterData (str): This describes the data of the Experimenter.
			ExperimenterDatalength (number): This describes the data length of the Experimenter.
			GroupId (number): NOT DEFINED
			Icmpv4Code (number): This describes the ICMP code.
			Icmpv4Type (number): This describes the ICMP type.
			Icmpv6Code (number): This describes the ICMPv6 code.
			Icmpv6Type (number): This describes the ICMPv6 type.
			IpDscp (str): This describes the IP DSCP value for advertising.
			IpEcn (number): This describes the ECN bits of the IP header.
			IpProtocol (number): This describes the IP Protocol used.
			Ipv4Destination (str): This describes the IPv4 destination address.
			Ipv4Source (str): This describes the IPv4 source address.
			Ipv6Destination (str): This describes the IPv6 destination address.
			Ipv6ExtHeader (number): This describes the IPv6 Extension Header pseudo-field.
			Ipv6FlowLabel (number): This describes the IPv6 Flow label.
			Ipv6NdSll (str): This describes the source link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6NdTarget (str): This describes the target address in an IPv6 Neighbor Discovery message.
			Ipv6NdTll (str): This describes the target link-layer address option in an IPv6 Neighbor Discovery message
			Ipv6Source (str): This describes the IPv6 source address.
			MaxByteLength (number): This describes the maximum amount of data from a packet that should be sent when the port is OFPP_CONTROLLER.
			MplsBos (number): This describes the BoS bit in the first MPLS shim header.
			MplsLabel (number): This describes the LABEL in the first MPLS shim header.
			MplsTc (number): This describes the TC in the first MPLS shim header.
			MplsTtl (number): This replaces the existing MPLS TTL. Only applies to packets with an existing MPLS shim header.
			NetworkTtl (number): This describes the IP TTL.
			OutputPort (number): This describes the out port value. It requires matching entries to include this as an output port.
			OutputPortType (str): This describes the Output Port Type for this Flow Range
			PbbIsid (number): This describes the I-SID in the first PBB service instance tag.
			QueueId (number): This describes the queue of the port in which the packet should be enqueued.
			SctpDestination (number): This describes the SCTP target port.
			SctpSource (number): This describes the SCTP source port.
			TcpDestination (number): This describes the TCP destination address.
			TcpSource (number): This describes the TCP source address.
			TunnelId (str): This describes the unique identifier used for the Tunnel.
			UdpDestination (number): This describes the UDP destination port.
			UdpSource (number): This describes the UDP source port.
			VlanId (number): This describes the unique VLAN Identifier.
			VlanPriority (number): This describes the User Priority for this VLAN.

		Returns:
			self: This instance with matching switchActionV131LearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchActionV131LearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchActionV131LearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
