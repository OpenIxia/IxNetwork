from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VariableRequestLearnedInfo(Base):
	"""The VariableRequestLearnedInfo class encapsulates a system managed variableRequestLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VariableRequestLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'variableRequestLearnedInfo'

	def __init__(self, parent):
		super(VariableRequestLearnedInfo, self).__init__(parent)

	@property
	def VariableBranch(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('variableBranch')

	@property
	def VariableIndication(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('variableIndication')

	@property
	def VariableLeaf(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('variableLeaf')

	@property
	def VariableValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('variableValue')

	@property
	def VariableWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('variableWidth')

	def find(self, VariableBranch=None, VariableIndication=None, VariableLeaf=None, VariableValue=None, VariableWidth=None):
		"""Finds and retrieves variableRequestLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve variableRequestLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all variableRequestLearnedInfo data from the server.

		Args:
			VariableBranch (str): 
			VariableIndication (bool): 
			VariableLeaf (str): 
			VariableValue (str): 
			VariableWidth (number): 

		Returns:
			self: This instance with matching variableRequestLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of variableRequestLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the variableRequestLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
