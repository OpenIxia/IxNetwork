from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv4Prefixes(Base):
	"""The Ipv4Prefixes class encapsulates a system managed ipv4Prefixes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4Prefixes property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4Prefixes'

	def __init__(self, parent):
		super(Ipv4Prefixes, self).__init__(parent)

	@property
	def Age(self):
		"""The time since last refreshed.

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def HostName(self):
		"""The host name as retrieved from the related packets.

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def Ipv4Prefix(self):
		"""Mask width of IPv4 Prefix.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Prefix')

	@property
	def LearnedVia(self):
		"""Learned via L1 Adjacency/L2 Adjacency.

		Returns:
			str
		"""
		return self._get_attribute('learnedVia')

	@property
	def LspId(self):
		"""The LSP number.

		Returns:
			str
		"""
		return self._get_attribute('lspId')

	@property
	def Metric(self):
		"""The route metric.

		Returns:
			number
		"""
		return self._get_attribute('metric')

	@property
	def SequenceNumber(self):
		"""Sequence number of the LSP containing the route.

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	def find(self, Age=None, HostName=None, Ipv4Prefix=None, LearnedVia=None, LspId=None, Metric=None, SequenceNumber=None):
		"""Finds and retrieves ipv4Prefixes data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4Prefixes data from the server.
		By default the find method takes no parameters and will retrieve all ipv4Prefixes data from the server.

		Args:
			Age (number): The time since last refreshed.
			HostName (str): The host name as retrieved from the related packets.
			Ipv4Prefix (str): Mask width of IPv4 Prefix.
			LearnedVia (str): Learned via L1 Adjacency/L2 Adjacency.
			LspId (str): The LSP number.
			Metric (number): The route metric.
			SequenceNumber (number): Sequence number of the LSP containing the route.

		Returns:
			self: This instance with matching ipv4Prefixes data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4Prefixes data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4Prefixes data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
