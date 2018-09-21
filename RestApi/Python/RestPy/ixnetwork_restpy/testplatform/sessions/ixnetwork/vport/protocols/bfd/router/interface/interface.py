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
	def Session(self):
		"""An instance of the Session class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bfd.router.interface.session.session.Session)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bfd.router.interface.session.session import Session
		return Session(self)

	@property
	def EchoConfigureSrcIp(self):
		"""If true, allows the user to configure the source IP address of the Echo Message, using echoSrcIpv4Address or echoSrcIpv6Address.

		Returns:
			bool
		"""
		return self._get_attribute('echoConfigureSrcIp')
	@EchoConfigureSrcIp.setter
	def EchoConfigureSrcIp(self, value):
		self._set_attribute('echoConfigureSrcIp', value)

	@property
	def EchoInterval(self):
		"""This option indicates the desired interval between BFD echo packets.

		Returns:
			number
		"""
		return self._get_attribute('echoInterval')
	@EchoInterval.setter
	def EchoInterval(self, value):
		self._set_attribute('echoInterval', value)

	@property
	def EchoSrcIpv4Address(self):
		"""Sets the IPv4 echo source address.

		Returns:
			str
		"""
		return self._get_attribute('echoSrcIpv4Address')
	@EchoSrcIpv4Address.setter
	def EchoSrcIpv4Address(self, value):
		self._set_attribute('echoSrcIpv4Address', value)

	@property
	def EchoSrcIpv6Address(self):
		"""Sets the IPv6 echo source address.

		Returns:
			str
		"""
		return self._get_attribute('echoSrcIpv6Address')
	@EchoSrcIpv6Address.setter
	def EchoSrcIpv6Address(self, value):
		self._set_attribute('echoSrcIpv6Address', value)

	@property
	def EchoTimeout(self):
		"""The interval, in microseconds, that the interface waits for a response to the last Echo packet sent out.

		Returns:
			number
		"""
		return self._get_attribute('echoTimeout')
	@EchoTimeout.setter
	def EchoTimeout(self, value):
		self._set_attribute('echoTimeout', value)

	@property
	def EchoTxInterval(self):
		"""The minimum interval, in microseconds, that the interface would like to use when transmitting BFD Echo packets.

		Returns:
			number
		"""
		return self._get_attribute('echoTxInterval')
	@EchoTxInterval.setter
	def EchoTxInterval(self, value):
		self._set_attribute('echoTxInterval', value)

	@property
	def EnableCtrlPlaneIndependent(self):
		"""Set to 1 if the local system's BFD implementation is independent of the control plane.

		Returns:
			bool
		"""
		return self._get_attribute('enableCtrlPlaneIndependent')
	@EnableCtrlPlaneIndependent.setter
	def EnableCtrlPlaneIndependent(self, value):
		self._set_attribute('enableCtrlPlaneIndependent', value)

	@property
	def EnableDemandMode(self):
		"""Enables demand mode. 1 indicates demand mode enabled, and 0 indicates demand mode disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enableDemandMode')
	@EnableDemandMode.setter
	def EnableDemandMode(self, value):
		self._set_attribute('enableDemandMode', value)

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
	def FlapTxInterval(self):
		"""BFD sessions will flap every flapTxIntvs. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('flapTxInterval')
	@FlapTxInterval.setter
	def FlapTxInterval(self, value):
		self._set_attribute('flapTxInterval', value)

	@property
	def InterfaceId(self):
		"""This is a local ID and is unique per router.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""The assigned protocol interface ID for this BFD interface.

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""The type of interface to be selected for this BFD interface.

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
	def IpDifferentiatedServiceField(self):
		"""Sets the TOS byte for IP Differentiated Service Field

		Returns:
			number
		"""
		return self._get_attribute('ipDifferentiatedServiceField')
	@IpDifferentiatedServiceField.setter
	def IpDifferentiatedServiceField(self, value):
		self._set_attribute('ipDifferentiatedServiceField', value)

	@property
	def MinRxInterval(self):
		"""This option indicates the desired minimum interval between received BFD control packets.

		Returns:
			number
		"""
		return self._get_attribute('minRxInterval')
	@MinRxInterval.setter
	def MinRxInterval(self, value):
		self._set_attribute('minRxInterval', value)

	@property
	def Multiplier(self):
		"""Multiplier * intv defines the timeout period. (default = 3)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def PollInterval(self):
		"""If in the Demand Mode, polling will take place every pollIntv interval. (default = 1,000)

		Returns:
			number
		"""
		return self._get_attribute('pollInterval')
	@PollInterval.setter
	def PollInterval(self, value):
		self._set_attribute('pollInterval', value)

	@property
	def TxInterval(self):
		"""This option indicates the desired interval between transmitted BFD control packets.

		Returns:
			number
		"""
		return self._get_attribute('txInterval')
	@TxInterval.setter
	def TxInterval(self, value):
		self._set_attribute('txInterval', value)

	def add(self, EchoConfigureSrcIp=None, EchoInterval=None, EchoSrcIpv4Address=None, EchoSrcIpv6Address=None, EchoTimeout=None, EchoTxInterval=None, EnableCtrlPlaneIndependent=None, EnableDemandMode=None, Enabled=None, FlapTxInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, IpDifferentiatedServiceField=None, MinRxInterval=None, Multiplier=None, PollInterval=None, TxInterval=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			EchoConfigureSrcIp (bool): If true, allows the user to configure the source IP address of the Echo Message, using echoSrcIpv4Address or echoSrcIpv6Address.
			EchoInterval (number): This option indicates the desired interval between BFD echo packets.
			EchoSrcIpv4Address (str): Sets the IPv4 echo source address.
			EchoSrcIpv6Address (str): Sets the IPv6 echo source address.
			EchoTimeout (number): The interval, in microseconds, that the interface waits for a response to the last Echo packet sent out.
			EchoTxInterval (number): The minimum interval, in microseconds, that the interface would like to use when transmitting BFD Echo packets.
			EnableCtrlPlaneIndependent (bool): Set to 1 if the local system's BFD implementation is independent of the control plane.
			EnableDemandMode (bool): Enables demand mode. 1 indicates demand mode enabled, and 0 indicates demand mode disabled.
			Enabled (bool): Enables the use of the simulated interface.
			FlapTxInterval (number): BFD sessions will flap every flapTxIntvs. (default = 0)
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This is a local ID and is unique per router.
			InterfaceIndex (number): The assigned protocol interface ID for this BFD interface.
			InterfaceType (str): The type of interface to be selected for this BFD interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IpDifferentiatedServiceField (number): Sets the TOS byte for IP Differentiated Service Field
			MinRxInterval (number): This option indicates the desired minimum interval between received BFD control packets.
			Multiplier (number): Multiplier * intv defines the timeout period. (default = 3)
			PollInterval (number): If in the Demand Mode, polling will take place every pollIntv interval. (default = 1,000)
			TxInterval (number): This option indicates the desired interval between transmitted BFD control packets.

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

	def find(self, EchoConfigureSrcIp=None, EchoInterval=None, EchoSrcIpv4Address=None, EchoSrcIpv6Address=None, EchoTimeout=None, EchoTxInterval=None, EnableCtrlPlaneIndependent=None, EnableDemandMode=None, Enabled=None, FlapTxInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, IpDifferentiatedServiceField=None, MinRxInterval=None, Multiplier=None, PollInterval=None, TxInterval=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			EchoConfigureSrcIp (bool): If true, allows the user to configure the source IP address of the Echo Message, using echoSrcIpv4Address or echoSrcIpv6Address.
			EchoInterval (number): This option indicates the desired interval between BFD echo packets.
			EchoSrcIpv4Address (str): Sets the IPv4 echo source address.
			EchoSrcIpv6Address (str): Sets the IPv6 echo source address.
			EchoTimeout (number): The interval, in microseconds, that the interface waits for a response to the last Echo packet sent out.
			EchoTxInterval (number): The minimum interval, in microseconds, that the interface would like to use when transmitting BFD Echo packets.
			EnableCtrlPlaneIndependent (bool): Set to 1 if the local system's BFD implementation is independent of the control plane.
			EnableDemandMode (bool): Enables demand mode. 1 indicates demand mode enabled, and 0 indicates demand mode disabled.
			Enabled (bool): Enables the use of the simulated interface.
			FlapTxInterval (number): BFD sessions will flap every flapTxIntvs. (default = 0)
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This is a local ID and is unique per router.
			InterfaceIndex (number): The assigned protocol interface ID for this BFD interface.
			InterfaceType (str): The type of interface to be selected for this BFD interface.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): The interfaces that are associated with the selected interface type.
			IpDifferentiatedServiceField (number): Sets the TOS byte for IP Differentiated Service Field
			MinRxInterval (number): This option indicates the desired minimum interval between received BFD control packets.
			Multiplier (number): Multiplier * intv defines the timeout period. (default = 3)
			PollInterval (number): If in the Demand Mode, polling will take place every pollIntv interval. (default = 1,000)
			TxInterval (number): This option indicates the desired interval between transmitted BFD control packets.

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

		NOT DEFINED

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
