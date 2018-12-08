
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


class SwitchActionV131LearnedInfo(Base):
	"""The SwitchActionV131LearnedInfo class encapsulates a system managed switchActionV131LearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchActionV131LearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchActionV131LearnedInfo'

	def __init__(self, parent):
		super(SwitchActionV131LearnedInfo, self).__init__(parent)

	@property
	def ActionType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionType')

	@property
	def ArpDstHwAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpDstHwAddress')

	@property
	def ArpDstIpv4Address(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('arpDstIpv4Address')

	@property
	def ArpOpcode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('arpOpcode')

	@property
	def ArpSrcHwAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('arpSrcHwAddress')

	@property
	def ArpSrcIpv4Address(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('arpSrcIpv4Address')

	@property
	def EthernetDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def EthernetType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def Experimenter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenter')

	@property
	def ExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDatalength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterDatalength')

	@property
	def GroupId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def Icmpv4Code(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Code')

	@property
	def Icmpv4Type(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv4Type')

	@property
	def Icmpv6Code(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Code')

	@property
	def Icmpv6Type(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('icmpv6Type')

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
			number
		"""
		return self._get_attribute('ipEcn')

	@property
	def IpProtocol(self):
		"""

		Returns:
			number
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
	def Ipv6ExtHeader(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6ExtHeader')

	@property
	def Ipv6FlowLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6FlowLabel')

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
	def Ipv6NdTll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6NdTll')

	@property
	def Ipv6Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Source')

	@property
	def MaxByteLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')

	@property
	def MplsBos(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsBos')

	@property
	def MplsLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsLabel')

	@property
	def MplsTc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsTc')

	@property
	def MplsTtl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsTtl')

	@property
	def NetworkTtl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('networkTtl')

	@property
	def OutputPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def OutputPortType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outputPortType')

	@property
	def PbbIsid(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pbbIsid')

	@property
	def QueueId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def SctpDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sctpDestination')

	@property
	def SctpSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sctpSource')

	@property
	def TcpDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tcpDestination')

	@property
	def TcpSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tcpSource')

	@property
	def TunnelId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tunnelId')

	@property
	def UdpDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('udpDestination')

	@property
	def UdpSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('udpSource')

	@property
	def VlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ActionType=None, ArpDstHwAddress=None, ArpDstIpv4Address=None, ArpOpcode=None, ArpSrcHwAddress=None, ArpSrcIpv4Address=None, EthernetDestination=None, EthernetSource=None, EthernetType=None, Experimenter=None, ExperimenterData=None, ExperimenterDatalength=None, GroupId=None, Icmpv4Code=None, Icmpv4Type=None, Icmpv6Code=None, Icmpv6Type=None, IpDscp=None, IpEcn=None, IpProtocol=None, Ipv4Destination=None, Ipv4Source=None, Ipv6Destination=None, Ipv6ExtHeader=None, Ipv6FlowLabel=None, Ipv6NdSll=None, Ipv6NdTarget=None, Ipv6NdTll=None, Ipv6Source=None, MaxByteLength=None, MplsBos=None, MplsLabel=None, MplsTc=None, MplsTtl=None, NetworkTtl=None, OutputPort=None, OutputPortType=None, PbbIsid=None, QueueId=None, SctpDestination=None, SctpSource=None, TcpDestination=None, TcpSource=None, TunnelId=None, UdpDestination=None, UdpSource=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves switchActionV131LearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchActionV131LearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchActionV131LearnedInfo data from the server.

		Args:
			ActionType (str): 
			ArpDstHwAddress (str): 
			ArpDstIpv4Address (number): 
			ArpOpcode (number): 
			ArpSrcHwAddress (str): 
			ArpSrcIpv4Address (number): 
			EthernetDestination (str): 
			EthernetSource (str): 
			EthernetType (str): 
			Experimenter (number): 
			ExperimenterData (str): 
			ExperimenterDatalength (number): 
			GroupId (number): 
			Icmpv4Code (number): 
			Icmpv4Type (number): 
			Icmpv6Code (number): 
			Icmpv6Type (number): 
			IpDscp (str): 
			IpEcn (number): 
			IpProtocol (number): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			Ipv6Destination (str): 
			Ipv6ExtHeader (number): 
			Ipv6FlowLabel (number): 
			Ipv6NdSll (str): 
			Ipv6NdTarget (str): 
			Ipv6NdTll (str): 
			Ipv6Source (str): 
			MaxByteLength (number): 
			MplsBos (number): 
			MplsLabel (number): 
			MplsTc (number): 
			MplsTtl (number): 
			NetworkTtl (number): 
			OutputPort (number): 
			OutputPortType (str): 
			PbbIsid (number): 
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
			self: This instance with matching switchActionV131LearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchActionV131LearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchActionV131LearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
