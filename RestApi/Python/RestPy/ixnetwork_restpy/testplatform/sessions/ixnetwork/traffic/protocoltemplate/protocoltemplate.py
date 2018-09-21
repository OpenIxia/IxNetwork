from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ProtocolTemplate(Base):
	"""The ProtocolTemplate class encapsulates a system managed protocolTemplate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ProtocolTemplate property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'protocolTemplate'

	def __init__(self, parent):
		super(ProtocolTemplate, self).__init__(parent)

	@property
	def Field(self):
		"""An instance of the Field class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.field.field.Field)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.field.field import Field
		return Field(self)

	@property
	def DisplayName(self):
		"""The display name of the template.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def StackTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('stackTypeId')

	@property
	def TemplateName(self):
		"""Indicates the protocol template name that is added to a packet.

		Returns:
			str
		"""
		return self._get_attribute('templateName')

	def find(self, DisplayName=None, StackTypeId=None, TemplateName=None):
		"""Finds and retrieves protocolTemplate data from the server.

		All named parameters support regex and can be used to selectively retrieve protocolTemplate data from the server.
		By default the find method takes no parameters and will retrieve all protocolTemplate data from the server.

		Args:
			DisplayName (str): The display name of the template.
			StackTypeId (str): 
			TemplateName (str): Indicates the protocol template name that is added to a packet.

		Returns:
			self: This instance with matching protocolTemplate data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of protocolTemplate data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the protocolTemplate data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
