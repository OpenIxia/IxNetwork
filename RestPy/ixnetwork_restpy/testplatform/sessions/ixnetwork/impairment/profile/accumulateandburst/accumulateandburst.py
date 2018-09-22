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
		"""Represents the burst octet size. The default value is 1014.

		Returns:
			number
		"""
		return self._get_attribute('burstSize')
	@BurstSize.setter
	def BurstSize(self, value):
		self._set_attribute('burstSize', value)

	@property
	def BurstSizeUnit(self):
		"""The burst size unit is either megabytes or kilobytes. The default unit is kilobytes.

		Returns:
			str(kilobytes|kKilobytes|kMegabytes|megabytes)
		"""
		return self._get_attribute('burstSizeUnit')
	@BurstSizeUnit.setter
	def BurstSizeUnit(self, value):
		self._set_attribute('burstSizeUnit', value)

	@property
	def BurstTimeout(self):
		"""The burst timeout.The default value is 5 seconds.

		Returns:
			str
		"""
		return self._get_attribute('burstTimeout')
	@BurstTimeout.setter
	def BurstTimeout(self, value):
		self._set_attribute('burstTimeout', value)

	@property
	def BurstTimeoutUnit(self):
		"""Seconds(default) / milliseconds / mm:ss.fff time format.

		Returns:
			str(kMilliseconds|kSeconds|kTimeFormat|milliseconds|seconds|timeFormat)
		"""
		return self._get_attribute('burstTimeoutUnit')
	@BurstTimeoutUnit.setter
	def BurstTimeoutUnit(self, value):
		self._set_attribute('burstTimeoutUnit', value)

	@property
	def Enabled(self):
		"""If true, received packets are queued and transmitted in bursts.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterBurstGap(self):
		"""Tail to head (default) / Head to head.

		Returns:
			str(headToHead|kHeadToHead|kTailToHead|tailToHead)
		"""
		return self._get_attribute('interBurstGap')
	@InterBurstGap.setter
	def InterBurstGap(self, value):
		self._set_attribute('interBurstGap', value)

	@property
	def InterBurstGapValue(self):
		"""The InterBurst gap value. The default value is 20 ms.

		Returns:
			number
		"""
		return self._get_attribute('interBurstGapValue')
	@InterBurstGapValue.setter
	def InterBurstGapValue(self, value):
		self._set_attribute('interBurstGapValue', value)

	@property
	def InterBurstGapValueUnit(self):
		"""Seconds / milliseconds (default).

		Returns:
			str(kMilliseconds|kSeconds|milliseconds|seconds)
		"""
		return self._get_attribute('interBurstGapValueUnit')
	@InterBurstGapValueUnit.setter
	def InterBurstGapValueUnit(self, value):
		self._set_attribute('interBurstGapValueUnit', value)

	@property
	def PacketCount(self):
		"""Represents the burst packet count. The default value is 1000 packets.

		Returns:
			number
		"""
		return self._get_attribute('packetCount')
	@PacketCount.setter
	def PacketCount(self, value):
		self._set_attribute('packetCount', value)

	@property
	def QueueAutoSize(self):
		"""Gets the automatically calculated queue size when queueAutoSizeEnable is true or zero when queueAutoSizeEnable is false.

		Returns:
			number
		"""
		return self._get_attribute('queueAutoSize')

	@property
	def QueueAutoSizeEnabled(self):
		"""Automatically calculate queue size. The default value is true.

		Returns:
			bool
		"""
		return self._get_attribute('queueAutoSizeEnabled')
	@QueueAutoSizeEnabled.setter
	def QueueAutoSizeEnabled(self, value):
		self._set_attribute('queueAutoSizeEnabled', value)

	@property
	def QueueSize(self):
		"""The accumulate-and-burst queue size expressed in MB. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('queueSize')
	@QueueSize.setter
	def QueueSize(self, value):
		self._set_attribute('queueSize', value)
