
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
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddr')

	@property
	def ArpDstHwAddressMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddressMask')

	@property
	def ArpDstIpv4Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4Address')

	@property
	def ArpDstIpv4AddressMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstIpv4AddressMask')

	@property
	def ArpOpcode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpOpcode')

	@property
	def ArpSrcHwAddr(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddr')

	@property
	def ArpSrcHwAddressMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddressMask')

	@property
	def ArpSrcIpv4Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4Address')

	@property
	def ArpSrcIpv4AddressMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcIpv4AddressMask')

	@property
	def BytesCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bytesCount')

	@property
	def Cookie(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cookie')

	@property
	def CookieMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cookieMask')

	@property
	def DataPathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def ErrorCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def EthernetDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetDestinationMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestinationMask')

	@property
	def EthernetSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def EthernetSourceMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSourceMask')

	@property
	def EthernetType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def ExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def ExperimenterField(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterField')

	@property
	def ExperimenterHashmask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('experimenterHashmask')

	@property
	def ExperimenterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterId')

	@property
	def FlowsCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowsCount')

	@property
	def Icmpv6Code(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Code')

	@property
	def Icmpv6Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('icmpv6Type')

	@property
	def InPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('inPort')

	@property
	def IpDscp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def IpEcn(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipEcn')

	@property
	def IpProtocol(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipProtocol')

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')

	@property
	def Ipv6Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Destination')

	@property
	def Ipv6DestinationMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6DestinationMask')

	@property
	def Ipv6ExtHeader(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6ExtHeaderMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeaderMask')

	@property
	def Ipv6FlowLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6FlowLabelMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabelMask')

	@property
	def Ipv6NdDll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdDll')

	@property
	def Ipv6NdSll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdSll')

	@property
	def Ipv6NdTarget(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTarget')

	@property
	def Ipv6Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')

	@property
	def Ipv6SourceMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6SourceMask')

	@property
	def Latency(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def Metadata(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadata')

	@property
	def MetadataMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataMask')

	@property
	def MplsBos(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsBos')

	@property
	def MplsLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsTc(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsTc')

	@property
	def NegotiatedVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def OutGroup(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outGroup')

	@property
	def OutPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outPort')

	@property
	def PacketsCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('packetsCount')

	@property
	def PbbISid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbISid')

	@property
	def PbbISidMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbISidMask')

	@property
	def PhysicalInPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('physicalInPort')

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def SctpDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sctpDestination')

	@property
	def SctpSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sctpSource')

	@property
	def TableId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tableId')

	@property
	def TcpDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tcpDestination')

	@property
	def TcpSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tcpSource')

	@property
	def TransportDestinationIcmpCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transportDestinationIcmpCode')

	@property
	def TransportSourceIcmpType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('transportSourceIcmpType')

	@property
	def TunnelId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')

	@property
	def TunnelIdMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelIdMask')

	@property
	def UdpDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('udpDestination')

	@property
	def UdpSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('udpSource')

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanMask')

	@property
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ArpDstHwAddr=None, ArpDstHwAddressMask=None, ArpDstIpv4Address=None, ArpDstIpv4AddressMask=None, ArpOpcode=None, ArpSrcHwAddr=None, ArpSrcHwAddressMask=None, ArpSrcIpv4Address=None, ArpSrcIpv4AddressMask=None, BytesCount=None, Cookie=None, CookieMask=None, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, EthernetDestination=None, EthernetDestinationMask=None, EthernetSource=None, EthernetSourceMask=None, EthernetType=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterField=None, ExperimenterHashmask=None, ExperimenterId=None, FlowsCount=None, Icmpv6Code=None, Icmpv6Type=None, InPort=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6DestinationMask=None, Ipv6ExtHeader=None, Ipv6ExtHeaderMask=None, Ipv6FlowLabel=None, Ipv6FlowLabelMask=None, Ipv6NdDll=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6Source=None, Ipv6SourceMask=None, Latency=None, LocalIp=None, Metadata=None, MetadataMask=None, MplsBos=None, MplsLabel=None, MplsTc=None, NegotiatedVersion=None, OutGroup=None, OutPort=None, PacketsCount=None, PbbISid=None, PbbISidMask=None, PhysicalInPort=None, RemoteIp=None, ReplyState=None, SctpDestination=None, SctpSource=None, TableId=None, TcpDestination=None, TcpSource=None, TransportDestinationIcmpCode=None, TransportSourceIcmpType=None, TunnelId=None, TunnelIdMask=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanMask=None, VlanPriority=None):
		"""Finds and retrieves flowAggregatedStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve flowAggregatedStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all flowAggregatedStatLearnedInformation data from the server.

		Args:
			ArpDstHwAddr (str): 
			ArpDstHwAddressMask (str): 
			ArpDstIpv4Address (str): 
			ArpDstIpv4AddressMask (str): 
			ArpOpcode (str): 
			ArpSrcHwAddr (str): 
			ArpSrcHwAddressMask (str): 
			ArpSrcIpv4Address (str): 
			ArpSrcIpv4AddressMask (str): 
			BytesCount (str): 
			Cookie (str): 
			CookieMask (str): 
			DataPathId (str): 
			DataPathIdAsHex (str): 
			ErrorCode (str): 
			ErrorType (str): 
			EthernetDestination (str): 
			EthernetDestinationMask (str): 
			EthernetSource (str): 
			EthernetSourceMask (str): 
			EthernetType (str): 
			ExperimenterData (str): 
			ExperimenterDataLength (number): 
			ExperimenterField (number): 
			ExperimenterHashmask (bool): 
			ExperimenterId (str): 
			FlowsCount (number): 
			Icmpv6Code (str): 
			Icmpv6Type (str): 
			InPort (str): 
			IpDscp (str): 
			IpEcn (str): 
			IpProtocol (str): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			Ipv6Destination (str): 
			Ipv6DestinationMask (str): 
			Ipv6ExtHeader (number): 
			Ipv6ExtHeaderMask (number): 
			Ipv6FlowLabel (str): 
			Ipv6FlowLabelMask (str): 
			Ipv6NdDll (str): 
			Ipv6NdSll (str): 
			Ipv6NdTarget (str): 
			Ipv6Source (str): 
			Ipv6SourceMask (str): 
			Latency (number): 
			LocalIp (str): 
			Metadata (str): 
			MetadataMask (str): 
			MplsBos (str): 
			MplsLabel (str): 
			MplsTc (str): 
			NegotiatedVersion (str): 
			OutGroup (number): 
			OutPort (number): 
			PacketsCount (str): 
			PbbISid (str): 
			PbbISidMask (str): 
			PhysicalInPort (str): 
			RemoteIp (str): 
			ReplyState (str): 
			SctpDestination (str): 
			SctpSource (str): 
			TableId (str): 
			TcpDestination (str): 
			TcpSource (str): 
			TransportDestinationIcmpCode (str): 
			TransportSourceIcmpType (str): 
			TunnelId (str): 
			TunnelIdMask (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanId (str): 
			VlanMask (number): 
			VlanPriority (str): 

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
