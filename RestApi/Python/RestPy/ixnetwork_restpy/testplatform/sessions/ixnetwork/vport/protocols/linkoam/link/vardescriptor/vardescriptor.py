from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VarDescriptor(Base):
	"""The VarDescriptor class encapsulates a user managed varDescriptor node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VarDescriptor property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'varDescriptor'

	def __init__(self, parent):
		super(VarDescriptor, self).__init__(parent)

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
	def VariableLeaf(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('variableLeaf')
	@VariableLeaf.setter
	def VariableLeaf(self, value):
		self._set_attribute('variableLeaf', value)

	def add(self, VariableBranch=None, VariableLeaf=None):
		"""Adds a new varDescriptor node on the server and retrieves it in this instance.

		Args:
			VariableBranch (number): 
			VariableLeaf (number): 

		Returns:
			self: This instance with all currently retrieved varDescriptor data using find and the newly added varDescriptor data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the varDescriptor data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, VariableBranch=None, VariableLeaf=None):
		"""Finds and retrieves varDescriptor data from the server.

		All named parameters support regex and can be used to selectively retrieve varDescriptor data from the server.
		By default the find method takes no parameters and will retrieve all varDescriptor data from the server.

		Args:
			VariableBranch (number): 
			VariableLeaf (number): 

		Returns:
			self: This instance with matching varDescriptor data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of varDescriptor data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the varDescriptor data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
