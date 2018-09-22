from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DiscoveredInterface(Base):
	"""The DiscoveredInterface class encapsulates a system managed discoveredInterface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DiscoveredInterface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'discoveredInterface'

	def __init__(self, parent):
		super(DiscoveredInterface, self).__init__(parent)

	@property
	def InterfaceName(self):
		"""Represents the interface name

		Returns:
			str
		"""
		return self._get_attribute('interfaceName')

	@property
	def State(self):
		"""Represents the interface state

		Returns:
			str(assigned|available|unusable)
		"""
		return self._get_attribute('state')

	def find(self, InterfaceName=None, State=None):
		"""Finds and retrieves discoveredInterface data from the server.

		All named parameters support regex and can be used to selectively retrieve discoveredInterface data from the server.
		By default the find method takes no parameters and will retrieve all discoveredInterface data from the server.

		Args:
			InterfaceName (str): Represents the interface name
			State (str(assigned|available|unusable)): Represents the interface state

		Returns:
			self: This instance with matching discoveredInterface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of discoveredInterface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the discoveredInterface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
