from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Duplicate(Base):
	"""The Duplicate class encapsulates a required duplicate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Duplicate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'duplicate'

	def __init__(self, parent):
		super(Duplicate, self).__init__(parent)

	@property
	def ClusterSize(self):
		"""Number of packets to duplicate on each occurrence.

		Returns:
			number
		"""
		return self._get_attribute('clusterSize')
	@ClusterSize.setter
	def ClusterSize(self, value):
		self._set_attribute('clusterSize', value)

	@property
	def DuplicateCount(self):
		"""Number of times to duplicate each packet.

		Returns:
			number
		"""
		return self._get_attribute('duplicateCount')
	@DuplicateCount.setter
	def DuplicateCount(self, value):
		self._set_attribute('duplicateCount', value)

	@property
	def Enabled(self):
		"""If true, periodically duplicate received packets.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def PercentRate(self):
		"""How often to duplicate packets.

		Returns:
			number
		"""
		return self._get_attribute('percentRate')
	@PercentRate.setter
	def PercentRate(self, value):
		self._set_attribute('percentRate', value)
