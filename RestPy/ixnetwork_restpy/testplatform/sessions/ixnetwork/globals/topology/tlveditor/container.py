from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Container(Base):
	"""The Container class encapsulates a user managed container node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Container property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'container'

	def __init__(self, parent):
		super(Container, self).__init__(parent)

	@property
	def Object(self):
		"""An instance of the Object class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object.Object)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object import Object
		return Object(self)

	@property
	def Description(self):
		"""Description of the tlv

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def IsEditable(self):
		"""Indicates whether this is editable or not

		Returns:
			bool
		"""
		return self._get_attribute('isEditable')
	@IsEditable.setter
	def IsEditable(self, value):
		self._set_attribute('isEditable', value)

	@property
	def IsRepeatable(self):
		"""Flag indicating whether this is repeatable or not

		Returns:
			bool
		"""
		return self._get_attribute('isRepeatable')
	@IsRepeatable.setter
	def IsRepeatable(self, value):
		self._set_attribute('isRepeatable', value)

	@property
	def IsRequired(self):
		"""Flag indicating whether this is required or not

		Returns:
			bool
		"""
		return self._get_attribute('isRequired')
	@IsRequired.setter
	def IsRequired(self, value):
		self._set_attribute('isRequired', value)

	@property
	def Name(self):
		"""Name of the tlv

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def add(self, Description=None, IsEditable=None, IsRepeatable=None, IsRequired=None, Name=None):
		"""Adds a new container node on the server and retrieves it in this instance.

		Args:
			Description (str): Description of the tlv
			IsEditable (bool): Indicates whether this is editable or not
			IsRepeatable (bool): Flag indicating whether this is repeatable or not
			IsRequired (bool): Flag indicating whether this is required or not
			Name (str): Name of the tlv

		Returns:
			self: This instance with all currently retrieved container data using find and the newly added container data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the container data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Description=None, IsEditable=None, IsRepeatable=None, IsRequired=None, Name=None):
		"""Finds and retrieves container data from the server.

		All named parameters support regex and can be used to selectively retrieve container data from the server.
		By default the find method takes no parameters and will retrieve all container data from the server.

		Args:
			Description (str): Description of the tlv
			IsEditable (bool): Indicates whether this is editable or not
			IsRepeatable (bool): Flag indicating whether this is repeatable or not
			IsRequired (bool): Flag indicating whether this is required or not
			Name (str): Name of the tlv

		Returns:
			self: This instance with matching container data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of container data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the container data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
