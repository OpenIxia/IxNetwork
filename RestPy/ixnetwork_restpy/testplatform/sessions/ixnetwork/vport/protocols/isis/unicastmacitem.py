from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UnicastMacItem(Base):
	"""The UnicastMacItem class encapsulates a system managed unicastMacItem node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UnicastMacItem property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'unicastMacItem'

	def __init__(self, parent):
		super(UnicastMacItem, self).__init__(parent)

	@property
	def UnicastSourceMacAddress(self):
		"""This indicates the MAC Source, if any, associated with the MAC Multicast Group Address.

		Returns:
			str
		"""
		return self._get_attribute('unicastSourceMacAddress')

	def find(self, UnicastSourceMacAddress=None):
		"""Finds and retrieves unicastMacItem data from the server.

		All named parameters support regex and can be used to selectively retrieve unicastMacItem data from the server.
		By default the find method takes no parameters and will retrieve all unicastMacItem data from the server.

		Args:
			UnicastSourceMacAddress (str): This indicates the MAC Source, if any, associated with the MAC Multicast Group Address.

		Returns:
			self: This instance with matching unicastMacItem data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of unicastMacItem data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the unicastMacItem data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
