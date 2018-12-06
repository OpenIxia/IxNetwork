
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


class ControllerTableFlowRanges(Base):
	"""The ControllerTableFlowRanges class encapsulates a user managed controllerTableFlowRanges node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ControllerTableFlowRanges property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'controllerTableFlowRanges'

	def __init__(self, parent):
		super(ControllerTableFlowRanges, self).__init__(parent)

	@property
	def Instructions(self):
		"""An instance of the Instructions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructions.Instructions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.instructions import Instructions
		return Instructions(self)

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
	def ArpDstHwAddrMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddrMask')
	@ArpDstHwAddrMask.setter
	def ArpDstHwAddrMask(self, value):
		self._set_attribute('arpDstHwAddrMask', value)

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
	def ArpDstIpv4AddrMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4AddrMask')
	@ArpDstIpv4AddrMask.setter
	def ArpDstIpv4AddrMask(self, value):
		self._set_attribute('arpDstIpv4AddrMask', value)

	@property
	def ArpOpcode(self):
		"""

		Returns:
			str
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
	def ArpSrcHwAddrMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddrMask')
	@ArpSrcHwAddrMask.setter
	def ArpSrcHwAddrMask(self, value):
		self._set_attribute('arpSrcHwAddrMask', value)

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
	def ArpSrcIpv4AddrMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4AddrMask')
	@ArpSrcIpv4AddrMask.setter
	def ArpSrcIpv4AddrMask(self, value):
		self._set_attribute('arpSrcIpv4AddrMask', value)

	@property
	def CheckOverlapFlags(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('checkOverlapFlags')
	@CheckOverlapFlags.setter
	def CheckOverlapFlags(self, value):
		self._set_attribute('checkOverlapFlags', value)

	@property
	def Cookie(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cookie')
	@Cookie.setter
	def Cookie(self, value):
		self._set_attribute('cookie', value)

	@property
	def CookieMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cookieMask')
	@CookieMask.setter
	def CookieMask(self, value):
		self._set_attribute('cookieMask', value)

	@property
	def Description(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

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
	def EthernetDestinationMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestinationMask')
	@EthernetDestinationMask.setter
	def EthernetDestinationMask(self, value):
		self._set_attribute('ethernetDestinationMask', value)

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
	def EthernetSourceMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSourceMask')
	@EthernetSourceMask.setter
	def EthernetSourceMask(self, value):
		self._set_attribute('ethernetSourceMask', value)

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
	def ExperimenterHasMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('experimenterHasMask')
	@ExperimenterHasMask.setter
	def ExperimenterHasMask(self, value):
		self._set_attribute('experimenterHasMask', value)

	@property
	def ExperimenterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterId')
	@ExperimenterId.setter
	def ExperimenterId(self, value):
		self._set_attribute('experimenterId', value)

	@property
	def FlowAdvertise(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('flowAdvertise')
	@FlowAdvertise.setter
	def FlowAdvertise(self, value):
		self._set_attribute('flowAdvertise', value)

	@property
	def FlowModStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('flowModStatus')

	@property
	def HardTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('hardTimeout')
	@HardTimeout.setter
	def HardTimeout(self, value):
		self._set_attribute('hardTimeout', value)

	@property
	def Icmpv4Code(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('icmpv4Code')
	@Icmpv4Code.setter
	def Icmpv4Code(self, value):
		self._set_attribute('icmpv4Code', value)

	@property
	def Icmpv4Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('icmpv4Type')
	@Icmpv4Type.setter
	def Icmpv4Type(self, value):
		self._set_attribute('icmpv4Type', value)

	@property
	def Icmpv6Code(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def IdleTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('idleTimeout')
	@IdleTimeout.setter
	def IdleTimeout(self, value):
		self._set_attribute('idleTimeout', value)

	@property
	def InPhyPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inPhyPort')
	@InPhyPort.setter
	def InPhyPort(self, value):
		self._set_attribute('inPhyPort', value)

	@property
	def InPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inPort')
	@InPort.setter
	def InPort(self, value):
		self._set_attribute('inPort', value)

	@property
	def IpDscp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""

		Returns:
			str
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
	def Ipv4DestinationMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4DestinationMask')
	@Ipv4DestinationMask.setter
	def Ipv4DestinationMask(self, value):
		self._set_attribute('ipv4DestinationMask', value)

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
	def Ipv4SourceMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4SourceMask')
	@Ipv4SourceMask.setter
	def Ipv4SourceMask(self, value):
		self._set_attribute('ipv4SourceMask', value)

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
	def Ipv6DestinationMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6DestinationMask')
	@Ipv6DestinationMask.setter
	def Ipv6DestinationMask(self, value):
		self._set_attribute('ipv6DestinationMask', value)

	@property
	def Ipv6ExtHeader(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6ExtHeaderMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6ExtHeaderMask')
	@Ipv6ExtHeaderMask.setter
	def Ipv6ExtHeaderMask(self, value):
		self._set_attribute('ipv6ExtHeaderMask', value)

	@property
	def Ipv6FlowLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6FlowLabelMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabelMask')
	@Ipv6FlowLabelMask.setter
	def Ipv6FlowLabelMask(self, value):
		self._set_attribute('ipv6FlowLabelMask', value)

	@property
	def Ipv6NdDll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdDll')
	@Ipv6NdDll.setter
	def Ipv6NdDll(self, value):
		self._set_attribute('ipv6NdDll', value)

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
	def Ipv6NdTarget(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTarget')
	@Ipv6NdTarget.setter
	def Ipv6NdTarget(self, value):
		self._set_attribute('ipv6NdTarget', value)

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
	def Ipv6SourceMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6SourceMask')
	@Ipv6SourceMask.setter
	def Ipv6SourceMask(self, value):
		self._set_attribute('ipv6SourceMask', value)

	@property
	def MatchType(self):
		"""

		Returns:
			str(loose|strict)
		"""
		return self._get_attribute('matchType')
	@MatchType.setter
	def MatchType(self, value):
		self._set_attribute('matchType', value)

	@property
	def Metadata(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadata')
	@Metadata.setter
	def Metadata(self, value):
		self._set_attribute('metadata', value)

	@property
	def MetadataMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataMask')
	@MetadataMask.setter
	def MetadataMask(self, value):
		self._set_attribute('metadataMask', value)

	@property
	def MplsBos(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def NoByteCounts(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('noByteCounts')
	@NoByteCounts.setter
	def NoByteCounts(self, value):
		self._set_attribute('noByteCounts', value)

	@property
	def NoPacketCounts(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('noPacketCounts')
	@NoPacketCounts.setter
	def NoPacketCounts(self, value):
		self._set_attribute('noPacketCounts', value)

	@property
	def NumberOfFlows(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfFlows')
	@NumberOfFlows.setter
	def NumberOfFlows(self, value):
		self._set_attribute('numberOfFlows', value)

	@property
	def PbbIsId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbIsId')
	@PbbIsId.setter
	def PbbIsId(self, value):
		self._set_attribute('pbbIsId', value)

	@property
	def PbbIsIdMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbIsIdMask')
	@PbbIsIdMask.setter
	def PbbIsIdMask(self, value):
		self._set_attribute('pbbIsIdMask', value)

	@property
	def Priority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def ResetCounts(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('resetCounts')
	@ResetCounts.setter
	def ResetCounts(self, value):
		self._set_attribute('resetCounts', value)

	@property
	def SctpDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def SendFlowRemoved(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendFlowRemoved')
	@SendFlowRemoved.setter
	def SendFlowRemoved(self, value):
		self._set_attribute('sendFlowRemoved', value)

	@property
	def TcpDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""

		Returns:
			str
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
	def TunnelIdMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelIdMask')
	@TunnelIdMask.setter
	def TunnelIdMask(self, value):
		self._set_attribute('tunnelIdMask', value)

	@property
	def UdpDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanIdMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanIdMask')
	@VlanIdMask.setter
	def VlanIdMask(self, value):
		self._set_attribute('vlanIdMask', value)

	@property
	def VlanMatchType(self):
		"""

		Returns:
			str(anyVlanTag|withoutVlanTag|withVlanTag|specificVlanTag)
		"""
		return self._get_attribute('vlanMatchType')
	@VlanMatchType.setter
	def VlanMatchType(self, value):
		self._set_attribute('vlanMatchType', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, ArpDstHwAddr=None, ArpDstHwAddrMask=None, ArpDstIpv4Addr=None, ArpDstIpv4AddrMask=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcHwAddrMask=None, ArpSrcIpv4Addr=None, ArpSrcIpv4AddrMask=None, CheckOverlapFlags=None, Cookie=None, CookieMask=None, Description=None, Enabled=None, EthernetDestination=None, EthernetDestinationMask=None, EthernetSource=None, EthernetSourceMask=None, EthernetType=None, ExperimenterData=None, ExperimenterDatalength=None, ExperimenterField=None, ExperimenterHasMask=None, ExperimenterId=None, FlowAdvertise=None, HardTimeout=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IdleTimeout=None, InPhyPort=None, InPort=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4DestinationMask=None, Ipv4Source=None, Ipv4SourceMask=None, Ipv6Destination=None, Ipv6DestinationMask=None, Ipv6ExtHeader=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabel=None, Ipv6FlowLabelMask=None, Ipv6NdDll=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6Source=None, Ipv6SourceMask=None, MatchType=None, Metadata=None, MetadataMask=None, MplsBos=None, MplsLabel=None, MplsTc=None, NoByteCounts=None, NoPacketCounts=None, NumberOfFlows=None, PbbIsId=None, PbbIsIdMask=None, Priority=None, ResetCounts=None, SctpDestination=None, SctpSource=None, SendFlowRemoved=None, TcpDestination=None, TcpSource=None, TunnelId=None, TunnelIdMask=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanIdMask=None, VlanMatchType=None, VlanPriority=None):
		"""Adds a new controllerTableFlowRanges node on the server and retrieves it in this instance.

		Args:
			ArpDstHwAddr (str): 
			ArpDstHwAddrMask (str): 
			ArpDstIpv4Addr (str): 
			ArpDstIpv4AddrMask (str): 
			ArpOpcode (str): 
			ArpSrcHwAddr (str): 
			ArpSrcHwAddrMask (str): 
			ArpSrcIpv4Addr (str): 
			ArpSrcIpv4AddrMask (str): 
			CheckOverlapFlags (bool): 
			Cookie (str): 
			CookieMask (str): 
			Description (str): 
			Enabled (bool): 
			EthernetDestination (str): 
			EthernetDestinationMask (str): 
			EthernetSource (str): 
			EthernetSourceMask (str): 
			EthernetType (str): 
			ExperimenterData (str): 
			ExperimenterDatalength (number): 
			ExperimenterField (number): 
			ExperimenterHasMask (bool): 
			ExperimenterId (str): 
			FlowAdvertise (bool): 
			HardTimeout (number): 
			Icmpv4Code (str): 
			Icmpv4Type (str): 
			Icmpv6Code (str): 
			Icmpv6Type (str): 
			IdleTimeout (number): 
			InPhyPort (str): 
			InPort (str): 
			IpDscp (str): 
			IpEcn (str): 
			IpProtocol (str): 
			Ipv4Destination (str): 
			Ipv4DestinationMask (str): 
			Ipv4Source (str): 
			Ipv4SourceMask (str): 
			Ipv6Destination (str): 
			Ipv6DestinationMask (str): 
			Ipv6ExtHeader (str): 
			Ipv6ExtHeaderMask (str): 
			Ipv6FlowLabel (str): 
			Ipv6FlowLabelMask (str): 
			Ipv6NdDll (str): 
			Ipv6NdSll (str): 
			Ipv6NdTarget (str): 
			Ipv6Source (str): 
			Ipv6SourceMask (str): 
			MatchType (str(loose|strict)): 
			Metadata (str): 
			MetadataMask (str): 
			MplsBos (str): 
			MplsLabel (str): 
			MplsTc (str): 
			NoByteCounts (bool): 
			NoPacketCounts (bool): 
			NumberOfFlows (number): 
			PbbIsId (str): 
			PbbIsIdMask (str): 
			Priority (number): 
			ResetCounts (bool): 
			SctpDestination (str): 
			SctpSource (str): 
			SendFlowRemoved (bool): 
			TcpDestination (str): 
			TcpSource (str): 
			TunnelId (str): 
			TunnelIdMask (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanId (str): 
			VlanIdMask (str): 
			VlanMatchType (str(anyVlanTag|withoutVlanTag|withVlanTag|specificVlanTag)): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved controllerTableFlowRanges data using find and the newly added controllerTableFlowRanges data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the controllerTableFlowRanges data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpDstHwAddr=None, ArpDstHwAddrMask=None, ArpDstIpv4Addr=None, ArpDstIpv4AddrMask=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcHwAddrMask=None, ArpSrcIpv4Addr=None, ArpSrcIpv4AddrMask=None, CheckOverlapFlags=None, Cookie=None, CookieMask=None, Description=None, Enabled=None, EthernetDestination=None, EthernetDestinationMask=None, EthernetSource=None, EthernetSourceMask=None, EthernetType=None, ExperimenterData=None, ExperimenterDatalength=None, ExperimenterField=None, ExperimenterHasMask=None, ExperimenterId=None, FlowAdvertise=None, FlowModStatus=None, HardTimeout=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IdleTimeout=None, InPhyPort=None, InPort=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4DestinationMask=None, Ipv4Source=None, Ipv4SourceMask=None, Ipv6Destination=None, Ipv6DestinationMask=None, Ipv6ExtHeader=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabel=None, Ipv6FlowLabelMask=None, Ipv6NdDll=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6Source=None, Ipv6SourceMask=None, MatchType=None, Metadata=None, MetadataMask=None, MplsBos=None, MplsLabel=None, MplsTc=None, NoByteCounts=None, NoPacketCounts=None, NumberOfFlows=None, PbbIsId=None, PbbIsIdMask=None, Priority=None, ResetCounts=None, SctpDestination=None, SctpSource=None, SendFlowRemoved=None, TcpDestination=None, TcpSource=None, TunnelId=None, TunnelIdMask=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanIdMask=None, VlanMatchType=None, VlanPriority=None):
		"""Finds and retrieves controllerTableFlowRanges data from the server.

		All named parameters support regex and can be used to selectively retrieve controllerTableFlowRanges data from the server.
		By default the find method takes no parameters and will retrieve all controllerTableFlowRanges data from the server.

		Args:
			ArpDstHwAddr (str): 
			ArpDstHwAddrMask (str): 
			ArpDstIpv4Addr (str): 
			ArpDstIpv4AddrMask (str): 
			ArpOpcode (str): 
			ArpSrcHwAddr (str): 
			ArpSrcHwAddrMask (str): 
			ArpSrcIpv4Addr (str): 
			ArpSrcIpv4AddrMask (str): 
			CheckOverlapFlags (bool): 
			Cookie (str): 
			CookieMask (str): 
			Description (str): 
			Enabled (bool): 
			EthernetDestination (str): 
			EthernetDestinationMask (str): 
			EthernetSource (str): 
			EthernetSourceMask (str): 
			EthernetType (str): 
			ExperimenterData (str): 
			ExperimenterDatalength (number): 
			ExperimenterField (number): 
			ExperimenterHasMask (bool): 
			ExperimenterId (str): 
			FlowAdvertise (bool): 
			FlowModStatus (str): 
			HardTimeout (number): 
			Icmpv4Code (str): 
			Icmpv4Type (str): 
			Icmpv6Code (str): 
			Icmpv6Type (str): 
			IdleTimeout (number): 
			InPhyPort (str): 
			InPort (str): 
			IpDscp (str): 
			IpEcn (str): 
			IpProtocol (str): 
			Ipv4Destination (str): 
			Ipv4DestinationMask (str): 
			Ipv4Source (str): 
			Ipv4SourceMask (str): 
			Ipv6Destination (str): 
			Ipv6DestinationMask (str): 
			Ipv6ExtHeader (str): 
			Ipv6ExtHeaderMask (str): 
			Ipv6FlowLabel (str): 
			Ipv6FlowLabelMask (str): 
			Ipv6NdDll (str): 
			Ipv6NdSll (str): 
			Ipv6NdTarget (str): 
			Ipv6Source (str): 
			Ipv6SourceMask (str): 
			MatchType (str(loose|strict)): 
			Metadata (str): 
			MetadataMask (str): 
			MplsBos (str): 
			MplsLabel (str): 
			MplsTc (str): 
			NoByteCounts (bool): 
			NoPacketCounts (bool): 
			NumberOfFlows (number): 
			PbbIsId (str): 
			PbbIsIdMask (str): 
			Priority (number): 
			ResetCounts (bool): 
			SctpDestination (str): 
			SctpSource (str): 
			SendFlowRemoved (bool): 
			TcpDestination (str): 
			TcpSource (str): 
			TunnelId (str): 
			TunnelIdMask (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanId (str): 
			VlanIdMask (str): 
			VlanMatchType (str(anyVlanTag|withoutVlanTag|withVlanTag|specificVlanTag)): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching controllerTableFlowRanges data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of controllerTableFlowRanges data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the controllerTableFlowRanges data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateFlowMod(self, Arg2):
		"""Executes the updateFlowMod operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=controllerTableFlowRanges)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(sendFlowAdd|sendFlowModify|sendFlowRemove)): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateFlowMod', payload=locals(), response_object=None)
