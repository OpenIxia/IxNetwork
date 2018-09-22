from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VpnRouteRange(Base):
	"""The VpnRouteRange class encapsulates a user managed vpnRouteRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VpnRouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'vpnRouteRange'

	def __init__(self, parent):
		super(VpnRouteRange, self).__init__(parent)

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
	def LabelSpace(self):
		"""An instance of the LabelSpace class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.labelspace.LabelSpace)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.labelspace import LabelSpace
		return LabelSpace(self)._select()

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
		"""The AS associated with the aggregator router ID in the AGGREGATOR attribute. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAsNum')
	@AggregatorAsNum.setter
	def AggregatorAsNum(self, value):
		self._set_attribute('aggregatorAsNum', value)

	@property
	def AggregatorIpAddress(self):
		"""The IP address of the router that aggregated two or more routes in the AGGREGATOR attribute. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('aggregatorIpAddress')
	@AggregatorIpAddress.setter
	def AggregatorIpAddress(self, value):
		self._set_attribute('aggregatorIpAddress', value)

	@property
	def DistinguisherAsNumber(self):
		"""If distinguisherType is set to bgp4DistinguisherTypeAS, this is the 2-byte AS number in the administrator sub-field of the value field of the VPN Route Distinguisher. It is the global part of the route distinguisher. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumber')
	@DistinguisherAsNumber.setter
	def DistinguisherAsNumber(self, value):
		self._set_attribute('distinguisherAsNumber', value)

	@property
	def DistinguisherAsNumberStep(self):
		"""The increment step for for the distinguisher AS number.

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumberStep')
	@DistinguisherAsNumberStep.setter
	def DistinguisherAsNumberStep(self, value):
		self._set_attribute('distinguisherAsNumberStep', value)

	@property
	def DistinguisherAsNumberStepAcrossVrfs(self):
		"""The increment step for per VRF distinguisher AS number within the VRF Range.

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumberStepAcrossVrfs')
	@DistinguisherAsNumberStepAcrossVrfs.setter
	def DistinguisherAsNumberStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherAsNumberStepAcrossVrfs', value)

	@property
	def DistinguisherAssignedNumber(self):
		"""The assigned number of the VPN route distinguisher. It is a number from a numbering space which is maintained by the enterprise administers for a given IP address or ASN space. It is the local part of the route distinguisher. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumber')
	@DistinguisherAssignedNumber.setter
	def DistinguisherAssignedNumber(self, value):
		self._set_attribute('distinguisherAssignedNumber', value)

	@property
	def DistinguisherAssignedNumberStep(self):
		"""The increment step for for the distinguisher assigned number.

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumberStep')
	@DistinguisherAssignedNumberStep.setter
	def DistinguisherAssignedNumberStep(self, value):
		self._set_attribute('distinguisherAssignedNumberStep', value)

	@property
	def DistinguisherAssignedNumberStepAcrossVrfs(self):
		"""The increment step for per VRF distinguisher assigned number within the VRF Range.

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumberStepAcrossVrfs')
	@DistinguisherAssignedNumberStepAcrossVrfs.setter
	def DistinguisherAssignedNumberStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherAssignedNumberStepAcrossVrfs', value)

	@property
	def DistinguisherCount(self):
		"""The number of times that the increment step will be used. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('distinguisherCount')
	@DistinguisherCount.setter
	def DistinguisherCount(self, value):
		self._set_attribute('distinguisherCount', value)

	@property
	def DistinguisherCountPerVrf(self):
		"""The number of times that the increment step is used per VRF.

		Returns:
			number
		"""
		return self._get_attribute('distinguisherCountPerVrf')
	@DistinguisherCountPerVrf.setter
	def DistinguisherCountPerVrf(self, value):
		self._set_attribute('distinguisherCountPerVrf', value)

	@property
	def DistinguisherIpAddress(self):
		"""If distinguisherType is set to bgp4DistinguisherTypeIP, this is the 4-byte IP address in the administrator subfield of the value field of the VPN Route Distinguisher. It is the global part of the route distinguisher. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddress')
	@DistinguisherIpAddress.setter
	def DistinguisherIpAddress(self, value):
		self._set_attribute('distinguisherIpAddress', value)

	@property
	def DistinguisherIpAddressStep(self):
		"""The increment step for for the distinguisher IP address.

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddressStep')
	@DistinguisherIpAddressStep.setter
	def DistinguisherIpAddressStep(self, value):
		self._set_attribute('distinguisherIpAddressStep', value)

	@property
	def DistinguisherIpAddressStepAcrossVrfs(self):
		"""The increment step for per VRF distinguisher IP address within the VRF Range.

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddressStepAcrossVrfs')
	@DistinguisherIpAddressStepAcrossVrfs.setter
	def DistinguisherIpAddressStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherIpAddressStepAcrossVrfs', value)

	@property
	def DistinguisherMode(self):
		"""Specifies which part of the route distinguisher you want to increment.

		Returns:
			str(global|local)
		"""
		return self._get_attribute('distinguisherMode')
	@DistinguisherMode.setter
	def DistinguisherMode(self, value):
		self._set_attribute('distinguisherMode', value)

	@property
	def DistinguisherStep(self):
		"""The size of the increment step to be used with the part of the route distinguisher which will be incremented. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('distinguisherStep')
	@DistinguisherStep.setter
	def DistinguisherStep(self, value):
		self._set_attribute('distinguisherStep', value)

	@property
	def DistinguisherType(self):
		"""Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.

		Returns:
			str(as|ip|asNumber2)
		"""
		return self._get_attribute('distinguisherType')
	@DistinguisherType.setter
	def DistinguisherType(self, value):
		self._set_attribute('distinguisherType', value)

	@property
	def EnableAggregator(self):
		"""Generates an AGGREGATOR attribute using the aggregatorIpAddress, aggregatorASNum, and aggregatorIDMode. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregator')
	@EnableAggregator.setter
	def EnableAggregator(self, value):
		self._set_attribute('enableAggregator', value)

	@property
	def EnableAggregatorIdIncrementMode(self):
		"""If true, increments the Aggregator ID by interationStep.

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregatorIdIncrementMode')
	@EnableAggregatorIdIncrementMode.setter
	def EnableAggregatorIdIncrementMode(self, value):
		self._set_attribute('enableAggregatorIdIncrementMode', value)

	@property
	def EnableAsPath(self):
		"""Enables the generation of AS Path related items.

		Returns:
			bool
		"""
		return self._get_attribute('enableAsPath')
	@EnableAsPath.setter
	def EnableAsPath(self, value):
		self._set_attribute('enableAsPath', value)

	@property
	def EnableAtomicAttribute(self):
		"""Sets the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAttribute')
	@EnableAtomicAttribute.setter
	def EnableAtomicAttribute(self, value):
		self._set_attribute('enableAtomicAttribute', value)

	@property
	def EnableCluster(self):
		"""Enables the generation of the CLUSTER attribute list based on information in clusterList. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableCluster')
	@EnableCluster.setter
	def EnableCluster(self, value):
		self._set_attribute('enableCluster', value)

	@property
	def EnableCommunity(self):
		"""Enables the generation of a COMMUNITY attribute list. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableCommunity')
	@EnableCommunity.setter
	def EnableCommunity(self, value):
		self._set_attribute('enableCommunity', value)

	@property
	def EnableGenerateUniqueRoutes(self):
		"""When set to 1, each router generates a different IP address range. When not enabled, each router will advertise the route range as is.

		Returns:
			bool
		"""
		return self._get_attribute('enableGenerateUniqueRoutes')
	@EnableGenerateUniqueRoutes.setter
	def EnableGenerateUniqueRoutes(self, value):
		self._set_attribute('enableGenerateUniqueRoutes', value)

	@property
	def EnableIncludeLoopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeLoopback')
	@EnableIncludeLoopback.setter
	def EnableIncludeLoopback(self, value):
		self._set_attribute('enableIncludeLoopback', value)

	@property
	def EnableIncludeMulticast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeMulticast')
	@EnableIncludeMulticast.setter
	def EnableIncludeMulticast(self, value):
		self._set_attribute('enableIncludeMulticast', value)

	@property
	def EnableLocalPref(self):
		"""Enables the generation of a LOCAL PREF attribute based on the information in localPref. This value should be set to true only for EBGP. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableLocalPref')
	@EnableLocalPref.setter
	def EnableLocalPref(self, value):
		self._set_attribute('enableLocalPref', value)

	@property
	def EnableMed(self):
		"""Enables the generation of a MULTI EXIT DISCRIMINATOR attribute. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableMed')
	@EnableMed.setter
	def EnableMed(self, value):
		self._set_attribute('enableMed', value)

	@property
	def EnableNextHop(self):
		"""Enables the generation of a NEXT HOP attribute. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('enableNextHop')
	@EnableNextHop.setter
	def EnableNextHop(self, value):
		self._set_attribute('enableNextHop', value)

	@property
	def EnableOrigin(self):
		"""Enables the generation of an ORIGIN attribute. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('enableOrigin')
	@EnableOrigin.setter
	def EnableOrigin(self, value):
		self._set_attribute('enableOrigin', value)

	@property
	def EnableOriginatorId(self):
		"""Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableOriginatorId')
	@EnableOriginatorId.setter
	def EnableOriginatorId(self, value):
		self._set_attribute('enableOriginatorId', value)

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
		"""Enables the VPN route range.

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
		"""The minimum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('fromPacking')
	@FromPacking.setter
	def FromPacking(self, value):
		self._set_attribute('fromPacking', value)

	@property
	def FromPrefix(self):
		"""The first prefix length to generate based on the networkAddress and numRanges. (default = 24)

		Returns:
			number
		"""
		return self._get_attribute('fromPrefix')
	@FromPrefix.setter
	def FromPrefix(self, value):
		self._set_attribute('fromPrefix', value)

	@property
	def IncludeSourceAsExtendedCommunityPresent(self):
		"""If for a given MVPN BGP is used for exchanging C-multicast routes, or if segmented

		Returns:
			bool
		"""
		return self._get_attribute('includeSourceAsExtendedCommunityPresent')
	@IncludeSourceAsExtendedCommunityPresent.setter
	def IncludeSourceAsExtendedCommunityPresent(self, value):
		self._set_attribute('includeSourceAsExtendedCommunityPresent', value)

	@property
	def IncludeVrfRouteImportExtendedCommunityPresent(self):
		"""Defines the route target extended community.

		Returns:
			bool
		"""
		return self._get_attribute('includeVrfRouteImportExtendedCommunityPresent')
	@IncludeVrfRouteImportExtendedCommunityPresent.setter
	def IncludeVrfRouteImportExtendedCommunityPresent(self, value):
		self._set_attribute('includeVrfRouteImportExtendedCommunityPresent', value)

	@property
	def IpType(self):
		"""The type of IP address in nextworkAddress.

		Returns:
			str(ipAny|ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def IterationStep(self):
		"""During prefix generation, the increment between prefixes. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('iterationStep')
	@IterationStep.setter
	def IterationStep(self, value):
		self._set_attribute('iterationStep', value)

	@property
	def LocalPref(self):
		"""The local preference value for the routes with the LOCAL PREF attribute. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('localPref')
	@LocalPref.setter
	def LocalPref(self, value):
		self._set_attribute('localPref', value)

	@property
	def Med(self):
		"""The multi-exit discriminator value in the MULTI EXIT DISCRIMINATOR attribute. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('med')
	@Med.setter
	def Med(self, value):
		self._set_attribute('med', value)

	@property
	def NetworkAddress(self):
		"""The network address used for the generated prefixes. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('networkAddress')
	@NetworkAddress.setter
	def NetworkAddress(self, value):
		self._set_attribute('networkAddress', value)

	@property
	def NextHopIpAddress(self):
		"""The IP address, in either IPv4 or IPv6 format of the next hop associated with the NEXT HOP attribute. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('nextHopIpAddress')
	@NextHopIpAddress.setter
	def NextHopIpAddress(self, value):
		self._set_attribute('nextHopIpAddress', value)

	@property
	def NextHopMode(self):
		"""Indicates that the nextHopIpAddress may be incremented for each neighbor session generated for the range of neighbor addresses.

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
		"""The router that originated a particular route; associated with the ORIGINATOR-ID attribute. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('originatorId')
	@OriginatorId.setter
	def OriginatorId(self, value):
		self._set_attribute('originatorId', value)

	@property
	def RouteStepAcrossVRFs(self):
		"""The route increment value across VRFs.

		Returns:
			str
		"""
		return self._get_attribute('routeStepAcrossVRFs')
	@RouteStepAcrossVRFs.setter
	def RouteStepAcrossVRFs(self, value):
		self._set_attribute('routeStepAcrossVRFs', value)

	@property
	def ThruPacking(self):
		"""The maximum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. See the discussion under fromPacking above. (default = 0)

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

	def add(self, AdvertiseNextHopAsV4=None, AggregatorAsNum=None, AggregatorIpAddress=None, DistinguisherAsNumber=None, DistinguisherAsNumberStep=None, DistinguisherAsNumberStepAcrossVrfs=None, DistinguisherAssignedNumber=None, DistinguisherAssignedNumberStep=None, DistinguisherAssignedNumberStepAcrossVrfs=None, DistinguisherCount=None, DistinguisherCountPerVrf=None, DistinguisherIpAddress=None, DistinguisherIpAddressStep=None, DistinguisherIpAddressStepAcrossVrfs=None, DistinguisherMode=None, DistinguisherStep=None, DistinguisherType=None, EnableAggregator=None, EnableAggregatorIdIncrementMode=None, EnableAsPath=None, EnableAtomicAttribute=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableIncludeLoopback=None, EnableIncludeMulticast=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableTraditionalNlriUpdate=None, Enabled=None, EndOfRib=None, FromPacking=None, FromPrefix=None, IncludeSourceAsExtendedCommunityPresent=None, IncludeVrfRouteImportExtendedCommunityPresent=None, IpType=None, IterationStep=None, LocalPref=None, Med=None, NetworkAddress=None, NextHopIpAddress=None, NextHopMode=None, NextHopSetMode=None, NumRoutes=None, OriginProtocol=None, OriginatorId=None, RouteStepAcrossVRFs=None, ThruPacking=None, ThruPrefix=None):
		"""Adds a new vpnRouteRange node on the server and retrieves it in this instance.

		Args:
			AdvertiseNextHopAsV4 (bool): NOT DEFINED
			AggregatorAsNum (number): The AS associated with the aggregator router ID in the AGGREGATOR attribute. (default = 0)
			AggregatorIpAddress (str): The IP address of the router that aggregated two or more routes in the AGGREGATOR attribute. (default = 0.0.0.0)
			DistinguisherAsNumber (number): If distinguisherType is set to bgp4DistinguisherTypeAS, this is the 2-byte AS number in the administrator sub-field of the value field of the VPN Route Distinguisher. It is the global part of the route distinguisher. (default = 0)
			DistinguisherAsNumberStep (number): The increment step for for the distinguisher AS number.
			DistinguisherAsNumberStepAcrossVrfs (number): The increment step for per VRF distinguisher AS number within the VRF Range.
			DistinguisherAssignedNumber (number): The assigned number of the VPN route distinguisher. It is a number from a numbering space which is maintained by the enterprise administers for a given IP address or ASN space. It is the local part of the route distinguisher. (default = 0)
			DistinguisherAssignedNumberStep (number): The increment step for for the distinguisher assigned number.
			DistinguisherAssignedNumberStepAcrossVrfs (number): The increment step for per VRF distinguisher assigned number within the VRF Range.
			DistinguisherCount (number): The number of times that the increment step will be used. (default = 1)
			DistinguisherCountPerVrf (number): The number of times that the increment step is used per VRF.
			DistinguisherIpAddress (str): If distinguisherType is set to bgp4DistinguisherTypeIP, this is the 4-byte IP address in the administrator subfield of the value field of the VPN Route Distinguisher. It is the global part of the route distinguisher. (default = 0.0.0.0)
			DistinguisherIpAddressStep (str): The increment step for for the distinguisher IP address.
			DistinguisherIpAddressStepAcrossVrfs (str): The increment step for per VRF distinguisher IP address within the VRF Range.
			DistinguisherMode (str(global|local)): Specifies which part of the route distinguisher you want to increment.
			DistinguisherStep (number): The size of the increment step to be used with the part of the route distinguisher which will be incremented. (default = 1)
			DistinguisherType (str(as|ip|asNumber2)): Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.
			EnableAggregator (bool): Generates an AGGREGATOR attribute using the aggregatorIpAddress, aggregatorASNum, and aggregatorIDMode. (default = false)
			EnableAggregatorIdIncrementMode (bool): If true, increments the Aggregator ID by interationStep.
			EnableAsPath (bool): Enables the generation of AS Path related items.
			EnableAtomicAttribute (bool): Sets the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)
			EnableCluster (bool): Enables the generation of the CLUSTER attribute list based on information in clusterList. (default = false)
			EnableCommunity (bool): Enables the generation of a COMMUNITY attribute list. (default = false)
			EnableGenerateUniqueRoutes (bool): When set to 1, each router generates a different IP address range. When not enabled, each router will advertise the route range as is.
			EnableIncludeLoopback (bool): 
			EnableIncludeMulticast (bool): 
			EnableLocalPref (bool): Enables the generation of a LOCAL PREF attribute based on the information in localPref. This value should be set to true only for EBGP. (default = false)
			EnableMed (bool): Enables the generation of a MULTI EXIT DISCRIMINATOR attribute. (default = false)
			EnableNextHop (bool): Enables the generation of a NEXT HOP attribute. (default = true)
			EnableOrigin (bool): Enables the generation of an ORIGIN attribute. (default = true)
			EnableOriginatorId (bool): Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)
			EnableTraditionalNlriUpdate (bool): If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)
			Enabled (bool): Enables the VPN route range.
			EndOfRib (bool): If true, enables end of rib
			FromPacking (number): The minimum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. (default = 0)
			FromPrefix (number): The first prefix length to generate based on the networkAddress and numRanges. (default = 24)
			IncludeSourceAsExtendedCommunityPresent (bool): If for a given MVPN BGP is used for exchanging C-multicast routes, or if segmented
			IncludeVrfRouteImportExtendedCommunityPresent (bool): Defines the route target extended community.
			IpType (str(ipAny|ipv4|ipv6)): The type of IP address in nextworkAddress.
			IterationStep (number): During prefix generation, the increment between prefixes. (default = 1)
			LocalPref (number): The local preference value for the routes with the LOCAL PREF attribute. (default = 0)
			Med (number): The multi-exit discriminator value in the MULTI EXIT DISCRIMINATOR attribute. (default = 0)
			NetworkAddress (str): The network address used for the generated prefixes. (default = 0.0.0.0)
			NextHopIpAddress (str): The IP address, in either IPv4 or IPv6 format of the next hop associated with the NEXT HOP attribute. (default = 0.0.0.0)
			NextHopMode (str(fixed|nextHopIncrement|incrementPerPrefix)): Indicates that the nextHopIpAddress may be incremented for each neighbor session generated for the range of neighbor addresses.
			NextHopSetMode (str(setManually|sameAsLocalIp)): Indicates now to set the next hop IP address.
			NumRoutes (number): The number of prefixes (routes) to generate for this routeItem. (default = 1)
			OriginProtocol (str(igp|egp|incomplete)): An indication of where the route entry originated.
			OriginatorId (str): The router that originated a particular route; associated with the ORIGINATOR-ID attribute. (default = 0.0.0.0)
			RouteStepAcrossVRFs (str): The route increment value across VRFs.
			ThruPacking (number): The maximum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. See the discussion under fromPacking above. (default = 0)
			ThruPrefix (number): The last prefix length to generate based on the networkAddress and numRanges. (default = 24)

		Returns:
			self: This instance with all currently retrieved vpnRouteRange data using find and the newly added vpnRouteRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the vpnRouteRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertiseNextHopAsV4=None, AggregatorAsNum=None, AggregatorIpAddress=None, DistinguisherAsNumber=None, DistinguisherAsNumberStep=None, DistinguisherAsNumberStepAcrossVrfs=None, DistinguisherAssignedNumber=None, DistinguisherAssignedNumberStep=None, DistinguisherAssignedNumberStepAcrossVrfs=None, DistinguisherCount=None, DistinguisherCountPerVrf=None, DistinguisherIpAddress=None, DistinguisherIpAddressStep=None, DistinguisherIpAddressStepAcrossVrfs=None, DistinguisherMode=None, DistinguisherStep=None, DistinguisherType=None, EnableAggregator=None, EnableAggregatorIdIncrementMode=None, EnableAsPath=None, EnableAtomicAttribute=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableIncludeLoopback=None, EnableIncludeMulticast=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableTraditionalNlriUpdate=None, Enabled=None, EndOfRib=None, FromPacking=None, FromPrefix=None, IncludeSourceAsExtendedCommunityPresent=None, IncludeVrfRouteImportExtendedCommunityPresent=None, IpType=None, IterationStep=None, LocalPref=None, Med=None, NetworkAddress=None, NextHopIpAddress=None, NextHopMode=None, NextHopSetMode=None, NumRoutes=None, OriginProtocol=None, OriginatorId=None, RouteStepAcrossVRFs=None, ThruPacking=None, ThruPrefix=None):
		"""Finds and retrieves vpnRouteRange data from the server.

		All named parameters support regex and can be used to selectively retrieve vpnRouteRange data from the server.
		By default the find method takes no parameters and will retrieve all vpnRouteRange data from the server.

		Args:
			AdvertiseNextHopAsV4 (bool): NOT DEFINED
			AggregatorAsNum (number): The AS associated with the aggregator router ID in the AGGREGATOR attribute. (default = 0)
			AggregatorIpAddress (str): The IP address of the router that aggregated two or more routes in the AGGREGATOR attribute. (default = 0.0.0.0)
			DistinguisherAsNumber (number): If distinguisherType is set to bgp4DistinguisherTypeAS, this is the 2-byte AS number in the administrator sub-field of the value field of the VPN Route Distinguisher. It is the global part of the route distinguisher. (default = 0)
			DistinguisherAsNumberStep (number): The increment step for for the distinguisher AS number.
			DistinguisherAsNumberStepAcrossVrfs (number): The increment step for per VRF distinguisher AS number within the VRF Range.
			DistinguisherAssignedNumber (number): The assigned number of the VPN route distinguisher. It is a number from a numbering space which is maintained by the enterprise administers for a given IP address or ASN space. It is the local part of the route distinguisher. (default = 0)
			DistinguisherAssignedNumberStep (number): The increment step for for the distinguisher assigned number.
			DistinguisherAssignedNumberStepAcrossVrfs (number): The increment step for per VRF distinguisher assigned number within the VRF Range.
			DistinguisherCount (number): The number of times that the increment step will be used. (default = 1)
			DistinguisherCountPerVrf (number): The number of times that the increment step is used per VRF.
			DistinguisherIpAddress (str): If distinguisherType is set to bgp4DistinguisherTypeIP, this is the 4-byte IP address in the administrator subfield of the value field of the VPN Route Distinguisher. It is the global part of the route distinguisher. (default = 0.0.0.0)
			DistinguisherIpAddressStep (str): The increment step for for the distinguisher IP address.
			DistinguisherIpAddressStepAcrossVrfs (str): The increment step for per VRF distinguisher IP address within the VRF Range.
			DistinguisherMode (str(global|local)): Specifies which part of the route distinguisher you want to increment.
			DistinguisherStep (number): The size of the increment step to be used with the part of the route distinguisher which will be incremented. (default = 1)
			DistinguisherType (str(as|ip|asNumber2)): Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.
			EnableAggregator (bool): Generates an AGGREGATOR attribute using the aggregatorIpAddress, aggregatorASNum, and aggregatorIDMode. (default = false)
			EnableAggregatorIdIncrementMode (bool): If true, increments the Aggregator ID by interationStep.
			EnableAsPath (bool): Enables the generation of AS Path related items.
			EnableAtomicAttribute (bool): Sets the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)
			EnableCluster (bool): Enables the generation of the CLUSTER attribute list based on information in clusterList. (default = false)
			EnableCommunity (bool): Enables the generation of a COMMUNITY attribute list. (default = false)
			EnableGenerateUniqueRoutes (bool): When set to 1, each router generates a different IP address range. When not enabled, each router will advertise the route range as is.
			EnableIncludeLoopback (bool): 
			EnableIncludeMulticast (bool): 
			EnableLocalPref (bool): Enables the generation of a LOCAL PREF attribute based on the information in localPref. This value should be set to true only for EBGP. (default = false)
			EnableMed (bool): Enables the generation of a MULTI EXIT DISCRIMINATOR attribute. (default = false)
			EnableNextHop (bool): Enables the generation of a NEXT HOP attribute. (default = true)
			EnableOrigin (bool): Enables the generation of an ORIGIN attribute. (default = true)
			EnableOriginatorId (bool): Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)
			EnableTraditionalNlriUpdate (bool): If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)
			Enabled (bool): Enables the VPN route range.
			EndOfRib (bool): If true, enables end of rib
			FromPacking (number): The minimum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. (default = 0)
			FromPrefix (number): The first prefix length to generate based on the networkAddress and numRanges. (default = 24)
			IncludeSourceAsExtendedCommunityPresent (bool): If for a given MVPN BGP is used for exchanging C-multicast routes, or if segmented
			IncludeVrfRouteImportExtendedCommunityPresent (bool): Defines the route target extended community.
			IpType (str(ipAny|ipv4|ipv6)): The type of IP address in nextworkAddress.
			IterationStep (number): During prefix generation, the increment between prefixes. (default = 1)
			LocalPref (number): The local preference value for the routes with the LOCAL PREF attribute. (default = 0)
			Med (number): The multi-exit discriminator value in the MULTI EXIT DISCRIMINATOR attribute. (default = 0)
			NetworkAddress (str): The network address used for the generated prefixes. (default = 0.0.0.0)
			NextHopIpAddress (str): The IP address, in either IPv4 or IPv6 format of the next hop associated with the NEXT HOP attribute. (default = 0.0.0.0)
			NextHopMode (str(fixed|nextHopIncrement|incrementPerPrefix)): Indicates that the nextHopIpAddress may be incremented for each neighbor session generated for the range of neighbor addresses.
			NextHopSetMode (str(setManually|sameAsLocalIp)): Indicates now to set the next hop IP address.
			NumRoutes (number): The number of prefixes (routes) to generate for this routeItem. (default = 1)
			OriginProtocol (str(igp|egp|incomplete)): An indication of where the route entry originated.
			OriginatorId (str): The router that originated a particular route; associated with the ORIGINATOR-ID attribute. (default = 0.0.0.0)
			RouteStepAcrossVRFs (str): The route increment value across VRFs.
			ThruPacking (number): The maximum number of routes to pack into an UPDATE message. Random numbers are chosen from the range fromPacking to toPacking. See the discussion under fromPacking above. (default = 0)
			ThruPrefix (number): The last prefix length to generate based on the networkAddress and numRanges. (default = 24)

		Returns:
			self: This instance with matching vpnRouteRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of vpnRouteRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the vpnRouteRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
