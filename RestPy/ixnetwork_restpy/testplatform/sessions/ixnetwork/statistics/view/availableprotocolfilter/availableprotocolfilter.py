from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableProtocolFilter(Base):
	"""The AvailableProtocolFilter class encapsulates a system managed availableProtocolFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableProtocolFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'availableProtocolFilter'

	def __init__(self, parent):
		super(AvailableProtocolFilter, self).__init__(parent)

	@property
	def Name(self):
		"""The unique identifier of the object.

		Returns:
			str
		"""
		return self._get_attribute('name')

	def find(self, Name=None):
		"""Finds and retrieves availableProtocolFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve availableProtocolFilter data from the server.
		By default the find method takes no parameters and will retrieve all availableProtocolFilter data from the server.

		Args:
			Name (str): The unique identifier of the object.

		Returns:
			self: This instance with matching availableProtocolFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of availableProtocolFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the availableProtocolFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
