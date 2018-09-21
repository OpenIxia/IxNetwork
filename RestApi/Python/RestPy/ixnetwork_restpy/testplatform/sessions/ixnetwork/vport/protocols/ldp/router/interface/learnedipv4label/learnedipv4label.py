from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedIpv4Label(Base):
	"""The LearnedIpv4Label class encapsulates a system managed learnedIpv4Label node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedIpv4Label property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedIpv4Label'

	def __init__(self, parent):
		super(LearnedIpv4Label, self).__init__(parent)

	@property
	def Fec(self):
		"""Forwarding equivalence class (FEC) type.

		Returns:
			str
		"""
		return self._get_attribute('fec')

	@property
	def FecPrefixLen(self):
		"""The length of the prefix associated with the FEC.

		Returns:
			number
		"""
		return self._get_attribute('fecPrefixLen')

	@property
	def Label(self):
		"""The label value added to the packet(s) by the upstream LDP peer.

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LabelSpaceId(self):
		"""Part of the LSR ID. It forms the last 2 octets of the 6-octet LDP identifier.

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceId')

	@property
	def PeerIpAddress(self):
		"""The RID of the upstream LDP peer. Part of the LSR ID. It must be globally unique. It forms the first 4 octets of the 6-octet LDP identifier.

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	def find(self, Fec=None, FecPrefixLen=None, Label=None, LabelSpaceId=None, PeerIpAddress=None):
		"""Finds and retrieves learnedIpv4Label data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedIpv4Label data from the server.
		By default the find method takes no parameters and will retrieve all learnedIpv4Label data from the server.

		Args:
			Fec (str): Forwarding equivalence class (FEC) type.
			FecPrefixLen (number): The length of the prefix associated with the FEC.
			Label (number): The label value added to the packet(s) by the upstream LDP peer.
			LabelSpaceId (number): Part of the LSR ID. It forms the last 2 octets of the 6-octet LDP identifier.
			PeerIpAddress (str): The RID of the upstream LDP peer. Part of the LSR ID. It must be globally unique. It forms the first 4 octets of the 6-octet LDP identifier.

		Returns:
			self: This instance with matching learnedIpv4Label data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedIpv4Label data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedIpv4Label data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
