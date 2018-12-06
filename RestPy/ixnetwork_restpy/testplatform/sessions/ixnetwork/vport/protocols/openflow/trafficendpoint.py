
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


class TrafficEndPoint(Base):
	"""The TrafficEndPoint class encapsulates a user managed trafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'trafficEndPoint'

	def __init__(self, parent):
		super(TrafficEndPoint, self).__init__(parent)

	@property
	def ArpViaInterface(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('arpViaInterface')
	@ArpViaInterface.setter
	def ArpViaInterface(self, value):
		self._set_attribute('arpViaInterface', value)

	@property
	def CustomEtherHeaderLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('customEtherHeaderLength')
	@CustomEtherHeaderLength.setter
	def CustomEtherHeaderLength(self, value):
		self._set_attribute('customEtherHeaderLength', value)

	@property
	def CustomEtherHeaderValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('customEtherHeaderValue')
	@CustomEtherHeaderValue.setter
	def CustomEtherHeaderValue(self, value):
		self._set_attribute('customEtherHeaderValue', value)

	@property
	def CustomEtherType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('customEtherType')
	@CustomEtherType.setter
	def CustomEtherType(self, value):
		self._set_attribute('customEtherType', value)

	@property
	def CustomIpHeaderLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('customIpHeaderLength')
	@CustomIpHeaderLength.setter
	def CustomIpHeaderLength(self, value):
		self._set_attribute('customIpHeaderLength', value)

	@property
	def CustomIpHeaderValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('customIpHeaderValue')
	@CustomIpHeaderValue.setter
	def CustomIpHeaderValue(self, value):
		self._set_attribute('customIpHeaderValue', value)

	@property
	def CustomIpProtocol(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('customIpProtocol')
	@CustomIpProtocol.setter
	def CustomIpProtocol(self, value):
		self._set_attribute('customIpProtocol', value)

	@property
	def DestinationPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationPort')
	@DestinationPort.setter
	def DestinationPort(self, value):
		self._set_attribute('destinationPort', value)

	@property
	def EnableMacInMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMacInMac')
	@EnableMacInMac.setter
	def EnableMacInMac(self, value):
		self._set_attribute('enableMacInMac', value)

	@property
	def EnableVlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def EtherType(self):
		"""

		Returns:
			str(custom|ipv4|ipv6|mplsUnicast)
		"""
		return self._get_attribute('etherType')
	@EtherType.setter
	def EtherType(self, value):
		self._set_attribute('etherType', value)

	@property
	def GatewayMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('gatewayMac')
	@GatewayMac.setter
	def GatewayMac(self, value):
		self._set_attribute('gatewayMac', value)

	@property
	def IpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipMask')
	@IpMask.setter
	def IpMask(self, value):
		self._set_attribute('ipMask', value)

	@property
	def IpProtocol(self):
		"""

		Returns:
			str(custom|tcp|udp)
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def IpTos(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipTos')
	@IpTos.setter
	def IpTos(self, value):
		self._set_attribute('ipTos', value)

	@property
	def Ipv4Dscp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Dscp')
	@Ipv4Dscp.setter
	def Ipv4Dscp(self, value):
		self._set_attribute('ipv4Dscp', value)

	@property
	def Ipv4Ecn(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Ecn')
	@Ipv4Ecn.setter
	def Ipv4Ecn(self, value):
		self._set_attribute('ipv4Ecn', value)

	@property
	def Ipv6Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Address')
	@Ipv6Address.setter
	def Ipv6Address(self, value):
		self._set_attribute('ipv6Address', value)

	@property
	def Ipv6AddressMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6AddressMask')
	@Ipv6AddressMask.setter
	def Ipv6AddressMask(self, value):
		self._set_attribute('ipv6AddressMask', value)

	@property
	def Ipv6CustomHeaderLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6CustomHeaderLength')
	@Ipv6CustomHeaderLength.setter
	def Ipv6CustomHeaderLength(self, value):
		self._set_attribute('ipv6CustomHeaderLength', value)

	@property
	def Ipv6CustomHeaderValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6CustomHeaderValue')
	@Ipv6CustomHeaderValue.setter
	def Ipv6CustomHeaderValue(self, value):
		self._set_attribute('ipv6CustomHeaderValue', value)

	@property
	def Ipv6CustomNextHeader(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6CustomNextHeader')
	@Ipv6CustomNextHeader.setter
	def Ipv6CustomNextHeader(self, value):
		self._set_attribute('ipv6CustomNextHeader', value)

	@property
	def Ipv6Dscp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Dscp')
	@Ipv6Dscp.setter
	def Ipv6Dscp(self, value):
		self._set_attribute('ipv6Dscp', value)

	@property
	def Ipv6Ecn(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6Ecn')
	@Ipv6Ecn.setter
	def Ipv6Ecn(self, value):
		self._set_attribute('ipv6Ecn', value)

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
	def Ipv6NextHeader(self):
		"""

		Returns:
			str(custom|tcp|udp)
		"""
		return self._get_attribute('ipv6NextHeader')
	@Ipv6NextHeader.setter
	def Ipv6NextHeader(self, value):
		self._set_attribute('ipv6NextHeader', value)

	@property
	def MacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MplsInnerMacSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerMacSource')
	@MplsInnerMacSource.setter
	def MplsInnerMacSource(self, value):
		self._set_attribute('mplsInnerMacSource', value)

	@property
	def MplsInnerVlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerVlanId')
	@MplsInnerVlanId.setter
	def MplsInnerVlanId(self, value):
		self._set_attribute('mplsInnerVlanId', value)

	@property
	def MplsInnerVlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsInnerVlanPriority')
	@MplsInnerVlanPriority.setter
	def MplsInnerVlanPriority(self, value):
		self._set_attribute('mplsInnerVlanPriority', value)

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
	def MplsLabelStackSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelStackSize')
	@MplsLabelStackSize.setter
	def MplsLabelStackSize(self, value):
		self._set_attribute('mplsLabelStackSize', value)

	@property
	def MplsPayloadType(self):
		"""

		Returns:
			str(ethernet|ipv4|ipv6)
		"""
		return self._get_attribute('mplsPayloadType')
	@MplsPayloadType.setter
	def MplsPayloadType(self, value):
		self._set_attribute('mplsPayloadType', value)

	@property
	def MplsTrafficClass(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mplsTrafficClass')
	@MplsTrafficClass.setter
	def MplsTrafficClass(self, value):
		self._set_attribute('mplsTrafficClass', value)

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PbbDestinamtionMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbDestinamtionMac')
	@PbbDestinamtionMac.setter
	def PbbDestinamtionMac(self, value):
		self._set_attribute('pbbDestinamtionMac', value)

	@property
	def PbbEtherType(self):
		"""

		Returns:
			str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)
		"""
		return self._get_attribute('pbbEtherType')
	@PbbEtherType.setter
	def PbbEtherType(self, value):
		self._set_attribute('pbbEtherType', value)

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
	def PbbSourceMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbSourceMac')
	@PbbSourceMac.setter
	def PbbSourceMac(self, value):
		self._set_attribute('pbbSourceMac', value)

	@property
	def PbbVlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbVlanId')
	@PbbVlanId.setter
	def PbbVlanId(self, value):
		self._set_attribute('pbbVlanId', value)

	@property
	def PbbVlanPcp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbVlanPcp')
	@PbbVlanPcp.setter
	def PbbVlanPcp(self, value):
		self._set_attribute('pbbVlanPcp', value)

	@property
	def ProtocolInterface(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def RangeSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rangeSize')
	@RangeSize.setter
	def RangeSize(self, value):
		self._set_attribute('rangeSize', value)

	@property
	def SourcePort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourcePort')
	@SourcePort.setter
	def SourcePort(self, value):
		self._set_attribute('sourcePort', value)

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
	def VlanCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

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
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, CustomIpHeaderLength=None, CustomIpHeaderValue=None, CustomIpProtocol=None, DestinationPort=None, EnableMacInMac=None, EnableVlan=None, EtherType=None, GatewayMac=None, IpAddress=None, IpMask=None, IpProtocol=None, IpTos=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6CustomHeaderLength=None, Ipv6CustomHeaderValue=None, Ipv6CustomNextHeader=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, Ipv6NextHeader=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new trafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): 
			CustomEtherHeaderLength (number): 
			CustomEtherHeaderValue (str): 
			CustomEtherType (str): 
			CustomIpHeaderLength (number): 
			CustomIpHeaderValue (str): 
			CustomIpProtocol (str): 
			DestinationPort (str): 
			EnableMacInMac (bool): 
			EnableVlan (bool): 
			EtherType (str(custom|ipv4|ipv6|mplsUnicast)): 
			GatewayMac (str): 
			IpAddress (str): 
			IpMask (number): 
			IpProtocol (str(custom|tcp|udp)): 
			IpTos (str): 
			Ipv4Dscp (str): 
			Ipv4Ecn (str): 
			Ipv6Address (str): 
			Ipv6AddressMask (number): 
			Ipv6CustomHeaderLength (number): 
			Ipv6CustomHeaderValue (str): 
			Ipv6CustomNextHeader (str): 
			Ipv6Dscp (str): 
			Ipv6Ecn (str): 
			Ipv6FlowLabel (str): 
			Ipv6NextHeader (str(custom|tcp|udp)): 
			MacAddress (str): 
			MplsInnerMacSource (str): 
			MplsInnerVlanId (str): 
			MplsInnerVlanPriority (str): 
			MplsLabel (str): 
			MplsLabelStackSize (number): 
			MplsPayloadType (str(ethernet|ipv4|ipv6)): 
			MplsTrafficClass (str): 
			Name (str): 
			PbbDestinamtionMac (str): 
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): 
			PbbIsId (str): 
			PbbSourceMac (str): 
			PbbVlanId (str): 
			PbbVlanPcp (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			SourcePort (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved trafficEndPoint data using find and the newly added trafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the trafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, CustomIpHeaderLength=None, CustomIpHeaderValue=None, CustomIpProtocol=None, DestinationPort=None, EnableMacInMac=None, EnableVlan=None, EtherType=None, GatewayMac=None, IpAddress=None, IpMask=None, IpProtocol=None, IpTos=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6CustomHeaderLength=None, Ipv6CustomHeaderValue=None, Ipv6CustomNextHeader=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, Ipv6NextHeader=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves trafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve trafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all trafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): 
			CustomEtherHeaderLength (number): 
			CustomEtherHeaderValue (str): 
			CustomEtherType (str): 
			CustomIpHeaderLength (number): 
			CustomIpHeaderValue (str): 
			CustomIpProtocol (str): 
			DestinationPort (str): 
			EnableMacInMac (bool): 
			EnableVlan (bool): 
			EtherType (str(custom|ipv4|ipv6|mplsUnicast)): 
			GatewayMac (str): 
			IpAddress (str): 
			IpMask (number): 
			IpProtocol (str(custom|tcp|udp)): 
			IpTos (str): 
			Ipv4Dscp (str): 
			Ipv4Ecn (str): 
			Ipv6Address (str): 
			Ipv6AddressMask (number): 
			Ipv6CustomHeaderLength (number): 
			Ipv6CustomHeaderValue (str): 
			Ipv6CustomNextHeader (str): 
			Ipv6Dscp (str): 
			Ipv6Ecn (str): 
			Ipv6FlowLabel (str): 
			Ipv6NextHeader (str(custom|tcp|udp)): 
			MacAddress (str): 
			MplsInnerMacSource (str): 
			MplsInnerVlanId (str): 
			MplsInnerVlanPriority (str): 
			MplsLabel (str): 
			MplsLabelStackSize (number): 
			MplsPayloadType (str(ethernet|ipv4|ipv6)): 
			MplsTrafficClass (str): 
			Name (str): 
			PbbDestinamtionMac (str): 
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): 
			PbbIsId (str): 
			PbbSourceMac (str): 
			PbbVlanId (str): 
			PbbVlanPcp (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			SourcePort (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching trafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
