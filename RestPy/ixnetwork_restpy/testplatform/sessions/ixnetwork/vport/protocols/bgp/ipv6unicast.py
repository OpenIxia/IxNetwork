from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv6Unicast(Base):
	"""The Ipv6Unicast class encapsulates a system managed ipv6Unicast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv6Unicast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv6Unicast'

	def __init__(self, parent):
		super(Ipv6Unicast, self).__init__(parent)

	@property
	def AsPath(self):
		"""Indicates the local IP address of the BGP router.

		Returns:
			str
		"""
		return self._get_attribute('asPath')

	@property
	def Community(self):
		"""The BGP Community attribute to be added to the BGP entry.

		Returns:
			str
		"""
		return self._get_attribute('community')

	@property
	def IpPrefix(self):
		"""The route IP prefix.

		Returns:
			str
		"""
		return self._get_attribute('ipPrefix')

	@property
	def LocalPreference(self):
		"""Indicates the value of the local preference attribute.

		Returns:
			number
		"""
		return self._get_attribute('localPreference')

	@property
	def MultiExitDiscriminator(self):
		"""A metric field of the route file.

		Returns:
			number
		"""
		return self._get_attribute('multiExitDiscriminator')

	@property
	def Neighbor(self):
		"""The descriptive identifier for the BGP neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def NextHop(self):
		"""A 4-octet IP address which indicates the next hop.

		Returns:
			str
		"""
		return self._get_attribute('nextHop')

	@property
	def OriginType(self):
		"""An indication of where the route entry originated.

		Returns:
			str
		"""
		return self._get_attribute('originType')

	@property
	def PrefixLength(self):
		"""The length of the route IP prefix, in bytes.

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')

	def find(self, AsPath=None, Community=None, IpPrefix=None, LocalPreference=None, MultiExitDiscriminator=None, Neighbor=None, NextHop=None, OriginType=None, PrefixLength=None):
		"""Finds and retrieves ipv6Unicast data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv6Unicast data from the server.
		By default the find method takes no parameters and will retrieve all ipv6Unicast data from the server.

		Args:
			AsPath (str): Indicates the local IP address of the BGP router.
			Community (str): The BGP Community attribute to be added to the BGP entry.
			IpPrefix (str): The route IP prefix.
			LocalPreference (number): Indicates the value of the local preference attribute.
			MultiExitDiscriminator (number): A metric field of the route file.
			Neighbor (str): The descriptive identifier for the BGP neighbor.
			NextHop (str): A 4-octet IP address which indicates the next hop.
			OriginType (str): An indication of where the route entry originated.
			PrefixLength (number): The length of the route IP prefix, in bytes.

		Returns:
			self: This instance with matching ipv6Unicast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv6Unicast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv6Unicast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
