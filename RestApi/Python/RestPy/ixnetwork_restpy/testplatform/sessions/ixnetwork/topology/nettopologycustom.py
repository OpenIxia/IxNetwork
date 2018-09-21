from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetTopologyCustom(Base):
	"""The NetTopologyCustom class encapsulates a user managed netTopologyCustom node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetTopologyCustom property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'netTopologyCustom'

	def __init__(self, parent):
		super(NetTopologyCustom, self).__init__(parent)

	@property
	def LinkTable(self):
		"""An instance of the LinkTable class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linktable.LinkTable)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linktable import LinkTable
		return LinkTable(self)._select()

	@property
	def IncludeEntryPoint(self):
		"""if true, entry node belongs to ring topology, otherwise it is outside of ring

		Returns:
			bool
		"""
		return self._get_attribute('includeEntryPoint')
	@IncludeEntryPoint.setter
	def IncludeEntryPoint(self, value):
		self._set_attribute('includeEntryPoint', value)

	@property
	def LinkMultiplier(self):
		"""number of links between two nodes

		Returns:
			number
		"""
		return self._get_attribute('linkMultiplier')
	@LinkMultiplier.setter
	def LinkMultiplier(self, value):
		self._set_attribute('linkMultiplier', value)

	@property
	def NumberOfNodes(self):
		"""Number Of Nodes

		Returns:
			number
		"""
		return self._get_attribute('numberOfNodes')

	def add(self, IncludeEntryPoint=None, LinkMultiplier=None):
		"""Adds a new netTopologyCustom node on the server and retrieves it in this instance.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes

		Returns:
			self: This instance with all currently retrieved netTopologyCustom data using find and the newly added netTopologyCustom data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the netTopologyCustom data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeEntryPoint=None, LinkMultiplier=None, NumberOfNodes=None):
		"""Finds and retrieves netTopologyCustom data from the server.

		All named parameters support regex and can be used to selectively retrieve netTopologyCustom data from the server.
		By default the find method takes no parameters and will retrieve all netTopologyCustom data from the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			NumberOfNodes (number): Number Of Nodes

		Returns:
			self: This instance with matching netTopologyCustom data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of netTopologyCustom data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the netTopologyCustom data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
