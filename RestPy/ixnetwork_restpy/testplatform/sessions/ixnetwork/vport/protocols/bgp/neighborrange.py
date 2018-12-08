
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
		"""

		Returns:
			str(fixed|increment)
		"""
		return self._get_attribute('asNumMode')
	@AsNumMode.setter
	def AsNumMode(self, value):
		self._set_attribute('asNumMode', value)

	@property
	def Authentication(self):
		"""

		Returns:
			str(null|md5)
		"""
		return self._get_attribute('authentication')
	@Authentication.setter
	def Authentication(self, value):
		self._set_attribute('authentication', value)

	@property
	def BfdModeOfOperation(self):
		"""

		Returns:
			str(multiHop|singleHop)
		"""
		return self._get_attribute('bfdModeOfOperation')
	@BfdModeOfOperation.setter
	def BfdModeOfOperation(self, value):
		self._set_attribute('bfdModeOfOperation', value)

	@property
	def BgpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bgpId')
	@BgpId.setter
	def BgpId(self, value):
		self._set_attribute('bgpId', value)

	@property
	def DutIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dutIpAddress')
	@DutIpAddress.setter
	def DutIpAddress(self, value):
		self._set_attribute('dutIpAddress', value)

	@property
	def Enable4ByteAsNum(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enable4ByteAsNum')
	@Enable4ByteAsNum.setter
	def Enable4ByteAsNum(self, value):
		self._set_attribute('enable4ByteAsNum', value)

	@property
	def EnableActAsRestarted(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableActAsRestarted')
	@EnableActAsRestarted.setter
	def EnableActAsRestarted(self, value):
		self._set_attribute('enableActAsRestarted', value)

	@property
	def EnableBfdRegistration(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableBgpId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBgpId')
	@EnableBgpId.setter
	def EnableBgpId(self, value):
		self._set_attribute('enableBgpId', value)

	@property
	def EnableDiscardIxiaGeneratedRoutes(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDiscardIxiaGeneratedRoutes')
	@EnableDiscardIxiaGeneratedRoutes.setter
	def EnableDiscardIxiaGeneratedRoutes(self, value):
		self._set_attribute('enableDiscardIxiaGeneratedRoutes', value)

	@property
	def EnableGracefulRestart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestart')
	@EnableGracefulRestart.setter
	def EnableGracefulRestart(self, value):
		self._set_attribute('enableGracefulRestart', value)

	@property
	def EnableLinkFlap(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkFlap')
	@EnableLinkFlap.setter
	def EnableLinkFlap(self, value):
		self._set_attribute('enableLinkFlap', value)

	@property
	def EnableNextHop(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableNextHop')
	@EnableNextHop.setter
	def EnableNextHop(self, value):
		self._set_attribute('enableNextHop', value)

	@property
	def EnableOptionalParameters(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOptionalParameters')
	@EnableOptionalParameters.setter
	def EnableOptionalParameters(self, value):
		self._set_attribute('enableOptionalParameters', value)

	@property
	def EnableSendIxiaSignatureWithRoutes(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSendIxiaSignatureWithRoutes')
	@EnableSendIxiaSignatureWithRoutes.setter
	def EnableSendIxiaSignatureWithRoutes(self, value):
		self._set_attribute('enableSendIxiaSignatureWithRoutes', value)

	@property
	def EnableStaggeredStart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableStaggeredStart')
	@EnableStaggeredStart.setter
	def EnableStaggeredStart(self, value):
		self._set_attribute('enableStaggeredStart', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Evpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('evpn')
	@Evpn.setter
	def Evpn(self, value):
		self._set_attribute('evpn', value)

	@property
	def EvpnNextHopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('evpnNextHopCount')
	@EvpnNextHopCount.setter
	def EvpnNextHopCount(self, value):
		self._set_attribute('evpnNextHopCount', value)

	@property
	def HoldTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('holdTimer')
	@HoldTimer.setter
	def HoldTimer(self, value):
		self._set_attribute('holdTimer', value)

	@property
	def InterfaceStartIndex(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceStartIndex')
	@InterfaceStartIndex.setter
	def InterfaceStartIndex(self, value):
		self._set_attribute('interfaceStartIndex', value)

	@property
	def InterfaceType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def IpV4Mdt(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Mdt')
	@IpV4Mdt.setter
	def IpV4Mdt(self, value):
		self._set_attribute('ipV4Mdt', value)

	@property
	def IpV4Mpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Mpls')
	@IpV4Mpls.setter
	def IpV4Mpls(self, value):
		self._set_attribute('ipV4Mpls', value)

	@property
	def IpV4MplsVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MplsVpn')
	@IpV4MplsVpn.setter
	def IpV4MplsVpn(self, value):
		self._set_attribute('ipV4MplsVpn', value)

	@property
	def IpV4Multicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Multicast')
	@IpV4Multicast.setter
	def IpV4Multicast(self, value):
		self._set_attribute('ipV4Multicast', value)

	@property
	def IpV4MulticastVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MulticastVpn')
	@IpV4MulticastVpn.setter
	def IpV4MulticastVpn(self, value):
		self._set_attribute('ipV4MulticastVpn', value)

	@property
	def IpV4Unicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Unicast')
	@IpV4Unicast.setter
	def IpV4Unicast(self, value):
		self._set_attribute('ipV4Unicast', value)

	@property
	def IpV6Mpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Mpls')
	@IpV6Mpls.setter
	def IpV6Mpls(self, value):
		self._set_attribute('ipV6Mpls', value)

	@property
	def IpV6MplsVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MplsVpn')
	@IpV6MplsVpn.setter
	def IpV6MplsVpn(self, value):
		self._set_attribute('ipV6MplsVpn', value)

	@property
	def IpV6Multicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Multicast')
	@IpV6Multicast.setter
	def IpV6Multicast(self, value):
		self._set_attribute('ipV6Multicast', value)

	@property
	def IpV6MulticastVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MulticastVpn')
	@IpV6MulticastVpn.setter
	def IpV6MulticastVpn(self, value):
		self._set_attribute('ipV6MulticastVpn', value)

	@property
	def IpV6Unicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Unicast')
	@IpV6Unicast.setter
	def IpV6Unicast(self, value):
		self._set_attribute('ipV6Unicast', value)

	@property
	def IsAsbr(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isAsbr')
	@IsAsbr.setter
	def IsAsbr(self, value):
		self._set_attribute('isAsbr', value)

	@property
	def IsInterfaceLearnedInfoAvailable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isInterfaceLearnedInfoAvailable')

	@property
	def IsLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def LinkFlapDownTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('linkFlapDownTime')
	@LinkFlapDownTime.setter
	def LinkFlapDownTime(self, value):
		self._set_attribute('linkFlapDownTime', value)

	@property
	def LinkFlapUpTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('linkFlapUpTime')
	@LinkFlapUpTime.setter
	def LinkFlapUpTime(self, value):
		self._set_attribute('linkFlapUpTime', value)

	@property
	def LocalAsNumber(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localAsNumber')
	@LocalAsNumber.setter
	def LocalAsNumber(self, value):
		self._set_attribute('localAsNumber', value)

	@property
	def LocalIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIpAddress')
	@LocalIpAddress.setter
	def LocalIpAddress(self, value):
		self._set_attribute('localIpAddress', value)

	@property
	def Md5Key(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('md5Key')
	@Md5Key.setter
	def Md5Key(self, value):
		self._set_attribute('md5Key', value)

	@property
	def NextHop(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NumUpdatesPerIteration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numUpdatesPerIteration')
	@NumUpdatesPerIteration.setter
	def NumUpdatesPerIteration(self, value):
		self._set_attribute('numUpdatesPerIteration', value)

	@property
	def RangeCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rangeCount')
	@RangeCount.setter
	def RangeCount(self, value):
		self._set_attribute('rangeCount', value)

	@property
	def RemoteAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteAsNumber')
	@RemoteAsNumber.setter
	def RemoteAsNumber(self, value):
		self._set_attribute('remoteAsNumber', value)

	@property
	def RestartTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('restartTime')
	@RestartTime.setter
	def RestartTime(self, value):
		self._set_attribute('restartTime', value)

	@property
	def StaggeredStartPeriod(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('staggeredStartPeriod')
	@StaggeredStartPeriod.setter
	def StaggeredStartPeriod(self, value):
		self._set_attribute('staggeredStartPeriod', value)

	@property
	def StaleTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('staleTime')
	@StaleTime.setter
	def StaleTime(self, value):
		self._set_attribute('staleTime', value)

	@property
	def TcpWindowSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tcpWindowSize')
	@TcpWindowSize.setter
	def TcpWindowSize(self, value):
		self._set_attribute('tcpWindowSize', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def TtlValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ttlValue')
	@TtlValue.setter
	def TtlValue(self, value):
		self._set_attribute('ttlValue', value)

	@property
	def Type(self):
		"""

		Returns:
			str(internal|external)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def UpdateInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('updateInterval')
	@UpdateInterval.setter
	def UpdateInterval(self, value):
		self._set_attribute('updateInterval', value)

	@property
	def Vpls(self):
		"""

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
			AsNumMode (str(fixed|increment)): 
			Authentication (str(null|md5)): 
			BfdModeOfOperation (str(multiHop|singleHop)): 
			BgpId (str): 
			DutIpAddress (str): 
			Enable4ByteAsNum (bool): 
			EnableActAsRestarted (bool): 
			EnableBfdRegistration (bool): 
			EnableBgpId (bool): 
			EnableDiscardIxiaGeneratedRoutes (bool): 
			EnableGracefulRestart (bool): 
			EnableLinkFlap (bool): 
			EnableNextHop (bool): 
			EnableOptionalParameters (bool): 
			EnableSendIxiaSignatureWithRoutes (bool): 
			EnableStaggeredStart (bool): 
			Enabled (bool): 
			Evpn (bool): 
			EvpnNextHopCount (number): 
			HoldTimer (number): 
			InterfaceStartIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IpV4Mdt (bool): 
			IpV4Mpls (bool): 
			IpV4MplsVpn (bool): 
			IpV4Multicast (bool): 
			IpV4MulticastVpn (bool): 
			IpV4Unicast (bool): 
			IpV6Mpls (bool): 
			IpV6MplsVpn (bool): 
			IpV6Multicast (bool): 
			IpV6MulticastVpn (bool): 
			IpV6Unicast (bool): 
			IsAsbr (bool): 
			LinkFlapDownTime (number): 
			LinkFlapUpTime (number): 
			LocalAsNumber (str): 
			LocalIpAddress (str): 
			Md5Key (str): 
			NextHop (str): 
			NumUpdatesPerIteration (number): 
			RangeCount (number): 
			RemoteAsNumber (number): 
			RestartTime (number): 
			StaggeredStartPeriod (number): 
			StaleTime (number): 
			TcpWindowSize (number): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TtlValue (number): 
			Type (str(internal|external)): 
			UpdateInterval (number): 
			Vpls (bool): 

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
			AsNumMode (str(fixed|increment)): 
			Authentication (str(null|md5)): 
			BfdModeOfOperation (str(multiHop|singleHop)): 
			BgpId (str): 
			DutIpAddress (str): 
			Enable4ByteAsNum (bool): 
			EnableActAsRestarted (bool): 
			EnableBfdRegistration (bool): 
			EnableBgpId (bool): 
			EnableDiscardIxiaGeneratedRoutes (bool): 
			EnableGracefulRestart (bool): 
			EnableLinkFlap (bool): 
			EnableNextHop (bool): 
			EnableOptionalParameters (bool): 
			EnableSendIxiaSignatureWithRoutes (bool): 
			EnableStaggeredStart (bool): 
			Enabled (bool): 
			Evpn (bool): 
			EvpnNextHopCount (number): 
			HoldTimer (number): 
			InterfaceStartIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IpV4Mdt (bool): 
			IpV4Mpls (bool): 
			IpV4MplsVpn (bool): 
			IpV4Multicast (bool): 
			IpV4MulticastVpn (bool): 
			IpV4Unicast (bool): 
			IpV6Mpls (bool): 
			IpV6MplsVpn (bool): 
			IpV6Multicast (bool): 
			IpV6MulticastVpn (bool): 
			IpV6Unicast (bool): 
			IsAsbr (bool): 
			IsInterfaceLearnedInfoAvailable (bool): 
			IsLearnedInfoRefreshed (bool): 
			LinkFlapDownTime (number): 
			LinkFlapUpTime (number): 
			LocalAsNumber (str): 
			LocalIpAddress (str): 
			Md5Key (str): 
			NextHop (str): 
			NumUpdatesPerIteration (number): 
			RangeCount (number): 
			RemoteAsNumber (number): 
			RestartTime (number): 
			StaggeredStartPeriod (number): 
			StaleTime (number): 
			TcpWindowSize (number): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TtlValue (number): 
			Type (str(internal|external)): 
			UpdateInterval (number): 
			Vpls (bool): 

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

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def GetInterfaceLearnedInfo(self):
		"""Executes the getInterfaceLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceLearnedInfo', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
