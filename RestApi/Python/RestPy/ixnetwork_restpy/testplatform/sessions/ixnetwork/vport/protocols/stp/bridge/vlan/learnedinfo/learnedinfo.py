from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInfo(Base):
	"""The LearnedInfo class encapsulates a required learnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedInfo'

	def __init__(self, parent):
		super(LearnedInfo, self).__init__(parent)

	@property
	def ActualId(self):
		"""The identifier of the designated port associated with this RSTP interface.

		Returns:
			number
		"""
		return self._get_attribute('actualId')

	@property
	def RootCost(self):
		"""Root Path Cost. The administrative cost for the shortest path from this bridge to the Root bridge. A 4-byte unsigned integer. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('rootCost')

	@property
	def RootMac(self):
		"""Common and internal spanning tree (CIST) regional (internal) MAC address. Part of the CIST regional root identifier.

		Returns:
			str
		"""
		return self._get_attribute('rootMac')

	@property
	def RootPriority(self):
		"""The priority value of the root bridge for the common and internal spanning tree (CIST)/MSTP region (internal). Part of the CIST regional root identifier. Since MAC address reduction is used, only multiples of 4096 are used.

		Returns:
			number
		"""
		return self._get_attribute('rootPriority')
