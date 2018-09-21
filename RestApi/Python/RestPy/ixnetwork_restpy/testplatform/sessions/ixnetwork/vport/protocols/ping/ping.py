from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ping(Base):
	"""The Ping class encapsulates a user managed ping node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ping property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ping'

	def __init__(self, parent):
		super(Ping, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables IPv4 PING transmission and reception for this port. PING messages are IPv4 ICMP messages of type Echo Request. Responses are IPv4 ICMP message of type Echo Response.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	def add(self, Enabled=None):
		"""Adds a new ping node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables IPv4 PING transmission and reception for this port. PING messages are IPv4 ICMP messages of type Echo Request. Responses are IPv4 ICMP message of type Echo Response.

		Returns:
			self: This instance with all currently retrieved ping data using find and the newly added ping data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ping data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None):
		"""Finds and retrieves ping data from the server.

		All named parameters support regex and can be used to selectively retrieve ping data from the server.
		By default the find method takes no parameters and will retrieve all ping data from the server.

		Args:
			Enabled (bool): Enables IPv4 PING transmission and reception for this port. PING messages are IPv4 ICMP messages of type Echo Request. Responses are IPv4 ICMP message of type Echo Response.

		Returns:
			self: This instance with matching ping data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ping data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ping data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
