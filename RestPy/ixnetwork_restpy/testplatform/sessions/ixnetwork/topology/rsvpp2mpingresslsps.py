
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


class RsvpP2mpIngressLsps(Base):
	"""The RsvpP2mpIngressLsps class encapsulates a required rsvpP2mpIngressLsps node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpP2mpIngressLsps property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rsvpP2mpIngressLsps'

	def __init__(self, parent):
		super(RsvpP2mpIngressLsps, self).__init__(parent)

	@property
	def RsvpDetourSubObjectsList(self):
		"""An instance of the RsvpDetourSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpdetoursubobjectslist.RsvpDetourSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpdetoursubobjectslist import RsvpDetourSubObjectsList
		return RsvpDetourSubObjectsList(self)

	@property
	def RsvpIngressRroSubObjectsList(self):
		"""An instance of the RsvpIngressRroSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpingressrrosubobjectslist.RsvpIngressRroSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpingressrrosubobjectslist import RsvpIngressRroSubObjectsList
		return RsvpIngressRroSubObjectsList(self)

	@property
	def RsvpP2mpIngressSubLsps(self):
		"""An instance of the RsvpP2mpIngressSubLsps class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpp2mpingresssublsps.RsvpP2mpIngressSubLsps)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpp2mpingresssublsps import RsvpP2mpIngressSubLsps
		return RsvpP2mpIngressSubLsps(self)._select()

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
	def AutoGenerateSessionName(self):
		"""Auto Generate Session Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoGenerateSessionName')

	@property
	def BackupLspId(self):
		"""Backup LSP Id Pool Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspId')

	@property
	def BandwidthProtectionDesired(self):
		"""Bandwidth Protection Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtectionDesired')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DelayLspSwitchOver(self):
		"""Delay LSP switch over

		Returns:
			bool
		"""
		return self._get_attribute('delayLspSwitchOver')
	@DelayLspSwitchOver.setter
	def DelayLspSwitchOver(self, value):
		self._set_attribute('delayLspSwitchOver', value)

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnableFastReroute(self):
		"""Enable Fast Reroute

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFastReroute')

	@property
	def EnablePathReOptimization(self):
		"""Enable Path Re-Optimization

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePathReOptimization')

	@property
	def EnablePeriodicReEvaluationRequest(self):
		"""Enable Periodic Re-Evaluation Request

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePeriodicReEvaluationRequest')

	@property
	def ExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

	@property
	def FacilityBackupDesired(self):
		"""Facility Backup Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('facilityBackupDesired')

	@property
	def FastRerouteBandwidth(self):
		"""Bandwidth (bps)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fastRerouteBandwidth')

	@property
	def FastRerouteExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fastRerouteExcludeAny')

	@property
	def FastRerouteHoldingPriority(self):
		"""Holding Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fastRerouteHoldingPriority')

	@property
	def FastRerouteIncludeAll(self):
		"""Include All

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fastRerouteIncludeAll')

	@property
	def FastRerouteIncludeAny(self):
		"""Include Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fastRerouteIncludeAny')

	@property
	def FastRerouteSetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fastRerouteSetupPriority')

	@property
	def HoldingPriority(self):
		"""Holding Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('holdingPriority')

	@property
	def HopLimit(self):
		"""Hop Limit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hopLimit')

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
	def IncludeConnectedIpOnTop(self):
		"""Include connected IP on top

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeConnectedIpOnTop')

	@property
	def IncludeHeadIpAtBottom(self):
		"""Include Head IP at bottom

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeHeadIpAtBottom')

	@property
	def IngressP2mpSubLspRanges(self):
		"""Number of P2MP Ingress Sub LSPs configured per RSVP-TE P2MP Ingress LSP

		Returns:
			number
		"""
		return self._get_attribute('ingressP2mpSubLspRanges')
	@IngressP2mpSubLspRanges.setter
	def IngressP2mpSubLspRanges(self, value):
		self._set_attribute('ingressP2mpSubLspRanges', value)

	@property
	def InsertIPv6ExplicitNull(self):
		"""Insert IPv6 explicit NULL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('insertIPv6ExplicitNull')

	@property
	def LabelRecordingDesired(self):
		"""Label Recording Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelRecordingDesired')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

	@property
	def LocalProtectionDesired(self):
		"""Local Protection Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtectionDesired')

	@property
	def LspId(self):
		"""LSP Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspId')

	@property
	def LspSwitchOverDelayTime(self):
		"""LSP Switch Over Delay timer (sec)

		Returns:
			number
		"""
		return self._get_attribute('lspSwitchOverDelayTime')
	@LspSwitchOverDelayTime.setter
	def LspSwitchOverDelayTime(self, value):
		self._set_attribute('lspSwitchOverDelayTime', value)

	@property
	def MaximumPacketSize(self):
		"""Maximum Packet Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maximumPacketSize')

	@property
	def MinimumPolicedUnit(self):
		"""Minimum Policed Unit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minimumPolicedUnit')

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
	def NodeProtectionDesired(self):
		"""Node Protection Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtectionDesired')

	@property
	def NumberOfDetourSubObjects(self):
		"""Number Of Detour Sub-Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfDetourSubObjects')
	@NumberOfDetourSubObjects.setter
	def NumberOfDetourSubObjects(self, value):
		self._set_attribute('numberOfDetourSubObjects', value)

	@property
	def NumberOfRroSubObjects(self):
		"""Number Of RRO Sub-Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfRroSubObjects')
	@NumberOfRroSubObjects.setter
	def NumberOfRroSubObjects(self, value):
		self._set_attribute('numberOfRroSubObjects', value)

	@property
	def OneToOneBackupDesired(self):
		"""One To One Backup Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('oneToOneBackupDesired')

	@property
	def P2mpIdAsNumber(self):
		"""P2MP ID displayed in Integer format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('p2mpIdAsNumber')

	@property
	def P2mpIdIp(self):
		"""P2MP ID displayed in IP Address format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('p2mpIdIp')

	@property
	def PeakDataRate(self):
		"""Peak Data Rate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peakDataRate')

	@property
	def ReEvaluationRequestInterval(self):
		"""Re-Evaluation Request Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reEvaluationRequestInterval')

	@property
	def RefreshInterval(self):
		"""Refresh Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('refreshInterval')

	@property
	def ResourceAffinities(self):
		"""Resource Affinities

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('resourceAffinities')

	@property
	def SeStyleDesired(self):
		"""SE Style Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('seStyleDesired')

	@property
	def SendDetour(self):
		"""Send Detour

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendDetour')

	@property
	def SendRro(self):
		"""Send RRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendRro')

	@property
	def SessionName(self):
		"""Session Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sessionName')

	@property
	def SetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SourceIpv4(self):
		"""Source IPv4

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv4')

	@property
	def SourceIpv6(self):
		"""Source IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv6')

	@property
	def State(self):
		"""State

		Returns:
			list(str[down|none|notStarted|up])
		"""
		return self._get_attribute('state')

	@property
	def TimeoutMultiplier(self):
		"""Timeout Multiplier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutMultiplier')

	@property
	def TokenBucketRate(self):
		"""Token Bucket Rate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tokenBucketRate')

	@property
	def TokenBucketSize(self):
		"""Token Bucket Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tokenBucketSize')

	@property
	def TunnelId(self):
		"""Tunnel ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tunnelId')

	@property
	def TypeP2mpId(self):
		"""P2MP ID Type

		Returns:
			str(iP|p2MPId)
		"""
		return self._get_attribute('typeP2mpId')
	@TypeP2mpId.setter
	def TypeP2mpId(self, value):
		self._set_attribute('typeP2mpId', value)

	@property
	def UsingHeadendIp(self):
		"""Using Headend IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('usingHeadendIp')

	def get_device_ids(self, PortNames=None, Active=None, AutoGenerateSessionName=None, BackupLspId=None, BandwidthProtectionDesired=None, EnableFastReroute=None, EnablePathReOptimization=None, EnablePeriodicReEvaluationRequest=None, ExcludeAny=None, FacilityBackupDesired=None, FastRerouteBandwidth=None, FastRerouteExcludeAny=None, FastRerouteHoldingPriority=None, FastRerouteIncludeAll=None, FastRerouteIncludeAny=None, FastRerouteSetupPriority=None, HoldingPriority=None, HopLimit=None, IncludeAll=None, IncludeAny=None, IncludeConnectedIpOnTop=None, IncludeHeadIpAtBottom=None, InsertIPv6ExplicitNull=None, LabelRecordingDesired=None, LocalProtectionDesired=None, LspId=None, MaximumPacketSize=None, MinimumPolicedUnit=None, NodeProtectionDesired=None, OneToOneBackupDesired=None, P2mpIdAsNumber=None, P2mpIdIp=None, PeakDataRate=None, ReEvaluationRequestInterval=None, RefreshInterval=None, ResourceAffinities=None, SeStyleDesired=None, SendDetour=None, SendRro=None, SessionName=None, SetupPriority=None, SourceIpv4=None, SourceIpv6=None, TimeoutMultiplier=None, TokenBucketRate=None, TokenBucketSize=None, TunnelId=None, UsingHeadendIp=None):
		"""Base class infrastructure that gets a list of rsvpP2mpIngressLsps device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AutoGenerateSessionName (str): optional regex of autoGenerateSessionName
			BackupLspId (str): optional regex of backupLspId
			BandwidthProtectionDesired (str): optional regex of bandwidthProtectionDesired
			EnableFastReroute (str): optional regex of enableFastReroute
			EnablePathReOptimization (str): optional regex of enablePathReOptimization
			EnablePeriodicReEvaluationRequest (str): optional regex of enablePeriodicReEvaluationRequest
			ExcludeAny (str): optional regex of excludeAny
			FacilityBackupDesired (str): optional regex of facilityBackupDesired
			FastRerouteBandwidth (str): optional regex of fastRerouteBandwidth
			FastRerouteExcludeAny (str): optional regex of fastRerouteExcludeAny
			FastRerouteHoldingPriority (str): optional regex of fastRerouteHoldingPriority
			FastRerouteIncludeAll (str): optional regex of fastRerouteIncludeAll
			FastRerouteIncludeAny (str): optional regex of fastRerouteIncludeAny
			FastRerouteSetupPriority (str): optional regex of fastRerouteSetupPriority
			HoldingPriority (str): optional regex of holdingPriority
			HopLimit (str): optional regex of hopLimit
			IncludeAll (str): optional regex of includeAll
			IncludeAny (str): optional regex of includeAny
			IncludeConnectedIpOnTop (str): optional regex of includeConnectedIpOnTop
			IncludeHeadIpAtBottom (str): optional regex of includeHeadIpAtBottom
			InsertIPv6ExplicitNull (str): optional regex of insertIPv6ExplicitNull
			LabelRecordingDesired (str): optional regex of labelRecordingDesired
			LocalProtectionDesired (str): optional regex of localProtectionDesired
			LspId (str): optional regex of lspId
			MaximumPacketSize (str): optional regex of maximumPacketSize
			MinimumPolicedUnit (str): optional regex of minimumPolicedUnit
			NodeProtectionDesired (str): optional regex of nodeProtectionDesired
			OneToOneBackupDesired (str): optional regex of oneToOneBackupDesired
			P2mpIdAsNumber (str): optional regex of p2mpIdAsNumber
			P2mpIdIp (str): optional regex of p2mpIdIp
			PeakDataRate (str): optional regex of peakDataRate
			ReEvaluationRequestInterval (str): optional regex of reEvaluationRequestInterval
			RefreshInterval (str): optional regex of refreshInterval
			ResourceAffinities (str): optional regex of resourceAffinities
			SeStyleDesired (str): optional regex of seStyleDesired
			SendDetour (str): optional regex of sendDetour
			SendRro (str): optional regex of sendRro
			SessionName (str): optional regex of sessionName
			SetupPriority (str): optional regex of setupPriority
			SourceIpv4 (str): optional regex of sourceIpv4
			SourceIpv6 (str): optional regex of sourceIpv6
			TimeoutMultiplier (str): optional regex of timeoutMultiplier
			TokenBucketRate (str): optional regex of tokenBucketRate
			TokenBucketSize (str): optional regex of tokenBucketSize
			TunnelId (str): optional regex of tunnelId
			UsingHeadendIp (str): optional regex of usingHeadendIp

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def InitiateP2mpPathReoptimization(self):
		"""Executes the initiateP2mpPathReoptimization operation on the server.

		Send P2MP Path with re-evaluation request bit of SESSION-ATTRIBUTE object set, for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('InitiateP2mpPathReoptimization', payload=locals(), response_object=None)

	def InitiateP2mpPathReoptimization(self, SessionIndices):
		"""Executes the initiateP2mpPathReoptimization operation on the server.

		Send P2MP Path with re-evaluation request bit of SESSION-ATTRIBUTE object set, for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('InitiateP2mpPathReoptimization', payload=locals(), response_object=None)

	def InitiateP2mpPathReoptimization(self, SessionIndices):
		"""Executes the initiateP2mpPathReoptimization operation on the server.

		Send P2MP Path with re-evaluation request bit of SESSION-ATTRIBUTE object set, for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('InitiateP2mpPathReoptimization', payload=locals(), response_object=None)

	def InitiatePathReoptimization(self, Arg2):
		"""Executes the initiatePathReoptimization operation on the server.

		Initiate Path Reoptimization

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
		return self._execute('InitiatePathReoptimization', payload=locals(), response_object=None)

	def MakeBeforeBreak(self, Arg2):
		"""Executes the makeBeforeBreak operation on the server.

		Make Before Break

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
		return self._execute('MakeBeforeBreak', payload=locals(), response_object=None)

	def P2mpMakeBeforeBreak(self):
		"""Executes the p2mpMakeBeforeBreak operation on the server.

		Initiate P2MP Make Before Break for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('P2mpMakeBeforeBreak', payload=locals(), response_object=None)

	def P2mpMakeBeforeBreak(self, SessionIndices):
		"""Executes the p2mpMakeBeforeBreak operation on the server.

		Initiate P2MP Make Before Break for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('P2mpMakeBeforeBreak', payload=locals(), response_object=None)

	def P2mpMakeBeforeBreak(self, SessionIndices):
		"""Executes the p2mpMakeBeforeBreak operation on the server.

		Initiate P2MP Make Before Break for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('P2mpMakeBeforeBreak', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Activate/Enable P2MP Tunnel selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable P2MP Tunnel selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable P2MP Tunnel selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		Start

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
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Deactivate/Disable P2MP selected Tunnel Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable P2MP selected Tunnel Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable P2MP selected Tunnel Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		Stop

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
		return self._execute('Stop', payload=locals(), response_object=None)
