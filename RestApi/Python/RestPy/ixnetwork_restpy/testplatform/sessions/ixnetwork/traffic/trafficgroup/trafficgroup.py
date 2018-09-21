from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrafficGroup(Base):
	"""The TrafficGroup class encapsulates a user managed trafficGroup node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrafficGroup property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'trafficGroup'

	def __init__(self, parent):
		super(TrafficGroup, self).__init__(parent)

	@property
	def Name(self):
		"""Name of the traffic item.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def add(self, Name=None):
		"""Adds a new trafficGroup node on the server and retrieves it in this instance.

		Args:
			Name (str): Name of the traffic item.

		Returns:
			self: This instance with all currently retrieved trafficGroup data using find and the newly added trafficGroup data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the trafficGroup data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Name=None):
		"""Finds and retrieves trafficGroup data from the server.

		All named parameters support regex and can be used to selectively retrieve trafficGroup data from the server.
		By default the find method takes no parameters and will retrieve all trafficGroup data from the server.

		Args:
			Name (str): Name of the traffic item.

		Returns:
			self: This instance with matching trafficGroup data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trafficGroup data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trafficGroup data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
