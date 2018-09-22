from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DelayVariation(Base):
	"""The DelayVariation class encapsulates a required delayVariation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DelayVariation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'delayVariation'

	def __init__(self, parent):
		super(DelayVariation, self).__init__(parent)

	@property
	def Enabled(self):
		"""If enabled, fetches latency delay variation statistics with average, minimum, and maximum measurements.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def LargeSequenceNumberErrorThreshold(self):
		"""The value for the large sequence number error.

		Returns:
			number
		"""
		return self._get_attribute('largeSequenceNumberErrorThreshold')
	@LargeSequenceNumberErrorThreshold.setter
	def LargeSequenceNumberErrorThreshold(self, value):
		self._set_attribute('largeSequenceNumberErrorThreshold', value)

	@property
	def LatencyMode(self):
		"""If enabled, allows to use Cut Through, Forwarding Delay, MEF, and Store and Forward Delay variation statictics measurements.

		Returns:
			str(cutThrough|forwardingDelay|mef|storeForward)
		"""
		return self._get_attribute('latencyMode')
	@LatencyMode.setter
	def LatencyMode(self, value):
		self._set_attribute('latencyMode', value)

	@property
	def StatisticsMode(self):
		"""If enabled, allows to receive delay variation statistics with sequence error measurements.

		Returns:
			str(rxDelayVariationAverage|rxDelayVariationErrorsAndRate|rxDelayVariationMinMaxAndRate)
		"""
		return self._get_attribute('statisticsMode')
	@StatisticsMode.setter
	def StatisticsMode(self, value):
		self._set_attribute('statisticsMode', value)
