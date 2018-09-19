from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LatencyBin(Base):
	"""The LatencyBin class encapsulates a required latencyBin node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LatencyBin property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'latencyBin'

	def __init__(self, parent):
		super(LatencyBin, self).__init__(parent)

	@property
	def BinLimits(self):
		"""Specifies the upper limit of each Time Bins for Latency Bin Tracking.

		Returns:
			list(number)
		"""
		return self._get_attribute('binLimits')
	@BinLimits.setter
	def BinLimits(self, value):
		self._set_attribute('binLimits', value)

	@property
	def Enabled(self):
		"""If true, Latency Bin Tracking is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def NumberOfBins(self):
		"""Specifies the number of Time Bins for Latency Bin Tracking.

		Returns:
			number
		"""
		return self._get_attribute('numberOfBins')
	@NumberOfBins.setter
	def NumberOfBins(self, value):
		self._set_attribute('numberOfBins', value)
