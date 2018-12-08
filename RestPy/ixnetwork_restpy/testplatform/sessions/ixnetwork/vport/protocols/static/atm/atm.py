
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


class Atm(Base):
	"""The Atm class encapsulates a user managed atm node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Atm property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'atm'

	def __init__(self, parent):
		super(Atm, self).__init__(parent)

	@property
	def AtmEncapsulation(self):
		"""

		Returns:
			str(llcRoutedSnap|llcBridged802p3WithFcs|llcBridged802p3WithOutFcs|ppp|vcMultiplexedPpp|vcMultiRouted|vcMultiBridged802p3WithFcs|vcMultiBridged802p3WithOutFcs)
		"""
		return self._get_attribute('atmEncapsulation')
	@AtmEncapsulation.setter
	def AtmEncapsulation(self, value):
		self._set_attribute('atmEncapsulation', value)

	@property
	def Count(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

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
	def IncrementVci(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('incrementVci')
	@IncrementVci.setter
	def IncrementVci(self, value):
		self._set_attribute('incrementVci', value)

	@property
	def IncrementVpi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('incrementVpi')
	@IncrementVpi.setter
	def IncrementVpi(self, value):
		self._set_attribute('incrementVpi', value)

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
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def Vci(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vci')
	@Vci.setter
	def Vci(self, value):
		self._set_attribute('vci', value)

	@property
	def Vpi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vpi')
	@Vpi.setter
	def Vpi(self, value):
		self._set_attribute('vpi', value)

	def add(self, AtmEncapsulation=None, Count=None, Enabled=None, IncrementVci=None, IncrementVpi=None, Name=None, TrafficGroupId=None, Vci=None, Vpi=None):
		"""Adds a new atm node on the server and retrieves it in this instance.

		Args:
			AtmEncapsulation (str(llcRoutedSnap|llcBridged802p3WithFcs|llcBridged802p3WithOutFcs|ppp|vcMultiplexedPpp|vcMultiRouted|vcMultiBridged802p3WithFcs|vcMultiBridged802p3WithOutFcs)): 
			Count (number): 
			Enabled (bool): 
			IncrementVci (number): 
			IncrementVpi (number): 
			Name (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			Vci (number): 
			Vpi (number): 

		Returns:
			self: This instance with all currently retrieved atm data using find and the newly added atm data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the atm data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AtmEncapsulation=None, Count=None, Enabled=None, IncrementVci=None, IncrementVpi=None, Name=None, TrafficGroupId=None, Vci=None, Vpi=None):
		"""Finds and retrieves atm data from the server.

		All named parameters support regex and can be used to selectively retrieve atm data from the server.
		By default the find method takes no parameters and will retrieve all atm data from the server.

		Args:
			AtmEncapsulation (str(llcRoutedSnap|llcBridged802p3WithFcs|llcBridged802p3WithOutFcs|ppp|vcMultiplexedPpp|vcMultiRouted|vcMultiBridged802p3WithFcs|vcMultiBridged802p3WithOutFcs)): 
			Count (number): 
			Enabled (bool): 
			IncrementVci (number): 
			IncrementVpi (number): 
			Name (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			Vci (number): 
			Vpi (number): 

		Returns:
			self: This instance with matching atm data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of atm data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the atm data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
