
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


class MulticastReceiverSite(Base):
	"""The MulticastReceiverSite class encapsulates a user managed multicastReceiverSite node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastReceiverSite property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastReceiverSite'

	def __init__(self, parent):
		super(MulticastReceiverSite, self).__init__(parent)

	@property
	def AddressFamilyType(self):
		"""

		Returns:
			str(addressFamilyIpv4|addressFamilyIpv6)
		"""
		return self._get_attribute('addressFamilyType')
	@AddressFamilyType.setter
	def AddressFamilyType(self, value):
		self._set_attribute('addressFamilyType', value)

	@property
	def CMcastRouteType(self):
		"""

		Returns:
			str(sourceTreeJoin|sharedTreeJoin)
		"""
		return self._get_attribute('cMcastRouteType')
	@CMcastRouteType.setter
	def CMcastRouteType(self, value):
		self._set_attribute('cMcastRouteType', value)

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
	def GroupAddressCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupAddressCount')
	@GroupAddressCount.setter
	def GroupAddressCount(self, value):
		self._set_attribute('groupAddressCount', value)

	@property
	def GroupMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupMaskWidth')
	@GroupMaskWidth.setter
	def GroupMaskWidth(self, value):
		self._set_attribute('groupMaskWidth', value)

	@property
	def SendTriggeredCmulticastRoute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendTriggeredCmulticastRoute')
	@SendTriggeredCmulticastRoute.setter
	def SendTriggeredCmulticastRoute(self, value):
		self._set_attribute('sendTriggeredCmulticastRoute', value)

	@property
	def SourceAddressCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceAddressCount')
	@SourceAddressCount.setter
	def SourceAddressCount(self, value):
		self._set_attribute('sourceAddressCount', value)

	@property
	def SourceGroupMapping(self):
		"""

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('sourceGroupMapping')
	@SourceGroupMapping.setter
	def SourceGroupMapping(self, value):
		self._set_attribute('sourceGroupMapping', value)

	@property
	def SourceMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceMaskWidth')
	@SourceMaskWidth.setter
	def SourceMaskWidth(self, value):
		self._set_attribute('sourceMaskWidth', value)

	@property
	def StartGroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startGroupAddress')
	@StartGroupAddress.setter
	def StartGroupAddress(self, value):
		self._set_attribute('startGroupAddress', value)

	@property
	def StartSourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startSourceAddress')
	@StartSourceAddress.setter
	def StartSourceAddress(self, value):
		self._set_attribute('startSourceAddress', value)

	@property
	def SupportLeafAdRoutesSending(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportLeafAdRoutesSending')
	@SupportLeafAdRoutesSending.setter
	def SupportLeafAdRoutesSending(self, value):
		self._set_attribute('supportLeafAdRoutesSending', value)

	def add(self, AddressFamilyType=None, CMcastRouteType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, SendTriggeredCmulticastRoute=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, SupportLeafAdRoutesSending=None):
		"""Adds a new multicastReceiverSite node on the server and retrieves it in this instance.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): 
			CMcastRouteType (str(sourceTreeJoin|sharedTreeJoin)): 
			Enabled (bool): 
			GroupAddressCount (number): 
			GroupMaskWidth (number): 
			SendTriggeredCmulticastRoute (bool): 
			SourceAddressCount (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne)): 
			SourceMaskWidth (number): 
			StartGroupAddress (str): 
			StartSourceAddress (str): 
			SupportLeafAdRoutesSending (bool): 

		Returns:
			self: This instance with all currently retrieved multicastReceiverSite data using find and the newly added multicastReceiverSite data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastReceiverSite data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddressFamilyType=None, CMcastRouteType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, SendTriggeredCmulticastRoute=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, SupportLeafAdRoutesSending=None):
		"""Finds and retrieves multicastReceiverSite data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastReceiverSite data from the server.
		By default the find method takes no parameters and will retrieve all multicastReceiverSite data from the server.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): 
			CMcastRouteType (str(sourceTreeJoin|sharedTreeJoin)): 
			Enabled (bool): 
			GroupAddressCount (number): 
			GroupMaskWidth (number): 
			SendTriggeredCmulticastRoute (bool): 
			SourceAddressCount (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne)): 
			SourceMaskWidth (number): 
			StartGroupAddress (str): 
			StartSourceAddress (str): 
			SupportLeafAdRoutesSending (bool): 

		Returns:
			self: This instance with matching multicastReceiverSite data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastReceiverSite data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastReceiverSite data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
