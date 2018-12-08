
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


class DynamicFrameSize(Base):
	"""The DynamicFrameSize class encapsulates a system managed dynamicFrameSize node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DynamicFrameSize property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'dynamicFrameSize'

	def __init__(self, parent):
		super(DynamicFrameSize, self).__init__(parent)

	@property
	def FixedSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fixedSize')
	@FixedSize.setter
	def FixedSize(self, value):
		self._set_attribute('fixedSize', value)

	@property
	def HighLevelStreamName(self):
		"""The name of the high level stream

		Returns:
			str
		"""
		return self._get_attribute('highLevelStreamName')

	@property
	def RandomMax(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('randomMax')
	@RandomMax.setter
	def RandomMax(self, value):
		self._set_attribute('randomMax', value)

	@property
	def RandomMin(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('randomMin')
	@RandomMin.setter
	def RandomMin(self, value):
		self._set_attribute('randomMin', value)

	@property
	def TrafficItemName(self):
		"""The name of the parent traffic item.

		Returns:
			str
		"""
		return self._get_attribute('trafficItemName')

	@property
	def Type(self):
		"""

		Returns:
			str(fixed|random)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def find(self, FixedSize=None, HighLevelStreamName=None, RandomMax=None, RandomMin=None, TrafficItemName=None, Type=None):
		"""Finds and retrieves dynamicFrameSize data from the server.

		All named parameters support regex and can be used to selectively retrieve dynamicFrameSize data from the server.
		By default the find method takes no parameters and will retrieve all dynamicFrameSize data from the server.

		Args:
			FixedSize (number): 
			HighLevelStreamName (str): The name of the high level stream
			RandomMax (number): 
			RandomMin (number): 
			TrafficItemName (str): The name of the parent traffic item.
			Type (str(fixed|random)): 

		Returns:
			self: This instance with matching dynamicFrameSize data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dynamicFrameSize data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dynamicFrameSize data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
