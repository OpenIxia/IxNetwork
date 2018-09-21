from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedLsa(Base):
	"""The LearnedLsa class encapsulates a system managed learnedLsa node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedLsa property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedLsa'

	def __init__(self, parent):
		super(LearnedLsa, self).__init__(parent)

	@property
	def AdvRouterId(self):
		"""The router ID of the router that is originating the LSA. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('advRouterId')

	@property
	def Age(self):
		"""Read only. Only available when this command is used to access a learned LSA. This value holds the age of the LSA extracted from the LSA header.

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def LinkStateId(self):
		"""The router ID of the originating router. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('linkStateId')

	@property
	def LsaType(self):
		"""Read-only. The current LSA type. (default = 0)

		Returns:
			str(router|network|areaSummary|externalSummary|external|nssa|opaqueLocalScope|opaqueAreaScope|opaqueAsScope)
		"""
		return self._get_attribute('lsaType')

	@property
	def SeqNumber(self):
		"""Read only. Only available when this command is used to access a learned LSA. This value holds the sequence number of the LSA extracted from the LSA header.

		Returns:
			str
		"""
		return self._get_attribute('seqNumber')

	def find(self, AdvRouterId=None, Age=None, LinkStateId=None, LsaType=None, SeqNumber=None):
		"""Finds and retrieves learnedLsa data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedLsa data from the server.
		By default the find method takes no parameters and will retrieve all learnedLsa data from the server.

		Args:
			AdvRouterId (str): The router ID of the router that is originating the LSA. (default = 0.0.0.0)
			Age (number): Read only. Only available when this command is used to access a learned LSA. This value holds the age of the LSA extracted from the LSA header.
			LinkStateId (str): The router ID of the originating router. (default = 0.0.0.0)
			LsaType (str(router|network|areaSummary|externalSummary|external|nssa|opaqueLocalScope|opaqueAreaScope|opaqueAsScope)): Read-only. The current LSA type. (default = 0)
			SeqNumber (str): Read only. Only available when this command is used to access a learned LSA. This value holds the sequence number of the LSA extracted from the LSA header.

		Returns:
			self: This instance with matching learnedLsa data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedLsa data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedLsa data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
