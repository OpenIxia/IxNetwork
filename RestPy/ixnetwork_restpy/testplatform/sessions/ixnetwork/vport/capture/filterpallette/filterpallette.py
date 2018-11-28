
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


class FilterPallette(Base):
	"""The FilterPallette class encapsulates a required filterPallette node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FilterPallette property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'filterPallette'

	def __init__(self, parent):
		super(FilterPallette, self).__init__(parent)

	@property
	def DA1(self):
		"""Only frames that contain this destination MAC address are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('DA1')
	@DA1.setter
	def DA1(self, value):
		self._set_attribute('DA1', value)

	@property
	def DA2(self):
		"""Only frames that contain this destination MAC address are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('DA2')
	@DA2.setter
	def DA2(self, value):
		self._set_attribute('DA2', value)

	@property
	def DAMask1(self):
		"""Only frames that contain this destination MAC address are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('DAMask1')
	@DAMask1.setter
	def DAMask1(self, value):
		self._set_attribute('DAMask1', value)

	@property
	def DAMask2(self):
		"""A bit mask that allows the user to specify which bits of the DA2 should be used when filtering. If the mask bit is set high, the pattern bit will be used in the filter

		Returns:
			str
		"""
		return self._get_attribute('DAMask2')
	@DAMask2.setter
	def DAMask2(self, value):
		self._set_attribute('DAMask2', value)

	@property
	def SA1(self):
		"""Only frames that contain this source MAC address are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('SA1')
	@SA1.setter
	def SA1(self, value):
		self._set_attribute('SA1', value)

	@property
	def SA2(self):
		"""Only frames that contain this source MAC address are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('SA2')
	@SA2.setter
	def SA2(self, value):
		self._set_attribute('SA2', value)

	@property
	def SAMask1(self):
		"""A bit mask that allows the user to specify which bits of the SA1 should be used when filtering. If the mask bit is set high, the pattern bit will be used in the filter.

		Returns:
			str
		"""
		return self._get_attribute('SAMask1')
	@SAMask1.setter
	def SAMask1(self, value):
		self._set_attribute('SAMask1', value)

	@property
	def SAMask2(self):
		"""A bit mask that allows the user to specify which bits of the SA2 should be used when filtering. If the mask bit is set high, the pattern bit will be used in the filter

		Returns:
			str
		"""
		return self._get_attribute('SAMask2')
	@SAMask2.setter
	def SAMask2(self, value):
		self._set_attribute('SAMask2', value)

	@property
	def Pattern1(self):
		"""Only frames that contain this pattern at offset patternOffset1 are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('pattern1')
	@Pattern1.setter
	def Pattern1(self, value):
		self._set_attribute('pattern1', value)

	@property
	def Pattern2(self):
		"""Only frames that contain this pattern at offset patternOffset2 are filtered, captured or counted.

		Returns:
			str
		"""
		return self._get_attribute('pattern2')
	@Pattern2.setter
	def Pattern2(self, value):
		self._set_attribute('pattern2', value)

	@property
	def PatternMask1(self):
		"""A bit mask that allows the user to specify which bits of pattern1 should be used when filtering. If the mask bit is set low, the pattern bit will be used in the filter.

		Returns:
			str
		"""
		return self._get_attribute('patternMask1')
	@PatternMask1.setter
	def PatternMask1(self, value):
		self._set_attribute('patternMask1', value)

	@property
	def PatternMask2(self):
		"""A bit mask that allows the user to specify which bits of pattern2 should be used when filtering. If the mask bit is set high, the pattern bit will be used in the filter.

		Returns:
			str
		"""
		return self._get_attribute('patternMask2')
	@PatternMask2.setter
	def PatternMask2(self, value):
		self._set_attribute('patternMask2', value)

	@property
	def PatternOffset1(self):
		"""Offset of pattern1 in the frame to be filtered, captured or counted.

		Returns:
			number
		"""
		return self._get_attribute('patternOffset1')
	@PatternOffset1.setter
	def PatternOffset1(self, value):
		self._set_attribute('patternOffset1', value)

	@property
	def PatternOffset2(self):
		"""Offset of pattern2 in the frame to be filtered, captured or counted.

		Returns:
			number
		"""
		return self._get_attribute('patternOffset2')
	@PatternOffset2.setter
	def PatternOffset2(self, value):
		self._set_attribute('patternOffset2', value)

	@property
	def PatternOffsetType1(self):
		"""For ports that support the portFeaturePatternOffsetFlexible feature, this option specifies the place that patternOffset1 is relative to.

		Returns:
			str(filterPalletteOffsetStartOfFrame|filterPalletteOffsetStartOfIp|filterPalletteOffsetStartOfProtocol)
		"""
		return self._get_attribute('patternOffsetType1')
	@PatternOffsetType1.setter
	def PatternOffsetType1(self, value):
		self._set_attribute('patternOffsetType1', value)

	@property
	def PatternOffsetType2(self):
		"""For ports that support the portFeaturePatternOffsetFlexible feature, this option specifies the place that patternOffset1 is relative to.

		Returns:
			str(filterPalletteOffsetStartOfFrame|filterPalletteOffsetStartOfIp|filterPalletteOffsetStartOfProtocol)
		"""
		return self._get_attribute('patternOffsetType2')
	@PatternOffsetType2.setter
	def PatternOffsetType2(self, value):
		self._set_attribute('patternOffsetType2', value)
