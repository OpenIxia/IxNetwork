
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


class AccumulateAndBurst(Base):
	"""The AccumulateAndBurst class encapsulates a required accumulateAndBurst node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AccumulateAndBurst property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'accumulateAndBurst'

	def __init__(self, parent):
		super(AccumulateAndBurst, self).__init__(parent)

	@property
	def BurstSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('burstSize')
	@BurstSize.setter
	def BurstSize(self, value):
		self._set_attribute('burstSize', value)

	@property
	def BurstSizeUnit(self):
		"""

		Returns:
			str(kilobytes|kKilobytes|kMegabytes|megabytes)
		"""
		return self._get_attribute('burstSizeUnit')
	@BurstSizeUnit.setter
	def BurstSizeUnit(self, value):
		self._set_attribute('burstSizeUnit', value)

	@property
	def BurstTimeout(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('burstTimeout')
	@BurstTimeout.setter
	def BurstTimeout(self, value):
		self._set_attribute('burstTimeout', value)

	@property
	def BurstTimeoutUnit(self):
		"""

		Returns:
			str(kMilliseconds|kSeconds|kTimeFormat|milliseconds|seconds|timeFormat)
		"""
		return self._get_attribute('burstTimeoutUnit')
	@BurstTimeoutUnit.setter
	def BurstTimeoutUnit(self, value):
		self._set_attribute('burstTimeoutUnit', value)

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
	def InterBurstGap(self):
		"""

		Returns:
			str(headToHead|kHeadToHead|kTailToHead|tailToHead)
		"""
		return self._get_attribute('interBurstGap')
	@InterBurstGap.setter
	def InterBurstGap(self, value):
		self._set_attribute('interBurstGap', value)

	@property
	def InterBurstGapValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interBurstGapValue')
	@InterBurstGapValue.setter
	def InterBurstGapValue(self, value):
		self._set_attribute('interBurstGapValue', value)

	@property
	def InterBurstGapValueUnit(self):
		"""

		Returns:
			str(kMilliseconds|kSeconds|milliseconds|seconds)
		"""
		return self._get_attribute('interBurstGapValueUnit')
	@InterBurstGapValueUnit.setter
	def InterBurstGapValueUnit(self, value):
		self._set_attribute('interBurstGapValueUnit', value)

	@property
	def PacketCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packetCount')
	@PacketCount.setter
	def PacketCount(self, value):
		self._set_attribute('packetCount', value)

	@property
	def QueueAutoSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueAutoSize')

	@property
	def QueueAutoSizeEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('queueAutoSizeEnabled')
	@QueueAutoSizeEnabled.setter
	def QueueAutoSizeEnabled(self, value):
		self._set_attribute('queueAutoSizeEnabled', value)

	@property
	def QueueSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueSize')
	@QueueSize.setter
	def QueueSize(self, value):
		self._set_attribute('queueSize', value)
