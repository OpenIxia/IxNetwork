from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Reorder(Base):
	"""The Reorder class encapsulates a required reorder node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Reorder property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'reorder'

	def __init__(self, parent):
		super(Reorder, self).__init__(parent)

	@property
	def ClusterSize(self):
		"""Number of packets to reorder on each occurrence.

		Returns:
			number
		"""
		return self._get_attribute('clusterSize')
	@ClusterSize.setter
	def ClusterSize(self, value):
		self._set_attribute('clusterSize', value)

	@property
	def Enabled(self):
		"""If true, periodically reorder received packets.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def PercentRate(self):
		"""How often to reorder packets.

		Returns:
			number
		"""
		return self._get_attribute('percentRate')
	@PercentRate.setter
	def PercentRate(self, value):
		self._set_attribute('percentRate', value)

	@property
	def SkipCount(self):
		"""How many packets to skip before sending the reordered packets.

		Returns:
			number
		"""
		return self._get_attribute('skipCount')
	@SkipCount.setter
	def SkipCount(self, value):
		self._set_attribute('skipCount', value)
