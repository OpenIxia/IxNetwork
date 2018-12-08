
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


class BgpIPv6EvpnVpws(Base):
	"""The BgpIPv6EvpnVpws class encapsulates a user managed bgpIPv6EvpnVpws node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpIPv6EvpnVpws property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bgpIPv6EvpnVpws'

	def __init__(self, parent):
		super(BgpIPv6EvpnVpws, self).__init__(parent)

	@property
	def BgpAsPathSegmentList(self):
		"""An instance of the BgpAsPathSegmentList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpaspathsegmentlist.BgpAsPathSegmentList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpaspathsegmentlist import BgpAsPathSegmentList
		return BgpAsPathSegmentList(self)

	@property
	def BgpClusterIdList(self):
		"""An instance of the BgpClusterIdList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpclusteridlist.BgpClusterIdList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpclusteridlist import BgpClusterIdList
		return BgpClusterIdList(self)

	@property
	def BgpCommunitiesList(self):
		"""An instance of the BgpCommunitiesList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpcommunitieslist.BgpCommunitiesList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpcommunitieslist import BgpCommunitiesList
		return BgpCommunitiesList(self)

	@property
	def BgpExtendedCommunitiesList(self):
		"""An instance of the BgpExtendedCommunitiesList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpextendedcommunitieslist.BgpExtendedCommunitiesList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpextendedcommunitieslist import BgpExtendedCommunitiesList
		return BgpExtendedCommunitiesList(self)

	@property
	def BroadcastDomainV6Vpws(self):
		"""An instance of the BroadcastDomainV6Vpws class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.broadcastdomainv6vpws.BroadcastDomainV6Vpws)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.broadcastdomainv6vpws import BroadcastDomainV6Vpws
		return BroadcastDomainV6Vpws(self)._select()

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
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdRouteLabel(self):
		"""AD Route Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('adRouteLabel')

	@property
	def AdvertiseL3vniSeparately(self):
		"""Advertise L3 Route Separately

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseL3vniSeparately')

	@property
	def AggregatorAs(self):
		"""Aggregator AS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('aggregatorAs')

	@property
	def AggregatorId(self):
		"""Aggregator ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('aggregatorId')

	@property
	def AsSetMode(self):
		"""AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asSetMode')

	@property
	def AutoConfigPMSITunnelId(self):
		"""Auto Configure PMSI Tunnel ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoConfigPMSITunnelId')

	@property
	def AutoConfigureRdIpAddress(self):
		"""Auto-Configure RD IP Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoConfigureRdIpAddress')

	@property
	def BMacFirstLabel(self):
		"""B MAC First Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bMacFirstLabel')

	@property
	def BMacSecondLabel(self):
		"""B MAC Second Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bMacSecondLabel')

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
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnableAggregatorId(self):
		"""Enable Aggregator ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAggregatorId')

	@property
	def EnableAsPathSegments(self):
		"""Enable AS Path Segments

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAsPathSegments')

	@property
	def EnableAtomicAggregate(self):
		"""Enable Atomic Aggregate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAtomicAggregate')

	@property
	def EnableBMacSecondLabel(self):
		"""Enable B MAC Second Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBMacSecondLabel')

	@property
	def EnableCluster(self):
		"""Enable Cluster

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableCluster')

	@property
	def EnableCommunity(self):
		"""Enable Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableCommunity')

	@property
	def EnableExtendedCommunity(self):
		"""Enable Extended Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableExtendedCommunity')

	@property
	def EnableL3TargetOnlyForRouteType5(self):
		"""Enable L3 Target only for Route Type 5

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableL3TargetOnlyForRouteType5')

	@property
	def EnableL3vniTargetList(self):
		"""Enable L3 Target List

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableL3vniTargetList')

	@property
	def EnableLocalPreference(self):
		"""Enable Local Preference

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLocalPreference')

	@property
	def EnableMultiExitDiscriminator(self):
		"""Enable Multi Exit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableMultiExitDiscriminator')

	@property
	def EnableNextHop(self):
		"""Enable Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableNextHop')

	@property
	def EnableOrigin(self):
		"""Enable Origin

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableOrigin')

	@property
	def EnableOriginatorId(self):
		"""Enable Originator ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableOriginatorId')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def EsiType(self):
		"""ESI Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('esiType')

	@property
	def EsiValue(self):
		"""ESI Value

		Returns:
			list(str)
		"""
		return self._get_attribute('esiValue')

	@property
	def ImportRtListSameAsExportRtList(self):
		"""Import RT List Same As Export RT List

		Returns:
			bool
		"""
		return self._get_attribute('importRtListSameAsExportRtList')
	@ImportRtListSameAsExportRtList.setter
	def ImportRtListSameAsExportRtList(self, value):
		self._set_attribute('importRtListSameAsExportRtList', value)

	@property
	def IncludePmsiTunnelAttribute(self):
		"""Include PMSI Tunnel Attribute

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includePmsiTunnelAttribute')

	@property
	def Ipv4NextHop(self):
		"""IPv4 Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4NextHop')

	@property
	def Ipv6NextHop(self):
		"""IPv6 Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6NextHop')

	@property
	def L3vniImportRtListSameAsL3vniExportRtList(self):
		"""L3 Import RT List Same As L3 Export RT List

		Returns:
			bool
		"""
		return self._get_attribute('l3vniImportRtListSameAsL3vniExportRtList')
	@L3vniImportRtListSameAsL3vniExportRtList.setter
	def L3vniImportRtListSameAsL3vniExportRtList(self, value):
		self._set_attribute('l3vniImportRtListSameAsL3vniExportRtList', value)

	@property
	def LocalPreference(self):
		"""Local Preference

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localPreference')

	@property
	def MultiExitDiscriminator(self):
		"""Multi Exit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multiExitDiscriminator')

	@property
	def MulticastTunnelType(self):
		"""Multicast Tunnel Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastTunnelType')

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
	def NoOfASPathSegmentsPerRouteRange(self):
		"""Number Of AS Path Segments Per Route Range

		Returns:
			number
		"""
		return self._get_attribute('noOfASPathSegmentsPerRouteRange')
	@NoOfASPathSegmentsPerRouteRange.setter
	def NoOfASPathSegmentsPerRouteRange(self, value):
		self._set_attribute('noOfASPathSegmentsPerRouteRange', value)

	@property
	def NoOfClusters(self):
		"""Number of Clusters

		Returns:
			number
		"""
		return self._get_attribute('noOfClusters')
	@NoOfClusters.setter
	def NoOfClusters(self, value):
		self._set_attribute('noOfClusters', value)

	@property
	def NoOfCommunities(self):
		"""Number of Communities

		Returns:
			number
		"""
		return self._get_attribute('noOfCommunities')
	@NoOfCommunities.setter
	def NoOfCommunities(self, value):
		self._set_attribute('noOfCommunities', value)

	@property
	def NoOfExtendedCommunity(self):
		"""Number of Extended Communities

		Returns:
			number
		"""
		return self._get_attribute('noOfExtendedCommunity')
	@NoOfExtendedCommunity.setter
	def NoOfExtendedCommunity(self, value):
		self._set_attribute('noOfExtendedCommunity', value)

	@property
	def NumBroadcastDomainV6(self):
		"""The number of broadcast domain to be configured under EVI

		Returns:
			number
		"""
		return self._get_attribute('numBroadcastDomainV6')
	@NumBroadcastDomainV6.setter
	def NumBroadcastDomainV6(self, value):
		self._set_attribute('numBroadcastDomainV6', value)

	@property
	def NumRtInExportRouteTargetList(self):
		"""Number of RTs in Export Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInExportRouteTargetList')
	@NumRtInExportRouteTargetList.setter
	def NumRtInExportRouteTargetList(self, value):
		self._set_attribute('numRtInExportRouteTargetList', value)

	@property
	def NumRtInImportRouteTargetList(self):
		"""Number of RTs in Import Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInImportRouteTargetList')
	@NumRtInImportRouteTargetList.setter
	def NumRtInImportRouteTargetList(self, value):
		self._set_attribute('numRtInImportRouteTargetList', value)

	@property
	def NumRtInL3vniExportRouteTargetList(self):
		"""Number of RTs in L3 Export Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInL3vniExportRouteTargetList')
	@NumRtInL3vniExportRouteTargetList.setter
	def NumRtInL3vniExportRouteTargetList(self, value):
		self._set_attribute('numRtInL3vniExportRouteTargetList', value)

	@property
	def NumRtInL3vniImportRouteTargetList(self):
		"""Number of RTs in L3 Import Route Target List(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('numRtInL3vniImportRouteTargetList')
	@NumRtInL3vniImportRouteTargetList.setter
	def NumRtInL3vniImportRouteTargetList(self, value):
		self._set_attribute('numRtInL3vniImportRouteTargetList', value)

	@property
	def Origin(self):
		"""Origin

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('origin')

	@property
	def OriginatorId(self):
		"""Originator ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('originatorId')

	@property
	def OverridePeerAsSetMode(self):
		"""Override Peer AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overridePeerAsSetMode')

	@property
	def PmsiTunnelIDv4(self):
		"""PMSI Tunnel ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pmsiTunnelIDv4')

	@property
	def PmsiTunnelIDv6(self):
		"""PMSI Tunnel ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pmsiTunnelIDv6')

	@property
	def RdEvi(self):
		"""RD EVI

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rdEvi')

	@property
	def RdIpAddress(self):
		"""RD IP Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rdIpAddress')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SetNextHop(self):
		"""Set Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setNextHop')

	@property
	def SetNextHopIpType(self):
		"""Set Next Hop IP Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setNextHopIpType')

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
	def UpstreamDownstreamAssignedMplsLabel(self):
		"""Upstream/Downstream Assigned MPLS Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('upstreamDownstreamAssignedMplsLabel')

	@property
	def UseIpv4MappedIpv6Address(self):
		"""Use IPv4 Mapped IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useIpv4MappedIpv6Address')

	@property
	def UseUpstreamDownstreamAssignedMplsLabel(self):
		"""Use Upstream/Downstream Assigned MPLS Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useUpstreamDownstreamAssignedMplsLabel')

	def add(self, ConnectedVia=None, ImportRtListSameAsExportRtList=None, L3vniImportRtListSameAsL3vniExportRtList=None, Multiplier=None, Name=None, NoOfASPathSegmentsPerRouteRange=None, NoOfClusters=None, NoOfCommunities=None, NoOfExtendedCommunity=None, NumBroadcastDomainV6=None, NumRtInExportRouteTargetList=None, NumRtInImportRouteTargetList=None, NumRtInL3vniExportRouteTargetList=None, NumRtInL3vniImportRouteTargetList=None, StackedLayers=None):
		"""Adds a new bgpIPv6EvpnVpws node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			ImportRtListSameAsExportRtList (bool): Import RT List Same As Export RT List
			L3vniImportRtListSameAsL3vniExportRtList (bool): L3 Import RT List Same As L3 Export RT List
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExtendedCommunity (number): Number of Extended Communities
			NumBroadcastDomainV6 (number): The number of broadcast domain to be configured under EVI
			NumRtInExportRouteTargetList (number): Number of RTs in Export Route Target List(multiplier)
			NumRtInImportRouteTargetList (number): Number of RTs in Import Route Target List(multiplier)
			NumRtInL3vniExportRouteTargetList (number): Number of RTs in L3 Export Route Target List(multiplier)
			NumRtInL3vniImportRouteTargetList (number): Number of RTs in L3 Import Route Target List(multiplier)
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved bgpIPv6EvpnVpws data using find and the newly added bgpIPv6EvpnVpws data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bgpIPv6EvpnVpws data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, EsiValue=None, ImportRtListSameAsExportRtList=None, L3vniImportRtListSameAsL3vniExportRtList=None, Multiplier=None, Name=None, NoOfASPathSegmentsPerRouteRange=None, NoOfClusters=None, NoOfCommunities=None, NoOfExtendedCommunity=None, NumBroadcastDomainV6=None, NumRtInExportRouteTargetList=None, NumRtInImportRouteTargetList=None, NumRtInL3vniExportRouteTargetList=None, NumRtInL3vniImportRouteTargetList=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves bgpIPv6EvpnVpws data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpIPv6EvpnVpws data from the server.
		By default the find method takes no parameters and will retrieve all bgpIPv6EvpnVpws data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			EsiValue (list(str)): ESI Value
			ImportRtListSameAsExportRtList (bool): Import RT List Same As Export RT List
			L3vniImportRtListSameAsL3vniExportRtList (bool): L3 Import RT List Same As L3 Export RT List
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExtendedCommunity (number): Number of Extended Communities
			NumBroadcastDomainV6 (number): The number of broadcast domain to be configured under EVI
			NumRtInExportRouteTargetList (number): Number of RTs in Export Route Target List(multiplier)
			NumRtInImportRouteTargetList (number): Number of RTs in Import Route Target List(multiplier)
			NumRtInL3vniExportRouteTargetList (number): Number of RTs in L3 Export Route Target List(multiplier)
			NumRtInL3vniImportRouteTargetList (number): Number of RTs in L3 Import Route Target List(multiplier)
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching bgpIPv6EvpnVpws data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgpIPv6EvpnVpws data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgpIPv6EvpnVpws data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, Active=None, AdRouteLabel=None, AdvertiseL3vniSeparately=None, AggregatorAs=None, AggregatorId=None, AsSetMode=None, AutoConfigPMSITunnelId=None, AutoConfigureRdIpAddress=None, BMacFirstLabel=None, BMacSecondLabel=None, EnableAggregatorId=None, EnableAsPathSegments=None, EnableAtomicAggregate=None, EnableBMacSecondLabel=None, EnableCluster=None, EnableCommunity=None, EnableExtendedCommunity=None, EnableL3TargetOnlyForRouteType5=None, EnableL3vniTargetList=None, EnableLocalPreference=None, EnableMultiExitDiscriminator=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EsiType=None, IncludePmsiTunnelAttribute=None, Ipv4NextHop=None, Ipv6NextHop=None, LocalPreference=None, MultiExitDiscriminator=None, MulticastTunnelType=None, Origin=None, OriginatorId=None, OverridePeerAsSetMode=None, PmsiTunnelIDv4=None, PmsiTunnelIDv6=None, RdEvi=None, RdIpAddress=None, SetNextHop=None, SetNextHopIpType=None, UpstreamDownstreamAssignedMplsLabel=None, UseIpv4MappedIpv6Address=None, UseUpstreamDownstreamAssignedMplsLabel=None):
		"""Base class infrastructure that gets a list of bgpIPv6EvpnVpws device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AdRouteLabel (str): optional regex of adRouteLabel
			AdvertiseL3vniSeparately (str): optional regex of advertiseL3vniSeparately
			AggregatorAs (str): optional regex of aggregatorAs
			AggregatorId (str): optional regex of aggregatorId
			AsSetMode (str): optional regex of asSetMode
			AutoConfigPMSITunnelId (str): optional regex of autoConfigPMSITunnelId
			AutoConfigureRdIpAddress (str): optional regex of autoConfigureRdIpAddress
			BMacFirstLabel (str): optional regex of bMacFirstLabel
			BMacSecondLabel (str): optional regex of bMacSecondLabel
			EnableAggregatorId (str): optional regex of enableAggregatorId
			EnableAsPathSegments (str): optional regex of enableAsPathSegments
			EnableAtomicAggregate (str): optional regex of enableAtomicAggregate
			EnableBMacSecondLabel (str): optional regex of enableBMacSecondLabel
			EnableCluster (str): optional regex of enableCluster
			EnableCommunity (str): optional regex of enableCommunity
			EnableExtendedCommunity (str): optional regex of enableExtendedCommunity
			EnableL3TargetOnlyForRouteType5 (str): optional regex of enableL3TargetOnlyForRouteType5
			EnableL3vniTargetList (str): optional regex of enableL3vniTargetList
			EnableLocalPreference (str): optional regex of enableLocalPreference
			EnableMultiExitDiscriminator (str): optional regex of enableMultiExitDiscriminator
			EnableNextHop (str): optional regex of enableNextHop
			EnableOrigin (str): optional regex of enableOrigin
			EnableOriginatorId (str): optional regex of enableOriginatorId
			EsiType (str): optional regex of esiType
			IncludePmsiTunnelAttribute (str): optional regex of includePmsiTunnelAttribute
			Ipv4NextHop (str): optional regex of ipv4NextHop
			Ipv6NextHop (str): optional regex of ipv6NextHop
			LocalPreference (str): optional regex of localPreference
			MultiExitDiscriminator (str): optional regex of multiExitDiscriminator
			MulticastTunnelType (str): optional regex of multicastTunnelType
			Origin (str): optional regex of origin
			OriginatorId (str): optional regex of originatorId
			OverridePeerAsSetMode (str): optional regex of overridePeerAsSetMode
			PmsiTunnelIDv4 (str): optional regex of pmsiTunnelIDv4
			PmsiTunnelIDv6 (str): optional regex of pmsiTunnelIDv6
			RdEvi (str): optional regex of rdEvi
			RdIpAddress (str): optional regex of rdIpAddress
			SetNextHop (str): optional regex of setNextHop
			SetNextHopIpType (str): optional regex of setNextHopIpType
			UpstreamDownstreamAssignedMplsLabel (str): optional regex of upstreamDownstreamAssignedMplsLabel
			UseIpv4MappedIpv6Address (str): optional regex of useIpv4MappedIpv6Address
			UseUpstreamDownstreamAssignedMplsLabel (str): optional regex of useUpstreamDownstreamAssignedMplsLabel

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

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

	def Start(self):
		"""Executes the start operation on the server.

		Start selected protocols.

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

		Start selected protocols.

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

		Start selected protocols.

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

		Stop selected protocols.

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

		Stop selected protocols.

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

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
