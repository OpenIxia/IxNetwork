from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MeterCapabilities(Base):
	"""The MeterCapabilities class encapsulates a required meterCapabilities node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterCapabilities property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'meterCapabilities'

	def __init__(self, parent):
		super(MeterCapabilities, self).__init__(parent)

	@property
	def CollectStatistics(self):
		"""The capability to collect statistics.

		Returns:
			bool
		"""
		return self._get_attribute('collectStatistics')
	@CollectStatistics.setter
	def CollectStatistics(self, value):
		self._set_attribute('collectStatistics', value)

	@property
	def DoBurstSize(self):
		"""The size of burst.

		Returns:
			bool
		"""
		return self._get_attribute('doBurstSize')
	@DoBurstSize.setter
	def DoBurstSize(self, value):
		self._set_attribute('doBurstSize', value)

	@property
	def KiloBitPerSecond(self):
		"""Rate value in kilo-bit per second.

		Returns:
			bool
		"""
		return self._get_attribute('kiloBitPerSecond')
	@KiloBitPerSecond.setter
	def KiloBitPerSecond(self, value):
		self._set_attribute('kiloBitPerSecond', value)

	@property
	def PacketPerSecond(self):
		"""Rate value in packet per second.

		Returns:
			bool
		"""
		return self._get_attribute('packetPerSecond')
	@PacketPerSecond.setter
	def PacketPerSecond(self, value):
		self._set_attribute('packetPerSecond', value)
