from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetTopologyGrid(Base):
	"""The NetTopologyGrid class encapsulates a user managed netTopologyGrid node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetTopologyGrid property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'netTopologyGrid'

	def __init__(self, parent):
		super(NetTopologyGrid, self).__init__(parent)

	@property
	def Columns(self):
		"""number of columns

		Returns:
			number
		"""
		return self._get_attribute('columns')
	@Columns.setter
	def Columns(self, value):
		self._set_attribute('columns', value)

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
	def Rows(self):
		"""number of rows

		Returns:
			number
		"""
		return self._get_attribute('rows')
	@Rows.setter
	def Rows(self, value):
		self._set_attribute('rows', value)

	def add(self, Columns=None, IncludeEntryPoint=None, LinkMultiplier=None, Rows=None):
		"""Adds a new netTopologyGrid node on the server and retrieves it in this instance.

		Args:
			Columns (number): number of columns
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			Rows (number): number of rows

		Returns:
			self: This instance with all currently retrieved netTopologyGrid data using find and the newly added netTopologyGrid data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the netTopologyGrid data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Columns=None, IncludeEntryPoint=None, LinkMultiplier=None, Rows=None):
		"""Finds and retrieves netTopologyGrid data from the server.

		All named parameters support regex and can be used to selectively retrieve netTopologyGrid data from the server.
		By default the find method takes no parameters and will retrieve all netTopologyGrid data from the server.

		Args:
			Columns (number): number of columns
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			Rows (number): number of rows

		Returns:
			self: This instance with matching netTopologyGrid data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of netTopologyGrid data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the netTopologyGrid data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
