
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


class RangeTe(Base):
	"""The RangeTe class encapsulates a required rangeTe node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RangeTe property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rangeTe'

	def __init__(self, parent):
		super(RangeTe, self).__init__(parent)

	@property
	def EnableRangeTe(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRangeTe')
	@EnableRangeTe.setter
	def EnableRangeTe(self, value):
		self._set_attribute('enableRangeTe', value)

	@property
	def TeAdmGroup(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('teAdmGroup')
	@TeAdmGroup.setter
	def TeAdmGroup(self, value):
		self._set_attribute('teAdmGroup', value)

	@property
	def TeLinkMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('teLinkMetric')
	@TeLinkMetric.setter
	def TeLinkMetric(self, value):
		self._set_attribute('teLinkMetric', value)

	@property
	def TeMaxBandWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('teMaxBandWidth')
	@TeMaxBandWidth.setter
	def TeMaxBandWidth(self, value):
		self._set_attribute('teMaxBandWidth', value)

	@property
	def TeMaxReserveBandWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('teMaxReserveBandWidth')
	@TeMaxReserveBandWidth.setter
	def TeMaxReserveBandWidth(self, value):
		self._set_attribute('teMaxReserveBandWidth', value)

	@property
	def TeRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('teRouterId')
	@TeRouterId.setter
	def TeRouterId(self, value):
		self._set_attribute('teRouterId', value)

	@property
	def TeRouterIdIncrement(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('teRouterIdIncrement')
	@TeRouterIdIncrement.setter
	def TeRouterIdIncrement(self, value):
		self._set_attribute('teRouterIdIncrement', value)

	@property
	def TeUnreservedBandWidth(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('teUnreservedBandWidth')
	@TeUnreservedBandWidth.setter
	def TeUnreservedBandWidth(self, value):
		self._set_attribute('teUnreservedBandWidth', value)
