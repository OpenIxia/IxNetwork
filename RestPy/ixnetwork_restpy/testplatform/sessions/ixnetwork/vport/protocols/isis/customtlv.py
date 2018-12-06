
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


class CustomTlv(Base):
	"""The CustomTlv class encapsulates a user managed customTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTlv'

	def __init__(self, parent):
		super(CustomTlv, self).__init__(parent)

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
	def IncludeInHello(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeInHello')
	@IncludeInHello.setter
	def IncludeInHello(self, value):
		self._set_attribute('includeInHello', value)

	@property
	def IncludeInLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeInLsp')
	@IncludeInLsp.setter
	def IncludeInLsp(self, value):
		self._set_attribute('includeInLsp', value)

	@property
	def IncludeInNetworkRange(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeInNetworkRange')
	@IncludeInNetworkRange.setter
	def IncludeInNetworkRange(self, value):
		self._set_attribute('includeInNetworkRange', value)

	@property
	def Length(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('length')
	@Length.setter
	def Length(self, value):
		self._set_attribute('length', value)

	@property
	def Type(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def Value(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Enabled=None, IncludeInHello=None, IncludeInLsp=None, IncludeInNetworkRange=None, Length=None, Type=None, Value=None):
		"""Adds a new customTlv node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			IncludeInHello (bool): 
			IncludeInLsp (bool): 
			IncludeInNetworkRange (bool): 
			Length (number): 
			Type (number): 
			Value (str): 

		Returns:
			self: This instance with all currently retrieved customTlv data using find and the newly added customTlv data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTlv data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, IncludeInHello=None, IncludeInLsp=None, IncludeInNetworkRange=None, Length=None, Type=None, Value=None):
		"""Finds and retrieves customTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve customTlv data from the server.
		By default the find method takes no parameters and will retrieve all customTlv data from the server.

		Args:
			Enabled (bool): 
			IncludeInHello (bool): 
			IncludeInLsp (bool): 
			IncludeInNetworkRange (bool): 
			Length (number): 
			Type (number): 
			Value (str): 

		Returns:
			self: This instance with matching customTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
