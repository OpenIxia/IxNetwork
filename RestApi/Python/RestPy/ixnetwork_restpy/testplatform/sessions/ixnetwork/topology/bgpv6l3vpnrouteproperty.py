from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpV6L3VpnRouteProperty(Base):
	"""The BgpV6L3VpnRouteProperty class encapsulates a user managed bgpV6L3VpnRouteProperty node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpV6L3VpnRouteProperty property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bgpV6L3VpnRouteProperty'

	def __init__(self, parent):
		super(BgpV6L3VpnRouteProperty, self).__init__(parent)

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
	def CMacProperties(self):
		"""An instance of the CMacProperties class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return CMacProperties(self)

	@property
	def EvpnIPv4PrefixRange(self):
		"""An instance of the EvpnIPv4PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return EvpnIPv4PrefixRange(self)

	@property
	def EvpnIPv6PrefixRange(self):
		"""An instance of the EvpnIPv6PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return EvpnIPv6PrefixRange(self)

	@property
	def OverridePeerAsSetMode(self):
		"""Override Peer AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('OverridePeerAsSetMode')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvSrv6SidInIgp(self):
		"""Advertise SRv6 SID in IGP (ISIS)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advSrv6SidInIgp')

	@property
	def AdvertiseNexthopAsV4(self):
		"""Advertise Nexthop as V4

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseNexthopAsV4')

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
	def AggregatorIdMode(self):
		"""Aggregator ID Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('aggregatorIdMode')

	@property
	def AsNumSuffixRange(self):
		"""Supported Formats: value value1-value2 Values or value ranges separated by comma(,). e.g. 100,150-200,400,600-800 etc. Cannot be kept empty. Should be >= (Max Number of AS Path Segments) x (Max AS Numbers Per Segment)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumSuffixRange')

	@property
	def AsPathASString(self):
		"""Displays configured AS paths. Random AS paths are appended after Non-Random AS paths when configured. Each row displays the AS Path configured for the 1st route of a Route Range.

		Returns:
			list(str)
		"""
		return self._get_attribute('asPathASString')

	@property
	def AsPathPerRoute(self):
		"""When there are multiple routes in a route range, this option decides whether to use same or different AS paths randomly generated for all the routes within that route range. For the Different option, each route will be sent in different update messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asPathPerRoute')

	@property
	def AsRandomSeed(self):
		"""Seed value decides the way the AS Values are generated. To generate different AS Paths for different Route ranges, select unique Seed Values.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asRandomSeed')

	@property
	def AsSegDist(self):
		"""Type of AS Segment generated. If user selects Random, then any of the four types (AS-SET, AS-SEQ, AS-SET-CONFEDERATION, AS-SEQ-CONFEDERATION) will get randomly generated.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asSegDist')

	@property
	def AsSetMode(self):
		"""AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asSetMode')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Delay(self):
		"""Delay

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delay')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DistinguisherAsNumber(self):
		"""L3VPN RR Distinguisher AS Number (2-byte or 4-Byte)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('distinguisherAsNumber')

	@property
	def DistinguisherAssignedNumber(self):
		"""L3VPN RR Distinguisher Assigned Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('distinguisherAssignedNumber')

	@property
	def DistinguisherIpAddress(self):
		"""L3VPN RR Distinguisher IP Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('distinguisherIpAddress')

	@property
	def DistinguisherType(self):
		"""L3VPN RR Distinguisher Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('distinguisherType')

	@property
	def Downtime(self):
		"""Downtime In Seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('downtime')

	@property
	def EnableAggregatorId(self):
		"""Enable Aggregator ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAggregatorId')

	@property
	def EnableAsPathSegments(self):
		"""Enable Non-Random AS Path Segments

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
	def EnableFlapping(self):
		"""Enable Flapping

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFlapping')

	@property
	def EnableIpv6Receiver(self):
		"""Enable IPv6 Receiver

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv6Receiver')
	@EnableIpv6Receiver.setter
	def EnableIpv6Receiver(self, value):
		self._set_attribute('enableIpv6Receiver', value)

	@property
	def EnableIpv6Sender(self):
		"""Enable IPv6 Sender

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv6Sender')
	@EnableIpv6Sender.setter
	def EnableIpv6Sender(self, value):
		self._set_attribute('enableIpv6Sender', value)

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
	def EnableRandomAsPath(self):
		"""Enables generation/advertisement of Random AS Path Segments.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRandomAsPath')

	@property
	def EnableSrv6Sid(self):
		"""Enable SRv6 SID With VPN Route

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableSrv6Sid')

	@property
	def EnableWeight(self):
		"""Enable Weight

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableWeight')

	@property
	def FlapFromRouteIndex(self):
		"""Flap From Route Index

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flapFromRouteIndex')

	@property
	def FlapToRouteIndex(self):
		"""Flap To Route Index

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flapToRouteIndex')

	@property
	def IncludeRdInNextHopLength(self):
		"""If RD is included in NH Len then NH Len is NH size + RD size else NH len is NH size.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeRdInNextHopLength')

	@property
	def IncludeSourceAsExtComm(self):
		"""Include Source AS ExtComm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSourceAsExtComm')

	@property
	def IncludeVrfRouteImportExtComm(self):
		"""Include VRF Route Import ExtComm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeVrfRouteImportExtComm')

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
	def LabelEnd(self):
		"""L3VPN RR Label End

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelEnd')

	@property
	def LabelMode(self):
		"""L3VPN RR Label Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelMode')

	@property
	def LabelSpaceId(self):
		"""L3VPN RR Label Space ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelSpaceId')

	@property
	def LabelStart(self):
		"""L3VPN RR Label Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelStart')

	@property
	def LabelStep(self):
		"""L3VPN RR Label Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelStep')

	@property
	def LocalPreference(self):
		"""Local Preference

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localPreference')

	@property
	def MaxASNumPerSegment(self):
		"""Maximum Number Of AS Numbers generated per Segment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxASNumPerSegment')

	@property
	def MaxNoOfASPathSegmentsPerRouteRange(self):
		"""Maximum Number Of AS Path Segments Per Route Range.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxNoOfASPathSegmentsPerRouteRange')

	@property
	def MinASNumPerSegment(self):
		"""Minimum Number Of AS Numbers generated per Segments.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minASNumPerSegment')

	@property
	def MinNoOfASPathSegmentsPerRouteRange(self):
		"""Minimum Number Of AS Path Segments Per Route Range.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minNoOfASPathSegmentsPerRouteRange')

	@property
	def MultiExitDiscriminator(self):
		"""Multi Exit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multiExitDiscriminator')

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
	def NextHopIPType(self):
		"""Set Next Hop IP Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nextHopIPType')

	@property
	def NextHopIncrementMode(self):
		"""Next Hop Increment Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nextHopIncrementMode')

	@property
	def NextHopType(self):
		"""Set Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nextHopType')

	@property
	def NoOfASPathSegmentsPerRouteRange(self):
		"""Number Of non-random or manually configured AS Path Segments Per Route Range

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
	def NoOfExternalCommunities(self):
		"""Number of Extended Communities

		Returns:
			number
		"""
		return self._get_attribute('noOfExternalCommunities')
	@NoOfExternalCommunities.setter
	def NoOfExternalCommunities(self, value):
		self._set_attribute('noOfExternalCommunities', value)

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
	def PackingFrom(self):
		"""Packing From

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packingFrom')

	@property
	def PackingTo(self):
		"""Packing To

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packingTo')

	@property
	def PartialFlap(self):
		"""Partial Flap

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('partialFlap')

	@property
	def Srv6SidFlags(self):
		"""SRv6 SID Flags field Value for all route in this Route Range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidFlags')

	@property
	def Srv6SidFuncAllocType(self):
		"""SRv6 Func Allocation Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidFuncAllocType')

	@property
	def Srv6SidLoc(self):
		"""SRv6 SID. It consists of Locator, Func and Args

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidLoc')

	@property
	def Srv6SidLocLen(self):
		"""SRv6 SID Locator Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidLocLen')

	@property
	def Srv6SidLocMetric(self):
		"""SRv6 SID Locator Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidLocMetric')

	@property
	def Srv6SidReserved(self):
		"""SRv6 SID Reserved Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidReserved')

	@property
	def Srv6SidStep(self):
		"""Route Range SRv6 SID Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6SidStep')

	@property
	def Uptime(self):
		"""Uptime In Seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('uptime')

	@property
	def UseAsIpv6UmhRoutes(self):
		"""Use As IPv6 UMH Routes

		Returns:
			bool
		"""
		return self._get_attribute('useAsIpv6UmhRoutes')
	@UseAsIpv6UmhRoutes.setter
	def UseAsIpv6UmhRoutes(self, value):
		self._set_attribute('useAsIpv6UmhRoutes', value)

	@property
	def UseAsUmhRoutes(self):
		"""Use As UMH Routes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useAsUmhRoutes')

	@property
	def UseTraditionalNlri(self):
		"""Use Traditional NLRI

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useTraditionalNlri')

	@property
	def Weight(self):
		"""Weight

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')

	def add(self, EnableIpv6Receiver=None, EnableIpv6Sender=None, Name=None, NoOfASPathSegmentsPerRouteRange=None, NoOfClusters=None, NoOfCommunities=None, NoOfExternalCommunities=None, UseAsIpv6UmhRoutes=None):
		"""Adds a new bgpV6L3VpnRouteProperty node on the server and retrieves it in this instance.

		Args:
			EnableIpv6Receiver (bool): Enable IPv6 Receiver
			EnableIpv6Sender (bool): Enable IPv6 Sender
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of non-random or manually configured AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExternalCommunities (number): Number of Extended Communities
			UseAsIpv6UmhRoutes (bool): Use As IPv6 UMH Routes

		Returns:
			self: This instance with all currently retrieved bgpV6L3VpnRouteProperty data using find and the newly added bgpV6L3VpnRouteProperty data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bgpV6L3VpnRouteProperty data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AsPathASString=None, Count=None, DescriptiveName=None, EnableIpv6Receiver=None, EnableIpv6Sender=None, Name=None, NoOfASPathSegmentsPerRouteRange=None, NoOfClusters=None, NoOfCommunities=None, NoOfExternalCommunities=None, UseAsIpv6UmhRoutes=None):
		"""Finds and retrieves bgpV6L3VpnRouteProperty data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpV6L3VpnRouteProperty data from the server.
		By default the find method takes no parameters and will retrieve all bgpV6L3VpnRouteProperty data from the server.

		Args:
			AsPathASString (list(str)): Displays configured AS paths. Random AS paths are appended after Non-Random AS paths when configured. Each row displays the AS Path configured for the 1st route of a Route Range.
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableIpv6Receiver (bool): Enable IPv6 Receiver
			EnableIpv6Sender (bool): Enable IPv6 Sender
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfASPathSegmentsPerRouteRange (number): Number Of non-random or manually configured AS Path Segments Per Route Range
			NoOfClusters (number): Number of Clusters
			NoOfCommunities (number): Number of Communities
			NoOfExternalCommunities (number): Number of Extended Communities
			UseAsIpv6UmhRoutes (bool): Use As IPv6 UMH Routes

		Returns:
			self: This instance with matching bgpV6L3VpnRouteProperty data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgpV6L3VpnRouteProperty data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgpV6L3VpnRouteProperty data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AgeOutRoutes(self, Percentage):
		"""Executes the ageOutRoutes operation on the server.

		Age out percentage of BGP Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Percentage (number): This parameter requires a percentage of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AgeOutRoutes', payload=locals(), response_object=None)

	def AgeOutRoutes(self, Percentage, SessionIndices):
		"""Executes the ageOutRoutes operation on the server.

		Age out percentage of BGP Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Percentage (number): This parameter requires a percentage of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AgeOutRoutes', payload=locals(), response_object=None)

	def AgeOutRoutes(self, SessionIndices, Percentage):
		"""Executes the ageOutRoutes operation on the server.

		Age out percentage of BGP Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a percentage of type kInteger
			Percentage (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AgeOutRoutes', payload=locals(), response_object=None)

	def Ageoutroutes(self, Arg2, Arg3):
		"""Executes the ageoutroutes operation on the server.

		Completely/Partially age out routes contained in this route range.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.
			Arg3 (number): What percentage of routes to age out. 100% means all routes.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Ageoutroutes', payload=locals(), response_object=None)

	def EnableIpv4Receiver(self):
		"""Executes the enableIpv4Receiver operation on the server.

		Activate or Deactivate Ipv4 Multicast Receiver Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv4Receiver', payload=locals(), response_object=None)

	def EnableIpv4Receiver(self, SessionIndices):
		"""Executes the enableIpv4Receiver operation on the server.

		Activate or Deactivate Ipv4 Multicast Receiver Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv4Receiver', payload=locals(), response_object=None)

	def EnableIpv4Receiver(self, SessionIndices):
		"""Executes the enableIpv4Receiver operation on the server.

		Activate or Deactivate Ipv4 Multicast Receiver Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv4Receiver', payload=locals(), response_object=None)

	def EnableIpv4Sender(self):
		"""Executes the enableIpv4Sender operation on the server.

		Activate or Deactivate Ipv4 Multicast Sender Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv4Sender', payload=locals(), response_object=None)

	def EnableIpv4Sender(self, SessionIndices):
		"""Executes the enableIpv4Sender operation on the server.

		Activate or Deactivate Ipv4 Multicast Sender Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv4Sender', payload=locals(), response_object=None)

	def EnableIpv4Sender(self, SessionIndices):
		"""Executes the enableIpv4Sender operation on the server.

		Activate or Deactivate Ipv4 Multicast Sender Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv4Sender', payload=locals(), response_object=None)

	def EnableIpv6Receiver(self):
		"""Executes the enableIpv6Receiver operation on the server.

		Activate or Deactivate Ipv6 Multicast Receiver Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv6Receiver', payload=locals(), response_object=None)

	def EnableIpv6Receiver(self, SessionIndices):
		"""Executes the enableIpv6Receiver operation on the server.

		Activate or Deactivate Ipv6 Multicast Receiver Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv6Receiver', payload=locals(), response_object=None)

	def EnableIpv6Receiver(self, SessionIndices):
		"""Executes the enableIpv6Receiver operation on the server.

		Activate or Deactivate Ipv6 Multicast Receiver Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv6Receiver', payload=locals(), response_object=None)

	def EnableIpv6Sender(self):
		"""Executes the enableIpv6Sender operation on the server.

		Activate or Deactivate Ipv6 Multicast Sender Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv6Sender', payload=locals(), response_object=None)

	def EnableIpv6Sender(self, SessionIndices):
		"""Executes the enableIpv6Sender operation on the server.

		Activate or Deactivate Ipv6 Multicast Sender Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv6Sender', payload=locals(), response_object=None)

	def EnableIpv6Sender(self, SessionIndices):
		"""Executes the enableIpv6Sender operation on the server.

		Activate or Deactivate Ipv6 Multicast Sender Site

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableIpv6Sender', payload=locals(), response_object=None)

	def ReadvertiseRoutes(self):
		"""Executes the readvertiseRoutes operation on the server.

		Re-advertise Aged out OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReadvertiseRoutes', payload=locals(), response_object=None)

	def ReadvertiseRoutes(self, SessionIndices):
		"""Executes the readvertiseRoutes operation on the server.

		Re-advertise Aged out OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReadvertiseRoutes', payload=locals(), response_object=None)

	def ReadvertiseRoutes(self, SessionIndices):
		"""Executes the readvertiseRoutes operation on the server.

		Re-advertise Aged out OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReadvertiseRoutes', payload=locals(), response_object=None)

	def Readvertiseroutes(self, Arg2):
		"""Executes the readvertiseroutes operation on the server.

		Readvertise only the aged-out routes contained in this route range.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Readvertiseroutes', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start BGP Route Range

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

		Start BGP Route Range

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

		Start BGP Route Range

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

		Stop BGP Route Range

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

		Stop BGP Route Range

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

		Stop BGP Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def UseAsIpv4UmhRoutes(self):
		"""Executes the useAsIpv4UmhRoutes operation on the server.

		Activate Deactivate Ipv4 UMH Route Selection

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UseAsIpv4UmhRoutes', payload=locals(), response_object=None)

	def UseAsIpv4UmhRoutes(self, SessionIndices):
		"""Executes the useAsIpv4UmhRoutes operation on the server.

		Activate Deactivate Ipv4 UMH Route Selection

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UseAsIpv4UmhRoutes', payload=locals(), response_object=None)

	def UseAsIpv4UmhRoutes(self, SessionIndices):
		"""Executes the useAsIpv4UmhRoutes operation on the server.

		Activate Deactivate Ipv4 UMH Route Selection

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UseAsIpv4UmhRoutes', payload=locals(), response_object=None)

	def UseAsIpv6UmhRoutes(self):
		"""Executes the useAsIpv6UmhRoutes operation on the server.

		Activate Deactivate Ipv6 UMH Route Selection

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UseAsIpv6UmhRoutes', payload=locals(), response_object=None)

	def UseAsIpv6UmhRoutes(self, SessionIndices):
		"""Executes the useAsIpv6UmhRoutes operation on the server.

		Activate Deactivate Ipv6 UMH Route Selection

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UseAsIpv6UmhRoutes', payload=locals(), response_object=None)

	def UseAsIpv6UmhRoutes(self, SessionIndices):
		"""Executes the useAsIpv6UmhRoutes operation on the server.

		Activate Deactivate Ipv6 UMH Route Selection

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UseAsIpv6UmhRoutes', payload=locals(), response_object=None)
