from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TunnelHeadTrafficEndPoint(Base):
	"""The TunnelHeadTrafficEndPoint class encapsulates a user managed tunnelHeadTrafficEndPoint node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TunnelHeadTrafficEndPoint property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'tunnelHeadTrafficEndPoint'

	def __init__(self, parent):
		super(TunnelHeadTrafficEndPoint, self).__init__(parent)

	@property
	def EndPointType(self):
		"""IPv4/IPv6 address. It has the same values as of IP Type for traffic item in parent Tail Range.

		Returns:
			str(ipv4|ipv6|17|18)
		"""
		return self._get_attribute('endPointType')
	@EndPointType.setter
	def EndPointType(self, value):
		self._set_attribute('endPointType', value)

	@property
	def InsertExplicitTrafficItem(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('insertExplicitTrafficItem')
	@InsertExplicitTrafficItem.setter
	def InsertExplicitTrafficItem(self, value):
		self._set_attribute('insertExplicitTrafficItem', value)

	@property
	def InsertIpv6ExplicitNull(self):
		"""This causes an IPv6 Explicit NULL to be inserted as the innermost label in addition to learned label when trying to generate IPv6 traffic over the IPv4 LSP. The purpose of this is to route the traffic to the IPv6 Protocol Stack at the egress for routing towards the IPv6 destination.

		Returns:
			bool
		"""
		return self._get_attribute('insertIpv6ExplicitNull')
	@InsertIpv6ExplicitNull.setter
	def InsertIpv6ExplicitNull(self, value):
		self._set_attribute('insertIpv6ExplicitNull', value)

	@property
	def IpCount(self):
		"""Allows value greater than or equal to Tunnel Head IP Count (1 by default). This can be used to simulate traffic from multiple source endpoints to be sent over the LSPs originated from the Head Range.

		Returns:
			number
		"""
		return self._get_attribute('ipCount')
	@IpCount.setter
	def IpCount(self, value):
		self._set_attribute('ipCount', value)

	@property
	def IpStart(self):
		"""The Source IP address, one of IPv4 or IPv6, to be used for traffic to be sent over LSPs from the Head End Point.

		Returns:
			str
		"""
		return self._get_attribute('ipStart')
	@IpStart.setter
	def IpStart(self, value):
		self._set_attribute('ipStart', value)

	def add(self, EndPointType=None, InsertExplicitTrafficItem=None, InsertIpv6ExplicitNull=None, IpCount=None, IpStart=None):
		"""Adds a new tunnelHeadTrafficEndPoint node on the server and retrieves it in this instance.

		Args:
			EndPointType (str(ipv4|ipv6|17|18)): IPv4/IPv6 address. It has the same values as of IP Type for traffic item in parent Tail Range.
			InsertExplicitTrafficItem (bool): NOT DEFINED
			InsertIpv6ExplicitNull (bool): This causes an IPv6 Explicit NULL to be inserted as the innermost label in addition to learned label when trying to generate IPv6 traffic over the IPv4 LSP. The purpose of this is to route the traffic to the IPv6 Protocol Stack at the egress for routing towards the IPv6 destination.
			IpCount (number): Allows value greater than or equal to Tunnel Head IP Count (1 by default). This can be used to simulate traffic from multiple source endpoints to be sent over the LSPs originated from the Head Range.
			IpStart (str): The Source IP address, one of IPv4 or IPv6, to be used for traffic to be sent over LSPs from the Head End Point.

		Returns:
			self: This instance with all currently retrieved tunnelHeadTrafficEndPoint data using find and the newly added tunnelHeadTrafficEndPoint data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the tunnelHeadTrafficEndPoint data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EndPointType=None, InsertExplicitTrafficItem=None, InsertIpv6ExplicitNull=None, IpCount=None, IpStart=None):
		"""Finds and retrieves tunnelHeadTrafficEndPoint data from the server.

		All named parameters support regex and can be used to selectively retrieve tunnelHeadTrafficEndPoint data from the server.
		By default the find method takes no parameters and will retrieve all tunnelHeadTrafficEndPoint data from the server.

		Args:
			EndPointType (str(ipv4|ipv6|17|18)): IPv4/IPv6 address. It has the same values as of IP Type for traffic item in parent Tail Range.
			InsertExplicitTrafficItem (bool): NOT DEFINED
			InsertIpv6ExplicitNull (bool): This causes an IPv6 Explicit NULL to be inserted as the innermost label in addition to learned label when trying to generate IPv6 traffic over the IPv4 LSP. The purpose of this is to route the traffic to the IPv6 Protocol Stack at the egress for routing towards the IPv6 destination.
			IpCount (number): Allows value greater than or equal to Tunnel Head IP Count (1 by default). This can be used to simulate traffic from multiple source endpoints to be sent over the LSPs originated from the Head Range.
			IpStart (str): The Source IP address, one of IPv4 or IPv6, to be used for traffic to be sent over LSPs from the Head End Point.

		Returns:
			self: This instance with matching tunnelHeadTrafficEndPoint data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tunnelHeadTrafficEndPoint data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tunnelHeadTrafficEndPoint data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
