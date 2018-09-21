from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Predefined(Base):
	"""The Predefined class encapsulates a user managed predefined node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Predefined property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'predefined'

	def __init__(self, parent):
		super(Predefined, self).__init__(parent)

	@property
	def ActionTemplate(self):
		"""An instance of the ActionTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.actiontemplate.ActionTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.actiontemplate import ActionTemplate
		return ActionTemplate(self)

	def add(self):
		"""Adds a new predefined node on the server and retrieves it in this instance.

		Returns:
			self: This instance with all currently retrieved predefined data using find and the newly added predefined data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the predefined data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self):
		"""Finds and retrieves predefined data from the server.

		All named parameters support regex and can be used to selectively retrieve predefined data from the server.
		By default the find method takes no parameters and will retrieve all predefined data from the server.

		Returns:
			self: This instance with matching predefined data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of predefined data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the predefined data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
