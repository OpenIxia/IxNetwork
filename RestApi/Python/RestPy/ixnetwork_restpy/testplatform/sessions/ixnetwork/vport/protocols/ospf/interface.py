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
	def LearnedFilter(self):
		"""An instance of the LearnedFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedfilter.LearnedFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedfilter import LearnedFilter
		return LearnedFilter(self)._select()

	@property
	def LearnedLsa(self):
		"""An instance of the LearnedLsa class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedlsa.LearnedLsa)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.learnedlsa import LearnedLsa
		return LearnedLsa(self)

	@property
	def AdvertiseNetworkRange(self):
		"""Enables the advertisement of the OSPF network range.

		Returns:
			bool
		"""
		return self._get_attribute('advertiseNetworkRange')
	@AdvertiseNetworkRange.setter
	def AdvertiseNetworkRange(self, value):
		self._set_attribute('advertiseNetworkRange', value)

	@property
	def AreaId(self):
		"""The OSPF area ID associated with the interface.

		Returns:
			number
		"""
		return self._get_attribute('areaId')
	@AreaId.setter
	def AreaId(self, value):
		self._set_attribute('areaId', value)

	@property
	def AuthenticationMethods(self):
		"""The type of authentication to be used on this link interface.

		Returns:
			str(null|password|md5)
		"""
		return self._get_attribute('authenticationMethods')
	@AuthenticationMethods.setter
	def AuthenticationMethods(self, value):
		self._set_attribute('authenticationMethods', value)

	@property
	def AuthenticationPassword(self):
		"""Enter a clear-text 64-bit password. A password is configured at each end of the link. The password is inserted as is into the packet, and is compared upon receipt at the other end of the link. The received packet is dropped if the contained password does not match the configured password.

		Returns:
			str
		"""
		return self._get_attribute('authenticationPassword')
	@AuthenticationPassword.setter
	def AuthenticationPassword(self, value):
		self._set_attribute('authenticationPassword', value)

	@property
	def BBit(self):
		"""Indicates that this router is an Area Border Router (ABR).

		Returns:
			bool
		"""
		return self._get_attribute('bBit')
	@BBit.setter
	def BBit(self, value):
		self._set_attribute('bBit', value)

	@property
	def ConnectedToDut(self):
		"""Indicates that this OSPF interface is directly connected to the DUT.

		Returns:
			bool
		"""
		return self._get_attribute('connectedToDut')
	@ConnectedToDut.setter
	def ConnectedToDut(self, value):
		self._set_attribute('connectedToDut', value)

	@property
	def DeadInterval(self):
		"""The number of seconds allowed before declaring a silent router as being down.

		Returns:
			number
		"""
		return self._get_attribute('deadInterval')
	@DeadInterval.setter
	def DeadInterval(self, value):
		self._set_attribute('deadInterval', value)

	@property
	def EBit(self):
		"""External bit. Specifies how AS-external-LSAs are flooded.

		Returns:
			bool
		"""
		return self._get_attribute('eBit')
	@EBit.setter
	def EBit(self, value):
		self._set_attribute('eBit', value)

	@property
	def EnableAdvertiseRouterLsaLoopback(self):
		"""If true, advertises the router's LSA loopback address. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvertiseRouterLsaLoopback')
	@EnableAdvertiseRouterLsaLoopback.setter
	def EnableAdvertiseRouterLsaLoopback(self, value):
		self._set_attribute('enableAdvertiseRouterLsaLoopback', value)

	@property
	def EnableBfdRegistration(self):
		"""Indicates if a BFD session is to be created to the OSPF peer IP address once the OSPF session is established. This allows OSPF to use BFD to maintain IPv4 connectivity the OSPF peer.

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableFastHello(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableFastHello')
	@EnableFastHello.setter
	def EnableFastHello(self, value):
		self._set_attribute('enableFastHello', value)

	@property
	def Enabled(self):
		"""Enables the use of the simulated interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EntryColumn(self):
		"""The column where the entry point router is located in the OSPFnetwork range grid.

		Returns:
			number
		"""
		return self._get_attribute('entryColumn')
	@EntryColumn.setter
	def EntryColumn(self, value):
		self._set_attribute('entryColumn', value)

	@property
	def EntryRow(self):
		"""The row where the entry point router is located in the OSPF network range grid.

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

	@property
	def HelloInterval(self):
		"""The number of seconds between Hello packets sent from an Ixia router. The Ixia state machine sends Hello packets at this interval for all of the defined interfaces.

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def HelloMultiplier(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('helloMultiplier')
	@HelloMultiplier.setter
	def HelloMultiplier(self, value):
		self._set_attribute('helloMultiplier', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this OSPF interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceIpAddress(self):
		"""The IP address for this OSPF interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceIpAddress')
	@InterfaceIpAddress.setter
	def InterfaceIpAddress(self, value):
		self._set_attribute('interfaceIpAddress', value)

	@property
	def InterfaceIpMaskAddress(self):
		"""The IP mask associated with the IP address for this interface. Only used if protocolInterfaceDescription is empty. (default = 255.255.255.0)

		Returns:
			str
		"""
		return self._get_attribute('interfaceIpMaskAddress')
	@InterfaceIpMaskAddress.setter
	def InterfaceIpMaskAddress(self, value):
		self._set_attribute('interfaceIpMaskAddress', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this OSPF interface.

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
	def IsLearnedInfoRefreshed(self):
		"""If true, refreshes learned information automatically.

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def LinkTypes(self):
		"""Indicates the type of network link for the interface.

		Returns:
			str(pointToPoint|transit|stub|virtual)
		"""
		return self._get_attribute('linkTypes')
	@LinkTypes.setter
	def LinkTypes(self, value):
		self._set_attribute('linkTypes', value)

	@property
	def Md5AuthenticationKey(self):
		"""If authenticationMethod is set to ospfInterfaceAuthenticationMD5, then this is MD5 key ID used for authentication. (default = 1)

		Returns:
			str
		"""
		return self._get_attribute('md5AuthenticationKey')
	@Md5AuthenticationKey.setter
	def Md5AuthenticationKey(self, value):
		self._set_attribute('md5AuthenticationKey', value)

	@property
	def Md5AuthenticationKeyId(self):
		"""A value to be used as a key ID associated with the MD5 key.

		Returns:
			number
		"""
		return self._get_attribute('md5AuthenticationKeyId')
	@Md5AuthenticationKeyId.setter
	def Md5AuthenticationKeyId(self, value):
		self._set_attribute('md5AuthenticationKeyId', value)

	@property
	def Metric(self):
		"""A user-assigned routing metric associated with the interface.

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def Mtu(self):
		"""The maximum transmission unit (MTU) that is allowed on this link.

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def NeighborIpAddress(self):
		"""If the link type is a point to point network, this is the address of the other end of the link.

		Returns:
			str
		"""
		return self._get_attribute('neighborIpAddress')
	@NeighborIpAddress.setter
	def NeighborIpAddress(self, value):
		self._set_attribute('neighborIpAddress', value)

	@property
	def NeighborRouterId(self):
		"""When the linkType option is set to ospfInterfaceLinkPointToPoint, then this option should be set to the ID of the router on the other end of the point-to-point connection. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('neighborRouterId')
	@NeighborRouterId.setter
	def NeighborRouterId(self, value):
		self._set_attribute('neighborRouterId', value)

	@property
	def NetworkRangeIp(self):
		"""The IP address for the first OSPFv2 network to be advertised in the range.

		Returns:
			str
		"""
		return self._get_attribute('networkRangeIp')
	@NetworkRangeIp.setter
	def NetworkRangeIp(self, value):
		self._set_attribute('networkRangeIp', value)

	@property
	def NetworkRangeIpByMask(self):
		"""The number of bits in the network mask used with the IP address of the first network, in creating a range of addresses.

		Returns:
			bool
		"""
		return self._get_attribute('networkRangeIpByMask')
	@NetworkRangeIpByMask.setter
	def NetworkRangeIpByMask(self, value):
		self._set_attribute('networkRangeIpByMask', value)

	@property
	def NetworkRangeIpIncrementBy(self):
		"""The step size by which to automatically increment the IP addresses in the range.

		Returns:
			str
		"""
		return self._get_attribute('networkRangeIpIncrementBy')
	@NetworkRangeIpIncrementBy.setter
	def NetworkRangeIpIncrementBy(self, value):
		self._set_attribute('networkRangeIpIncrementBy', value)

	@property
	def NetworkRangeIpMask(self):
		"""The number of bits in the network mask used with the IP address of the first network, in creating a range of addresses.

		Returns:
			number
		"""
		return self._get_attribute('networkRangeIpMask')
	@NetworkRangeIpMask.setter
	def NetworkRangeIpMask(self, value):
		self._set_attribute('networkRangeIpMask', value)

	@property
	def NetworkRangeLinkType(self):
		"""The attribute for the network range link type.

		Returns:
			str(broadcast|pointToPoint)
		"""
		return self._get_attribute('networkRangeLinkType')
	@NetworkRangeLinkType.setter
	def NetworkRangeLinkType(self, value):
		self._set_attribute('networkRangeLinkType', value)

	@property
	def NetworkRangeRouterId(self):
		"""The unique identifier for the network range router.

		Returns:
			str
		"""
		return self._get_attribute('networkRangeRouterId')
	@NetworkRangeRouterId.setter
	def NetworkRangeRouterId(self, value):
		self._set_attribute('networkRangeRouterId', value)

	@property
	def NetworkRangeRouterIdIncrementBy(self):
		"""The step size by which to automatically increment the IP addresses in the range.

		Returns:
			str
		"""
		return self._get_attribute('networkRangeRouterIdIncrementBy')
	@NetworkRangeRouterIdIncrementBy.setter
	def NetworkRangeRouterIdIncrementBy(self, value):
		self._set_attribute('networkRangeRouterIdIncrementBy', value)

	@property
	def NetworkRangeTeEnable(self):
		"""Enables network range TEs.

		Returns:
			bool
		"""
		return self._get_attribute('networkRangeTeEnable')
	@NetworkRangeTeEnable.setter
	def NetworkRangeTeEnable(self, value):
		self._set_attribute('networkRangeTeEnable', value)

	@property
	def NetworkRangeTeMaxBandwidth(self):
		"""The maximum bandwidth for the network range TEs.

		Returns:
			number
		"""
		return self._get_attribute('networkRangeTeMaxBandwidth')
	@NetworkRangeTeMaxBandwidth.setter
	def NetworkRangeTeMaxBandwidth(self, value):
		self._set_attribute('networkRangeTeMaxBandwidth', value)

	@property
	def NetworkRangeTeMetric(self):
		"""The metrics for network range TEs.

		Returns:
			number
		"""
		return self._get_attribute('networkRangeTeMetric')
	@NetworkRangeTeMetric.setter
	def NetworkRangeTeMetric(self, value):
		self._set_attribute('networkRangeTeMetric', value)

	@property
	def NetworkRangeTeResMaxBandwidth(self):
		"""The maximum bandwidth for reserved network range TEs.

		Returns:
			number
		"""
		return self._get_attribute('networkRangeTeResMaxBandwidth')
	@NetworkRangeTeResMaxBandwidth.setter
	def NetworkRangeTeResMaxBandwidth(self, value):
		self._set_attribute('networkRangeTeResMaxBandwidth', value)

	@property
	def NetworkRangeTeUnreservedBwPriority(self):
		"""The maximum bandwidth for unreserved network range TEs.

		Returns:
			dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)
		"""
		return self._get_attribute('networkRangeTeUnreservedBwPriority')
	@NetworkRangeTeUnreservedBwPriority.setter
	def NetworkRangeTeUnreservedBwPriority(self, value):
		self._set_attribute('networkRangeTeUnreservedBwPriority', value)

	@property
	def NetworkType(self):
		"""The type of network attached to the link.

		Returns:
			str(pointToPoint|broadcast|pointToMultipoint)
		"""
		return self._get_attribute('networkType')
	@NetworkType.setter
	def NetworkType(self, value):
		self._set_attribute('networkType', value)

	@property
	def NoOfCols(self):
		"""The number of columns in a grid.

		Returns:
			number
		"""
		return self._get_attribute('noOfCols')
	@NoOfCols.setter
	def NoOfCols(self, value):
		self._set_attribute('noOfCols', value)

	@property
	def NoOfRows(self):
		"""The number or rows in a grid.

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def Options(self):
		"""Options related to the interface. Multiple options may be or'd together.

		Returns:
			number
		"""
		return self._get_attribute('options')
	@Options.setter
	def Options(self, value):
		self._set_attribute('options', value)

	@property
	def Priority(self):
		"""The priority of the interface, for use in election of the designated or backup master.

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def ProtocolInterface(self):
		"""The name of the defined interface entry from which IP address and mask are extracted for this interface.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def ShowExternal(self):
		"""Enables the use of External routes on this interface.

		Returns:
			bool
		"""
		return self._get_attribute('showExternal')
	@ShowExternal.setter
	def ShowExternal(self, value):
		self._set_attribute('showExternal', value)

	@property
	def ShowNssa(self):
		"""Enables the use of Not So Stubby Area routes on this interface.

		Returns:
			bool
		"""
		return self._get_attribute('showNssa')
	@ShowNssa.setter
	def ShowNssa(self, value):
		self._set_attribute('showNssa', value)

	@property
	def TeAdminGroup(self):
		"""Assignment of traffic engineering administrative group numbers to the interface.

		Returns:
			str
		"""
		return self._get_attribute('teAdminGroup')
	@TeAdminGroup.setter
	def TeAdminGroup(self, value):
		self._set_attribute('teAdminGroup', value)

	@property
	def TeEnable(self):
		"""Enables the generation of the Traffic Engineering opaque LSA with the remainder of the options in this class.

		Returns:
			bool
		"""
		return self._get_attribute('teEnable')
	@TeEnable.setter
	def TeEnable(self, value):
		self._set_attribute('teEnable', value)

	@property
	def TeMaxBandwidth(self):
		"""The maximum bandwidth that can possibly be used on this link in this direction.

		Returns:
			number
		"""
		return self._get_attribute('teMaxBandwidth')
	@TeMaxBandwidth.setter
	def TeMaxBandwidth(self, value):
		self._set_attribute('teMaxBandwidth', value)

	@property
	def TeMetricLevel(self):
		"""The user-assigned link metric for traffic engineering.

		Returns:
			number
		"""
		return self._get_attribute('teMetricLevel')
	@TeMetricLevel.setter
	def TeMetricLevel(self, value):
		self._set_attribute('teMetricLevel', value)

	@property
	def TeResMaxBandwidth(self):
		"""If enableTrafficEngineering is 1, then this indicates the maximum bandwidth, in bytes per second, that can be reserved on the link between this interface and its neighbors in the outbound direction. (default = 0.0)

		Returns:
			number
		"""
		return self._get_attribute('teResMaxBandwidth')
	@TeResMaxBandwidth.setter
	def TeResMaxBandwidth(self, value):
		self._set_attribute('teResMaxBandwidth', value)

	@property
	def TeUnreservedBwPriority(self):
		"""The amount of bandwidth not yet reserved at each of the eight priority levels.

		Returns:
			dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)
		"""
		return self._get_attribute('teUnreservedBwPriority')
	@TeUnreservedBwPriority.setter
	def TeUnreservedBwPriority(self, value):
		self._set_attribute('teUnreservedBwPriority', value)

	@property
	def ValidateReceivedMtuSize(self):
		"""If enabled (the default setting), the MTU will be verified during the Database (DB) exchange. If disabled, the advertised MTU size is set to 0, and the received MTU size is ignored during the DB exchange. NOTE: This option is only available for OSPFv2 interfaces that are directly connected to the DUT.

		Returns:
			bool
		"""
		return self._get_attribute('validateReceivedMtuSize')
	@ValidateReceivedMtuSize.setter
	def ValidateReceivedMtuSize(self, value):
		self._set_attribute('validateReceivedMtuSize', value)

	def add(self, AdvertiseNetworkRange=None, AreaId=None, AuthenticationMethods=None, AuthenticationPassword=None, BBit=None, ConnectedToDut=None, DeadInterval=None, EBit=None, EnableAdvertiseRouterLsaLoopback=None, EnableBfdRegistration=None, EnableFastHello=None, Enabled=None, EntryColumn=None, EntryRow=None, HelloInterval=None, HelloMultiplier=None, InterfaceIndex=None, InterfaceIpAddress=None, InterfaceIpMaskAddress=None, InterfaceType=None, Interfaces=None, LinkTypes=None, Md5AuthenticationKey=None, Md5AuthenticationKeyId=None, Metric=None, Mtu=None, NeighborIpAddress=None, NeighborRouterId=None, NetworkRangeIp=None, NetworkRangeIpByMask=None, NetworkRangeIpIncrementBy=None, NetworkRangeIpMask=None, NetworkRangeLinkType=None, NetworkRangeRouterId=None, NetworkRangeRouterIdIncrementBy=None, NetworkRangeTeEnable=None, NetworkRangeTeMaxBandwidth=None, NetworkRangeTeMetric=None, NetworkRangeTeResMaxBandwidth=None, NetworkRangeTeUnreservedBwPriority=None, NetworkType=None, NoOfCols=None, NoOfRows=None, Options=None, Priority=None, ProtocolInterface=None, ShowExternal=None, ShowNssa=None, TeAdminGroup=None, TeEnable=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None, ValidateReceivedMtuSize=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AdvertiseNetworkRange (bool): Enables the advertisement of the OSPF network range.
			AreaId (number): The OSPF area ID associated with the interface.
			AuthenticationMethods (str(null|password|md5)): The type of authentication to be used on this link interface.
			AuthenticationPassword (str): Enter a clear-text 64-bit password. A password is configured at each end of the link. The password is inserted as is into the packet, and is compared upon receipt at the other end of the link. The received packet is dropped if the contained password does not match the configured password.
			BBit (bool): Indicates that this router is an Area Border Router (ABR).
			ConnectedToDut (bool): Indicates that this OSPF interface is directly connected to the DUT.
			DeadInterval (number): The number of seconds allowed before declaring a silent router as being down.
			EBit (bool): External bit. Specifies how AS-external-LSAs are flooded.
			EnableAdvertiseRouterLsaLoopback (bool): If true, advertises the router's LSA loopback address. (default = false)
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the OSPF peer IP address once the OSPF session is established. This allows OSPF to use BFD to maintain IPv4 connectivity the OSPF peer.
			EnableFastHello (bool): NOT DEFINED
			Enabled (bool): Enables the use of the simulated interface.
			EntryColumn (number): The column where the entry point router is located in the OSPFnetwork range grid.
			EntryRow (number): The row where the entry point router is located in the OSPF network range grid.
			HelloInterval (number): The number of seconds between Hello packets sent from an Ixia router. The Ixia state machine sends Hello packets at this interval for all of the defined interfaces.
			HelloMultiplier (number): NOT DEFINED
			InterfaceIndex (number): The assigned protocol interface ID for this OSPF interface.
			InterfaceIpAddress (str): The IP address for this OSPF interface.
			InterfaceIpMaskAddress (str): The IP mask associated with the IP address for this interface. Only used if protocolInterfaceDescription is empty. (default = 255.255.255.0)
			InterfaceType (str): The type of interface to be selected for this OSPF interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			LinkTypes (str(pointToPoint|transit|stub|virtual)): Indicates the type of network link for the interface.
			Md5AuthenticationKey (str): If authenticationMethod is set to ospfInterfaceAuthenticationMD5, then this is MD5 key ID used for authentication. (default = 1)
			Md5AuthenticationKeyId (number): A value to be used as a key ID associated with the MD5 key.
			Metric (number): A user-assigned routing metric associated with the interface.
			Mtu (number): The maximum transmission unit (MTU) that is allowed on this link.
			NeighborIpAddress (str): If the link type is a point to point network, this is the address of the other end of the link.
			NeighborRouterId (str): When the linkType option is set to ospfInterfaceLinkPointToPoint, then this option should be set to the ID of the router on the other end of the point-to-point connection. (default = 0.0.0.0)
			NetworkRangeIp (str): The IP address for the first OSPFv2 network to be advertised in the range.
			NetworkRangeIpByMask (bool): The number of bits in the network mask used with the IP address of the first network, in creating a range of addresses.
			NetworkRangeIpIncrementBy (str): The step size by which to automatically increment the IP addresses in the range.
			NetworkRangeIpMask (number): The number of bits in the network mask used with the IP address of the first network, in creating a range of addresses.
			NetworkRangeLinkType (str(broadcast|pointToPoint)): The attribute for the network range link type.
			NetworkRangeRouterId (str): The unique identifier for the network range router.
			NetworkRangeRouterIdIncrementBy (str): The step size by which to automatically increment the IP addresses in the range.
			NetworkRangeTeEnable (bool): Enables network range TEs.
			NetworkRangeTeMaxBandwidth (number): The maximum bandwidth for the network range TEs.
			NetworkRangeTeMetric (number): The metrics for network range TEs.
			NetworkRangeTeResMaxBandwidth (number): The maximum bandwidth for reserved network range TEs.
			NetworkRangeTeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): The maximum bandwidth for unreserved network range TEs.
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): The type of network attached to the link.
			NoOfCols (number): The number of columns in a grid.
			NoOfRows (number): The number or rows in a grid.
			Options (number): Options related to the interface. Multiple options may be or'd together.
			Priority (number): The priority of the interface, for use in election of the designated or backup master.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The name of the defined interface entry from which IP address and mask are extracted for this interface.
			ShowExternal (bool): Enables the use of External routes on this interface.
			ShowNssa (bool): Enables the use of Not So Stubby Area routes on this interface.
			TeAdminGroup (str): Assignment of traffic engineering administrative group numbers to the interface.
			TeEnable (bool): Enables the generation of the Traffic Engineering opaque LSA with the remainder of the options in this class.
			TeMaxBandwidth (number): The maximum bandwidth that can possibly be used on this link in this direction.
			TeMetricLevel (number): The user-assigned link metric for traffic engineering.
			TeResMaxBandwidth (number): If enableTrafficEngineering is 1, then this indicates the maximum bandwidth, in bytes per second, that can be reserved on the link between this interface and its neighbors in the outbound direction. (default = 0.0)
			TeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): The amount of bandwidth not yet reserved at each of the eight priority levels.
			ValidateReceivedMtuSize (bool): If enabled (the default setting), the MTU will be verified during the Database (DB) exchange. If disabled, the advertised MTU size is set to 0, and the received MTU size is ignored during the DB exchange. NOTE: This option is only available for OSPFv2 interfaces that are directly connected to the DUT.

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

	def find(self, AdvertiseNetworkRange=None, AreaId=None, AuthenticationMethods=None, AuthenticationPassword=None, BBit=None, ConnectedToDut=None, DeadInterval=None, EBit=None, EnableAdvertiseRouterLsaLoopback=None, EnableBfdRegistration=None, EnableFastHello=None, Enabled=None, EntryColumn=None, EntryRow=None, HelloInterval=None, HelloMultiplier=None, InterfaceIndex=None, InterfaceIpAddress=None, InterfaceIpMaskAddress=None, InterfaceType=None, Interfaces=None, IsLearnedInfoRefreshed=None, LinkTypes=None, Md5AuthenticationKey=None, Md5AuthenticationKeyId=None, Metric=None, Mtu=None, NeighborIpAddress=None, NeighborRouterId=None, NetworkRangeIp=None, NetworkRangeIpByMask=None, NetworkRangeIpIncrementBy=None, NetworkRangeIpMask=None, NetworkRangeLinkType=None, NetworkRangeRouterId=None, NetworkRangeRouterIdIncrementBy=None, NetworkRangeTeEnable=None, NetworkRangeTeMaxBandwidth=None, NetworkRangeTeMetric=None, NetworkRangeTeResMaxBandwidth=None, NetworkRangeTeUnreservedBwPriority=None, NetworkType=None, NoOfCols=None, NoOfRows=None, Options=None, Priority=None, ProtocolInterface=None, ShowExternal=None, ShowNssa=None, TeAdminGroup=None, TeEnable=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None, ValidateReceivedMtuSize=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AdvertiseNetworkRange (bool): Enables the advertisement of the OSPF network range.
			AreaId (number): The OSPF area ID associated with the interface.
			AuthenticationMethods (str(null|password|md5)): The type of authentication to be used on this link interface.
			AuthenticationPassword (str): Enter a clear-text 64-bit password. A password is configured at each end of the link. The password is inserted as is into the packet, and is compared upon receipt at the other end of the link. The received packet is dropped if the contained password does not match the configured password.
			BBit (bool): Indicates that this router is an Area Border Router (ABR).
			ConnectedToDut (bool): Indicates that this OSPF interface is directly connected to the DUT.
			DeadInterval (number): The number of seconds allowed before declaring a silent router as being down.
			EBit (bool): External bit. Specifies how AS-external-LSAs are flooded.
			EnableAdvertiseRouterLsaLoopback (bool): If true, advertises the router's LSA loopback address. (default = false)
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the OSPF peer IP address once the OSPF session is established. This allows OSPF to use BFD to maintain IPv4 connectivity the OSPF peer.
			EnableFastHello (bool): NOT DEFINED
			Enabled (bool): Enables the use of the simulated interface.
			EntryColumn (number): The column where the entry point router is located in the OSPFnetwork range grid.
			EntryRow (number): The row where the entry point router is located in the OSPF network range grid.
			HelloInterval (number): The number of seconds between Hello packets sent from an Ixia router. The Ixia state machine sends Hello packets at this interval for all of the defined interfaces.
			HelloMultiplier (number): NOT DEFINED
			InterfaceIndex (number): The assigned protocol interface ID for this OSPF interface.
			InterfaceIpAddress (str): The IP address for this OSPF interface.
			InterfaceIpMaskAddress (str): The IP mask associated with the IP address for this interface. Only used if protocolInterfaceDescription is empty. (default = 255.255.255.0)
			InterfaceType (str): The type of interface to be selected for this OSPF interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IsLearnedInfoRefreshed (bool): If true, refreshes learned information automatically.
			LinkTypes (str(pointToPoint|transit|stub|virtual)): Indicates the type of network link for the interface.
			Md5AuthenticationKey (str): If authenticationMethod is set to ospfInterfaceAuthenticationMD5, then this is MD5 key ID used for authentication. (default = 1)
			Md5AuthenticationKeyId (number): A value to be used as a key ID associated with the MD5 key.
			Metric (number): A user-assigned routing metric associated with the interface.
			Mtu (number): The maximum transmission unit (MTU) that is allowed on this link.
			NeighborIpAddress (str): If the link type is a point to point network, this is the address of the other end of the link.
			NeighborRouterId (str): When the linkType option is set to ospfInterfaceLinkPointToPoint, then this option should be set to the ID of the router on the other end of the point-to-point connection. (default = 0.0.0.0)
			NetworkRangeIp (str): The IP address for the first OSPFv2 network to be advertised in the range.
			NetworkRangeIpByMask (bool): The number of bits in the network mask used with the IP address of the first network, in creating a range of addresses.
			NetworkRangeIpIncrementBy (str): The step size by which to automatically increment the IP addresses in the range.
			NetworkRangeIpMask (number): The number of bits in the network mask used with the IP address of the first network, in creating a range of addresses.
			NetworkRangeLinkType (str(broadcast|pointToPoint)): The attribute for the network range link type.
			NetworkRangeRouterId (str): The unique identifier for the network range router.
			NetworkRangeRouterIdIncrementBy (str): The step size by which to automatically increment the IP addresses in the range.
			NetworkRangeTeEnable (bool): Enables network range TEs.
			NetworkRangeTeMaxBandwidth (number): The maximum bandwidth for the network range TEs.
			NetworkRangeTeMetric (number): The metrics for network range TEs.
			NetworkRangeTeResMaxBandwidth (number): The maximum bandwidth for reserved network range TEs.
			NetworkRangeTeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): The maximum bandwidth for unreserved network range TEs.
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): The type of network attached to the link.
			NoOfCols (number): The number of columns in a grid.
			NoOfRows (number): The number or rows in a grid.
			Options (number): Options related to the interface. Multiple options may be or'd together.
			Priority (number): The priority of the interface, for use in election of the designated or backup master.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The name of the defined interface entry from which IP address and mask are extracted for this interface.
			ShowExternal (bool): Enables the use of External routes on this interface.
			ShowNssa (bool): Enables the use of Not So Stubby Area routes on this interface.
			TeAdminGroup (str): Assignment of traffic engineering administrative group numbers to the interface.
			TeEnable (bool): Enables the generation of the Traffic Engineering opaque LSA with the remainder of the options in this class.
			TeMaxBandwidth (number): The maximum bandwidth that can possibly be used on this link in this direction.
			TeMetricLevel (number): The user-assigned link metric for traffic engineering.
			TeResMaxBandwidth (number): If enableTrafficEngineering is 1, then this indicates the maximum bandwidth, in bytes per second, that can be reserved on the link between this interface and its neighbors in the outbound direction. (default = 0.0)
			TeUnreservedBwPriority (dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:number,arg8:number)): The amount of bandwidth not yet reserved at each of the eight priority levels.
			ValidateReceivedMtuSize (bool): If enabled (the default setting), the MTU will be verified during the Database (DB) exchange. If disabled, the advertised MTU size is set to 0, and the received MTU size is ignored during the DB exchange. NOTE: This option is only available for OSPFv2 interfaces that are directly connected to the DUT.

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

		Fetches interfaces accessor Iface list.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		A list of objects on which this exec can be used. This exec requires an object reference as an argument.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
