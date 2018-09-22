from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedIpv4P2mpLables(Base):
	"""The LearnedIpv4P2mpLables class encapsulates a system managed learnedIpv4P2mpLables node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedIpv4P2mpLables property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedIpv4P2mpLables'

	def __init__(self, parent):
		super(LearnedIpv4P2mpLables, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4p2mplables.opaquevalueelement.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4p2mplables.opaquevalueelement.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def Label(self):
		"""Indicates the label value added to the packet(s) by the upstream LDP peer.

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LabelSpaceId(self):
		"""Part of the LSR Id. It forms the last 2 octets of the 6-octet LDP Identifier.

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceId')

	@property
	def PeerIpAddress(self):
		"""The RID of the upstream LDP peer. Part of the LSR Id. It must be globally unique. It forms the first 4 octets of the 6-octet LDP Identifier.

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	@property
	def RootAddress(self):
		"""Root Address of IPv4 P2MP labels learned.

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')

	def find(self, Label=None, LabelSpaceId=None, PeerIpAddress=None, RootAddress=None):
		"""Finds and retrieves learnedIpv4P2mpLables data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedIpv4P2mpLables data from the server.
		By default the find method takes no parameters and will retrieve all learnedIpv4P2mpLables data from the server.

		Args:
			Label (number): Indicates the label value added to the packet(s) by the upstream LDP peer.
			LabelSpaceId (number): Part of the LSR Id. It forms the last 2 octets of the 6-octet LDP Identifier.
			PeerIpAddress (str): The RID of the upstream LDP peer. Part of the LSR Id. It must be globally unique. It forms the first 4 octets of the 6-octet LDP Identifier.
			RootAddress (str): Root Address of IPv4 P2MP labels learned.

		Returns:
			self: This instance with matching learnedIpv4P2mpLables data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedIpv4P2mpLables data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedIpv4P2mpLables data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
