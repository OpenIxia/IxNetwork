from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Drop(Base):
	"""The Drop class encapsulates a required drop node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Drop property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'drop'

	def __init__(self, parent):
		super(Drop, self).__init__(parent)

	@property
	def ClusterSize(self):
		"""Number of packets to drop on each occurrence.

		Returns:
			number
		"""
		return self._get_attribute('clusterSize')
	@ClusterSize.setter
	def ClusterSize(self, value):
		self._set_attribute('clusterSize', value)

	@property
	def Enabled(self):
		"""If true, periodically drop received packets.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def PercentRate(self):
		"""How often to drop packets, as a percentage.

		Returns:
			number
		"""
		return self._get_attribute('percentRate')
	@PercentRate.setter
	def PercentRate(self, value):
		self._set_attribute('percentRate', value)
