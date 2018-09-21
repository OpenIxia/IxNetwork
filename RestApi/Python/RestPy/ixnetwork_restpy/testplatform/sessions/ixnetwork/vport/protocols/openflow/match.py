from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Match(Base):
	"""The Match class encapsulates a required match node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Match property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'match'

	def __init__(self, parent):
		super(Match, self).__init__(parent)

	@property
	def ArpDestinationHardwareAddress(self):
		"""If selected, ARP Destination Hardware Address matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('arpDestinationHardwareAddress')
	@ArpDestinationHardwareAddress.setter
	def ArpDestinationHardwareAddress(self, value):
		self._set_attribute('arpDestinationHardwareAddress', value)

	@property
	def ArpDestinationIpv4Address(self):
		"""If selected, ARP Destination IPv4 Address matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('arpDestinationIpv4Address')
	@ArpDestinationIpv4Address.setter
	def ArpDestinationIpv4Address(self, value):
		self._set_attribute('arpDestinationIpv4Address', value)

	@property
	def ArpOpcode(self):
		"""If selected, ARP Opcode matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('arpOpcode')
	@ArpOpcode.setter
	def ArpOpcode(self, value):
		self._set_attribute('arpOpcode', value)

	@property
	def ArpSourceHardwareAddress(self):
		"""If selected, ARP Source Hardware Address matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('arpSourceHardwareAddress')
	@ArpSourceHardwareAddress.setter
	def ArpSourceHardwareAddress(self, value):
		self._set_attribute('arpSourceHardwareAddress', value)

	@property
	def ArpSourceIpv4Address(self):
		"""If selected, ARP Source IPv4 Address matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('arpSourceIpv4Address')
	@ArpSourceIpv4Address.setter
	def ArpSourceIpv4Address(self, value):
		self._set_attribute('arpSourceIpv4Address', value)

	@property
	def EthernetDestination(self):
		"""If selected, Ethernet Destination matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""If selected, Ethernet Source matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""If selected, Ethernet Type matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def Experimenter(self):
		"""If selected, Experimenter matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def IcmpCode(self):
		"""If selected, ICMP Code matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('icmpCode')
	@IcmpCode.setter
	def IcmpCode(self, value):
		self._set_attribute('icmpCode', value)

	@property
	def IcmpType(self):
		"""If selected, ICMP Type matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('icmpType')
	@IcmpType.setter
	def IcmpType(self, value):
		self._set_attribute('icmpType', value)

	@property
	def Icmpv6Code(self):
		"""If selected, ICMPv6 Code matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""If selected, ICMPv6 Type matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def InPort(self):
		"""If selected, In Port matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""If selected, IP DSCP matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""If selected, IP ECN matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""If selected, IP Protocol matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""If selected, IPv4 Destination matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""If selected, IPv4 Source matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv6Destination(self):
		"""If selected, IPv6 Destination matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6Destination')
	@Ipv6Destination.setter
	def Ipv6Destination(self, value):
		self._set_attribute('ipv6Destination', value)

	@property
	def Ipv6ExtHeader(self):
		"""If selected, IPv6 Ext Header matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6FlowLabel(self):
		"""If selected, IPv6 Flow Label matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NdSll(self):
		"""If selected, IPv6 ND SLL matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6NdSll')
	@Ipv6NdSll.setter
	def Ipv6NdSll(self, value):
		self._set_attribute('ipv6NdSll', value)

	@property
	def Ipv6NdTarget(self):
		"""If selected, IPv6 ND Target matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6NdTarget')
	@Ipv6NdTarget.setter
	def Ipv6NdTarget(self, value):
		self._set_attribute('ipv6NdTarget', value)

	@property
	def Ipv6NdTll(self):
		"""If selected, IPv6 ND TLL matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6NdTll')
	@Ipv6NdTll.setter
	def Ipv6NdTll(self, value):
		self._set_attribute('ipv6NdTll', value)

	@property
	def Ipv6Source(self):
		"""If selected, IPv6 Source matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('ipv6Source')
	@Ipv6Source.setter
	def Ipv6Source(self, value):
		self._set_attribute('ipv6Source', value)

	@property
	def Metadata(self):
		"""If selected, Metadata matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('metadata')
	@Metadata.setter
	def Metadata(self, value):
		self._set_attribute('metadata', value)

	@property
	def MplsBos(self):
		"""If selected, MPLS BoS matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""If selected, MPLS Label matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""If selected, MPLS TC matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def PbbIsid(self):
		"""If selected, PBB ISID matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('pbbIsid')
	@PbbIsid.setter
	def PbbIsid(self, value):
		self._set_attribute('pbbIsid', value)

	@property
	def PhysicalInPort(self):
		"""If selected, Physical In Port matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('physicalInPort')
	@PhysicalInPort.setter
	def PhysicalInPort(self, value):
		self._set_attribute('physicalInPort', value)

	@property
	def SctpDestination(self):
		"""If selected, SCTP Destination matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""If selected, SCTP Source matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def TcpDestination(self):
		"""If selected, TCP Destination matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""If selected, TCP Source matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('tcpSource')
	@TcpSource.setter
	def TcpSource(self, value):
		self._set_attribute('tcpSource', value)

	@property
	def TunnelId(self):
		"""If selected, Tunnel ID matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('tunnelId')
	@TunnelId.setter
	def TunnelId(self, value):
		self._set_attribute('tunnelId', value)

	@property
	def UdpDestination(self):
		"""If selected, UDP Destination matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""If selected, UDP Source matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""If selected, VLAN ID matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""If selected, VLAN Priority matching is supported.

		Returns:
			bool
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
