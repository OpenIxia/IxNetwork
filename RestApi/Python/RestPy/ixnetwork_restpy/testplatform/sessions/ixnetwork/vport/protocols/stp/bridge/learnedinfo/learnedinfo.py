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
	def BridgeMac(self):
		"""The MAC address of the bridge advertising information on this link.

		Returns:
			str
		"""
		return self._get_attribute('bridgeMac')

	@property
	def RootCost(self):
		"""The cost for the shortest path from this bridge to the root bridge.

		Returns:
			number
		"""
		return self._get_attribute('rootCost')

	@property
	def RootMac(self):
		"""The root bridge MAC address being advertised by the bridge.

		Returns:
			str
		"""
		return self._get_attribute('rootMac')

	@property
	def RootPriority(self):
		"""The priority for the root bridge.

		Returns:
			number
		"""
		return self._get_attribute('rootPriority')
