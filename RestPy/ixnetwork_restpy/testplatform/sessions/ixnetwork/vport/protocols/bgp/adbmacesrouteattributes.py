
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


class AdBmacEsRouteAttributes(Base):
	"""The AdBmacEsRouteAttributes class encapsulates a required adBmacEsRouteAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdBmacEsRouteAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'adBmacEsRouteAttributes'

	def __init__(self, parent):
		super(AdBmacEsRouteAttributes, self).__init__(parent)

	@property
	def AggregatorAs(self):
		"""This signifies the AS associated with the aggregator router ID in the AGGREGATOR attribute. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAs')
	@AggregatorAs.setter
	def AggregatorAs(self, value):
		self._set_attribute('aggregatorAs', value)

	@property
	def AggregatorId(self):
		"""This signifies the IP address of the router that aggregated two or more routes in the AGGREGATOR attribute. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('aggregatorId')
	@AggregatorId.setter
	def AggregatorId(self, value):
		self._set_attribute('aggregatorId', value)

	@property
	def AsPath(self):
		"""This signifes the local IP address of the BGP router

		Returns:
			list(dict(arg1:bool,arg2:str[unknown|asSet|asSequence|asConfedSet|asConfedSequence],arg3:list[number]))
		"""
		return self._get_attribute('asPath')
	@AsPath.setter
	def AsPath(self, value):
		self._set_attribute('asPath', value)

	@property
	def AsSetMode(self):
		"""NOT DEFINED

		Returns:
			str(includeAsSeq|includeAsSeqConf|includeAsSet|includeAsSetConf|noInclude|prependAs)
		"""
		return self._get_attribute('asSetMode')
	@AsSetMode.setter
	def AsSetMode(self, value):
		self._set_attribute('asSetMode', value)

	@property
	def Cluster(self):
		"""The list of BGP clusters that a particular route has passed through.

		Returns:
			list(number)
		"""
		return self._get_attribute('cluster')
	@Cluster.setter
	def Cluster(self, value):
		self._set_attribute('cluster', value)

	@property
	def Community(self):
		"""This signifies the BGP Community attribute to be added to the BGP entry

		Returns:
			list(number)
		"""
		return self._get_attribute('community')
	@Community.setter
	def Community(self, value):
		self._set_attribute('community', value)

	@property
	def EnableAggregator(self):
		"""This signifies to generate an AGGREGATOR attribute using the aggregatorIpAddress, aggregatorASNum, and aggregatorIDMode. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableAggregator')
	@EnableAggregator.setter
	def EnableAggregator(self, value):
		self._set_attribute('enableAggregator', value)

	@property
	def EnableAsPath(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableAsPath')
	@EnableAsPath.setter
	def EnableAsPath(self, value):
		self._set_attribute('enableAsPath', value)

	@property
	def EnableAtomicAggregate(self):
		"""This signifies to set the attribute bit that indicates that the router has aggregated two or more prefixes in the AGGREGATOR attribute. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAggregate')
	@EnableAtomicAggregate.setter
	def EnableAtomicAggregate(self, value):
		self._set_attribute('enableAtomicAggregate', value)

	@property
	def EnableCluster(self):
		"""This signifies to enable the generation of the CLUSTER attribute list based on information in clusterList. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableCluster')
	@EnableCluster.setter
	def EnableCluster(self, value):
		self._set_attribute('enableCluster', value)

	@property
	def EnableCommunity(self):
		"""This enables the generation of a COMMUNITY attribute list. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableCommunity')
	@EnableCommunity.setter
	def EnableCommunity(self, value):
		self._set_attribute('enableCommunity', value)

	@property
	def EnableLocalPref(self):
		"""This enables the generation of a LOCAL PREF attribute based on the information in localPref. This value should be set to true only for EBGP. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableLocalPref')
	@EnableLocalPref.setter
	def EnableLocalPref(self, value):
		self._set_attribute('enableLocalPref', value)

	@property
	def EnableMultiExit(self):
		"""This enables the generation of a MULTI EXIT DISCRIMINATOR attribute. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableMultiExit')
	@EnableMultiExit.setter
	def EnableMultiExit(self, value):
		self._set_attribute('enableMultiExit', value)

	@property
	def EnableNextHop(self):
		"""This enables the generation of a NEXT HOP attribute. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('enableNextHop')
	@EnableNextHop.setter
	def EnableNextHop(self, value):
		self._set_attribute('enableNextHop', value)

	@property
	def EnableOrigin(self):
		"""This enables the generation of an ORIGIN attribute. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('enableOrigin')
	@EnableOrigin.setter
	def EnableOrigin(self, value):
		self._set_attribute('enableOrigin', value)

	@property
	def EnableOriginator(self):
		"""This signifies to enable the generation of an ORIGINATOR-ID attribute, based on information in originatorId. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableOriginator')
	@EnableOriginator.setter
	def EnableOriginator(self, value):
		self._set_attribute('enableOriginator', value)

	@property
	def ExtendedCommunity(self):
		"""This is used to construct an extended community attribute for a route item

		Returns:
			list(dict(arg1:str[decimal|hex|ip|ieeeFloat],arg2:str[decimal|hex|ip|ieeeFloat],arg3:str[twoOctetAs|ip|fourOctetAs|opaque|administratorAsTwoOctetLinkBw],arg4:str[routeTarget|origin|extendedBandwidthSubType],arg5:str))
		"""
		return self._get_attribute('extendedCommunity')
	@ExtendedCommunity.setter
	def ExtendedCommunity(self, value):
		self._set_attribute('extendedCommunity', value)

	@property
	def LocalPref(self):
		"""This signifies the local preference value for the routes with the LOCAL PREF attribute. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('localPref')
	@LocalPref.setter
	def LocalPref(self, value):
		self._set_attribute('localPref', value)

	@property
	def MultiExit(self):
		"""This signifies the multi-exit discriminator value in the MULTI EXIT DISCRIMINATOR attribute. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('multiExit')
	@MultiExit.setter
	def MultiExit(self, value):
		self._set_attribute('multiExit', value)

	@property
	def NextHop(self):
		"""This signifies the IP address, in either IPv4 or IPv6 format of the next hop associated with the NEXT HOP attribute. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NextHopIpType(self):
		"""This signifies the IP type of Next Hop. Default is IPv4.

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('nextHopIpType')
	@NextHopIpType.setter
	def NextHopIpType(self, value):
		self._set_attribute('nextHopIpType', value)

	@property
	def NextHopMode(self):
		"""This signifies that the nextHopIpAddress may be incremented for each neighbor session generated for the range of neighbor addresses.

		Returns:
			str(fixed|incrementPerPeer)
		"""
		return self._get_attribute('nextHopMode')
	@NextHopMode.setter
	def NextHopMode(self, value):
		self._set_attribute('nextHopMode', value)

	@property
	def Origin(self):
		"""This signifies an indication of where the route entry originated.

		Returns:
			str(igp|egp|incomplete)
		"""
		return self._get_attribute('origin')
	@Origin.setter
	def Origin(self, value):
		self._set_attribute('origin', value)

	@property
	def OriginatorId(self):
		"""This signifies the router that originated a particular route; associated with the ORIGINATOR-ID attribute. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('originatorId')
	@OriginatorId.setter
	def OriginatorId(self, value):
		self._set_attribute('originatorId', value)

	@property
	def SetNextHop(self):
		"""This signifies now to set the next hop IP address.

		Returns:
			str(manually|sameAsLocalIp)
		"""
		return self._get_attribute('setNextHop')
	@SetNextHop.setter
	def SetNextHop(self, value):
		self._set_attribute('setNextHop', value)
