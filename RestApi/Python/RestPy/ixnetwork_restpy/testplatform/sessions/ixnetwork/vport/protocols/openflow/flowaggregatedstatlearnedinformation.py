from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowAggregatedStatLearnedInformation(Base):
	"""The FlowAggregatedStatLearnedInformation class encapsulates a system managed flowAggregatedStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowAggregatedStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'flowAggregatedStatLearnedInformation'

	def __init__(self, parent):
		super(FlowAggregatedStatLearnedInformation, self).__init__(parent)

	@property
	def ArpDstHwAddr(self):
		"""Value of the ARP destination hardware address.

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddr')

	@property
	def ArpDstHwAddressMask(self):
		"""Value of the ARP destination hardware address mask field.

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddressMask')

	@property
	def ArpDstIpv4Address(self):
		"""Value of the ARP destination IPv4 address field.

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4Address')

	@property
	def ArpDstIpv4AddressMask(self):
		"""Value of the ARP destination IPv4 address mask field.

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4AddressMask')

	@property
	def ArpOpcode(self):
		"""Value of the ARP opcode field.

		Returns:
			str
		"""
		return self._get_attribute('arpOpcode')

	@property
	def ArpSrcHwAddr(self):
		"""Value of the ARP source hardware address.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddr')

	@property
	def ArpSrcHwAddressMask(self):
		"""Value of the ARP source hardware address mask field value

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddressMask')

	@property
	def ArpSrcIpv4Address(self):
		"""Value of the ARP source IPv4 address field.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4Address')

	@property
	def ArpSrcIpv4AddressMask(self):
		"""Value of the ARP source IPv4 address mask field

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4AddressMask')

	@property
	def BytesCount(self):
		"""Signifies the count of bytes.

		Returns:
			str
		"""
		return self._get_attribute('bytesCount')

	@property
	def Cookie(self):
		"""The Cookie field value.

		Returns:
			str
		"""
		return self._get_attribute('cookie')

	@property
	def CookieMask(self):
		"""Value of the cookie mask field.

		Returns:
			str
		"""
		return self._get_attribute('cookieMask')

	@property
	def DataPathId(self):
		"""Signifies the datapath ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Signifies the datapath ID of the OpenFlow switch in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def ErrorCode(self):
		"""Signifies the error code of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""Signifies the type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def EthernetDestination(self):
		"""Signifies the destination address of the Ethernet port.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetDestinationMask(self):
		"""The ethernet destination mask field.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestinationMask')

	@property
	def EthernetSource(self):
		"""Signifies the source address of the Ethernet port.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def EthernetSourceMask(self):
		"""Value of the ethernet source mask field.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSourceMask')

	@property
	def EthernetType(self):
		"""Signifies the type of Ethernet port used.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def ExperimenterData(self):
		"""Value of the experimenter data field.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""Value of the Experimenter data length field.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def ExperimenterField(self):
		"""Value of the Experimenter Field field.

		Returns:
			number
		"""
		return self._get_attribute('experimenterField')

	@property
	def ExperimenterHashmask(self):
		"""Value of the experimenter hasmask field.

		Returns:
			bool
		"""
		return self._get_attribute('experimenterHashmask')

	@property
	def ExperimenterId(self):
		"""Value of the experimenter ID field.

		Returns:
			str
		"""
		return self._get_attribute('experimenterId')

	@property
	def FlowsCount(self):
		"""Signifies the flow count value.

		Returns:
			number
		"""
		return self._get_attribute('flowsCount')

	@property
	def Icmpv6Code(self):
		"""Value of the ICMPv6 code field.

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Code')

	@property
	def Icmpv6Type(self):
		"""Value of the ICMPv6 type field.

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Type')

	@property
	def InPort(self):
		"""Signifies the input port used.

		Returns:
			str
		"""
		return self._get_attribute('inPort')

	@property
	def IpDscp(self):
		"""Signifies the IP DSCP value for advertising.

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def IpEcn(self):
		"""Value of the IP ECN field.

		Returns:
			str
		"""
		return self._get_attribute('ipEcn')

	@property
	def IpProtocol(self):
		"""Signifies the IP Protocol used.

		Returns:
			str
		"""
		return self._get_attribute('ipProtocol')

	@property
	def Ipv4Destination(self):
		"""Signifie the IPv4 Destination address for the port.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""Signifies the IPv4 Source address for the port.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')

	@property
	def Ipv6Destination(self):
		"""Value of the IPv6 destination field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Destination')

	@property
	def Ipv6DestinationMask(self):
		"""Value of the IPv6 destination mask field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6DestinationMask')

	@property
	def Ipv6ExtHeader(self):
		"""The Ipv6 extension header field value.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6ExtHeaderMask(self):
		"""Velue of ipv6 Extended header mask field.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeaderMask')

	@property
	def Ipv6FlowLabel(self):
		"""Value of the IPv6 flow label field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6FlowLabelMask(self):
		"""Value of the IPv6 flow label mask field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabelMask')

	@property
	def Ipv6NdDll(self):
		"""The IPv6 ND DLL field value.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdDll')

	@property
	def Ipv6NdSll(self):
		"""The IPv6 ND SLL field value.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')

	@property
	def Ipv6NdTarget(self):
		"""The IPv6 ND target field value.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTarget')

	@property
	def Ipv6Source(self):
		"""Value of the IPv6 source field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')

	@property
	def Ipv6SourceMask(self):
		"""Value of the IPv6 source mask field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6SourceMask')

	@property
	def Latency(self):
		"""Signifies the latency measurement for the OpenFlow channel in microseconds.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""The local interface IP address through which the OpenFlow session is connected.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def Metadata(self):
		"""Value of the metadata field.

		Returns:
			str
		"""
		return self._get_attribute('metadata')

	@property
	def MetadataMask(self):
		"""Metadata mask value.

		Returns:
			str
		"""
		return self._get_attribute('metadataMask')

	@property
	def MplsBos(self):
		"""Value of the MPLS BoS field.

		Returns:
			str
		"""
		return self._get_attribute('mplsBos')

	@property
	def MplsLabel(self):
		"""Value of the MPLS label field.

		Returns:
			str
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsTc(self):
		"""The MPLS TC field value.

		Returns:
			str
		"""
		return self._get_attribute('mplsTc')

	@property
	def NegotiatedVersion(self):
		"""The OpenFlow version supported by this configuration.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def OutGroup(self):
		"""Value of the out group field.

		Returns:
			number
		"""
		return self._get_attribute('outGroup')

	@property
	def OutPort(self):
		"""Value of the out port field.

		Returns:
			number
		"""
		return self._get_attribute('outPort')

	@property
	def PacketsCount(self):
		"""Signifies the count of packets transmitted.

		Returns:
			str
		"""
		return self._get_attribute('packetsCount')

	@property
	def PbbISid(self):
		"""Value of the PBB I-SID field.

		Returns:
			str
		"""
		return self._get_attribute('pbbISid')

	@property
	def PbbISidMask(self):
		"""Value of the PBB I-SID mask field.

		Returns:
			str
		"""
		return self._get_attribute('pbbISidMask')

	@property
	def PhysicalInPort(self):
		"""Value of the Physical IN port field.

		Returns:
			str
		"""
		return self._get_attribute('physicalInPort')

	@property
	def RemoteIp(self):
		"""Signifies the Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""Signifies the reply state of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def SctpDestination(self):
		"""The SCTP destination field value.

		Returns:
			str
		"""
		return self._get_attribute('sctpDestination')

	@property
	def SctpSource(self):
		"""Value of the SCTP source field.

		Returns:
			str
		"""
		return self._get_attribute('sctpSource')

	@property
	def TableId(self):
		"""Signifies the identifier value for the table.

		Returns:
			str
		"""
		return self._get_attribute('tableId')

	@property
	def TcpDestination(self):
		"""The Transport destination address.

		Returns:
			str
		"""
		return self._get_attribute('tcpDestination')

	@property
	def TcpSource(self):
		"""Value of the TCP source field.

		Returns:
			str
		"""
		return self._get_attribute('tcpSource')

	@property
	def TransportDestinationIcmpCode(self):
		"""Signifies the Transport destination address.

		Returns:
			str
		"""
		return self._get_attribute('transportDestinationIcmpCode')

	@property
	def TransportSourceIcmpType(self):
		"""Signifies the Transport source address.

		Returns:
			str
		"""
		return self._get_attribute('transportSourceIcmpType')

	@property
	def TunnelId(self):
		"""Value of the tunnel ID field.

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')

	@property
	def TunnelIdMask(self):
		"""Value of the tunnel ID mask field.

		Returns:
			str
		"""
		return self._get_attribute('tunnelIdMask')

	@property
	def UdpDestination(self):
		"""Value of the UDP destination field.

		Returns:
			str
		"""
		return self._get_attribute('udpDestination')

	@property
	def UdpSource(self):
		"""Value of the UDP source field.

		Returns:
			str
		"""
		return self._get_attribute('udpSource')

	@property
	def VlanId(self):
		"""Signifies the unique VLAN Identifier.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanMask(self):
		"""Value of the VLAN mask field.

		Returns:
			number
		"""
		return self._get_attribute('vlanMask')

	@property
	def VlanPriority(self):
		"""Signifies the User Priority for this VLAN.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ArpDstHwAddr=None, ArpDstHwAddressMask=None, ArpDstIpv4Address=None, ArpDstIpv4AddressMask=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcHwAddressMask=None, ArpSrcIpv4Address=None, ArpSrcIpv4AddressMask=None, BytesCount=None, Cookie=None, CookieMask=None, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, EthernetDestination=None, EthernetDestinationMask=None, EthernetSource=None, EthernetSourceMask=None, EthernetType=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterField=None, ExperimenterHashmask=None, ExperimenterId=None, FlowsCount=None, Icmpv6Code=None, Icmpv6Type=None, InPort=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6DestinationMask=None, Ipv6ExtHeader=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabel=None, Ipv6FlowLabelMask=None, Ipv6NdDll=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6Source=None, Ipv6SourceMask=None, Latency=None, LocalIp=None, Metadata=None, MetadataMask=None, MplsBos=None, MplsLabel=None, MplsTc=None, NegotiatedVersion=None, OutGroup=None, OutPort=None, PacketsCount=None, PbbISid=None, PbbISidMask=None, PhysicalInPort=None, RemoteIp=None, ReplyState=None, SctpDestination=None, SctpSource=None, TableId=None, TcpDestination=None, TcpSource=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, TunnelId=None, TunnelIdMask=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanMask=None, VlanPriority=None):
		"""Finds and retrieves flowAggregatedStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve flowAggregatedStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all flowAggregatedStatLearnedInformation data from the server.

		Args:
			ArpDstHwAddr (str): Value of the ARP destination hardware address.
			ArpDstHwAddressMask (str): Value of the ARP destination hardware address mask field.
			ArpDstIpv4Address (str): Value of the ARP destination IPv4 address field.
			ArpDstIpv4AddressMask (str): Value of the ARP destination IPv4 address mask field.
			ArpOpcode (str): Value of the ARP opcode field.
			ArpSrcHwAddr (str): Value of the ARP source hardware address.
			ArpSrcHwAddressMask (str): Value of the ARP source hardware address mask field value
			ArpSrcIpv4Address (str): Value of the ARP source IPv4 address field.
			ArpSrcIpv4AddressMask (str): Value of the ARP source IPv4 address mask field
			BytesCount (str): Signifies the count of bytes.
			Cookie (str): The Cookie field value.
			CookieMask (str): Value of the cookie mask field.
			DataPathId (str): Signifies the datapath ID of the OpenFlow switch.
			DataPathIdAsHex (str): Signifies the datapath ID of the OpenFlow switch in hexadecimal format.
			ErrorCode (str): Signifies the error code of the error received.
			ErrorType (str): Signifies the type of the error received.
			EthernetDestination (str): Signifies the destination address of the Ethernet port.
			EthernetDestinationMask (str): The ethernet destination mask field.
			EthernetSource (str): Signifies the source address of the Ethernet port.
			EthernetSourceMask (str): Value of the ethernet source mask field.
			EthernetType (str): Signifies the type of Ethernet port used.
			ExperimenterData (str): Value of the experimenter data field.
			ExperimenterDataLength (number): Value of the Experimenter data length field.
			ExperimenterField (number): Value of the Experimenter Field field.
			ExperimenterHashmask (bool): Value of the experimenter hasmask field.
			ExperimenterId (str): Value of the experimenter ID field.
			FlowsCount (number): Signifies the flow count value.
			Icmpv6Code (str): Value of the ICMPv6 code field.
			Icmpv6Type (str): Value of the ICMPv6 type field.
			InPort (str): Signifies the input port used.
			IpDscp (str): Signifies the IP DSCP value for advertising.
			IpEcn (str): Value of the IP ECN field.
			IpProtocol (str): Signifies the IP Protocol used.
			Ipv4Destination (str): Signifie the IPv4 Destination address for the port.
			Ipv4Source (str): Signifies the IPv4 Source address for the port.
			Ipv6Destination (str): Value of the IPv6 destination field.
			Ipv6DestinationMask (str): Value of the IPv6 destination mask field.
			Ipv6ExtHeader (number): The Ipv6 extension header field value.
			Ipv6ExtHeaderMask (number): Velue of ipv6 Extended header mask field.
			Ipv6FlowLabel (str): Value of the IPv6 flow label field.
			Ipv6FlowLabelMask (str): Value of the IPv6 flow label mask field.
			Ipv6NdDll (str): The IPv6 ND DLL field value.
			Ipv6NdSll (str): The IPv6 ND SLL field value.
			Ipv6NdTarget (str): The IPv6 ND target field value.
			Ipv6Source (str): Value of the IPv6 source field.
			Ipv6SourceMask (str): Value of the IPv6 source mask field.
			Latency (number): Signifies the latency measurement for the OpenFlow channel in microseconds.
			LocalIp (str): The local interface IP address through which the OpenFlow session is connected.
			Metadata (str): Value of the metadata field.
			MetadataMask (str): Metadata mask value.
			MplsBos (str): Value of the MPLS BoS field.
			MplsLabel (str): Value of the MPLS label field.
			MplsTc (str): The MPLS TC field value.
			NegotiatedVersion (str): The OpenFlow version supported by this configuration.
			OutGroup (number): Value of the out group field.
			OutPort (number): Value of the out port field.
			PacketsCount (str): Signifies the count of packets transmitted.
			PbbISid (str): Value of the PBB I-SID field.
			PbbISidMask (str): Value of the PBB I-SID mask field.
			PhysicalInPort (str): Value of the Physical IN port field.
			RemoteIp (str): Signifies the Remote IP address of the selected interface.
			ReplyState (str): Signifies the reply state of the OF Channel.
			SctpDestination (str): The SCTP destination field value.
			SctpSource (str): Value of the SCTP source field.
			TableId (str): Signifies the identifier value for the table.
			TcpDestination (str): The Transport destination address.
			TcpSource (str): Value of the TCP source field.
			TransportDestinationIcmpCode (str): Signifies the Transport destination address.
			TransportSourceIcmpType (str): Signifies the Transport source address.
			TunnelId (str): Value of the tunnel ID field.
			TunnelIdMask (str): Value of the tunnel ID mask field.
			UdpDestination (str): Value of the UDP destination field.
			UdpSource (str): Value of the UDP source field.
			VlanId (str): Signifies the unique VLAN Identifier.
			VlanMask (number): Value of the VLAN mask field.
			VlanPriority (str): Signifies the User Priority for this VLAN.

		Returns:
			self: This instance with matching flowAggregatedStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowAggregatedStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowAggregatedStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
