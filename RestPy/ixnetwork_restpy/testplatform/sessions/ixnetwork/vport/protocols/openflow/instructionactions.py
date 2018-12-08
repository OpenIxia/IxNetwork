
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			str(drop|output|setEthernetSource|setEthernetDestination|setEthernetType|setVlanId|setVlanPriority|setIpDscp|setIpEcn|setIpProtocol|setIpv4Source|setIpv4Destination|setTcpSource|setTcpDestination|setUdpSource|setUdpDestination|setSctpSource|setSctpDestination|setIcmpv4Type|setIcmpv4Code|setArpOpcode|setArpSourceHwAddress|setArpTargetHwAddress|setArpSourceIpv4Address|setArpTargetIpv4Address|setIpv6Source|setIpv6Destination|setIpv6FlowLabel|setIcmpv6Type|setIcmpv6Code|setIpv6NdTarget|setIpv6NdSll|setIpv6NdTll|setMplsLabel|setMplsTc|setMplsBos|setPbbIsid|setTunnelId|setIpv6ExtHeader|copyTtlOut|copyTtlIn|setMplsTtl|decrementMplsTtl|pushVlan|popVlan|pushMpls|popMpls|setQueue|group|setNetworkTtl|decrementNetworkTtl|pushPbb|popPbb|experimenter|setExperimenter)
		"""
		return self._get_attribute('actionType')
	@ActionType.setter
	def ActionType(self, value):
		self._set_attribute('actionType', value)

	@property
	def ArpDstHwAddr(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddr')
	@ArpDstHwAddr.setter
	def ArpDstHwAddr(self, value):
		self._set_attribute('arpDstHwAddr', value)

	@property
	def ArpDstIpv4Addr(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4Addr')
	@ArpDstIpv4Addr.setter
	def ArpDstIpv4Addr(self, value):
		self._set_attribute('arpDstIpv4Addr', value)

	@property
	def ArpOpcode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('arpOpcode')
	@ArpOpcode.setter
	def ArpOpcode(self, value):
		self._set_attribute('arpOpcode', value)

	@property
	def ArpSrcHwAddr(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddr')
	@ArpSrcHwAddr.setter
	def ArpSrcHwAddr(self, value):
		self._set_attribute('arpSrcHwAddr', value)

	@property
	def ArpSrcIpv4Addr(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4Addr')
	@ArpSrcIpv4Addr.setter
	def ArpSrcIpv4Addr(self, value):
		self._set_attribute('arpSrcIpv4Addr', value)

	@property
	def EthernetDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def Experimenter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def ExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')
	@ExperimenterData.setter
	def ExperimenterData(self, value):
		self._set_attribute('experimenterData', value)

	@property
	def ExperimenterDatalength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterDatalength')
	@ExperimenterDatalength.setter
	def ExperimenterDatalength(self, value):
		self._set_attribute('experimenterDatalength', value)

	@property
	def ExperimenterField(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterField')
	@ExperimenterField.setter
	def ExperimenterField(self, value):
		self._set_attribute('experimenterField', value)

	@property
	def GroupId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupId')
	@GroupId.setter
	def GroupId(self, value):
		self._set_attribute('groupId', value)

	@property
	def Icmpv4Code(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Code')
	@Icmpv4Code.setter
	def Icmpv4Code(self, value):
		self._set_attribute('icmpv4Code', value)

	@property
	def Icmpv4Type(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Type')
	@Icmpv4Type.setter
	def Icmpv4Type(self, value):
		self._set_attribute('icmpv4Type', value)

	@property
	def Icmpv6Code(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def IpDscp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv6Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Destination')
	@Ipv6Destination.setter
	def Ipv6Destination(self, value):
		self._set_attribute('ipv6Destination', value)

	@property
	def Ipv6ExtHeader(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6FlowLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NdSll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')
	@Ipv6NdSll.setter
	def Ipv6NdSll(self, value):
		self._set_attribute('ipv6NdSll', value)

	@property
	def Ipv6NdTll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTll')
	@Ipv6NdTll.setter
	def Ipv6NdTll(self, value):
		self._set_attribute('ipv6NdTll', value)

	@property
	def Ipv6Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')
	@Ipv6Source.setter
	def Ipv6Source(self, value):
		self._set_attribute('ipv6Source', value)

	@property
	def Ipv6ndTarget(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6ndTarget')
	@Ipv6ndTarget.setter
	def Ipv6ndTarget(self, value):
		self._set_attribute('ipv6ndTarget', value)

	@property
	def MaxByteLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')
	@MaxByteLength.setter
	def MaxByteLength(self, value):
		self._set_attribute('maxByteLength', value)

	@property
	def MplsBos(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def MplsTtl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsTtl')
	@MplsTtl.setter
	def MplsTtl(self, value):
		self._set_attribute('mplsTtl', value)

	@property
	def NwTtl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nwTtl')
	@NwTtl.setter
	def NwTtl(self, value):
		self._set_attribute('nwTtl', value)

	@property
	def OutputPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outputPort')
	@OutputPort.setter
	def OutputPort(self, value):
		self._set_attribute('outputPort', value)

	@property
	def OutputPortType(self):
		"""

		Returns:
			str(ofppInPort|manual|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal)
		"""
		return self._get_attribute('outputPortType')
	@OutputPortType.setter
	def OutputPortType(self, value):
		self._set_attribute('outputPortType', value)

	@property
	def PbbIsId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pbbIsId')
	@PbbIsId.setter
	def PbbIsId(self, value):
		self._set_attribute('pbbIsId', value)

	@property
	def QueueId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueId')
	@QueueId.setter
	def QueueId(self, value):
		self._set_attribute('queueId', value)

	@property
	def SctpDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def TcpDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tcpSource')
	@TcpSource.setter
	def TcpSource(self, value):
		self._set_attribute('tcpSource', value)

	@property
	def TunnelId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')
	@TunnelId.setter
	def TunnelId(self, value):
		self._set_attribute('tunnelId', value)

	@property
	def UdpDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""

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
			ActionType (str(drop|output|setEthernetSource|setEthernetDestination|setEthernetType|setVlanId|setVlanPriority|setIpDscp|setIpEcn|setIpProtocol|setIpv4Source|setIpv4Destination|setTcpSource|setTcpDestination|setUdpSource|setUdpDestination|setSctpSource|setSctpDestination|setIcmpv4Type|setIcmpv4Code|setArpOpcode|setArpSourceHwAddress|setArpTargetHwAddress|setArpSourceIpv4Address|setArpTargetIpv4Address|setIpv6Source|setIpv6Destination|setIpv6FlowLabel|setIcmpv6Type|setIcmpv6Code|setIpv6NdTarget|setIpv6NdSll|setIpv6NdTll|setMplsLabel|setMplsTc|setMplsBos|setPbbIsid|setTunnelId|setIpv6ExtHeader|copyTtlOut|copyTtlIn|setMplsTtl|decrementMplsTtl|pushVlan|popVlan|pushMpls|popMpls|setQueue|group|setNetworkTtl|decrementNetworkTtl|pushPbb|popPbb|experimenter|setExperimenter)): 
			ArpDstHwAddr (str): 
			ArpDstIpv4Addr (str): 
			ArpOpcode (number): 
			ArpSrcHwAddr (str): 
			ArpSrcIpv4Addr (str): 
			EthernetDestination (str): 
			EthernetSource (str): 
			EthernetType (str): 
			Experimenter (number): 
			ExperimenterData (str): 
			ExperimenterDatalength (number): 
			ExperimenterField (number): 
			GroupId (number): 
			Icmpv4Code (number): 
			Icmpv4Type (number): 
			Icmpv6Code (number): 
			Icmpv6Type (number): 
			IpDscp (number): 
			IpEcn (number): 
			IpProtocol (number): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			Ipv6Destination (str): 
			Ipv6ExtHeader (number): 
			Ipv6FlowLabel (number): 
			Ipv6NdSll (str): 
			Ipv6NdTll (str): 
			Ipv6Source (str): 
			Ipv6ndTarget (str): 
			MaxByteLength (number): 
			MplsBos (number): 
			MplsLabel (number): 
			MplsTc (number): 
			MplsTtl (number): 
			NwTtl (number): 
			OutputPort (number): 
			OutputPortType (str(ofppInPort|manual|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal)): 
			PbbIsId (number): 
			QueueId (number): 
			SctpDestination (number): 
			SctpSource (number): 
			TcpDestination (number): 
			TcpSource (number): 
			TunnelId (str): 
			UdpDestination (number): 
			UdpSource (number): 
			VlanId (number): 
			VlanPriority (number): 

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
			ActionType (str(drop|output|setEthernetSource|setEthernetDestination|setEthernetType|setVlanId|setVlanPriority|setIpDscp|setIpEcn|setIpProtocol|setIpv4Source|setIpv4Destination|setTcpSource|setTcpDestination|setUdpSource|setUdpDestination|setSctpSource|setSctpDestination|setIcmpv4Type|setIcmpv4Code|setArpOpcode|setArpSourceHwAddress|setArpTargetHwAddress|setArpSourceIpv4Address|setArpTargetIpv4Address|setIpv6Source|setIpv6Destination|setIpv6FlowLabel|setIcmpv6Type|setIcmpv6Code|setIpv6NdTarget|setIpv6NdSll|setIpv6NdTll|setMplsLabel|setMplsTc|setMplsBos|setPbbIsid|setTunnelId|setIpv6ExtHeader|copyTtlOut|copyTtlIn|setMplsTtl|decrementMplsTtl|pushVlan|popVlan|pushMpls|popMpls|setQueue|group|setNetworkTtl|decrementNetworkTtl|pushPbb|popPbb|experimenter|setExperimenter)): 
			ArpDstHwAddr (str): 
			ArpDstIpv4Addr (str): 
			ArpOpcode (number): 
			ArpSrcHwAddr (str): 
			ArpSrcIpv4Addr (str): 
			EthernetDestination (str): 
			EthernetSource (str): 
			EthernetType (str): 
			Experimenter (number): 
			ExperimenterData (str): 
			ExperimenterDatalength (number): 
			ExperimenterField (number): 
			GroupId (number): 
			Icmpv4Code (number): 
			Icmpv4Type (number): 
			Icmpv6Code (number): 
			Icmpv6Type (number): 
			IpDscp (number): 
			IpEcn (number): 
			IpProtocol (number): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			Ipv6Destination (str): 
			Ipv6ExtHeader (number): 
			Ipv6FlowLabel (number): 
			Ipv6NdSll (str): 
			Ipv6NdTll (str): 
			Ipv6Source (str): 
			Ipv6ndTarget (str): 
			MaxByteLength (number): 
			MplsBos (number): 
			MplsLabel (number): 
			MplsTc (number): 
			MplsTtl (number): 
			NwTtl (number): 
			OutputPort (number): 
			OutputPortType (str(ofppInPort|manual|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal)): 
			PbbIsId (number): 
			QueueId (number): 
			SctpDestination (number): 
			SctpSource (number): 
			TcpDestination (number): 
			TcpSource (number): 
			TunnelId (str): 
			UdpDestination (number): 
			UdpSource (number): 
			VlanId (number): 
			VlanPriority (number): 

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
