from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Container(Base):
	"""The Container class encapsulates a system managed container node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Container property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'container'

	def __init__(self, parent):
		super(Container, self).__init__(parent)

	@property
	def Object(self):
		"""An instance of the Object class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.object.Object)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.object import Object
		return Object(self)

	@property
	def IsEnabled(self):
		"""Enables/disables this field

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

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

	def find(self, IsEnabled=None, Name=None):
		"""Finds and retrieves container data from the server.

		All named parameters support regex and can be used to selectively retrieve container data from the server.
		By default the find method takes no parameters and will retrieve all container data from the server.

		Args:
			IsEnabled (bool): Enables/disables this field
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
