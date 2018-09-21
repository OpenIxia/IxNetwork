from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Router(Base):
	"""The Router class encapsulates a user managed router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'router'

	def __init__(self, parent):
		super(Router, self).__init__(parent)

	@property
	def CustomTlv(self):
		"""An instance of the CustomTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtlv.CustomTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtlv import CustomTlv
		return CustomTlv(self)

	@property
	def CustomTopology(self):
		"""An instance of the CustomTopology class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopology.CustomTopology)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopology import CustomTopology
		return CustomTopology(self)

	@property
	def DceMulticastIpv4GroupRange(self):
		"""An instance of the DceMulticastIpv4GroupRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv4grouprange.DceMulticastIpv4GroupRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv4grouprange import DceMulticastIpv4GroupRange
		return DceMulticastIpv4GroupRange(self)

	@property
	def DceMulticastIpv6GroupRange(self):
		"""An instance of the DceMulticastIpv6GroupRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv6grouprange.DceMulticastIpv6GroupRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastipv6grouprange import DceMulticastIpv6GroupRange
		return DceMulticastIpv6GroupRange(self)

	@property
	def DceMulticastMacRange(self):
		"""An instance of the DceMulticastMacRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastmacrange.DceMulticastMacRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcemulticastmacrange import DceMulticastMacRange
		return DceMulticastMacRange(self)

	@property
	def DceNetworkRange(self):
		"""An instance of the DceNetworkRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenetworkrange.DceNetworkRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenetworkrange import DceNetworkRange
		return DceNetworkRange(self)

	@property
	def DceTopologyRange(self):
		"""An instance of the DceTopologyRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcetopologyrange.DceTopologyRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcetopologyrange import DceTopologyRange
		return DceTopologyRange(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.interface import Interface
		return Interface(self)

	@property
	def LearnedInformation(self):
		"""An instance of the LearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.learnedinformation.LearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.learnedinformation import LearnedInformation
		return LearnedInformation(self)._select()

	@property
	def NetworkRange(self):
		"""An instance of the NetworkRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.networkrange.NetworkRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.networkrange import NetworkRange
		return NetworkRange(self)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.routerange import RouteRange
		return RouteRange(self)

	@property
	def SpbNetworkRange(self):
		"""An instance of the SpbNetworkRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbnetworkrange.SpbNetworkRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbnetworkrange import SpbNetworkRange
		return SpbNetworkRange(self)

	@property
	def SpbTopologyRange(self):
		"""An instance of the SpbTopologyRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbtopologyrange.SpbTopologyRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbtopologyrange import SpbTopologyRange
		return SpbTopologyRange(self)

	@property
	def TrillPingOam(self):
		"""An instance of the TrillPingOam class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillpingoam.TrillPingOam)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillpingoam import TrillPingOam
		return TrillPingOam(self)._select()

	@property
	def TrillUnicastMacRange(self):
		"""An instance of the TrillUnicastMacRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillunicastmacrange.TrillUnicastMacRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillunicastmacrange import TrillUnicastMacRange
		return TrillUnicastMacRange(self)

	@property
	def AreaAddressList(self):
		"""The list of area addresses to use.

		Returns:
			list(str)
		"""
		return self._get_attribute('areaAddressList')
	@AreaAddressList.setter
	def AreaAddressList(self, value):
		self._set_attribute('areaAddressList', value)

	@property
	def AreaAuthType(self):
		"""Sets up authentication for Level 1 LSPs.

		Returns:
			str(none|password|md5)
		"""
		return self._get_attribute('areaAuthType')
	@AreaAuthType.setter
	def AreaAuthType(self, value):
		self._set_attribute('areaAuthType', value)

	@property
	def AreaReceivedPasswordList(self):
		"""If areaAuthType is isisAuthTypePassword, then this is a list of passwords that the router will accept on received LSPs.

		Returns:
			list(str)
		"""
		return self._get_attribute('areaReceivedPasswordList')
	@AreaReceivedPasswordList.setter
	def AreaReceivedPasswordList(self, value):
		self._set_attribute('areaReceivedPasswordList', value)

	@property
	def AreaTransmitPassword(self):
		"""If areaAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted LSPs.

		Returns:
			str
		"""
		return self._get_attribute('areaTransmitPassword')
	@AreaTransmitPassword.setter
	def AreaTransmitPassword(self, value):
		self._set_attribute('areaTransmitPassword', value)

	@property
	def BroadcastRootPriority(self):
		"""The value of the Broadcast Root Priority of a particular DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('broadcastRootPriority')
	@BroadcastRootPriority.setter
	def BroadcastRootPriority(self, value):
		self._set_attribute('broadcastRootPriority', value)

	@property
	def CapabilityRouterId(self):
		"""The IPv4 address format of the Capability Router.

		Returns:
			str
		"""
		return self._get_attribute('capabilityRouterId')
	@CapabilityRouterId.setter
	def CapabilityRouterId(self, value):
		self._set_attribute('capabilityRouterId', value)

	@property
	def DeviceId(self):
		"""This is a deprecated attribute in DCE ISIS mode.

		Returns:
			number
		"""
		return self._get_attribute('deviceId')
	@DeviceId.setter
	def DeviceId(self, value):
		self._set_attribute('deviceId', value)

	@property
	def DevicePriority(self):
		"""This is a deprecated attribute in DCE ISIS mode.

		Returns:
			number
		"""
		return self._get_attribute('devicePriority')
	@DevicePriority.setter
	def DevicePriority(self, value):
		self._set_attribute('devicePriority', value)

	@property
	def DomainAuthType(self):
		"""Sets up authentication for Level 2 LSPs.

		Returns:
			str(none|password|md5)
		"""
		return self._get_attribute('domainAuthType')
	@DomainAuthType.setter
	def DomainAuthType(self, value):
		self._set_attribute('domainAuthType', value)

	@property
	def DomainReceivedPasswordList(self):
		"""If domainAuthType is isisAuthTypePassword, then this is a list of passwords that the router will accept on received LSPs.

		Returns:
			list(str)
		"""
		return self._get_attribute('domainReceivedPasswordList')
	@DomainReceivedPasswordList.setter
	def DomainReceivedPasswordList(self, value):
		self._set_attribute('domainReceivedPasswordList', value)

	@property
	def DomainTransmitPassword(self):
		"""If domainAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted LSPs.

		Returns:
			str
		"""
		return self._get_attribute('domainTransmitPassword')
	@DomainTransmitPassword.setter
	def DomainTransmitPassword(self, value):
		self._set_attribute('domainTransmitPassword', value)

	@property
	def EnableAttached(self):
		"""Indicates that the Attached Flag is set. It indicates that this ISIS router can use L2 routing to reach other areas.

		Returns:
			bool
		"""
		return self._get_attribute('enableAttached')
	@EnableAttached.setter
	def EnableAttached(self, value):
		self._set_attribute('enableAttached', value)

	@property
	def EnableAutoLoopback(self):
		"""If enabled, loopback addresses are allowed in the generated routes.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoLoopback')
	@EnableAutoLoopback.setter
	def EnableAutoLoopback(self, value):
		self._set_attribute('enableAutoLoopback', value)

	@property
	def EnableDiscardLearnedLsps(self):
		"""If enabled, LSPs learned from this router's interfaces will be discarded.

		Returns:
			bool
		"""
		return self._get_attribute('enableDiscardLearnedLsps')
	@EnableDiscardLearnedLsps.setter
	def EnableDiscardLearnedLsps(self, value):
		self._set_attribute('enableDiscardLearnedLsps', value)

	@property
	def EnableHelloPadding(self):
		"""If true, enables padding of hello messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableHelloPadding')
	@EnableHelloPadding.setter
	def EnableHelloPadding(self, value):
		self._set_attribute('enableHelloPadding', value)

	@property
	def EnableHitlessRestart(self):
		"""Hitless Restart is enabled for this emulated ISIS router.

		Returns:
			bool
		"""
		return self._get_attribute('enableHitlessRestart')
	@EnableHitlessRestart.setter
	def EnableHitlessRestart(self, value):
		self._set_attribute('enableHitlessRestart', value)

	@property
	def EnableHostName(self):
		"""If true, the given dynamic host name is transmitted in all the packets sent from this router.

		Returns:
			bool
		"""
		return self._get_attribute('enableHostName')
	@EnableHostName.setter
	def EnableHostName(self, value):
		self._set_attribute('enableHostName', value)

	@property
	def EnableIgnoreMtPortCapability(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableIgnoreMtPortCapability')
	@EnableIgnoreMtPortCapability.setter
	def EnableIgnoreMtPortCapability(self, value):
		self._set_attribute('enableIgnoreMtPortCapability', value)

	@property
	def EnableIgnoreRecvMd5(self):
		"""MD5 authentication will be disabled for incoming/received packets.

		Returns:
			bool
		"""
		return self._get_attribute('enableIgnoreRecvMd5')
	@EnableIgnoreRecvMd5.setter
	def EnableIgnoreRecvMd5(self, value):
		self._set_attribute('enableIgnoreRecvMd5', value)

	@property
	def EnableMtIpv6(self):
		"""If checked in L3, emulation type traffic group ID at router level is grayed out and unassigned.

		Returns:
			bool
		"""
		return self._get_attribute('enableMtIpv6')
	@EnableMtIpv6.setter
	def EnableMtIpv6(self, value):
		self._set_attribute('enableMtIpv6', value)

	@property
	def EnableMtuProbe(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableMtuProbe')
	@EnableMtuProbe.setter
	def EnableMtuProbe(self, value):
		self._set_attribute('enableMtuProbe', value)

	@property
	def EnableMultiTopology(self):
		"""Enables more than one topology (distribution tree) corresponding to the given R bridge.

		Returns:
			bool
		"""
		return self._get_attribute('enableMultiTopology')
	@EnableMultiTopology.setter
	def EnableMultiTopology(self, value):
		self._set_attribute('enableMultiTopology', value)

	@property
	def EnableOverloaded(self):
		"""If enabled, the LSP Database Overload Bit is set. It indicates that the LSP database on this router is overloaded and that there is not enough memory to store a received LSP. This router enters the Waiting State and floods an LSP (with LSP number = 0) with the overload bit set, so other routers will not forward ISIS packets to it.

		Returns:
			bool
		"""
		return self._get_attribute('enableOverloaded')
	@EnableOverloaded.setter
	def EnableOverloaded(self, value):
		self._set_attribute('enableOverloaded', value)

	@property
	def EnablePartitionRepair(self):
		"""Enables the optional partition repair option specified in ISO/IEC 10589 and RFC 1195 for Level 1 areas.

		Returns:
			bool
		"""
		return self._get_attribute('enablePartitionRepair')
	@EnablePartitionRepair.setter
	def EnablePartitionRepair(self, value):
		self._set_attribute('enablePartitionRepair', value)

	@property
	def EnableTrillOam(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableTrillOam')
	@EnableTrillOam.setter
	def EnableTrillOam(self, value):
		self._set_attribute('enableTrillOam', value)

	@property
	def EnableWideMetric(self):
		"""Enables the use of extended reachability (wide) metrics (defined to support TE): 32-bits wide for IP reachability (routes) and 24-bits wide for IS reachability (IS neighbors). If TE is enabled, wide metrics will be enabled automatically. The wide metrics may be used without enabling TE, however.

		Returns:
			bool
		"""
		return self._get_attribute('enableWideMetric')
	@EnableWideMetric.setter
	def EnableWideMetric(self, value):
		self._set_attribute('enableWideMetric', value)

	@property
	def Enabled(self):
		"""Enables or disables the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FTagValue(self):
		"""This is a deprecated attribute in DCE ISIS mode.

		Returns:
			number
		"""
		return self._get_attribute('fTagValue')
	@FTagValue.setter
	def FTagValue(self, value):
		self._set_attribute('fTagValue', value)

	@property
	def FilterIpv4MulticastTlvs(self):
		"""If true, retrieves IPv4 Multicast learned information in the DCE ISIS mode.

		Returns:
			bool
		"""
		return self._get_attribute('filterIpv4MulticastTlvs')
	@FilterIpv4MulticastTlvs.setter
	def FilterIpv4MulticastTlvs(self, value):
		self._set_attribute('filterIpv4MulticastTlvs', value)

	@property
	def FilterIpv6MulticastTlvs(self):
		"""If true, retrieves IPv6 Multicast learned information in the DCE ISIS mode.

		Returns:
			bool
		"""
		return self._get_attribute('filterIpv6MulticastTlvs')
	@FilterIpv6MulticastTlvs.setter
	def FilterIpv6MulticastTlvs(self, value):
		self._set_attribute('filterIpv6MulticastTlvs', value)

	@property
	def FilterLearnedIpv4Prefixes(self):
		"""If true, retrieves IPv4 Unicast learned information in the ISIS L3 Routing mode.

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedIpv4Prefixes')
	@FilterLearnedIpv4Prefixes.setter
	def FilterLearnedIpv4Prefixes(self, value):
		self._set_attribute('filterLearnedIpv4Prefixes', value)

	@property
	def FilterLearnedIpv6Prefixes(self):
		"""If true, retrieves IPv6 Unicast learned information in the ISIS L3 Routing mode.

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedIpv6Prefixes')
	@FilterLearnedIpv6Prefixes.setter
	def FilterLearnedIpv6Prefixes(self, value):
		self._set_attribute('filterLearnedIpv6Prefixes', value)

	@property
	def FilterLearnedRbridges(self):
		"""If true, retrieves RBridges learned information in the DCE ISIS mode.

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedRbridges')
	@FilterLearnedRbridges.setter
	def FilterLearnedRbridges(self, value):
		self._set_attribute('filterLearnedRbridges', value)

	@property
	def FilterLearnedSpbRbridges(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedSpbRbridges')
	@FilterLearnedSpbRbridges.setter
	def FilterLearnedSpbRbridges(self, value):
		self._set_attribute('filterLearnedSpbRbridges', value)

	@property
	def FilterLearnedTrillMacUnicast(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('filterLearnedTrillMacUnicast')
	@FilterLearnedTrillMacUnicast.setter
	def FilterLearnedTrillMacUnicast(self, value):
		self._set_attribute('filterLearnedTrillMacUnicast', value)

	@property
	def FilterMacMulticastTlvs(self):
		"""If true, retrieves MAC Multicast learned information in the DCE ISIS mode.

		Returns:
			bool
		"""
		return self._get_attribute('filterMacMulticastTlvs')
	@FilterMacMulticastTlvs.setter
	def FilterMacMulticastTlvs(self, value):
		self._set_attribute('filterMacMulticastTlvs', value)

	@property
	def HostName(self):
		"""Allows to add a host name to this router.

		Returns:
			str
		"""
		return self._get_attribute('hostName')
	@HostName.setter
	def HostName(self, value):
		self._set_attribute('hostName', value)

	@property
	def InterLspMgroupPduBurstGap(self):
		"""Indicates the gap between each LSP MGROUP-PDUs.

		Returns:
			number
		"""
		return self._get_attribute('interLspMgroupPduBurstGap')
	@InterLspMgroupPduBurstGap.setter
	def InterLspMgroupPduBurstGap(self, value):
		self._set_attribute('interLspMgroupPduBurstGap', value)

	@property
	def LspLifeTime(self):
		"""(in sec) The MaxAge for retaining a learned LSP on this router. The default value is 1,200 sec.

		Returns:
			number
		"""
		return self._get_attribute('lspLifeTime')
	@LspLifeTime.setter
	def LspLifeTime(self, value):
		self._set_attribute('lspLifeTime', value)

	@property
	def LspMaxSize(self):
		"""(in bytes) The maximum allowable length of an ISIS LSP message. The default is 1,492 bytes.

		Returns:
			number
		"""
		return self._get_attribute('lspMaxSize')
	@LspMaxSize.setter
	def LspMaxSize(self, value):
		self._set_attribute('lspMaxSize', value)

	@property
	def LspMgroupPduMinTransmissionInterval(self):
		"""Indicates the minimum wait time for each LSP MGROUP-PDU transmission.

		Returns:
			number
		"""
		return self._get_attribute('lspMgroupPduMinTransmissionInterval')
	@LspMgroupPduMinTransmissionInterval.setter
	def LspMgroupPduMinTransmissionInterval(self, value):
		self._set_attribute('lspMgroupPduMinTransmissionInterval', value)

	@property
	def LspRefreshRate(self):
		"""(in sec) The rate at which LSPs are resent. The default value is 900 sec.

		Returns:
			number
		"""
		return self._get_attribute('lspRefreshRate')
	@LspRefreshRate.setter
	def LspRefreshRate(self, value):
		self._set_attribute('lspRefreshRate', value)

	@property
	def MaxAreaAddresses(self):
		"""The number of area addresses permitted for this IS area.

		Returns:
			number
		"""
		return self._get_attribute('maxAreaAddresses')
	@MaxAreaAddresses.setter
	def MaxAreaAddresses(self, value):
		self._set_attribute('maxAreaAddresses', value)

	@property
	def MaxLspMgroupPdusPerBurst(self):
		"""Indicates the maximum number of LSP MGROUP-PDUs for each burst.

		Returns:
			number
		"""
		return self._get_attribute('maxLspMgroupPdusPerBurst')
	@MaxLspMgroupPdusPerBurst.setter
	def MaxLspMgroupPdusPerBurst(self, value):
		self._set_attribute('maxLspMgroupPdusPerBurst', value)

	@property
	def NumberOfMtuProbes(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numberOfMtuProbes')
	@NumberOfMtuProbes.setter
	def NumberOfMtuProbes(self, value):
		self._set_attribute('numberOfMtuProbes', value)

	@property
	def NumberOfMultiDestinationTrees(self):
		"""The number of Multi-Destination Trees for the emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMultiDestinationTrees')
	@NumberOfMultiDestinationTrees.setter
	def NumberOfMultiDestinationTrees(self, value):
		self._set_attribute('numberOfMultiDestinationTrees', value)

	@property
	def OriginatingLspBufSize(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('originatingLspBufSize')
	@OriginatingLspBufSize.setter
	def OriginatingLspBufSize(self, value):
		self._set_attribute('originatingLspBufSize', value)

	@property
	def PsnpInterval(self):
		"""The PSPN Interval.

		Returns:
			number
		"""
		return self._get_attribute('psnpInterval')
	@PsnpInterval.setter
	def PsnpInterval(self, value):
		self._set_attribute('psnpInterval', value)

	@property
	def RestartMode(self):
		"""If enableHitlessRestart is true, this indicates the mode in which this router is to operate.

		Returns:
			str(normalRouter|restartingRouter|startingRouter|helperRouter)
		"""
		return self._get_attribute('restartMode')
	@RestartMode.setter
	def RestartMode(self, value):
		self._set_attribute('restartMode', value)

	@property
	def RestartTime(self):
		"""Enter the restart time in seconds.

		Returns:
			number
		"""
		return self._get_attribute('restartTime')
	@RestartTime.setter
	def RestartTime(self, value):
		self._set_attribute('restartTime', value)

	@property
	def RestartVersion(self):
		"""If enableHitlessRestart is true, this indicates the version of the draft-ietf-isis-restart-nn document that the router should conform to.

		Returns:
			str(version3|version4)
		"""
		return self._get_attribute('restartVersion')
	@RestartVersion.setter
	def RestartVersion(self, value):
		self._set_attribute('restartVersion', value)

	@property
	def StartFtagValue(self):
		"""The starting FTAG value of the emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('startFtagValue')
	@StartFtagValue.setter
	def StartFtagValue(self, value):
		self._set_attribute('startFtagValue', value)

	@property
	def SwitchId(self):
		"""The Switch ID of the emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('switchId')
	@SwitchId.setter
	def SwitchId(self, value):
		self._set_attribute('switchId', value)

	@property
	def SwitchIdPriority(self):
		"""The Switch ID priority of the emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('switchIdPriority')
	@SwitchIdPriority.setter
	def SwitchIdPriority(self, value):
		self._set_attribute('switchIdPriority', value)

	@property
	def SystemId(self):
		"""The neighbor's system ID.

		Returns:
			str
		"""
		return self._get_attribute('systemId')
	@SystemId.setter
	def SystemId(self, value):
		self._set_attribute('systemId', value)

	@property
	def TeEnable(self):
		"""Enables traffic engineering (TE) on this emulated ISIS router.

		Returns:
			bool
		"""
		return self._get_attribute('teEnable')
	@TeEnable.setter
	def TeEnable(self, value):
		self._set_attribute('teEnable', value)

	@property
	def TeRouterId(self):
		"""The ID of the simulated router, expressed as an IP address.

		Returns:
			str
		"""
		return self._get_attribute('teRouterId')
	@TeRouterId.setter
	def TeRouterId(self, value):
		self._set_attribute('teRouterId', value)

	@property
	def TrafficGroupId(self):
		"""Contains the object reference to a traffic group identifier as configured with the trafficGroup object.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, AreaAddressList=None, AreaAuthType=None, AreaReceivedPasswordList=None, AreaTransmitPassword=None, BroadcastRootPriority=None, CapabilityRouterId=None, DeviceId=None, DevicePriority=None, DomainAuthType=None, DomainReceivedPasswordList=None, DomainTransmitPassword=None, EnableAttached=None, EnableAutoLoopback=None, EnableDiscardLearnedLsps=None, EnableHelloPadding=None, EnableHitlessRestart=None, EnableHostName=None, EnableIgnoreMtPortCapability=None, EnableIgnoreRecvMd5=None, EnableMtIpv6=None, EnableMtuProbe=None, EnableMultiTopology=None, EnableOverloaded=None, EnablePartitionRepair=None, EnableTrillOam=None, EnableWideMetric=None, Enabled=None, FTagValue=None, FilterIpv4MulticastTlvs=None, FilterIpv6MulticastTlvs=None, FilterLearnedIpv4Prefixes=None, FilterLearnedIpv6Prefixes=None, FilterLearnedRbridges=None, FilterLearnedSpbRbridges=None, FilterLearnedTrillMacUnicast=None, FilterMacMulticastTlvs=None, HostName=None, InterLspMgroupPduBurstGap=None, LspLifeTime=None, LspMaxSize=None, LspMgroupPduMinTransmissionInterval=None, LspRefreshRate=None, MaxAreaAddresses=None, MaxLspMgroupPdusPerBurst=None, NumberOfMtuProbes=None, NumberOfMultiDestinationTrees=None, OriginatingLspBufSize=None, PsnpInterval=None, RestartMode=None, RestartTime=None, RestartVersion=None, StartFtagValue=None, SwitchId=None, SwitchIdPriority=None, SystemId=None, TeEnable=None, TeRouterId=None, TrafficGroupId=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			AreaAddressList (list(str)): The list of area addresses to use.
			AreaAuthType (str(none|password|md5)): Sets up authentication for Level 1 LSPs.
			AreaReceivedPasswordList (list(str)): If areaAuthType is isisAuthTypePassword, then this is a list of passwords that the router will accept on received LSPs.
			AreaTransmitPassword (str): If areaAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted LSPs.
			BroadcastRootPriority (number): The value of the Broadcast Root Priority of a particular DCE ISIS router.
			CapabilityRouterId (str): The IPv4 address format of the Capability Router.
			DeviceId (number): This is a deprecated attribute in DCE ISIS mode.
			DevicePriority (number): This is a deprecated attribute in DCE ISIS mode.
			DomainAuthType (str(none|password|md5)): Sets up authentication for Level 2 LSPs.
			DomainReceivedPasswordList (list(str)): If domainAuthType is isisAuthTypePassword, then this is a list of passwords that the router will accept on received LSPs.
			DomainTransmitPassword (str): If domainAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted LSPs.
			EnableAttached (bool): Indicates that the Attached Flag is set. It indicates that this ISIS router can use L2 routing to reach other areas.
			EnableAutoLoopback (bool): If enabled, loopback addresses are allowed in the generated routes.
			EnableDiscardLearnedLsps (bool): If enabled, LSPs learned from this router's interfaces will be discarded.
			EnableHelloPadding (bool): If true, enables padding of hello messages.
			EnableHitlessRestart (bool): Hitless Restart is enabled for this emulated ISIS router.
			EnableHostName (bool): If true, the given dynamic host name is transmitted in all the packets sent from this router.
			EnableIgnoreMtPortCapability (bool): NOT DEFINED
			EnableIgnoreRecvMd5 (bool): MD5 authentication will be disabled for incoming/received packets.
			EnableMtIpv6 (bool): If checked in L3, emulation type traffic group ID at router level is grayed out and unassigned.
			EnableMtuProbe (bool): NOT DEFINED
			EnableMultiTopology (bool): Enables more than one topology (distribution tree) corresponding to the given R bridge.
			EnableOverloaded (bool): If enabled, the LSP Database Overload Bit is set. It indicates that the LSP database on this router is overloaded and that there is not enough memory to store a received LSP. This router enters the Waiting State and floods an LSP (with LSP number = 0) with the overload bit set, so other routers will not forward ISIS packets to it.
			EnablePartitionRepair (bool): Enables the optional partition repair option specified in ISO/IEC 10589 and RFC 1195 for Level 1 areas.
			EnableTrillOam (bool): NOT DEFINED
			EnableWideMetric (bool): Enables the use of extended reachability (wide) metrics (defined to support TE): 32-bits wide for IP reachability (routes) and 24-bits wide for IS reachability (IS neighbors). If TE is enabled, wide metrics will be enabled automatically. The wide metrics may be used without enabling TE, however.
			Enabled (bool): Enables or disables the simulated router.
			FTagValue (number): This is a deprecated attribute in DCE ISIS mode.
			FilterIpv4MulticastTlvs (bool): If true, retrieves IPv4 Multicast learned information in the DCE ISIS mode.
			FilterIpv6MulticastTlvs (bool): If true, retrieves IPv6 Multicast learned information in the DCE ISIS mode.
			FilterLearnedIpv4Prefixes (bool): If true, retrieves IPv4 Unicast learned information in the ISIS L3 Routing mode.
			FilterLearnedIpv6Prefixes (bool): If true, retrieves IPv6 Unicast learned information in the ISIS L3 Routing mode.
			FilterLearnedRbridges (bool): If true, retrieves RBridges learned information in the DCE ISIS mode.
			FilterLearnedSpbRbridges (bool): NOT DEFINED
			FilterLearnedTrillMacUnicast (bool): NOT DEFINED
			FilterMacMulticastTlvs (bool): If true, retrieves MAC Multicast learned information in the DCE ISIS mode.
			HostName (str): Allows to add a host name to this router.
			InterLspMgroupPduBurstGap (number): Indicates the gap between each LSP MGROUP-PDUs.
			LspLifeTime (number): (in sec) The MaxAge for retaining a learned LSP on this router. The default value is 1,200 sec.
			LspMaxSize (number): (in bytes) The maximum allowable length of an ISIS LSP message. The default is 1,492 bytes.
			LspMgroupPduMinTransmissionInterval (number): Indicates the minimum wait time for each LSP MGROUP-PDU transmission.
			LspRefreshRate (number): (in sec) The rate at which LSPs are resent. The default value is 900 sec.
			MaxAreaAddresses (number): The number of area addresses permitted for this IS area.
			MaxLspMgroupPdusPerBurst (number): Indicates the maximum number of LSP MGROUP-PDUs for each burst.
			NumberOfMtuProbes (number): NOT DEFINED
			NumberOfMultiDestinationTrees (number): The number of Multi-Destination Trees for the emulated DCE ISIS router.
			OriginatingLspBufSize (number): NOT DEFINED
			PsnpInterval (number): The PSPN Interval.
			RestartMode (str(normalRouter|restartingRouter|startingRouter|helperRouter)): If enableHitlessRestart is true, this indicates the mode in which this router is to operate.
			RestartTime (number): Enter the restart time in seconds.
			RestartVersion (str(version3|version4)): If enableHitlessRestart is true, this indicates the version of the draft-ietf-isis-restart-nn document that the router should conform to.
			StartFtagValue (number): The starting FTAG value of the emulated DCE ISIS router.
			SwitchId (number): The Switch ID of the emulated DCE ISIS router.
			SwitchIdPriority (number): The Switch ID priority of the emulated DCE ISIS router.
			SystemId (str): The neighbor's system ID.
			TeEnable (bool): Enables traffic engineering (TE) on this emulated ISIS router.
			TeRouterId (str): The ID of the simulated router, expressed as an IP address.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Contains the object reference to a traffic group identifier as configured with the trafficGroup object.

		Returns:
			self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the router data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AreaAddressList=None, AreaAuthType=None, AreaReceivedPasswordList=None, AreaTransmitPassword=None, BroadcastRootPriority=None, CapabilityRouterId=None, DeviceId=None, DevicePriority=None, DomainAuthType=None, DomainReceivedPasswordList=None, DomainTransmitPassword=None, EnableAttached=None, EnableAutoLoopback=None, EnableDiscardLearnedLsps=None, EnableHelloPadding=None, EnableHitlessRestart=None, EnableHostName=None, EnableIgnoreMtPortCapability=None, EnableIgnoreRecvMd5=None, EnableMtIpv6=None, EnableMtuProbe=None, EnableMultiTopology=None, EnableOverloaded=None, EnablePartitionRepair=None, EnableTrillOam=None, EnableWideMetric=None, Enabled=None, FTagValue=None, FilterIpv4MulticastTlvs=None, FilterIpv6MulticastTlvs=None, FilterLearnedIpv4Prefixes=None, FilterLearnedIpv6Prefixes=None, FilterLearnedRbridges=None, FilterLearnedSpbRbridges=None, FilterLearnedTrillMacUnicast=None, FilterMacMulticastTlvs=None, HostName=None, InterLspMgroupPduBurstGap=None, LspLifeTime=None, LspMaxSize=None, LspMgroupPduMinTransmissionInterval=None, LspRefreshRate=None, MaxAreaAddresses=None, MaxLspMgroupPdusPerBurst=None, NumberOfMtuProbes=None, NumberOfMultiDestinationTrees=None, OriginatingLspBufSize=None, PsnpInterval=None, RestartMode=None, RestartTime=None, RestartVersion=None, StartFtagValue=None, SwitchId=None, SwitchIdPriority=None, SystemId=None, TeEnable=None, TeRouterId=None, TrafficGroupId=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			AreaAddressList (list(str)): The list of area addresses to use.
			AreaAuthType (str(none|password|md5)): Sets up authentication for Level 1 LSPs.
			AreaReceivedPasswordList (list(str)): If areaAuthType is isisAuthTypePassword, then this is a list of passwords that the router will accept on received LSPs.
			AreaTransmitPassword (str): If areaAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted LSPs.
			BroadcastRootPriority (number): The value of the Broadcast Root Priority of a particular DCE ISIS router.
			CapabilityRouterId (str): The IPv4 address format of the Capability Router.
			DeviceId (number): This is a deprecated attribute in DCE ISIS mode.
			DevicePriority (number): This is a deprecated attribute in DCE ISIS mode.
			DomainAuthType (str(none|password|md5)): Sets up authentication for Level 2 LSPs.
			DomainReceivedPasswordList (list(str)): If domainAuthType is isisAuthTypePassword, then this is a list of passwords that the router will accept on received LSPs.
			DomainTransmitPassword (str): If domainAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted LSPs.
			EnableAttached (bool): Indicates that the Attached Flag is set. It indicates that this ISIS router can use L2 routing to reach other areas.
			EnableAutoLoopback (bool): If enabled, loopback addresses are allowed in the generated routes.
			EnableDiscardLearnedLsps (bool): If enabled, LSPs learned from this router's interfaces will be discarded.
			EnableHelloPadding (bool): If true, enables padding of hello messages.
			EnableHitlessRestart (bool): Hitless Restart is enabled for this emulated ISIS router.
			EnableHostName (bool): If true, the given dynamic host name is transmitted in all the packets sent from this router.
			EnableIgnoreMtPortCapability (bool): NOT DEFINED
			EnableIgnoreRecvMd5 (bool): MD5 authentication will be disabled for incoming/received packets.
			EnableMtIpv6 (bool): If checked in L3, emulation type traffic group ID at router level is grayed out and unassigned.
			EnableMtuProbe (bool): NOT DEFINED
			EnableMultiTopology (bool): Enables more than one topology (distribution tree) corresponding to the given R bridge.
			EnableOverloaded (bool): If enabled, the LSP Database Overload Bit is set. It indicates that the LSP database on this router is overloaded and that there is not enough memory to store a received LSP. This router enters the Waiting State and floods an LSP (with LSP number = 0) with the overload bit set, so other routers will not forward ISIS packets to it.
			EnablePartitionRepair (bool): Enables the optional partition repair option specified in ISO/IEC 10589 and RFC 1195 for Level 1 areas.
			EnableTrillOam (bool): NOT DEFINED
			EnableWideMetric (bool): Enables the use of extended reachability (wide) metrics (defined to support TE): 32-bits wide for IP reachability (routes) and 24-bits wide for IS reachability (IS neighbors). If TE is enabled, wide metrics will be enabled automatically. The wide metrics may be used without enabling TE, however.
			Enabled (bool): Enables or disables the simulated router.
			FTagValue (number): This is a deprecated attribute in DCE ISIS mode.
			FilterIpv4MulticastTlvs (bool): If true, retrieves IPv4 Multicast learned information in the DCE ISIS mode.
			FilterIpv6MulticastTlvs (bool): If true, retrieves IPv6 Multicast learned information in the DCE ISIS mode.
			FilterLearnedIpv4Prefixes (bool): If true, retrieves IPv4 Unicast learned information in the ISIS L3 Routing mode.
			FilterLearnedIpv6Prefixes (bool): If true, retrieves IPv6 Unicast learned information in the ISIS L3 Routing mode.
			FilterLearnedRbridges (bool): If true, retrieves RBridges learned information in the DCE ISIS mode.
			FilterLearnedSpbRbridges (bool): NOT DEFINED
			FilterLearnedTrillMacUnicast (bool): NOT DEFINED
			FilterMacMulticastTlvs (bool): If true, retrieves MAC Multicast learned information in the DCE ISIS mode.
			HostName (str): Allows to add a host name to this router.
			InterLspMgroupPduBurstGap (number): Indicates the gap between each LSP MGROUP-PDUs.
			LspLifeTime (number): (in sec) The MaxAge for retaining a learned LSP on this router. The default value is 1,200 sec.
			LspMaxSize (number): (in bytes) The maximum allowable length of an ISIS LSP message. The default is 1,492 bytes.
			LspMgroupPduMinTransmissionInterval (number): Indicates the minimum wait time for each LSP MGROUP-PDU transmission.
			LspRefreshRate (number): (in sec) The rate at which LSPs are resent. The default value is 900 sec.
			MaxAreaAddresses (number): The number of area addresses permitted for this IS area.
			MaxLspMgroupPdusPerBurst (number): Indicates the maximum number of LSP MGROUP-PDUs for each burst.
			NumberOfMtuProbes (number): NOT DEFINED
			NumberOfMultiDestinationTrees (number): The number of Multi-Destination Trees for the emulated DCE ISIS router.
			OriginatingLspBufSize (number): NOT DEFINED
			PsnpInterval (number): The PSPN Interval.
			RestartMode (str(normalRouter|restartingRouter|startingRouter|helperRouter)): If enableHitlessRestart is true, this indicates the mode in which this router is to operate.
			RestartTime (number): Enter the restart time in seconds.
			RestartVersion (str(version3|version4)): If enableHitlessRestart is true, this indicates the version of the draft-ietf-isis-restart-nn document that the router should conform to.
			StartFtagValue (number): The starting FTAG value of the emulated DCE ISIS router.
			SwitchId (number): The Switch ID of the emulated DCE ISIS router.
			SwitchIdPriority (number): The Switch ID priority of the emulated DCE ISIS router.
			SystemId (str): The neighbor's system ID.
			TeEnable (bool): Enables traffic engineering (TE) on this emulated ISIS router.
			TeRouterId (str): The ID of the simulated router, expressed as an IP address.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Contains the object reference to a traffic group identifier as configured with the trafficGroup object.

		Returns:
			self: This instance with matching router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshLearnedInformation(self):
		"""Executes the refreshLearnedInformation operation on the server.

		This option refreshes the learned information of ISIS router.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: Boolean.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInformation', payload=locals(), response_object=None)

	def SendTrillOamPing(self):
		"""Executes the sendTrillOamPing operation on the server.

		This option will send trill OAM ping.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: Boolean.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendTrillOamPing', payload=locals(), response_object=None)
