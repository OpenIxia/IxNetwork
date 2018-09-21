from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Source(Base):
	"""The Source class encapsulates a user managed source node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Source property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'source'

	def __init__(self, parent):
		super(Source, self).__init__(parent)

	@property
	def SourceRangeCount(self):
		"""The number of IP addresses in the source range.

		Returns:
			number
		"""
		return self._get_attribute('sourceRangeCount')
	@SourceRangeCount.setter
	def SourceRangeCount(self, value):
		self._set_attribute('sourceRangeCount', value)

	@property
	def SourceRangeStart(self):
		"""The first IP address in the source range.

		Returns:
			str
		"""
		return self._get_attribute('sourceRangeStart')
	@SourceRangeStart.setter
	def SourceRangeStart(self, value):
		self._set_attribute('sourceRangeStart', value)

	def add(self, SourceRangeCount=None, SourceRangeStart=None):
		"""Adds a new source node on the server and retrieves it in this instance.

		Args:
			SourceRangeCount (number): The number of IP addresses in the source range.
			SourceRangeStart (str): The first IP address in the source range.

		Returns:
			self: This instance with all currently retrieved source data using find and the newly added source data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the source data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, SourceRangeCount=None, SourceRangeStart=None):
		"""Finds and retrieves source data from the server.

		All named parameters support regex and can be used to selectively retrieve source data from the server.
		By default the find method takes no parameters and will retrieve all source data from the server.

		Args:
			SourceRangeCount (number): The number of IP addresses in the source range.
			SourceRangeStart (str): The first IP address in the source range.

		Returns:
			self: This instance with matching source data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of source data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the source data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
