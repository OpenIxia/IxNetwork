from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SourceRange(Base):
	"""The SourceRange class encapsulates a user managed sourceRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SourceRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'sourceRange'

	def __init__(self, parent):
		super(SourceRange, self).__init__(parent)

	@property
	def Count(self):
		"""The number of IP addresses in the source range.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def IpFrom(self):
		"""The first IP address in the source range.

		Returns:
			str
		"""
		return self._get_attribute('ipFrom')
	@IpFrom.setter
	def IpFrom(self, value):
		self._set_attribute('ipFrom', value)

	def add(self, Count=None, IpFrom=None):
		"""Adds a new sourceRange node on the server and retrieves it in this instance.

		Args:
			Count (number): The number of IP addresses in the source range.
			IpFrom (str): The first IP address in the source range.

		Returns:
			self: This instance with all currently retrieved sourceRange data using find and the newly added sourceRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the sourceRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, IpFrom=None):
		"""Finds and retrieves sourceRange data from the server.

		All named parameters support regex and can be used to selectively retrieve sourceRange data from the server.
		By default the find method takes no parameters and will retrieve all sourceRange data from the server.

		Args:
			Count (number): The number of IP addresses in the source range.
			IpFrom (str): The first IP address in the source range.

		Returns:
			self: This instance with matching sourceRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of sourceRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the sourceRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
