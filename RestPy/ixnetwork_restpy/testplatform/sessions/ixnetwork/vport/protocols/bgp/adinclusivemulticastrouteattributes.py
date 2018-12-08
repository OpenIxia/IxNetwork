
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


class AdInclusiveMulticastRouteAttributes(Base):
	"""The AdInclusiveMulticastRouteAttributes class encapsulates a required adInclusiveMulticastRouteAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdInclusiveMulticastRouteAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'adInclusiveMulticastRouteAttributes'

	def __init__(self, parent):
		super(AdInclusiveMulticastRouteAttributes, self).__init__(parent)

	@property
	def AggregatorAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('aggregatorAs')
	@AggregatorAs.setter
	def AggregatorAs(self, value):
		self._set_attribute('aggregatorAs', value)

	@property
	def AggregatorId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('aggregatorId')
	@AggregatorId.setter
	def AggregatorId(self, value):
		self._set_attribute('aggregatorId', value)

	@property
	def AsPath(self):
		"""

		Returns:
			list(dict(arg1:bool,arg2:str[unknown|asSet|asSequence|asConfedSet|asConfedSequence],arg3:list[number]))
		"""
		return self._get_attribute('asPath')
	@AsPath.setter
	def AsPath(self, value):
		self._set_attribute('asPath', value)

	@property
	def AsSetMode(self):
		"""

		Returns:
			str(includeAsSeq|includeAsSeqConf|includeAsSet|includeAsSetConf|noInclude|prependAs)
		"""
		return self._get_attribute('asSetMode')
	@AsSetMode.setter
	def AsSetMode(self, value):
		self._set_attribute('asSetMode', value)

	@property
	def Cluster(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('cluster')
	@Cluster.setter
	def Cluster(self, value):
		self._set_attribute('cluster', value)

	@property
	def Community(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('community')
	@Community.setter
	def Community(self, value):
		self._set_attribute('community', value)

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
	def EnableAtomicAggregate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAtomicAggregate')
	@EnableAtomicAggregate.setter
	def EnableAtomicAggregate(self, value):
		self._set_attribute('enableAtomicAggregate', value)

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
	def EnableMultiExit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMultiExit')
	@EnableMultiExit.setter
	def EnableMultiExit(self, value):
		self._set_attribute('enableMultiExit', value)

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
	def ExtendedCommunity(self):
		"""

		Returns:
			list(dict(arg1:str[decimal|hex|ip|ieeeFloat],arg2:str[decimal|hex|ip|ieeeFloat],arg3:str[twoOctetAs|ip|fourOctetAs|opaque|administratorAsTwoOctetLinkBw],arg4:str[routeTarget|origin|extendedBandwidthSubType],arg5:str))
		"""
		return self._get_attribute('extendedCommunity')
	@ExtendedCommunity.setter
	def ExtendedCommunity(self, value):
		self._set_attribute('extendedCommunity', value)

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
	def MultiExit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multiExit')
	@MultiExit.setter
	def MultiExit(self, value):
		self._set_attribute('multiExit', value)

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
	def NextHopIpType(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('nextHopIpType')
	@NextHopIpType.setter
	def NextHopIpType(self, value):
		self._set_attribute('nextHopIpType', value)

	@property
	def NextHopMode(self):
		"""

		Returns:
			str(fixed|incrementPerPeer)
		"""
		return self._get_attribute('nextHopMode')
	@NextHopMode.setter
	def NextHopMode(self, value):
		self._set_attribute('nextHopMode', value)

	@property
	def Origin(self):
		"""

		Returns:
			str(igp|egp|incomplete)
		"""
		return self._get_attribute('origin')
	@Origin.setter
	def Origin(self, value):
		self._set_attribute('origin', value)

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
	def SetNextHop(self):
		"""

		Returns:
			str(manually|sameAsLocalIp)
		"""
		return self._get_attribute('setNextHop')
	@SetNextHop.setter
	def SetNextHop(self, value):
		self._set_attribute('setNextHop', value)
