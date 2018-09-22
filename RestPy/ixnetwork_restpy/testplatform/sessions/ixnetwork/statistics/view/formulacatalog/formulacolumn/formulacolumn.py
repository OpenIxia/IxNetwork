from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FormulaColumn(Base):
	"""The FormulaColumn class encapsulates a user managed formulaColumn node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FormulaColumn property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'formulaColumn'

	def __init__(self, parent):
		super(FormulaColumn, self).__init__(parent)

	@property
	def Caption(self):
		"""The name of the formula.

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def Formula(self):
		"""The formula that is filtered.

		Returns:
			str
		"""
		return self._get_attribute('formula')
	@Formula.setter
	def Formula(self, value):
		self._set_attribute('formula', value)

	def add(self, Caption=None, Formula=None):
		"""Adds a new formulaColumn node on the server and retrieves it in this instance.

		Args:
			Caption (str): The name of the formula.
			Formula (str): The formula that is filtered.

		Returns:
			self: This instance with all currently retrieved formulaColumn data using find and the newly added formulaColumn data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the formulaColumn data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Caption=None, Formula=None):
		"""Finds and retrieves formulaColumn data from the server.

		All named parameters support regex and can be used to selectively retrieve formulaColumn data from the server.
		By default the find method takes no parameters and will retrieve all formulaColumn data from the server.

		Args:
			Caption (str): The name of the formula.
			Formula (str): The formula that is filtered.

		Returns:
			self: This instance with matching formulaColumn data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of formulaColumn data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the formulaColumn data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
