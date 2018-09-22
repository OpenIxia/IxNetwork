from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedMdtState(Base):
	"""The LearnedMdtState class encapsulates a system managed learnedMdtState node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedMdtState property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedMdtState'

	def __init__(self, parent):
		super(LearnedMdtState, self).__init__(parent)

	@property
	def Group(self):
		"""List of learned MDT group addresses.

		Returns:
			str
		"""
		return self._get_attribute('group')

	def find(self, Group=None):
		"""Finds and retrieves learnedMdtState data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedMdtState data from the server.
		By default the find method takes no parameters and will retrieve all learnedMdtState data from the server.

		Args:
			Group (str): List of learned MDT group addresses.

		Returns:
			self: This instance with matching learnedMdtState data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedMdtState data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedMdtState data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
