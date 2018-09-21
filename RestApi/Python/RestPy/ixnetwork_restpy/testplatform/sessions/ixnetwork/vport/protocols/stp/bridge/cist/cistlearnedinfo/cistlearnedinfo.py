from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CistLearnedInfo(Base):
	"""The CistLearnedInfo class encapsulates a required cistLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CistLearnedInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'cistLearnedInfo'

	def __init__(self, parent):
		super(CistLearnedInfo, self).__init__(parent)

	@property
	def RegRootCost(self):
		"""(Read-only) The cost for the shortest path from the advertising bridge to the regional root bridge.

		Returns:
			number
		"""
		return self._get_attribute('regRootCost')

	@property
	def RegRootMac(self):
		"""(Read-only) The regional root MAC address being advertised by the bridge.

		Returns:
			str
		"""
		return self._get_attribute('regRootMac')

	@property
	def RegRootPriority(self):
		"""(Read-only) The regional root priority being advertised by the bridge.

		Returns:
			number
		"""
		return self._get_attribute('regRootPriority')

	@property
	def RootCost(self):
		"""(Read-only) The cost for the shortest path from the advertising bridge to the root bridge.

		Returns:
			number
		"""
		return self._get_attribute('rootCost')

	@property
	def RootMac(self):
		"""(Read-only) The root bridge MAC address being advertised.

		Returns:
			str
		"""
		return self._get_attribute('rootMac')

	@property
	def RootPriority(self):
		"""(Read-only) The priority being advertised for the root bridge.

		Returns:
			number
		"""
		return self._get_attribute('rootPriority')
