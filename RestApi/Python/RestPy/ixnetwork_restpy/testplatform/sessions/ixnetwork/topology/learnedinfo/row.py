from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Row(Base):
	"""The Row class encapsulates a system managed row node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Row property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'row'

	def __init__(self, parent):
		super(Row, self).__init__(parent)

	@property
	def Value(self):
		"""A learned information value

		Returns:
			str
		"""
		return self._get_attribute('value')

	def find(self, Value=None):
		"""Finds and retrieves row data from the server.

		All named parameters support regex and can be used to selectively retrieve row data from the server.
		By default the find method takes no parameters and will retrieve all row data from the server.

		Args:
			Value (str): A learned information value

		Returns:
			self: This instance with matching row data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of row data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the row data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
