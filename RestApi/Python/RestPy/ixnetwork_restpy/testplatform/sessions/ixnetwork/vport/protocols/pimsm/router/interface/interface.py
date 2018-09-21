from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interface(Base):
	"""The Interface class encapsulates a user managed interface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def CrpRange(self):
		"""An instance of the CrpRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.crprange.crprange.CrpRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.crprange.crprange import CrpRange
		return CrpRange(self)

	@property
	def DataMdt(self):
		"""An instance of the DataMdt class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.datamdt.datamdt.DataMdt)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.datamdt.datamdt import DataMdt
		return DataMdt(self)

	@property
	def JoinPrune(self):
		"""An instance of the JoinPrune class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.joinprune.JoinPrune)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.joinprune.joinprune import JoinPrune
		return JoinPrune(self)

	@property
	def LearnedBsrInfo(self):
		"""An instance of the LearnedBsrInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedbsrinfo.learnedbsrinfo.LearnedBsrInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedbsrinfo.learnedbsrinfo import LearnedBsrInfo
		return LearnedBsrInfo(self)

	@property
	def LearnedCrpInfo(self):
		"""An instance of the LearnedCrpInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedcrpinfo.learnedcrpinfo.LearnedCrpInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedcrpinfo.learnedcrpinfo import LearnedCrpInfo
		return LearnedCrpInfo(self)

	@property
	def LearnedMdtInfo(self):
		"""An instance of the LearnedMdtInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedmdtinfo.learnedmdtinfo.LearnedMdtInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.learnedmdtinfo.learnedmdtinfo import LearnedMdtInfo
		return LearnedMdtInfo(self)

	@property
	def Source(self):
		"""An instance of the Source class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.source.source.Source)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.source.source import Source
		return Source(self)

	@property
	def AddressFamily(self):
		"""Choose an Address Family for this PIM-SM Interface.

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('addressFamily')
	@AddressFamily.setter
	def AddressFamily(self, value):
		self._set_attribute('addressFamily', value)

	@property
	def AutoPickUpstreamNeighbor(self):
		"""Enables the time-saving Auto Pick feature and the Upstream Neighbor field is not available for use. The Upstream Neighbor address used in the Join/Prune message is determined automatically from received Hello messages. The first time a Hello message is received - containing a Source (link-local) address that does not belong to this interface, that source address will be used as the Upstream Neighbor address.

		Returns:
			bool
		"""
		return self._get_attribute('autoPickUpstreamNeighbor')
	@AutoPickUpstreamNeighbor.setter
	def AutoPickUpstreamNeighbor(self, value):
		self._set_attribute('autoPickUpstreamNeighbor', value)

	@property
	def BootstrapEnable(self):
		"""If checked, enables the PIM-SM interface to participate in Bootstrap Router election procedure.

		Returns:
			bool
		"""
		return self._get_attribute('bootstrapEnable')
	@BootstrapEnable.setter
	def BootstrapEnable(self, value):
		self._set_attribute('bootstrapEnable', value)

	@property
	def BootstrapHashMaskLen(self):
		"""Hash Mask Length of the Bootstrap Router (BSR) that is set with the same name in all Bootstrap Messages sent by this BSR.

		Returns:
			number
		"""
		return self._get_attribute('bootstrapHashMaskLen')
	@BootstrapHashMaskLen.setter
	def BootstrapHashMaskLen(self, value):
		self._set_attribute('bootstrapHashMaskLen', value)

	@property
	def BootstrapInterval(self):
		"""The time interval (in seconds) between two consecutive bootstrap messages sent by the BSR.

		Returns:
			number
		"""
		return self._get_attribute('bootstrapInterval')
	@BootstrapInterval.setter
	def BootstrapInterval(self, value):
		self._set_attribute('bootstrapInterval', value)

	@property
	def BootstrapPriority(self):
		"""Priority of the Bootstrap Router (BSR) that is set with the same name in all Bootstrap Messages sent by this BSR.

		Returns:
			number
		"""
		return self._get_attribute('bootstrapPriority')
	@BootstrapPriority.setter
	def BootstrapPriority(self, value):
		self._set_attribute('bootstrapPriority', value)

	@property
	def BootstrapTimeout(self):
		"""Amount of time (in seconds) of not receiving any Bootstrap Messages, after which the BSR if candidate at that point of time will decide that the currently elected BSR has gone down and will restart BSR election procedure.

		Returns:
			number
		"""
		return self._get_attribute('bootstrapTimeout')
	@BootstrapTimeout.setter
	def BootstrapTimeout(self, value):
		self._set_attribute('bootstrapTimeout', value)

	@property
	def DisableTriggeredHello(self):
		"""If enabled, the triggered hello delay function is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('disableTriggeredHello')
	@DisableTriggeredHello.setter
	def DisableTriggeredHello(self, value):
		self._set_attribute('disableTriggeredHello', value)

	@property
	def DiscardDataMdtTlv(self):
		"""If enabled, received Data MDT TLVs will be discarded.

		Returns:
			bool
		"""
		return self._get_attribute('discardDataMdtTlv')
	@DiscardDataMdtTlv.setter
	def DiscardDataMdtTlv(self, value):
		self._set_attribute('discardDataMdtTlv', value)

	@property
	def DiscardLearnedRpInfo(self):
		"""If checked, disregards group mappings learnt from Bootstrap Message (in case not acting as elected BSR) or from Candidate RP Advertisement (in case of elected BSR).

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedRpInfo')
	@DiscardLearnedRpInfo.setter
	def DiscardLearnedRpInfo(self, value):
		self._set_attribute('discardLearnedRpInfo', value)

	@property
	def EnableBfdRegistration(self):
		"""Indicates if a BFD session is to be created to the PIMSM peer IP address once the PIMSM session is established. This allows PIMSM to use BFD to maintain IPv4 connectivity the PIMSM peer.

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableV4MappedV6Address(self):
		"""Use IpV4 mapped IpV6 address

		Returns:
			bool
		"""
		return self._get_attribute('enableV4MappedV6Address')
	@EnableV4MappedV6Address.setter
	def EnableV4MappedV6Address(self, value):
		self._set_attribute('enableV4MappedV6Address', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of the interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ForceSemanticFragmentation(self):
		"""If enabled, this forces the BSR to send only one group specific RP list per bootstrap message.

		Returns:
			bool
		"""
		return self._get_attribute('forceSemanticFragmentation')
	@ForceSemanticFragmentation.setter
	def ForceSemanticFragmentation(self, value):
		self._set_attribute('forceSemanticFragmentation', value)

	@property
	def GenerationIdMode(self):
		"""The mode used for creating the 32-bit value for the Generation ID. This can either be incrementing, random or constant. (default = constant)

		Returns:
			str(incremental|random|constant)
		"""
		return self._get_attribute('generationIdMode')
	@GenerationIdMode.setter
	def GenerationIdMode(self, value):
		self._set_attribute('generationIdMode', value)

	@property
	def HelloHoldTime(self):
		"""The amount of time that neighbor routers should hold the interface as reachable.

		Returns:
			number
		"""
		return self._get_attribute('helloHoldTime')
	@HelloHoldTime.setter
	def HelloHoldTime(self, value):
		self._set_attribute('helloHoldTime', value)

	@property
	def HelloInterval(self):
		"""The interval between transmitted hello messages.

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def InterfaceId(self):
		"""The identifier for this PIM-SM Interface.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this PIM-SM interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this PIM-SM interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""The interfaces that are associated with the selected interface type.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def IsRefreshRpSetComplete(self):
		"""If enabled, shows the desired set of RPs.

		Returns:
			bool
		"""
		return self._get_attribute('isRefreshRpSetComplete')

	@property
	def LanPruneDelay(self):
		"""The value of the LAN Prune (propagation) Delay for this PIM-SM interface. The expected delay for messages propagated on the link. It indicates to an upstream router how long to wait for a Join override message before it prunes an interface.The default value is 500 msec. The valid range is 100 to 0x7FFF msec. (LAN Prune Delay is an Option included in Hello messages.)

		Returns:
			number
		"""
		return self._get_attribute('lanPruneDelay')
	@LanPruneDelay.setter
	def LanPruneDelay(self, value):
		self._set_attribute('lanPruneDelay', value)

	@property
	def LanPruneDelayTBit(self):
		"""If enabled, the T flag bit in the LAN Prune Delay option of the Hello message is set (= 1). Setting this bit specifies that the sending PIM-SM router has the ability to disable Join message suppression.

		Returns:
			bool
		"""
		return self._get_attribute('lanPruneDelayTBit')
	@LanPruneDelayTBit.setter
	def LanPruneDelayTBit(self, value):
		self._set_attribute('lanPruneDelayTBit', value)

	@property
	def LearnSelectedRpSet(self):
		"""If enabled, this displays only the best RP per group (member of selected RP set).

		Returns:
			bool
		"""
		return self._get_attribute('learnSelectedRpSet')
	@LearnSelectedRpSet.setter
	def LearnSelectedRpSet(self, value):
		self._set_attribute('learnSelectedRpSet', value)

	@property
	def OverrideInterval(self):
		"""The delay interval, in milliseconds, for randomizing the transmission time for override messages, which are used when scheduling a delayed Join message. This is part of the LAN Prune Delay option included in Hello messages. The valid range is 100 to 7FFF msec. (default = 2500)

		Returns:
			number
		"""
		return self._get_attribute('overrideInterval')
	@OverrideInterval.setter
	def OverrideInterval(self, value):
		self._set_attribute('overrideInterval', value)

	@property
	def SendBiDirCapableOption(self):
		"""If enabled, sets the bidirectional PIM-SM flag bit (=1), per IETF DRAFT draft-ietf-pim-bidir-04.

		Returns:
			bool
		"""
		return self._get_attribute('sendBiDirCapableOption')
	@SendBiDirCapableOption.setter
	def SendBiDirCapableOption(self, value):
		self._set_attribute('sendBiDirCapableOption', value)

	@property
	def SendGenIdOption(self):
		"""Enables the send generation ID option.

		Returns:
			bool
		"""
		return self._get_attribute('sendGenIdOption')
	@SendGenIdOption.setter
	def SendGenIdOption(self, value):
		self._set_attribute('sendGenIdOption', value)

	@property
	def SendHelloLanPruneDelayOption(self):
		"""If set, the LAN Prune propagation delay is enabled for this interface, as indicated in the pruneDelay option. The option is indicated in Hello messages from the interface. (default = true)

		Returns:
			bool
		"""
		return self._get_attribute('sendHelloLanPruneDelayOption')
	@SendHelloLanPruneDelayOption.setter
	def SendHelloLanPruneDelayOption(self, value):
		self._set_attribute('sendHelloLanPruneDelayOption', value)

	@property
	def ShowSelectedRpSetOnly(self):
		"""If enabled, this displays only the best RP per group (member of selected RP set).

		Returns:
			bool
		"""
		return self._get_attribute('showSelectedRpSetOnly')
	@ShowSelectedRpSetOnly.setter
	def ShowSelectedRpSetOnly(self, value):
		self._set_attribute('showSelectedRpSetOnly', value)

	@property
	def SupportUnicastBootstrap(self):
		"""If enabled, this supports the sending and processing of Unicast bootstrap messages.

		Returns:
			bool
		"""
		return self._get_attribute('supportUnicastBootstrap')
	@SupportUnicastBootstrap.setter
	def SupportUnicastBootstrap(self, value):
		self._set_attribute('supportUnicastBootstrap', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this emulated router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def TriggeredHelloDelay(self):
		"""The time (in seconds) after which the router senses a delay in sending or receiving PIM-SM hello message.

		Returns:
			number
		"""
		return self._get_attribute('triggeredHelloDelay')
	@TriggeredHelloDelay.setter
	def TriggeredHelloDelay(self, value):
		self._set_attribute('triggeredHelloDelay', value)

	@property
	def UpstreamNeighbor(self):
		"""The IP address of the upstream neighbor.

		Returns:
			str
		"""
		return self._get_attribute('upstreamNeighbor')
	@UpstreamNeighbor.setter
	def UpstreamNeighbor(self, value):
		self._set_attribute('upstreamNeighbor', value)

	def add(self, AddressFamily=None, AutoPickUpstreamNeighbor=None, BootstrapEnable=None, BootstrapHashMaskLen=None, BootstrapInterval=None, BootstrapPriority=None, BootstrapTimeout=None, DisableTriggeredHello=None, DiscardDataMdtTlv=None, DiscardLearnedRpInfo=None, EnableBfdRegistration=None, EnableV4MappedV6Address=None, Enabled=None, ForceSemanticFragmentation=None, GenerationIdMode=None, HelloHoldTime=None, HelloInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, LanPruneDelay=None, LanPruneDelayTBit=None, LearnSelectedRpSet=None, OverrideInterval=None, SendBiDirCapableOption=None, SendGenIdOption=None, SendHelloLanPruneDelayOption=None, ShowSelectedRpSetOnly=None, SupportUnicastBootstrap=None, TrafficGroupId=None, TriggeredHelloDelay=None, UpstreamNeighbor=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AddressFamily (str(ipv4|ipv6)): Choose an Address Family for this PIM-SM Interface.
			AutoPickUpstreamNeighbor (bool): Enables the time-saving Auto Pick feature and the Upstream Neighbor field is not available for use. The Upstream Neighbor address used in the Join/Prune message is determined automatically from received Hello messages. The first time a Hello message is received - containing a Source (link-local) address that does not belong to this interface, that source address will be used as the Upstream Neighbor address.
			BootstrapEnable (bool): If checked, enables the PIM-SM interface to participate in Bootstrap Router election procedure.
			BootstrapHashMaskLen (number): Hash Mask Length of the Bootstrap Router (BSR) that is set with the same name in all Bootstrap Messages sent by this BSR.
			BootstrapInterval (number): The time interval (in seconds) between two consecutive bootstrap messages sent by the BSR.
			BootstrapPriority (number): Priority of the Bootstrap Router (BSR) that is set with the same name in all Bootstrap Messages sent by this BSR.
			BootstrapTimeout (number): Amount of time (in seconds) of not receiving any Bootstrap Messages, after which the BSR if candidate at that point of time will decide that the currently elected BSR has gone down and will restart BSR election procedure.
			DisableTriggeredHello (bool): If enabled, the triggered hello delay function is disabled.
			DiscardDataMdtTlv (bool): If enabled, received Data MDT TLVs will be discarded.
			DiscardLearnedRpInfo (bool): If checked, disregards group mappings learnt from Bootstrap Message (in case not acting as elected BSR) or from Candidate RP Advertisement (in case of elected BSR).
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the PIMSM peer IP address once the PIMSM session is established. This allows PIMSM to use BFD to maintain IPv4 connectivity the PIMSM peer.
			EnableV4MappedV6Address (bool): Use IpV4 mapped IpV6 address
			Enabled (bool): Enables or disables the use of the interface.
			ForceSemanticFragmentation (bool): If enabled, this forces the BSR to send only one group specific RP list per bootstrap message.
			GenerationIdMode (str(incremental|random|constant)): The mode used for creating the 32-bit value for the Generation ID. This can either be incrementing, random or constant. (default = constant)
			HelloHoldTime (number): The amount of time that neighbor routers should hold the interface as reachable.
			HelloInterval (number): The interval between transmitted hello messages.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The identifier for this PIM-SM Interface.
			InterfaceIndex (number): The assigned protocol interface ID for this PIM-SM interface.
			InterfaceType (str): The type of interface to be selected for this PIM-SM interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			LanPruneDelay (number): The value of the LAN Prune (propagation) Delay for this PIM-SM interface. The expected delay for messages propagated on the link. It indicates to an upstream router how long to wait for a Join override message before it prunes an interface.The default value is 500 msec. The valid range is 100 to 0x7FFF msec. (LAN Prune Delay is an Option included in Hello messages.)
			LanPruneDelayTBit (bool): If enabled, the T flag bit in the LAN Prune Delay option of the Hello message is set (= 1). Setting this bit specifies that the sending PIM-SM router has the ability to disable Join message suppression.
			LearnSelectedRpSet (bool): If enabled, this displays only the best RP per group (member of selected RP set).
			OverrideInterval (number): The delay interval, in milliseconds, for randomizing the transmission time for override messages, which are used when scheduling a delayed Join message. This is part of the LAN Prune Delay option included in Hello messages. The valid range is 100 to 7FFF msec. (default = 2500)
			SendBiDirCapableOption (bool): If enabled, sets the bidirectional PIM-SM flag bit (=1), per IETF DRAFT draft-ietf-pim-bidir-04.
			SendGenIdOption (bool): Enables the send generation ID option.
			SendHelloLanPruneDelayOption (bool): If set, the LAN Prune propagation delay is enabled for this interface, as indicated in the pruneDelay option. The option is indicated in Hello messages from the interface. (default = true)
			ShowSelectedRpSetOnly (bool): If enabled, this displays only the best RP per group (member of selected RP set).
			SupportUnicastBootstrap (bool): If enabled, this supports the sending and processing of Unicast bootstrap messages.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this emulated router is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			TriggeredHelloDelay (number): The time (in seconds) after which the router senses a delay in sending or receiving PIM-SM hello message.
			UpstreamNeighbor (str): The IP address of the upstream neighbor.

		Returns:
			self: This instance with all currently retrieved interface data using find and the newly added interface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddressFamily=None, AutoPickUpstreamNeighbor=None, BootstrapEnable=None, BootstrapHashMaskLen=None, BootstrapInterval=None, BootstrapPriority=None, BootstrapTimeout=None, DisableTriggeredHello=None, DiscardDataMdtTlv=None, DiscardLearnedRpInfo=None, EnableBfdRegistration=None, EnableV4MappedV6Address=None, Enabled=None, ForceSemanticFragmentation=None, GenerationIdMode=None, HelloHoldTime=None, HelloInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, IsRefreshRpSetComplete=None, LanPruneDelay=None, LanPruneDelayTBit=None, LearnSelectedRpSet=None, OverrideInterval=None, SendBiDirCapableOption=None, SendGenIdOption=None, SendHelloLanPruneDelayOption=None, ShowSelectedRpSetOnly=None, SupportUnicastBootstrap=None, TrafficGroupId=None, TriggeredHelloDelay=None, UpstreamNeighbor=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AddressFamily (str(ipv4|ipv6)): Choose an Address Family for this PIM-SM Interface.
			AutoPickUpstreamNeighbor (bool): Enables the time-saving Auto Pick feature and the Upstream Neighbor field is not available for use. The Upstream Neighbor address used in the Join/Prune message is determined automatically from received Hello messages. The first time a Hello message is received - containing a Source (link-local) address that does not belong to this interface, that source address will be used as the Upstream Neighbor address.
			BootstrapEnable (bool): If checked, enables the PIM-SM interface to participate in Bootstrap Router election procedure.
			BootstrapHashMaskLen (number): Hash Mask Length of the Bootstrap Router (BSR) that is set with the same name in all Bootstrap Messages sent by this BSR.
			BootstrapInterval (number): The time interval (in seconds) between two consecutive bootstrap messages sent by the BSR.
			BootstrapPriority (number): Priority of the Bootstrap Router (BSR) that is set with the same name in all Bootstrap Messages sent by this BSR.
			BootstrapTimeout (number): Amount of time (in seconds) of not receiving any Bootstrap Messages, after which the BSR if candidate at that point of time will decide that the currently elected BSR has gone down and will restart BSR election procedure.
			DisableTriggeredHello (bool): If enabled, the triggered hello delay function is disabled.
			DiscardDataMdtTlv (bool): If enabled, received Data MDT TLVs will be discarded.
			DiscardLearnedRpInfo (bool): If checked, disregards group mappings learnt from Bootstrap Message (in case not acting as elected BSR) or from Candidate RP Advertisement (in case of elected BSR).
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the PIMSM peer IP address once the PIMSM session is established. This allows PIMSM to use BFD to maintain IPv4 connectivity the PIMSM peer.
			EnableV4MappedV6Address (bool): Use IpV4 mapped IpV6 address
			Enabled (bool): Enables or disables the use of the interface.
			ForceSemanticFragmentation (bool): If enabled, this forces the BSR to send only one group specific RP list per bootstrap message.
			GenerationIdMode (str(incremental|random|constant)): The mode used for creating the 32-bit value for the Generation ID. This can either be incrementing, random or constant. (default = constant)
			HelloHoldTime (number): The amount of time that neighbor routers should hold the interface as reachable.
			HelloInterval (number): The interval between transmitted hello messages.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The identifier for this PIM-SM Interface.
			InterfaceIndex (number): The assigned protocol interface ID for this PIM-SM interface.
			InterfaceType (str): The type of interface to be selected for this PIM-SM interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IsRefreshRpSetComplete (bool): If enabled, shows the desired set of RPs.
			LanPruneDelay (number): The value of the LAN Prune (propagation) Delay for this PIM-SM interface. The expected delay for messages propagated on the link. It indicates to an upstream router how long to wait for a Join override message before it prunes an interface.The default value is 500 msec. The valid range is 100 to 0x7FFF msec. (LAN Prune Delay is an Option included in Hello messages.)
			LanPruneDelayTBit (bool): If enabled, the T flag bit in the LAN Prune Delay option of the Hello message is set (= 1). Setting this bit specifies that the sending PIM-SM router has the ability to disable Join message suppression.
			LearnSelectedRpSet (bool): If enabled, this displays only the best RP per group (member of selected RP set).
			OverrideInterval (number): The delay interval, in milliseconds, for randomizing the transmission time for override messages, which are used when scheduling a delayed Join message. This is part of the LAN Prune Delay option included in Hello messages. The valid range is 100 to 7FFF msec. (default = 2500)
			SendBiDirCapableOption (bool): If enabled, sets the bidirectional PIM-SM flag bit (=1), per IETF DRAFT draft-ietf-pim-bidir-04.
			SendGenIdOption (bool): Enables the send generation ID option.
			SendHelloLanPruneDelayOption (bool): If set, the LAN Prune propagation delay is enabled for this interface, as indicated in the pruneDelay option. The option is indicated in Hello messages from the interface. (default = true)
			ShowSelectedRpSetOnly (bool): If enabled, this displays only the best RP per group (member of selected RP set).
			SupportUnicastBootstrap (bool): If enabled, this supports the sending and processing of Unicast bootstrap messages.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this emulated router is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			TriggeredHelloDelay (number): The time (in seconds) after which the router senses a delay in sending or receiving PIM-SM hello message.
			UpstreamNeighbor (str): The IP address of the upstream neighbor.

		Returns:
			self: This instance with matching interface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		Gets the interface accesor Iface list.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: Return list of interface.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def RefreshCrpBsrLearnedInfo(self):
		"""Executes the refreshCrpBsrLearnedInfo operation on the server.

		If true, refreshes the Bsr learned information

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: Returns boolean value on success.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshCrpBsrLearnedInfo', payload=locals(), response_object=None)
