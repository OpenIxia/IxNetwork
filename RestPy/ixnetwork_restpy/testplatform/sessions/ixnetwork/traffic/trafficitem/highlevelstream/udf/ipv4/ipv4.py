
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


class Ipv4(Base):
	"""The Ipv4 class encapsulates a system managed ipv4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4 property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4'

	def __init__(self, parent):
		super(Ipv4, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def BitmaskCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bitmaskCount')
	@BitmaskCount.setter
	def BitmaskCount(self, value):
		self._set_attribute('bitmaskCount', value)

	@property
	def InnerLoopIncrementBy(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('innerLoopIncrementBy')
	@InnerLoopIncrementBy.setter
	def InnerLoopIncrementBy(self, value):
		self._set_attribute('innerLoopIncrementBy', value)

	@property
	def InnerLoopLoopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('innerLoopLoopCount')
	@InnerLoopLoopCount.setter
	def InnerLoopLoopCount(self, value):
		self._set_attribute('innerLoopLoopCount', value)

	@property
	def OuterLoopLoopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outerLoopLoopCount')
	@OuterLoopLoopCount.setter
	def OuterLoopLoopCount(self, value):
		self._set_attribute('outerLoopLoopCount', value)

	@property
	def SkipValues(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('skipValues')
	@SkipValues.setter
	def SkipValues(self, value):
		self._set_attribute('skipValues', value)

	@property
	def StartValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def Width(self):
		"""

		Returns:
			str(32)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)

	def find(self, AvailableWidths=None, BitmaskCount=None, InnerLoopIncrementBy=None, InnerLoopLoopCount=None, OuterLoopLoopCount=None, SkipValues=None, StartValue=None, Width=None):
		"""Finds and retrieves ipv4 data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4 data from the server.
		By default the find method takes no parameters and will retrieve all ipv4 data from the server.

		Args:
			AvailableWidths (list(str)): 
			BitmaskCount (number): 
			InnerLoopIncrementBy (number): 
			InnerLoopLoopCount (number): 
			OuterLoopLoopCount (number): 
			SkipValues (bool): 
			StartValue (number): 
			Width (str(32)): 

		Returns:
			self: This instance with matching ipv4 data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4 data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4 data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
