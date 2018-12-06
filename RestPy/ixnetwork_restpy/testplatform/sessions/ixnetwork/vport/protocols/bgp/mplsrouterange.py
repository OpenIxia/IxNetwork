
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


class MplsRouteRange(Base):
	"""The MplsRouteRange class encapsulates a user managed mplsRouteRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MplsRouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'mplsRouteRange'

	def __init__(self, parent):
		super(MplsRouteRange, self).__init__(parent)

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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('advertiseNextHopAsV4')
	@AdvertiseNextHopAsV4.setter
	def AdvertiseNextHopAsV4(self, value):
		self._set_attribute('advertiseNextHopAsV4', value)

	@property
	def AggregatorAsNum(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAsNum')
	@AggregatorAsNum.setter
	def AggregatorAsNum(self, value):
		self._set_attribute('aggregatorAsNum', value)

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
	def AsPathSetMode(self):
		"""

		Returns:
			str(noInclude|includeAsSeq|includeAsSet|includeAsSeqConf|includeAsSetConf|prependAs)
		"""
		return self._get_attribute('asPathSetMode')
	@AsPathSetMode.setter
	def AsPathSetMode(self, value):
		self._set_attribute('asPathSetMode', value)

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
	def EnableAggregatorIdIncrementMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregatorIdIncrementMode')
	@EnableAggregatorIdIncrementMode.setter
	def EnableAggregatorIdIncrementMode(self, value):
		self._set_attribute('enableAggregatorIdIncrementMode', value)

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
	def EnableAtomicAttribute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAttribute')
	@EnableAtomicAttribute.setter
	def EnableAtomicAttribute(self, value):
		self._set_attribute('enableAtomicAttribute', value)

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
	def EnableOriginatorId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOriginatorId')
	@EnableOriginatorId.setter
	def EnableOriginatorId(self, value):
		self._set_attribute('enableOriginatorId', value)

	@property
	def EnableTraditionalNlriUpdate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableTraditionalNlriUpdate')
	@EnableTraditionalNlriUpdate.setter
	def EnableTraditionalNlriUpdate(self, value):
		self._set_attribute('enableTraditionalNlriUpdate', value)

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
	def EndOfRib(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('endOfRib')
	@EndOfRib.setter
	def EndOfRib(self, value):
		self._set_attribute('endOfRib', value)

	@property
	def FromPacking(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fromPacking')
	@FromPacking.setter
	def FromPacking(self, value):
		self._set_attribute('fromPacking', value)

	@property
	def FromPrefix(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fromPrefix')
	@FromPrefix.setter
	def FromPrefix(self, value):
		self._set_attribute('fromPrefix', value)

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
	def IterationStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iterationStep')
	@IterationStep.setter
	def IterationStep(self, value):
		self._set_attribute('iterationStep', value)

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
	def NetworkAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('networkAddress')
	@NetworkAddress.setter
	def NetworkAddress(self, value):
		self._set_attribute('networkAddress', value)

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
			str(fixed|nextHopIncrement|incrementPerPrefix)
		"""
		return self._get_attribute('nextHopMode')
	@NextHopMode.setter
	def NextHopMode(self, value):
		self._set_attribute('nextHopMode', value)

	@property
	def NextHopSetMode(self):
		"""

		Returns:
			str(setManually|sameAsLocalIp)
		"""
		return self._get_attribute('nextHopSetMode')
	@NextHopSetMode.setter
	def NextHopSetMode(self, value):
		self._set_attribute('nextHopSetMode', value)

	@property
	def NumRoutes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numRoutes')
	@NumRoutes.setter
	def NumRoutes(self, value):
		self._set_attribute('numRoutes', value)

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
	def ThruPacking(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('thruPacking')
	@ThruPacking.setter
	def ThruPacking(self, value):
		self._set_attribute('thruPacking', value)

	@property
	def ThruPrefix(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('thruPrefix')
	@ThruPrefix.setter
	def ThruPrefix(self, value):
		self._set_attribute('thruPrefix', value)

	def add(self, AdvertiseNextHopAsV4=None, AggregatorAsNum=None, AggregatorIpAddress=None, AsPathSetMode=None, EnableAggregator=None, EnableAggregatorIdIncrementMode=None, EnableAsPath=None, EnableAtomicAttribute=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableIncludeLoopback=None, EnableIncludeMulticast=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableTraditionalNlriUpdate=None, Enabled=None, EndOfRib=None, FromPacking=None, FromPrefix=None, IpType=None, IterationStep=None, LocalPref=None, Med=None, NetworkAddress=None, NextHopIpAddress=None, NextHopMode=None, NextHopSetMode=None, NumRoutes=None, OriginProtocol=None, OriginatorId=None, ThruPacking=None, ThruPrefix=None):
		"""Adds a new mplsRouteRange node on the server and retrieves it in this instance.

		Args:
			AdvertiseNextHopAsV4 (bool): 
			AggregatorAsNum (number): 
			AggregatorIpAddress (str): 
			AsPathSetMode (str(noInclude|includeAsSeq|includeAsSet|includeAsSeqConf|includeAsSetConf|prependAs)): 
			EnableAggregator (bool): 
			EnableAggregatorIdIncrementMode (bool): 
			EnableAsPath (bool): 
			EnableAtomicAttribute (bool): 
			EnableCluster (bool): 
			EnableCommunity (bool): 
			EnableGenerateUniqueRoutes (bool): 
			EnableIncludeLoopback (bool): 
			EnableIncludeMulticast (bool): 
			EnableLocalPref (bool): 
			EnableMed (bool): 
			EnableNextHop (bool): 
			EnableOrigin (bool): 
			EnableOriginatorId (bool): 
			EnableTraditionalNlriUpdate (bool): 
			Enabled (bool): 
			EndOfRib (bool): 
			FromPacking (number): 
			FromPrefix (number): 
			IpType (str(ipAny|ipv4|ipv6)): 
			IterationStep (number): 
			LocalPref (number): 
			Med (number): 
			NetworkAddress (str): 
			NextHopIpAddress (str): 
			NextHopMode (str(fixed|nextHopIncrement|incrementPerPrefix)): 
			NextHopSetMode (str(setManually|sameAsLocalIp)): 
			NumRoutes (number): 
			OriginProtocol (str(igp|egp|incomplete)): 
			OriginatorId (str): 
			ThruPacking (number): 
			ThruPrefix (number): 

		Returns:
			self: This instance with all currently retrieved mplsRouteRange data using find and the newly added mplsRouteRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the mplsRouteRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertiseNextHopAsV4=None, AggregatorAsNum=None, AggregatorIpAddress=None, AsPathSetMode=None, EnableAggregator=None, EnableAggregatorIdIncrementMode=None, EnableAsPath=None, EnableAtomicAttribute=None, EnableCluster=None, EnableCommunity=None, EnableGenerateUniqueRoutes=None, EnableIncludeLoopback=None, EnableIncludeMulticast=None, EnableLocalPref=None, EnableMed=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableTraditionalNlriUpdate=None, Enabled=None, EndOfRib=None, FromPacking=None, FromPrefix=None, IpType=None, IterationStep=None, LocalPref=None, Med=None, NetworkAddress=None, NextHopIpAddress=None, NextHopMode=None, NextHopSetMode=None, NumRoutes=None, OriginProtocol=None, OriginatorId=None, ThruPacking=None, ThruPrefix=None):
		"""Finds and retrieves mplsRouteRange data from the server.

		All named parameters support regex and can be used to selectively retrieve mplsRouteRange data from the server.
		By default the find method takes no parameters and will retrieve all mplsRouteRange data from the server.

		Args:
			AdvertiseNextHopAsV4 (bool): 
			AggregatorAsNum (number): 
			AggregatorIpAddress (str): 
			AsPathSetMode (str(noInclude|includeAsSeq|includeAsSet|includeAsSeqConf|includeAsSetConf|prependAs)): 
			EnableAggregator (bool): 
			EnableAggregatorIdIncrementMode (bool): 
			EnableAsPath (bool): 
			EnableAtomicAttribute (bool): 
			EnableCluster (bool): 
			EnableCommunity (bool): 
			EnableGenerateUniqueRoutes (bool): 
			EnableIncludeLoopback (bool): 
			EnableIncludeMulticast (bool): 
			EnableLocalPref (bool): 
			EnableMed (bool): 
			EnableNextHop (bool): 
			EnableOrigin (bool): 
			EnableOriginatorId (bool): 
			EnableTraditionalNlriUpdate (bool): 
			Enabled (bool): 
			EndOfRib (bool): 
			FromPacking (number): 
			FromPrefix (number): 
			IpType (str(ipAny|ipv4|ipv6)): 
			IterationStep (number): 
			LocalPref (number): 
			Med (number): 
			NetworkAddress (str): 
			NextHopIpAddress (str): 
			NextHopMode (str(fixed|nextHopIncrement|incrementPerPrefix)): 
			NextHopSetMode (str(setManually|sameAsLocalIp)): 
			NumRoutes (number): 
			OriginProtocol (str(igp|egp|incomplete)): 
			OriginatorId (str): 
			ThruPacking (number): 
			ThruPrefix (number): 

		Returns:
			self: This instance with matching mplsRouteRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of mplsRouteRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the mplsRouteRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
