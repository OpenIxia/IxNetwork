from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RsvpP2PIngressLsps(Base):
	"""The RsvpP2PIngressLsps class encapsulates a required rsvpP2PIngressLsps node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpP2PIngressLsps property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rsvpP2PIngressLsps'

	def __init__(self, parent):
		super(RsvpP2PIngressLsps, self).__init__(parent)

	@property
	def BackupLspEROSubObjectsList(self):
		"""An instance of the BackupLspEROSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.backuplsperosubobjectslist.BackupLspEROSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.backuplsperosubobjectslist import BackupLspEROSubObjectsList
		return BackupLspEROSubObjectsList(self)

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
	def RsvpEROSubObjectsList(self):
		"""An instance of the RsvpEROSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvperosubobjectslist.RsvpEROSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvperosubobjectslist import RsvpEROSubObjectsList
		return RsvpEROSubObjectsList(self)

	@property
	def RsvpIngressRROSubObjectsList(self):
		"""An instance of the RsvpIngressRROSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpingressrrosubobjectslist.RsvpIngressRROSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvpingressrrosubobjectslist import RsvpIngressRROSubObjectsList
		return RsvpIngressRROSubObjectsList(self)

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
	def AssociationId(self):
		"""The Association ID of this LSP.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('associationId')

	@property
	def AutoGenerateSessionName(self):
		"""Auto Generate Session Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoGenerateSessionName')

	@property
	def AutorouteTraffic(self):
		"""Autoroute Traffic

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autorouteTraffic')

	@property
	def BackupLspEnableEro(self):
		"""Enable ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspEnableEro')

	@property
	def BackupLspId(self):
		"""Backup LSP Id Pool Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspId')

	@property
	def BackupLspMaximumPacketSize(self):
		"""Maximum Packet Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspMaximumPacketSize')

	@property
	def BackupLspMinimumPolicedUnit(self):
		"""Minimum Policed Unit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspMinimumPolicedUnit')

	@property
	def BackupLspNumberOfEroSubObjects(self):
		"""Number Of ERO Sub-Objects

		Returns:
			number
		"""
		return self._get_attribute('backupLspNumberOfEroSubObjects')
	@BackupLspNumberOfEroSubObjects.setter
	def BackupLspNumberOfEroSubObjects(self, value):
		self._set_attribute('backupLspNumberOfEroSubObjects', value)

	@property
	def BackupLspPeakDataRate(self):
		"""Peak Data Rate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspPeakDataRate')

	@property
	def BackupLspPrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspPrefixLength')

	@property
	def BackupLspPrependDutToEro(self):
		"""Prepend DUT to ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspPrependDutToEro')

	@property
	def BackupLspTokenBucketRate(self):
		"""Token Bucket Rate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspTokenBucketRate')

	@property
	def BackupLspTokenBucketSize(self):
		"""Token Bucket Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupLspTokenBucketSize')

	@property
	def Bandwidth(self):
		"""Bandwidth (bps)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

	@property
	def BandwidthProtectionDesired(self):
		"""Bandwidth Protection Desired

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtectionDesired')

	@property
	def ConfigureSyncLspObject(self):
		"""Include Objects

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureSyncLspObject')

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
	def DoMBBOnApplyChanges(self):
		"""Do Make Before Break on Apply Changes

		Returns:
			bool
		"""
		return self._get_attribute('doMBBOnApplyChanges')
	@DoMBBOnApplyChanges.setter
	def DoMBBOnApplyChanges(self, value):
		self._set_attribute('doMBBOnApplyChanges', value)

	@property
	def EnableBfdMpls(self):
		"""If selected, BFD MPLS is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBfdMpls')

	@property
	def EnableEro(self):
		"""Enable ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEro')

	@property
	def EnableFastReroute(self):
		"""Enable Fast Reroute

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFastReroute')

	@property
	def EnableLspPing(self):
		"""If selected, LSP Ping is enabled for learned LSPs.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLspPing')

	@property
	def EnableLspSelfPing(self):
		"""If selected, LSP Self Ping is enabled for learned LSPs.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLspSelfPing')

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
	def EroSameAsPrimary(self):
		"""ERO Same As Primary

		Returns:
			bool
		"""
		return self._get_attribute('eroSameAsPrimary')
	@EroSameAsPrimary.setter
	def EroSameAsPrimary(self, value):
		self._set_attribute('eroSameAsPrimary', value)

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
	def IncludeAssociation(self):
		"""Indicates whether Association will be included in a RSVP Sync LSP. All other attributes in sub-tab-PPAG would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAssociation')

	@property
	def InitialDelegation(self):
		"""Initial Delegation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initialDelegation')

	@property
	def InsertIPv6ExplicitNull(self):
		"""Insert IPv6 explicit NULL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('insertIPv6ExplicitNull')

	@property
	def IpDSCPofLspSelfPing(self):
		"""IP DSCP of LSP Self Ping.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipDSCPofLspSelfPing')

	@property
	def IpTTLofLspSelfPing(self):
		"""IP TTL of LSP Self Ping.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipTTLofLspSelfPing')

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
	def LspCount(self):
		"""LSP#

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspCount')

	@property
	def LspDelegationState(self):
		"""LSP Delegation State

		Returns:
			list(str[delegated|delegationConfirmed|delegationRejected|delegationReturned|delegationRevoked|nonDelegated|none])
		"""
		return self._get_attribute('lspDelegationState')

	@property
	def LspId(self):
		"""LSP Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspId')

	@property
	def LspOperativeMode(self):
		"""The mode of LSP in which it is currently behaving.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspOperativeMode')

	@property
	def LspSelfPingRetryCount(self):
		"""LSP Self Ping Retry Count.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspSelfPingRetryCount')

	@property
	def LspSelfPingRetryInterval(self):
		"""LSP Self Ping Retry Interval (ms).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspSelfPingRetryInterval')

	@property
	def LspSelfPingSessionId(self):
		"""LSP Self Ping Session Id.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspSelfPingSessionId')

	@property
	def LspSelfPingStatus(self):
		"""LSP Self Ping Status

		Returns:
			list(str[none|success|timedOut])
		"""
		return self._get_attribute('lspSelfPingStatus')

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
	def NumberOfEroSubObjects(self):
		"""Number Of ERO Sub-Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfEroSubObjects')
	@NumberOfEroSubObjects.setter
	def NumberOfEroSubObjects(self, value):
		self._set_attribute('numberOfEroSubObjects', value)

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
	def PccIp(self):
		"""PCC IP

		Returns:
			list(str)
		"""
		return self._get_attribute('pccIp')

	@property
	def PeakDataRate(self):
		"""Peak Data Rate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peakDataRate')

	@property
	def PpagTLVType(self):
		"""PPAG TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ppagTLVType')

	@property
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def PrependDutToEro(self):
		"""Prepend DUT to ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prependDutToEro')

	@property
	def ProtectionLsp(self):
		"""Indicates whether Protection LSP Bit is On.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionLsp')

	@property
	def ReDelegationTimerStatus(self):
		"""Re-Delegation Timer Status

		Returns:
			list(str[expired|none|notStarted|running|stopped])
		"""
		return self._get_attribute('reDelegationTimerStatus')

	@property
	def ReEvaluationRequestInterval(self):
		"""Re-Evaluation Request Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reEvaluationRequestInterval')

	@property
	def RedelegationTimeoutInterval(self):
		"""The period of time a PCC waits for, when a PCEP session is terminated, before revoking LSP delegation to a PCE and attempting to redelegate LSPs associated with the terminated PCEP session to PCE.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('redelegationTimeoutInterval')

	@property
	def RefreshInterval(self):
		"""Refresh Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('refreshInterval')

	@property
	def RemoteIp(self):
		"""Remote IP Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIp')

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
	def SessionInformation(self):
		"""Logs additional information about the RSVP session state

		Returns:
			list(str[lastErrLSPAdmissionControlFailure|lastErrLSPBadAdSpecValue|lastErrLSPBadExplicitRoute|lastErrLSPBadFlowspecValue|lastErrLSPBadInitialSubobject|lastErrLSPBadLooseNode|lastErrLSPBadStrictNode|lastErrLSPBadTSpecValue|lastErrLSPDelayBoundNotMet|lastErrLSPMPLSAllocationFailure|lastErrLSPMTUTooBig|lastErrLSPNonRSVPRouter|lastErrLSPNoRouteAvailable|lastErrLSPPathErr|lastErrLSPPathTearSent|lastErrLSPRequestedBandwidthUnavailable|lastErrLSPReservationTearReceived|lastErrLSPReservationTearSent|lastErrLSPReservationTimeout|lastErrLSPRoutingLoops|lastErrLSPRoutingProblem|lastErrLSPRSVPSystemError|lastErrLSPServiceConflict|lastErrLSPServiceUnsupported|lastErrLSPTrafficControlError|lastErrLSPTrafficControlSystemError|lastErrLSPTrafficOrganizationError|lastErrLSPTrafficServiceError|lastErrLSPUnknownObjectClass|lastErrLSPUnknownObjectCType|lastErrLSPUnsupportedL3PID|lSPAdmissionControlFailure|lSPBadAdSpecValue|lSPBadExplicitRoute|lSPBadFlowspecValue|lSPBadInitialSubobject|lSPBadLooseNode|lSPBadStrictNode|lSPBadTSpecValue|lSPDelayBoundNotMet|lSPMPLSAllocationFailure|lSPMTUTooBig|lSPNonRSVPRouter|lSPNoRouteAvailable|lSPPathErr|lSPPathTearSent|lSPRequestedBandwidthUnavailable|lSPReservationNotReceived|lSPReservationTearReceived|lSPReservationTearSent|lSPReservationTimeout|lSPRoutingLoops|lSPRoutingProblem|lSPRSVPSystemError|lSPServiceConflict|lSPServiceUnsupported|lSPTrafficControlError|lSPTrafficControlSystemError|lSPTrafficOrganizationError|lSPTrafficServiceError|lSPUnknownObjectClass|lSPUnknownObjectCType|lSPUnsupportedL3PID|mbbCompleted|mbbTriggered|none|noPathReceived|pCRepReceived|pCReqSent])
		"""
		return self._get_attribute('sessionInformation')

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
	def SourceIp(self):
		"""Source IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIp')

	@property
	def SourceIpv6(self):
		"""Source IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv6')

	@property
	def StandbyMode(self):
		"""Indicates whether Standby LSP Bit is On.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('standbyMode')

	@property
	def State(self):
		"""State

		Returns:
			list(str[down|none|notStarted|up])
		"""
		return self._get_attribute('state')

	@property
	def TSpecSameAsPrimary(self):
		"""TSpec Same As Primary

		Returns:
			bool
		"""
		return self._get_attribute('tSpecSameAsPrimary')
	@TSpecSameAsPrimary.setter
	def TSpecSameAsPrimary(self, value):
		self._set_attribute('tSpecSameAsPrimary', value)

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
	def UsingHeadendIp(self):
		"""Using Headend IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('usingHeadendIp')

	def InitiatePathReoptimization(self):
		"""Executes the initiatePathReoptimization operation on the server.

		Send Path with re-evaluation request bit of SESSION-ATTRIBUTE object set, for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('InitiatePathReoptimization', payload=locals(), response_object=None)

	def InitiatePathReoptimization(self, SessionIndices):
		"""Executes the initiatePathReoptimization operation on the server.

		Send Path with re-evaluation request bit of SESSION-ATTRIBUTE object set, for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('InitiatePathReoptimization', payload=locals(), response_object=None)

	def InitiatePathReoptimization(self, SessionIndices):
		"""Executes the initiatePathReoptimization operation on the server.

		Send Path with re-evaluation request bit of SESSION-ATTRIBUTE object set, for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('InitiatePathReoptimization', payload=locals(), response_object=None)

	def InitiatePathReoptimization(self, Arg2):
		"""Executes the initiatePathReoptimization operation on the server.

		Initiate Path Reoptimization

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('InitiatePathReoptimization', payload=locals(), response_object=None)

	def MakeBeforeBreak(self):
		"""Executes the makeBeforeBreak operation on the server.

		Initiate Make Before Break for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('MakeBeforeBreak', payload=locals(), response_object=None)

	def MakeBeforeBreak(self, SessionIndices):
		"""Executes the makeBeforeBreak operation on the server.

		Initiate Make Before Break for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('MakeBeforeBreak', payload=locals(), response_object=None)

	def MakeBeforeBreak(self, SessionIndices):
		"""Executes the makeBeforeBreak operation on the server.

		Initiate Make Before Break for selected Head Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('MakeBeforeBreak', payload=locals(), response_object=None)

	def MakeBeforeBreak(self, Arg2):
		"""Executes the makeBeforeBreak operation on the server.

		Make Before Break

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('MakeBeforeBreak', payload=locals(), response_object=None)

	def PcepDelegate(self):
		"""Executes the pcepDelegate operation on the server.

		Delegate the non-delegated LSPs among the selected RSVP-TE LSPs to PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PcepDelegate', payload=locals(), response_object=None)

	def PcepDelegate(self, SessionIndices):
		"""Executes the pcepDelegate operation on the server.

		Delegate the non-delegated LSPs among the selected RSVP-TE LSPs to PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PcepDelegate', payload=locals(), response_object=None)

	def PcepDelegate(self, SessionIndices):
		"""Executes the pcepDelegate operation on the server.

		Delegate the non-delegated LSPs among the selected RSVP-TE LSPs to PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PcepDelegate', payload=locals(), response_object=None)

	def PcepDelegate(self, Arg2):
		"""Executes the pcepDelegate operation on the server.

		Delegate

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('PcepDelegate', payload=locals(), response_object=None)

	def PcepRevokeDelegation(self):
		"""Executes the pcepRevokeDelegation operation on the server.

		Revoke Delegation from PCE for delegated LSPs among the selected LSPs.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PcepRevokeDelegation', payload=locals(), response_object=None)

	def PcepRevokeDelegation(self, SessionIndices):
		"""Executes the pcepRevokeDelegation operation on the server.

		Revoke Delegation from PCE for delegated LSPs among the selected LSPs.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PcepRevokeDelegation', payload=locals(), response_object=None)

	def PcepRevokeDelegation(self, SessionIndices):
		"""Executes the pcepRevokeDelegation operation on the server.

		Revoke Delegation from PCE for delegated LSPs among the selected LSPs.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PcepRevokeDelegation', payload=locals(), response_object=None)

	def PcepRevokeDelegation(self, Arg2):
		"""Executes the pcepRevokeDelegation operation on the server.

		Revoke Delegation

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('PcepRevokeDelegation', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Activate/Enable Tunnel selected Head Ranges

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

		Activate/Enable Tunnel selected Head Ranges

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

		Activate/Enable Tunnel selected Head Ranges

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
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
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

		Deactivate/Disable selected Tunnel Head Ranges

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

		Deactivate/Disable selected Tunnel Head Ranges

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

		Deactivate/Disable selected Tunnel Head Ranges

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
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
