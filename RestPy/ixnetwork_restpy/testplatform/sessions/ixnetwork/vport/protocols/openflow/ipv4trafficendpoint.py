
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


class Ipv4TrafficEndPoint(Base):
	"""The Ipv4TrafficEndPoint class encapsulates a user managed ipv4TrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4TrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ipv4TrafficEndPoint'

	def __init__(self, parent):
		super(Ipv4TrafficEndPoint, self).__init__(parent)

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

	def add(self, ArpViaInterface=None, CustomIpHeaderLength=None, CustomIpHeaderValue=None, CustomIpProtocol=None, DestinationPort=None, EnableVlan=None, GatewayMac=None, IpAddress=None, IpMask=None, IpProtocol=None, Ipv4Dscp=None, Ipv4Ecn=None, MacAddress=None, Name=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new ipv4TrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): 
			CustomIpHeaderLength (number): 
			CustomIpHeaderValue (str): 
			CustomIpProtocol (str): 
			DestinationPort (str): 
			EnableVlan (bool): 
			GatewayMac (str): 
			IpAddress (str): 
			IpMask (number): 
			IpProtocol (str(custom|tcp|udp)): 
			Ipv4Dscp (str): 
			Ipv4Ecn (str): 
			MacAddress (str): 
			Name (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			SourcePort (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved ipv4TrafficEndPoint data using find and the newly added ipv4TrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ipv4TrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, CustomIpHeaderLength=None, CustomIpHeaderValue=None, CustomIpProtocol=None, DestinationPort=None, EnableVlan=None, GatewayMac=None, IpAddress=None, IpMask=None, IpProtocol=None, Ipv4Dscp=None, Ipv4Ecn=None, MacAddress=None, Name=None, ProtocolInterface=None, RangeSize=None, SourcePort=None, UdpDestination=None, UdpSource=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves ipv4TrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4TrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all ipv4TrafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): 
			CustomIpHeaderLength (number): 
			CustomIpHeaderValue (str): 
			CustomIpProtocol (str): 
			DestinationPort (str): 
			EnableVlan (bool): 
			GatewayMac (str): 
			IpAddress (str): 
			IpMask (number): 
			IpProtocol (str(custom|tcp|udp)): 
			Ipv4Dscp (str): 
			Ipv4Ecn (str): 
			MacAddress (str): 
			Name (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			SourcePort (str): 
			UdpDestination (str): 
			UdpSource (str): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching ipv4TrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4TrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4TrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
