from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Capabilities(Base):
	"""The Capabilities class encapsulates a required capabilities node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Capabilities property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'capabilities'

	def __init__(self, parent):
		super(Capabilities, self).__init__(parent)

	@property
	def AdVpls(self):
		"""If true, enables the BGP autodiscovery VPLS tunnels.

		Returns:
			bool
		"""
		return self._get_attribute('adVpls')
	@AdVpls.setter
	def AdVpls(self, value):
		self._set_attribute('adVpls', value)

	@property
	def Evpn(self):
		"""If enabled, then this BGP peer range supports BGP MPLS Based Ethernet VPN per draft-ietf-l2vpn-evpn-03. Default value is false.

		Returns:
			bool
		"""
		return self._get_attribute('evpn')
	@Evpn.setter
	def Evpn(self, value):
		self._set_attribute('evpn', value)

	@property
	def FetchDetailedIpV4UnicastInfo(self):
		"""If enabled, this BGP router displays complete information about the Ipv4UnicastInfo.

		Returns:
			bool
		"""
		return self._get_attribute('fetchDetailedIpV4UnicastInfo')
	@FetchDetailedIpV4UnicastInfo.setter
	def FetchDetailedIpV4UnicastInfo(self, value):
		self._set_attribute('fetchDetailedIpV4UnicastInfo', value)

	@property
	def FetchDetailedIpV6UnicastInfo(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('fetchDetailedIpV6UnicastInfo')
	@FetchDetailedIpV6UnicastInfo.setter
	def FetchDetailedIpV6UnicastInfo(self, value):
		self._set_attribute('fetchDetailedIpV6UnicastInfo', value)

	@property
	def IpV4Mpls(self):
		"""If true, learns IPv4 MPLS routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Mpls')
	@IpV4Mpls.setter
	def IpV4Mpls(self, value):
		self._set_attribute('ipV4Mpls', value)

	@property
	def IpV4MplsVpn(self):
		"""If true, learns MPLS VPN routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MplsVpn')
	@IpV4MplsVpn.setter
	def IpV4MplsVpn(self, value):
		self._set_attribute('ipV4MplsVpn', value)

	@property
	def IpV4Multicast(self):
		"""If true, learns IPv4 Multicast routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Multicast')
	@IpV4Multicast.setter
	def IpV4Multicast(self, value):
		self._set_attribute('ipV4Multicast', value)

	@property
	def IpV4MulticastMplsVpn(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MulticastMplsVpn')
	@IpV4MulticastMplsVpn.setter
	def IpV4MulticastMplsVpn(self, value):
		self._set_attribute('ipV4MulticastMplsVpn', value)

	@property
	def IpV4MulticastVpn(self):
		"""If enabled, this BGP router/peer supports the IPv4 Multicast/VPN address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MulticastVpn')
	@IpV4MulticastVpn.setter
	def IpV4MulticastVpn(self, value):
		self._set_attribute('ipV4MulticastVpn', value)

	@property
	def IpV4Unicast(self):
		"""If true, learns IPv4 Unicast routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Unicast')
	@IpV4Unicast.setter
	def IpV4Unicast(self, value):
		self._set_attribute('ipV4Unicast', value)

	@property
	def IpV6Mpls(self):
		"""If true, learns IPv6 MPLS routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Mpls')
	@IpV6Mpls.setter
	def IpV6Mpls(self, value):
		self._set_attribute('ipV6Mpls', value)

	@property
	def IpV6MplsVpn(self):
		"""If true, learns IPv6 MPLS VPN routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MplsVpn')
	@IpV6MplsVpn.setter
	def IpV6MplsVpn(self, value):
		self._set_attribute('ipV6MplsVpn', value)

	@property
	def IpV6Multicast(self):
		"""If true, learns IPv6 Multicast routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Multicast')
	@IpV6Multicast.setter
	def IpV6Multicast(self, value):
		self._set_attribute('ipV6Multicast', value)

	@property
	def IpV6MulticastMplsVpn(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MulticastMplsVpn')
	@IpV6MulticastMplsVpn.setter
	def IpV6MulticastMplsVpn(self, value):
		self._set_attribute('ipV6MulticastMplsVpn', value)

	@property
	def IpV6MulticastVpn(self):
		"""If enabled, this BGP router/peer supports the IPv6 Multicast/VPN address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MulticastVpn')
	@IpV6MulticastVpn.setter
	def IpV6MulticastVpn(self, value):
		self._set_attribute('ipV6MulticastVpn', value)

	@property
	def IpV6Unicast(self):
		"""If true, learns IPv6 Unicast routes.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Unicast')
	@IpV6Unicast.setter
	def IpV6Unicast(self, value):
		self._set_attribute('ipV6Unicast', value)

	@property
	def Vpls(self):
		"""If true, learns VPLS routes.

		Returns:
			bool
		"""
		return self._get_attribute('vpls')
	@Vpls.setter
	def Vpls(self, value):
		self._set_attribute('vpls', value)
