from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ExternalLink(Base):
	"""The ExternalLink class encapsulates a user managed externalLink node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ExternalLink property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'externalLink'

	def __init__(self, parent):
		super(ExternalLink, self).__init__(parent)

	@property
	def FromNodeIndex(self):
		"""Index of the originating node as defined in fromNetworkTopology

		Returns:
			number
		"""
		return self._get_attribute('fromNodeIndex')
	@FromNodeIndex.setter
	def FromNodeIndex(self, value):
		self._set_attribute('fromNodeIndex', value)

	@property
	def ToNetworkTopology(self):
		"""Network Topology this link is pointing to

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('toNetworkTopology')
	@ToNetworkTopology.setter
	def ToNetworkTopology(self, value):
		self._set_attribute('toNetworkTopology', value)

	@property
	def ToNodeIndex(self):
		"""Index of the target node as defined in toNetworkTopology

		Returns:
			number
		"""
		return self._get_attribute('toNodeIndex')
	@ToNodeIndex.setter
	def ToNodeIndex(self, value):
		self._set_attribute('toNodeIndex', value)

	def add(self, FromNodeIndex=None, ToNetworkTopology=None, ToNodeIndex=None):
		"""Adds a new externalLink node on the server and retrieves it in this instance.

		Args:
			FromNodeIndex (number): Index of the originating node as defined in fromNetworkTopology
			ToNetworkTopology (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): Network Topology this link is pointing to
			ToNodeIndex (number): Index of the target node as defined in toNetworkTopology

		Returns:
			self: This instance with all currently retrieved externalLink data using find and the newly added externalLink data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the externalLink data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, FromNodeIndex=None, ToNetworkTopology=None, ToNodeIndex=None):
		"""Finds and retrieves externalLink data from the server.

		All named parameters support regex and can be used to selectively retrieve externalLink data from the server.
		By default the find method takes no parameters and will retrieve all externalLink data from the server.

		Args:
			FromNodeIndex (number): Index of the originating node as defined in fromNetworkTopology
			ToNetworkTopology (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): Network Topology this link is pointing to
			ToNodeIndex (number): Index of the target node as defined in toNetworkTopology

		Returns:
			self: This instance with matching externalLink data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of externalLink data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the externalLink data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
