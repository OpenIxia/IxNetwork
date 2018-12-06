
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


class OpaqueRouteRange(Base):
	"""The OpaqueRouteRange class encapsulates a user managed opaqueRouteRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpaqueRouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'opaqueRouteRange'

	def __init__(self, parent):
		super(OpaqueRouteRange, self).__init__(parent)

	@property
	def __id__(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('__id__')
	@__id__.setter
	def __id__(self, value):
		self._set_attribute('__id__', value)

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
	def ImportedFile(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('importedFile')
	@ImportedFile.setter
	def ImportedFile(self, value):
		self._set_attribute('importedFile', value)

	@property
	def NextHopAsIs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('nextHopAsIs')
	@NextHopAsIs.setter
	def NextHopAsIs(self, value):
		self._set_attribute('nextHopAsIs', value)

	@property
	def NumberOfRoutes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoutes')
	@NumberOfRoutes.setter
	def NumberOfRoutes(self, value):
		self._set_attribute('numberOfRoutes', value)

	@property
	def SendMultiExitDiscovery(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendMultiExitDiscovery')
	@SendMultiExitDiscovery.setter
	def SendMultiExitDiscovery(self, value):
		self._set_attribute('sendMultiExitDiscovery', value)

	@property
	def Status(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('status')

	def add(self, __id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None):
		"""Adds a new opaqueRouteRange node on the server and retrieves it in this instance.

		Args:
			__id__ (str): 
			Enabled (bool): 
			ImportedFile (str): 
			NextHopAsIs (bool): 
			NumberOfRoutes (number): 
			SendMultiExitDiscovery (bool): 

		Returns:
			self: This instance with all currently retrieved opaqueRouteRange data using find and the newly added opaqueRouteRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the opaqueRouteRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, __id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None, Status=None):
		"""Finds and retrieves opaqueRouteRange data from the server.

		All named parameters support regex and can be used to selectively retrieve opaqueRouteRange data from the server.
		By default the find method takes no parameters and will retrieve all opaqueRouteRange data from the server.

		Args:
			__id__ (str): 
			Enabled (bool): 
			ImportedFile (str): 
			NextHopAsIs (bool): 
			NumberOfRoutes (number): 
			SendMultiExitDiscovery (bool): 
			Status (str): 

		Returns:
			self: This instance with matching opaqueRouteRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of opaqueRouteRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the opaqueRouteRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ApplyOpaqueRouteRange(self):
		"""Executes the applyOpaqueRouteRange operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=opaqueRouteRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ApplyOpaqueRouteRange', payload=locals(), response_object=None)
