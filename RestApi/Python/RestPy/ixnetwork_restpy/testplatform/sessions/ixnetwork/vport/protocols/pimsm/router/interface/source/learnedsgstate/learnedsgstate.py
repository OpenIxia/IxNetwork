from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedSgState(Base):
	"""The LearnedSgState class encapsulates a system managed learnedSgState node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedSgState property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedSgState'

	def __init__(self, parent):
		super(LearnedSgState, self).__init__(parent)

	@property
	def Group(self):
		"""The first IPv4 multicast group address in the range of group addresses included in the Register message. (default = 255.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('group')

	@property
	def Source(self):
		"""The first source address to be included in the Register messages. (default = 0.0.0.1)

		Returns:
			str
		"""
		return self._get_attribute('source')

	def find(self, Group=None, Source=None):
		"""Finds and retrieves learnedSgState data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedSgState data from the server.
		By default the find method takes no parameters and will retrieve all learnedSgState data from the server.

		Args:
			Group (str): The first IPv4 multicast group address in the range of group addresses included in the Register message. (default = 255.0.0.0)
			Source (str): The first source address to be included in the Register messages. (default = 0.0.0.1)

		Returns:
			self: This instance with matching learnedSgState data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedSgState data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedSgState data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
