from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CellTable(Base):
	"""The CellTable class encapsulates a system managed cellTable node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CellTable property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'cellTable'

	def __init__(self, parent):
		super(CellTable, self).__init__(parent)

	@property
	def Col(self):
		"""An instance of the Col class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.col.Col)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.col import Col
		return Col(self)

	@property
	def Actions(self):
		"""The list of actions allowed on the learned information table

		Returns:
			list(str)
		"""
		return self._get_attribute('actions')

	@property
	def Columns(self):
		"""The list of columns in the learned information table

		Returns:
			list(str)
		"""
		return self._get_attribute('columns')

	@property
	def Type(self):
		"""Description of the learned information type

		Returns:
			str
		"""
		return self._get_attribute('type')

	@property
	def Values(self):
		"""A list of rows of learned information values

		Returns:
			list(list[str])
		"""
		return self._get_attribute('values')

	def find(self, Actions=None, Columns=None, Type=None, Values=None):
		"""Finds and retrieves cellTable data from the server.

		All named parameters support regex and can be used to selectively retrieve cellTable data from the server.
		By default the find method takes no parameters and will retrieve all cellTable data from the server.

		Args:
			Actions (list(str)): The list of actions allowed on the learned information table
			Columns (list(str)): The list of columns in the learned information table
			Type (str): Description of the learned information type
			Values (list(list[str])): A list of rows of learned information values

		Returns:
			self: This instance with matching cellTable data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of cellTable data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the cellTable data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
