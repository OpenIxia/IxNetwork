
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


class ExperimenterMissLearnedInfo(Base):
	"""The ExperimenterMissLearnedInfo class encapsulates a user managed experimenterMissLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ExperimenterMissLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'experimenterMissLearnedInfo'

	def __init__(self, parent):
		super(ExperimenterMissLearnedInfo, self).__init__(parent)

	@property
	def ExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def ExperimenterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterId')

	@property
	def NextTableIds(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextTableIds')

	@property
	def Property(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('property')

	@property
	def SupportedField(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('supportedField')

	def add(self):
		"""Adds a new experimenterMissLearnedInfo node on the server and retrieves it in this instance.

		Returns:
			self: This instance with all currently retrieved experimenterMissLearnedInfo data using find and the newly added experimenterMissLearnedInfo data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the experimenterMissLearnedInfo data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterId=None, NextTableIds=None, Property=None, SupportedField=None):
		"""Finds and retrieves experimenterMissLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve experimenterMissLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all experimenterMissLearnedInfo data from the server.

		Args:
			ExperimenterData (str): 
			ExperimenterDataLength (number): 
			ExperimenterId (number): 
			NextTableIds (str): 
			Property (str): 
			SupportedField (str): 

		Returns:
			self: This instance with matching experimenterMissLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of experimenterMissLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the experimenterMissLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
