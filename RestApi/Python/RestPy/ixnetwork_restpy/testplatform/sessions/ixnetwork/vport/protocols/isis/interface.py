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
	def CircuitAuthType(self):
		"""The type of Circuit Authentication to be used for this emulated ISIS router.

		Returns:
			str(none|password|md5)
		"""
		return self._get_attribute('circuitAuthType')
	@CircuitAuthType.setter
	def CircuitAuthType(self, value):
		self._set_attribute('circuitAuthType', value)

	@property
	def CircuitReceivedPasswordList(self):
		"""The Receive Password List is used only for Cleartext Password authentication. MD5 Authentication requires that both of the neighbors have the same MD5 key for the packets to be accepted.

		Returns:
			list(str)
		"""
		return self._get_attribute('circuitReceivedPasswordList')
	@CircuitReceivedPasswordList.setter
	def CircuitReceivedPasswordList(self, value):
		self._set_attribute('circuitReceivedPasswordList', value)

	@property
	def CircuitTransmitPassword(self):
		"""If circuitAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted IIHs.

		Returns:
			str
		"""
		return self._get_attribute('circuitTransmitPassword')
	@CircuitTransmitPassword.setter
	def CircuitTransmitPassword(self, value):
		self._set_attribute('circuitTransmitPassword', value)

	@property
	def ConfiguredHoldTime(self):
		"""The configured hold time for the interface. This value is only used if enableConfiguredHoldTime is set to true.

		Returns:
			number
		"""
		return self._get_attribute('configuredHoldTime')
	@ConfiguredHoldTime.setter
	def ConfiguredHoldTime(self, value):
		self._set_attribute('configuredHoldTime', value)

	@property
	def Enable3WayHandshake(self):
		"""If true, Ixia emulated point-to-point circuit will include 3-way TLV in its P2P IIH and attempt to establish the adjacency as specified in RFC 5303.

		Returns:
			bool
		"""
		return self._get_attribute('enable3WayHandshake')
	@Enable3WayHandshake.setter
	def Enable3WayHandshake(self, value):
		self._set_attribute('enable3WayHandshake', value)

	@property
	def EnableAutoAdjustArea(self):
		"""If set, and a HELLO message is received which contains a protocols TLV, then the interfaces protocols will be adjusted to match the received TLV.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoAdjustArea')
	@EnableAutoAdjustArea.setter
	def EnableAutoAdjustArea(self, value):
		self._set_attribute('enableAutoAdjustArea', value)

	@property
	def EnableAutoAdjustMtu(self):
		"""If set, and a padded HELLO message is received on the interface, then the interfaces MTU will be adjusted to match the packet length of the received HELLO message.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoAdjustMtu')
	@EnableAutoAdjustMtu.setter
	def EnableAutoAdjustMtu(self, value):
		self._set_attribute('enableAutoAdjustMtu', value)

	@property
	def EnableAutoAdjustProtocolsSupported(self):
		"""If set, and a HELLO message is received which contains a protocols TLV, then the interfaces protocols will be adjusted to match the received TLV.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoAdjustProtocolsSupported')
	@EnableAutoAdjustProtocolsSupported.setter
	def EnableAutoAdjustProtocolsSupported(self, value):
		self._set_attribute('enableAutoAdjustProtocolsSupported', value)

	@property
	def EnableBfdRegistration(self):
		"""Indicates if a BFD session is to be created to the ISIS peer IP address once the ISIS session is established. This allows ISIS to use BFD to maintain IPv4 connectivity the ISIS peer.

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableConfiguredHoldTime(self):
		"""If true, enables a hold time for the created interfaces, based on the value set in the configuredHoldTime object.

		Returns:
			bool
		"""
		return self._get_attribute('enableConfiguredHoldTime')
	@EnableConfiguredHoldTime.setter
	def EnableConfiguredHoldTime(self, value):
		self._set_attribute('enableConfiguredHoldTime', value)

	@property
	def EnableConnectedToDut(self):
		"""If enabled, this ISIS interface is directly connected to the DUT.

		Returns:
			bool
		"""
		return self._get_attribute('enableConnectedToDut')
	@EnableConnectedToDut.setter
	def EnableConnectedToDut(self, value):
		self._set_attribute('enableConnectedToDut', value)

	@property
	def Enabled(self):
		"""Enables the use of this interface for the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExtendedCircuitId(self):
		"""The integer value of the local circuit ID.

		Returns:
			number
		"""
		return self._get_attribute('extendedCircuitId')
	@ExtendedCircuitId.setter
	def ExtendedCircuitId(self, value):
		self._set_attribute('extendedCircuitId', value)

	@property
	def InterfaceId(self):
		"""The OSI interface ID for this interface.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIp(self):
		"""The IP address for this interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceIp')
	@InterfaceIp.setter
	def InterfaceIp(self, value):
		self._set_attribute('interfaceIp', value)

	@property
	def InterfaceIpMask(self):
		"""Available only when Interface Connected to DUT is disabled. The mask used with the IPv4 address for this virtual interface on the emulated ISIS router. This interface address is used to connect to virtual ISIS Network Ranges behind the Ixia-emulated ISIS router.

		Returns:
			str
		"""
		return self._get_attribute('interfaceIpMask')
	@InterfaceIpMask.setter
	def InterfaceIpMask(self, value):
		self._set_attribute('interfaceIpMask', value)

	@property
	def Ipv6MtMetric(self):
		"""This metric is same as the Interface Metric. If true, it allows you to enter data.

		Returns:
			number
		"""
		return self._get_attribute('ipv6MtMetric')
	@Ipv6MtMetric.setter
	def Ipv6MtMetric(self, value):
		self._set_attribute('ipv6MtMetric', value)

	@property
	def Level(self):
		"""The IS-IS level associated with the interface.

		Returns:
			str(level1|level2|level1Level2)
		"""
		return self._get_attribute('level')
	@Level.setter
	def Level(self, value):
		self._set_attribute('level', value)

	@property
	def Level1DeadTime(self):
		"""The dead (holding time) interval for level 1 hello messages, in seconds. If an ISIS router sending L1 hellos is not heard from within this time period, it will be considered down.

		Returns:
			number
		"""
		return self._get_attribute('level1DeadTime')
	@Level1DeadTime.setter
	def Level1DeadTime(self, value):
		self._set_attribute('level1DeadTime', value)

	@property
	def Level1HelloTime(self):
		"""The hello interval for level 1 hello messages, in seconds.

		Returns:
			number
		"""
		return self._get_attribute('level1HelloTime')
	@Level1HelloTime.setter
	def Level1HelloTime(self, value):
		self._set_attribute('level1HelloTime', value)

	@property
	def Level2DeadTime(self):
		"""The dead (holding time) interval for level 2 hello messages, in seconds. If an ISIS router sending L2 hellos is not heard from within this time period, it will be considered down.

		Returns:
			number
		"""
		return self._get_attribute('level2DeadTime')
	@Level2DeadTime.setter
	def Level2DeadTime(self, value):
		self._set_attribute('level2DeadTime', value)

	@property
	def Level2HelloTime(self):
		"""The hello interval for level 2 hello messages, in seconds.

		Returns:
			number
		"""
		return self._get_attribute('level2HelloTime')
	@Level2HelloTime.setter
	def Level2HelloTime(self, value):
		self._set_attribute('level2HelloTime', value)

	@property
	def Metric(self):
		"""The cost metric associated with the route.

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def NetworkType(self):
		"""Indicates the type of network attached to the interface: broadcast or point-to-point.

		Returns:
			str(pointToPoint|broadcast|pointToMultipoint)
		"""
		return self._get_attribute('networkType')
	@NetworkType.setter
	def NetworkType(self, value):
		self._set_attribute('networkType', value)

	@property
	def PriorityLevel1(self):
		"""Indicates the priority level 1.

		Returns:
			number
		"""
		return self._get_attribute('priorityLevel1')
	@PriorityLevel1.setter
	def PriorityLevel1(self, value):
		self._set_attribute('priorityLevel1', value)

	@property
	def PriorityLevel2(self):
		"""Indicates the priority level 2.

		Returns:
			number
		"""
		return self._get_attribute('priorityLevel2')
	@PriorityLevel2.setter
	def PriorityLevel2(self, value):
		self._set_attribute('priorityLevel2', value)

	@property
	def TeAdminGroup(self):
		"""The traffic engineering administrative group associated with the interface. (default = {00 00 00 00})

		Returns:
			str
		"""
		return self._get_attribute('teAdminGroup')
	@TeAdminGroup.setter
	def TeAdminGroup(self, value):
		self._set_attribute('teAdminGroup', value)

	@property
	def TeMaxBandwidth(self):
		"""For setting the maximum link bandwidth (sub-TLV 9) allowed for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('teMaxBandwidth')
	@TeMaxBandwidth.setter
	def TeMaxBandwidth(self, value):
		self._set_attribute('teMaxBandwidth', value)

	@property
	def TeMetricLevel(self):
		"""A user-defined metric for this TE path.

		Returns:
			number
		"""
		return self._get_attribute('teMetricLevel')
	@TeMetricLevel.setter
	def TeMetricLevel(self, value):
		self._set_attribute('teMetricLevel', value)

	@property
	def TeResMaxBandwidth(self):
		"""For setting the Maximum reservable link bandwidth (sub-TLV 10). It is the maximum bandwidth that can be reserved for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('teResMaxBandwidth')
	@TeResMaxBandwidth.setter
	def TeResMaxBandwidth(self, value):
		self._set_attribute('teResMaxBandwidth', value)

	@property
	def TeUnreservedBwPriority(self):
		"""The traffic engineering unreserved bandwidth for each priority to be advertised. There are eight distinct options. (default = 0.0)

		Returns:
			list(number)
		"""
		return self._get_attribute('teUnreservedBwPriority')
	@TeUnreservedBwPriority.setter
	def TeUnreservedBwPriority(self, value):
		self._set_attribute('teUnreservedBwPriority', value)

	def add(self, CircuitAuthType=None, CircuitReceivedPasswordList=None, CircuitTransmitPassword=None, ConfiguredHoldTime=None, Enable3WayHandshake=None, EnableAutoAdjustArea=None, EnableAutoAdjustMtu=None, EnableAutoAdjustProtocolsSupported=None, EnableBfdRegistration=None, EnableConfiguredHoldTime=None, EnableConnectedToDut=None, Enabled=None, ExtendedCircuitId=None, InterfaceId=None, InterfaceIp=None, InterfaceIpMask=None, Ipv6MtMetric=None, Level=None, Level1DeadTime=None, Level1HelloTime=None, Level2DeadTime=None, Level2HelloTime=None, Metric=None, NetworkType=None, PriorityLevel1=None, PriorityLevel2=None, TeAdminGroup=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			CircuitAuthType (str(none|password|md5)): The type of Circuit Authentication to be used for this emulated ISIS router.
			CircuitReceivedPasswordList (list(str)): The Receive Password List is used only for Cleartext Password authentication. MD5 Authentication requires that both of the neighbors have the same MD5 key for the packets to be accepted.
			CircuitTransmitPassword (str): If circuitAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted IIHs.
			ConfiguredHoldTime (number): The configured hold time for the interface. This value is only used if enableConfiguredHoldTime is set to true.
			Enable3WayHandshake (bool): If true, Ixia emulated point-to-point circuit will include 3-way TLV in its P2P IIH and attempt to establish the adjacency as specified in RFC 5303.
			EnableAutoAdjustArea (bool): If set, and a HELLO message is received which contains a protocols TLV, then the interfaces protocols will be adjusted to match the received TLV.
			EnableAutoAdjustMtu (bool): If set, and a padded HELLO message is received on the interface, then the interfaces MTU will be adjusted to match the packet length of the received HELLO message.
			EnableAutoAdjustProtocolsSupported (bool): If set, and a HELLO message is received which contains a protocols TLV, then the interfaces protocols will be adjusted to match the received TLV.
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the ISIS peer IP address once the ISIS session is established. This allows ISIS to use BFD to maintain IPv4 connectivity the ISIS peer.
			EnableConfiguredHoldTime (bool): If true, enables a hold time for the created interfaces, based on the value set in the configuredHoldTime object.
			EnableConnectedToDut (bool): If enabled, this ISIS interface is directly connected to the DUT.
			Enabled (bool): Enables the use of this interface for the simulated router.
			ExtendedCircuitId (number): The integer value of the local circuit ID.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The OSI interface ID for this interface.
			InterfaceIp (str): The IP address for this interface.
			InterfaceIpMask (str): Available only when Interface Connected to DUT is disabled. The mask used with the IPv4 address for this virtual interface on the emulated ISIS router. This interface address is used to connect to virtual ISIS Network Ranges behind the Ixia-emulated ISIS router.
			Ipv6MtMetric (number): This metric is same as the Interface Metric. If true, it allows you to enter data.
			Level (str(level1|level2|level1Level2)): The IS-IS level associated with the interface.
			Level1DeadTime (number): The dead (holding time) interval for level 1 hello messages, in seconds. If an ISIS router sending L1 hellos is not heard from within this time period, it will be considered down.
			Level1HelloTime (number): The hello interval for level 1 hello messages, in seconds.
			Level2DeadTime (number): The dead (holding time) interval for level 2 hello messages, in seconds. If an ISIS router sending L2 hellos is not heard from within this time period, it will be considered down.
			Level2HelloTime (number): The hello interval for level 2 hello messages, in seconds.
			Metric (number): The cost metric associated with the route.
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): Indicates the type of network attached to the interface: broadcast or point-to-point.
			PriorityLevel1 (number): Indicates the priority level 1.
			PriorityLevel2 (number): Indicates the priority level 2.
			TeAdminGroup (str): The traffic engineering administrative group associated with the interface. (default = {00 00 00 00})
			TeMaxBandwidth (number): For setting the maximum link bandwidth (sub-TLV 9) allowed for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.
			TeMetricLevel (number): A user-defined metric for this TE path.
			TeResMaxBandwidth (number): For setting the Maximum reservable link bandwidth (sub-TLV 10). It is the maximum bandwidth that can be reserved for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.
			TeUnreservedBwPriority (list(number)): The traffic engineering unreserved bandwidth for each priority to be advertised. There are eight distinct options. (default = 0.0)

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

	def find(self, CircuitAuthType=None, CircuitReceivedPasswordList=None, CircuitTransmitPassword=None, ConfiguredHoldTime=None, Enable3WayHandshake=None, EnableAutoAdjustArea=None, EnableAutoAdjustMtu=None, EnableAutoAdjustProtocolsSupported=None, EnableBfdRegistration=None, EnableConfiguredHoldTime=None, EnableConnectedToDut=None, Enabled=None, ExtendedCircuitId=None, InterfaceId=None, InterfaceIp=None, InterfaceIpMask=None, Ipv6MtMetric=None, Level=None, Level1DeadTime=None, Level1HelloTime=None, Level2DeadTime=None, Level2HelloTime=None, Metric=None, NetworkType=None, PriorityLevel1=None, PriorityLevel2=None, TeAdminGroup=None, TeMaxBandwidth=None, TeMetricLevel=None, TeResMaxBandwidth=None, TeUnreservedBwPriority=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			CircuitAuthType (str(none|password|md5)): The type of Circuit Authentication to be used for this emulated ISIS router.
			CircuitReceivedPasswordList (list(str)): The Receive Password List is used only for Cleartext Password authentication. MD5 Authentication requires that both of the neighbors have the same MD5 key for the packets to be accepted.
			CircuitTransmitPassword (str): If circuitAuthType is isisAuthTypePassword, then this is the password (or MD5Key) that will be sent with transmitted IIHs.
			ConfiguredHoldTime (number): The configured hold time for the interface. This value is only used if enableConfiguredHoldTime is set to true.
			Enable3WayHandshake (bool): If true, Ixia emulated point-to-point circuit will include 3-way TLV in its P2P IIH and attempt to establish the adjacency as specified in RFC 5303.
			EnableAutoAdjustArea (bool): If set, and a HELLO message is received which contains a protocols TLV, then the interfaces protocols will be adjusted to match the received TLV.
			EnableAutoAdjustMtu (bool): If set, and a padded HELLO message is received on the interface, then the interfaces MTU will be adjusted to match the packet length of the received HELLO message.
			EnableAutoAdjustProtocolsSupported (bool): If set, and a HELLO message is received which contains a protocols TLV, then the interfaces protocols will be adjusted to match the received TLV.
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the ISIS peer IP address once the ISIS session is established. This allows ISIS to use BFD to maintain IPv4 connectivity the ISIS peer.
			EnableConfiguredHoldTime (bool): If true, enables a hold time for the created interfaces, based on the value set in the configuredHoldTime object.
			EnableConnectedToDut (bool): If enabled, this ISIS interface is directly connected to the DUT.
			Enabled (bool): Enables the use of this interface for the simulated router.
			ExtendedCircuitId (number): The integer value of the local circuit ID.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The OSI interface ID for this interface.
			InterfaceIp (str): The IP address for this interface.
			InterfaceIpMask (str): Available only when Interface Connected to DUT is disabled. The mask used with the IPv4 address for this virtual interface on the emulated ISIS router. This interface address is used to connect to virtual ISIS Network Ranges behind the Ixia-emulated ISIS router.
			Ipv6MtMetric (number): This metric is same as the Interface Metric. If true, it allows you to enter data.
			Level (str(level1|level2|level1Level2)): The IS-IS level associated with the interface.
			Level1DeadTime (number): The dead (holding time) interval for level 1 hello messages, in seconds. If an ISIS router sending L1 hellos is not heard from within this time period, it will be considered down.
			Level1HelloTime (number): The hello interval for level 1 hello messages, in seconds.
			Level2DeadTime (number): The dead (holding time) interval for level 2 hello messages, in seconds. If an ISIS router sending L2 hellos is not heard from within this time period, it will be considered down.
			Level2HelloTime (number): The hello interval for level 2 hello messages, in seconds.
			Metric (number): The cost metric associated with the route.
			NetworkType (str(pointToPoint|broadcast|pointToMultipoint)): Indicates the type of network attached to the interface: broadcast or point-to-point.
			PriorityLevel1 (number): Indicates the priority level 1.
			PriorityLevel2 (number): Indicates the priority level 2.
			TeAdminGroup (str): The traffic engineering administrative group associated with the interface. (default = {00 00 00 00})
			TeMaxBandwidth (number): For setting the maximum link bandwidth (sub-TLV 9) allowed for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.
			TeMetricLevel (number): A user-defined metric for this TE path.
			TeResMaxBandwidth (number): For setting the Maximum reservable link bandwidth (sub-TLV 10). It is the maximum bandwidth that can be reserved for this link in this direction. It is a 32-bit IEEE floating point value, in bytes/sec. The default is 0.
			TeUnreservedBwPriority (list(number)): The traffic engineering unreserved bandwidth for each priority to be advertised. There are eight distinct options. (default = 0.0)

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
