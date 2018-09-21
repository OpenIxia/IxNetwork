from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomValue(Base):
	"""The CustomValue class encapsulates a user managed customValue node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomValue property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customValue'

	def __init__(self, parent):
		super(CustomValue, self).__init__(parent)

	@property
	def Percentage(self):
		"""How often this value occurs, as a percentage.

		Returns:
			number
		"""
		return self._get_attribute('percentage')
	@Percentage.setter
	def Percentage(self, value):
		self._set_attribute('percentage', value)

	@property
	def Value(self):
		"""Delay value, in microseconds.

		Returns:
			number
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Percentage=None, Value=None):
		"""Adds a new customValue node on the server and retrieves it in this instance.

		Args:
			Percentage (number): How often this value occurs, as a percentage.
			Value (number): Delay value, in microseconds.

		Returns:
			self: This instance with all currently retrieved customValue data using find and the newly added customValue data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customValue data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Percentage=None, Value=None):
		"""Finds and retrieves customValue data from the server.

		All named parameters support regex and can be used to selectively retrieve customValue data from the server.
		By default the find method takes no parameters and will retrieve all customValue data from the server.

		Args:
			Percentage (number): How often this value occurs, as a percentage.
			Value (number): Delay value, in microseconds.

		Returns:
			self: This instance with matching customValue data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customValue data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customValue data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
