from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Flags(Base):
	"""The Flags class encapsulates a required flags node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Flags property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flags'

	def __init__(self, parent):
		super(Flags, self).__init__(parent)

	@property
	def BurstSize(self):
		"""This flag indicate that burst size calculation is to be done while applying the bands.

		Returns:
			bool
		"""
		return self._get_attribute('burstSize')
	@BurstSize.setter
	def BurstSize(self, value):
		self._set_attribute('burstSize', value)

	@property
	def CollectStatistics(self):
		"""This flag enables statistics collection for the meter and each band.

		Returns:
			bool
		"""
		return self._get_attribute('collectStatistics')
	@CollectStatistics.setter
	def CollectStatistics(self, value):
		self._set_attribute('collectStatistics', value)

	@property
	def RateKb(self):
		"""This flag indicates the rate value for bands associated with this meter is considered in kilo-bits per second.

		Returns:
			bool
		"""
		return self._get_attribute('rateKb')
	@RateKb.setter
	def RateKb(self, value):
		self._set_attribute('rateKb', value)

	@property
	def RatePacket(self):
		"""This flag indicates same as Rate (kb/sec)but the rate value is in packet per second.

		Returns:
			bool
		"""
		return self._get_attribute('ratePacket')
	@RatePacket.setter
	def RatePacket(self, value):
		self._set_attribute('ratePacket', value)
