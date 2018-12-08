
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


class EthernetTrafficEndPoint(Base):
	"""The EthernetTrafficEndPoint class encapsulates a user managed ethernetTrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EthernetTrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ethernetTrafficEndPoint'

	def __init__(self, parent):
		super(EthernetTrafficEndPoint, self).__init__(parent)

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

	def add(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, EnableMacInMac=None, EnableVlan=None, GatewayMac=None, MacAddress=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new ethernetTrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			ArpViaInterface (bool): 
			CustomEtherHeaderLength (number): 
			CustomEtherHeaderValue (str): 
			CustomEtherType (str): 
			EnableMacInMac (bool): 
			EnableVlan (bool): 
			GatewayMac (str): 
			MacAddress (str): 
			Name (str): 
			PbbDestinamtionMac (str): 
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): 
			PbbIsId (str): 
			PbbSourceMac (str): 
			PbbVlanId (str): 
			PbbVlanPcp (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved ethernetTrafficEndPoint data using find and the newly added ethernetTrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ethernetTrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ArpViaInterface=None, CustomEtherHeaderLength=None, CustomEtherHeaderValue=None, CustomEtherType=None, EnableMacInMac=None, EnableVlan=None, GatewayMac=None, MacAddress=None, Name=None, PbbDestinamtionMac=None, PbbEtherType=None, PbbIsId=None, PbbSourceMac=None, PbbVlanId=None, PbbVlanPcp=None, ProtocolInterface=None, RangeSize=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves ethernetTrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve ethernetTrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all ethernetTrafficEndPoint data from the server.

		Args:
			ArpViaInterface (bool): 
			CustomEtherHeaderLength (number): 
			CustomEtherHeaderValue (str): 
			CustomEtherType (str): 
			EnableMacInMac (bool): 
			EnableVlan (bool): 
			GatewayMac (str): 
			MacAddress (str): 
			Name (str): 
			PbbDestinamtionMac (str): 
			PbbEtherType (str(bEtherType8100|bEtherType88A8|bEtherType88E7|bEtherType9100|bEtherType9200)): 
			PbbIsId (str): 
			PbbSourceMac (str): 
			PbbVlanId (str): 
			PbbVlanPcp (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			RangeSize (number): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching ethernetTrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ethernetTrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ethernetTrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
