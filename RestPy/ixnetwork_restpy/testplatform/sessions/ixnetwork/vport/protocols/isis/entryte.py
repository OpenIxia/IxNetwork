
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


class EntryTe(Base):
	"""The EntryTe class encapsulates a required entryTe node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EntryTe property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'entryTe'

	def __init__(self, parent):
		super(EntryTe, self).__init__(parent)

	@property
	def EnableEntryTe(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableEntryTe')
	@EnableEntryTe.setter
	def EnableEntryTe(self, value):
		self._set_attribute('enableEntryTe', value)

	@property
	def EteAdmGroup(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eteAdmGroup')
	@EteAdmGroup.setter
	def EteAdmGroup(self, value):
		self._set_attribute('eteAdmGroup', value)

	@property
	def EteLinkMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eteLinkMetric')
	@EteLinkMetric.setter
	def EteLinkMetric(self, value):
		self._set_attribute('eteLinkMetric', value)

	@property
	def EteMaxBandWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eteMaxBandWidth')
	@EteMaxBandWidth.setter
	def EteMaxBandWidth(self, value):
		self._set_attribute('eteMaxBandWidth', value)

	@property
	def EteMaxReserveBandWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eteMaxReserveBandWidth')
	@EteMaxReserveBandWidth.setter
	def EteMaxReserveBandWidth(self, value):
		self._set_attribute('eteMaxReserveBandWidth', value)

	@property
	def EteRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eteRouterId')
	@EteRouterId.setter
	def EteRouterId(self, value):
		self._set_attribute('eteRouterId', value)

	@property
	def EteRouterIdIncrement(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eteRouterIdIncrement')
	@EteRouterIdIncrement.setter
	def EteRouterIdIncrement(self, value):
		self._set_attribute('eteRouterIdIncrement', value)

	@property
	def EteUnreservedBandWidth(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('eteUnreservedBandWidth')
	@EteUnreservedBandWidth.setter
	def EteUnreservedBandWidth(self, value):
		self._set_attribute('eteUnreservedBandWidth', value)
