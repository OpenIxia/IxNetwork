from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistic(Base):
	"""The Statistic class encapsulates a user managed statistic node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Statistic property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'statistic'

	def __init__(self, parent):
		super(Statistic, self).__init__(parent)

	@property
	def Enable(self):
		"""Enable/Disable monitoring for the current statistic.

		Returns:
			bool
		"""
		return self._get_attribute('enable')
	@Enable.setter
	def Enable(self, value):
		self._set_attribute('enable', value)

	@property
	def Name(self):
		"""The name of the statistic that is being monitored.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Notes(self):
		"""Additional notes that explain what is being monitored for this statistic.

		Returns:
			str
		"""
		return self._get_attribute('notes')

	@property
	def Operator(self):
		"""The operator that is being used to compare the actual value of the statistic with the configured threshold.

		Returns:
			str
		"""
		return self._get_attribute('operator')

	@property
	def Unit(self):
		"""The measurement unit being used for this statistic.

		Returns:
			str
		"""
		return self._get_attribute('unit')

	@property
	def Value(self):
		"""The threshold for the current statistic. Exceeding this value will trigger a warning if monitoring is enabled for this statistic.

		Returns:
			number
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Enable=None, Value=None):
		"""Adds a new statistic node on the server and retrieves it in this instance.

		Args:
			Enable (bool): Enable/Disable monitoring for the current statistic.
			Value (number): The threshold for the current statistic. Exceeding this value will trigger a warning if monitoring is enabled for this statistic.

		Returns:
			self: This instance with all currently retrieved statistic data using find and the newly added statistic data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the statistic data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enable=None, Name=None, Notes=None, Operator=None, Unit=None, Value=None):
		"""Finds and retrieves statistic data from the server.

		All named parameters support regex and can be used to selectively retrieve statistic data from the server.
		By default the find method takes no parameters and will retrieve all statistic data from the server.

		Args:
			Enable (bool): Enable/Disable monitoring for the current statistic.
			Name (str): The name of the statistic that is being monitored.
			Notes (str): Additional notes that explain what is being monitored for this statistic.
			Operator (str): The operator that is being used to compare the actual value of the statistic with the configured threshold.
			Unit (str): The measurement unit being used for this statistic.
			Value (number): The threshold for the current statistic. Exceeding this value will trigger a warning if monitoring is enabled for this statistic.

		Returns:
			self: This instance with matching statistic data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of statistic data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the statistic data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
