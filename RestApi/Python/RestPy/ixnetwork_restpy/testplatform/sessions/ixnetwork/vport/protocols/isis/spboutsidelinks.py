from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbOutsideLinks(Base):
	"""The SpbOutsideLinks class encapsulates a user managed spbOutsideLinks node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbOutsideLinks property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbOutsideLinks'

	def __init__(self, parent):
		super(SpbOutsideLinks, self).__init__(parent)

	@property
	def ConnectionCol(self):
		"""Signifies the connection between the columns.

		Returns:
			number
		"""
		return self._get_attribute('connectionCol')
	@ConnectionCol.setter
	def ConnectionCol(self, value):
		self._set_attribute('connectionCol', value)

	@property
	def ConnectionRow(self):
		"""Signifies the connection between the rows.

		Returns:
			number
		"""
		return self._get_attribute('connectionRow')
	@ConnectionRow.setter
	def ConnectionRow(self, value):
		self._set_attribute('connectionRow', value)

	@property
	def LinkedRid(self):
		"""Signifies the link between R identifier.

		Returns:
			str
		"""
		return self._get_attribute('linkedRid')
	@LinkedRid.setter
	def LinkedRid(self, value):
		self._set_attribute('linkedRid', value)

	def add(self, ConnectionCol=None, ConnectionRow=None, LinkedRid=None):
		"""Adds a new spbOutsideLinks node on the server and retrieves it in this instance.

		Args:
			ConnectionCol (number): Signifies the connection between the columns.
			ConnectionRow (number): Signifies the connection between the rows.
			LinkedRid (str): Signifies the link between R identifier.

		Returns:
			self: This instance with all currently retrieved spbOutsideLinks data using find and the newly added spbOutsideLinks data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbOutsideLinks data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectionCol=None, ConnectionRow=None, LinkedRid=None):
		"""Finds and retrieves spbOutsideLinks data from the server.

		All named parameters support regex and can be used to selectively retrieve spbOutsideLinks data from the server.
		By default the find method takes no parameters and will retrieve all spbOutsideLinks data from the server.

		Args:
			ConnectionCol (number): Signifies the connection between the columns.
			ConnectionRow (number): Signifies the connection between the rows.
			LinkedRid (str): Signifies the link between R identifier.

		Returns:
			self: This instance with matching spbOutsideLinks data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbOutsideLinks data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbOutsideLinks data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
