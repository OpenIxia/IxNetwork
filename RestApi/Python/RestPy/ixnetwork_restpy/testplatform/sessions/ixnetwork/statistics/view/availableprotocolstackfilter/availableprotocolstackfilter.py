from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableProtocolStackFilter(Base):
	"""The AvailableProtocolStackFilter class encapsulates a system managed availableProtocolStackFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableProtocolStackFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'availableProtocolStackFilter'

	def __init__(self, parent):
		super(AvailableProtocolStackFilter, self).__init__(parent)

	@property
	def Name(self):
		"""The name of the protocol stack ranges.

		Returns:
			str
		"""
		return self._get_attribute('name')

	def find(self, Name=None):
		"""Finds and retrieves availableProtocolStackFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve availableProtocolStackFilter data from the server.
		By default the find method takes no parameters and will retrieve all availableProtocolStackFilter data from the server.

		Args:
			Name (str): The name of the protocol stack ranges.

		Returns:
			self: This instance with matching availableProtocolStackFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of availableProtocolStackFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the availableProtocolStackFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
