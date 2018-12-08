
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


class RequestedLsps(Base):
	"""The RequestedLsps class encapsulates a required requestedLsps node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RequestedLsps property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'requestedLsps'

	def __init__(self, parent):
		super(RequestedLsps, self).__init__(parent)

	@property
	def PccRequestedMetricSubObjectsList(self):
		"""An instance of the PccRequestedMetricSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pccrequestedmetricsubobjectslist.PccRequestedMetricSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pccrequestedmetricsubobjectslist import PccRequestedMetricSubObjectsList
		return PccRequestedMetricSubObjectsList(self)

	@property
	def PcepIroSubObjectsList(self):
		"""An instance of the PcepIroSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepirosubobjectslist.PcepIroSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepirosubobjectslist import PcepIroSubObjectsList
		return PcepIroSubObjectsList(self)

	@property
	def PcepXroSubObjectsList(self):
		"""An instance of the PcepXroSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepxrosubobjectslist.PcepXroSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepxrosubobjectslist import PcepXroSubObjectsList
		return PcepXroSubObjectsList(self)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ActiveDataTrafficEndPoints(self):
		"""Specifies whether that specific Data Traffic Endpoint will generate data traffic

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('activeDataTrafficEndPoints')

	@property
	def Bandwidth(self):
		"""Bandwidth (bits/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

	@property
	def BiDirectional(self):
		"""Bi-directional

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('biDirectional')

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
	def DestinationIpv4Address(self):
		"""Destination IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destinationIpv4Address')

	@property
	def DestinationIpv6Address(self):
		"""Destination IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destinationIpv6Address')

	@property
	def ExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

	@property
	def FailBit(self):
		"""Fail Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('failBit')

	@property
	def HoldingPriority(self):
		"""Holding Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('holdingPriority')

	@property
	def IncludeAll(self):
		"""Include All

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAll')

	@property
	def IncludeAny(self):
		"""Include Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAny')

	@property
	def IncludeBandwidth(self):
		"""Include Bandwidth

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeBandwidth')

	@property
	def IncludeEndPoints(self):
		"""Include End Points

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeEndPoints')

	@property
	def IncludeIro(self):
		"""Include IRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeIro')

	@property
	def IncludeLsp(self):
		"""Include LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLsp')

	@property
	def IncludeLspa(self):
		"""Include LSPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLspa')

	@property
	def IncludeMetric(self):
		"""Include Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMetric')

	@property
	def IncludeRp(self):
		"""Include RP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeRp')

	@property
	def IncludeSymbolicPathNameTlv(self):
		"""Include Symbolic Path Name TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSymbolicPathNameTlv')

	@property
	def IncludeXro(self):
		"""Include XRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeXro')

	@property
	def InitialDelegation(self):
		"""Initial Delegation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initialDelegation')

	@property
	def InsertIpv6ExplicitNull(self):
		"""Insert IPv6 Explicit Null MPLS header if the traffic type is of type IPv6

		Returns:
			bool
		"""
		return self._get_attribute('insertIpv6ExplicitNull')
	@InsertIpv6ExplicitNull.setter
	def InsertIpv6ExplicitNull(self, value):
		self._set_attribute('insertIpv6ExplicitNull', value)

	@property
	def IpVersion(self):
		"""IP Version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipVersion')

	@property
	def LocalProtection(self):
		"""Local Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

	@property
	def Loose(self):
		"""Loose

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('loose')

	@property
	def LspDelegationState(self):
		"""LSP Delegation State

		Returns:
			list(str[delegated|delegationConfirmed|delegationRejected|delegationReturned|delegationRevoked|nonDelegated|none])
		"""
		return self._get_attribute('lspDelegationState')

	@property
	def MaxExpectedSegmentCount(self):
		"""This control is used to set the maximum Segment count/ MPLS labels that would be present in the generted traffic.

		Returns:
			number
		"""
		return self._get_attribute('maxExpectedSegmentCount')
	@MaxExpectedSegmentCount.setter
	def MaxExpectedSegmentCount(self, value):
		self._set_attribute('maxExpectedSegmentCount', value)

	@property
	def MaxNoOfIroSubObjects(self):
		"""Max Number of IRO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('maxNoOfIroSubObjects')
	@MaxNoOfIroSubObjects.setter
	def MaxNoOfIroSubObjects(self, value):
		self._set_attribute('maxNoOfIroSubObjects', value)

	@property
	def MaxNoOfXroSubObjects(self):
		"""Max Number of XRO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('maxNoOfXroSubObjects')
	@MaxNoOfXroSubObjects.setter
	def MaxNoOfXroSubObjects(self, value):
		self._set_attribute('maxNoOfXroSubObjects', value)

	@property
	def MaxNumberOfMetrics(self):
		"""Max Number of Metrics

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfMetrics')
	@MaxNumberOfMetrics.setter
	def MaxNumberOfMetrics(self, value):
		self._set_attribute('maxNumberOfMetrics', value)

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
	def OverridePlspId(self):
		"""Override PLSP-ID

		Returns:
			bool
		"""
		return self._get_attribute('overridePlspId')
	@OverridePlspId.setter
	def OverridePlspId(self, value):
		self._set_attribute('overridePlspId', value)

	@property
	def OverrideRequestId(self):
		"""Override Request ID

		Returns:
			bool
		"""
		return self._get_attribute('overrideRequestId')
	@OverrideRequestId.setter
	def OverrideRequestId(self, value):
		self._set_attribute('overrideRequestId', value)

	@property
	def OverrideSourceAddress(self):
		"""Override Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overrideSourceAddress')

	@property
	def PFlagBandwidth(self):
		"""Bandwidth P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlagBandwidth')

	@property
	def PFlagIro(self):
		"""IRO P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlagIro')

	@property
	def PFlagLsp(self):
		"""LSP P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlagLsp')

	@property
	def PFlagLspa(self):
		"""LSPA P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlagLspa')

	@property
	def PFlagRp(self):
		"""RP P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlagRp')

	@property
	def PFlagXro(self):
		"""XRO P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlagXro')

	@property
	def PflagEndpoints(self):
		"""End Points P Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pflagEndpoints')

	@property
	def PlspId(self):
		"""An identifier for the LSP. A PCC creates a unique PLSP-ID for each LSP that is constant for the lifetime of a PCEP session. The PCC will advertise the same PLSP-ID on all PCEP sessions it maintains at a given time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('plspId')

	@property
	def Priority(self):
		"""Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priority')

	@property
	def ReDelegationTimerStatus(self):
		"""Re-Delegation Timer Status

		Returns:
			list(str[expired|none|notStarted|running|stopped])
		"""
		return self._get_attribute('reDelegationTimerStatus')

	@property
	def ReOptimization(self):
		"""Re-optimization

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reOptimization')

	@property
	def RedelegationTimeoutInterval(self):
		"""The period of time a PCC waits for, when a PCEP session is terminated, before revoking LSP delegation to a PCE and attempting to redelegate LSPs associated with the terminated PCEP session to PCE.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redelegationTimeoutInterval')

	@property
	def RequestId(self):
		"""Request ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestId')

	@property
	def SetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SourceEndPointIPv4(self):
		"""Source IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceEndPointIPv4')

	@property
	def SourceEndPointIPv6(self):
		"""Source IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceEndPointIPv6')

	@property
	def SourceIpv4Address(self):
		"""Source IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv4Address')

	@property
	def SourceIpv6Address(self):
		"""Source IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv6Address')

	@property
	def SymbolicPathName(self):
		"""Symbolic Path Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('symbolicPathName')

	def get_device_ids(self, PortNames=None, Active=None, ActiveDataTrafficEndPoints=None, Bandwidth=None, BiDirectional=None, DestinationIpv4Address=None, DestinationIpv6Address=None, ExcludeAny=None, FailBit=None, HoldingPriority=None, IncludeAll=None, IncludeAny=None, IncludeBandwidth=None, IncludeEndPoints=None, IncludeIro=None, IncludeLsp=None, IncludeLspa=None, IncludeMetric=None, IncludeRp=None, IncludeSymbolicPathNameTlv=None, IncludeXro=None, InitialDelegation=None, IpVersion=None, LocalProtection=None, Loose=None, OverrideSourceAddress=None, PFlagBandwidth=None, PFlagIro=None, PFlagLsp=None, PFlagLspa=None, PFlagRp=None, PFlagXro=None, PflagEndpoints=None, PlspId=None, Priority=None, ReOptimization=None, RedelegationTimeoutInterval=None, RequestId=None, SetupPriority=None, SourceEndPointIPv4=None, SourceEndPointIPv6=None, SourceIpv4Address=None, SourceIpv6Address=None, SymbolicPathName=None):
		"""Base class infrastructure that gets a list of requestedLsps device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			ActiveDataTrafficEndPoints (str): optional regex of activeDataTrafficEndPoints
			Bandwidth (str): optional regex of bandwidth
			BiDirectional (str): optional regex of biDirectional
			DestinationIpv4Address (str): optional regex of destinationIpv4Address
			DestinationIpv6Address (str): optional regex of destinationIpv6Address
			ExcludeAny (str): optional regex of excludeAny
			FailBit (str): optional regex of failBit
			HoldingPriority (str): optional regex of holdingPriority
			IncludeAll (str): optional regex of includeAll
			IncludeAny (str): optional regex of includeAny
			IncludeBandwidth (str): optional regex of includeBandwidth
			IncludeEndPoints (str): optional regex of includeEndPoints
			IncludeIro (str): optional regex of includeIro
			IncludeLsp (str): optional regex of includeLsp
			IncludeLspa (str): optional regex of includeLspa
			IncludeMetric (str): optional regex of includeMetric
			IncludeRp (str): optional regex of includeRp
			IncludeSymbolicPathNameTlv (str): optional regex of includeSymbolicPathNameTlv
			IncludeXro (str): optional regex of includeXro
			InitialDelegation (str): optional regex of initialDelegation
			IpVersion (str): optional regex of ipVersion
			LocalProtection (str): optional regex of localProtection
			Loose (str): optional regex of loose
			OverrideSourceAddress (str): optional regex of overrideSourceAddress
			PFlagBandwidth (str): optional regex of pFlagBandwidth
			PFlagIro (str): optional regex of pFlagIro
			PFlagLsp (str): optional regex of pFlagLsp
			PFlagLspa (str): optional regex of pFlagLspa
			PFlagRp (str): optional regex of pFlagRp
			PFlagXro (str): optional regex of pFlagXro
			PflagEndpoints (str): optional regex of pflagEndpoints
			PlspId (str): optional regex of plspId
			Priority (str): optional regex of priority
			ReOptimization (str): optional regex of reOptimization
			RedelegationTimeoutInterval (str): optional regex of redelegationTimeoutInterval
			RequestId (str): optional regex of requestId
			SetupPriority (str): optional regex of setupPriority
			SourceEndPointIPv4 (str): optional regex of sourceEndPointIPv4
			SourceEndPointIPv6 (str): optional regex of sourceEndPointIPv6
			SourceIpv4Address (str): optional regex of sourceIpv4Address
			SourceIpv6Address (str): optional regex of sourceIpv6Address
			SymbolicPathName (str): optional regex of symbolicPathName

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def Delegate(self, Arg2):
		"""Executes the delegate operation on the server.

		Delegate

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Delegate', payload=locals(), response_object=None)

	def RevokeDelegation(self, Arg2):
		"""Executes the revokeDelegation operation on the server.

		Revoke Delegation

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RevokeDelegation', payload=locals(), response_object=None)
