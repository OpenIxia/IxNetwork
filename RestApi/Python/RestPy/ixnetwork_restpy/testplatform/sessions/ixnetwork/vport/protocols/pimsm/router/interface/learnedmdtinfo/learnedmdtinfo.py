from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedMdtInfo(Base):
	"""The LearnedMdtInfo class encapsulates a system managed learnedMdtInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedMdtInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedMdtInfo'

	def __init__(self, parent):
		super(LearnedMdtInfo, self).__init__(parent)

	@property
	def Age(self):
		"""The amount of time (in seconds) remaining before this TLV times out.

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def CeGroupAddress(self):
		"""The CE group address contained in this data MDT TLV.

		Returns:
			str
		"""
		return self._get_attribute('ceGroupAddress')

	@property
	def CeSourceAddress(self):
		"""The CE source address contained in this data MDT TLV.

		Returns:
			str
		"""
		return self._get_attribute('ceSourceAddress')

	@property
	def MdtGroupAddress(self):
		"""The MDT (PE) group address contained in this data MDT TLV.

		Returns:
			str
		"""
		return self._get_attribute('mdtGroupAddress')

	@property
	def MdtSourceAddress(self):
		"""The MDT (PE) source address contained in this data MDT TLV.

		Returns:
			str
		"""
		return self._get_attribute('mdtSourceAddress')

	def find(self, Age=None, CeGroupAddress=None, CeSourceAddress=None, MdtGroupAddress=None, MdtSourceAddress=None):
		"""Finds and retrieves learnedMdtInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedMdtInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedMdtInfo data from the server.

		Args:
			Age (number): The amount of time (in seconds) remaining before this TLV times out.
			CeGroupAddress (str): The CE group address contained in this data MDT TLV.
			CeSourceAddress (str): The CE source address contained in this data MDT TLV.
			MdtGroupAddress (str): The MDT (PE) group address contained in this data MDT TLV.
			MdtSourceAddress (str): The MDT (PE) source address contained in this data MDT TLV.

		Returns:
			self: This instance with matching learnedMdtInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedMdtInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedMdtInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
