
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


class MsAllowedEidRange(Base):
	"""The MsAllowedEidRange class encapsulates a user managed msAllowedEidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MsAllowedEidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'msAllowedEidRange'

	def __init__(self, parent):
		super(MsAllowedEidRange, self).__init__(parent)

	@property
	def Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('address')
	@Address.setter
	def Address(self, value):
		self._set_attribute('address', value)

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
	def Family(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('family')
	@Family.setter
	def Family(self, value):
		self._set_attribute('family', value)

	@property
	def PrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')
	@PrefixLength.setter
	def PrefixLength(self, value):
		self._set_attribute('prefixLength', value)

	def add(self, Address=None, Count=None, Enabled=None, Family=None, PrefixLength=None):
		"""Adds a new msAllowedEidRange node on the server and retrieves it in this instance.

		Args:
			Address (str): 
			Count (number): 
			Enabled (bool): 
			Family (str(ipv4|ipv6)): 
			PrefixLength (number): 

		Returns:
			self: This instance with all currently retrieved msAllowedEidRange data using find and the newly added msAllowedEidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the msAllowedEidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Address=None, Count=None, Enabled=None, Family=None, PrefixLength=None):
		"""Finds and retrieves msAllowedEidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve msAllowedEidRange data from the server.
		By default the find method takes no parameters and will retrieve all msAllowedEidRange data from the server.

		Args:
			Address (str): 
			Count (number): 
			Enabled (bool): 
			Family (str(ipv4|ipv6)): 
			PrefixLength (number): 

		Returns:
			self: This instance with matching msAllowedEidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of msAllowedEidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the msAllowedEidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
