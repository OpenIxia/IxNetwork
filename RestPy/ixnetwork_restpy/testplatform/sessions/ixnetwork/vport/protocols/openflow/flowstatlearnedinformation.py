from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowStatLearnedInformation(Base):
	"""The FlowStatLearnedInformation class encapsulates a system managed flowStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'flowStatLearnedInformation'

	def __init__(self, parent):
		super(FlowStatLearnedInformation, self).__init__(parent)

	@property
	def ActiveNanoSeconds(self):
		"""Signifies the active time in nano seconds for the session.

		Returns:
			number
		"""
		return self._get_attribute('activeNanoSeconds')

	@property
	def ActiveSeconds(self):
		"""Signifies the number of active seconds for the session.

		Returns:
			number
		"""
		return self._get_attribute('activeSeconds')

	@property
	def ApplyActionsInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('applyActionsInstruction')

	@property
	def ApplyMeterInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('applyMeterInstruction')

	@property
	def ArpDstHwAddr(self):
		"""The hardware address of the ARP destination.

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
		"""Value of the ARP destination IPv4 address mask field value.

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
		"""The hardware address of the ARP source.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddr')

	@property
	def ArpSrcHwAddressMask(self):
		"""Value of the ARP source hardware address mask field.

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
		"""Value of the ARP source IPv4 address mask field.

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
	def ClearActionsInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('clearActionsInstruction')

	@property
	def Cookie(self):
		"""Signifies the cookie value.

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
		"""The data path identification of the switch, in decimal format.

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
		"""The OpenFlow error code, if any error is received in reply to the statistics request.

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
		"""Value of the ethernet destination mask field.

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
		"""Value of the Experimenter field.

		Returns:
			number
		"""
		return self._get_attribute('experimenterField')

	@property
	def ExperimenterHashmask(self):
		"""Value of the experimenter hashmask field.

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
	def ExperimenterInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('experimenterInstruction')

	@property
	def Flags(self):
		"""Specifies Flags configured.

		Returns:
			str
		"""
		return self._get_attribute('flags')

	@property
	def GoToTableInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('goToTableInstruction')

	@property
	def HardTimeout(self):
		"""Signifies the inactive time in seconds after which the Flow range will hard timeout and close.

		Returns:
			number
		"""
		return self._get_attribute('hardTimeout')

	@property
	def Icmpv4Code(self):
		"""The code of ICMPv4 port used.

		Returns:
			str
		"""
		return self._get_attribute('icmpv4Code')

	@property
	def Icmpv4Type(self):
		"""Value of the ICMPv4 type field.

		Returns:
			str
		"""
		return self._get_attribute('icmpv4Type')

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
	def IdleTimeout(self):
		"""Signifies the inactive time in seconds after which the Flow range will timeout and become idle.

		Returns:
			number
		"""
		return self._get_attribute('idleTimeout')

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
		"""Signifies the IPv4 Destination address for the port.

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
		"""Value of the Ipv6 extension header field.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6ExtHeaderMask(self):
		"""Value of the IPv6 external header mask field.

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
		"""Value of the Ipv6 ND SLL field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')

	@property
	def Ipv6NdTarget(self):
		"""Value of the IPv6 ND target field.

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
		"""The latency measured in microseconds. This shows the timethat is needed to receive a reply to the statistics request sent.

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
		"""Value of the metadata mask field.

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
		"""Value of the MPLS TC field.

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
	def NoOfApplyActions(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('noOfApplyActions')

	@property
	def NoOfWriteActions(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('noOfWriteActions')

	@property
	def NumberOfActions(self):
		"""Signifies the number of actions configured for this OpenFlow channel.

		Returns:
			str
		"""
		return self._get_attribute('numberOfActions')

	@property
	def OutGroup(self):
		"""Value of the out group field.

		Returns:
			number
		"""
		return self._get_attribute('outGroup')

	@property
	def OutPort(self):
		"""Specifies Output port number.

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
	def Priority(self):
		"""Signifies the level of priority.

		Returns:
			number
		"""
		return self._get_attribute('priority')

	@property
	def RemoteIp(self):
		"""The IP address of the switch that is used to connect to controller.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""This displays the status of the statistics request. It displays the following values: Reply Received Session Not Established Empty Reply Received No Reply Received.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def SctpDestination(self):
		"""Value of the SCTP destination field.

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
		"""Value of the TCP destination field.

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

	@property
	def WriteActionsInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('writeActionsInstruction')

	@property
	def WriteMetadataInstruction(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('writeMetadataInstruction')

	def find(self, ActiveNanoSeconds=None, ActiveSeconds=None, ApplyActionsInstruction=None, ApplyMeterInstruction=None, ArpDstHwAddr=None, ArpDstHwAddressMask=None, ArpDstIpv4Address=None, ArpDstIpv4AddressMask=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcHwAddressMask=None, ArpSrcIpv4Address=None, ArpSrcIpv4AddressMask=None, BytesCount=None, ClearActionsInstruction=None, Cookie=None, CookieMask=None, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, EthernetDestination=None, EthernetDestinationMask=None, EthernetSource=None, EthernetSourceMask=None, EthernetType=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterField=None, ExperimenterHashmask=None, ExperimenterId=None, ExperimenterInstruction=None, Flags=None, GoToTableInstruction=None, HardTimeout=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IdleTimeout=None, InPort=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6DestinationMask=None, Ipv6ExtHeader=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabel=None, Ipv6FlowLabelMask=None, Ipv6NdDll=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6Source=None, Ipv6SourceMask=None, Latency=None, LocalIp=None, Metadata=None, MetadataMask=None, MplsBos=None, MplsLabel=None, MplsTc=None, NegotiatedVersion=None, NoOfApplyActions=None, NoOfWriteActions=None, NumberOfActions=None, OutGroup=None, OutPort=None, PacketsCount=None, PbbISid=None, PbbISidMask=None, PhysicalInPort=None, Priority=None, RemoteIp=None, ReplyState=None, SctpDestination=None, SctpSource=None, TableId=None, TcpDestination=None, TcpSource=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, TunnelId=None, TunnelIdMask=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanMask=None, VlanPriority=None, WriteActionsInstruction=None, WriteMetadataInstruction=None):
		"""Finds and retrieves flowStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve flowStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all flowStatLearnedInformation data from the server.

		Args:
			ActiveNanoSeconds (number): Signifies the active time in nano seconds for the session.
			ActiveSeconds (number): Signifies the number of active seconds for the session.
			ApplyActionsInstruction (str): NOT DEFINED
			ApplyMeterInstruction (str): NOT DEFINED
			ArpDstHwAddr (str): The hardware address of the ARP destination.
			ArpDstHwAddressMask (str): Value of the ARP destination hardware address mask field.
			ArpDstIpv4Address (str): Value of the ARP destination IPv4 address field.
			ArpDstIpv4AddressMask (str): Value of the ARP destination IPv4 address mask field value.
			ArpOpcode (str): Value of the ARP opcode field.
			ArpSrcHwAddr (str): The hardware address of the ARP source.
			ArpSrcHwAddressMask (str): Value of the ARP source hardware address mask field.
			ArpSrcIpv4Address (str): Value of the ARP source IPv4 address field.
			ArpSrcIpv4AddressMask (str): Value of the ARP source IPv4 address mask field.
			BytesCount (str): Signifies the count of bytes.
			ClearActionsInstruction (str): NOT DEFINED
			Cookie (str): Signifies the cookie value.
			CookieMask (str): Value of the cookie mask field.
			DataPathId (str): The data path identification of the switch, in decimal format.
			DataPathIdAsHex (str): Signifies the datapath ID of the OpenFlow switch in hexadecimal format.
			ErrorCode (str): The OpenFlow error code, if any error is received in reply to the statistics request.
			ErrorType (str): Signifies the type of the error received.
			EthernetDestination (str): Signifies the destination address of the Ethernet port.
			EthernetDestinationMask (str): Value of the ethernet destination mask field.
			EthernetSource (str): Signifies the source address of the Ethernet port.
			EthernetSourceMask (str): Value of the ethernet source mask field.
			EthernetType (str): Signifies the type of Ethernet port used.
			ExperimenterData (str): Value of the experimenter data field.
			ExperimenterDataLength (number): Value of the Experimenter data length field.
			ExperimenterField (number): Value of the Experimenter field.
			ExperimenterHashmask (bool): Value of the experimenter hashmask field.
			ExperimenterId (str): Value of the experimenter ID field.
			ExperimenterInstruction (str): NOT DEFINED
			Flags (str): Specifies Flags configured.
			GoToTableInstruction (str): NOT DEFINED
			HardTimeout (number): Signifies the inactive time in seconds after which the Flow range will hard timeout and close.
			Icmpv4Code (str): The code of ICMPv4 port used.
			Icmpv4Type (str): Value of the ICMPv4 type field.
			Icmpv6Code (str): Value of the ICMPv6 code field.
			Icmpv6Type (str): Value of the ICMPv6 type field.
			IdleTimeout (number): Signifies the inactive time in seconds after which the Flow range will timeout and become idle.
			InPort (str): Signifies the input port used.
			IpDscp (str): Signifies the IP DSCP value for advertising.
			IpEcn (str): Value of the IP ECN field.
			IpProtocol (str): Signifies the IP Protocol used.
			Ipv4Destination (str): Signifies the IPv4 Destination address for the port.
			Ipv4Source (str): Signifies the IPv4 Source address for the port.
			Ipv6Destination (str): Value of the IPv6 destination field.
			Ipv6DestinationMask (str): Value of the IPv6 destination mask field.
			Ipv6ExtHeader (number): Value of the Ipv6 extension header field.
			Ipv6ExtHeaderMask (number): Value of the IPv6 external header mask field.
			Ipv6FlowLabel (str): Value of the IPv6 flow label field.
			Ipv6FlowLabelMask (str): Value of the IPv6 flow label mask field.
			Ipv6NdDll (str): The IPv6 ND DLL field value.
			Ipv6NdSll (str): Value of the Ipv6 ND SLL field.
			Ipv6NdTarget (str): Value of the IPv6 ND target field.
			Ipv6Source (str): Value of the IPv6 source field.
			Ipv6SourceMask (str): Value of the IPv6 source mask field.
			Latency (number): The latency measured in microseconds. This shows the timethat is needed to receive a reply to the statistics request sent.
			LocalIp (str): The local interface IP address through which the OpenFlow session is connected.
			Metadata (str): Value of the metadata field.
			MetadataMask (str): Value of the metadata mask field.
			MplsBos (str): Value of the MPLS BoS field.
			MplsLabel (str): Value of the MPLS label field.
			MplsTc (str): Value of the MPLS TC field.
			NegotiatedVersion (str): The OpenFlow version supported by this configuration.
			NoOfApplyActions (str): NOT DEFINED
			NoOfWriteActions (str): NOT DEFINED
			NumberOfActions (str): Signifies the number of actions configured for this OpenFlow channel.
			OutGroup (number): Value of the out group field.
			OutPort (number): Specifies Output port number.
			PacketsCount (str): Signifies the count of packets transmitted.
			PbbISid (str): Value of the PBB I-SID field.
			PbbISidMask (str): Value of the PBB I-SID mask field.
			PhysicalInPort (str): Value of the Physical IN port field.
			Priority (number): Signifies the level of priority.
			RemoteIp (str): The IP address of the switch that is used to connect to controller.
			ReplyState (str): This displays the status of the statistics request. It displays the following values: Reply Received Session Not Established Empty Reply Received No Reply Received.
			SctpDestination (str): Value of the SCTP destination field.
			SctpSource (str): Value of the SCTP source field.
			TableId (str): Signifies the identifier value for the table.
			TcpDestination (str): Value of the TCP destination field.
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
			WriteActionsInstruction (str): NOT DEFINED
			WriteMetadataInstruction (str): NOT DEFINED

		Returns:
			self: This instance with matching flowStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
