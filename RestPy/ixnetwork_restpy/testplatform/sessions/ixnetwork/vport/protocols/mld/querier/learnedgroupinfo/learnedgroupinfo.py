from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedGroupInfo(Base):
	"""The LearnedGroupInfo class encapsulates a system managed learnedGroupInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedGroupInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedGroupInfo'

	def __init__(self, parent):
		super(LearnedGroupInfo, self).__init__(parent)

	@property
	def CompatibilityMode(self):
		"""(read only) The MLD version compatibility mode of the MLD querier.

		Returns:
			str(mldv1|mldv2)
		"""
		return self._get_attribute('compatibilityMode')

	@property
	def CompatibilityTimer(self):
		"""(read only) The number of seconds remaining in the compatibility timer.

		Returns:
			number
		"""
		return self._get_attribute('compatibilityTimer')

	@property
	def FilterMode(self):
		"""Displays the filter mode of the querier.

		Returns:
			str(include|exclude)
		"""
		return self._get_attribute('filterMode')

	@property
	def GroupAddress(self):
		"""(read only) The IPv4 address for the multicast group.

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')

	@property
	def GroupTimer(self):
		"""(read only) The number of seconds remaining in the group address timer.

		Returns:
			number
		"""
		return self._get_attribute('groupTimer')

	@property
	def SourceAddress(self):
		"""(read only) The source IP addresses from which the host receives messages for this multicast group.

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')

	@property
	def SourceTimer(self):
		"""(read only) The number of seconds remaining in the source address timer.

		Returns:
			number
		"""
		return self._get_attribute('sourceTimer')

	def find(self, CompatibilityMode=None, CompatibilityTimer=None, FilterMode=None, GroupAddress=None, GroupTimer=None, SourceAddress=None, SourceTimer=None):
		"""Finds and retrieves learnedGroupInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedGroupInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedGroupInfo data from the server.

		Args:
			CompatibilityMode (str(mldv1|mldv2)): (read only) The MLD version compatibility mode of the MLD querier.
			CompatibilityTimer (number): (read only) The number of seconds remaining in the compatibility timer.
			FilterMode (str(include|exclude)): Displays the filter mode of the querier.
			GroupAddress (str): (read only) The IPv4 address for the multicast group.
			GroupTimer (number): (read only) The number of seconds remaining in the group address timer.
			SourceAddress (str): (read only) The source IP addresses from which the host receives messages for this multicast group.
			SourceTimer (number): (read only) The number of seconds remaining in the source address timer.

		Returns:
			self: This instance with matching learnedGroupInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedGroupInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedGroupInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
