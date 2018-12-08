
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


class BgpEthernetSegmentV4(Base):
	"""The BgpEthernetSegmentV4 class encapsulates a required bgpEthernetSegmentV4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpEthernetSegmentV4 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpEthernetSegmentV4'

	def __init__(self, parent):
		super(BgpEthernetSegmentV4, self).__init__(parent)

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
	def Bgpv4BMacMappedIpList(self):
		"""An instance of the Bgpv4BMacMappedIpList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv4bmacmappediplist.Bgpv4BMacMappedIpList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpv4bmacmappediplist import Bgpv4BMacMappedIpList
		return Bgpv4BMacMappedIpList(self)._select()

	@property
	def AdvertiseAliasingBeforeAdPerEsRoute(self):
		"""Advertise Aliasing Before A-D/ES Route

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('AdvertiseAliasingBeforeAdPerEsRoute')

	@property
	def AdvertiseInclusiveMulticastRoute(self):
		"""Support Inclusive Multicast Ethernet Tag Route (RT Type 3)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('AdvertiseInclusiveMulticastRoute')

	@property
	def AliasingRouteGranularity(self):
		"""Aliasing Route Granularity

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('AliasingRouteGranularity')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvertiseAliasingAutomatically(self):
		"""Advertise Aliasing Automatically

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseAliasingAutomatically')

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
	def AutoConfigureEsImport(self):
		"""Auto Configure ES-Import

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoConfigureEsImport')

	@property
	def BMacPrefix(self):
		"""B-MAC Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bMacPrefix')

	@property
	def BMacPrefixLength(self):
		"""B-MAC Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bMacPrefixLength')

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
	def DfElectionTimer(self):
		"""DF Election Timer(s)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dfElectionTimer')

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
	def EnableSingleActive(self):
		"""Enable Single-Active

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableSingleActive')

	@property
	def EnableStickyStaticFlag(self):
		"""Enable B-MAC Sticky/Static Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableStickyStaticFlag')

	@property
	def EsImport(self):
		"""ES Import

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('esImport')

	@property
	def EsiLabel(self):
		"""ESI Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('esiLabel')

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
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('esiValue')

	@property
	def EvisCount(self):
		"""Number of EVIs

		Returns:
			number
		"""
		return self._get_attribute('evisCount')
	@EvisCount.setter
	def EvisCount(self, value):
		self._set_attribute('evisCount', value)

	@property
	def IncludeMacMobilityExtendedCommunity(self):
		"""Include MAC Mobility Extended Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMacMobilityExtendedCommunity')

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
	def NoOfbMacMappedIpsV4(self):
		"""Number of B-MAC Mapped IPs

		Returns:
			number
		"""
		return self._get_attribute('noOfbMacMappedIpsV4')
	@NoOfbMacMappedIpsV4.setter
	def NoOfbMacMappedIpsV4(self, value):
		self._set_attribute('noOfbMacMappedIpsV4', value)

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
	def SupportFastConvergence(self):
		"""Support Fast Convergence

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportFastConvergence')

	@property
	def SupportMultihomedEsAutoDiscovery(self):
		"""Support Multi-homed ES Auto Discovery

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportMultihomedEsAutoDiscovery')

	@property
	def UseControlWord(self):
		"""Use Control Word

		Returns:
			bool
		"""
		return self._get_attribute('useControlWord')
	@UseControlWord.setter
	def UseControlWord(self, value):
		self._set_attribute('useControlWord', value)

	@property
	def UseSameSequenceNumber(self):
		"""Use B-MAC Same Sequence Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useSameSequenceNumber')

	def get_device_ids(self, PortNames=None, AdvertiseAliasingBeforeAdPerEsRoute=None, AdvertiseInclusiveMulticastRoute=None, AliasingRouteGranularity=None, Active=None, AdvertiseAliasingAutomatically=None, AggregatorAs=None, AggregatorId=None, AsSetMode=None, AutoConfigureEsImport=None, BMacPrefix=None, BMacPrefixLength=None, DfElectionTimer=None, EnableAggregatorId=None, EnableAsPathSegments=None, EnableAtomicAggregate=None, EnableCluster=None, EnableCommunity=None, EnableExtendedCommunity=None, EnableLocalPreference=None, EnableMultiExitDiscriminator=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableSingleActive=None, EnableStickyStaticFlag=None, EsImport=None, EsiLabel=None, EsiType=None, EsiValue=None, IncludeMacMobilityExtendedCommunity=None, Ipv4NextHop=None, Ipv6NextHop=None, LocalPreference=None, MultiExitDiscriminator=None, Origin=None, OriginatorId=None, OverridePeerAsSetMode=None, SetNextHop=None, SetNextHopIpType=None, SupportFastConvergence=None, SupportMultihomedEsAutoDiscovery=None, UseSameSequenceNumber=None):
		"""Base class infrastructure that gets a list of bgpEthernetSegmentV4 device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AdvertiseAliasingBeforeAdPerEsRoute (str): optional regex of AdvertiseAliasingBeforeAdPerEsRoute
			AdvertiseInclusiveMulticastRoute (str): optional regex of AdvertiseInclusiveMulticastRoute
			AliasingRouteGranularity (str): optional regex of AliasingRouteGranularity
			Active (str): optional regex of active
			AdvertiseAliasingAutomatically (str): optional regex of advertiseAliasingAutomatically
			AggregatorAs (str): optional regex of aggregatorAs
			AggregatorId (str): optional regex of aggregatorId
			AsSetMode (str): optional regex of asSetMode
			AutoConfigureEsImport (str): optional regex of autoConfigureEsImport
			BMacPrefix (str): optional regex of bMacPrefix
			BMacPrefixLength (str): optional regex of bMacPrefixLength
			DfElectionTimer (str): optional regex of dfElectionTimer
			EnableAggregatorId (str): optional regex of enableAggregatorId
			EnableAsPathSegments (str): optional regex of enableAsPathSegments
			EnableAtomicAggregate (str): optional regex of enableAtomicAggregate
			EnableCluster (str): optional regex of enableCluster
			EnableCommunity (str): optional regex of enableCommunity
			EnableExtendedCommunity (str): optional regex of enableExtendedCommunity
			EnableLocalPreference (str): optional regex of enableLocalPreference
			EnableMultiExitDiscriminator (str): optional regex of enableMultiExitDiscriminator
			EnableNextHop (str): optional regex of enableNextHop
			EnableOrigin (str): optional regex of enableOrigin
			EnableOriginatorId (str): optional regex of enableOriginatorId
			EnableSingleActive (str): optional regex of enableSingleActive
			EnableStickyStaticFlag (str): optional regex of enableStickyStaticFlag
			EsImport (str): optional regex of esImport
			EsiLabel (str): optional regex of esiLabel
			EsiType (str): optional regex of esiType
			EsiValue (str): optional regex of esiValue
			IncludeMacMobilityExtendedCommunity (str): optional regex of includeMacMobilityExtendedCommunity
			Ipv4NextHop (str): optional regex of ipv4NextHop
			Ipv6NextHop (str): optional regex of ipv6NextHop
			LocalPreference (str): optional regex of localPreference
			MultiExitDiscriminator (str): optional regex of multiExitDiscriminator
			Origin (str): optional regex of origin
			OriginatorId (str): optional regex of originatorId
			OverridePeerAsSetMode (str): optional regex of overridePeerAsSetMode
			SetNextHop (str): optional regex of setNextHop
			SetNextHopIpType (str): optional regex of setNextHopIpType
			SupportFastConvergence (str): optional regex of supportFastConvergence
			SupportMultihomedEsAutoDiscovery (str): optional regex of supportMultihomedEsAutoDiscovery
			UseSameSequenceNumber (str): optional regex of useSameSequenceNumber

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def AdvertiseAdPerEsRoute(self, Arg2):
		"""Executes the advertiseAdPerEsRoute operation on the server.

		Advertise AD per ES Route.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AdvertiseAdPerEsRoute', payload=locals(), response_object=None)

	def FlushRemoteCMACForwardingTable(self):
		"""Executes the flushRemoteCMACForwardingTable operation on the server.

		Flush Remote CMAC Forwarding Table

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('FlushRemoteCMACForwardingTable', payload=locals(), response_object=None)

	def FlushRemoteCMACForwardingTable(self, SessionIndices):
		"""Executes the flushRemoteCMACForwardingTable operation on the server.

		Flush Remote CMAC Forwarding Table

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('FlushRemoteCMACForwardingTable', payload=locals(), response_object=None)

	def FlushRemoteCMACForwardingTable(self, SessionIndices):
		"""Executes the flushRemoteCMACForwardingTable operation on the server.

		Flush Remote CMAC Forwarding Table

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('FlushRemoteCMACForwardingTable', payload=locals(), response_object=None)

	def FlushRemoteCMACForwardingTable(self, Arg2):
		"""Executes the flushRemoteCMACForwardingTable operation on the server.

		Flush Remote CMAC Forwarding Table.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FlushRemoteCMACForwardingTable', payload=locals(), response_object=None)

	def WithdrawAdPerEsRoute(self, Arg2):
		"""Executes the withdrawAdPerEsRoute operation on the server.

		Withdraw AD per ES Route.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('WithdrawAdPerEsRoute', payload=locals(), response_object=None)
