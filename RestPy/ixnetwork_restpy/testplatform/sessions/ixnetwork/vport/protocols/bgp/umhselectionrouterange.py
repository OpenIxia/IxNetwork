from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UmhSelectionRouteRange(Base):
	"""The UmhSelectionRouteRange class encapsulates a user managed umhSelectionRouteRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UmhSelectionRouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'umhSelectionRouteRange'

	def __init__(self, parent):
		super(UmhSelectionRouteRange, self).__init__(parent)

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
	def AggregatorAsNumber(self):
		"""AS number associated with Aggregator ID in Aggregator attribute

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAsNumber')
	@AggregatorAsNumber.setter
	def AggregatorAsNumber(self, value):
		self._set_attribute('aggregatorAsNumber', value)

	@property
	def AggregatorIdIncrementMode(self):
		"""Increment mode of aggregator ID

		Returns:
			str(fixed|increment)
		"""
		return self._get_attribute('aggregatorIdIncrementMode')
	@AggregatorIdIncrementMode.setter
	def AggregatorIdIncrementMode(self, value):
		self._set_attribute('aggregatorIdIncrementMode', value)

	@property
	def AggregatorIpAddress(self):
		"""IP address of the aggregator in Aggregator attribute

		Returns:
			str
		"""
		return self._get_attribute('aggregatorIpAddress')
	@AggregatorIpAddress.setter
	def AggregatorIpAddress(self, value):
		self._set_attribute('aggregatorIpAddress', value)

	@property
	def DistinguisherAsNumber(self):
		"""Distinguisher AS number

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumber')
	@DistinguisherAsNumber.setter
	def DistinguisherAsNumber(self, value):
		self._set_attribute('distinguisherAsNumber', value)

	@property
	def DistinguisherAsNumberStep(self):
		"""Increment step of Distinguisher AS number across the routes in route range

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumberStep')
	@DistinguisherAsNumberStep.setter
	def DistinguisherAsNumberStep(self, value):
		self._set_attribute('distinguisherAsNumberStep', value)

	@property
	def DistinguisherAsNumberStepAcrossVrfs(self):
		"""Increment step of Distinguisher AS number across the VRFs in VRF range

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumberStepAcrossVrfs')
	@DistinguisherAsNumberStepAcrossVrfs.setter
	def DistinguisherAsNumberStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherAsNumberStepAcrossVrfs', value)

	@property
	def DistinguisherAssignedNumber(self):
		"""Distinguisher assigned number

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumber')
	@DistinguisherAssignedNumber.setter
	def DistinguisherAssignedNumber(self, value):
		self._set_attribute('distinguisherAssignedNumber', value)

	@property
	def DistinguisherAssignedNumberStep(self):
		"""Increment step of distinguisher assigned number across routes in route range

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumberStep')
	@DistinguisherAssignedNumberStep.setter
	def DistinguisherAssignedNumberStep(self, value):
		self._set_attribute('distinguisherAssignedNumberStep', value)

	@property
	def DistinguisherAssignedNumberStepAcrossVrfs(self):
		"""Increment step of distinguisher assigned number across VRFs in VRF range

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumberStepAcrossVrfs')
	@DistinguisherAssignedNumberStepAcrossVrfs.setter
	def DistinguisherAssignedNumberStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherAssignedNumberStepAcrossVrfs', value)

	@property
	def DistinguisherCount(self):
		"""Number of times increment step will be used ( default = 1 )

		Returns:
			number
		"""
		return self._get_attribute('distinguisherCount')
	@DistinguisherCount.setter
	def DistinguisherCount(self, value):
		self._set_attribute('distinguisherCount', value)

	@property
	def DistinguisherCountPerVrf(self):
		"""Number of times increment step will be used per VRF

		Returns:
			number
		"""
		return self._get_attribute('distinguisherCountPerVrf')
	@DistinguisherCountPerVrf.setter
	def DistinguisherCountPerVrf(self, value):
		self._set_attribute('distinguisherCountPerVrf', value)

	@property
	def DistinguisherIpAddress(self):
		"""Distinguisher IP address

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddress')
	@DistinguisherIpAddress.setter
	def DistinguisherIpAddress(self, value):
		self._set_attribute('distinguisherIpAddress', value)

	@property
	def DistinguisherIpAddressStep(self):
		"""Increment step of distinguisher IP address across routes in route range

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddressStep')
	@DistinguisherIpAddressStep.setter
	def DistinguisherIpAddressStep(self, value):
		self._set_attribute('distinguisherIpAddressStep', value)

	@property
	def DistinguisherIpAddressStepAcrossVrfs(self):
		"""Increment step of distinguisher IP address across VRFs in VRF range

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
	def EnableAtomicAggregator(self):
		"""Sets the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAggregator')
	@EnableAtomicAggregator.setter
	def EnableAtomicAggregator(self, value):
		self._set_attribute('enableAtomicAggregator', value)

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
	def EnableOriginator(self):
		"""Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableOriginator')
	@EnableOriginator.setter
	def EnableOriginator(self, value):
		self._set_attribute('enableOriginator', value)

	@property
	def EnableUseTraditionalNlri(self):
		"""If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)

		Returns:
			bool
		"""
		return self._get_attribute('enableUseTraditionalNlri')
	@EnableUseTraditionalNlri.setter
	def EnableUseTraditionalNlri(self, value):
		self._set_attribute('enableUseTraditionalNlri', value)

	@property
	def Enabled(self):
		"""Enables the UMH route range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstRoute(self):
		"""First route in route range

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

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
	def MaskWidth(self):
		"""Mask width of route range

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def MaskWidthTo(self):
		"""mask width of last route range

		Returns:
			number
		"""
		return self._get_attribute('maskWidthTo')
	@MaskWidthTo.setter
	def MaskWidthTo(self, value):
		self._set_attribute('maskWidthTo', value)

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
			str(nextHopIncrement|fixed|incrementPerPrefix)
		"""
		return self._get_attribute('nextHopMode')
	@NextHopMode.setter
	def NextHopMode(self, value):
		self._set_attribute('nextHopMode', value)

	@property
	def NextHopSetMode(self):
		"""Indicates now to set the next hop IP address.

		Returns:
			str(sameAsLocalIp|setManually)
		"""
		return self._get_attribute('nextHopSetMode')
	@NextHopSetMode.setter
	def NextHopSetMode(self, value):
		self._set_attribute('nextHopSetMode', value)

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
	def PackingFrom(self):
		"""Initial number of route packed in one BGP update

		Returns:
			number
		"""
		return self._get_attribute('packingFrom')
	@PackingFrom.setter
	def PackingFrom(self, value):
		self._set_attribute('packingFrom', value)

	@property
	def PackingTo(self):
		"""Final number of routes packed in one BGP update

		Returns:
			number
		"""
		return self._get_attribute('packingTo')
	@PackingTo.setter
	def PackingTo(self, value):
		self._set_attribute('packingTo', value)

	@property
	def RouteCountPerVrfs(self):
		"""Number of route per VRF

		Returns:
			number
		"""
		return self._get_attribute('routeCountPerVrfs')
	@RouteCountPerVrfs.setter
	def RouteCountPerVrfs(self, value):
		self._set_attribute('routeCountPerVrfs', value)

	@property
	def RouteStepAcrossVrfs(self):
		"""The route increment value across VRFs.

		Returns:
			str
		"""
		return self._get_attribute('routeStepAcrossVrfs')
	@RouteStepAcrossVrfs.setter
	def RouteStepAcrossVrfs(self, value):
		self._set_attribute('routeStepAcrossVrfs', value)

	@property
	def Step(self):
		"""step

		Returns:
			number
		"""
		return self._get_attribute('step')
	@Step.setter
	def Step(self, value):
		self._set_attribute('step', value)

	def add(self, AggregatorAsNumber=None, AggregatorIdIncrementMode=None, AggregatorIpAddress=None, DistinguisherAsNumber=None, DistinguisherAsNumberStep=None, DistinguisherAsNumberStepAcrossVrfs=None, DistinguisherAssignedNumber=None, DistinguisherAssignedNumberStep=None, DistinguisherAssignedNumberStepAcrossVrfs=None, DistinguisherCount=None, DistinguisherCountPerVrf=None, DistinguisherIpAddress=None, DistinguisherIpAddressStep=None, DistinguisherIpAddressStepAcrossVrfs=None, DistinguisherMode=None, DistinguisherStep=None, DistinguisherType=None, EnableAggregator=None, EnableAsPath=None, EnableAtomicAggregator=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginator=None, EnableUseTraditionalNlri=None, Enabled=None, FirstRoute=None, IncludeSourceAsExtendedCommunityPresent=None, IncludeVrfRouteImportExtendedCommunityPresent=None, IpType=None, LocalPref=None, MaskWidth=None, MaskWidthTo=None, Med=None, NextHopIpAddress=None, NextHopMode=None, NextHopSetMode=None, OriginProtocol=None, OriginatorId=None, PackingFrom=None, PackingTo=None, RouteCountPerVrfs=None, RouteStepAcrossVrfs=None, Step=None):
		"""Adds a new umhSelectionRouteRange node on the server and retrieves it in this instance.

		Args:
			AggregatorAsNumber (number): AS number associated with Aggregator ID in Aggregator attribute
			AggregatorIdIncrementMode (str(fixed|increment)): Increment mode of aggregator ID
			AggregatorIpAddress (str): IP address of the aggregator in Aggregator attribute
			DistinguisherAsNumber (number): Distinguisher AS number
			DistinguisherAsNumberStep (number): Increment step of Distinguisher AS number across the routes in route range
			DistinguisherAsNumberStepAcrossVrfs (number): Increment step of Distinguisher AS number across the VRFs in VRF range
			DistinguisherAssignedNumber (number): Distinguisher assigned number
			DistinguisherAssignedNumberStep (number): Increment step of distinguisher assigned number across routes in route range
			DistinguisherAssignedNumberStepAcrossVrfs (number): Increment step of distinguisher assigned number across VRFs in VRF range
			DistinguisherCount (number): Number of times increment step will be used ( default = 1 )
			DistinguisherCountPerVrf (number): Number of times increment step will be used per VRF
			DistinguisherIpAddress (str): Distinguisher IP address
			DistinguisherIpAddressStep (str): Increment step of distinguisher IP address across routes in route range
			DistinguisherIpAddressStepAcrossVrfs (str): Increment step of distinguisher IP address across VRFs in VRF range
			DistinguisherMode (str(global|local)): Specifies which part of the route distinguisher you want to increment.
			DistinguisherStep (number): The size of the increment step to be used with the part of the route distinguisher which will be incremented. (default = 1)
			DistinguisherType (str(as|ip|asNumber2)): Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.
			EnableAggregator (bool): Generates an AGGREGATOR attribute using the aggregatorIpAddress, aggregatorASNum, and aggregatorIDMode. (default = false)
			EnableAsPath (bool): Enables the generation of AS Path related items.
			EnableAtomicAggregator (bool): Sets the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)
			EnableCluster (bool): Enables the generation of the CLUSTER attribute list based on information in clusterList. (default = false)
			EnableCommunity (bool): Enables the generation of a COMMUNITY attribute list. (default = false)
			EnableGenerateUniqueRoutes (bool): When set to 1, each router generates a different IP address range. When not enabled, each router will advertise the route range as is.
			EnableLocalPref (bool): Enables the generation of a LOCAL PREF attribute based on the information in localPref. This value should be set to true only for EBGP. (default = false)
			EnableMed (bool): Enables the generation of a MULTI EXIT DISCRIMINATOR attribute. (default = false)
			EnableNextHop (bool): Enables the generation of a NEXT HOP attribute. (default = true)
			EnableOrigin (bool): Enables the generation of an ORIGIN attribute. (default = true)
			EnableOriginator (bool): Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)
			EnableUseTraditionalNlri (bool): If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)
			Enabled (bool): Enables the UMH route range.
			FirstRoute (str): First route in route range
			IncludeSourceAsExtendedCommunityPresent (bool): If for a given MVPN BGP is used for exchanging C-multicast routes, or if segmented
			IncludeVrfRouteImportExtendedCommunityPresent (bool): Defines the route target extended community.
			IpType (str(ipAny|ipv4|ipv6)): The type of IP address in nextworkAddress.
			LocalPref (number): The local preference value for the routes with the LOCAL PREF attribute. (default = 0)
			MaskWidth (number): Mask width of route range
			MaskWidthTo (number): mask width of last route range
			Med (number): The multi-exit discriminator value in the MULTI EXIT DISCRIMINATOR attribute. (default = 0)
			NextHopIpAddress (str): The IP address, in either IPv4 or IPv6 format of the next hop associated with the NEXT HOP attribute. (default = 0.0.0.0)
			NextHopMode (str(nextHopIncrement|fixed|incrementPerPrefix)): Indicates that the nextHopIpAddress may be incremented for each neighbor session generated for the range of neighbor addresses.
			NextHopSetMode (str(sameAsLocalIp|setManually)): Indicates now to set the next hop IP address.
			OriginProtocol (str(igp|egp|incomplete)): An indication of where the route entry originated.
			OriginatorId (str): The router that originated a particular route; associated with the ORIGINATOR-ID attribute. (default = 0.0.0.0)
			PackingFrom (number): Initial number of route packed in one BGP update
			PackingTo (number): Final number of routes packed in one BGP update
			RouteCountPerVrfs (number): Number of route per VRF
			RouteStepAcrossVrfs (str): The route increment value across VRFs.
			Step (number): step

		Returns:
			self: This instance with all currently retrieved umhSelectionRouteRange data using find and the newly added umhSelectionRouteRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the umhSelectionRouteRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AggregatorAsNumber=None, AggregatorIdIncrementMode=None, AggregatorIpAddress=None, DistinguisherAsNumber=None, DistinguisherAsNumberStep=None, DistinguisherAsNumberStepAcrossVrfs=None, DistinguisherAssignedNumber=None, DistinguisherAssignedNumberStep=None, DistinguisherAssignedNumberStepAcrossVrfs=None, DistinguisherCount=None, DistinguisherCountPerVrf=None, DistinguisherIpAddress=None, DistinguisherIpAddressStep=None, DistinguisherIpAddressStepAcrossVrfs=None, DistinguisherMode=None, DistinguisherStep=None, DistinguisherType=None, EnableAggregator=None, EnableAsPath=None, EnableAtomicAggregator=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginator=None, EnableUseTraditionalNlri=None, Enabled=None, FirstRoute=None, IncludeSourceAsExtendedCommunityPresent=None, IncludeVrfRouteImportExtendedCommunityPresent=None, IpType=None, LocalPref=None, MaskWidth=None, MaskWidthTo=None, Med=None, NextHopIpAddress=None, NextHopMode=None, NextHopSetMode=None, OriginProtocol=None, OriginatorId=None, PackingFrom=None, PackingTo=None, RouteCountPerVrfs=None, RouteStepAcrossVrfs=None, Step=None):
		"""Finds and retrieves umhSelectionRouteRange data from the server.

		All named parameters support regex and can be used to selectively retrieve umhSelectionRouteRange data from the server.
		By default the find method takes no parameters and will retrieve all umhSelectionRouteRange data from the server.

		Args:
			AggregatorAsNumber (number): AS number associated with Aggregator ID in Aggregator attribute
			AggregatorIdIncrementMode (str(fixed|increment)): Increment mode of aggregator ID
			AggregatorIpAddress (str): IP address of the aggregator in Aggregator attribute
			DistinguisherAsNumber (number): Distinguisher AS number
			DistinguisherAsNumberStep (number): Increment step of Distinguisher AS number across the routes in route range
			DistinguisherAsNumberStepAcrossVrfs (number): Increment step of Distinguisher AS number across the VRFs in VRF range
			DistinguisherAssignedNumber (number): Distinguisher assigned number
			DistinguisherAssignedNumberStep (number): Increment step of distinguisher assigned number across routes in route range
			DistinguisherAssignedNumberStepAcrossVrfs (number): Increment step of distinguisher assigned number across VRFs in VRF range
			DistinguisherCount (number): Number of times increment step will be used ( default = 1 )
			DistinguisherCountPerVrf (number): Number of times increment step will be used per VRF
			DistinguisherIpAddress (str): Distinguisher IP address
			DistinguisherIpAddressStep (str): Increment step of distinguisher IP address across routes in route range
			DistinguisherIpAddressStepAcrossVrfs (str): Increment step of distinguisher IP address across VRFs in VRF range
			DistinguisherMode (str(global|local)): Specifies which part of the route distinguisher you want to increment.
			DistinguisherStep (number): The size of the increment step to be used with the part of the route distinguisher which will be incremented. (default = 1)
			DistinguisherType (str(as|ip|asNumber2)): Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.
			EnableAggregator (bool): Generates an AGGREGATOR attribute using the aggregatorIpAddress, aggregatorASNum, and aggregatorIDMode. (default = false)
			EnableAsPath (bool): Enables the generation of AS Path related items.
			EnableAtomicAggregator (bool): Sets the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)
			EnableCluster (bool): Enables the generation of the CLUSTER attribute list based on information in clusterList. (default = false)
			EnableCommunity (bool): Enables the generation of a COMMUNITY attribute list. (default = false)
			EnableGenerateUniqueRoutes (bool): When set to 1, each router generates a different IP address range. When not enabled, each router will advertise the route range as is.
			EnableLocalPref (bool): Enables the generation of a LOCAL PREF attribute based on the information in localPref. This value should be set to true only for EBGP. (default = false)
			EnableMed (bool): Enables the generation of a MULTI EXIT DISCRIMINATOR attribute. (default = false)
			EnableNextHop (bool): Enables the generation of a NEXT HOP attribute. (default = true)
			EnableOrigin (bool): Enables the generation of an ORIGIN attribute. (default = true)
			EnableOriginator (bool): Enables the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)
			EnableUseTraditionalNlri (bool): If enabled, use the traditional NLRI in the UPDATE message, instead of using the MP_REACH_NLRI Multi-protocol extension to advertise the routes. (Not applicable for MPLS and MPLS VPN Route Ranges.)
			Enabled (bool): Enables the UMH route range.
			FirstRoute (str): First route in route range
			IncludeSourceAsExtendedCommunityPresent (bool): If for a given MVPN BGP is used for exchanging C-multicast routes, or if segmented
			IncludeVrfRouteImportExtendedCommunityPresent (bool): Defines the route target extended community.
			IpType (str(ipAny|ipv4|ipv6)): The type of IP address in nextworkAddress.
			LocalPref (number): The local preference value for the routes with the LOCAL PREF attribute. (default = 0)
			MaskWidth (number): Mask width of route range
			MaskWidthTo (number): mask width of last route range
			Med (number): The multi-exit discriminator value in the MULTI EXIT DISCRIMINATOR attribute. (default = 0)
			NextHopIpAddress (str): The IP address, in either IPv4 or IPv6 format of the next hop associated with the NEXT HOP attribute. (default = 0.0.0.0)
			NextHopMode (str(nextHopIncrement|fixed|incrementPerPrefix)): Indicates that the nextHopIpAddress may be incremented for each neighbor session generated for the range of neighbor addresses.
			NextHopSetMode (str(sameAsLocalIp|setManually)): Indicates now to set the next hop IP address.
			OriginProtocol (str(igp|egp|incomplete)): An indication of where the route entry originated.
			OriginatorId (str): The router that originated a particular route; associated with the ORIGINATOR-ID attribute. (default = 0.0.0.0)
			PackingFrom (number): Initial number of route packed in one BGP update
			PackingTo (number): Final number of routes packed in one BGP update
			RouteCountPerVrfs (number): Number of route per VRF
			RouteStepAcrossVrfs (str): The route increment value across VRFs.
			Step (number): step

		Returns:
			self: This instance with matching umhSelectionRouteRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of umhSelectionRouteRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the umhSelectionRouteRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
