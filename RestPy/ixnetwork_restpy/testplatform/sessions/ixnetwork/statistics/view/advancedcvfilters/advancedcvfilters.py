
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


class AdvancedCVFilters(Base):
	"""The AdvancedCVFilters class encapsulates a user managed advancedCVFilters node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdvancedCVFilters property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'advancedCVFilters'

	def __init__(self, parent):
		super(AdvancedCVFilters, self).__init__(parent)

	@property
	def AvailableFilterOptions(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('availableFilterOptions')

	@property
	def AvailableGroupingOptions(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('availableGroupingOptions')

	@property
	def Caption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def Expression(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('expression')
	@Expression.setter
	def Expression(self, value):
		self._set_attribute('expression', value)

	@property
	def Grouping(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('grouping')
	@Grouping.setter
	def Grouping(self, value):
		self._set_attribute('grouping', value)

	@property
	def Protocol(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('protocol')
	@Protocol.setter
	def Protocol(self, value):
		self._set_attribute('protocol', value)

	@property
	def SortingStats(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sortingStats')
	@SortingStats.setter
	def SortingStats(self, value):
		self._set_attribute('sortingStats', value)

	def add(self, Caption=None, Expression=None, Grouping=None, Protocol=None, SortingStats=None):
		"""Adds a new advancedCVFilters node on the server and retrieves it in this instance.

		Args:
			Caption (str): 
			Expression (str): 
			Grouping (str): 
			Protocol (str): 
			SortingStats (str): 

		Returns:
			self: This instance with all currently retrieved advancedCVFilters data using find and the newly added advancedCVFilters data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the advancedCVFilters data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AvailableFilterOptions=None, AvailableGroupingOptions=None, Caption=None, Expression=None, Grouping=None, Protocol=None, SortingStats=None):
		"""Finds and retrieves advancedCVFilters data from the server.

		All named parameters support regex and can be used to selectively retrieve advancedCVFilters data from the server.
		By default the find method takes no parameters and will retrieve all advancedCVFilters data from the server.

		Args:
			AvailableFilterOptions (str): 
			AvailableGroupingOptions (str): 
			Caption (str): 
			Expression (str): 
			Grouping (str): 
			Protocol (str): 
			SortingStats (str): 

		Returns:
			self: This instance with matching advancedCVFilters data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of advancedCVFilters data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the advancedCVFilters data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
