
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


class TxLane(Base):
	"""The TxLane class encapsulates a required txLane node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TxLane property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'txLane'

	def __init__(self, parent):
		super(TxLane, self).__init__(parent)

	@property
	def IsSkewSynchronized(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isSkewSynchronized')
	@IsSkewSynchronized.setter
	def IsSkewSynchronized(self, value):
		self._set_attribute('isSkewSynchronized', value)

	@property
	def LaneMappingType(self):
		"""

		Returns:
			str(custom|decrement|default|increment|random)
		"""
		return self._get_attribute('laneMappingType')
	@LaneMappingType.setter
	def LaneMappingType(self, value):
		self._set_attribute('laneMappingType', value)

	@property
	def MaxSkewVal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxSkewVal')

	@property
	def MinSkewVal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minSkewVal')

	@property
	def NoOfLanes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfLanes')

	@property
	def PcsLane(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('pcsLane')
	@PcsLane.setter
	def PcsLane(self, value):
		self._set_attribute('pcsLane', value)

	@property
	def PhysicalLanes(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('physicalLanes')

	@property
	def Resolution(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('resolution')

	@property
	def SkewValues(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('skewValues')
	@SkewValues.setter
	def SkewValues(self, value):
		self._set_attribute('skewValues', value)

	@property
	def SynchronizedSkewVal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('synchronizedSkewVal')
	@SynchronizedSkewVal.setter
	def SynchronizedSkewVal(self, value):
		self._set_attribute('synchronizedSkewVal', value)
