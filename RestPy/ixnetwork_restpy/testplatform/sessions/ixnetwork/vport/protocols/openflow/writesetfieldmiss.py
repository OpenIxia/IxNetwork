
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


class WriteSetFieldMiss(Base):
	"""The WriteSetFieldMiss class encapsulates a required writeSetFieldMiss node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the WriteSetFieldMiss property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'writeSetFieldMiss'

	def __init__(self, parent):
		super(WriteSetFieldMiss, self).__init__(parent)

	@property
	def ArpDestinationHardwareAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('arpDestinationHardwareAddress')
	@ArpDestinationHardwareAddress.setter
	def ArpDestinationHardwareAddress(self, value):
		self._set_attribute('arpDestinationHardwareAddress', value)

	@property
	def ArpDestinationIpv4Address(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('arpDestinationIpv4Address')
	@ArpDestinationIpv4Address.setter
	def ArpDestinationIpv4Address(self, value):
		self._set_attribute('arpDestinationIpv4Address', value)

	@property
	def ArpOpcode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('arpOpcode')
	@ArpOpcode.setter
	def ArpOpcode(self, value):
		self._set_attribute('arpOpcode', value)

	@property
	def ArpSourceHardwareAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('arpSourceHardwareAddress')
	@ArpSourceHardwareAddress.setter
	def ArpSourceHardwareAddress(self, value):
		self._set_attribute('arpSourceHardwareAddress', value)

	@property
	def ArpSourceIpv4Address(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('arpSourceIpv4Address')
	@ArpSourceIpv4Address.setter
	def ArpSourceIpv4Address(self, value):
		self._set_attribute('arpSourceIpv4Address', value)

	@property
	def EthernetDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def EthernetType(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetType')
	@EthernetType.setter
	def EthernetType(self, value):
		self._set_attribute('ethernetType', value)

	@property
	def IcmpCode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('icmpCode')
	@IcmpCode.setter
	def IcmpCode(self, value):
		self._set_attribute('icmpCode', value)

	@property
	def IcmpType(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('icmpType')
	@IcmpType.setter
	def IcmpType(self, value):
		self._set_attribute('icmpType', value)

	@property
	def Icmpv6Code(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('icmpv6Code')
	@Icmpv6Code.setter
	def Icmpv6Code(self, value):
		self._set_attribute('icmpv6Code', value)

	@property
	def Icmpv6Type(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('icmpv6Type')
	@Icmpv6Type.setter
	def Icmpv6Type(self, value):
		self._set_attribute('icmpv6Type', value)

	@property
	def IpDscp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def IpEcn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipEcn')
	@IpEcn.setter
	def IpEcn(self, value):
		self._set_attribute('ipEcn', value)

	@property
	def IpProtocol(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Ipv6Destination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6Destination')
	@Ipv6Destination.setter
	def Ipv6Destination(self, value):
		self._set_attribute('ipv6Destination', value)

	@property
	def Ipv6ExtHeader(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6ExtHeader')
	@Ipv6ExtHeader.setter
	def Ipv6ExtHeader(self, value):
		self._set_attribute('ipv6ExtHeader', value)

	@property
	def Ipv6FlowLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6FlowLabel')
	@Ipv6FlowLabel.setter
	def Ipv6FlowLabel(self, value):
		self._set_attribute('ipv6FlowLabel', value)

	@property
	def Ipv6NdSll(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6NdSll')
	@Ipv6NdSll.setter
	def Ipv6NdSll(self, value):
		self._set_attribute('ipv6NdSll', value)

	@property
	def Ipv6NdTarget(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6NdTarget')
	@Ipv6NdTarget.setter
	def Ipv6NdTarget(self, value):
		self._set_attribute('ipv6NdTarget', value)

	@property
	def Ipv6NdTll(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6NdTll')
	@Ipv6NdTll.setter
	def Ipv6NdTll(self, value):
		self._set_attribute('ipv6NdTll', value)

	@property
	def Ipv6Source(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv6Source')
	@Ipv6Source.setter
	def Ipv6Source(self, value):
		self._set_attribute('ipv6Source', value)

	@property
	def MplsBos(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('mplsBos')
	@MplsBos.setter
	def MplsBos(self, value):
		self._set_attribute('mplsBos', value)

	@property
	def MplsLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('mplsLabel')
	@MplsLabel.setter
	def MplsLabel(self, value):
		self._set_attribute('mplsLabel', value)

	@property
	def MplsTc(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('mplsTc')
	@MplsTc.setter
	def MplsTc(self, value):
		self._set_attribute('mplsTc', value)

	@property
	def PbbIsid(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('pbbIsid')
	@PbbIsid.setter
	def PbbIsid(self, value):
		self._set_attribute('pbbIsid', value)

	@property
	def SctpDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sctpDestination')
	@SctpDestination.setter
	def SctpDestination(self, value):
		self._set_attribute('sctpDestination', value)

	@property
	def SctpSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sctpSource')
	@SctpSource.setter
	def SctpSource(self, value):
		self._set_attribute('sctpSource', value)

	@property
	def TcpDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tcpDestination')
	@TcpDestination.setter
	def TcpDestination(self, value):
		self._set_attribute('tcpDestination', value)

	@property
	def TcpSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tcpSource')
	@TcpSource.setter
	def TcpSource(self, value):
		self._set_attribute('tcpSource', value)

	@property
	def TunnelId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tunnelId')
	@TunnelId.setter
	def TunnelId(self, value):
		self._set_attribute('tunnelId', value)

	@property
	def UdpDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('udpDestination')
	@UdpDestination.setter
	def UdpDestination(self, value):
		self._set_attribute('udpDestination', value)

	@property
	def UdpSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('udpSource')
	@UdpSource.setter
	def UdpSource(self, value):
		self._set_attribute('udpSource', value)

	@property
	def VlanId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
