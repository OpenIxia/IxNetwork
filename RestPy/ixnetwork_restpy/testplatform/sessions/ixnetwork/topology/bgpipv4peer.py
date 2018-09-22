from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpIpv4Peer(Base):
	"""The BgpIpv4Peer class encapsulates a user managed bgpIpv4Peer node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpIpv4Peer property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bgpIpv4Peer'

	def __init__(self, parent):
		super(BgpIpv4Peer, self).__init__(parent)

	@property
	def BgpCustomAfiSafiv4(self):
		"""An instance of the BgpCustomAfiSafiv4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpcustomafisafiv4.BgpCustomAfiSafiv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpcustomafisafiv4 import BgpCustomAfiSafiv4
		return BgpCustomAfiSafiv4(self)._select()

	@property
	def BgpEpePeerList(self):
		"""An instance of the BgpEpePeerList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpepepeerlist.BgpEpePeerList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpepepeerlist import BgpEpePeerList
		return BgpEpePeerList(self)._select()

	@property
	def BgpEpePeerSetList(self):
		"""An instance of the BgpEpePeerSetList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpepepeersetlist.BgpEpePeerSetList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpepepeersetlist import BgpEpePeerSetList
		return BgpEpePeerSetList(self)._select()

	@property
	def BgpEthernetSegmentV4(self):
		"""An instance of the BgpEthernetSegmentV4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpethernetsegmentv4.BgpEthernetSegmentV4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpethernetsegmentv4 import BgpEthernetSegmentV4
		return BgpEthernetSegmentV4(self)._select()

	@property
	def BgpFlowSpecRangesList(self):
		"""An instance of the BgpFlowSpecRangesList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpflowspecrangeslist.BgpFlowSpecRangesList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpflowspecrangeslist import BgpFlowSpecRangesList
		return BgpFlowSpecRangesList(self)._select()

	@property
	def BgpFlowSpecRangesListV4(self):
		"""An instance of the BgpFlowSpecRangesListV4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpflowspecrangeslistv4.BgpFlowSpecRangesListV4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpflowspecrangeslistv4 import BgpFlowSpecRangesListV4
		return BgpFlowSpecRangesListV4(self)._select()

	@property
	def BgpFlowSpecRangesListV6(self):
		"""An instance of the BgpFlowSpecRangesListV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpflowspecrangeslistv6.BgpFlowSpecRangesListV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpflowspecrangeslistv6 import BgpFlowSpecRangesListV6
		return BgpFlowSpecRangesListV6(self)._select()

	@property
	def BgpIPv4EvpnEvi(self):
		"""An instance of the BgpIPv4EvpnEvi class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnevi.BgpIPv4EvpnEvi)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnevi import BgpIPv4EvpnEvi
		return BgpIPv4EvpnEvi(self)

	@property
	def BgpIPv4EvpnPbb(self):
		"""An instance of the BgpIPv4EvpnPbb class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnpbb.BgpIPv4EvpnPbb)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnpbb import BgpIPv4EvpnPbb
		return BgpIPv4EvpnPbb(self)

	@property
	def BgpIPv4EvpnVXLAN(self):
		"""An instance of the BgpIPv4EvpnVXLAN class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnvxlan.BgpIPv4EvpnVXLAN)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnvxlan import BgpIPv4EvpnVXLAN
		return BgpIPv4EvpnVXLAN(self)

	@property
	def BgpIPv4EvpnVXLANVpws(self):
		"""An instance of the BgpIPv4EvpnVXLANVpws class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnvxlanvpws.BgpIPv4EvpnVXLANVpws)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnvxlanvpws import BgpIPv4EvpnVXLANVpws
		return BgpIPv4EvpnVXLANVpws(self)

	@property
	def BgpIPv4EvpnVpws(self):
		"""An instance of the BgpIPv4EvpnVpws class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnvpws.BgpIPv4EvpnVpws)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4evpnvpws import BgpIPv4EvpnVpws
		return BgpIPv4EvpnVpws(self)

	@property
	def BgpIpv4AdL2Vpn(self):
		"""An instance of the BgpIpv4AdL2Vpn class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4adl2vpn.BgpIpv4AdL2Vpn)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4adl2vpn import BgpIpv4AdL2Vpn
		return BgpIpv4AdL2Vpn(self)

	@property
	def BgpIpv4L2Site(self):
		"""An instance of the BgpIpv4L2Site class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4l2site.BgpIpv4L2Site)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4l2site import BgpIpv4L2Site
		return BgpIpv4L2Site(self)

	@property
	def BgpIpv4MVrf(self):
		"""An instance of the BgpIpv4MVrf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4mvrf.BgpIpv4MVrf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpipv4mvrf import BgpIpv4MVrf
		return BgpIpv4MVrf(self)

	@property
	def BgpLsAsPathSegmentList(self):
		"""An instance of the BgpLsAsPathSegmentList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplsaspathsegmentlist.BgpLsAsPathSegmentList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplsaspathsegmentlist import BgpLsAsPathSegmentList
		return BgpLsAsPathSegmentList(self)

	@property
	def BgpLsClusterIdList(self):
		"""An instance of the BgpLsClusterIdList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplsclusteridlist.BgpLsClusterIdList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplsclusteridlist import BgpLsClusterIdList
		return BgpLsClusterIdList(self)

	@property
	def BgpLsCommunitiesList(self):
		"""An instance of the BgpLsCommunitiesList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplscommunitieslist.BgpLsCommunitiesList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplscommunitieslist import BgpLsCommunitiesList
		return BgpLsCommunitiesList(self)

	@property
	def BgpLsExtendedCommunitiesList(self):
		"""An instance of the BgpLsExtendedCommunitiesList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplsextendedcommunitieslist.BgpLsExtendedCommunitiesList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgplsextendedcommunitieslist import BgpLsExtendedCommunitiesList
		return BgpLsExtendedCommunitiesList(self)

	@property
	def BgpSRGBRangeSubObjectsList(self):
		"""An instance of the BgpSRGBRangeSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrgbrangesubobjectslist.BgpSRGBRangeSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrgbrangesubobjectslist import BgpSRGBRangeSubObjectsList
		return BgpSRGBRangeSubObjectsList(self)

	@property
	def BgpSRTEPoliciesListV4(self):
		"""An instance of the BgpSRTEPoliciesListV4 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepolicieslistv4.BgpSRTEPoliciesListV4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpsrtepolicieslistv4 import BgpSRTEPoliciesListV4
		return BgpSRTEPoliciesListV4(self)._select()

	@property
	def BgpVrf(self):
		"""An instance of the BgpVrf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpvrf.BgpVrf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpvrf import BgpVrf
		return BgpVrf(self)

	@property
	def Connector(self):
		"""An instance of the Connector class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return Connector(self)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)

	@property
	def TlvProfile(self):
		"""An instance of the TlvProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlvprofile.TlvProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlvprofile import TlvProfile
		return TlvProfile(self)

	@property
	def ActAsRestarted(self):
		"""Act as restarted

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actAsRestarted')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvertiseEndOfRib(self):
		"""Advertise End-Of-RIB

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseEndOfRib')

	@property
	def AlwaysIncludeTunnelEncExtCommunity(self):
		"""Always Include Tunnel Encapsulation Extended Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('alwaysIncludeTunnelEncExtCommunity')

	@property
	def AsSetMode(self):
		"""AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asSetMode')

	@property
	def Authentication(self):
		"""Authentication Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authentication')

	@property
	def BgpFsmState(self):
		"""Logs additional information about the BGP Peer State

		Returns:
			list(str[active|connect|error|established|idle|none|openConfirm|openSent])
		"""
		return self._get_attribute('bgpFsmState')

	@property
	def BgpId(self):
		"""BGP ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpId')

	@property
	def BgpLsAsSetMode(self):
		"""AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpLsAsSetMode')

	@property
	def BgpLsEnableAsPathSegments(self):
		"""Enable AS Path Segments

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpLsEnableAsPathSegments')

	@property
	def BgpLsEnableCluster(self):
		"""Enable Cluster

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpLsEnableCluster')

	@property
	def BgpLsEnableExtendedCommunity(self):
		"""Enable Extended Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpLsEnableExtendedCommunity')

	@property
	def BgpLsNoOfASPathSegments(self):
		"""Number Of AS Path Segments Per Route Range

		Returns:
			number
		"""
		return self._get_attribute('bgpLsNoOfASPathSegments')
	@BgpLsNoOfASPathSegments.setter
	def BgpLsNoOfASPathSegments(self, value):
		self._set_attribute('bgpLsNoOfASPathSegments', value)

	@property
	def BgpLsNoOfClusters(self):
		"""Number of Clusters

		Returns:
			number
		"""
		return self._get_attribute('bgpLsNoOfClusters')
	@BgpLsNoOfClusters.setter
	def BgpLsNoOfClusters(self, value):
		self._set_attribute('bgpLsNoOfClusters', value)

	@property
	def BgpLsNoOfCommunities(self):
		"""Number of Communities

		Returns:
			number
		"""
		return self._get_attribute('bgpLsNoOfCommunities')
	@BgpLsNoOfCommunities.setter
	def BgpLsNoOfCommunities(self, value):
		self._set_attribute('bgpLsNoOfCommunities', value)

	@property
	def BgpLsOverridePeerAsSetMode(self):
		"""Override Peer AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpLsOverridePeerAsSetMode')

	@property
	def CapabilityIpV4Mdt(self):
		"""IPv4 MDT

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV4Mdt')

	@property
	def CapabilityIpV4Mpls(self):
		"""IPv4 MPLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV4Mpls')

	@property
	def CapabilityIpV4MplsVpn(self):
		"""IPv4 MPLS VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV4MplsVpn')

	@property
	def CapabilityIpV4Multicast(self):
		"""IPv4 Multicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV4Multicast')

	@property
	def CapabilityIpV4MulticastVpn(self):
		"""IPv4 Multicast VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV4MulticastVpn')

	@property
	def CapabilityIpV4Unicast(self):
		"""IPv4 Unicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV4Unicast')

	@property
	def CapabilityIpV6Mpls(self):
		"""IPv6 MPLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV6Mpls')

	@property
	def CapabilityIpV6MplsVpn(self):
		"""IPv6 MPLS VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV6MplsVpn')

	@property
	def CapabilityIpV6Multicast(self):
		"""IPv6 Multicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV6Multicast')

	@property
	def CapabilityIpV6MulticastVpn(self):
		"""IPv6 Multicast VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV6MulticastVpn')

	@property
	def CapabilityIpV6Unicast(self):
		"""IPv6 Unicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpV6Unicast')

	@property
	def CapabilityIpv4MplsAddPath(self):
		"""IPv4 MPLS Add Path Capability

		Returns:
			bool
		"""
		return self._get_attribute('capabilityIpv4MplsAddPath')
	@CapabilityIpv4MplsAddPath.setter
	def CapabilityIpv4MplsAddPath(self, value):
		self._set_attribute('capabilityIpv4MplsAddPath', value)

	@property
	def CapabilityIpv4UnicastAddPath(self):
		"""Check box for IPv4 Unicast Add Path

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpv4UnicastAddPath')

	@property
	def CapabilityIpv6MplsAddPath(self):
		"""IPv6 MPLS Add Path Capability

		Returns:
			bool
		"""
		return self._get_attribute('capabilityIpv6MplsAddPath')
	@CapabilityIpv6MplsAddPath.setter
	def CapabilityIpv6MplsAddPath(self, value):
		self._set_attribute('capabilityIpv6MplsAddPath', value)

	@property
	def CapabilityIpv6UnicastAddPath(self):
		"""Check box for IPv6 Unicast Add Path

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityIpv6UnicastAddPath')

	@property
	def CapabilityLinkStateNonVpn(self):
		"""Link State Non-VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityLinkStateNonVpn')

	@property
	def CapabilityRouteConstraint(self):
		"""Route Constraint

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityRouteConstraint')

	@property
	def CapabilityRouteRefresh(self):
		"""Route Refresh

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityRouteRefresh')

	@property
	def CapabilitySRTEPoliciesV4(self):
		"""Enable IPv4 SR TE Policy Capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitySRTEPoliciesV4')

	@property
	def CapabilitySRTEPoliciesV6(self):
		"""Enable IPv6 SR TE Policy Capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitySRTEPoliciesV6')

	@property
	def CapabilityVpls(self):
		"""VPLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityVpls')

	@property
	def Capabilityipv4UnicastFlowSpec(self):
		"""IPv4 Unicast Flow Spec

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityipv4UnicastFlowSpec')

	@property
	def Capabilityipv6UnicastFlowSpec(self):
		"""IPv6 Unicast Flow Spec

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilityipv6UnicastFlowSpec')

	@property
	def ConfigureKeepaliveTimer(self):
		"""Configure Keepalive Timer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureKeepaliveTimer')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def CustomSidType(self):
		"""moved to port data in bgp/srv6 Custom SID Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('customSidType')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DiscardIxiaGeneratedRoutes(self):
		"""Discard Ixia Generated Routes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardIxiaGeneratedRoutes')

	@property
	def DowntimeInSec(self):
		"""Downtime in Seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('downtimeInSec')

	@property
	def DutIp(self):
		"""DUT IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dutIp')

	@property
	def Enable4ByteAs(self):
		"""Enable 4-Byte AS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enable4ByteAs')

	@property
	def EnableBfdRegistration(self):
		"""Enable BFD Registration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBfdRegistration')

	@property
	def EnableBgpId(self):
		"""Enable BGP ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBgpId')

	@property
	def EnableBgpIdSameasRouterId(self):
		"""BGP ID Same as Router ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBgpIdSameasRouterId')

	@property
	def EnableBgpLsCommunity(self):
		"""Enable Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBgpLsCommunity')

	@property
	def EnableEPETraffic(self):
		"""Enable EPE Traffic

		Returns:
			bool
		"""
		return self._get_attribute('enableEPETraffic')
	@EnableEPETraffic.setter
	def EnableEPETraffic(self, value):
		self._set_attribute('enableEPETraffic', value)

	@property
	def EnableGracefulRestart(self):
		"""Enable Graceful Restart

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableGracefulRestart')

	@property
	def EnableLlgr(self):
		"""Enable LLGR

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLlgr')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def EthernetSegmentsCountV4(self):
		"""Number of Ethernet Segments

		Returns:
			number
		"""
		return self._get_attribute('ethernetSegmentsCountV4')
	@EthernetSegmentsCountV4.setter
	def EthernetSegmentsCountV4(self, value):
		self._set_attribute('ethernetSegmentsCountV4', value)

	@property
	def Evpn(self):
		"""Check box for EVPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('evpn')

	@property
	def FilterEvpn(self):
		"""Check box for EVPN filter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterEvpn')

	@property
	def FilterIpV4Mpls(self):
		"""Filter IPv4 MPLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV4Mpls')

	@property
	def FilterIpV4MplsVpn(self):
		"""Filter IPv4 MPLS VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV4MplsVpn')

	@property
	def FilterIpV4Multicast(self):
		"""Filter IPv4 Multicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV4Multicast')

	@property
	def FilterIpV4MulticastVpn(self):
		"""Filter IPv4 Multicast VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV4MulticastVpn')

	@property
	def FilterIpV4Unicast(self):
		"""Filter IPv4 Unicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV4Unicast')

	@property
	def FilterIpV6Mpls(self):
		"""Filter IPv6 MPLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV6Mpls')

	@property
	def FilterIpV6MplsVpn(self):
		"""Filter IPv6 MPLS VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV6MplsVpn')

	@property
	def FilterIpV6Multicast(self):
		"""Filter IPv6 Multicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV6Multicast')

	@property
	def FilterIpV6MulticastVpn(self):
		"""Filter IPv6 Multicast VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV6MulticastVpn')

	@property
	def FilterIpV6Unicast(self):
		"""Filter IPv6 Unicast

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpV6Unicast')

	@property
	def FilterIpv4MulticastBgpMplsVpn(self):
		"""Check box for IPv4 Multicast BGP/MPLS VPN filter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpv4MulticastBgpMplsVpn')

	@property
	def FilterIpv4UnicastFlowSpec(self):
		"""Filter IPv4 Unicast Flow Spec

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpv4UnicastFlowSpec')

	@property
	def FilterIpv6MulticastBgpMplsVpn(self):
		"""Check box for IPv6 Multicast BGP/MPLS VPN filter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpv6MulticastBgpMplsVpn')

	@property
	def FilterIpv6UnicastFlowSpec(self):
		"""Filter IPv6 Unicast Flow Spec

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterIpv6UnicastFlowSpec')

	@property
	def FilterLinkState(self):
		"""Filter Link State

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterLinkState')

	@property
	def FilterSRTEPoliciesV4(self):
		"""Enable IPv4 SR TE Policy Filter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterSRTEPoliciesV4')

	@property
	def FilterSRTEPoliciesV6(self):
		"""Enable IPv6 SR TE Policy Filter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterSRTEPoliciesV6')

	@property
	def FilterVpls(self):
		"""Filter VPLS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterVpls')

	@property
	def Flap(self):
		"""Flap

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flap')

	@property
	def HoldTimer(self):
		"""Hold Timer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('holdTimer')

	@property
	def IpVrfToIpVrfType(self):
		"""IP-VRF-to-IP-VRF Model Type

		Returns:
			str(interfacefullWithCorefacingIRB|interfacefullWithUnnumberedCorefacingIRB|interfaceLess)
		"""
		return self._get_attribute('ipVrfToIpVrfType')
	@IpVrfToIpVrfType.setter
	def IpVrfToIpVrfType(self, value):
		self._set_attribute('ipVrfToIpVrfType', value)

	@property
	def Ipv4MplsAddPathMode(self):
		"""IPv4 MPLS Add Path Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4MplsAddPathMode')

	@property
	def Ipv4MplsCapability(self):
		"""IPv4 MPLS Capability

		Returns:
			bool
		"""
		return self._get_attribute('ipv4MplsCapability')
	@Ipv4MplsCapability.setter
	def Ipv4MplsCapability(self, value):
		self._set_attribute('ipv4MplsCapability', value)

	@property
	def Ipv4MulticastBgpMplsVpn(self):
		"""Check box for IPv4 Multicast BGP/MPLS VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4MulticastBgpMplsVpn')

	@property
	def Ipv4MultipleMplsLabelsCapability(self):
		"""IPv4 Multiple MPLS Labels Capability

		Returns:
			bool
		"""
		return self._get_attribute('ipv4MultipleMplsLabelsCapability')
	@Ipv4MultipleMplsLabelsCapability.setter
	def Ipv4MultipleMplsLabelsCapability(self, value):
		self._set_attribute('ipv4MultipleMplsLabelsCapability', value)

	@property
	def Ipv4UnicastAddPathMode(self):
		"""IPv4 Unicast Add Path Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4UnicastAddPathMode')

	@property
	def Ipv6MplsAddPathMode(self):
		"""IPv6 MPLS Add Path Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6MplsAddPathMode')

	@property
	def Ipv6MplsCapability(self):
		"""IPv6 MPLS Capability

		Returns:
			bool
		"""
		return self._get_attribute('ipv6MplsCapability')
	@Ipv6MplsCapability.setter
	def Ipv6MplsCapability(self, value):
		self._set_attribute('ipv6MplsCapability', value)

	@property
	def Ipv6MulticastBgpMplsVpn(self):
		"""Check box for IPv6 Multicast BGP/MPLS VPN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6MulticastBgpMplsVpn')

	@property
	def Ipv6MultipleMplsLabelsCapability(self):
		"""IPv6 Multiple MPLS Labels Capability

		Returns:
			bool
		"""
		return self._get_attribute('ipv6MultipleMplsLabelsCapability')
	@Ipv6MultipleMplsLabelsCapability.setter
	def Ipv6MultipleMplsLabelsCapability(self, value):
		self._set_attribute('ipv6MultipleMplsLabelsCapability', value)

	@property
	def Ipv6UnicastAddPathMode(self):
		"""IPv6 Unicast Add Path Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6UnicastAddPathMode')

	@property
	def IrbInterfaceLabel(self):
		"""Label to be used for Route Type 2 carrying IRB MAC and/or IRB IP in Route Type 2

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('irbInterfaceLabel')

	@property
	def IrbIpv4Address(self):
		"""IRB IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('irbIpv4Address')

	@property
	def KeepaliveTimer(self):
		"""Keepalive Timer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keepaliveTimer')

	@property
	def LocalAs2Bytes(self):
		"""Local AS# (2-Bytes)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localAs2Bytes')

	@property
	def LocalAs4Bytes(self):
		"""Local AS# (4-Bytes)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localAs4Bytes')

	@property
	def LocalIpv4Ver2(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIpv4Ver2')

	@property
	def LocalRouterID(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterID')

	@property
	def Md5Key(self):
		"""MD5 Key

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('md5Key')

	@property
	def ModeOfBfdOperations(self):
		"""Mode of BFD Operations

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('modeOfBfdOperations')

	@property
	def MplsLabelsCountForIpv4MplsRoute(self):
		"""MPLS Labels Count For IPv4 MPLS Route

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelsCountForIpv4MplsRoute')
	@MplsLabelsCountForIpv4MplsRoute.setter
	def MplsLabelsCountForIpv4MplsRoute(self, value):
		self._set_attribute('mplsLabelsCountForIpv4MplsRoute', value)

	@property
	def MplsLabelsCountForIpv6MplsRoute(self):
		"""MPLS Labels Count For IPv6 MPLS Route

		Returns:
			number
		"""
		return self._get_attribute('mplsLabelsCountForIpv6MplsRoute')
	@MplsLabelsCountForIpv6MplsRoute.setter
	def MplsLabelsCountForIpv6MplsRoute(self, value):
		self._set_attribute('mplsLabelsCountForIpv6MplsRoute', value)

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NoOfEPEPeers(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfEPEPeers')
	@NoOfEPEPeers.setter
	def NoOfEPEPeers(self, value):
		self._set_attribute('noOfEPEPeers', value)

	@property
	def NoOfExtendedCommunities(self):
		"""Number of Extended Communities

		Returns:
			number
		"""
		return self._get_attribute('noOfExtendedCommunities')
	@NoOfExtendedCommunities.setter
	def NoOfExtendedCommunities(self, value):
		self._set_attribute('noOfExtendedCommunities', value)

	@property
	def NoOfPeerSet(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfPeerSet')
	@NoOfPeerSet.setter
	def NoOfPeerSet(self, value):
		self._set_attribute('noOfPeerSet', value)

	@property
	def NoOfUserDefinedAfiSafi(self):
		"""Count of User Defined AFI SAFI

		Returns:
			number
		"""
		return self._get_attribute('noOfUserDefinedAfiSafi')
	@NoOfUserDefinedAfiSafi.setter
	def NoOfUserDefinedAfiSafi(self, value):
		self._set_attribute('noOfUserDefinedAfiSafi', value)

	@property
	def NumBgpLsId(self):
		"""BGP LS Instance ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numBgpLsId')

	@property
	def NumBgpLsInstanceIdentifier(self):
		"""IGP Multi instance unique identifier. 0 is default single-instance IGP. (e.g. for OSPFv3 it is possible to separately run 4 instances of OSPFv3 with peer, one advertising v4 only, another v6 only and other 2 mcast v4 and v6 respectively) .

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numBgpLsInstanceIdentifier')

	@property
	def NumBgpUpdatesGeneratedPerIteration(self):
		"""Num BGP Updates Generated Per Iteration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numBgpUpdatesGeneratedPerIteration')

	@property
	def NumberFlowSpecRangeV4(self):
		"""Number of IPv4 Flow Spec Ranges

		Returns:
			number
		"""
		return self._get_attribute('numberFlowSpecRangeV4')
	@NumberFlowSpecRangeV4.setter
	def NumberFlowSpecRangeV4(self, value):
		self._set_attribute('numberFlowSpecRangeV4', value)

	@property
	def NumberFlowSpecRangeV6(self):
		"""Number of IPv6 Flow Spec Ranges

		Returns:
			number
		"""
		return self._get_attribute('numberFlowSpecRangeV6')
	@NumberFlowSpecRangeV6.setter
	def NumberFlowSpecRangeV6(self, value):
		self._set_attribute('numberFlowSpecRangeV6', value)

	@property
	def NumberSRTEPolicies(self):
		"""Count of SR TE Policies

		Returns:
			number
		"""
		return self._get_attribute('numberSRTEPolicies')
	@NumberSRTEPolicies.setter
	def NumberSRTEPolicies(self, value):
		self._set_attribute('numberSRTEPolicies', value)

	@property
	def OperationalModel(self):
		"""Operational Model

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('operationalModel')

	@property
	def RestartTime(self):
		"""Restart Time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('restartTime')

	@property
	def RoutersMacOrIrbMacAddress(self):
		"""Router's MAC/IRB MAC Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routersMacOrIrbMacAddress')

	@property
	def SRGBRangeCount(self):
		"""SRGB Range Count

		Returns:
			number
		"""
		return self._get_attribute('sRGBRangeCount')
	@SRGBRangeCount.setter
	def SRGBRangeCount(self, value):
		self._set_attribute('sRGBRangeCount', value)

	@property
	def SendIxiaSignatureWithRoutes(self):
		"""Send Ixia Signature With Routes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendIxiaSignatureWithRoutes')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[aSRoutingLoopErrorRx|attributeFlagErrorRx|attributesLengthErrorRx|authenticationFailureErrorRx|badBGPIdentifierErrorRx|badMessageLengthErrorRx|badMessageTypeErrorRx|badPeerASErrorRx|bGPHeaderErrorRx|bGPHeaderErrorTx|bGPHoldTimerExpiredErrorRx|bGPOpenPacketErrorRx|bGPStateMachineErrorRx|bGPUpdatePacketErrorRx|ceaseErrorRx|ceaseNotificationErrorTx|connectionNotsynchronizedErrorRx|holdtimeExpiredErrorTx|invalidASPathErrorRx|invalidNetworkFieldErrorRx|invalidNextHopAttributeErrorRx|invalidOriginAttributeErrorRx|malformedAttributeListErrorRx|missingWellKnownAttributeErrorRx|none|openPacketErrTx|optionalAttributeErrorRx|stateMachineErrorTx|unacceptableHoldTimeErrorRx|unrecognizedWellKnownAttributeErrorRx|unspecifiedErrorRx|unspecifiedErrorTx|unspecifiedSubcodeErrorRx|unsupportedOptionalParameterErrorRx|unsupportedversionNumberErrorRx|updatePacketErrorTx])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StaleTime(self):
		"""Stale Time/ LLGR Stale Time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('staleTime')

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def TcpWindowSizeInBytes(self):
		"""TCP Window Size (in bytes)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tcpWindowSizeInBytes')

	@property
	def Ttl(self):
		"""TTL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ttl')

	@property
	def Type(self):
		"""Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

	@property
	def UpdateInterval(self):
		"""Update Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('updateInterval')

	@property
	def UptimeInSec(self):
		"""Uptime in Seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('uptimeInSec')

	@property
	def VplsEnableNextHop(self):
		"""VPLS Enable Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vplsEnableNextHop')

	@property
	def VplsNextHop(self):
		"""VPLS Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vplsNextHop')

	def add(self, BgpLsNoOfASPathSegments=None, BgpLsNoOfClusters=None, BgpLsNoOfCommunities=None, CapabilityIpv4MplsAddPath=None, CapabilityIpv6MplsAddPath=None, ConnectedVia=None, EnableEPETraffic=None, EthernetSegmentsCountV4=None, IpVrfToIpVrfType=None, Ipv4MplsCapability=None, Ipv4MultipleMplsLabelsCapability=None, Ipv6MplsCapability=None, Ipv6MultipleMplsLabelsCapability=None, MplsLabelsCountForIpv4MplsRoute=None, MplsLabelsCountForIpv6MplsRoute=None, Multiplier=None, Name=None, NoOfEPEPeers=None, NoOfExtendedCommunities=None, NoOfPeerSet=None, NoOfUserDefinedAfiSafi=None, NumberFlowSpecRangeV4=None, NumberFlowSpecRangeV6=None, NumberSRTEPolicies=None, SRGBRangeCount=None, StackedLayers=None):
		"""Adds a new bgpIpv4Peer node on the server and retrieves it in this instance.

		Args:
			BgpLsNoOfASPathSegments (number): Number Of AS Path Segments Per Route Range
			BgpLsNoOfClusters (number): Number of Clusters
			BgpLsNoOfCommunities (number): Number of Communities
			CapabilityIpv4MplsAddPath (bool): IPv4 MPLS Add Path Capability
			CapabilityIpv6MplsAddPath (bool): IPv6 MPLS Add Path Capability
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableEPETraffic (bool): Enable EPE Traffic
			EthernetSegmentsCountV4 (number): Number of Ethernet Segments
			IpVrfToIpVrfType (str(interfacefullWithCorefacingIRB|interfacefullWithUnnumberedCorefacingIRB|interfaceLess)): IP-VRF-to-IP-VRF Model Type
			Ipv4MplsCapability (bool): IPv4 MPLS Capability
			Ipv4MultipleMplsLabelsCapability (bool): IPv4 Multiple MPLS Labels Capability
			Ipv6MplsCapability (bool): IPv6 MPLS Capability
			Ipv6MultipleMplsLabelsCapability (bool): IPv6 Multiple MPLS Labels Capability
			MplsLabelsCountForIpv4MplsRoute (number): MPLS Labels Count For IPv4 MPLS Route
			MplsLabelsCountForIpv6MplsRoute (number): MPLS Labels Count For IPv6 MPLS Route
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfEPEPeers (number): 
			NoOfExtendedCommunities (number): Number of Extended Communities
			NoOfPeerSet (number): 
			NoOfUserDefinedAfiSafi (number): Count of User Defined AFI SAFI
			NumberFlowSpecRangeV4 (number): Number of IPv4 Flow Spec Ranges
			NumberFlowSpecRangeV6 (number): Number of IPv6 Flow Spec Ranges
			NumberSRTEPolicies (number): Count of SR TE Policies
			SRGBRangeCount (number): SRGB Range Count
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved bgpIpv4Peer data using find and the newly added bgpIpv4Peer data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bgpIpv4Peer data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BgpFsmState=None, BgpLsNoOfASPathSegments=None, BgpLsNoOfClusters=None, BgpLsNoOfCommunities=None, CapabilityIpv4MplsAddPath=None, CapabilityIpv6MplsAddPath=None, ConnectedVia=None, Count=None, DescriptiveName=None, EnableEPETraffic=None, Errors=None, EthernetSegmentsCountV4=None, IpVrfToIpVrfType=None, Ipv4MplsCapability=None, Ipv4MultipleMplsLabelsCapability=None, Ipv6MplsCapability=None, Ipv6MultipleMplsLabelsCapability=None, LocalIpv4Ver2=None, LocalRouterID=None, MplsLabelsCountForIpv4MplsRoute=None, MplsLabelsCountForIpv6MplsRoute=None, Multiplier=None, Name=None, NoOfEPEPeers=None, NoOfExtendedCommunities=None, NoOfPeerSet=None, NoOfUserDefinedAfiSafi=None, NumberFlowSpecRangeV4=None, NumberFlowSpecRangeV6=None, NumberSRTEPolicies=None, SRGBRangeCount=None, SessionInfo=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves bgpIpv4Peer data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpIpv4Peer data from the server.
		By default the find method takes no parameters and will retrieve all bgpIpv4Peer data from the server.

		Args:
			BgpFsmState (list(str[active|connect|error|established|idle|none|openConfirm|openSent])): Logs additional information about the BGP Peer State
			BgpLsNoOfASPathSegments (number): Number Of AS Path Segments Per Route Range
			BgpLsNoOfClusters (number): Number of Clusters
			BgpLsNoOfCommunities (number): Number of Communities
			CapabilityIpv4MplsAddPath (bool): IPv4 MPLS Add Path Capability
			CapabilityIpv6MplsAddPath (bool): IPv6 MPLS Add Path Capability
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableEPETraffic (bool): Enable EPE Traffic
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			EthernetSegmentsCountV4 (number): Number of Ethernet Segments
			IpVrfToIpVrfType (str(interfacefullWithCorefacingIRB|interfacefullWithUnnumberedCorefacingIRB|interfaceLess)): IP-VRF-to-IP-VRF Model Type
			Ipv4MplsCapability (bool): IPv4 MPLS Capability
			Ipv4MultipleMplsLabelsCapability (bool): IPv4 Multiple MPLS Labels Capability
			Ipv6MplsCapability (bool): IPv6 MPLS Capability
			Ipv6MultipleMplsLabelsCapability (bool): IPv6 Multiple MPLS Labels Capability
			LocalIpv4Ver2 (list(str)): Local IP
			LocalRouterID (list(str)): Router ID
			MplsLabelsCountForIpv4MplsRoute (number): MPLS Labels Count For IPv4 MPLS Route
			MplsLabelsCountForIpv6MplsRoute (number): MPLS Labels Count For IPv6 MPLS Route
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfEPEPeers (number): 
			NoOfExtendedCommunities (number): Number of Extended Communities
			NoOfPeerSet (number): 
			NoOfUserDefinedAfiSafi (number): Count of User Defined AFI SAFI
			NumberFlowSpecRangeV4 (number): Number of IPv4 Flow Spec Ranges
			NumberFlowSpecRangeV6 (number): Number of IPv6 Flow Spec Ranges
			NumberSRTEPolicies (number): Count of SR TE Policies
			SRGBRangeCount (number): SRGB Range Count
			SessionInfo (list(str[aSRoutingLoopErrorRx|attributeFlagErrorRx|attributesLengthErrorRx|authenticationFailureErrorRx|badBGPIdentifierErrorRx|badMessageLengthErrorRx|badMessageTypeErrorRx|badPeerASErrorRx|bGPHeaderErrorRx|bGPHeaderErrorTx|bGPHoldTimerExpiredErrorRx|bGPOpenPacketErrorRx|bGPStateMachineErrorRx|bGPUpdatePacketErrorRx|ceaseErrorRx|ceaseNotificationErrorTx|connectionNotsynchronizedErrorRx|holdtimeExpiredErrorTx|invalidASPathErrorRx|invalidNetworkFieldErrorRx|invalidNextHopAttributeErrorRx|invalidOriginAttributeErrorRx|malformedAttributeListErrorRx|missingWellKnownAttributeErrorRx|none|openPacketErrTx|optionalAttributeErrorRx|stateMachineErrorTx|unacceptableHoldTimeErrorRx|unrecognizedWellKnownAttributeErrorRx|unspecifiedErrorRx|unspecifiedErrorTx|unspecifiedSubcodeErrorRx|unsupportedOptionalParameterErrorRx|unsupportedversionNumberErrorRx|updatePacketErrorTx])): Logs additional information about the session state
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching bgpIpv4Peer data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgpIpv4Peer data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgpIpv4Peer data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def BgpIPv4FlowSpecLearnedInfo(self):
		"""Executes the bgpIPv4FlowSpecLearnedInfo operation on the server.

		Get IPv4 FlowSpec Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BgpIPv4FlowSpecLearnedInfo', payload=locals(), response_object=None)

	def BgpIPv4FlowSpecLearnedInfo(self, SessionIndices):
		"""Executes the bgpIPv4FlowSpecLearnedInfo operation on the server.

		Get IPv4 FlowSpec Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BgpIPv4FlowSpecLearnedInfo', payload=locals(), response_object=None)

	def BgpIPv4FlowSpecLearnedInfo(self, SessionIndices):
		"""Executes the bgpIPv4FlowSpecLearnedInfo operation on the server.

		Get IPv4 FlowSpec Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BgpIPv4FlowSpecLearnedInfo', payload=locals(), response_object=None)

	def BgpIPv6FlowSpecLearnedInfo(self):
		"""Executes the bgpIPv6FlowSpecLearnedInfo operation on the server.

		Get IPv6 FlowSpec Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BgpIPv6FlowSpecLearnedInfo', payload=locals(), response_object=None)

	def BgpIPv6FlowSpecLearnedInfo(self, SessionIndices):
		"""Executes the bgpIPv6FlowSpecLearnedInfo operation on the server.

		Get IPv6 FlowSpec Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BgpIPv6FlowSpecLearnedInfo', payload=locals(), response_object=None)

	def BgpIPv6FlowSpecLearnedInfo(self, SessionIndices):
		"""Executes the bgpIPv6FlowSpecLearnedInfo operation on the server.

		Get IPv6 FlowSpec Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BgpIPv6FlowSpecLearnedInfo', payload=locals(), response_object=None)

	def BreakTCPSession(self, Notification_code, Notification_sub_code):
		"""Executes the breakTCPSession operation on the server.

		Break TCP Session

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Notification_code (number): This parameter requires a notification_code of type kInteger
			Notification_sub_code (number): This parameter requires a notification_sub_code of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BreakTCPSession', payload=locals(), response_object=None)

	def BreakTCPSession(self, Notification_code, Notification_sub_code, SessionIndices):
		"""Executes the breakTCPSession operation on the server.

		Break TCP Session

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Notification_code (number): This parameter requires a notification_code of type kInteger
			Notification_sub_code (number): This parameter requires a notification_sub_code of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BreakTCPSession', payload=locals(), response_object=None)

	def BreakTCPSession(self, SessionIndices, Notification_code, Notification_sub_code):
		"""Executes the breakTCPSession operation on the server.

		Break TCP Session

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a notification_code of type kInteger
			Notification_code (number): This parameter requires a notification_sub_code of type kInteger
			Notification_sub_code (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('BreakTCPSession', payload=locals(), response_object=None)

	def Breaktcpsession(self, Arg2, Arg3, Arg4):
		"""Executes the breaktcpsession operation on the server.

		Break BGP Peer Range TCP Session.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (number): Notification Code
			Arg4 (number): Notification Sub Code

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Breaktcpsession', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfoInClient(self, Arg2):
		"""Executes the clearAllLearnedInfoInClient operation on the server.

		Clears ALL routes from GUI grid for the selected BGP Peers.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearAllLearnedInfoInClient', payload=locals(), response_object=None)

	def GetADVPLSLearnedInfo(self):
		"""Executes the getADVPLSLearnedInfo operation on the server.

		Get ADVPLS Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetADVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetADVPLSLearnedInfo(self, SessionIndices):
		"""Executes the getADVPLSLearnedInfo operation on the server.

		Get ADVPLS Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetADVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetADVPLSLearnedInfo(self, SessionIndices):
		"""Executes the getADVPLSLearnedInfo operation on the server.

		Get ADVPLS Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetADVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetADVPLSLearnedInfo(self, Arg2):
		"""Executes the getADVPLSLearnedInfo operation on the server.

		Fetches AD-VPLS routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetADVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self):
		"""Executes the getAllLearnedInfo operation on the server.

		Get All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, SessionIndices):
		"""Executes the getAllLearnedInfo operation on the server.

		Get All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, SessionIndices):
		"""Executes the getAllLearnedInfo operation on the server.

		Get All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, Arg2):
		"""Executes the getAllLearnedInfo operation on the server.

		Gets ALL routes learnt and stored by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetAllLearnedInfo', payload=locals(), response_object=None)

	def GetbgpIpv4FlowSpecLearnedInfoLearnedInfo(self, Arg2):
		"""Executes the getbgpIpv4FlowSpecLearnedInfoLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): Please provide a proper description here.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetbgpIpv4FlowSpecLearnedInfoLearnedInfo', payload=locals(), response_object=None)

	def GetbgpIpv6FlowSpecLearnedInfoLearnedInfo(self, Arg2):
		"""Executes the getbgpIpv6FlowSpecLearnedInfoLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): Please provide a proper description here.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetbgpIpv6FlowSpecLearnedInfoLearnedInfo', payload=locals(), response_object=None)

	def GetbgpSrTeLearnedInfoLearnedInfo(self, Arg2):
		"""Executes the getbgpSrTeLearnedInfoLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): Please provide a proper description here.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetbgpSrTeLearnedInfoLearnedInfo', payload=locals(), response_object=None)

	def GetEVPNLearnedInfo(self):
		"""Executes the getEVPNLearnedInfo operation on the server.

		Get EVPN Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetEVPNLearnedInfo', payload=locals(), response_object=None)

	def GetEVPNLearnedInfo(self, SessionIndices):
		"""Executes the getEVPNLearnedInfo operation on the server.

		Get EVPN Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetEVPNLearnedInfo', payload=locals(), response_object=None)

	def GetEVPNLearnedInfo(self, SessionIndices):
		"""Executes the getEVPNLearnedInfo operation on the server.

		Get EVPN Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetEVPNLearnedInfo', payload=locals(), response_object=None)

	def GetEVPNLearnedInfo(self, Arg2):
		"""Executes the getEVPNLearnedInfo operation on the server.

		Fetches EVPN MAC IP routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetEVPNLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4LearnedInfo(self):
		"""Executes the getIPv4LearnedInfo operation on the server.

		Get IPv4 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv4LearnedInfo', payload=locals(), response_object=None)

	def GetIPv4LearnedInfo(self, SessionIndices):
		"""Executes the getIPv4LearnedInfo operation on the server.

		Get IPv4 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv4LearnedInfo', payload=locals(), response_object=None)

	def GetIPv4LearnedInfo(self, SessionIndices):
		"""Executes the getIPv4LearnedInfo operation on the server.

		Get IPv4 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv4LearnedInfo', payload=locals(), response_object=None)

	def GetIPv4LearnedInfo(self, Arg2):
		"""Executes the getIPv4LearnedInfo operation on the server.

		Fetches IPv4 routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIPv4LearnedInfo', payload=locals(), response_object=None)

	def GetIPv4MplsLearnedInfo(self, Arg2):
		"""Executes the getIPv4MplsLearnedInfo operation on the server.

		Fetches IPv4 MPLS routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIPv4MplsLearnedInfo', payload=locals(), response_object=None)

	def GetIpv4MvpnLearnedInfo(self, Arg2):
		"""Executes the getIpv4MvpnLearnedInfo operation on the server.

		Fetches MVPN MAC IP routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIpv4MvpnLearnedInfo', payload=locals(), response_object=None)

	def GetIpv4UmhRoutesLearnedInfo(self, Arg2):
		"""Executes the getIpv4UmhRoutesLearnedInfo operation on the server.

		Fetches Umh Routes learned by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIpv4UmhRoutesLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4VpnLearnedInfo(self):
		"""Executes the getIPv4VpnLearnedInfo operation on the server.

		Get IPv4 Vpn Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv4VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4VpnLearnedInfo(self, SessionIndices):
		"""Executes the getIPv4VpnLearnedInfo operation on the server.

		Get IPv4 Vpn Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv4VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4VpnLearnedInfo(self, SessionIndices):
		"""Executes the getIPv4VpnLearnedInfo operation on the server.

		Get IPv4 Vpn Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv4VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4VpnLearnedInfo(self, Arg2):
		"""Executes the getIPv4VpnLearnedInfo operation on the server.

		Fetches IPv4 VPN routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIPv4VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6LearnedInfo(self):
		"""Executes the getIPv6LearnedInfo operation on the server.

		Get IPv6 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv6LearnedInfo', payload=locals(), response_object=None)

	def GetIPv6LearnedInfo(self, SessionIndices):
		"""Executes the getIPv6LearnedInfo operation on the server.

		Get IPv6 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv6LearnedInfo', payload=locals(), response_object=None)

	def GetIPv6LearnedInfo(self, SessionIndices):
		"""Executes the getIPv6LearnedInfo operation on the server.

		Get IPv6 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv6LearnedInfo', payload=locals(), response_object=None)

	def GetIPv6LearnedInfo(self, Arg2):
		"""Executes the getIPv6LearnedInfo operation on the server.

		Gets IPv6 routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIPv6LearnedInfo', payload=locals(), response_object=None)

	def GetIPv6MplsLearnedInfo(self, Arg2):
		"""Executes the getIPv6MplsLearnedInfo operation on the server.

		Gets IPv6 Mpls routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIPv6MplsLearnedInfo', payload=locals(), response_object=None)

	def GetIpv6MvpnLearnedInfo(self, Arg2):
		"""Executes the getIpv6MvpnLearnedInfo operation on the server.

		Fetches MVPN MAC IP routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIpv6MvpnLearnedInfo', payload=locals(), response_object=None)

	def GetIpv6UmhRoutesLearnedInfo(self, Arg2):
		"""Executes the getIpv6UmhRoutesLearnedInfo operation on the server.

		Fetches Umh Route learned by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIpv6UmhRoutesLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6VpnLearnedInfo(self):
		"""Executes the getIPv6VpnLearnedInfo operation on the server.

		Get IPv6 Vpn Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv6VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6VpnLearnedInfo(self, SessionIndices):
		"""Executes the getIPv6VpnLearnedInfo operation on the server.

		Get IPv6 Vpn Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv6VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6VpnLearnedInfo(self, SessionIndices):
		"""Executes the getIPv6VpnLearnedInfo operation on the server.

		Get IPv6 Vpn Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetIPv6VpnLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6VpnLearnedInfo(self, Arg2):
		"""Executes the getIPv6VpnLearnedInfo operation on the server.

		Gets IPv6 VPN routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetIPv6VpnLearnedInfo', payload=locals(), response_object=None)

	def GetLinkStateLearnedInfo(self):
		"""Executes the getLinkStateLearnedInfo operation on the server.

		Get Link State Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetLinkStateLearnedInfo', payload=locals(), response_object=None)

	def GetLinkStateLearnedInfo(self, SessionIndices):
		"""Executes the getLinkStateLearnedInfo operation on the server.

		Get Link State Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetLinkStateLearnedInfo', payload=locals(), response_object=None)

	def GetLinkStateLearnedInfo(self, SessionIndices):
		"""Executes the getLinkStateLearnedInfo operation on the server.

		Get Link State Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetLinkStateLearnedInfo', payload=locals(), response_object=None)

	def GetLinkStateLearnedInfo(self, Arg2):
		"""Executes the getLinkStateLearnedInfo operation on the server.

		Fetches Link State Information learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetLinkStateLearnedInfo', payload=locals(), response_object=None)

	def GetVPLSLearnedInfo(self):
		"""Executes the getVPLSLearnedInfo operation on the server.

		Get VPLS Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetVPLSLearnedInfo(self, SessionIndices):
		"""Executes the getVPLSLearnedInfo operation on the server.

		Get VPLS Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetVPLSLearnedInfo(self, SessionIndices):
		"""Executes the getVPLSLearnedInfo operation on the server.

		Get VPLS Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetVPLSLearnedInfo', payload=locals(), response_object=None)

	def GetVPLSLearnedInfo(self, Arg2):
		"""Executes the getVPLSLearnedInfo operation on the server.

		Fetches VPLS routes learnt by this BGP peer.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetVPLSLearnedInfo', payload=locals(), response_object=None)

	def GracefulRestart(self, Restart_time):
		"""Executes the gracefulRestart operation on the server.

		Graceful restart Peers on selected Peer Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Restart_time (number): This parameter requires a restart_time of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GracefulRestart', payload=locals(), response_object=None)

	def GracefulRestart(self, Restart_time, SessionIndices):
		"""Executes the gracefulRestart operation on the server.

		Graceful restart Peers on selected Peer Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Restart_time (number): This parameter requires a restart_time of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GracefulRestart', payload=locals(), response_object=None)

	def GracefulRestart(self, SessionIndices, Restart_time):
		"""Executes the gracefulRestart operation on the server.

		Graceful restart Peers on selected Peer Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a restart_time of type kInteger
			Restart_time (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GracefulRestart', payload=locals(), response_object=None)

	def Gracefulrestart(self, Arg2, Arg3):
		"""Executes the gracefulrestart operation on the server.

		Graceful restart Peers on selected Peer Ranges.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.
			Arg3 (number): Restart After Time(in secs).

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Gracefulrestart', payload=locals(), response_object=None)

	def RestartDown(self):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def ResumeKeepAlive(self):
		"""Executes the resumeKeepAlive operation on the server.

		Resume sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumeKeepAlive', payload=locals(), response_object=None)

	def ResumeKeepAlive(self, SessionIndices):
		"""Executes the resumeKeepAlive operation on the server.

		Resume sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumeKeepAlive', payload=locals(), response_object=None)

	def ResumeKeepAlive(self, SessionIndices):
		"""Executes the resumeKeepAlive operation on the server.

		Resume sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumeKeepAlive', payload=locals(), response_object=None)

	def Resumekeepalive(self, Arg2):
		"""Executes the resumekeepalive operation on the server.

		Start Sending Keep Alive Messages.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Resumekeepalive', payload=locals(), response_object=None)

	def ResumeTCPSession(self, Notification_code, Notification_sub_code):
		"""Executes the resumeTCPSession operation on the server.

		Resume TCP Session

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Notification_code (number): This parameter requires a notification_code of type kInteger
			Notification_sub_code (number): This parameter requires a notification_sub_code of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumeTCPSession', payload=locals(), response_object=None)

	def ResumeTCPSession(self, Notification_code, Notification_sub_code, SessionIndices):
		"""Executes the resumeTCPSession operation on the server.

		Resume TCP Session

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Notification_code (number): This parameter requires a notification_code of type kInteger
			Notification_sub_code (number): This parameter requires a notification_sub_code of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumeTCPSession', payload=locals(), response_object=None)

	def ResumeTCPSession(self, SessionIndices, Notification_code, Notification_sub_code):
		"""Executes the resumeTCPSession operation on the server.

		Resume TCP Session

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a notification_code of type kInteger
			Notification_code (number): This parameter requires a notification_sub_code of type kInteger
			Notification_sub_code (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumeTCPSession', payload=locals(), response_object=None)

	def Resumetcpsession(self, Arg2, Arg3, Arg4):
		"""Executes the resumetcpsession operation on the server.

		Resume BGP Peer Range TCP Session.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.
			Arg3 (number): Notification Code
			Arg4 (number): Notification Sub Code

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Resumetcpsession', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start BGP Peer

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start BGP Peer

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start BGP Peer

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop BGP Peer

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop BGP Peer

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop BGP Peer

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def StopKeepAlive(self):
		"""Executes the stopKeepAlive operation on the server.

		Stop sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopKeepAlive', payload=locals(), response_object=None)

	def StopKeepAlive(self, SessionIndices):
		"""Executes the stopKeepAlive operation on the server.

		Stop sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopKeepAlive', payload=locals(), response_object=None)

	def StopKeepAlive(self, SessionIndices):
		"""Executes the stopKeepAlive operation on the server.

		Stop sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopKeepAlive', payload=locals(), response_object=None)

	def Stopkeepalive(self, Arg2):
		"""Executes the stopkeepalive operation on the server.

		Stop Sending Keep Alive Messages.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stopkeepalive', payload=locals(), response_object=None)
