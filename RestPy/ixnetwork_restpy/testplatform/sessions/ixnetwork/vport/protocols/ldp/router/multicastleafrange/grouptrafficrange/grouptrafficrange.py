
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


class GroupTrafficRange(Base):
	"""The GroupTrafficRange class encapsulates a user managed groupTrafficRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupTrafficRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'groupTrafficRange'

	def __init__(self, parent):
		super(GroupTrafficRange, self).__init__(parent)

	@property
	def AddrFamilyType(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('addrFamilyType')
	@AddrFamilyType.setter
	def AddrFamilyType(self, value):
		self._set_attribute('addrFamilyType', value)

	@property
	def GrpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('grpAddress')
	@GrpAddress.setter
	def GrpAddress(self, value):
		self._set_attribute('grpAddress', value)

	@property
	def GrpCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('grpCount')
	@GrpCount.setter
	def GrpCount(self, value):
		self._set_attribute('grpCount', value)

	def add(self, AddrFamilyType=None, GrpAddress=None, GrpCount=None):
		"""Adds a new groupTrafficRange node on the server and retrieves it in this instance.

		Args:
			AddrFamilyType (str(ipv4|ipv6)): 
			GrpAddress (str): 
			GrpCount (number): 

		Returns:
			self: This instance with all currently retrieved groupTrafficRange data using find and the newly added groupTrafficRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the groupTrafficRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddrFamilyType=None, GrpAddress=None, GrpCount=None):
		"""Finds and retrieves groupTrafficRange data from the server.

		All named parameters support regex and can be used to selectively retrieve groupTrafficRange data from the server.
		By default the find method takes no parameters and will retrieve all groupTrafficRange data from the server.

		Args:
			AddrFamilyType (str(ipv4|ipv6)): 
			GrpAddress (str): 
			GrpCount (number): 

		Returns:
			self: This instance with matching groupTrafficRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupTrafficRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupTrafficRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
