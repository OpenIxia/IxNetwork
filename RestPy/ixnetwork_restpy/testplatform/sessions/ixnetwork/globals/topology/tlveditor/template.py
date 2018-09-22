from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Template(Base):
	"""The Template class encapsulates a user managed template node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Template property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'template'

	def __init__(self, parent):
		super(Template, self).__init__(parent)

	@property
	def Tlv(self):
		"""An instance of the Tlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlv.Tlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.tlv import Tlv
		return Tlv(self)

	@property
	def Name(self):
		"""The name of the template

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def add(self, Name=None):
		"""Adds a new template node on the server and retrieves it in this instance.

		Args:
			Name (str): The name of the template

		Returns:
			self: This instance with all currently retrieved template data using find and the newly added template data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the template data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Name=None):
		"""Finds and retrieves template data from the server.

		All named parameters support regex and can be used to selectively retrieve template data from the server.
		By default the find method takes no parameters and will retrieve all template data from the server.

		Args:
			Name (str): The name of the template

		Returns:
			self: This instance with matching template data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of template data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the template data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
