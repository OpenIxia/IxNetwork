
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


class MacAddressRange(Base):
	"""The MacAddressRange class encapsulates a user managed macAddressRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MacAddressRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'macAddressRange'

	def __init__(self, parent):
		super(MacAddressRange, self).__init__(parent)

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
	def IncrementVlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('incrementVlan')
	@IncrementVlan.setter
	def IncrementVlan(self, value):
		self._set_attribute('incrementVlan', value)

	@property
	def IncrementVlanMode(self):
		"""

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementVlanMode')
	@IncrementVlanMode.setter
	def IncrementVlanMode(self, value):
		self._set_attribute('incrementVlanMode', value)

	@property
	def IncremetVlanMode(self):
		"""

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incremetVlanMode')
	@IncremetVlanMode.setter
	def IncremetVlanMode(self, value):
		self._set_attribute('incremetVlanMode', value)

	@property
	def MacCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('macCount')
	@MacCount.setter
	def MacCount(self, value):
		self._set_attribute('macCount', value)

	@property
	def MacCountPerL2Site(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('macCountPerL2Site')
	@MacCountPerL2Site.setter
	def MacCountPerL2Site(self, value):
		self._set_attribute('macCountPerL2Site', value)

	@property
	def MacIncrement(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('macIncrement')
	@MacIncrement.setter
	def MacIncrement(self, value):
		self._set_attribute('macIncrement', value)

	@property
	def SkipVlanIdZero(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('skipVlanIdZero')
	@SkipVlanIdZero.setter
	def SkipVlanIdZero(self, value):
		self._set_attribute('skipVlanIdZero', value)

	@property
	def StartMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startMacAddress')
	@StartMacAddress.setter
	def StartMacAddress(self, value):
		self._set_attribute('startMacAddress', value)

	@property
	def TotalMacCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalMacCount')

	@property
	def Tpid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tpid')
	@Tpid.setter
	def Tpid(self, value):
		self._set_attribute('tpid', value)

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

	def add(self, EnableVlan=None, Enabled=None, IncrementVlan=None, IncrementVlanMode=None, IncremetVlanMode=None, MacCount=None, MacCountPerL2Site=None, MacIncrement=None, SkipVlanIdZero=None, StartMacAddress=None, Tpid=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new macAddressRange node on the server and retrieves it in this instance.

		Args:
			EnableVlan (bool): 
			Enabled (bool): 
			IncrementVlan (bool): 
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			MacCount (number): 
			MacCountPerL2Site (number): 
			MacIncrement (bool): 
			SkipVlanIdZero (bool): 
			StartMacAddress (str): 
			Tpid (str): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved macAddressRange data using find and the newly added macAddressRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the macAddressRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableVlan=None, Enabled=None, IncrementVlan=None, IncrementVlanMode=None, IncremetVlanMode=None, MacCount=None, MacCountPerL2Site=None, MacIncrement=None, SkipVlanIdZero=None, StartMacAddress=None, TotalMacCount=None, Tpid=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves macAddressRange data from the server.

		All named parameters support regex and can be used to selectively retrieve macAddressRange data from the server.
		By default the find method takes no parameters and will retrieve all macAddressRange data from the server.

		Args:
			EnableVlan (bool): 
			Enabled (bool): 
			IncrementVlan (bool): 
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			MacCount (number): 
			MacCountPerL2Site (number): 
			MacIncrement (bool): 
			SkipVlanIdZero (bool): 
			StartMacAddress (str): 
			TotalMacCount (number): 
			Tpid (str): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching macAddressRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of macAddressRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the macAddressRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
