
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


class FilterPalette(Base):
	"""The FilterPalette class encapsulates a required filterPalette node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FilterPalette property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'filterPalette'

	def __init__(self, parent):
		super(FilterPalette, self).__init__(parent)

	@property
	def DestinationAddress1(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationAddress1')
	@DestinationAddress1.setter
	def DestinationAddress1(self, value):
		self._set_attribute('destinationAddress1', value)

	@property
	def DestinationAddress1Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationAddress1Mask')
	@DestinationAddress1Mask.setter
	def DestinationAddress1Mask(self, value):
		self._set_attribute('destinationAddress1Mask', value)

	@property
	def DestinationAddress2(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationAddress2')
	@DestinationAddress2.setter
	def DestinationAddress2(self, value):
		self._set_attribute('destinationAddress2', value)

	@property
	def DestinationAddress2Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationAddress2Mask')
	@DestinationAddress2Mask.setter
	def DestinationAddress2Mask(self, value):
		self._set_attribute('destinationAddress2Mask', value)

	@property
	def Pattern1(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pattern1')
	@Pattern1.setter
	def Pattern1(self, value):
		self._set_attribute('pattern1', value)

	@property
	def Pattern1Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pattern1Mask')
	@Pattern1Mask.setter
	def Pattern1Mask(self, value):
		self._set_attribute('pattern1Mask', value)

	@property
	def Pattern1Offset(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pattern1Offset')
	@Pattern1Offset.setter
	def Pattern1Offset(self, value):
		self._set_attribute('pattern1Offset', value)

	@property
	def Pattern1OffsetType(self):
		"""

		Returns:
			str(fromStartOfFrame|fromStartOfIp|fromStartOfProtocol|fromStartOfSonet)
		"""
		return self._get_attribute('pattern1OffsetType')
	@Pattern1OffsetType.setter
	def Pattern1OffsetType(self, value):
		self._set_attribute('pattern1OffsetType', value)

	@property
	def Pattern2(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pattern2')
	@Pattern2.setter
	def Pattern2(self, value):
		self._set_attribute('pattern2', value)

	@property
	def Pattern2Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pattern2Mask')
	@Pattern2Mask.setter
	def Pattern2Mask(self, value):
		self._set_attribute('pattern2Mask', value)

	@property
	def Pattern2Offset(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pattern2Offset')
	@Pattern2Offset.setter
	def Pattern2Offset(self, value):
		self._set_attribute('pattern2Offset', value)

	@property
	def Pattern2OffsetType(self):
		"""

		Returns:
			str(fromStartOfFrame|fromStartOfIp|fromStartOfProtocol|fromStartOfSonet)
		"""
		return self._get_attribute('pattern2OffsetType')
	@Pattern2OffsetType.setter
	def Pattern2OffsetType(self, value):
		self._set_attribute('pattern2OffsetType', value)

	@property
	def SourceAddress1(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress1')
	@SourceAddress1.setter
	def SourceAddress1(self, value):
		self._set_attribute('sourceAddress1', value)

	@property
	def SourceAddress1Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress1Mask')
	@SourceAddress1Mask.setter
	def SourceAddress1Mask(self, value):
		self._set_attribute('sourceAddress1Mask', value)

	@property
	def SourceAddress2(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress2')
	@SourceAddress2.setter
	def SourceAddress2(self, value):
		self._set_attribute('sourceAddress2', value)

	@property
	def SourceAddress2Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress2Mask')
	@SourceAddress2Mask.setter
	def SourceAddress2Mask(self, value):
		self._set_attribute('sourceAddress2Mask', value)
