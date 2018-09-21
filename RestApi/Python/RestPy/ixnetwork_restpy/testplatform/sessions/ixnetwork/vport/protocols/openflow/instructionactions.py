from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InstructionActions(Base):
	"""The InstructionActions class encapsulates a user managed instructionActions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InstructionActions property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'instructionActions'

	def __init__(self, parent):
		super(InstructionActions, self).__init__(parent)

	@property
	def ActionType(self):
		"""The action type associated with this instruction.

		Returns:
			str(drop|output|setEthernetSource|setEthernetDestination|setEthernetType|setVlanId|setVlanPriority|setIpDscp|setIpEcn|setIpProtocol|setIpv4Source|setIpv4Destination|setTcpSource|setTcpDestination|setUdpSource|setUdpDestination|setSctpSource|setSctpDestination|setIcmpv4Type|setIcmpv4Code|setArpOpcode|setArpSourceHwAddress|setArpTargetHwAddress|setArpSourceIpv4Address|setArpTargetIpv4Address|setIpv6Source|setIpv6Destination|setIpv6FlowLabel|setIcmpv6Type|setIcmpv6Code|setIpv6NdTarget|setIpv6NdSll|setIpv6NdTll|setMplsLabel|setMplsTc|setMplsBos|setPbbIsid|setTunnelId|setIpv6ExtHeader|copyTtlOut|copyTtlIn|setMplsTtl|decrementMplsTtl|pushVlan|popVlan|pushMpls|popMpls|setQueue|group|setNetworkTtl|decrementNetworkTtl|pushPbb|popPbb|experimenter|setExperimenter)
		"""
		return self._get_attribute('actionType')
	@ActionType.setter
	def ActionType(self, value):
		self._set_attribute('actionType', value)

	@property
	def ArpDstHwAddr(self):
		"""Value of the ARP destination hardware address.

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddr')
	@ArpDstHwAddr.setter
	def ArpDstHwAddr(self, value):
		self._set_attribute('arpDstHwAddr', value)

	@property
	def ArpDstIpv4Addr(self):
		"""The ARP destination IPv4 address field value.

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4Addr')
	@ArpDstIpv4Addr.setter
	def ArpDstIpv4Addr(self, value):
		self._set_attribute('arpDstIpv4Addr', value)

	@property
	def ArpOpcode(self):
		"""Value of the ARP opcode field.

		Returns:
			number
		"""
		return self._get_attribute('arpOpcode')
	@ArpOpcode.setter
	def ArpOpcode(self, value):
		self._set_attribute('arpOpcode', value)

	@property
	def ArpSrcHwAddr(self):
		"""Value of the ARP source hardware address.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddr')
	@ArpSrcHwAddr.setter
	def ArpSrcHwAddr(self, value):
		self._set_attribute('arpSrcHwAddr', value)

	@property
	def ArpSrcIpv4Addr(self):
		"""The ARP source IPv4 address field value.

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4Addr')
	@ArpSrcIpv4Addr.setter
	def ArpSrcIpv4Addr(self, value):
		self._set_attribute('arpSrcIpv4Addr', value)

	@property
	def EthernetDestination(self):
		"""The Ethernet destination address.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""The Ethernet source address.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""The type of Ethernet port used.

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def Experimenter(self):
		"""The unique Experimenter identifier. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def ExperimenterData(self):
		"""The experimenter data field value.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDatalength(self):
		"""Value of the Experimenter data length field.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDatalength')
	@ExperimenterDatalength.setter
	def ExperimenterDatalength(self, value):
		self._set_attribute('experimenterDatalength', value)

	@property
	def ExperimenterField(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('experimenterField')
	@ExperimenterField.setter
	def ExperimenterField(self, value):
		self._set_attribute('experimenterField', value)

	@property
	def GroupId(self):
		"""Set the Group identifier.

		Returns:
			number
		"""
		return self._get_attribute('groupId')
	@GroupId.setter
	def GroupId(self, value):
		self._set_attribute('groupId', value)

	@property
	def Icmpv4Code(self):
		"""The code of ICMPv4 port used.

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Code')
	@Icmpv4Code.setter
	def Icmpv4Code(self, value):
		self._set_attribute('icmpv4Code', value)

	@property
	def Icmpv4Type(self):
		"""The type of ICMPv4 port used.

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Type')
	@Icmpv4Type.setter
	def Icmpv4Type(self, value):
		self._set_attribute('icmpv4Type', value)

	@property
	def Icmpv6Code(self):
		"""Value of the ICMPv6 code field.

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""Value of the ICMPv6 type field.

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def IpDscp(self):
		"""The IP DSCP value for advertising.

		Returns:
			number
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""The IP ECN field value.

		Returns:
			number
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""The IP protocol used.

		Returns:
			number
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""The IPv4 destination address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""The IPv4 source address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv6Destination(self):
		"""Value of the IPv6 destination field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Destination')
	@Ipv6Destination.setter
	def Ipv6Destination(self, value):
		self._set_attribute('ipv6Destination', value)

	@property
	def Ipv6ExtHeader(self):
		"""The Ipv6 extension header field value.

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6FlowLabel(self):
		"""Value of the IPv6 flow label field.

		Returns:
			number
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NdSll(self):
		"""Set the source link-layer address option in an IPv6 Neighbor Discovery message.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')
	@Ipv6NdSll.setter
	def Ipv6NdSll(self, value):
		self._set_attribute('ipv6NdSll', value)

	@property
	def Ipv6NdTll(self):
		"""Set the target link-layer address option in an IPv6 Neighbor Discovery message.

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTll')
	@Ipv6NdTll.setter
	def Ipv6NdTll(self, value):
		self._set_attribute('ipv6NdTll', value)

	@property
	def Ipv6Source(self):
		"""Value of the IPv6 source field.

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')
	@Ipv6Source.setter
	def Ipv6Source(self, value):
		self._set_attribute('ipv6Source', value)

	@property
	def Ipv6ndTarget(self):
		"""The IPv6 ND target field value.

		Returns:
			str
		"""
		return self._get_attribute('ipv6ndTarget')
	@Ipv6ndTarget.setter
	def Ipv6ndTarget(self, value):
		self._set_attribute('ipv6ndTarget', value)

	@property
	def MaxByteLength(self):
		"""Sets the maximum length in bytes. The minimum value is 0 and the maximum value is 65,535 bytes.

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')
	@MaxByteLength.setter
	def MaxByteLength(self, value):
		self._set_attribute('maxByteLength', value)

	@property
	def MplsBos(self):
		"""Value of the MPLS BoS field.

		Returns:
			number
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""Set the LABEL in the first MPLS shim header.

		Returns:
			number
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""The MPLS TC field value.

		Returns:
			number
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def MplsTtl(self):
		"""Replaces the existing MPLS TTL. Only applies to packets with an existing MPLS shim header.

		Returns:
			number
		"""
		return self._get_attribute('mplsTtl')
	@MplsTtl.setter
	def MplsTtl(self, value):
		self._set_attribute('mplsTtl', value)

	@property
	def NwTtl(self):
		"""Set the IP TTL.

		Returns:
			number
		"""
		return self._get_attribute('nwTtl')
	@NwTtl.setter
	def NwTtl(self, value):
		self._set_attribute('nwTtl', value)

	@property
	def OutputPort(self):
		"""The Output port number to be used.

		Returns:
			number
		"""
		return self._get_attribute('outputPort')
	@OutputPort.setter
	def OutputPort(self, value):
		self._set_attribute('outputPort', value)

	@property
	def OutputPortType(self):
		"""Specify the Output Port Type for this Instruction.

		Returns:
			str(ofppInPort|manual|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal)
		"""
		return self._get_attribute('outputPortType')
	@OutputPortType.setter
	def OutputPortType(self, value):
		self._set_attribute('outputPortType', value)

	@property
	def PbbIsId(self):
		"""Value of the PBB I-SID field.

		Returns:
			number
		"""
		return self._get_attribute('pbbIsId')
	@PbbIsId.setter
	def PbbIsId(self, value):
		self._set_attribute('pbbIsId', value)

	@property
	def QueueId(self):
		"""The identifier of the Queue.

		Returns:
			number
		"""
		return self._get_attribute('queueId')
	@QueueId.setter
	def QueueId(self, value):
		self._set_attribute('queueId', value)

	@property
	def SctpDestination(self):
		"""The SCTP destination field value.

		Returns:
			number
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""Value of the SCTP source field.

		Returns:
			number
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def TcpDestination(self):
		"""The Transport destination address.

		Returns:
			number
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""Value of the TCP source field.

		Returns:
			number
		"""
		return self._get_attribute('tcpSource')
	@TcpSource.setter
	def TcpSource(self, value):
		self._set_attribute('tcpSource', value)

	@property
	def TunnelId(self):
		"""Value of the tunnel ID field.

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')
	@TunnelId.setter
	def TunnelId(self, value):
		self._set_attribute('tunnelId', value)

	@property
	def UdpDestination(self):
		"""Value of the UDP destination field.

		Returns:
			number
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""Value of the UDP source field.

		Returns:
			number
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""The unique VLAN Identifier.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""The User Priority for this VLAN.

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, ActionType=None, ArpDstHwAddr=None, ArpDstIpv4Addr=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcIpv4Addr=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, Experimenter=None, ExperimenterData=None, ExperimenterDatalength=None, ExperimenterField=None, GroupId=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6ExtHeader=None, Ipv6FlowLabel=None, Ipv6NdSll=None, Ipv6NdTll=None, Ipv6Source=None, Ipv6ndTarget=None, MaxByteLength=None, MplsBos=None, MplsLabel=None, MplsTc=None, MplsTtl=None, NwTtl=None, OutputPort=None, OutputPortType=None, PbbIsId=None, QueueId=None, SctpDestination=None, SctpSource=None, TcpDestination=None, TcpSource=None, TunnelId=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanPriority=None):
		"""Adds a new instructionActions node on the server and retrieves it in this instance.

		Args:
			ActionType (str(drop|output|setEthernetSource|setEthernetDestination|setEthernetType|setVlanId|setVlanPriority|setIpDscp|setIpEcn|setIpProtocol|setIpv4Source|setIpv4Destination|setTcpSource|setTcpDestination|setUdpSource|setUdpDestination|setSctpSource|setSctpDestination|setIcmpv4Type|setIcmpv4Code|setArpOpcode|setArpSourceHwAddress|setArpTargetHwAddress|setArpSourceIpv4Address|setArpTargetIpv4Address|setIpv6Source|setIpv6Destination|setIpv6FlowLabel|setIcmpv6Type|setIcmpv6Code|setIpv6NdTarget|setIpv6NdSll|setIpv6NdTll|setMplsLabel|setMplsTc|setMplsBos|setPbbIsid|setTunnelId|setIpv6ExtHeader|copyTtlOut|copyTtlIn|setMplsTtl|decrementMplsTtl|pushVlan|popVlan|pushMpls|popMpls|setQueue|group|setNetworkTtl|decrementNetworkTtl|pushPbb|popPbb|experimenter|setExperimenter)): The action type associated with this instruction.
			ArpDstHwAddr (str): Value of the ARP destination hardware address.
			ArpDstIpv4Addr (str): The ARP destination IPv4 address field value.
			ArpOpcode (number): Value of the ARP opcode field.
			ArpSrcHwAddr (str): Value of the ARP source hardware address.
			ArpSrcIpv4Addr (str): The ARP source IPv4 address field value.
			EthernetDestination (str): The Ethernet destination address.
			EthernetSource (str): The Ethernet source address.
			EthernetType (str): The type of Ethernet port used.
			Experimenter (number): The unique Experimenter identifier. The default value is 1.
			ExperimenterData (str): The experimenter data field value.
			ExperimenterDatalength (number): Value of the Experimenter data length field.
			ExperimenterField (number): NOT DEFINED
			GroupId (number): Set the Group identifier.
			Icmpv4Code (number): The code of ICMPv4 port used.
			Icmpv4Type (number): The type of ICMPv4 port used.
			Icmpv6Code (number): Value of the ICMPv6 code field.
			Icmpv6Type (number): Value of the ICMPv6 type field.
			IpDscp (number): The IP DSCP value for advertising.
			IpEcn (number): The IP ECN field value.
			IpProtocol (number): The IP protocol used.
			Ipv4Destination (str): The IPv4 destination address.
			Ipv4Source (str): The IPv4 source address.
			Ipv6Destination (str): Value of the IPv6 destination field.
			Ipv6ExtHeader (number): The Ipv6 extension header field value.
			Ipv6FlowLabel (number): Value of the IPv6 flow label field.
			Ipv6NdSll (str): Set the source link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6NdTll (str): Set the target link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6Source (str): Value of the IPv6 source field.
			Ipv6ndTarget (str): The IPv6 ND target field value.
			MaxByteLength (number): Sets the maximum length in bytes. The minimum value is 0 and the maximum value is 65,535 bytes.
			MplsBos (number): Value of the MPLS BoS field.
			MplsLabel (number): Set the LABEL in the first MPLS shim header.
			MplsTc (number): The MPLS TC field value.
			MplsTtl (number): Replaces the existing MPLS TTL. Only applies to packets with an existing MPLS shim header.
			NwTtl (number): Set the IP TTL.
			OutputPort (number): The Output port number to be used.
			OutputPortType (str(ofppInPort|manual|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal)): Specify the Output Port Type for this Instruction.
			PbbIsId (number): Value of the PBB I-SID field.
			QueueId (number): The identifier of the Queue.
			SctpDestination (number): The SCTP destination field value.
			SctpSource (number): Value of the SCTP source field.
			TcpDestination (number): The Transport destination address.
			TcpSource (number): Value of the TCP source field.
			TunnelId (str): Value of the tunnel ID field.
			UdpDestination (number): Value of the UDP destination field.
			UdpSource (number): Value of the UDP source field.
			VlanId (number): The unique VLAN Identifier.
			VlanPriority (number): The User Priority for this VLAN.

		Returns:
			self: This instance with all currently retrieved instructionActions data using find and the newly added instructionActions data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the instructionActions data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActionType=None, ArpDstHwAddr=None, ArpDstIpv4Addr=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcIpv4Addr=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, Experimenter=None, ExperimenterData=None, ExperimenterDatalength=None, ExperimenterField=None, GroupId=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6ExtHeader=None, Ipv6FlowLabel=None, Ipv6NdSll=None, Ipv6NdTll=None, Ipv6Source=None, Ipv6ndTarget=None, MaxByteLength=None, MplsBos=None, MplsLabel=None, MplsTc=None, MplsTtl=None, NwTtl=None, OutputPort=None, OutputPortType=None, PbbIsId=None, QueueId=None, SctpDestination=None, SctpSource=None, TcpDestination=None, TcpSource=None, TunnelId=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves instructionActions data from the server.

		All named parameters support regex and can be used to selectively retrieve instructionActions data from the server.
		By default the find method takes no parameters and will retrieve all instructionActions data from the server.

		Args:
			ActionType (str(drop|output|setEthernetSource|setEthernetDestination|setEthernetType|setVlanId|setVlanPriority|setIpDscp|setIpEcn|setIpProtocol|setIpv4Source|setIpv4Destination|setTcpSource|setTcpDestination|setUdpSource|setUdpDestination|setSctpSource|setSctpDestination|setIcmpv4Type|setIcmpv4Code|setArpOpcode|setArpSourceHwAddress|setArpTargetHwAddress|setArpSourceIpv4Address|setArpTargetIpv4Address|setIpv6Source|setIpv6Destination|setIpv6FlowLabel|setIcmpv6Type|setIcmpv6Code|setIpv6NdTarget|setIpv6NdSll|setIpv6NdTll|setMplsLabel|setMplsTc|setMplsBos|setPbbIsid|setTunnelId|setIpv6ExtHeader|copyTtlOut|copyTtlIn|setMplsTtl|decrementMplsTtl|pushVlan|popVlan|pushMpls|popMpls|setQueue|group|setNetworkTtl|decrementNetworkTtl|pushPbb|popPbb|experimenter|setExperimenter)): The action type associated with this instruction.
			ArpDstHwAddr (str): Value of the ARP destination hardware address.
			ArpDstIpv4Addr (str): The ARP destination IPv4 address field value.
			ArpOpcode (number): Value of the ARP opcode field.
			ArpSrcHwAddr (str): Value of the ARP source hardware address.
			ArpSrcIpv4Addr (str): The ARP source IPv4 address field value.
			EthernetDestination (str): The Ethernet destination address.
			EthernetSource (str): The Ethernet source address.
			EthernetType (str): The type of Ethernet port used.
			Experimenter (number): The unique Experimenter identifier. The default value is 1.
			ExperimenterData (str): The experimenter data field value.
			ExperimenterDatalength (number): Value of the Experimenter data length field.
			ExperimenterField (number): NOT DEFINED
			GroupId (number): Set the Group identifier.
			Icmpv4Code (number): The code of ICMPv4 port used.
			Icmpv4Type (number): The type of ICMPv4 port used.
			Icmpv6Code (number): Value of the ICMPv6 code field.
			Icmpv6Type (number): Value of the ICMPv6 type field.
			IpDscp (number): The IP DSCP value for advertising.
			IpEcn (number): The IP ECN field value.
			IpProtocol (number): The IP protocol used.
			Ipv4Destination (str): The IPv4 destination address.
			Ipv4Source (str): The IPv4 source address.
			Ipv6Destination (str): Value of the IPv6 destination field.
			Ipv6ExtHeader (number): The Ipv6 extension header field value.
			Ipv6FlowLabel (number): Value of the IPv6 flow label field.
			Ipv6NdSll (str): Set the source link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6NdTll (str): Set the target link-layer address option in an IPv6 Neighbor Discovery message.
			Ipv6Source (str): Value of the IPv6 source field.
			Ipv6ndTarget (str): The IPv6 ND target field value.
			MaxByteLength (number): Sets the maximum length in bytes. The minimum value is 0 and the maximum value is 65,535 bytes.
			MplsBos (number): Value of the MPLS BoS field.
			MplsLabel (number): Set the LABEL in the first MPLS shim header.
			MplsTc (number): The MPLS TC field value.
			MplsTtl (number): Replaces the existing MPLS TTL. Only applies to packets with an existing MPLS shim header.
			NwTtl (number): Set the IP TTL.
			OutputPort (number): The Output port number to be used.
			OutputPortType (str(ofppInPort|manual|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal)): Specify the Output Port Type for this Instruction.
			PbbIsId (number): Value of the PBB I-SID field.
			QueueId (number): The identifier of the Queue.
			SctpDestination (number): The SCTP destination field value.
			SctpSource (number): Value of the SCTP source field.
			TcpDestination (number): The Transport destination address.
			TcpSource (number): Value of the TCP source field.
			TunnelId (str): Value of the tunnel ID field.
			UdpDestination (number): Value of the UDP destination field.
			UdpSource (number): Value of the UDP source field.
			VlanId (number): The unique VLAN Identifier.
			VlanPriority (number): The User Priority for this VLAN.

		Returns:
			self: This instance with matching instructionActions data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of instructionActions data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the instructionActions data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
