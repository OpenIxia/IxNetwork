
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


class BgpFlowSpecRangesListV4(Base):
	"""The BgpFlowSpecRangesListV4 class encapsulates a required bgpFlowSpecRangesListV4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpFlowSpecRangesListV4 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpFlowSpecRangesListV4'

	def __init__(self, parent):
		super(BgpFlowSpecRangesListV4, self).__init__(parent)

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
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def AsNumber2Bytes(self):
		"""AS 2-Bytes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber2Bytes')

	@property
	def AsNumber4Bytes(self):
		"""AS 4-Bytes

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber4Bytes')

	@property
	def AsSetMode(self):
		"""AS# Set Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asSetMode')

	@property
	def AssignedNumber2Bytes(self):
		"""Assigned Number(2 Octets)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('assignedNumber2Bytes')

	@property
	def AssignedNumber4Bytes(self):
		"""Assigned Number(4 Octets)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('assignedNumber4Bytes')

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
	def DestPortMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-300&!250|>=500 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destPortMatch')

	@property
	def DestPrefixLengthV4(self):
		"""Destination Prefix Length (bits) - Controlled by Enable Destination Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destPrefixLengthV4')

	@property
	def DestPrefixV4(self):
		"""Destination Prefix - Controlled by Enable Destination Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destPrefixV4')

	@property
	def DscpMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 10, 10-20, <10, 10&20, 10|20-30&!25|>=50 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dscpMatch')

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
	def EnableDestPrefixV4(self):
		"""Click to Enable Destination Prefix and Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDestPrefixV4')

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
	def EnableRedirect(self):
		"""Enable Redirect

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRedirect')

	@property
	def EnableSourcePrefixV4(self):
		"""Click to Enable Source Prefix and Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableSourcePrefixV4')

	@property
	def EnableTrafficAction(self):
		"""Enable Traffic Action

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableTrafficAction')

	@property
	def EnableTrafficMarketing(self):
		"""Enable Traffic Marketing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableTrafficMarketing')

	@property
	def EnableTrafficMarking(self):
		"""Enable Traffic Marking

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableTrafficMarking')

	@property
	def EnableTrafficRate(self):
		"""Enable Traffic Rate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableTrafficRate')

	@property
	def FlowSpecName(self):
		"""Flow Spec Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowSpecName')

	@property
	def FragmentMatch(self):
		"""Supported Flags: lf,ff,isf,df join different matchcriteria using | or & join flags using | (bitwise or) Eg. (lf), (lf|ff|isf|df), (not)(lf|isf), (not|match)(df|ff)|(isf|lf) Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fragmentMatch')

	@property
	def IcmpCodeMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-220&!210|>=230 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('icmpCodeMatch')

	@property
	def IcmpTypeMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-220&!210|>=230 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('icmpTypeMatch')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def IpPacketLenMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-300&!250|>=500 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipPacketLenMatch')

	@property
	def IpProto(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-220&!210|>=230 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipProto')

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
	def NumberOfFlows(self):
		"""Number of Flows in a Flow Range

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfFlows')

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
	def PortMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-300&!250|>=500 etc Keep Empty If Not Requried This Field Matches Source OR Destination TCP/UDP Ports

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portMatch')

	@property
	def RedirectCBit(self):
		"""C Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redirectCBit')

	@property
	def RedirectExtCommunityType(self):
		"""Extended Community Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redirectExtCommunityType')

	@property
	def Redirectnexthop(self):
		"""Next Hop

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redirectnexthop')

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
	def SourcePortMatch(self):
		"""Supported Formats: value value1-value2 >value (!, >, <, >=, <= supported) join using | or & Eg. 100, 100-200, <100, 100&200, 100|200-300&!250|>=500 etc Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourcePortMatch')

	@property
	def SourcePrefixLengthV4(self):
		"""Source Prefix Length (bits) - Controlled by Enable Source Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourcePrefixLengthV4')

	@property
	def SourcePrefixV4(self):
		"""Source Prefix - Controlled by Enable Source Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourcePrefixV4')

	@property
	def TcpFlagsMatch(self):
		"""Supported Flags: ns,cwr,ece,urg,ack,psh,rst,syn,fin join different matchcriteria using | or & join flags using | (bitwise or) Eg. (cwr), (ece|urg|psh|syn), (not)(cwr|syn), (not|match)(ece|psh)|(psh|rst)&(not)(ns) Keep Empty If Not Requried

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tcpFlagsMatch')

	@property
	def TerminalAction(self):
		"""Terminal Action

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('terminalAction')

	@property
	def TrafficActionSample(self):
		"""Sample

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('trafficActionSample')

	@property
	def TrafficDscp(self):
		"""DSCP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('trafficDscp')

	@property
	def TrafficRate(self):
		"""Traffic Rate (Bytes/s)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('trafficRate')

	def get_device_ids(self, PortNames=None, Active=None, AggregatorAs=None, AggregatorId=None, AsNumber2Bytes=None, AsNumber4Bytes=None, AsSetMode=None, AssignedNumber2Bytes=None, AssignedNumber4Bytes=None, DestPortMatch=None, DestPrefixLengthV4=None, DestPrefixV4=None, DscpMatch=None, EnableAggregatorId=None, EnableAsPathSegments=None, EnableAtomicAggregate=None, EnableCluster=None, EnableCommunity=None, EnableDestPrefixV4=None, EnableExtendedCommunity=None, EnableLocalPreference=None, EnableMultiExitDiscriminator=None, EnableNextHop=None, EnableOrigin=None, EnableOriginatorId=None, EnableRedirect=None, EnableSourcePrefixV4=None, EnableTrafficAction=None, EnableTrafficMarketing=None, EnableTrafficMarking=None, EnableTrafficRate=None, FlowSpecName=None, FragmentMatch=None, IcmpCodeMatch=None, IcmpTypeMatch=None, Ip=None, IpPacketLenMatch=None, IpProto=None, Ipv4NextHop=None, Ipv6NextHop=None, LocalPreference=None, MultiExitDiscriminator=None, NumberOfFlows=None, Origin=None, OriginatorId=None, OverridePeerAsSetMode=None, PortMatch=None, RedirectCBit=None, RedirectExtCommunityType=None, Redirectnexthop=None, SetNextHop=None, SetNextHopIpType=None, SourcePortMatch=None, SourcePrefixLengthV4=None, SourcePrefixV4=None, TcpFlagsMatch=None, TerminalAction=None, TrafficActionSample=None, TrafficDscp=None, TrafficRate=None):
		"""Base class infrastructure that gets a list of bgpFlowSpecRangesListV4 device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AggregatorAs (str): optional regex of aggregatorAs
			AggregatorId (str): optional regex of aggregatorId
			AsNumber2Bytes (str): optional regex of asNumber2Bytes
			AsNumber4Bytes (str): optional regex of asNumber4Bytes
			AsSetMode (str): optional regex of asSetMode
			AssignedNumber2Bytes (str): optional regex of assignedNumber2Bytes
			AssignedNumber4Bytes (str): optional regex of assignedNumber4Bytes
			DestPortMatch (str): optional regex of destPortMatch
			DestPrefixLengthV4 (str): optional regex of destPrefixLengthV4
			DestPrefixV4 (str): optional regex of destPrefixV4
			DscpMatch (str): optional regex of dscpMatch
			EnableAggregatorId (str): optional regex of enableAggregatorId
			EnableAsPathSegments (str): optional regex of enableAsPathSegments
			EnableAtomicAggregate (str): optional regex of enableAtomicAggregate
			EnableCluster (str): optional regex of enableCluster
			EnableCommunity (str): optional regex of enableCommunity
			EnableDestPrefixV4 (str): optional regex of enableDestPrefixV4
			EnableExtendedCommunity (str): optional regex of enableExtendedCommunity
			EnableLocalPreference (str): optional regex of enableLocalPreference
			EnableMultiExitDiscriminator (str): optional regex of enableMultiExitDiscriminator
			EnableNextHop (str): optional regex of enableNextHop
			EnableOrigin (str): optional regex of enableOrigin
			EnableOriginatorId (str): optional regex of enableOriginatorId
			EnableRedirect (str): optional regex of enableRedirect
			EnableSourcePrefixV4 (str): optional regex of enableSourcePrefixV4
			EnableTrafficAction (str): optional regex of enableTrafficAction
			EnableTrafficMarketing (str): optional regex of enableTrafficMarketing
			EnableTrafficMarking (str): optional regex of enableTrafficMarking
			EnableTrafficRate (str): optional regex of enableTrafficRate
			FlowSpecName (str): optional regex of flowSpecName
			FragmentMatch (str): optional regex of fragmentMatch
			IcmpCodeMatch (str): optional regex of icmpCodeMatch
			IcmpTypeMatch (str): optional regex of icmpTypeMatch
			Ip (str): optional regex of ip
			IpPacketLenMatch (str): optional regex of ipPacketLenMatch
			IpProto (str): optional regex of ipProto
			Ipv4NextHop (str): optional regex of ipv4NextHop
			Ipv6NextHop (str): optional regex of ipv6NextHop
			LocalPreference (str): optional regex of localPreference
			MultiExitDiscriminator (str): optional regex of multiExitDiscriminator
			NumberOfFlows (str): optional regex of numberOfFlows
			Origin (str): optional regex of origin
			OriginatorId (str): optional regex of originatorId
			OverridePeerAsSetMode (str): optional regex of overridePeerAsSetMode
			PortMatch (str): optional regex of portMatch
			RedirectCBit (str): optional regex of redirectCBit
			RedirectExtCommunityType (str): optional regex of redirectExtCommunityType
			Redirectnexthop (str): optional regex of redirectnexthop
			SetNextHop (str): optional regex of setNextHop
			SetNextHopIpType (str): optional regex of setNextHopIpType
			SourcePortMatch (str): optional regex of sourcePortMatch
			SourcePrefixLengthV4 (str): optional regex of sourcePrefixLengthV4
			SourcePrefixV4 (str): optional regex of sourcePrefixV4
			TcpFlagsMatch (str): optional regex of tcpFlagsMatch
			TerminalAction (str): optional regex of terminalAction
			TrafficActionSample (str): optional regex of trafficActionSample
			TrafficDscp (str): optional regex of trafficDscp
			TrafficRate (str): optional regex of trafficRate

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
