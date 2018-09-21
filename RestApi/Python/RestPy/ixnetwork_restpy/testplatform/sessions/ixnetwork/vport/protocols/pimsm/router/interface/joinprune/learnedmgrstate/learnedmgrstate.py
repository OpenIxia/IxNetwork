from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedMgrState(Base):
	"""The LearnedMgrState class encapsulates a system managed learnedMgrState node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedMgrState property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedMgrState'

	def __init__(self, parent):
		super(LearnedMgrState, self).__init__(parent)

	@property
	def Group(self):
		"""An IPv4 address used with the groupMaskWidth to create a range of multicast addresses. Not used with rangeType = pimsmJoinPruneTypeG. (default = 225.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('group')

	@property
	def Source(self):
		"""The source address that generates multicast traffic. It must be a unicast address.

		Returns:
			str
		"""
		return self._get_attribute('source')

	def find(self, Group=None, Source=None):
		"""Finds and retrieves learnedMgrState data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedMgrState data from the server.
		By default the find method takes no parameters and will retrieve all learnedMgrState data from the server.

		Args:
			Group (str): An IPv4 address used with the groupMaskWidth to create a range of multicast addresses. Not used with rangeType = pimsmJoinPruneTypeG. (default = 225.0.0.0)
			Source (str): The source address that generates multicast traffic. It must be a unicast address.

		Returns:
			self: This instance with matching learnedMgrState data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedMgrState data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedMgrState data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
