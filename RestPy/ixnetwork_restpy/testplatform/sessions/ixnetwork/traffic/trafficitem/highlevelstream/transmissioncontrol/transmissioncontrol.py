from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TransmissionControl(Base):
	"""The TransmissionControl class encapsulates a required transmissionControl node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TransmissionControl property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'transmissionControl'

	def __init__(self, parent):
		super(TransmissionControl, self).__init__(parent)

	@property
	def BurstPacketCount(self):
		"""Specifies the number of packets per burst.

		Returns:
			number
		"""
		return self._get_attribute('burstPacketCount')
	@BurstPacketCount.setter
	def BurstPacketCount(self, value):
		self._set_attribute('burstPacketCount', value)

	@property
	def Duration(self):
		"""Indicates the time duration.

		Returns:
			number
		"""
		return self._get_attribute('duration')
	@Duration.setter
	def Duration(self, value):
		self._set_attribute('duration', value)

	@property
	def EnableInterBurstGap(self):
		"""Enables the inter-burst gap of a frame.

		Returns:
			bool
		"""
		return self._get_attribute('enableInterBurstGap')
	@EnableInterBurstGap.setter
	def EnableInterBurstGap(self, value):
		self._set_attribute('enableInterBurstGap', value)

	@property
	def EnableInterStreamGap(self):
		"""Enables the inter-stream gap of a frame.

		Returns:
			bool
		"""
		return self._get_attribute('enableInterStreamGap')
	@EnableInterStreamGap.setter
	def EnableInterStreamGap(self, value):
		self._set_attribute('enableInterStreamGap', value)

	@property
	def FrameCount(self):
		"""Specifies Fixed Packet Count when Transmission Mode is Interleaved.

		Returns:
			number
		"""
		return self._get_attribute('frameCount')
	@FrameCount.setter
	def FrameCount(self, value):
		self._set_attribute('frameCount', value)

	@property
	def InterBurstGap(self):
		"""Specifies the gap between any two consecutive burst.

		Returns:
			number
		"""
		return self._get_attribute('interBurstGap')
	@InterBurstGap.setter
	def InterBurstGap(self, value):
		self._set_attribute('interBurstGap', value)

	@property
	def InterBurstGapUnits(self):
		"""Specifies unit of Inter Burst Gap either in bytes or nanoseconds.

		Returns:
			str(bytes|nanoseconds)
		"""
		return self._get_attribute('interBurstGapUnits')
	@InterBurstGapUnits.setter
	def InterBurstGapUnits(self, value):
		self._set_attribute('interBurstGapUnits', value)

	@property
	def InterStreamGap(self):
		"""Specifies the gap between any two consecutive Flow Groups when Transmission Mode is Sequential.

		Returns:
			number
		"""
		return self._get_attribute('interStreamGap')
	@InterStreamGap.setter
	def InterStreamGap(self, value):
		self._set_attribute('interStreamGap', value)

	@property
	def IterationCount(self):
		"""Specifies the number of iterations the Flow Group can have when Transmission Mode is Interleaved.

		Returns:
			number
		"""
		return self._get_attribute('iterationCount')
	@IterationCount.setter
	def IterationCount(self, value):
		self._set_attribute('iterationCount', value)

	@property
	def MinGapBytes(self):
		"""Specifies the minimum gap between any 2 packets or frames in term of bytes.

		Returns:
			number
		"""
		return self._get_attribute('minGapBytes')
	@MinGapBytes.setter
	def MinGapBytes(self, value):
		self._set_attribute('minGapBytes', value)

	@property
	def RepeatBurst(self):
		"""Specifies number of times a burst can be repeated when Transmission Mode is Sequential.

		Returns:
			number
		"""
		return self._get_attribute('repeatBurst')
	@RepeatBurst.setter
	def RepeatBurst(self, value):
		self._set_attribute('repeatBurst', value)

	@property
	def StartDelay(self):
		"""Specifies the delay in Start when Transmission Mode is Interleaved.

		Returns:
			number
		"""
		return self._get_attribute('startDelay')
	@StartDelay.setter
	def StartDelay(self, value):
		self._set_attribute('startDelay', value)

	@property
	def StartDelayUnits(self):
		"""Specifies the unit for Delay in Start when Transmission Mode is Interleaved.

		Returns:
			str(bytes|nanoseconds)
		"""
		return self._get_attribute('startDelayUnits')
	@StartDelayUnits.setter
	def StartDelayUnits(self, value):
		self._set_attribute('startDelayUnits', value)

	@property
	def Type(self):
		"""The Transmission Control types.

		Returns:
			str(auto|continuous|custom|fixedDuration|fixedFrameCount|fixedIterationCount)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)
