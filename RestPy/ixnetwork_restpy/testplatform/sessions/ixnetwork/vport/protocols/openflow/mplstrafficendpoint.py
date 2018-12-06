
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


class MplsTrafficEndPoint(Base):
	"""The MplsTrafficEndPoint class encapsulates a user managed mplsTrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MplsTrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'mplsTrafficEndPoint'

	def __init__(self, parent):
		super(MplsTrafficEndPoint, self).__init__(parent)

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

	def add(self, ArpViaInterface=None, EnableVlan=None, GatewayMac=None, IpAddress=None, IpMask=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new mplsTrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): 
			EnableVlan (bool): 
			GatewayMac (str): 
			IpAddress (str): 
			IpMask (number): 
			Ipv4Dscp (str): 
			Ipv4Ecn (str): 
			Ipv6Address (str): 
			Ipv6AddressMask (number): 
			Ipv6Dscp (str): 
			Ipv6Ecn (str): 
			Ipv6FlowLabel (str): 
			MacAddress (str): 
			MplsInnerMacSource (str): 
			MplsInnerVlanId (str): 
			MplsInnerVlanPriority (str): 
			MplsLabel (str): 
			MplsLabelStackSize (number): 
			MplsPayloadType (str(ethernet|ipv4|ipv6)): 
			MplsTrafficClass (str): 
			Name (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved mplsTrafficEndPoint data using find and the newly added mplsTrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the mplsTrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, EnableVlan=None, GatewayMac=None, IpAddress=None, IpMask=None, Ipv4Dscp=None, Ipv4Ecn=None, Ipv6Address=None, Ipv6AddressMask=None, Ipv6Dscp=None, Ipv6Ecn=None, Ipv6FlowLabel=None, MacAddress=None, MplsInnerMacSource=None, MplsInnerVlanId=None, MplsInnerVlanPriority=None, MplsLabel=None, MplsLabelStackSize=None, MplsPayloadType=None, MplsTrafficClass=None, Name=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves mplsTrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve mplsTrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all mplsTrafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): 
			EnableVlan (bool): 
			GatewayMac (str): 
			IpAddress (str): 
			IpMask (number): 
			Ipv4Dscp (str): 
			Ipv4Ecn (str): 
			Ipv6Address (str): 
			Ipv6AddressMask (number): 
			Ipv6Dscp (str): 
			Ipv6Ecn (str): 
			Ipv6FlowLabel (str): 
			MacAddress (str): 
			MplsInnerMacSource (str): 
			MplsInnerVlanId (str): 
			MplsInnerVlanPriority (str): 
			MplsLabel (str): 
			MplsLabelStackSize (number): 
			MplsPayloadType (str(ethernet|ipv4|ipv6)): 
			MplsTrafficClass (str): 
			Name (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching mplsTrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of mplsTrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the mplsTrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
