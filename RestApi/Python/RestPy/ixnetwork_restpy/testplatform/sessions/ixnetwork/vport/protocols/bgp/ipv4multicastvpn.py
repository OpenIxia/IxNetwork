from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv4MulticastVpn(Base):
	"""The Ipv4MulticastVpn class encapsulates a system managed ipv4MulticastVpn node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4MulticastVpn property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4MulticastVpn'

	def __init__(self, parent):
		super(Ipv4MulticastVpn, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def AddressFamily(self):
		"""(read only) The address family identifier value.

		Returns:
			number
		"""
		return self._get_attribute('addressFamily')

	@property
	def AddressLength(self):
		"""(read only) The length of the address.

		Returns:
			number
		"""
		return self._get_attribute('addressLength')

	@property
	def CMcastRouteType(self):
		"""The c-multicast route type.

		Returns:
			str
		"""
		return self._get_attribute('cMcastRouteType')

	@property
	def GroupAddress(self):
		"""The IPv4 Multicast group address in the range of group addresses included in this Register message.

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')

	@property
	def Neighbor(self):
		"""The neighbor address.

		Returns:
			str
		"""
		return self._get_attribute('neighbor')

	@property
	def OpaqueLength(self):
		"""(read only) Indicates the opaque length.

		Returns:
			number
		"""
		return self._get_attribute('opaqueLength')

	@property
	def OriginatingRouter(self):
		"""The originating router address.

		Returns:
			str
		"""
		return self._get_attribute('originatingRouter')

	@property
	def RootAddress(self):
		"""(read only) Indicates the root address.

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')

	@property
	def RouteDistinguisher(self):
		"""The route distinguisher for the route, for use with IPv4 multicast VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisher')

	@property
	def RouteKeyGroupAddress(self):
		"""The key group address of the route.

		Returns:
			str
		"""
		return self._get_attribute('routeKeyGroupAddress')

	@property
	def RouteKeyOriginatingRouter(self):
		"""The key originating address of the router.

		Returns:
			str
		"""
		return self._get_attribute('routeKeyOriginatingRouter')

	@property
	def RouteKeyRouteDistinguisher(self):
		"""The key route distinguisher for the route, for use with IPv4 multicast VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeKeyRouteDistinguisher')

	@property
	def RouteKeyRsvpP2mpExtendedTunnelId(self):
		"""The key rsvp p2mp extended tunnel id for the route, for use with IPv4 multicast VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeKeyRsvpP2mpExtendedTunnelId')

	@property
	def RouteKeyRsvpP2mpId(self):
		"""The key rsvp p2mp id for the route, for use with IPv4 multicast VPN address types.

		Returns:
			number
		"""
		return self._get_attribute('routeKeyRsvpP2mpId')

	@property
	def RouteKeyRsvpP2mpTunnelId(self):
		"""The key rsvp p2mp tunnel id for the route, for use with IPv4 multicast VPN address types.

		Returns:
			number
		"""
		return self._get_attribute('routeKeyRsvpP2mpTunnelId')

	@property
	def RouteKeySourceAddress(self):
		"""The key source address for the route, for use with IPv4 multicast VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeKeySourceAddress')

	@property
	def RouteKeyTunnelType(self):
		"""The key tunnel type for the route, for use with IPv4 multicast VPN address types.

		Returns:
			str
		"""
		return self._get_attribute('routeKeyTunnelType')

	@property
	def RouteKeyUpstreamLabel(self):
		"""The key upstream label for the route, for use with IPv4 multicast VPN address types.

		Returns:
			number
		"""
		return self._get_attribute('routeKeyUpstreamLabel')

	@property
	def RouteType(self):
		"""The route type.

		Returns:
			str
		"""
		return self._get_attribute('routeType')

	@property
	def RsvpP2mpExtendedTunnelId(self):
		"""The rsvp p2mp extended tunnel id.

		Returns:
			str
		"""
		return self._get_attribute('rsvpP2mpExtendedTunnelId')

	@property
	def RsvpP2mpId(self):
		"""The rsvp p2mp id.

		Returns:
			number
		"""
		return self._get_attribute('rsvpP2mpId')

	@property
	def RsvpP2mpTunnelId(self):
		"""The rsvp p2mp tunnel id.

		Returns:
			number
		"""
		return self._get_attribute('rsvpP2mpTunnelId')

	@property
	def SourceAddress(self):
		"""The source address.

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')

	@property
	def SourceAs(self):
		"""The source AS number.

		Returns:
			number
		"""
		return self._get_attribute('sourceAs')

	@property
	def TunnelType(self):
		"""The tunnel type.

		Returns:
			str
		"""
		return self._get_attribute('tunnelType')

	@property
	def UpstreamLabel(self):
		"""The upstream label.

		Returns:
			number
		"""
		return self._get_attribute('upstreamLabel')

	def find(self, AddressFamily=None, AddressLength=None, CMcastRouteType=None, GroupAddress=None, Neighbor=None, OpaqueLength=None, OriginatingRouter=None, RootAddress=None, RouteDistinguisher=None, RouteKeyGroupAddress=None, RouteKeyOriginatingRouter=None, RouteKeyRouteDistinguisher=None, RouteKeyRsvpP2mpExtendedTunnelId=None, RouteKeyRsvpP2mpId=None, RouteKeyRsvpP2mpTunnelId=None, RouteKeySourceAddress=None, RouteKeyTunnelType=None, RouteKeyUpstreamLabel=None, RouteType=None, RsvpP2mpExtendedTunnelId=None, RsvpP2mpId=None, RsvpP2mpTunnelId=None, SourceAddress=None, SourceAs=None, TunnelType=None, UpstreamLabel=None):
		"""Finds and retrieves ipv4MulticastVpn data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4MulticastVpn data from the server.
		By default the find method takes no parameters and will retrieve all ipv4MulticastVpn data from the server.

		Args:
			AddressFamily (number): (read only) The address family identifier value.
			AddressLength (number): (read only) The length of the address.
			CMcastRouteType (str): The c-multicast route type.
			GroupAddress (str): The IPv4 Multicast group address in the range of group addresses included in this Register message.
			Neighbor (str): The neighbor address.
			OpaqueLength (number): (read only) Indicates the opaque length.
			OriginatingRouter (str): The originating router address.
			RootAddress (str): (read only) Indicates the root address.
			RouteDistinguisher (str): The route distinguisher for the route, for use with IPv4 multicast VPN address types.
			RouteKeyGroupAddress (str): The key group address of the route.
			RouteKeyOriginatingRouter (str): The key originating address of the router.
			RouteKeyRouteDistinguisher (str): The key route distinguisher for the route, for use with IPv4 multicast VPN address types.
			RouteKeyRsvpP2mpExtendedTunnelId (str): The key rsvp p2mp extended tunnel id for the route, for use with IPv4 multicast VPN address types.
			RouteKeyRsvpP2mpId (number): The key rsvp p2mp id for the route, for use with IPv4 multicast VPN address types.
			RouteKeyRsvpP2mpTunnelId (number): The key rsvp p2mp tunnel id for the route, for use with IPv4 multicast VPN address types.
			RouteKeySourceAddress (str): The key source address for the route, for use with IPv4 multicast VPN address types.
			RouteKeyTunnelType (str): The key tunnel type for the route, for use with IPv4 multicast VPN address types.
			RouteKeyUpstreamLabel (number): The key upstream label for the route, for use with IPv4 multicast VPN address types.
			RouteType (str): The route type.
			RsvpP2mpExtendedTunnelId (str): The rsvp p2mp extended tunnel id.
			RsvpP2mpId (number): The rsvp p2mp id.
			RsvpP2mpTunnelId (number): The rsvp p2mp tunnel id.
			SourceAddress (str): The source address.
			SourceAs (number): The source AS number.
			TunnelType (str): The tunnel type.
			UpstreamLabel (number): The upstream label.

		Returns:
			self: This instance with matching ipv4MulticastVpn data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4MulticastVpn data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4MulticastVpn data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
