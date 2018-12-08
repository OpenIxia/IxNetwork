
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInformation(Base):
	"""The LearnedInformation class encapsulates a required learnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedInformation'

	def __init__(self, parent):
		super(LearnedInformation, self).__init__(parent)

	@property
	def AdVpls(self):
		"""An instance of the AdVpls class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.advpls.AdVpls)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.advpls import AdVpls
		return AdVpls(self)

	@property
	def EvpnEthernetAd(self):
		"""An instance of the EvpnEthernetAd class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnethernetad.EvpnEthernetAd)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnethernetad import EvpnEthernetAd
		return EvpnEthernetAd(self)

	@property
	def EvpnEthernetSegment(self):
		"""An instance of the EvpnEthernetSegment class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnethernetsegment.EvpnEthernetSegment)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnethernetsegment import EvpnEthernetSegment
		return EvpnEthernetSegment(self)

	@property
	def EvpnMac(self):
		"""An instance of the EvpnMac class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnmac.EvpnMac)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnmac import EvpnMac
		return EvpnMac(self)

	@property
	def EvpnMulticast(self):
		"""An instance of the EvpnMulticast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnmulticast.EvpnMulticast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evpnmulticast import EvpnMulticast
		return EvpnMulticast(self)

	@property
	def IpV4MulticastMplsVpn(self):
		"""An instance of the IpV4MulticastMplsVpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4multicastmplsvpn.IpV4MulticastMplsVpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4multicastmplsvpn import IpV4MulticastMplsVpn
		return IpV4MulticastMplsVpn(self)

	@property
	def IpV6MulticastMplsVpn(self):
		"""An instance of the IpV6MulticastMplsVpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6multicastmplsvpn.IpV6MulticastMplsVpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6multicastmplsvpn import IpV6MulticastMplsVpn
		return IpV6MulticastMplsVpn(self)

	@property
	def Ipv4Multicast(self):
		"""An instance of the Ipv4Multicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4multicast.Ipv4Multicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4multicast import Ipv4Multicast
		return Ipv4Multicast(self)

	@property
	def Ipv4MulticastVpn(self):
		"""An instance of the Ipv4MulticastVpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4multicastvpn.Ipv4MulticastVpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4multicastvpn import Ipv4MulticastVpn
		return Ipv4MulticastVpn(self)

	@property
	def Ipv4Unicast(self):
		"""An instance of the Ipv4Unicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4unicast.Ipv4Unicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4unicast import Ipv4Unicast
		return Ipv4Unicast(self)

	@property
	def Ipv4mpls(self):
		"""An instance of the Ipv4mpls class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4mpls.Ipv4mpls)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4mpls import Ipv4mpls
		return Ipv4mpls(self)

	@property
	def Ipv4vpn(self):
		"""An instance of the Ipv4vpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4vpn.Ipv4vpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv4vpn import Ipv4vpn
		return Ipv4vpn(self)

	@property
	def Ipv6Multicast(self):
		"""An instance of the Ipv6Multicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6multicast.Ipv6Multicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6multicast import Ipv6Multicast
		return Ipv6Multicast(self)

	@property
	def Ipv6MulticastVpn(self):
		"""An instance of the Ipv6MulticastVpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6multicastvpn.Ipv6MulticastVpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6multicastvpn import Ipv6MulticastVpn
		return Ipv6MulticastVpn(self)

	@property
	def Ipv6Unicast(self):
		"""An instance of the Ipv6Unicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6unicast.Ipv6Unicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6unicast import Ipv6Unicast
		return Ipv6Unicast(self)

	@property
	def Ipv6mpls(self):
		"""An instance of the Ipv6mpls class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6mpls.Ipv6mpls)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6mpls import Ipv6mpls
		return Ipv6mpls(self)

	@property
	def Ipv6vpn(self):
		"""An instance of the Ipv6vpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6vpn.Ipv6vpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ipv6vpn import Ipv6vpn
		return Ipv6vpn(self)

	@property
	def Vpls(self):
		"""An instance of the Vpls class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.vpls.Vpls)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.vpls import Vpls
		return Vpls(self)

	@property
	def EvpnEthernetAdRouteCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('evpnEthernetAdRouteCount')

	@property
	def EvpnEthernetSegmentRouteCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('evpnEthernetSegmentRouteCount')

	@property
	def EvpnMacRouteCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('evpnMacRouteCount')

	@property
	def EvpnMulticastRouteCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('evpnMulticastRouteCount')
