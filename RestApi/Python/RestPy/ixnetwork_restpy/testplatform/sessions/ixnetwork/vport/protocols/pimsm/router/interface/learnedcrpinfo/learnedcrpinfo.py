from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedCrpInfo(Base):
	"""The LearnedCrpInfo class encapsulates a system managed learnedCrpInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedCrpInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedCrpInfo'

	def __init__(self, parent):
		super(LearnedCrpInfo, self).__init__(parent)

	@property
	def CrpAddress(self):
		"""The RP address expresing candidacy for the specific group of RPs.

		Returns:
			str
		"""
		return self._get_attribute('crpAddress')

	@property
	def ExpiryTimer(self):
		"""The expiry time for the specific record as received in CRP Adv Message.

		Returns:
			number
		"""
		return self._get_attribute('expiryTimer')

	@property
	def GroupAddress(self):
		"""The Group Address learnt through Candidate RP advertisements.

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')

	@property
	def GroupMaskWidth(self):
		"""It shows the prefix length (in bits) of the group address learnt.

		Returns:
			number
		"""
		return self._get_attribute('groupMaskWidth')

	@property
	def Priority(self):
		"""Priority of the selected Candidate RP.

		Returns:
			number
		"""
		return self._get_attribute('priority')

	def find(self, CrpAddress=None, ExpiryTimer=None, GroupAddress=None, GroupMaskWidth=None, Priority=None):
		"""Finds and retrieves learnedCrpInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedCrpInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedCrpInfo data from the server.

		Args:
			CrpAddress (str): The RP address expresing candidacy for the specific group of RPs.
			ExpiryTimer (number): The expiry time for the specific record as received in CRP Adv Message.
			GroupAddress (str): The Group Address learnt through Candidate RP advertisements.
			GroupMaskWidth (number): It shows the prefix length (in bits) of the group address learnt.
			Priority (number): Priority of the selected Candidate RP.

		Returns:
			self: This instance with matching learnedCrpInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedCrpInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedCrpInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
