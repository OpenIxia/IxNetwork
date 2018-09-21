from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchFlowMatchCriteria131TriggerAttributes(Base):
	"""The SwitchFlowMatchCriteria131TriggerAttributes class encapsulates a required switchFlowMatchCriteria131TriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchFlowMatchCriteria131TriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'switchFlowMatchCriteria131TriggerAttributes'

	def __init__(self, parent):
		super(SwitchFlowMatchCriteria131TriggerAttributes, self).__init__(parent)

	@property
	def ArpDstHwAddr(self):
		"""This describes the target hardware address in the ARP payload.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpDstHwAddr')
	@ArpDstHwAddr.setter
	def ArpDstHwAddr(self, value):
		self._set_attribute('arpDstHwAddr', value)

	@property
	def ArpDstIpv4Addr(self):
		"""This describes the target IPv4 address in the ARP payload.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpDstIpv4Addr')
	@ArpDstIpv4Addr.setter
	def ArpDstIpv4Addr(self, value):
		self._set_attribute('arpDstIpv4Addr', value)

	@property
	def ArpOpcode(self):
		"""This describes the ARP opcode.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpOpcode')
	@ArpOpcode.setter
	def ArpOpcode(self, value):
		self._set_attribute('arpOpcode', value)

	@property
	def ArpSrcHwAddr(self):
		"""This describes the source hardware address in the ARP payload.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpSrcHwAddr')
	@ArpSrcHwAddr.setter
	def ArpSrcHwAddr(self, value):
		self._set_attribute('arpSrcHwAddr', value)

	@property
	def ArpSrcIpv4Addr(self):
		"""This describes the source IPv4 address in the ARP payload.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('arpSrcIpv4Addr')
	@ArpSrcIpv4Addr.setter
	def ArpSrcIpv4Addr(self, value):
		self._set_attribute('arpSrcIpv4Addr', value)

	@property
	def Cookie(self):
		"""This describes the Cookie of the flow entry that was looked up. This is the opaque controller-issued identifier.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('cookie')
	@Cookie.setter
	def Cookie(self, value):
		self._set_attribute('cookie', value)

	@property
	def EthernetDestination(self):
		"""This describes the destination address of the Ethernet port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""This describes the source address of the Ethernet port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""This describes the Ethernet type of the flow match.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def ExperimenterData(self):
		"""This describes the data of the Experimenter.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDataLength(self):
		"""This describes the data length of the Experimenter.

		Returns:
			dict(arg1:number,arg2:str)
		"""
		return self._get_attribute('experimenterDataLength')
	@ExperimenterDataLength.setter
	def ExperimenterDataLength(self, value):
		self._set_attribute('experimenterDataLength', value)

	@property
	def ExperimenterField(self):
		"""This describes the field type for experimenter match.

		Returns:
			dict(arg1:number,arg2:str)
		"""
		return self._get_attribute('experimenterField')
	@ExperimenterField.setter
	def ExperimenterField(self, value):
		self._set_attribute('experimenterField', value)

	@property
	def ExperimenterHashmask(self):
		"""This describes the experimenter hash mask value.

		Returns:
			dict(arg1:bool,arg2:str)
		"""
		return self._get_attribute('experimenterHashmask')
	@ExperimenterHashmask.setter
	def ExperimenterHashmask(self, value):
		self._set_attribute('experimenterHashmask', value)

	@property
	def ExperimenterId(self):
		"""This describes the unique identifier for the Experimenter.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('experimenterId')
	@ExperimenterId.setter
	def ExperimenterId(self, value):
		self._set_attribute('experimenterId', value)

	@property
	def Icmpv4Code(self):
		"""This describes the ICMP code.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv4Code')
	@Icmpv4Code.setter
	def Icmpv4Code(self, value):
		self._set_attribute('icmpv4Code', value)

	@property
	def Icmpv4Type(self):
		"""This describes the ICMP type.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv4Type')
	@Icmpv4Type.setter
	def Icmpv4Type(self, value):
		self._set_attribute('icmpv4Type', value)

	@property
	def Icmpv6Code(self):
		"""This describes the ICMPv6 code.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""This describes the ICMPv6 type.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def InPort(self):
		"""This describes the input port used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""This describes the IP DSCP value for advertising.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""This describes the ECN bits of the IP header.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""This describes the IP Protocol used.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""This describes the IPv4 Destination address for the port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""This describes the IPv4 source address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv6Destination(self):
		"""This describes the IPv6 destination address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6Destination')
	@Ipv6Destination.setter
	def Ipv6Destination(self, value):
		self._set_attribute('ipv6Destination', value)

	@property
	def Ipv6ExtHeader(self):
		"""This describes the IPv6 Extension Header pseudo-field.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6FlowLabel(self):
		"""This describes the IPv6 Flow label.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NdDll(self):
		"""This describes the target link-layer address option in an IPv6 Neighbor Discovery message.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6NdDll')
	@Ipv6NdDll.setter
	def Ipv6NdDll(self, value):
		self._set_attribute('ipv6NdDll', value)

	@property
	def Ipv6NdSll(self):
		"""This describes the source link-layer address option in an IPv6 Neighbor Discovery message.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6NdSll')
	@Ipv6NdSll.setter
	def Ipv6NdSll(self, value):
		self._set_attribute('ipv6NdSll', value)

	@property
	def Ipv6NdTarget(self):
		"""This describes the target address in an IPv6 Neighbor Discovery message.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6NdTarget')
	@Ipv6NdTarget.setter
	def Ipv6NdTarget(self, value):
		self._set_attribute('ipv6NdTarget', value)

	@property
	def Ipv6Source(self):
		"""This describes the IPv6 source address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('ipv6Source')
	@Ipv6Source.setter
	def Ipv6Source(self, value):
		self._set_attribute('ipv6Source', value)

	@property
	def MetaData(self):
		"""This describes the table metadata value used to pass information between tables.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('metaData')
	@MetaData.setter
	def MetaData(self, value):
		self._set_attribute('metaData', value)

	@property
	def MplsBos(self):
		"""This describes the BoS bit in the first MPLS shim header.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""This describes the LABEL in the first MPLS shim header.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""This describes the TC in the first MPLS shim header.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def PbbIsid(self):
		"""This describes the I-SID in the first PBB service instance tag.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('pbbIsid')
	@PbbIsid.setter
	def PbbIsid(self, value):
		self._set_attribute('pbbIsid', value)

	@property
	def PhysicalInPort(self):
		"""This describes the physical In port value for this flow range. It is the underlying physical port when packet is received on a logical port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('physicalInPort')
	@PhysicalInPort.setter
	def PhysicalInPort(self, value):
		self._set_attribute('physicalInPort', value)

	@property
	def SctpDestination(self):
		"""This describes the SCTP target port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""This describes the SCTP source port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def TcpDestination(self):
		"""This describes the TCP destination address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""This describes the TCP source address.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('tcpSource')
	@TcpSource.setter
	def TcpSource(self, value):
		self._set_attribute('tcpSource', value)

	@property
	def TunnelId(self):
		"""This describes the unique identifier used for the Tunnel.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('tunnelId')
	@TunnelId.setter
	def TunnelId(self, value):
		self._set_attribute('tunnelId', value)

	@property
	def UdpDestination(self):
		"""This describes the UDP destination port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""This describes the UDP source port.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""This describes the unique VLAN Identifier.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""This describes the User Priority for this VLAN.

		Returns:
			dict(arg1:str,arg2:str)
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
