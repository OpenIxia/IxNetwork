
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


class DiscoveredNeighbor(Base):
	"""The DiscoveredNeighbor class encapsulates a user managed discoveredNeighbor node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DiscoveredNeighbor property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'discoveredNeighbor'

	def __init__(self, parent):
		super(DiscoveredNeighbor, self).__init__(parent)

	@property
	def IsRouter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('isRouter')

	@property
	def LastUpdate(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastUpdate')

	@property
	def NeighborIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighborIp')

	@property
	def NeighborMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('neighborMac')

	def add(self):
		"""Adds a new discoveredNeighbor node on the server and retrieves it in this instance.

		Returns:
			self: This instance with all currently retrieved discoveredNeighbor data using find and the newly added discoveredNeighbor data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the discoveredNeighbor data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IsRouter=None, LastUpdate=None, NeighborIp=None, NeighborMac=None):
		"""Finds and retrieves discoveredNeighbor data from the server.

		All named parameters support regex and can be used to selectively retrieve discoveredNeighbor data from the server.
		By default the find method takes no parameters and will retrieve all discoveredNeighbor data from the server.

		Args:
			IsRouter (str): 
			LastUpdate (str): 
			NeighborIp (str): 
			NeighborMac (str): 

		Returns:
			self: This instance with matching discoveredNeighbor data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of discoveredNeighbor data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the discoveredNeighbor data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
