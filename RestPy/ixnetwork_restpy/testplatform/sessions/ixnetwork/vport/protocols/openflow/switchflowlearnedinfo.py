from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchFlowLearnedInfo(Base):
	"""The SwitchFlowLearnedInfo class encapsulates a system managed switchFlowLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchFlowLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchFlowLearnedInfo'

	def __init__(self, parent):
		super(SwitchFlowLearnedInfo, self).__init__(parent)

	@property
	def SwitchActionLearnedInfo(self):
		"""An instance of the SwitchActionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchactionlearnedinfo.SwitchActionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchactionlearnedinfo import SwitchActionLearnedInfo
		return SwitchActionLearnedInfo(self)

	@property
	def SwitchFlowInstructionLearnedInfo(self):
		"""An instance of the SwitchFlowInstructionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflowinstructionlearnedinfo.SwitchFlowInstructionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchflowinstructionlearnedinfo import SwitchFlowInstructionLearnedInfo
		return SwitchFlowInstructionLearnedInfo(self)

	@property
	def ActiveNanoSeconds(self):
		"""This describes the duration (in ns) for which the flow entry is active.

		Returns:
			number
		"""
		return self._get_attribute('activeNanoSeconds')

	@property
	def ActiveSeconds(self):
		"""This describes the duration (in sec) for which the flow entry is active.

		Returns:
			number
		"""
		return self._get_attribute('activeSeconds')

	@property
	def ArpDstHwAddress(self):
		"""This describes the target hardware address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddress')

	@property
	def ArpDstHwAddressMask(self):
		"""This describes the mask value of the target hardware address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddressMask')

	@property
	def ArpDstIpv4Address(self):
		"""This describes the target IPv4 address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4Address')

	@property
	def ArpDstIpv4AddressMask(self):
		"""This describes the mask value of the target IPv4 address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4AddressMask')

	@property
	def ArpOpcode(self):
		"""This describes the ARP opcode.

		Returns:
			str
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
	def ArpSrcHwAddressMask(self):
		"""This describes the mask value of the source hardware address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddressMask')

	@property
	def ArpSrcIpv4Address(self):
		"""This describes the source IPv4 address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4Address')

	@property
	def ArpSrcIpv4AddressMask(self):
		"""This describes the mask value of the source IPv4 address in the ARP payload.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4AddressMask')

	@property
	def BytesCount(self):
		"""This describes the number of bytes in flow.

		Returns:
			str
		"""
		return self._get_attribute('bytesCount')

	@property
	def Cookie(self):
		"""This describes the opaque controller-issued identifier.

		Returns:
			str
		"""
		return self._get_attribute('cookie')

	@property
	def CookieMask(self):
		"""This describes the mask used to restrict the cookie bits.

		Returns:
			str
		"""
		return self._get_attribute('cookieMask')

	@property
	def DataPathId(self):
		"""This describes the datapath ID of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""This describes the datapath ID, in hexadecimal format, of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def EthernetDestination(self):
		"""This describes the ethernet destination address of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetDestinationMask(self):
		"""This describes the Ethernet destination mask value.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestinationMask')

	@property
	def EthernetSource(self):
		"""This describes the ethernet source address of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def EthernetSourceMask(self):
		"""This describes the Ethernet Source mask value.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSourceMask')

	@property
	def EthernetType(self):
		"""This describes the Ethernet type of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def ExperimenterData(self):
		"""This describes the data of the Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""This describes the data length of the Experimenter.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def ExperimenterField(self):
		"""This describes the field type for experimenter match.

		Returns:
			number
		"""
		return self._get_attribute('experimenterField')

	@property
	def ExperimenterHashMask(self):
		"""This describes the experimenter hash mask value.

		Returns:
			bool
		"""
		return self._get_attribute('experimenterHashMask')

	@property
	def ExperimenterId(self):
		"""This describes the unique identifier for the Experimenter.

		Returns:
			str
		"""
		return self._get_attribute('experimenterId')

	@property
	def Flags(self):
		"""This describes the flags used for this configuration.

		Returns:
			number
		"""
		return self._get_attribute('flags')

	@property
	def HardTimeout(self):
		"""This describes the duration (in sec) before expiration.

		Returns:
			number
		"""
		return self._get_attribute('hardTimeout')

	@property
	def Icmpv4Code(self):
		"""This describes the ICMP code.

		Returns:
			str
		"""
		return self._get_attribute('icmpv4Code')

	@property
	def Icmpv4Type(self):
		"""This describes the ICMP type.

		Returns:
			str
		"""
		return self._get_attribute('icmpv4Type')

	@property
	def Icmpv6Code(self):
		"""This describes the ICMPv6 code.

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Code')

	@property
	def Icmpv6Type(self):
		"""This describes the ICMPv6 type.

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Type')

	@property
	def IdleTimeout(self):
		"""This describes the duration (in sec) for which the switch is idle before expiration.

		Returns:
			number
		"""
		return self._get_attribute('idleTimeout')

	@property
	def InPort(self):
		"""This describes the input port of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('inPort')

	@property
	def IpDscp(self):
		"""This describes the IP ToS of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def IpEcn(self):
		"""This describes the ECN bits of the IP header.

		Returns:
			str
		"""
		return self._get_attribute('ipEcn')

	@property
	def IpProtocol(self):
		"""This describes the IP Protocol type of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ipProtocol')

	@property
	def Ipv4Destination(self):
		"""This describes the IPv4 destination of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""This describes the IPv4 source address of the flow match.

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
	def Ipv6DestinationMask(self):
		"""This describes the mask value of IPv6 destination address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6DestinationMask')

	@property
	def Ipv6ExtHeader(self):
		"""The IPv6 Extension Header pseudo-field.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6ExtHeaderMask(self):
		"""This describes the mask value of the IPv6 Extension Header.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeaderMask')

	@property
	def Ipv6FlowLabel(self):
		"""This describes the IPv6 Flow label.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6FlowLabelMask(self):
		"""This describes the mask value of IPv6 Flow label.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabelMask')

	@property
	def Ipv6NdDll(self):
		"""The target link-layer address option in an IPv6 Neighbor Discovery message.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdDll')

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
	def Ipv6Source(self):
		"""This describes the IPv6 source address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')

	@property
	def Ipv6SourceMask(self):
		"""This describes the mask value of IPv6 source address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6SourceMask')

	@property
	def LocalIp(self):
		"""This describes the local IP address of the switch.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def Metadata(self):
		"""This describes the table metadata value used to pass information between tables.

		Returns:
			str
		"""
		return self._get_attribute('metadata')

	@property
	def MetadataMask(self):
		"""This describes the metadata bitmask value.

		Returns:
			str
		"""
		return self._get_attribute('metadataMask')

	@property
	def MplsBos(self):
		"""This describes the BoS bit in the first MPLS shim header.

		Returns:
			str
		"""
		return self._get_attribute('mplsBos')

	@property
	def MplsLabel(self):
		"""This describes the LABEL in the first MPLS shim header.

		Returns:
			str
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsTc(self):
		"""This describes the TC in the first MPLS shim header.

		Returns:
			str
		"""
		return self._get_attribute('mplsTc')

	@property
	def NegotiatedVersion(self):
		"""This describes the OpenFlow version supported by this configuration.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfInstructions(self):
		"""This describes the number of instructions for this Flow range. The default value is 0. The minimum value is 0 and the maximum value is 10.

		Returns:
			str
		"""
		return self._get_attribute('numberOfInstructions')

	@property
	def NumberofActions(self):
		"""This describes the number of actions associated with the flow entry.

		Returns:
			str
		"""
		return self._get_attribute('numberofActions')

	@property
	def OutGroup(self):
		"""This describes the out group value. It requires matching entries to include this as an output group.

		Returns:
			number
		"""
		return self._get_attribute('outGroup')

	@property
	def OutPort(self):
		"""This describes the out port value. It requires matching entries to include this as an output port.

		Returns:
			number
		"""
		return self._get_attribute('outPort')

	@property
	def PacketsCount(self):
		"""This describes the number of packets in flow.

		Returns:
			str
		"""
		return self._get_attribute('packetsCount')

	@property
	def PbbIsid(self):
		"""This describes the I-SID in the first PBB service instance tag.

		Returns:
			str
		"""
		return self._get_attribute('pbbIsid')

	@property
	def PbbIsidMask(self):
		"""This describes the mask value of PBB I-SID.

		Returns:
			str
		"""
		return self._get_attribute('pbbIsidMask')

	@property
	def PhysicalInPort(self):
		"""This describes the physical In port value for this flow range. It is the underlying physical port when packet is received on a logical port.

		Returns:
			str
		"""
		return self._get_attribute('physicalInPort')

	@property
	def Priority(self):
		"""This describes the Priority of the flow entry.

		Returns:
			number
		"""
		return self._get_attribute('priority')

	@property
	def RemoteIp(self):
		"""This describes the IP address of the remote end of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def SctpDestination(self):
		"""This describes the SCTP target port.

		Returns:
			str
		"""
		return self._get_attribute('sctpDestination')

	@property
	def SctpSource(self):
		"""This describes the SCTP source port.

		Returns:
			str
		"""
		return self._get_attribute('sctpSource')

	@property
	def TableId(self):
		"""This describes the ID of the table in which the entry is stored.

		Returns:
			str
		"""
		return self._get_attribute('tableId')

	@property
	def TcpDestination(self):
		"""This describes the TCP destination port.

		Returns:
			str
		"""
		return self._get_attribute('tcpDestination')

	@property
	def TcpSource(self):
		"""This describes the TCP source port.

		Returns:
			str
		"""
		return self._get_attribute('tcpSource')

	@property
	def TransportDestination(self):
		"""This describes the transport destination port of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('transportDestination')

	@property
	def TransportSource(self):
		"""This describes the transport source port of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('transportSource')

	@property
	def TunnelId(self):
		"""This describes the unique identifier used for the Tunnel.

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')

	@property
	def TunnelIdMask(self):
		"""This describes the Tunnel ID mask value.

		Returns:
			str
		"""
		return self._get_attribute('tunnelIdMask')

	@property
	def UdpDestination(self):
		"""This describes the UDP destination port.

		Returns:
			str
		"""
		return self._get_attribute('udpDestination')

	@property
	def UdpSource(self):
		"""This describes the UDP source port.

		Returns:
			str
		"""
		return self._get_attribute('udpSource')

	@property
	def VlanId(self):
		"""This describes the VLAN ID of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanMask(self):
		"""This describes the VLAN mask value.

		Returns:
			number
		"""
		return self._get_attribute('vlanMask')

	@property
	def VlanPriority(self):
		"""This describes the VLAN Priority of the flow match.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ActiveNanoSeconds=None, ActiveSeconds=None, ArpDstHwAddress=None, ArpDstHwAddressMask=None, ArpDstIpv4Address=None, ArpDstIpv4AddressMask=None, ArpOpcode=None, ArpSrcHwAddress=None, ArpSrcHwAddressMask=None, ArpSrcIpv4Address=None, ArpSrcIpv4AddressMask=None, BytesCount=None, Cookie=None, CookieMask=None, DataPathId=None, DataPathIdAsHex=None, EthernetDestination=None, EthernetDestinationMask=None, EthernetSource=None, EthernetSourceMask=None, EthernetType=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterField=None, ExperimenterHashMask=None, ExperimenterId=None, Flags=None, HardTimeout=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IdleTimeout=None, InPort=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6DestinationMask=None, Ipv6ExtHeader=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabel=None, Ipv6FlowLabelMask=None, Ipv6NdDll=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6Source=None, Ipv6SourceMask=None, LocalIp=None, Metadata=None, MetadataMask=None, MplsBos=None, MplsLabel=None, MplsTc=None, NegotiatedVersion=None, NumberOfInstructions=None, NumberofActions=None, OutGroup=None, OutPort=None, PacketsCount=None, PbbIsid=None, PbbIsidMask=None, PhysicalInPort=None, Priority=None, RemoteIp=None, SctpDestination=None, SctpSource=None, TableId=None, TcpDestination=None, TcpSource=None, TransportDestination=None, TransportSource=None, TunnelId=None, TunnelIdMask=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanMask=None, VlanPriority=None):
		"""Finds and retrieves switchFlowLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchFlowLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchFlowLearnedInfo data from the server.

		Args:
			ActiveNanoSeconds (number): This describes the duration (in ns) for which the flow entry is active.
			ActiveSeconds (number): This describes the duration (in sec) for which the flow entry is active.
			ArpDstHwAddress (str): This describes the target hardware address in the ARP payload.
			ArpDstHwAddressMask (str): This describes the mask value of the target hardware address in the ARP payload.
			ArpDstIpv4Address (str): This describes the target IPv4 address in the ARP payload.
			ArpDstIpv4AddressMask (str): This describes the mask value of the target IPv4 address in the ARP payload.
			ArpOpcode (str): This describes the ARP opcode.
			ArpSrcHwAddress (str): This describes the source hardware address in the ARP payload.
			ArpSrcHwAddressMask (str): This describes the mask value of the source hardware address in the ARP payload.
			ArpSrcIpv4Address (str): This describes the source IPv4 address in the ARP payload.
			ArpSrcIpv4AddressMask (str): This describes the mask value of the source IPv4 address in the ARP payload.
			BytesCount (str): This describes the number of bytes in flow.
			Cookie (str): This describes the opaque controller-issued identifier.
			CookieMask (str): This describes the mask used to restrict the cookie bits.
			DataPathId (str): This describes the datapath ID of the switch.
			DataPathIdAsHex (str): This describes the datapath ID, in hexadecimal format, of the switch.
			EthernetDestination (str): This describes the ethernet destination address of the flow match.
			EthernetDestinationMask (str): This describes the Ethernet destination mask value.
			EthernetSource (str): This describes the ethernet source address of the flow match.
			EthernetSourceMask (str): This describes the Ethernet Source mask value.
			EthernetType (str): This describes the Ethernet type of the flow match.
			ExperimenterData (str): This describes the data of the Experimenter.
			ExperimenterDataLength (number): This describes the data length of the Experimenter.
			ExperimenterField (number): This describes the field type for experimenter match.
			ExperimenterHashMask (bool): This describes the experimenter hash mask value.
			ExperimenterId (str): This describes the unique identifier for the Experimenter.
			Flags (number): This describes the flags used for this configuration.
			HardTimeout (number): This describes the duration (in sec) before expiration.
			Icmpv4Code (str): This describes the ICMP code.
			Icmpv4Type (str): This describes the ICMP type.
			Icmpv6Code (str): This describes the ICMPv6 code.
			Icmpv6Type (str): This describes the ICMPv6 type.
			IdleTimeout (number): This describes the duration (in sec) for which the switch is idle before expiration.
			InPort (str): This describes the input port of the flow match.
			IpDscp (str): This describes the IP ToS of the flow match.
			IpEcn (str): This describes the ECN bits of the IP header.
			IpProtocol (str): This describes the IP Protocol type of the flow match.
			Ipv4Destination (str): This describes the IPv4 destination of the flow match.
			Ipv4Source (str): This describes the IPv4 source address of the flow match.
			Ipv6Destination (str): This describes the IPv6 destination address.
			Ipv6DestinationMask (str): This describes the mask value of IPv6 destination address.
			Ipv6ExtHeader (number): The IPv6 Extension Header pseudo-field.
			Ipv6ExtHeaderMask (number): This describes the mask value of the IPv6 Extension Header.
			Ipv6FlowLabel (str): This describes the IPv6 Flow label.
			Ipv6FlowLabelMask (str): This describes the mask value of IPv6 Flow label.
			Ipv6NdDll (str): The target link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6NdSll (str): This describes the source link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6NdTarget (str): This describes the target address in an IPv6 Neighbor Discovery message.
			Ipv6Source (str): This describes the IPv6 source address.
			Ipv6SourceMask (str): This describes the mask value of IPv6 source address.
			LocalIp (str): This describes the local IP address of the switch.
			Metadata (str): This describes the table metadata value used to pass information between tables.
			MetadataMask (str): This describes the metadata bitmask value.
			MplsBos (str): This describes the BoS bit in the first MPLS shim header.
			MplsLabel (str): This describes the LABEL in the first MPLS shim header.
			MplsTc (str): This describes the TC in the first MPLS shim header.
			NegotiatedVersion (str): This describes the OpenFlow version supported by this configuration.
			NumberOfInstructions (str): This describes the number of instructions for this Flow range. The default value is 0. The minimum value is 0 and the maximum value is 10.
			NumberofActions (str): This describes the number of actions associated with the flow entry.
			OutGroup (number): This describes the out group value. It requires matching entries to include this as an output group.
			OutPort (number): This describes the out port value. It requires matching entries to include this as an output port.
			PacketsCount (str): This describes the number of packets in flow.
			PbbIsid (str): This describes the I-SID in the first PBB service instance tag.
			PbbIsidMask (str): This describes the mask value of PBB I-SID.
			PhysicalInPort (str): This describes the physical In port value for this flow range. It is the underlying physical port when packet is received on a logical port.
			Priority (number): This describes the Priority of the flow entry.
			RemoteIp (str): This describes the IP address of the remote end of the OF Channel.
			SctpDestination (str): This describes the SCTP target port.
			SctpSource (str): This describes the SCTP source port.
			TableId (str): This describes the ID of the table in which the entry is stored.
			TcpDestination (str): This describes the TCP destination port.
			TcpSource (str): This describes the TCP source port.
			TransportDestination (str): This describes the transport destination port of the flow match.
			TransportSource (str): This describes the transport source port of the flow match.
			TunnelId (str): This describes the unique identifier used for the Tunnel.
			TunnelIdMask (str): This describes the Tunnel ID mask value.
			UdpDestination (str): This describes the UDP destination port.
			UdpSource (str): This describes the UDP source port.
			VlanId (str): This describes the VLAN ID of the flow match.
			VlanMask (number): This describes the VLAN mask value.
			VlanPriority (str): This describes the VLAN Priority of the flow match.

		Returns:
			self: This instance with matching switchFlowLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchFlowLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchFlowLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
