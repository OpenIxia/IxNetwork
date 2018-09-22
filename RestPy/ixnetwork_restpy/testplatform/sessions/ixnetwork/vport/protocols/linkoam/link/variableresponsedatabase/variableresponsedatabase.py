from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VariableResponseDatabase(Base):
	"""The VariableResponseDatabase class encapsulates a user managed variableResponseDatabase node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VariableResponseDatabase property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'variableResponseDatabase'

	def __init__(self, parent):
		super(VariableResponseDatabase, self).__init__(parent)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def VariableBranch(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('variableBranch')
	@VariableBranch.setter
	def VariableBranch(self, value):
		self._set_attribute('variableBranch', value)

	@property
	def VariableIndication(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('variableIndication')
	@VariableIndication.setter
	def VariableIndication(self, value):
		self._set_attribute('variableIndication', value)

	@property
	def VariableLeaf(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('variableLeaf')
	@VariableLeaf.setter
	def VariableLeaf(self, value):
		self._set_attribute('variableLeaf', value)

	@property
	def VariableValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('variableValue')
	@VariableValue.setter
	def VariableValue(self, value):
		self._set_attribute('variableValue', value)

	@property
	def VariableWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('variableWidth')
	@VariableWidth.setter
	def VariableWidth(self, value):
		self._set_attribute('variableWidth', value)

	def add(self, Enabled=None, VariableBranch=None, VariableIndication=None, VariableLeaf=None, VariableValue=None, VariableWidth=None):
		"""Adds a new variableResponseDatabase node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			VariableBranch (number): 
			VariableIndication (bool): 
			VariableLeaf (number): 
			VariableValue (str): 
			VariableWidth (number): 

		Returns:
			self: This instance with all currently retrieved variableResponseDatabase data using find and the newly added variableResponseDatabase data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the variableResponseDatabase data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, VariableBranch=None, VariableIndication=None, VariableLeaf=None, VariableValue=None, VariableWidth=None):
		"""Finds and retrieves variableResponseDatabase data from the server.

		All named parameters support regex and can be used to selectively retrieve variableResponseDatabase data from the server.
		By default the find method takes no parameters and will retrieve all variableResponseDatabase data from the server.

		Args:
			Enabled (bool): 
			VariableBranch (number): 
			VariableIndication (bool): 
			VariableLeaf (number): 
			VariableValue (str): 
			VariableWidth (number): 

		Returns:
			self: This instance with matching variableResponseDatabase data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of variableResponseDatabase data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the variableResponseDatabase data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
