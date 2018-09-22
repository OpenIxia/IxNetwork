from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Stack(Base):
	"""The Stack class encapsulates a system managed stack node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Stack property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'stack'

	def __init__(self, parent):
		super(Stack, self).__init__(parent)

	@property
	def Field(self):
		"""An instance of the Field class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.field.field.Field)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.field.field import Field
		return Field(self)

	@property
	def DisplayName(self):
		"""Refers to the name of the stack.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	def find(self, DisplayName=None):
		"""Finds and retrieves stack data from the server.

		All named parameters support regex and can be used to selectively retrieve stack data from the server.
		By default the find method takes no parameters and will retrieve all stack data from the server.

		Args:
			DisplayName (str): Refers to the name of the stack.

		Returns:
			self: This instance with matching stack data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of stack data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the stack data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
