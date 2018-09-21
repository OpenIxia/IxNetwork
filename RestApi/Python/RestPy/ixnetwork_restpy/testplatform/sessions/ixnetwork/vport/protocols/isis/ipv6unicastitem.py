from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv6UnicastItem(Base):
	"""The Ipv6UnicastItem class encapsulates a system managed ipv6UnicastItem node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv6UnicastItem property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv6UnicastItem'

	def __init__(self, parent):
		super(Ipv6UnicastItem, self).__init__(parent)

	@property
	def Ipv6UnicastSourceAddress(self):
		"""This indicates the IPv6 Source, if any, associated with the IPv6 Multicast Group Address.

		Returns:
			str
		"""
		return self._get_attribute('ipv6UnicastSourceAddress')

	def find(self, Ipv6UnicastSourceAddress=None):
		"""Finds and retrieves ipv6UnicastItem data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv6UnicastItem data from the server.
		By default the find method takes no parameters and will retrieve all ipv6UnicastItem data from the server.

		Args:
			Ipv6UnicastSourceAddress (str): This indicates the IPv6 Source, if any, associated with the IPv6 Multicast Group Address.

		Returns:
			self: This instance with matching ipv6UnicastItem data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv6UnicastItem data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv6UnicastItem data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
