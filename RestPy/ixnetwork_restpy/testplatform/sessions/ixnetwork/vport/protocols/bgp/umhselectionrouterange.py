
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
		"""

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAsNumber')
	@AggregatorAsNumber.setter
	def AggregatorAsNumber(self, value):
		self._set_attribute('aggregatorAsNumber', value)

	@property
	def AggregatorIdIncrementMode(self):
		"""

		Returns:
			str(fixed|increment)
		"""
		return self._get_attribute('aggregatorIdIncrementMode')
	@AggregatorIdIncrementMode.setter
	def AggregatorIdIncrementMode(self, value):
		self._set_attribute('aggregatorIdIncrementMode', value)

	@property
	def AggregatorIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('aggregatorIpAddress')
	@AggregatorIpAddress.setter
	def AggregatorIpAddress(self, value):
		self._set_attribute('aggregatorIpAddress', value)

	@property
	def DistinguisherAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumber')
	@DistinguisherAsNumber.setter
	def DistinguisherAsNumber(self, value):
		self._set_attribute('distinguisherAsNumber', value)

	@property
	def DistinguisherAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumberStep')
	@DistinguisherAsNumberStep.setter
	def DistinguisherAsNumberStep(self, value):
		self._set_attribute('distinguisherAsNumberStep', value)

	@property
	def DistinguisherAsNumberStepAcrossVrfs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAsNumberStepAcrossVrfs')
	@DistinguisherAsNumberStepAcrossVrfs.setter
	def DistinguisherAsNumberStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherAsNumberStepAcrossVrfs', value)

	@property
	def DistinguisherAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumber')
	@DistinguisherAssignedNumber.setter
	def DistinguisherAssignedNumber(self, value):
		self._set_attribute('distinguisherAssignedNumber', value)

	@property
	def DistinguisherAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumberStep')
	@DistinguisherAssignedNumberStep.setter
	def DistinguisherAssignedNumberStep(self, value):
		self._set_attribute('distinguisherAssignedNumberStep', value)

	@property
	def DistinguisherAssignedNumberStepAcrossVrfs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherAssignedNumberStepAcrossVrfs')
	@DistinguisherAssignedNumberStepAcrossVrfs.setter
	def DistinguisherAssignedNumberStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherAssignedNumberStepAcrossVrfs', value)

	@property
	def DistinguisherCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherCount')
	@DistinguisherCount.setter
	def DistinguisherCount(self, value):
		self._set_attribute('distinguisherCount', value)

	@property
	def DistinguisherCountPerVrf(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherCountPerVrf')
	@DistinguisherCountPerVrf.setter
	def DistinguisherCountPerVrf(self, value):
		self._set_attribute('distinguisherCountPerVrf', value)

	@property
	def DistinguisherIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddress')
	@DistinguisherIpAddress.setter
	def DistinguisherIpAddress(self, value):
		self._set_attribute('distinguisherIpAddress', value)

	@property
	def DistinguisherIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddressStep')
	@DistinguisherIpAddressStep.setter
	def DistinguisherIpAddressStep(self, value):
		self._set_attribute('distinguisherIpAddressStep', value)

	@property
	def DistinguisherIpAddressStepAcrossVrfs(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('distinguisherIpAddressStepAcrossVrfs')
	@DistinguisherIpAddressStepAcrossVrfs.setter
	def DistinguisherIpAddressStepAcrossVrfs(self, value):
		self._set_attribute('distinguisherIpAddressStepAcrossVrfs', value)

	@property
	def DistinguisherMode(self):
		"""

		Returns:
			str(global|local)
		"""
		return self._get_attribute('distinguisherMode')
	@DistinguisherMode.setter
	def DistinguisherMode(self, value):
		self._set_attribute('distinguisherMode', value)

	@property
	def DistinguisherStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguisherStep')
	@DistinguisherStep.setter
	def DistinguisherStep(self, value):
		self._set_attribute('distinguisherStep', value)

	@property
	def DistinguisherType(self):
		"""

		Returns:
			str(as|ip|asNumber2)
		"""
		return self._get_attribute('distinguisherType')
	@DistinguisherType.setter
	def DistinguisherType(self, value):
		self._set_attribute('distinguisherType', value)

	@property
	def EnableAggregator(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregator')
	@EnableAggregator.setter
	def EnableAggregator(self, value):
		self._set_attribute('enableAggregator', value)

	@property
	def EnableAsPath(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAsPath')
	@EnableAsPath.setter
	def EnableAsPath(self, value):
		self._set_attribute('enableAsPath', value)

	@property
	def EnableAtomicAggregator(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAggregator')
	@EnableAtomicAggregator.setter
	def EnableAtomicAggregator(self, value):
		self._set_attribute('enableAtomicAggregator', value)

	@property
	def EnableCluster(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCluster')
	@EnableCluster.setter
	def EnableCluster(self, value):
		self._set_attribute('enableCluster', value)

	@property
	def EnableCommunity(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCommunity')
	@EnableCommunity.setter
	def EnableCommunity(self, value):
		self._set_attribute('enableCommunity', value)

	@property
	def EnableGenerateUniqueRoutes(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableGenerateUniqueRoutes')
	@EnableGenerateUniqueRoutes.setter
	def EnableGenerateUniqueRoutes(self, value):
		self._set_attribute('enableGenerateUniqueRoutes', value)

	@property
	def EnableLocalPref(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLocalPref')
	@EnableLocalPref.setter
	def EnableLocalPref(self, value):
		self._set_attribute('enableLocalPref', value)

	@property
	def EnableMed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMed')
	@EnableMed.setter
	def EnableMed(self, value):
		self._set_attribute('enableMed', value)

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
	def EnableOrigin(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOrigin')
	@EnableOrigin.setter
	def EnableOrigin(self, value):
		self._set_attribute('enableOrigin', value)

	@property
	def EnableOriginator(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOriginator')
	@EnableOriginator.setter
	def EnableOriginator(self, value):
		self._set_attribute('enableOriginator', value)

	@property
	def EnableUseTraditionalNlri(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableUseTraditionalNlri')
	@EnableUseTraditionalNlri.setter
	def EnableUseTraditionalNlri(self, value):
		self._set_attribute('enableUseTraditionalNlri', value)

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
	def FirstRoute(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

	@property
	def IncludeSourceAsExtendedCommunityPresent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeSourceAsExtendedCommunityPresent')
	@IncludeSourceAsExtendedCommunityPresent.setter
	def IncludeSourceAsExtendedCommunityPresent(self, value):
		self._set_attribute('includeSourceAsExtendedCommunityPresent', value)

	@property
	def IncludeVrfRouteImportExtendedCommunityPresent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeVrfRouteImportExtendedCommunityPresent')
	@IncludeVrfRouteImportExtendedCommunityPresent.setter
	def IncludeVrfRouteImportExtendedCommunityPresent(self, value):
		self._set_attribute('includeVrfRouteImportExtendedCommunityPresent', value)

	@property
	def IpType(self):
		"""

		Returns:
			str(ipAny|ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def LocalPref(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localPref')
	@LocalPref.setter
	def LocalPref(self, value):
		self._set_attribute('localPref', value)

	@property
	def MaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def MaskWidthTo(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maskWidthTo')
	@MaskWidthTo.setter
	def MaskWidthTo(self, value):
		self._set_attribute('maskWidthTo', value)

	@property
	def Med(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('med')
	@Med.setter
	def Med(self, value):
		self._set_attribute('med', value)

	@property
	def NextHopIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('nextHopIpAddress')
	@NextHopIpAddress.setter
	def NextHopIpAddress(self, value):
		self._set_attribute('nextHopIpAddress', value)

	@property
	def NextHopMode(self):
		"""

		Returns:
			str(nextHopIncrement|fixed|incrementPerPrefix)
		"""
		return self._get_attribute('nextHopMode')
	@NextHopMode.setter
	def NextHopMode(self, value):
		self._set_attribute('nextHopMode', value)

	@property
	def NextHopSetMode(self):
		"""

		Returns:
			str(sameAsLocalIp|setManually)
		"""
		return self._get_attribute('nextHopSetMode')
	@NextHopSetMode.setter
	def NextHopSetMode(self, value):
		self._set_attribute('nextHopSetMode', value)

	@property
	def OriginProtocol(self):
		"""

		Returns:
			str(igp|egp|incomplete)
		"""
		return self._get_attribute('originProtocol')
	@OriginProtocol.setter
	def OriginProtocol(self, value):
		self._set_attribute('originProtocol', value)

	@property
	def OriginatorId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('originatorId')
	@OriginatorId.setter
	def OriginatorId(self, value):
		self._set_attribute('originatorId', value)

	@property
	def PackingFrom(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packingFrom')
	@PackingFrom.setter
	def PackingFrom(self, value):
		self._set_attribute('packingFrom', value)

	@property
	def PackingTo(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('packingTo')
	@PackingTo.setter
	def PackingTo(self, value):
		self._set_attribute('packingTo', value)

	@property
	def RouteCountPerVrfs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeCountPerVrfs')
	@RouteCountPerVrfs.setter
	def RouteCountPerVrfs(self, value):
		self._set_attribute('routeCountPerVrfs', value)

	@property
	def RouteStepAcrossVrfs(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeStepAcrossVrfs')
	@RouteStepAcrossVrfs.setter
	def RouteStepAcrossVrfs(self, value):
		self._set_attribute('routeStepAcrossVrfs', value)

	@property
	def Step(self):
		"""

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
			AggregatorAsNumber (number): 
			AggregatorIdIncrementMode (str(fixed|increment)): 
			AggregatorIpAddress (str): 
			DistinguisherAsNumber (number): 
			DistinguisherAsNumberStep (number): 
			DistinguisherAsNumberStepAcrossVrfs (number): 
			DistinguisherAssignedNumber (number): 
			DistinguisherAssignedNumberStep (number): 
			DistinguisherAssignedNumberStepAcrossVrfs (number): 
			DistinguisherCount (number): 
			DistinguisherCountPerVrf (number): 
			DistinguisherIpAddress (str): 
			DistinguisherIpAddressStep (str): 
			DistinguisherIpAddressStepAcrossVrfs (str): 
			DistinguisherMode (str(global|local)): 
			DistinguisherStep (number): 
			DistinguisherType (str(as|ip|asNumber2)): 
			EnableAggregator (bool): 
			EnableAsPath (bool): 
			EnableAtomicAggregator (bool): 
			EnableCluster (bool): 
			EnableCommunity (bool): 
			EnableGenerateUniqueRoutes (bool): 
			EnableLocalPref (bool): 
			EnableMed (bool): 
			EnableNextHop (bool): 
			EnableOrigin (bool): 
			EnableOriginator (bool): 
			EnableUseTraditionalNlri (bool): 
			Enabled (bool): 
			FirstRoute (str): 
			IncludeSourceAsExtendedCommunityPresent (bool): 
			IncludeVrfRouteImportExtendedCommunityPresent (bool): 
			IpType (str(ipAny|ipv4|ipv6)): 
			LocalPref (number): 
			MaskWidth (number): 
			MaskWidthTo (number): 
			Med (number): 
			NextHopIpAddress (str): 
			NextHopMode (str(nextHopIncrement|fixed|incrementPerPrefix)): 
			NextHopSetMode (str(sameAsLocalIp|setManually)): 
			OriginProtocol (str(igp|egp|incomplete)): 
			OriginatorId (str): 
			PackingFrom (number): 
			PackingTo (number): 
			RouteCountPerVrfs (number): 
			RouteStepAcrossVrfs (str): 
			Step (number): 

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
			AggregatorAsNumber (number): 
			AggregatorIdIncrementMode (str(fixed|increment)): 
			AggregatorIpAddress (str): 
			DistinguisherAsNumber (number): 
			DistinguisherAsNumberStep (number): 
			DistinguisherAsNumberStepAcrossVrfs (number): 
			DistinguisherAssignedNumber (number): 
			DistinguisherAssignedNumberStep (number): 
			DistinguisherAssignedNumberStepAcrossVrfs (number): 
			DistinguisherCount (number): 
			DistinguisherCountPerVrf (number): 
			DistinguisherIpAddress (str): 
			DistinguisherIpAddressStep (str): 
			DistinguisherIpAddressStepAcrossVrfs (str): 
			DistinguisherMode (str(global|local)): 
			DistinguisherStep (number): 
			DistinguisherType (str(as|ip|asNumber2)): 
			EnableAggregator (bool): 
			EnableAsPath (bool): 
			EnableAtomicAggregator (bool): 
			EnableCluster (bool): 
			EnableCommunity (bool): 
			EnableGenerateUniqueRoutes (bool): 
			EnableLocalPref (bool): 
			EnableMed (bool): 
			EnableNextHop (bool): 
			EnableOrigin (bool): 
			EnableOriginator (bool): 
			EnableUseTraditionalNlri (bool): 
			Enabled (bool): 
			FirstRoute (str): 
			IncludeSourceAsExtendedCommunityPresent (bool): 
			IncludeVrfRouteImportExtendedCommunityPresent (bool): 
			IpType (str(ipAny|ipv4|ipv6)): 
			LocalPref (number): 
			MaskWidth (number): 
			MaskWidthTo (number): 
			Med (number): 
			NextHopIpAddress (str): 
			NextHopMode (str(nextHopIncrement|fixed|incrementPerPrefix)): 
			NextHopSetMode (str(sameAsLocalIp|setManually)): 
			OriginProtocol (str(igp|egp|incomplete)): 
			OriginatorId (str): 
			PackingFrom (number): 
			PackingTo (number): 
			RouteCountPerVrfs (number): 
			RouteStepAcrossVrfs (str): 
			Step (number): 

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
