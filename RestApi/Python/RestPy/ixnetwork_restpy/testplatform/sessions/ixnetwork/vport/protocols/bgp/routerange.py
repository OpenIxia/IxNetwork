from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RouteRange(Base):
	"""The RouteRange class encapsulates a user managed routeRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'routeRange'

	def __init__(self, parent):
		super(RouteRange, self).__init__(parent)

	@property
	def AsSegment(self):
		"""An instance of the AsSegment class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.assegment.AsSegment)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.assegment import AsSegment
		return AsSegment(self)._select()

	@property
	def Cluster(self):
		"""An instance of the Cluster class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cluster.Cluster)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cluster import Cluster
		return Cluster(self)._select()

	@property
	def Community(self):
		"""An instance of the Community class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.community.Community)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.community import Community
		return Community(self)._select()

	@property
	def ExtendedCommunity(self):
		"""An instance of the ExtendedCommunity class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.extendedcommunity.ExtendedCommunity)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.extendedcommunity import ExtendedCommunity
		return ExtendedCommunity(self)._select()

	@property
	def Flapping(self):
		"""An instance of the Flapping class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.flapping.Flapping)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.flapping import Flapping
		return Flapping(self)._select()

	@property
	def AdvertiseNextHopAsV4(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('advertiseNextHopAsV4')
	@AdvertiseNextHopAsV4.setter
	def AdvertiseNextHopAsV4(self, value):
		self._set_attribute('advertiseNextHopAsV4', value)

	@property
	def AggregatorAsNum(self):
		"""Sets the AS associated with the aggregator router ID.

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAsNum')
	@AggregatorAsNum.setter
	def AggregatorAsNum(self, value):
		self._set_attribute('aggregatorAsNum', value)

	@property
	def AggregatorIpAddress(self):
		"""The IP address for the aggregator.

		Returns:
			str
		"""
		return self._get_attribute('aggregatorIpAddress')
	@AggregatorIpAddress.setter
	def AggregatorIpAddress(self, value):
		self._set_attribute('aggregatorIpAddress', value)

	@property
	def AsPathSetMode(self):
		"""The mode to set the AsPath.

		Returns:
			str(noInclude|includeAsSeq|includeAsSet|includeAsSeqConf|includeAsSetConf|prependAs)
		"""
		return self._get_attribute('asPathSetMode')
	@AsPathSetMode.setter
	def AsPathSetMode(self, value):
		self._set_attribute('asPathSetMode', value)

	@property
	def EnableAggregator(self):
		"""If enabled, generates an aggregator attribute that indicates the router ID that aggregated two or more routes into one.

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregator')
	@EnableAggregator.setter
	def EnableAggregator(self, value):
		self._set_attribute('enableAggregator', value)

	@property
	def EnableAggregatorIdIncrementMode(self):
		"""The mode for the router ID of the router that aggregated two or more routes into one. Choose one of the following options: (1) Fixed-the same Aggregator ID will be used each time. (2) Increment-the Aggregator ID will increment by 1.

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregatorIdIncrementMode')
	@EnableAggregatorIdIncrementMode.setter
	def EnableAggregatorIdIncrementMode(self, value):
		self._set_attribute('enableAggregatorIdIncrementMode', value)

	@property
	def EnableAsPath(self):
		"""Indicates that AS-PATH attributes are to be generated.

		Returns:
			bool
		"""
		return self._get_attribute('enableAsPath')
	@EnableAsPath.setter
	def EnableAsPath(self, value):
		self._set_attribute('enableAsPath', value)

	@property
	def EnableAtomicAttribute(self):
		"""Sets the attribute bit that indicates the router has aggregated two or more prefixes together into one.

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAttribute')
	@EnableAtomicAttribute.setter
	def EnableAtomicAttribute(self, value):
		self._set_attribute('enableAtomicAttribute', value)

	@property
	def EnableCluster(self):
		"""Generates a list of BGP clusters that a particular route has passed through.

		Returns:
			bool
		"""
		return self._get_attribute('enableCluster')
	@EnableCluster.setter
	def EnableCluster(self, value):
		self._set_attribute('enableCluster', value)

	@property
	def EnableCommunity(self):
		"""Indicates that a community attribute should be added to the BGP entry.

		Returns:
			bool
		"""
		return self._get_attribute('enableCommunity')
	@EnableCommunity.setter
	def EnableCommunity(self, value):
		self._set_attribute('enableCommunity', value)

	@property
	def EnableGenerateUniqueRoutes(self):
		"""Enables the generate unique routes option. Without this option enabled, every neighbor in the range will generate exactly the same set of routes, starting from the first route.

		Returns:
			bool
		"""
		return self._get_attribute('enableGenerateUniqueRoutes')
	@EnableGenerateUniqueRoutes.setter
	def EnableGenerateUniqueRoutes(self, value):
		self._set_attribute('enableGenerateUniqueRoutes', value)

	@property
	def EnableIncludeLoopback(self):
		"""Includes loopback addresses (for example, 127.0.0.0 for IPv4) in the list of VPN route ranges.

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeLoopback')
	@EnableIncludeLoopback.setter
	def EnableIncludeLoopback(self, value):
		self._set_attribute('enableIncludeLoopback', value)

	@property
	def EnableIncludeMulticast(self):
		"""Includes multicast addresses (for example, 224.0.0.0 for IPv4) in the list of VPN route ranges.

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeMulticast')
	@EnableIncludeMulticast.setter
	def EnableIncludeMulticast(self, value):
		self._set_attribute('enableIncludeMulticast', value)

	@property
	def EnableLocalPref(self):
		"""inserts a LOCAL PREF attribute with the indicated value. (INTERNAL BGP only)

		Returns:
			bool
		"""
		return self._get_attribute('enableLocalPref')
	@EnableLocalPref.setter
	def EnableLocalPref(self, value):
		self._set_attribute('enableLocalPref', value)

	@property
	def EnableMed(self):
		"""Inserts a multi-exit discriminator (MED) attribute with the indicated value.

		Returns:
			bool
		"""
		return self._get_attribute('enableMed')
	@EnableMed.setter
	def EnableMed(self, value):
		self._set_attribute('enableMed', value)

	@property
	def EnableNextHop(self):
		"""Enables Next Hop. Inserts a Next Hop attribute that indicates the next router to send packets to, in order to get to the indicated prefixes/network addresses.

		Returns:
			bool
		"""
		return self._get_attribute('enableNextHop')
	@EnableNextHop.setter
	def EnableNextHop(self, value):
		self._set_attribute('enableNextHop', value)

	@property
	def EnableOrigin(self):
		"""If enabled, the origin of the route will be indicated in the Origin field.

		Returns:
			bool
		"""
		return self._get_attribute('enableOrigin')
	@EnableOrigin.setter
	def EnableOrigin(self, value):
		self._set_attribute('enableOrigin', value)

	@property
	def EnableOriginatorId(self):
		"""Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId.

		Returns:
			bool
		"""
		return self._get_attribute('enableOriginatorId')
	@EnableOriginatorId.setter
	def EnableOriginatorId(self, value):
		self._set_attribute('enableOriginatorId', value)

	@property
	def EnableProperSafi(self):
		"""(Not available for MPLS Route Ranges.) If enabled, the Multiprotocol BGP extensions are included with the SAFI set to 2 to indicate Network Layer Reachability Information for Multicast forwarding.

		Returns:
			bool
		"""
		return self._get_attribute('enableProperSafi')
	@EnableProperSafi.setter
	def EnableProperSafi(self, value):
		self._set_attribute('enableProperSafi', value)

	@property
	def EnableTraditionalNlriUpdate(self):
		"""If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)

		Returns:
			bool
		"""
		return self._get_attribute('enableTraditionalNlriUpdate')
	@EnableTraditionalNlriUpdate.setter
	def EnableTraditionalNlriUpdate(self, value):
		self._set_attribute('enableTraditionalNlriUpdate', value)

	@property
	def Enabled(self):
		"""If true, the route range is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EndOfRib(self):
		"""If true, enables end of rib

		Returns:
			bool
		"""
		return self._get_attribute('endOfRib')
	@EndOfRib.setter
	def EndOfRib(self, value):
		self._set_attribute('endOfRib', value)

	@property
	def FromPacking(self):
		"""The minimum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking.

		Returns:
			number
		"""
		return self._get_attribute('fromPacking')
	@FromPacking.setter
	def FromPacking(self, value):
		self._set_attribute('fromPacking', value)

	@property
	def FromPrefix(self):
		"""The first prefix length to generate based on the networkAddress and numRoutes.

		Returns:
			number
		"""
		return self._get_attribute('fromPrefix')
	@FromPrefix.setter
	def FromPrefix(self, value):
		self._set_attribute('fromPrefix', value)

	@property
	def IpType(self):
		"""The version of the Internet Protocol.

		Returns:
			str(ipAny|ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def IterationStep(self):
		"""The step value to use for incrementing the network mask.

		Returns:
			number
		"""
		return self._get_attribute('iterationStep')
	@IterationStep.setter
	def IterationStep(self, value):
		self._set_attribute('iterationStep', value)

	@property
	def LocalPref(self):
		"""Inserts a local pref attribute with the indicated value.

		Returns:
			number
		"""
		return self._get_attribute('localPref')
	@LocalPref.setter
	def LocalPref(self, value):
		self._set_attribute('localPref', value)

	@property
	def Med(self):
		"""A multi-exit discriminator (MED) attribute.

		Returns:
			number
		"""
		return self._get_attribute('med')
	@Med.setter
	def Med(self, value):
		self._set_attribute('med', value)

	@property
	def NetworkAddress(self):
		"""The network address used for the generated prefixes, in either IPv4 or IPv6 format.

		Returns:
			str
		"""
		return self._get_attribute('networkAddress')
	@NetworkAddress.setter
	def NetworkAddress(self, value):
		self._set_attribute('networkAddress', value)

	@property
	def NextHopIpAddress(self):
		"""The network (Layer 3) address of the router that is the next hop on the path to the destination.

		Returns:
			str
		"""
		return self._get_attribute('nextHopIpAddress')
	@NextHopIpAddress.setter
	def NextHopIpAddress(self, value):
		self._set_attribute('nextHopIpAddress', value)

	@property
	def NextHopIpType(self):
		"""The type of IP address in nextHopIpAddress.

		Returns:
			str(ipAny|ipv4|ipv6)
		"""
		return self._get_attribute('nextHopIpType')
	@NextHopIpType.setter
	def NextHopIpType(self, value):
		self._set_attribute('nextHopIpType', value)

	@property
	def NextHopMode(self):
		"""Generates the NEXT HOP attribute.

		Returns:
			str(fixed|nextHopIncrement|incrementPerPrefix)
		"""
		return self._get_attribute('nextHopMode')
	@NextHopMode.setter
	def NextHopMode(self, value):
		self._set_attribute('nextHopMode', value)

	@property
	def NextHopSetMode(self):
		"""Indicates now to set the next hop IP address.

		Returns:
			str(setManually|sameAsLocalIp)
		"""
		return self._get_attribute('nextHopSetMode')
	@NextHopSetMode.setter
	def NextHopSetMode(self, value):
		self._set_attribute('nextHopSetMode', value)

	@property
	def NumRoutes(self):
		"""The number of prefixes (routes) to generate for this routeItem. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('numRoutes')
	@NumRoutes.setter
	def NumRoutes(self, value):
		self._set_attribute('numRoutes', value)

	@property
	def OriginProtocol(self):
		"""An indication of where the route entry originated.

		Returns:
			str(igp|egp|incomplete)
		"""
		return self._get_attribute('originProtocol')
	@OriginProtocol.setter
	def OriginProtocol(self, value):
		self._set_attribute('originProtocol', value)

	@property
	def OriginatorId(self):
		"""The ID for the router that originated the route.

		Returns:
			str
		"""
		return self._get_attribute('originatorId')
	@OriginatorId.setter
	def OriginatorId(self, value):
		self._set_attribute('originatorId', value)

	@property
	def ThruPacking(self):
		"""The maximum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('thruPacking')
	@ThruPacking.setter
	def ThruPacking(self, value):
		self._set_attribute('thruPacking', value)

	@property
	def ThruPrefix(self):
		"""The last prefix length to generate based on the networkAddress and numRanges. (default = 24)

		Returns:
			number
		"""
		return self._get_attribute('thruPrefix')
	@ThruPrefix.setter
	def ThruPrefix(self, value):
		self._set_attribute('thruPrefix', value)

	def add(self, AdvertiseNextHopAsV4=None, AggregatorAsNum=None, AggregatorIpAddress=None, AsPathSetMode=None, EnableAggregator=None, EnableAggregatorIdIncrementMode=None, EnableAsPath=None, EnableAtomicAttribute=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableIncludeLoopback=None, EnableIncludeMulticast=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableProperSafi=None, EnableTraditionalNlriUpdate=None, Enabled=None, EndOfRib=None, FromPacking=None, FromPrefix=None, IpType=None, IterationStep=None, LocalPref=None, Med=None, NetworkAddress=None, NextHopIpAddress=None, NextHopIpType=None, NextHopMode=None, NextHopSetMode=None, NumRoutes=None, OriginProtocol=None, OriginatorId=None, ThruPacking=None, ThruPrefix=None):
		"""Adds a new routeRange node on the server and retrieves it in this instance.

		Args:
			AdvertiseNextHopAsV4 (bool): NOT DEFINED
			AggregatorAsNum (number): Sets the AS associated with the aggregator router ID.
			AggregatorIpAddress (str): The IP address for the aggregator.
			AsPathSetMode (str(noInclude|includeAsSeq|includeAsSet|includeAsSeqConf|includeAsSetConf|prependAs)): The mode to set the AsPath.
			EnableAggregator (bool): If enabled, generates an aggregator attribute that indicates the router ID that aggregated two or more routes into one.
			EnableAggregatorIdIncrementMode (bool): The mode for the router ID of the router that aggregated two or more routes into one. Choose one of the following options: (1) Fixed-the same Aggregator ID will be used each time. (2) Increment-the Aggregator ID will increment by 1.
			EnableAsPath (bool): Indicates that AS-PATH attributes are to be generated.
			EnableAtomicAttribute (bool): Sets the attribute bit that indicates the router has aggregated two or more prefixes together into one.
			EnableCluster (bool): Generates a list of BGP clusters that a particular route has passed through.
			EnableCommunity (bool): Indicates that a community attribute should be added to the BGP entry.
			EnableGenerateUniqueRoutes (bool): Enables the generate unique routes option. Without this option enabled, every neighbor in the range will generate exactly the same set of routes, starting from the first route.
			EnableIncludeLoopback (bool): Includes loopback addresses (for example, 127.0.0.0 for IPv4) in the list of VPN route ranges.
			EnableIncludeMulticast (bool): Includes multicast addresses (for example, 224.0.0.0 for IPv4) in the list of VPN route ranges.
			EnableLocalPref (bool): inserts a LOCAL PREF attribute with the indicated value. (INTERNAL BGP only)
			EnableMed (bool): Inserts a multi-exit discriminator (MED) attribute with the indicated value.
			EnableNextHop (bool): Enables Next Hop. Inserts a Next Hop attribute that indicates the next router to send packets to, in order to get to the indicated prefixes/network addresses.
			EnableOrigin (bool): If enabled, the origin of the route will be indicated in the Origin field.
			EnableOriginatorId (bool): Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId.
			EnableProperSafi (bool): (Not available for MPLS Route Ranges.) If enabled, the Multiprotocol BGP extensions are included with the SAFI set to 2 to indicate Network Layer Reachability Information for Multicast forwarding.
			EnableTraditionalNlriUpdate (bool): If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)
			Enabled (bool): If true, the route range is enabled.
			EndOfRib (bool): If true, enables end of rib
			FromPacking (number): The minimum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking.
			FromPrefix (number): The first prefix length to generate based on the networkAddress and numRoutes.
			IpType (str(ipAny|ipv4|ipv6)): The version of the Internet Protocol.
			IterationStep (number): The step value to use for incrementing the network mask.
			LocalPref (number): Inserts a local pref attribute with the indicated value.
			Med (number): A multi-exit discriminator (MED) attribute.
			NetworkAddress (str): The network address used for the generated prefixes, in either IPv4 or IPv6 format.
			NextHopIpAddress (str): The network (Layer 3) address of the router that is the next hop on the path to the destination.
			NextHopIpType (str(ipAny|ipv4|ipv6)): The type of IP address in nextHopIpAddress.
			NextHopMode (str(fixed|nextHopIncrement|incrementPerPrefix)): Generates the NEXT HOP attribute.
			NextHopSetMode (str(setManually|sameAsLocalIp)): Indicates now to set the next hop IP address.
			NumRoutes (number): The number of prefixes (routes) to generate for this routeItem. (default = 1)
			OriginProtocol (str(igp|egp|incomplete)): An indication of where the route entry originated.
			OriginatorId (str): The ID for the router that originated the route.
			ThruPacking (number): The maximum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. (default = 0)
			ThruPrefix (number): The last prefix length to generate based on the networkAddress and numRanges. (default = 24)

		Returns:
			self: This instance with all currently retrieved routeRange data using find and the newly added routeRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the routeRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertiseNextHopAsV4=None, AggregatorAsNum=None, AggregatorIpAddress=None, AsPathSetMode=None, EnableAggregator=None, EnableAggregatorIdIncrementMode=None, EnableAsPath=None, EnableAtomicAttribute=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableIncludeLoopback=None, EnableIncludeMulticast=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableProperSafi=None, EnableTraditionalNlriUpdate=None, Enabled=None, EndOfRib=None, FromPacking=None, FromPrefix=None, IpType=None, IterationStep=None, LocalPref=None, Med=None, NetworkAddress=None, NextHopIpAddress=None, NextHopIpType=None, NextHopMode=None, NextHopSetMode=None, NumRoutes=None, OriginProtocol=None, OriginatorId=None, ThruPacking=None, ThruPrefix=None):
		"""Finds and retrieves routeRange data from the server.

		All named parameters support regex and can be used to selectively retrieve routeRange data from the server.
		By default the find method takes no parameters and will retrieve all routeRange data from the server.

		Args:
			AdvertiseNextHopAsV4 (bool): NOT DEFINED
			AggregatorAsNum (number): Sets the AS associated with the aggregator router ID.
			AggregatorIpAddress (str): The IP address for the aggregator.
			AsPathSetMode (str(noInclude|includeAsSeq|includeAsSet|includeAsSeqConf|includeAsSetConf|prependAs)): The mode to set the AsPath.
			EnableAggregator (bool): If enabled, generates an aggregator attribute that indicates the router ID that aggregated two or more routes into one.
			EnableAggregatorIdIncrementMode (bool): The mode for the router ID of the router that aggregated two or more routes into one. Choose one of the following options: (1) Fixed-the same Aggregator ID will be used each time. (2) Increment-the Aggregator ID will increment by 1.
			EnableAsPath (bool): Indicates that AS-PATH attributes are to be generated.
			EnableAtomicAttribute (bool): Sets the attribute bit that indicates the router has aggregated two or more prefixes together into one.
			EnableCluster (bool): Generates a list of BGP clusters that a particular route has passed through.
			EnableCommunity (bool): Indicates that a community attribute should be added to the BGP entry.
			EnableGenerateUniqueRoutes (bool): Enables the generate unique routes option. Without this option enabled, every neighbor in the range will generate exactly the same set of routes, starting from the first route.
			EnableIncludeLoopback (bool): Includes loopback addresses (for example, 127.0.0.0 for IPv4) in the list of VPN route ranges.
			EnableIncludeMulticast (bool): Includes multicast addresses (for example, 224.0.0.0 for IPv4) in the list of VPN route ranges.
			EnableLocalPref (bool): inserts a LOCAL PREF attribute with the indicated value. (INTERNAL BGP only)
			EnableMed (bool): Inserts a multi-exit discriminator (MED) attribute with the indicated value.
			EnableNextHop (bool): Enables Next Hop. Inserts a Next Hop attribute that indicates the next router to send packets to, in order to get to the indicated prefixes/network addresses.
			EnableOrigin (bool): If enabled, the origin of the route will be indicated in the Origin field.
			EnableOriginatorId (bool): Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId.
			EnableProperSafi (bool): (Not available for MPLS Route Ranges.) If enabled, the Multiprotocol BGP extensions are included with the SAFI set to 2 to indicate Network Layer Reachability Information for Multicast forwarding.
			EnableTraditionalNlriUpdate (bool): If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)
			Enabled (bool): If true, the route range is enabled.
			EndOfRib (bool): If true, enables end of rib
			FromPacking (number): The minimum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking.
			FromPrefix (number): The first prefix length to generate based on the networkAddress and numRoutes.
			IpType (str(ipAny|ipv4|ipv6)): The version of the Internet Protocol.
			IterationStep (number): The step value to use for incrementing the network mask.
			LocalPref (number): Inserts a local pref attribute with the indicated value.
			Med (number): A multi-exit discriminator (MED) attribute.
			NetworkAddress (str): The network address used for the generated prefixes, in either IPv4 or IPv6 format.
			NextHopIpAddress (str): The network (Layer 3) address of the router that is the next hop on the path to the destination.
			NextHopIpType (str(ipAny|ipv4|ipv6)): The type of IP address in nextHopIpAddress.
			NextHopMode (str(fixed|nextHopIncrement|incrementPerPrefix)): Generates the NEXT HOP attribute.
			NextHopSetMode (str(setManually|sameAsLocalIp)): Indicates now to set the next hop IP address.
			NumRoutes (number): The number of prefixes (routes) to generate for this routeItem. (default = 1)
			OriginProtocol (str(igp|egp|incomplete)): An indication of where the route entry originated.
			OriginatorId (str): The ID for the router that originated the route.
			ThruPacking (number): The maximum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. (default = 0)
			ThruPrefix (number): The last prefix length to generate based on the networkAddress and numRanges. (default = 24)

		Returns:
			self: This instance with matching routeRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of routeRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the routeRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ReAdvertiseRoutes(self):
		"""Executes the reAdvertiseRoutes operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=routeRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ReAdvertiseRoutes', payload=locals(), response_object=None)
