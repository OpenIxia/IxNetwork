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
	def Bandwidth(self):
		"""The minimum amount of bandwidth available on this link, in Kbps. The valid range is 1 to 4294967295. (default = 10,000 Kbps)

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def Delay(self):
		"""The total of delays on the path to the route/network, in microseconds. The valid range is 0 to 4294967295. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('delay')
	@Delay.setter
	def Delay(self, value):
		self._set_attribute('delay', value)

	@property
	def EnableBfdRegistration(self):
		"""Indicates if a BFD session is to be created to the EIGRP peer IP address once the EIGRP session is established. This allows EIGRP to use BFD to maintain IPv4 connectivity the EIGRP peer.

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def Enabled(self):
		"""Enables the EIGRP interface. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def HelloInterval(self):
		"""The time interval between Hello packets sent over the interface, in seconds. (default = 5 seconds)

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def HoldTime(self):
		"""The amount of time starting from the reception of a HELLO from a neighbor until the moment when the neighbor is to be dropped if no further HELLO is received from it, in seconds. (default = 15 seconds)

		Returns:
			number
		"""
		return self._get_attribute('holdTime')
	@HoldTime.setter
	def HoldTime(self, value):
		self._set_attribute('holdTime', value)

	@property
	def InterfaceId(self):
		"""The local ID associated with the interface, which is unique per router.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this EIGRP interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this EIGRP interface.

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
	def Load(self):
		"""The amount of load on the link. The valid range is 0 to 255. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('load')
	@Load.setter
	def Load(self, value):
		self._set_attribute('load', value)

	@property
	def MaxTlvPerPacket(self):
		"""The maximum number of TLVs that will be packed into a single Update packet, taking MTU into consideration. The valid range is 0-255. A value of 0 means that maximum possible packing will be used, which depends on the MTU of the link. (default = 30)

		Returns:
			number
		"""
		return self._get_attribute('maxTlvPerPacket')
	@MaxTlvPerPacket.setter
	def MaxTlvPerPacket(self, value):
		self._set_attribute('maxTlvPerPacket', value)

	@property
	def Mtu(self):
		"""The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def Reliability(self):
		"""The reliability factor. The valid range is 0 to 255. (default =255, which means 100% reliable)

		Returns:
			number
		"""
		return self._get_attribute('reliability')
	@Reliability.setter
	def Reliability(self, value):
		self._set_attribute('reliability', value)

	@property
	def SplitHorizon(self):
		"""Split Horizon is a method for omitting routes learned from a neighbor in update messages to that same neighbor. This enables or disables poison reverse.

		Returns:
			bool
		"""
		return self._get_attribute('splitHorizon')
	@SplitHorizon.setter
	def SplitHorizon(self, value):
		self._set_attribute('splitHorizon', value)

	def add(self, Bandwidth=None, Delay=None, EnableBfdRegistration=None, Enabled=None, HelloInterval=None, HoldTime=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, Load=None, MaxTlvPerPacket=None, Mtu=None, Reliability=None, SplitHorizon=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			Bandwidth (number): The minimum amount of bandwidth available on this link, in Kbps. The valid range is 1 to 4294967295. (default = 10,000 Kbps)
			Delay (number): The total of delays on the path to the route/network, in microseconds. The valid range is 0 to 4294967295. (default = 0)
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the EIGRP peer IP address once the EIGRP session is established. This allows EIGRP to use BFD to maintain IPv4 connectivity the EIGRP peer.
			Enabled (bool): Enables the EIGRP interface. (default = disabled)
			HelloInterval (number): The time interval between Hello packets sent over the interface, in seconds. (default = 5 seconds)
			HoldTime (number): The amount of time starting from the reception of a HELLO from a neighbor until the moment when the neighbor is to be dropped if no further HELLO is received from it, in seconds. (default = 15 seconds)
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The local ID associated with the interface, which is unique per router.
			InterfaceIndex (number): The assigned protocol interface ID for this EIGRP interface.
			InterfaceType (str): The type of interface to be selected for this EIGRP interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			Load (number): The amount of load on the link. The valid range is 0 to 255. (default = 0)
			MaxTlvPerPacket (number): The maximum number of TLVs that will be packed into a single Update packet, taking MTU into consideration. The valid range is 0-255. A value of 0 means that maximum possible packing will be used, which depends on the MTU of the link. (default = 30)
			Mtu (number): The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)
			Reliability (number): The reliability factor. The valid range is 0 to 255. (default =255, which means 100% reliable)
			SplitHorizon (bool): Split Horizon is a method for omitting routes learned from a neighbor in update messages to that same neighbor. This enables or disables poison reverse.

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

	def find(self, Bandwidth=None, Delay=None, EnableBfdRegistration=None, Enabled=None, HelloInterval=None, HoldTime=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, Load=None, MaxTlvPerPacket=None, Mtu=None, Reliability=None, SplitHorizon=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			Bandwidth (number): The minimum amount of bandwidth available on this link, in Kbps. The valid range is 1 to 4294967295. (default = 10,000 Kbps)
			Delay (number): The total of delays on the path to the route/network, in microseconds. The valid range is 0 to 4294967295. (default = 0)
			EnableBfdRegistration (bool): Indicates if a BFD session is to be created to the EIGRP peer IP address once the EIGRP session is established. This allows EIGRP to use BFD to maintain IPv4 connectivity the EIGRP peer.
			Enabled (bool): Enables the EIGRP interface. (default = disabled)
			HelloInterval (number): The time interval between Hello packets sent over the interface, in seconds. (default = 5 seconds)
			HoldTime (number): The amount of time starting from the reception of a HELLO from a neighbor until the moment when the neighbor is to be dropped if no further HELLO is received from it, in seconds. (default = 15 seconds)
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The local ID associated with the interface, which is unique per router.
			InterfaceIndex (number): The assigned protocol interface ID for this EIGRP interface.
			InterfaceType (str): The type of interface to be selected for this EIGRP interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			Load (number): The amount of load on the link. The valid range is 0 to 255. (default = 0)
			MaxTlvPerPacket (number): The maximum number of TLVs that will be packed into a single Update packet, taking MTU into consideration. The valid range is 0-255. A value of 0 means that maximum possible packing will be used, which depends on the MTU of the link. (default = 30)
			Mtu (number): The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)
			Reliability (number): The reliability factor. The valid range is 0 to 255. (default =255, which means 100% reliable)
			SplitHorizon (bool): Split Horizon is a method for omitting routes learned from a neighbor in update messages to that same neighbor. This enables or disables poison reverse.

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
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)
