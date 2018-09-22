from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowStatMatchCriteria131TriggerAttributes(Base):
	"""The FlowStatMatchCriteria131TriggerAttributes class encapsulates a required flowStatMatchCriteria131TriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowStatMatchCriteria131TriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flowStatMatchCriteria131TriggerAttributes'

	def __init__(self, parent):
		super(FlowStatMatchCriteria131TriggerAttributes, self).__init__(parent)

	@property
	def ArpDstHwAddr(self):
		"""Value of the ARP destination hardware address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpDstHwAddr')
	@ArpDstHwAddr.setter
	def ArpDstHwAddr(self, value):
		self._set_attribute('arpDstHwAddr', value)

	@property
	def ArpDstIpv4Addr(self):
		"""The ARP destination IPv4 address field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpDstIpv4Addr')
	@ArpDstIpv4Addr.setter
	def ArpDstIpv4Addr(self, value):
		self._set_attribute('arpDstIpv4Addr', value)

	@property
	def ArpOpcode(self):
		"""Value of the ARP opcode field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpOpcode')
	@ArpOpcode.setter
	def ArpOpcode(self, value):
		self._set_attribute('arpOpcode', value)

	@property
	def ArpSrcHwAddr(self):
		"""Value of the ARP source hardware address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpSrcHwAddr')
	@ArpSrcHwAddr.setter
	def ArpSrcHwAddr(self, value):
		self._set_attribute('arpSrcHwAddr', value)

	@property
	def ArpSrcIpv4Addr(self):
		"""The ARP source IPv4 address field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpSrcIpv4Addr')
	@ArpSrcIpv4Addr.setter
	def ArpSrcIpv4Addr(self, value):
		self._set_attribute('arpSrcIpv4Addr', value)

	@property
	def Cookie(self):
		"""The Cookie field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('cookie')
	@Cookie.setter
	def Cookie(self, value):
		self._set_attribute('cookie', value)

	@property
	def EthernetDestination(self):
		"""The Ethernet destination address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""The Ethernet source address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""The type of Ethernet port used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def ExperimenterData(self):
		"""The experimenter data field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDataLength(self):
		"""Value of the Experimenter data length field.

		Returns:
			dict(arg1:number,arg2:str)
		"""
		return self._get_attribute('experimenterDataLength')
	@ExperimenterDataLength.setter
	def ExperimenterDataLength(self, value):
		self._set_attribute('experimenterDataLength', value)

	@property
	def ExperimenterField(self):
		"""Value of the Experimenter Field field.

		Returns:
			dict(arg1:number,arg2:str)
		"""
		return self._get_attribute('experimenterField')
	@ExperimenterField.setter
	def ExperimenterField(self, value):
		self._set_attribute('experimenterField', value)

	@property
	def ExperimenterHashmask(self):
		"""The experimented hasmask field value.

		Returns:
			dict(arg1:bool,arg2:str)
		"""
		return self._get_attribute('experimenterHashmask')
	@ExperimenterHashmask.setter
	def ExperimenterHashmask(self, value):
		self._set_attribute('experimenterHashmask', value)

	@property
	def ExperimenterId(self):
		"""Value of the experimenter ID field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('experimenterId')
	@ExperimenterId.setter
	def ExperimenterId(self, value):
		self._set_attribute('experimenterId', value)

	@property
	def Icmpv4Code(self):
		"""The code of ICMPv4 port used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv4Code')
	@Icmpv4Code.setter
	def Icmpv4Code(self, value):
		self._set_attribute('icmpv4Code', value)

	@property
	def Icmpv4Type(self):
		"""The type of ICMPv4 port used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv4Type')
	@Icmpv4Type.setter
	def Icmpv4Type(self, value):
		self._set_attribute('icmpv4Type', value)

	@property
	def Icmpv6Code(self):
		"""Value of the ICMPv4 code field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""Value of the ICMPv6 type field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def InPort(self):
		"""The input port used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""The IP DSCP value for advertising.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""The IP ECN field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""The IP protocol used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""The IPv4 destination address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""The IPv4 source address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv6Destination(self):
		"""Value of the IPv6 destination field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6Destination')
	@Ipv6Destination.setter
	def Ipv6Destination(self, value):
		self._set_attribute('ipv6Destination', value)

	@property
	def Ipv6ExtHeader(self):
		"""The Ipv6 extension header field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6FlowLabel(self):
		"""Value of the IPv6 flow label field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NdDll(self):
		"""The IPv6 ND DLL field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6NdDll')
	@Ipv6NdDll.setter
	def Ipv6NdDll(self, value):
		self._set_attribute('ipv6NdDll', value)

	@property
	def Ipv6NdSll(self):
		"""Source link-layer for IPv6 neighbour discovery.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6NdSll')
	@Ipv6NdSll.setter
	def Ipv6NdSll(self, value):
		self._set_attribute('ipv6NdSll', value)

	@property
	def Ipv6NdTarget(self):
		"""The IPv6 ND target field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6NdTarget')
	@Ipv6NdTarget.setter
	def Ipv6NdTarget(self, value):
		self._set_attribute('ipv6NdTarget', value)

	@property
	def Ipv6Source(self):
		"""Value of the IPv6 source field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6Source')
	@Ipv6Source.setter
	def Ipv6Source(self, value):
		self._set_attribute('ipv6Source', value)

	@property
	def MetaData(self):
		"""Value of the metadata field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('metaData')
	@MetaData.setter
	def MetaData(self, value):
		self._set_attribute('metaData', value)

	@property
	def MplsBos(self):
		"""Value of the MPLS BoS field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""Value of the MPLS label field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""The MPLS TC field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def PbbISid(self):
		"""Value of the PBB I-SID field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('pbbISid')
	@PbbISid.setter
	def PbbISid(self, value):
		self._set_attribute('pbbISid', value)

	@property
	def PhysicalInPort(self):
		"""Value of the Physical IN port field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('physicalInPort')
	@PhysicalInPort.setter
	def PhysicalInPort(self, value):
		self._set_attribute('physicalInPort', value)

	@property
	def SctpDestination(self):
		"""The SCTP destination field value.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""Value of the SCTP source field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def TcpDestination(self):
		"""The Transport destination address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""Value of the TCP source field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('tcpSource')
	@TcpSource.setter
	def TcpSource(self, value):
		self._set_attribute('tcpSource', value)

	@property
	def TunnelId(self):
		"""Value of the tunnel ID field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('tunnelId')
	@TunnelId.setter
	def TunnelId(self, value):
		self._set_attribute('tunnelId', value)

	@property
	def UdpDestination(self):
		"""Value of the UDP destination field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""Value of the UDP source field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""The unique VLAN Identifier.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""The User Priority for this VLAN.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
