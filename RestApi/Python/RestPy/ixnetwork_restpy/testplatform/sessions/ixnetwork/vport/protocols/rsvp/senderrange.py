from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SenderRange(Base):
	"""The SenderRange class encapsulates a user managed senderRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SenderRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'senderRange'

	def __init__(self, parent):
		super(SenderRange, self).__init__(parent)

	@property
	def TunnelHeadToLeaf(self):
		"""An instance of the TunnelHeadToLeaf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtoleaf.TunnelHeadToLeaf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtoleaf import TunnelHeadToLeaf
		return TunnelHeadToLeaf(self)

	@property
	def TunnelHeadTrafficEndPoint(self):
		"""An instance of the TunnelHeadTrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtrafficendpoint.TunnelHeadTrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtrafficendpoint import TunnelHeadTrafficEndPoint
		return TunnelHeadTrafficEndPoint(self)

	@property
	def AutoGenerateSessionName(self):
		"""If enabled, the session name is generated automatically. If it is not enabled, the session name field is activated and must be filled in.

		Returns:
			bool
		"""
		return self._get_attribute('autoGenerateSessionName')
	@AutoGenerateSessionName.setter
	def AutoGenerateSessionName(self, value):
		self._set_attribute('autoGenerateSessionName', value)

	@property
	def BackupLspIdPoolStart(self):
		"""It helps to set the LSP Id for the re-optimized LSP.

		Returns:
			number
		"""
		return self._get_attribute('backupLspIdPoolStart')
	@BackupLspIdPoolStart.setter
	def BackupLspIdPoolStart(self, value):
		self._set_attribute('backupLspIdPoolStart', value)

	@property
	def Bandwidth(self):
		"""The bandwidth requested for the connection, expressed in kbits/sec.

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def BandwidthProtectionDesired(self):
		"""Indicates that PLRs should skip at least the next node for a backup path.

		Returns:
			bool
		"""
		return self._get_attribute('bandwidthProtectionDesired')
	@BandwidthProtectionDesired.setter
	def BandwidthProtectionDesired(self, value):
		self._set_attribute('bandwidthProtectionDesired', value)

	@property
	def EnableBfdMpls(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdMpls')
	@EnableBfdMpls.setter
	def EnableBfdMpls(self, value):
		self._set_attribute('enableBfdMpls', value)

	@property
	def EnableFastReroute(self):
		"""Enables the use of the fast reroute feature.

		Returns:
			bool
		"""
		return self._get_attribute('enableFastReroute')
	@EnableFastReroute.setter
	def EnableFastReroute(self, value):
		self._set_attribute('enableFastReroute', value)

	@property
	def EnableLspPing(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPing')
	@EnableLspPing.setter
	def EnableLspPing(self, value):
		self._set_attribute('enableLspPing', value)

	@property
	def EnablePathReoptimization(self):
		"""If true, enables the Path Re-optimization option.

		Returns:
			bool
		"""
		return self._get_attribute('enablePathReoptimization')
	@EnablePathReoptimization.setter
	def EnablePathReoptimization(self, value):
		self._set_attribute('enablePathReoptimization', value)

	@property
	def EnablePeriodicReEvaluationRequest(self):
		"""If true, enables the head LSR to send periodic path re-evaluation request in every Re-Optimization Interval.

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicReEvaluationRequest')
	@EnablePeriodicReEvaluationRequest.setter
	def EnablePeriodicReEvaluationRequest(self, value):
		self._set_attribute('enablePeriodicReEvaluationRequest', value)

	@property
	def EnableResourceAffinities(self):
		"""Enables the use of RSVP resource class affinities for LSP tunnels.

		Returns:
			bool
		"""
		return self._get_attribute('enableResourceAffinities')
	@EnableResourceAffinities.setter
	def EnableResourceAffinities(self, value):
		self._set_attribute('enableResourceAffinities', value)

	@property
	def Enabled(self):
		"""Enables the sender range entry.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExcludeAny(self):
		"""Represents a set of attribute filters associated with a tunnel, any of which renders a link unacceptable.

		Returns:
			number
		"""
		return self._get_attribute('excludeAny')
	@ExcludeAny.setter
	def ExcludeAny(self, value):
		self._set_attribute('excludeAny', value)

	@property
	def FastRerouteBandwidth(self):
		"""An estimate of the bandwidth needed for the protection path.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteBandwidth')
	@FastRerouteBandwidth.setter
	def FastRerouteBandwidth(self, value):
		self._set_attribute('fastRerouteBandwidth', value)

	@property
	def FastRerouteDetour(self):
		"""Used to provide backup LSP tunnels for local repair of LSP tunnels, in the event of failure of a node or link. Contains the specifics of the detour LSPs: nodes to use and nodes to avoid.

		Returns:
			list(dict(arg1:str,arg2:str))
		"""
		return self._get_attribute('fastRerouteDetour')
	@FastRerouteDetour.setter
	def FastRerouteDetour(self, value):
		self._set_attribute('fastRerouteDetour', value)

	@property
	def FastRerouteExcludeAny(self):
		"""Capability filters used to dictate which backup paths are acceptable or unacceptable.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteExcludeAny')
	@FastRerouteExcludeAny.setter
	def FastRerouteExcludeAny(self, value):
		self._set_attribute('fastRerouteExcludeAny', value)

	@property
	def FastRerouteFacilityBackupDesired(self):
		"""If enabled, indicates that facility backup should be used. With this method, the MPLS label stack allows the creation of a bypass tunnel to protect a set of LSPs with similar characteristics/constraints. Protects both links and nodes.

		Returns:
			bool
		"""
		return self._get_attribute('fastRerouteFacilityBackupDesired')
	@FastRerouteFacilityBackupDesired.setter
	def FastRerouteFacilityBackupDesired(self, value):
		self._set_attribute('fastRerouteFacilityBackupDesired', value)

	@property
	def FastRerouteHoldingPriority(self):
		"""The priority value for the backup path, pertaining to holding resources - whether a session can be preempted BY another session.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteHoldingPriority')
	@FastRerouteHoldingPriority.setter
	def FastRerouteHoldingPriority(self, value):
		self._set_attribute('fastRerouteHoldingPriority', value)

	@property
	def FastRerouteHopLimit(self):
		"""Indicates the number of extra hops that may be added by a protection path.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteHopLimit')
	@FastRerouteHopLimit.setter
	def FastRerouteHopLimit(self, value):
		self._set_attribute('fastRerouteHopLimit', value)

	@property
	def FastRerouteIncludeAll(self):
		"""Capability filters used to dictate which backup paths are acceptable or unacceptable.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteIncludeAll')
	@FastRerouteIncludeAll.setter
	def FastRerouteIncludeAll(self, value):
		self._set_attribute('fastRerouteIncludeAll', value)

	@property
	def FastRerouteIncludeAny(self):
		"""Capability filters used to dictate which backup paths are acceptable or unacceptable.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteIncludeAny')
	@FastRerouteIncludeAny.setter
	def FastRerouteIncludeAny(self, value):
		self._set_attribute('fastRerouteIncludeAny', value)

	@property
	def FastRerouteOne2OneBackupDesired(self):
		"""If enabled, indicates that one-to-one backup should be used. With this method, one detour LSP will be created for each protected LSP for each place where the LSP could potentially be repaired locally. Protects both links and nodes.

		Returns:
			bool
		"""
		return self._get_attribute('fastRerouteOne2OneBackupDesired')
	@FastRerouteOne2OneBackupDesired.setter
	def FastRerouteOne2OneBackupDesired(self, value):
		self._set_attribute('fastRerouteOne2OneBackupDesired', value)

	@property
	def FastRerouteSendDetour(self):
		"""Enables the generation of a DETOUR object for one to one operation.

		Returns:
			bool
		"""
		return self._get_attribute('fastRerouteSendDetour')
	@FastRerouteSendDetour.setter
	def FastRerouteSendDetour(self, value):
		self._set_attribute('fastRerouteSendDetour', value)

	@property
	def FastRerouteSetupPriority(self):
		"""Indicate the priority for taking and holding resources along the backup path.

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteSetupPriority')
	@FastRerouteSetupPriority.setter
	def FastRerouteSetupPriority(self, value):
		self._set_attribute('fastRerouteSetupPriority', value)

	@property
	def HoldingPriority(self):
		"""Priority in holding onto resources. Range is 0 to 7, with 0 the highest priority.

		Returns:
			number
		"""
		return self._get_attribute('holdingPriority')
	@HoldingPriority.setter
	def HoldingPriority(self, value):
		self._set_attribute('holdingPriority', value)

	@property
	def IncludeAll(self):
		"""32-bit value. Represents a set of attribute filters associated with a tunnel, all of which must be present for a link to be acceptable (with respect to this test). When all bits are set to 0 (null set), it automatically passes.

		Returns:
			number
		"""
		return self._get_attribute('includeAll')
	@IncludeAll.setter
	def IncludeAll(self, value):
		self._set_attribute('includeAll', value)

	@property
	def IncludeAny(self):
		"""32-bit value. Represents a set of attribute filters associated with a tunnel, any of which makes a link acceptable (with respect to this test). When all bits are set to 0 (null set), it automatically passes.

		Returns:
			number
		"""
		return self._get_attribute('includeAny')
	@IncludeAny.setter
	def IncludeAny(self, value):
		self._set_attribute('includeAny', value)

	@property
	def IpCount(self):
		"""The number of routers in the destination range.

		Returns:
			number
		"""
		return self._get_attribute('ipCount')
	@IpCount.setter
	def IpCount(self, value):
		self._set_attribute('ipCount', value)

	@property
	def IpStart(self):
		"""The IP address of the first destination router.

		Returns:
			str
		"""
		return self._get_attribute('ipStart')
	@IpStart.setter
	def IpStart(self, value):
		self._set_attribute('ipStart', value)

	@property
	def LabelRecordingDesired(self):
		"""If enabled, indicates that label information is to be included when doing a route record.

		Returns:
			bool
		"""
		return self._get_attribute('labelRecordingDesired')
	@LabelRecordingDesired.setter
	def LabelRecordingDesired(self, value):
		self._set_attribute('labelRecordingDesired', value)

	@property
	def LocalProtectionDesired(self):
		"""(Enabled by default) This permits transit routers to use a local traffic rerouting repair mechanism in the event of a fault on an adjacent downstream link or node. This may result in a violation of the explicit route object.

		Returns:
			bool
		"""
		return self._get_attribute('localProtectionDesired')
	@LocalProtectionDesired.setter
	def LocalProtectionDesired(self, value):
		self._set_attribute('localProtectionDesired', value)

	@property
	def LspIdCount(self):
		"""The number of LSP IDs in the range.

		Returns:
			number
		"""
		return self._get_attribute('lspIdCount')
	@LspIdCount.setter
	def LspIdCount(self, value):
		self._set_attribute('lspIdCount', value)

	@property
	def LspIdStart(self):
		"""The first label-switched path ID (LSP ID) value in the range of LSP IDs.

		Returns:
			number
		"""
		return self._get_attribute('lspIdStart')
	@LspIdStart.setter
	def LspIdStart(self, value):
		self._set_attribute('lspIdStart', value)

	@property
	def MaximumPacketSize(self):
		"""32-bit integer. The maximum number of bytes allowed to cross the interface in a transmitted packet.

		Returns:
			number
		"""
		return self._get_attribute('maximumPacketSize')
	@MaximumPacketSize.setter
	def MaximumPacketSize(self, value):
		self._set_attribute('maximumPacketSize', value)

	@property
	def MinimumPolicedUnit(self):
		"""32-bit integer. The minimum allowable size for a policed unit.

		Returns:
			number
		"""
		return self._get_attribute('minimumPolicedUnit')
	@MinimumPolicedUnit.setter
	def MinimumPolicedUnit(self, value):
		self._set_attribute('minimumPolicedUnit', value)

	@property
	def NodeProtectionDesired(self):
		"""For Fast Reroute - if enabled, sets the Node Protection Desired Flag in the Session_Attribute object of the RRO message. It indicates to PLRs associated with the protected LSP path, that a backup path is desired that bypasses (avoids) at least the next node on the LSP.

		Returns:
			bool
		"""
		return self._get_attribute('nodeProtectionDesired')
	@NodeProtectionDesired.setter
	def NodeProtectionDesired(self, value):
		self._set_attribute('nodeProtectionDesired', value)

	@property
	def PathTearTlv(self):
		"""A set of custom TLVs to be included in TEAR messages, constructed with the rsvpCustomTlv command.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('pathTearTlv')
	@PathTearTlv.setter
	def PathTearTlv(self, value):
		self._set_attribute('pathTearTlv', value)

	@property
	def PathTlv(self):
		"""A set of custom TLVs to be included in PATH messages, constructed with the rsvpCustomTlv command.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('pathTlv')
	@PathTlv.setter
	def PathTlv(self, value):
		self._set_attribute('pathTlv', value)

	@property
	def PeakDataRate(self):
		"""The maximum traffic rate that can be maintained. The policing mechanism allows some burstiness, but restricts it so the overall packet transmission rate is less than the rate at which tokens.

		Returns:
			number
		"""
		return self._get_attribute('peakDataRate')
	@PeakDataRate.setter
	def PeakDataRate(self, value):
		self._set_attribute('peakDataRate', value)

	@property
	def ReEvaluationRequestInterval(self):
		"""Represents the time period (in milliseconds) at which the path re-evaluation request is sent by the head LSR. The default value is: 180000 ms (3 mins).

		Returns:
			number
		"""
		return self._get_attribute('reEvaluationRequestInterval')
	@ReEvaluationRequestInterval.setter
	def ReEvaluationRequestInterval(self, value):
		self._set_attribute('reEvaluationRequestInterval', value)

	@property
	def RefreshInterval(self):
		"""The interval between summary refresh messages.

		Returns:
			number
		"""
		return self._get_attribute('refreshInterval')
	@RefreshInterval.setter
	def RefreshInterval(self, value):
		self._set_attribute('refreshInterval', value)

	@property
	def SeStyleDesired(self):
		"""This indicates that the tunnel ingress node may reroute this tunnel without tearing it down. A tunnel egress node should use the SE Style when responding with an RESV message.

		Returns:
			bool
		"""
		return self._get_attribute('seStyleDesired')
	@SeStyleDesired.setter
	def SeStyleDesired(self, value):
		self._set_attribute('seStyleDesired', value)

	@property
	def SessionName(self):
		"""If enableAutoSessionName is not set, this is the name assigned to this session.

		Returns:
			str
		"""
		return self._get_attribute('sessionName')
	@SessionName.setter
	def SessionName(self, value):
		self._set_attribute('sessionName', value)

	@property
	def SetupPriority(self):
		"""This is the session priority with respect to taking resources, such as preempting another session. The valid range is from 0 to 7. The highest priority is indicated by 0.

		Returns:
			number
		"""
		return self._get_attribute('setupPriority')
	@SetupPriority.setter
	def SetupPriority(self, value):
		self._set_attribute('setupPriority', value)

	@property
	def TimeoutMultiplier(self):
		"""The number of Hellos before a neighbor is declared dead.

		Returns:
			number
		"""
		return self._get_attribute('timeoutMultiplier')
	@TimeoutMultiplier.setter
	def TimeoutMultiplier(self, value):
		self._set_attribute('timeoutMultiplier', value)

	@property
	def TokenBucketRate(self):
		"""The rate of transfer for data in a flow. In this application, it is used with a traffic policing mechanism. The data tokens enter the bucket, filling the bucket. The data from a number of tokens is combined to form and send a packet. The goal is to determine a rate which will not overflow the specified token bucket size, and cause new data (tokens) to be rejected/discarded.

		Returns:
			number
		"""
		return self._get_attribute('tokenBucketRate')
	@TokenBucketRate.setter
	def TokenBucketRate(self, value):
		self._set_attribute('tokenBucketRate', value)

	@property
	def TokenBucketSize(self):
		"""The maximum capacity (in bytes) the token bucket can hold, and above which newly received tokens cannot be processed and are discarded.

		Returns:
			number
		"""
		return self._get_attribute('tokenBucketSize')
	@TokenBucketSize.setter
	def TokenBucketSize(self, value):
		self._set_attribute('tokenBucketSize', value)

	def add(self, AutoGenerateSessionName=None, BackupLspIdPoolStart=None, Bandwidth=None, BandwidthProtectionDesired=None, EnableBfdMpls=None, EnableFastReroute=None, EnableLspPing=None, EnablePathReoptimization=None, EnablePeriodicReEvaluationRequest=None, EnableResourceAffinities=None, Enabled=None, ExcludeAny=None, FastRerouteBandwidth=None, FastRerouteDetour=None, FastRerouteExcludeAny=None, FastRerouteFacilityBackupDesired=None, FastRerouteHoldingPriority=None, FastRerouteHopLimit=None, FastRerouteIncludeAll=None, FastRerouteIncludeAny=None, FastRerouteOne2OneBackupDesired=None, FastRerouteSendDetour=None, FastRerouteSetupPriority=None, HoldingPriority=None, IncludeAll=None, IncludeAny=None, IpCount=None, IpStart=None, LabelRecordingDesired=None, LocalProtectionDesired=None, LspIdCount=None, LspIdStart=None, MaximumPacketSize=None, MinimumPolicedUnit=None, NodeProtectionDesired=None, PathTearTlv=None, PathTlv=None, PeakDataRate=None, ReEvaluationRequestInterval=None, RefreshInterval=None, SeStyleDesired=None, SessionName=None, SetupPriority=None, TimeoutMultiplier=None, TokenBucketRate=None, TokenBucketSize=None):
		"""Adds a new senderRange node on the server and retrieves it in this instance.

		Args:
			AutoGenerateSessionName (bool): If enabled, the session name is generated automatically. If it is not enabled, the session name field is activated and must be filled in.
			BackupLspIdPoolStart (number): It helps to set the LSP Id for the re-optimized LSP.
			Bandwidth (number): The bandwidth requested for the connection, expressed in kbits/sec.
			BandwidthProtectionDesired (bool): Indicates that PLRs should skip at least the next node for a backup path.
			EnableBfdMpls (bool): NOT DEFINED
			EnableFastReroute (bool): Enables the use of the fast reroute feature.
			EnableLspPing (bool): NOT DEFINED
			EnablePathReoptimization (bool): If true, enables the Path Re-optimization option.
			EnablePeriodicReEvaluationRequest (bool): If true, enables the head LSR to send periodic path re-evaluation request in every Re-Optimization Interval.
			EnableResourceAffinities (bool): Enables the use of RSVP resource class affinities for LSP tunnels.
			Enabled (bool): Enables the sender range entry.
			ExcludeAny (number): Represents a set of attribute filters associated with a tunnel, any of which renders a link unacceptable.
			FastRerouteBandwidth (number): An estimate of the bandwidth needed for the protection path.
			FastRerouteDetour (list(dict(arg1:str,arg2:str))): Used to provide backup LSP tunnels for local repair of LSP tunnels, in the event of failure of a node or link. Contains the specifics of the detour LSPs: nodes to use and nodes to avoid.
			FastRerouteExcludeAny (number): Capability filters used to dictate which backup paths are acceptable or unacceptable.
			FastRerouteFacilityBackupDesired (bool): If enabled, indicates that facility backup should be used. With this method, the MPLS label stack allows the creation of a bypass tunnel to protect a set of LSPs with similar characteristics/constraints. Protects both links and nodes.
			FastRerouteHoldingPriority (number): The priority value for the backup path, pertaining to holding resources - whether a session can be preempted BY another session.
			FastRerouteHopLimit (number): Indicates the number of extra hops that may be added by a protection path.
			FastRerouteIncludeAll (number): Capability filters used to dictate which backup paths are acceptable or unacceptable.
			FastRerouteIncludeAny (number): Capability filters used to dictate which backup paths are acceptable or unacceptable.
			FastRerouteOne2OneBackupDesired (bool): If enabled, indicates that one-to-one backup should be used. With this method, one detour LSP will be created for each protected LSP for each place where the LSP could potentially be repaired locally. Protects both links and nodes.
			FastRerouteSendDetour (bool): Enables the generation of a DETOUR object for one to one operation.
			FastRerouteSetupPriority (number): Indicate the priority for taking and holding resources along the backup path.
			HoldingPriority (number): Priority in holding onto resources. Range is 0 to 7, with 0 the highest priority.
			IncludeAll (number): 32-bit value. Represents a set of attribute filters associated with a tunnel, all of which must be present for a link to be acceptable (with respect to this test). When all bits are set to 0 (null set), it automatically passes.
			IncludeAny (number): 32-bit value. Represents a set of attribute filters associated with a tunnel, any of which makes a link acceptable (with respect to this test). When all bits are set to 0 (null set), it automatically passes.
			IpCount (number): The number of routers in the destination range.
			IpStart (str): The IP address of the first destination router.
			LabelRecordingDesired (bool): If enabled, indicates that label information is to be included when doing a route record.
			LocalProtectionDesired (bool): (Enabled by default) This permits transit routers to use a local traffic rerouting repair mechanism in the event of a fault on an adjacent downstream link or node. This may result in a violation of the explicit route object.
			LspIdCount (number): The number of LSP IDs in the range.
			LspIdStart (number): The first label-switched path ID (LSP ID) value in the range of LSP IDs.
			MaximumPacketSize (number): 32-bit integer. The maximum number of bytes allowed to cross the interface in a transmitted packet.
			MinimumPolicedUnit (number): 32-bit integer. The minimum allowable size for a policed unit.
			NodeProtectionDesired (bool): For Fast Reroute - if enabled, sets the Node Protection Desired Flag in the Session_Attribute object of the RRO message. It indicates to PLRs associated with the protected LSP path, that a backup path is desired that bypasses (avoids) at least the next node on the LSP.
			PathTearTlv (list(dict(arg1:number,arg2:number,arg3:str))): A set of custom TLVs to be included in TEAR messages, constructed with the rsvpCustomTlv command.
			PathTlv (list(dict(arg1:number,arg2:number,arg3:str))): A set of custom TLVs to be included in PATH messages, constructed with the rsvpCustomTlv command.
			PeakDataRate (number): The maximum traffic rate that can be maintained. The policing mechanism allows some burstiness, but restricts it so the overall packet transmission rate is less than the rate at which tokens.
			ReEvaluationRequestInterval (number): Represents the time period (in milliseconds) at which the path re-evaluation request is sent by the head LSR. The default value is: 180000 ms (3 mins).
			RefreshInterval (number): The interval between summary refresh messages.
			SeStyleDesired (bool): This indicates that the tunnel ingress node may reroute this tunnel without tearing it down. A tunnel egress node should use the SE Style when responding with an RESV message.
			SessionName (str): If enableAutoSessionName is not set, this is the name assigned to this session.
			SetupPriority (number): This is the session priority with respect to taking resources, such as preempting another session. The valid range is from 0 to 7. The highest priority is indicated by 0.
			TimeoutMultiplier (number): The number of Hellos before a neighbor is declared dead.
			TokenBucketRate (number): The rate of transfer for data in a flow. In this application, it is used with a traffic policing mechanism. The data tokens enter the bucket, filling the bucket. The data from a number of tokens is combined to form and send a packet. The goal is to determine a rate which will not overflow the specified token bucket size, and cause new data (tokens) to be rejected/discarded.
			TokenBucketSize (number): The maximum capacity (in bytes) the token bucket can hold, and above which newly received tokens cannot be processed and are discarded.

		Returns:
			self: This instance with all currently retrieved senderRange data using find and the newly added senderRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the senderRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoGenerateSessionName=None, BackupLspIdPoolStart=None, Bandwidth=None, BandwidthProtectionDesired=None, EnableBfdMpls=None, EnableFastReroute=None, EnableLspPing=None, EnablePathReoptimization=None, EnablePeriodicReEvaluationRequest=None, EnableResourceAffinities=None, Enabled=None, ExcludeAny=None, FastRerouteBandwidth=None, FastRerouteDetour=None, FastRerouteExcludeAny=None, FastRerouteFacilityBackupDesired=None, FastRerouteHoldingPriority=None, FastRerouteHopLimit=None, FastRerouteIncludeAll=None, FastRerouteIncludeAny=None, FastRerouteOne2OneBackupDesired=None, FastRerouteSendDetour=None, FastRerouteSetupPriority=None, HoldingPriority=None, IncludeAll=None, IncludeAny=None, IpCount=None, IpStart=None, LabelRecordingDesired=None, LocalProtectionDesired=None, LspIdCount=None, LspIdStart=None, MaximumPacketSize=None, MinimumPolicedUnit=None, NodeProtectionDesired=None, PathTearTlv=None, PathTlv=None, PeakDataRate=None, ReEvaluationRequestInterval=None, RefreshInterval=None, SeStyleDesired=None, SessionName=None, SetupPriority=None, TimeoutMultiplier=None, TokenBucketRate=None, TokenBucketSize=None):
		"""Finds and retrieves senderRange data from the server.

		All named parameters support regex and can be used to selectively retrieve senderRange data from the server.
		By default the find method takes no parameters and will retrieve all senderRange data from the server.

		Args:
			AutoGenerateSessionName (bool): If enabled, the session name is generated automatically. If it is not enabled, the session name field is activated and must be filled in.
			BackupLspIdPoolStart (number): It helps to set the LSP Id for the re-optimized LSP.
			Bandwidth (number): The bandwidth requested for the connection, expressed in kbits/sec.
			BandwidthProtectionDesired (bool): Indicates that PLRs should skip at least the next node for a backup path.
			EnableBfdMpls (bool): NOT DEFINED
			EnableFastReroute (bool): Enables the use of the fast reroute feature.
			EnableLspPing (bool): NOT DEFINED
			EnablePathReoptimization (bool): If true, enables the Path Re-optimization option.
			EnablePeriodicReEvaluationRequest (bool): If true, enables the head LSR to send periodic path re-evaluation request in every Re-Optimization Interval.
			EnableResourceAffinities (bool): Enables the use of RSVP resource class affinities for LSP tunnels.
			Enabled (bool): Enables the sender range entry.
			ExcludeAny (number): Represents a set of attribute filters associated with a tunnel, any of which renders a link unacceptable.
			FastRerouteBandwidth (number): An estimate of the bandwidth needed for the protection path.
			FastRerouteDetour (list(dict(arg1:str,arg2:str))): Used to provide backup LSP tunnels for local repair of LSP tunnels, in the event of failure of a node or link. Contains the specifics of the detour LSPs: nodes to use and nodes to avoid.
			FastRerouteExcludeAny (number): Capability filters used to dictate which backup paths are acceptable or unacceptable.
			FastRerouteFacilityBackupDesired (bool): If enabled, indicates that facility backup should be used. With this method, the MPLS label stack allows the creation of a bypass tunnel to protect a set of LSPs with similar characteristics/constraints. Protects both links and nodes.
			FastRerouteHoldingPriority (number): The priority value for the backup path, pertaining to holding resources - whether a session can be preempted BY another session.
			FastRerouteHopLimit (number): Indicates the number of extra hops that may be added by a protection path.
			FastRerouteIncludeAll (number): Capability filters used to dictate which backup paths are acceptable or unacceptable.
			FastRerouteIncludeAny (number): Capability filters used to dictate which backup paths are acceptable or unacceptable.
			FastRerouteOne2OneBackupDesired (bool): If enabled, indicates that one-to-one backup should be used. With this method, one detour LSP will be created for each protected LSP for each place where the LSP could potentially be repaired locally. Protects both links and nodes.
			FastRerouteSendDetour (bool): Enables the generation of a DETOUR object for one to one operation.
			FastRerouteSetupPriority (number): Indicate the priority for taking and holding resources along the backup path.
			HoldingPriority (number): Priority in holding onto resources. Range is 0 to 7, with 0 the highest priority.
			IncludeAll (number): 32-bit value. Represents a set of attribute filters associated with a tunnel, all of which must be present for a link to be acceptable (with respect to this test). When all bits are set to 0 (null set), it automatically passes.
			IncludeAny (number): 32-bit value. Represents a set of attribute filters associated with a tunnel, any of which makes a link acceptable (with respect to this test). When all bits are set to 0 (null set), it automatically passes.
			IpCount (number): The number of routers in the destination range.
			IpStart (str): The IP address of the first destination router.
			LabelRecordingDesired (bool): If enabled, indicates that label information is to be included when doing a route record.
			LocalProtectionDesired (bool): (Enabled by default) This permits transit routers to use a local traffic rerouting repair mechanism in the event of a fault on an adjacent downstream link or node. This may result in a violation of the explicit route object.
			LspIdCount (number): The number of LSP IDs in the range.
			LspIdStart (number): The first label-switched path ID (LSP ID) value in the range of LSP IDs.
			MaximumPacketSize (number): 32-bit integer. The maximum number of bytes allowed to cross the interface in a transmitted packet.
			MinimumPolicedUnit (number): 32-bit integer. The minimum allowable size for a policed unit.
			NodeProtectionDesired (bool): For Fast Reroute - if enabled, sets the Node Protection Desired Flag in the Session_Attribute object of the RRO message. It indicates to PLRs associated with the protected LSP path, that a backup path is desired that bypasses (avoids) at least the next node on the LSP.
			PathTearTlv (list(dict(arg1:number,arg2:number,arg3:str))): A set of custom TLVs to be included in TEAR messages, constructed with the rsvpCustomTlv command.
			PathTlv (list(dict(arg1:number,arg2:number,arg3:str))): A set of custom TLVs to be included in PATH messages, constructed with the rsvpCustomTlv command.
			PeakDataRate (number): The maximum traffic rate that can be maintained. The policing mechanism allows some burstiness, but restricts it so the overall packet transmission rate is less than the rate at which tokens.
			ReEvaluationRequestInterval (number): Represents the time period (in milliseconds) at which the path re-evaluation request is sent by the head LSR. The default value is: 180000 ms (3 mins).
			RefreshInterval (number): The interval between summary refresh messages.
			SeStyleDesired (bool): This indicates that the tunnel ingress node may reroute this tunnel without tearing it down. A tunnel egress node should use the SE Style when responding with an RESV message.
			SessionName (str): If enableAutoSessionName is not set, this is the name assigned to this session.
			SetupPriority (number): This is the session priority with respect to taking resources, such as preempting another session. The valid range is from 0 to 7. The highest priority is indicated by 0.
			TimeoutMultiplier (number): The number of Hellos before a neighbor is declared dead.
			TokenBucketRate (number): The rate of transfer for data in a flow. In this application, it is used with a traffic policing mechanism. The data tokens enter the bucket, filling the bucket. The data from a number of tokens is combined to form and send a packet. The goal is to determine a rate which will not overflow the specified token bucket size, and cause new data (tokens) to be rejected/discarded.
			TokenBucketSize (number): The maximum capacity (in bytes) the token bucket can hold, and above which newly received tokens cannot be processed and are discarded.

		Returns:
			self: This instance with matching senderRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of senderRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the senderRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def DoMakeBeforeBreak(self):
		"""Executes the doMakeBeforeBreak operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=senderRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DoMakeBeforeBreak', payload=locals(), response_object=None)

	def SendReEvaluationRequest(self):
		"""Executes the sendReEvaluationRequest operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=senderRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendReEvaluationRequest', payload=locals(), response_object=None)
