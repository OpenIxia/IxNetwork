from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Tag(Base):
	"""The Tag class encapsulates a user managed tag node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Tag property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'tag'

	def __init__(self, parent):
		super(Tag, self).__init__(parent)

	@property
	def __id__(self):
		"""the tag ids that this entity will use/publish

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('__id__')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Enabled(self):
		"""Enables/disables tags

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Name(self):
		"""specifies the name of the tag the entity will be part of

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def add(self, Enabled=None, Name=None):
		"""Adds a new tag node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables/disables tags
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			self: This instance with all currently retrieved tag data using find and the newly added tag data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the tag data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, Enabled=None, Name=None):
		"""Finds and retrieves tag data from the server.

		All named parameters support regex and can be used to selectively retrieve tag data from the server.
		By default the find method takes no parameters and will retrieve all tag data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			Enabled (bool): Enables/disables tags
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			self: This instance with matching tag data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tag data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tag data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
