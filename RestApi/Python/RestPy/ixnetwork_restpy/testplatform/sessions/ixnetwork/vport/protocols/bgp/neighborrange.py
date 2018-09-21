from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NeighborRange(Base):
	"""The NeighborRange class encapsulates a user managed neighborRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NeighborRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'neighborRange'

	def __init__(self, parent):
		super(NeighborRange, self).__init__(parent)

	@property
	def Bgp4VpnBgpAdVplsRange(self):
		"""An instance of the Bgp4VpnBgpAdVplsRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.bgp4vpnbgpadvplsrange.Bgp4VpnBgpAdVplsRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.bgp4vpnbgpadvplsrange import Bgp4VpnBgpAdVplsRange
		return Bgp4VpnBgpAdVplsRange(self)

	@property
	def EthernetSegments(self):
		"""An instance of the EthernetSegments class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ethernetsegments.EthernetSegments)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.ethernetsegments import EthernetSegments
		return EthernetSegments(self)

	@property
	def InterfaceLearnedInfo(self):
		"""An instance of the InterfaceLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.interfacelearnedinfo.InterfaceLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.interfacelearnedinfo import InterfaceLearnedInfo
		return InterfaceLearnedInfo(self)._select()

	@property
	def L2Site(self):
		"""An instance of the L2Site class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.l2site.L2Site)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.l2site import L2Site
		return L2Site(self)

	@property
	def L3Site(self):
		"""An instance of the L3Site class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.l3site.L3Site)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.l3site import L3Site
		return L3Site(self)

	@property
	def LearnedFilter(self):
		"""An instance of the LearnedFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.learnedfilter.LearnedFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.learnedfilter import LearnedFilter
		return LearnedFilter(self)._select()

	@property
	def LearnedInformation(self):
		"""An instance of the LearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.learnedinformation.LearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.learnedinformation import LearnedInformation
		return LearnedInformation(self)._select()

	@property
	def MplsRouteRange(self):
		"""An instance of the MplsRouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.mplsrouterange.MplsRouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.mplsrouterange import MplsRouteRange
		return MplsRouteRange(self)

	@property
	def OpaqueRouteRange(self):
		"""An instance of the OpaqueRouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquerouterange.OpaqueRouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquerouterange import OpaqueRouteRange
		return OpaqueRouteRange(self)

	@property
	def RouteImportOptions(self):
		"""An instance of the RouteImportOptions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.routeimportoptions.RouteImportOptions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.routeimportoptions import RouteImportOptions
		return RouteImportOptions(self)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.routerange import RouteRange
		return RouteRange(self)

	@property
	def UserDefinedAfiSafi(self):
		"""An instance of the UserDefinedAfiSafi class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.userdefinedafisafi.UserDefinedAfiSafi)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.userdefinedafisafi import UserDefinedAfiSafi
		return UserDefinedAfiSafi(self)

	@property
	def AsNumMode(self):
		"""(External only) Indicates that each new session uses a different AS number.

		Returns:
			str(fixed|increment)
		"""
		return self._get_attribute('asNumMode')
	@AsNumMode.setter
	def AsNumMode(self, value):
		self._set_attribute('asNumMode', value)

	@property
	def Authentication(self):
		"""Select the type of cryptographic authentication to be used for the BGP peers in this peer range.

		Returns:
			str(null|md5)
		"""
		return self._get_attribute('authentication')
	@Authentication.setter
	def Authentication(self, value):
		self._set_attribute('authentication', value)

	@property
	def BfdModeOfOperation(self):
		"""Indicates whether to use a single-hop or a multi-hop mode of operation for the BFD session being created with a BGP peer.

		Returns:
			str(multiHop|singleHop)
		"""
		return self._get_attribute('bfdModeOfOperation')
	@BfdModeOfOperation.setter
	def BfdModeOfOperation(self, value):
		self._set_attribute('bfdModeOfOperation', value)

	@property
	def BgpId(self):
		"""The BGP ID used in OPEN messages.

		Returns:
			str
		"""
		return self._get_attribute('bgpId')
	@BgpId.setter
	def BgpId(self, value):
		self._set_attribute('bgpId', value)

	@property
	def DutIpAddress(self):
		"""The IP address of the DUT router.

		Returns:
			str
		"""
		return self._get_attribute('dutIpAddress')
	@DutIpAddress.setter
	def DutIpAddress(self, value):
		self._set_attribute('dutIpAddress', value)

	@property
	def Enable4ByteAsNum(self):
		"""Enables the 4-byte Autonomous System (AS) number of the DUT/SUT.

		Returns:
			bool
		"""
		return self._get_attribute('enable4ByteAsNum')
	@Enable4ByteAsNum.setter
	def Enable4ByteAsNum(self, value):
		self._set_attribute('enable4ByteAsNum', value)

	@property
	def EnableActAsRestarted(self):
		"""Controls the operation of BGP Graceful Restart.

		Returns:
			bool
		"""
		return self._get_attribute('enableActAsRestarted')
	@EnableActAsRestarted.setter
	def EnableActAsRestarted(self, value):
		self._set_attribute('enableActAsRestarted', value)

	@property
	def EnableBfdRegistration(self):
		"""Enables the BFD registration.

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableBgpId(self):
		"""The BGP ID used in OPEN messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableBgpId')
	@EnableBgpId.setter
	def EnableBgpId(self, value):
		self._set_attribute('enableBgpId', value)

	@property
	def EnableDiscardIxiaGeneratedRoutes(self):
		"""If true, enables the discard of Ixia generated routes

		Returns:
			bool
		"""
		return self._get_attribute('enableDiscardIxiaGeneratedRoutes')
	@EnableDiscardIxiaGeneratedRoutes.setter
	def EnableDiscardIxiaGeneratedRoutes(self, value):
		self._set_attribute('enableDiscardIxiaGeneratedRoutes', value)

	@property
	def EnableGracefulRestart(self):
		"""Controls the operation of BGP Graceful Restart.

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestart')
	@EnableGracefulRestart.setter
	def EnableGracefulRestart(self, value):
		self._set_attribute('enableGracefulRestart', value)

	@property
	def EnableLinkFlap(self):
		"""If true, enables link flap

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkFlap')
	@EnableLinkFlap.setter
	def EnableLinkFlap(self, value):
		self._set_attribute('enableLinkFlap', value)

	@property
	def EnableNextHop(self):
		"""Used for IPv4 traffic. Controls the use of the NEXT_HOP attribute. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enableNextHop')
	@EnableNextHop.setter
	def EnableNextHop(self, value):
		self._set_attribute('enableNextHop', value)

	@property
	def EnableOptionalParameters(self):
		"""Controls how an OPEN is conducted in the presence of optional parameters.

		Returns:
			bool
		"""
		return self._get_attribute('enableOptionalParameters')
	@EnableOptionalParameters.setter
	def EnableOptionalParameters(self, value):
		self._set_attribute('enableOptionalParameters', value)

	@property
	def EnableSendIxiaSignatureWithRoutes(self):
		"""If true, enables sending of Ixia signature with routes

		Returns:
			bool
		"""
		return self._get_attribute('enableSendIxiaSignatureWithRoutes')
	@EnableSendIxiaSignatureWithRoutes.setter
	def EnableSendIxiaSignatureWithRoutes(self, value):
		self._set_attribute('enableSendIxiaSignatureWithRoutes', value)

	@property
	def EnableStaggeredStart(self):
		"""Controls the staggering and period of initial start messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableStaggeredStart')
	@EnableStaggeredStart.setter
	def EnableStaggeredStart(self, value):
		self._set_attribute('enableStaggeredStart', value)

	@property
	def Enabled(self):
		"""Enables or disables simulation of the router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

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
	def EvpnNextHopCount(self):
		"""It is used to replicate the traffic among the available Next Hops in Ingress Replication mode. Default value is 1. Minimum value is 1 and maximum value is 255.

		Returns:
			number
		"""
		return self._get_attribute('evpnNextHopCount')
	@EvpnNextHopCount.setter
	def EvpnNextHopCount(self, value):
		self._set_attribute('evpnNextHopCount', value)

	@property
	def HoldTimer(self):
		"""The period of time between KEEP-ALIVE messages sent to the DUT.

		Returns:
			number
		"""
		return self._get_attribute('holdTimer')
	@HoldTimer.setter
	def HoldTimer(self, value):
		self._set_attribute('holdTimer', value)

	@property
	def InterfaceStartIndex(self):
		"""The assigned protocol interface ID for this SM interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceStartIndex')
	@InterfaceStartIndex.setter
	def InterfaceStartIndex(self, value):
		self._set_attribute('interfaceStartIndex', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this BGP interface. One of:Protocol Interface, DHCP, PPP

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""The interfaces that are associated with the selected interface type.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def IpV4Mdt(self):
		"""Enables the use of this Data MDT range on the simulated interface.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Mdt')
	@IpV4Mdt.setter
	def IpV4Mdt(self, value):
		self._set_attribute('ipV4Mdt', value)

	@property
	def IpV4Mpls(self):
		"""If enabled, this BGP router/peer supports the IPv4 MPLS address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Mpls')
	@IpV4Mpls.setter
	def IpV4Mpls(self, value):
		self._set_attribute('ipV4Mpls', value)

	@property
	def IpV4MplsVpn(self):
		"""If enabled, this BGP router/peer supports the IPv4 MPLS/VPN address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MplsVpn')
	@IpV4MplsVpn.setter
	def IpV4MplsVpn(self, value):
		self._set_attribute('ipV4MplsVpn', value)

	@property
	def IpV4Multicast(self):
		"""If enabled, this BGP router/peer supports the IPv4 multicast address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Multicast')
	@IpV4Multicast.setter
	def IpV4Multicast(self, value):
		self._set_attribute('ipV4Multicast', value)

	@property
	def IpV4MulticastVpn(self):
		"""If true, this BGP router/peer supports the IPv4 Multicast/VPN address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MulticastVpn')
	@IpV4MulticastVpn.setter
	def IpV4MulticastVpn(self, value):
		self._set_attribute('ipV4MulticastVpn', value)

	@property
	def IpV4Unicast(self):
		"""If enabled, this BGP router/peer supports the IPv4 unicast address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Unicast')
	@IpV4Unicast.setter
	def IpV4Unicast(self, value):
		self._set_attribute('ipV4Unicast', value)

	@property
	def IpV6Mpls(self):
		"""If enabled, this BGP router/peer supports the IPv6 MPLS address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Mpls')
	@IpV6Mpls.setter
	def IpV6Mpls(self, value):
		self._set_attribute('ipV6Mpls', value)

	@property
	def IpV6MplsVpn(self):
		"""If enabled, this BGP router/peer supports the IPv6 MPLS/VPN address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MplsVpn')
	@IpV6MplsVpn.setter
	def IpV6MplsVpn(self, value):
		self._set_attribute('ipV6MplsVpn', value)

	@property
	def IpV6Multicast(self):
		"""If enabled, this BGP router/peer supports the IPv6 multicast address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Multicast')
	@IpV6Multicast.setter
	def IpV6Multicast(self, value):
		self._set_attribute('ipV6Multicast', value)

	@property
	def IpV6MulticastVpn(self):
		"""If true, this BGP router/peer supports the IPv6 Multicast/VPN address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MulticastVpn')
	@IpV6MulticastVpn.setter
	def IpV6MulticastVpn(self, value):
		self._set_attribute('ipV6MulticastVpn', value)

	@property
	def IpV6Unicast(self):
		"""If enabled, this BGP router/peer supports the IPv6 unicast address family.

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Unicast')
	@IpV6Unicast.setter
	def IpV6Unicast(self, value):
		self._set_attribute('ipV6Unicast', value)

	@property
	def IsAsbr(self):
		"""If true, it is ASBR

		Returns:
			bool
		"""
		return self._get_attribute('isAsbr')
	@IsAsbr.setter
	def IsAsbr(self, value):
		self._set_attribute('isAsbr', value)

	@property
	def IsInterfaceLearnedInfoAvailable(self):
		"""If true, learned information is made avavilable.

		Returns:
			bool
		"""
		return self._get_attribute('isInterfaceLearnedInfoAvailable')

	@property
	def IsLearnedInfoRefreshed(self):
		"""If true, learned information is refreshed.

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def LinkFlapDownTime(self):
		"""Signifies the link flap down time

		Returns:
			number
		"""
		return self._get_attribute('linkFlapDownTime')
	@LinkFlapDownTime.setter
	def LinkFlapDownTime(self, value):
		self._set_attribute('linkFlapDownTime', value)

	@property
	def LinkFlapUpTime(self):
		"""Signifies the link flap up time

		Returns:
			number
		"""
		return self._get_attribute('linkFlapUpTime')
	@LinkFlapUpTime.setter
	def LinkFlapUpTime(self, value):
		self._set_attribute('linkFlapUpTime', value)

	@property
	def LocalAsNumber(self):
		"""(External only) The first AS Num assigned to the simulated neighbor router. May be set for external neighbors on any port type, but only Linux-based ports may set this for internal neighbors.

		Returns:
			str
		"""
		return self._get_attribute('localAsNumber')
	@LocalAsNumber.setter
	def LocalAsNumber(self, value):
		self._set_attribute('localAsNumber', value)

	@property
	def LocalIpAddress(self):
		"""The first IP address for the simulated neighbor routers and the number of routers.

		Returns:
			str
		"""
		return self._get_attribute('localIpAddress')
	@LocalIpAddress.setter
	def LocalIpAddress(self, value):
		self._set_attribute('localIpAddress', value)

	@property
	def Md5Key(self):
		"""(Active only when MD5 is selected in the Authentication Type field.) (String) Enter a value to be used as a secret MD5 Key for authentication. The maximum length allowed is 255 characters.One MD5 key can be configured per BGP peer range. Sessions from all peers in this peer range will use this MD5 key if MD5 is enabled.

		Returns:
			str
		"""
		return self._get_attribute('md5Key')
	@Md5Key.setter
	def Md5Key(self, value):
		self._set_attribute('md5Key', value)

	@property
	def NextHop(self):
		"""If enableNextHop is true, this is the IPv4 address used as the next hop. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NumUpdatesPerIteration(self):
		"""When the protocol server operates on older ports that do not possess a local processor, this tuning parameter controls how many UPDATE messages will be sent at a time. When many routers are being simulated on such a port, changing this value may help to increase or decrease performance. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('numUpdatesPerIteration')
	@NumUpdatesPerIteration.setter
	def NumUpdatesPerIteration(self, value):
		self._set_attribute('numUpdatesPerIteration', value)

	@property
	def RangeCount(self):
		"""The number of routers.

		Returns:
			number
		"""
		return self._get_attribute('rangeCount')
	@RangeCount.setter
	def RangeCount(self, value):
		self._set_attribute('rangeCount', value)

	@property
	def RemoteAsNumber(self):
		"""The remote Autonomous System number associated with the routers.

		Returns:
			number
		"""
		return self._get_attribute('remoteAsNumber')
	@RemoteAsNumber.setter
	def RemoteAsNumber(self, value):
		self._set_attribute('remoteAsNumber', value)

	@property
	def RestartTime(self):
		"""Controls the operation of BGP Graceful Restart.

		Returns:
			number
		"""
		return self._get_attribute('restartTime')
	@RestartTime.setter
	def RestartTime(self, value):
		self._set_attribute('restartTime', value)

	@property
	def StaggeredStartPeriod(self):
		"""Controls the staggering and period of initial start messages.

		Returns:
			number
		"""
		return self._get_attribute('staggeredStartPeriod')
	@StaggeredStartPeriod.setter
	def StaggeredStartPeriod(self, value):
		self._set_attribute('staggeredStartPeriod', value)

	@property
	def StaleTime(self):
		"""Controls the operation of BGP Graceful Restart.

		Returns:
			number
		"""
		return self._get_attribute('staleTime')
	@StaleTime.setter
	def StaleTime(self, value):
		self._set_attribute('staleTime', value)

	@property
	def TcpWindowSize(self):
		"""(External neighbor only) The TCP window used for communications from the neighbor. (default = 8,192)

		Returns:
			number
		"""
		return self._get_attribute('tcpWindowSize')
	@TcpWindowSize.setter
	def TcpWindowSize(self, value):
		self._set_attribute('tcpWindowSize', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def TtlValue(self):
		"""The limited number of iterations that a unit of data can experience before the data is discarded.

		Returns:
			number
		"""
		return self._get_attribute('ttlValue')
	@TtlValue.setter
	def TtlValue(self, value):
		self._set_attribute('ttlValue', value)

	@property
	def Type(self):
		"""Indicates that the neighbor is either an internal or external router.

		Returns:
			str(internal|external)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def UpdateInterval(self):
		"""The frequency with which UPDATE messages are sent to the DUT.

		Returns:
			number
		"""
		return self._get_attribute('updateInterval')
	@UpdateInterval.setter
	def UpdateInterval(self, value):
		self._set_attribute('updateInterval', value)

	@property
	def Vpls(self):
		"""If enabled, this BGP router/peer supports BGP VPLS per the Kompella draft.

		Returns:
			bool
		"""
		return self._get_attribute('vpls')
	@Vpls.setter
	def Vpls(self, value):
		self._set_attribute('vpls', value)

	def add(self, AsNumMode=None, Authentication=None, BfdModeOfOperation=None, BgpId=None, DutIpAddress=None, Enable4ByteAsNum=None, EnableActAsRestarted=None, EnableBfdRegistration=None, EnableBgpId=None, EnableDiscardIxiaGeneratedRoutes=None, EnableGracefulRestart=None, EnableLinkFlap=None, EnableNextHop=None, EnableOptionalParameters=None, EnableSendIxiaSignatureWithRoutes=None, EnableStaggeredStart=None, Enabled=None, Evpn=None, EvpnNextHopCount=None, HoldTimer=None, InterfaceStartIndex=None, InterfaceType=None, Interfaces=None, IpV4Mdt=None, IpV4Mpls=None, IpV4MplsVpn=None, IpV4Multicast=None, IpV4MulticastVpn=None, IpV4Unicast=None, IpV6Mpls=None, IpV6MplsVpn=None, IpV6Multicast=None, IpV6MulticastVpn=None, IpV6Unicast=None, IsAsbr=None, LinkFlapDownTime=None, LinkFlapUpTime=None, LocalAsNumber=None, LocalIpAddress=None, Md5Key=None, NextHop=None, NumUpdatesPerIteration=None, RangeCount=None, RemoteAsNumber=None, RestartTime=None, StaggeredStartPeriod=None, StaleTime=None, TcpWindowSize=None, TrafficGroupId=None, TtlValue=None, Type=None, UpdateInterval=None, Vpls=None):
		"""Adds a new neighborRange node on the server and retrieves it in this instance.

		Args:
			AsNumMode (str(fixed|increment)): (External only) Indicates that each new session uses a different AS number.
			Authentication (str(null|md5)): Select the type of cryptographic authentication to be used for the BGP peers in this peer range.
			BfdModeOfOperation (str(multiHop|singleHop)): Indicates whether to use a single-hop or a multi-hop mode of operation for the BFD session being created with a BGP peer.
			BgpId (str): The BGP ID used in OPEN messages.
			DutIpAddress (str): The IP address of the DUT router.
			Enable4ByteAsNum (bool): Enables the 4-byte Autonomous System (AS) number of the DUT/SUT.
			EnableActAsRestarted (bool): Controls the operation of BGP Graceful Restart.
			EnableBfdRegistration (bool): Enables the BFD registration.
			EnableBgpId (bool): The BGP ID used in OPEN messages.
			EnableDiscardIxiaGeneratedRoutes (bool): If true, enables the discard of Ixia generated routes
			EnableGracefulRestart (bool): Controls the operation of BGP Graceful Restart.
			EnableLinkFlap (bool): If true, enables link flap
			EnableNextHop (bool): Used for IPv4 traffic. Controls the use of the NEXT_HOP attribute. (default = disabled)
			EnableOptionalParameters (bool): Controls how an OPEN is conducted in the presence of optional parameters.
			EnableSendIxiaSignatureWithRoutes (bool): If true, enables sending of Ixia signature with routes
			EnableStaggeredStart (bool): Controls the staggering and period of initial start messages.
			Enabled (bool): Enables or disables simulation of the router.
			Evpn (bool): If enabled, then this BGP peer range supports BGP MPLS Based Ethernet VPN per draft-ietf-l2vpn-evpn-03. Default value is false.
			EvpnNextHopCount (number): It is used to replicate the traffic among the available Next Hops in Ingress Replication mode. Default value is 1. Minimum value is 1 and maximum value is 255.
			HoldTimer (number): The period of time between KEEP-ALIVE messages sent to the DUT.
			InterfaceStartIndex (number): The assigned protocol interface ID for this SM interface.
			InterfaceType (str): The type of interface to be selected for this BGP interface. One of:Protocol Interface, DHCP, PPP
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IpV4Mdt (bool): Enables the use of this Data MDT range on the simulated interface.
			IpV4Mpls (bool): If enabled, this BGP router/peer supports the IPv4 MPLS address family.
			IpV4MplsVpn (bool): If enabled, this BGP router/peer supports the IPv4 MPLS/VPN address family.
			IpV4Multicast (bool): If enabled, this BGP router/peer supports the IPv4 multicast address family.
			IpV4MulticastVpn (bool): If true, this BGP router/peer supports the IPv4 Multicast/VPN address family.
			IpV4Unicast (bool): If enabled, this BGP router/peer supports the IPv4 unicast address family.
			IpV6Mpls (bool): If enabled, this BGP router/peer supports the IPv6 MPLS address family.
			IpV6MplsVpn (bool): If enabled, this BGP router/peer supports the IPv6 MPLS/VPN address family.
			IpV6Multicast (bool): If enabled, this BGP router/peer supports the IPv6 multicast address family.
			IpV6MulticastVpn (bool): If true, this BGP router/peer supports the IPv6 Multicast/VPN address family.
			IpV6Unicast (bool): If enabled, this BGP router/peer supports the IPv6 unicast address family.
			IsAsbr (bool): If true, it is ASBR
			LinkFlapDownTime (number): Signifies the link flap down time
			LinkFlapUpTime (number): Signifies the link flap up time
			LocalAsNumber (str): (External only) The first AS Num assigned to the simulated neighbor router. May be set for external neighbors on any port type, but only Linux-based ports may set this for internal neighbors.
			LocalIpAddress (str): The first IP address for the simulated neighbor routers and the number of routers.
			Md5Key (str): (Active only when MD5 is selected in the Authentication Type field.) (String) Enter a value to be used as a secret MD5 Key for authentication. The maximum length allowed is 255 characters.One MD5 key can be configured per BGP peer range. Sessions from all peers in this peer range will use this MD5 key if MD5 is enabled.
			NextHop (str): If enableNextHop is true, this is the IPv4 address used as the next hop. (default = 0.0.0.0)
			NumUpdatesPerIteration (number): When the protocol server operates on older ports that do not possess a local processor, this tuning parameter controls how many UPDATE messages will be sent at a time. When many routers are being simulated on such a port, changing this value may help to increase or decrease performance. (default = 1)
			RangeCount (number): The number of routers.
			RemoteAsNumber (number): The remote Autonomous System number associated with the routers.
			RestartTime (number): Controls the operation of BGP Graceful Restart.
			StaggeredStartPeriod (number): Controls the staggering and period of initial start messages.
			StaleTime (number): Controls the operation of BGP Graceful Restart.
			TcpWindowSize (number): (External neighbor only) The TCP window used for communications from the neighbor. (default = 8,192)
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			TtlValue (number): The limited number of iterations that a unit of data can experience before the data is discarded.
			Type (str(internal|external)): Indicates that the neighbor is either an internal or external router.
			UpdateInterval (number): The frequency with which UPDATE messages are sent to the DUT.
			Vpls (bool): If enabled, this BGP router/peer supports BGP VPLS per the Kompella draft.

		Returns:
			self: This instance with all currently retrieved neighborRange data using find and the newly added neighborRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the neighborRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AsNumMode=None, Authentication=None, BfdModeOfOperation=None, BgpId=None, DutIpAddress=None, Enable4ByteAsNum=None, EnableActAsRestarted=None, EnableBfdRegistration=None, EnableBgpId=None, EnableDiscardIxiaGeneratedRoutes=None, EnableGracefulRestart=None, EnableLinkFlap=None, EnableNextHop=None, EnableOptionalParameters=None, EnableSendIxiaSignatureWithRoutes=None, EnableStaggeredStart=None, Enabled=None, Evpn=None, EvpnNextHopCount=None, HoldTimer=None, InterfaceStartIndex=None, InterfaceType=None, Interfaces=None, IpV4Mdt=None, IpV4Mpls=None, IpV4MplsVpn=None, IpV4Multicast=None, IpV4MulticastVpn=None, IpV4Unicast=None, IpV6Mpls=None, IpV6MplsVpn=None, IpV6Multicast=None, IpV6MulticastVpn=None, IpV6Unicast=None, IsAsbr=None, IsInterfaceLearnedInfoAvailable=None, IsLearnedInfoRefreshed=None, LinkFlapDownTime=None, LinkFlapUpTime=None, LocalAsNumber=None, LocalIpAddress=None, Md5Key=None, NextHop=None, NumUpdatesPerIteration=None, RangeCount=None, RemoteAsNumber=None, RestartTime=None, StaggeredStartPeriod=None, StaleTime=None, TcpWindowSize=None, TrafficGroupId=None, TtlValue=None, Type=None, UpdateInterval=None, Vpls=None):
		"""Finds and retrieves neighborRange data from the server.

		All named parameters support regex and can be used to selectively retrieve neighborRange data from the server.
		By default the find method takes no parameters and will retrieve all neighborRange data from the server.

		Args:
			AsNumMode (str(fixed|increment)): (External only) Indicates that each new session uses a different AS number.
			Authentication (str(null|md5)): Select the type of cryptographic authentication to be used for the BGP peers in this peer range.
			BfdModeOfOperation (str(multiHop|singleHop)): Indicates whether to use a single-hop or a multi-hop mode of operation for the BFD session being created with a BGP peer.
			BgpId (str): The BGP ID used in OPEN messages.
			DutIpAddress (str): The IP address of the DUT router.
			Enable4ByteAsNum (bool): Enables the 4-byte Autonomous System (AS) number of the DUT/SUT.
			EnableActAsRestarted (bool): Controls the operation of BGP Graceful Restart.
			EnableBfdRegistration (bool): Enables the BFD registration.
			EnableBgpId (bool): The BGP ID used in OPEN messages.
			EnableDiscardIxiaGeneratedRoutes (bool): If true, enables the discard of Ixia generated routes
			EnableGracefulRestart (bool): Controls the operation of BGP Graceful Restart.
			EnableLinkFlap (bool): If true, enables link flap
			EnableNextHop (bool): Used for IPv4 traffic. Controls the use of the NEXT_HOP attribute. (default = disabled)
			EnableOptionalParameters (bool): Controls how an OPEN is conducted in the presence of optional parameters.
			EnableSendIxiaSignatureWithRoutes (bool): If true, enables sending of Ixia signature with routes
			EnableStaggeredStart (bool): Controls the staggering and period of initial start messages.
			Enabled (bool): Enables or disables simulation of the router.
			Evpn (bool): If enabled, then this BGP peer range supports BGP MPLS Based Ethernet VPN per draft-ietf-l2vpn-evpn-03. Default value is false.
			EvpnNextHopCount (number): It is used to replicate the traffic among the available Next Hops in Ingress Replication mode. Default value is 1. Minimum value is 1 and maximum value is 255.
			HoldTimer (number): The period of time between KEEP-ALIVE messages sent to the DUT.
			InterfaceStartIndex (number): The assigned protocol interface ID for this SM interface.
			InterfaceType (str): The type of interface to be selected for this BGP interface. One of:Protocol Interface, DHCP, PPP
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IpV4Mdt (bool): Enables the use of this Data MDT range on the simulated interface.
			IpV4Mpls (bool): If enabled, this BGP router/peer supports the IPv4 MPLS address family.
			IpV4MplsVpn (bool): If enabled, this BGP router/peer supports the IPv4 MPLS/VPN address family.
			IpV4Multicast (bool): If enabled, this BGP router/peer supports the IPv4 multicast address family.
			IpV4MulticastVpn (bool): If true, this BGP router/peer supports the IPv4 Multicast/VPN address family.
			IpV4Unicast (bool): If enabled, this BGP router/peer supports the IPv4 unicast address family.
			IpV6Mpls (bool): If enabled, this BGP router/peer supports the IPv6 MPLS address family.
			IpV6MplsVpn (bool): If enabled, this BGP router/peer supports the IPv6 MPLS/VPN address family.
			IpV6Multicast (bool): If enabled, this BGP router/peer supports the IPv6 multicast address family.
			IpV6MulticastVpn (bool): If true, this BGP router/peer supports the IPv6 Multicast/VPN address family.
			IpV6Unicast (bool): If enabled, this BGP router/peer supports the IPv6 unicast address family.
			IsAsbr (bool): If true, it is ASBR
			IsInterfaceLearnedInfoAvailable (bool): If true, learned information is made avavilable.
			IsLearnedInfoRefreshed (bool): If true, learned information is refreshed.
			LinkFlapDownTime (number): Signifies the link flap down time
			LinkFlapUpTime (number): Signifies the link flap up time
			LocalAsNumber (str): (External only) The first AS Num assigned to the simulated neighbor router. May be set for external neighbors on any port type, but only Linux-based ports may set this for internal neighbors.
			LocalIpAddress (str): The first IP address for the simulated neighbor routers and the number of routers.
			Md5Key (str): (Active only when MD5 is selected in the Authentication Type field.) (String) Enter a value to be used as a secret MD5 Key for authentication. The maximum length allowed is 255 characters.One MD5 key can be configured per BGP peer range. Sessions from all peers in this peer range will use this MD5 key if MD5 is enabled.
			NextHop (str): If enableNextHop is true, this is the IPv4 address used as the next hop. (default = 0.0.0.0)
			NumUpdatesPerIteration (number): When the protocol server operates on older ports that do not possess a local processor, this tuning parameter controls how many UPDATE messages will be sent at a time. When many routers are being simulated on such a port, changing this value may help to increase or decrease performance. (default = 1)
			RangeCount (number): The number of routers.
			RemoteAsNumber (number): The remote Autonomous System number associated with the routers.
			RestartTime (number): Controls the operation of BGP Graceful Restart.
			StaggeredStartPeriod (number): Controls the staggering and period of initial start messages.
			StaleTime (number): Controls the operation of BGP Graceful Restart.
			TcpWindowSize (number): (External neighbor only) The TCP window used for communications from the neighbor. (default = 8,192)
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			TtlValue (number): The limited number of iterations that a unit of data can experience before the data is discarded.
			Type (str(internal|external)): Indicates that the neighbor is either an internal or external router.
			UpdateInterval (number): The frequency with which UPDATE messages are sent to the DUT.
			Vpls (bool): If enabled, this BGP router/peer supports BGP VPLS per the Kompella draft.

		Returns:
			self: This instance with matching neighborRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of neighborRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the neighborRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		?

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def GetInterfaceLearnedInfo(self):
		"""Executes the getInterfaceLearnedInfo operation on the server.

		This function allows to Get the interface learned information.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceLearnedInfo', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		This function allows to refresh the BGP learned information from the DUT.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
