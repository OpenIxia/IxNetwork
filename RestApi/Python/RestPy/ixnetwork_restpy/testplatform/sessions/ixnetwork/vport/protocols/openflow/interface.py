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
	def OfChannel(self):
		"""An instance of the OfChannel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannel.OfChannel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannel import OfChannel
		return OfChannel(self)

	@property
	def Switch(self):
		"""An instance of the Switch class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switch.Switch)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switch import Switch
		return Switch(self)

	@property
	def AcceptUnconfiguredChannel(self):
		"""If true, un-configured channels are accepted for this interface.

		Returns:
			bool
		"""
		return self._get_attribute('acceptUnconfiguredChannel')
	@AcceptUnconfiguredChannel.setter
	def AcceptUnconfiguredChannel(self, value):
		self._set_attribute('acceptUnconfiguredChannel', value)

	@property
	def AllFlowsDelOnStart(self):
		"""If set, Ixia sends out an OpenFlow flow delete message (all wildcard) at startup. This should delete all existing flows in DUT.

		Returns:
			bool
		"""
		return self._get_attribute('allFlowsDelOnStart')
	@AllFlowsDelOnStart.setter
	def AllFlowsDelOnStart(self, value):
		self._set_attribute('allFlowsDelOnStart', value)

	@property
	def AuxiliaryConnectionTimeout(self):
		"""Period of time after which auxiliary connection will time out , if no messages are received.

		Returns:
			str(auxReSendFeatureRequest|auxFeatureRequestTerminateConnection)
		"""
		return self._get_attribute('auxiliaryConnectionTimeout')
	@AuxiliaryConnectionTimeout.setter
	def AuxiliaryConnectionTimeout(self, value):
		self._set_attribute('auxiliaryConnectionTimeout', value)

	@property
	def BadVersionErrorAction(self):
		"""Defines what action to take in case an auxiliary connection receives an error of type OFPET_BAD_REQUEST and code OFPBRC_BAD_VERSION.

		Returns:
			str(auxReSendHello|auxTerminateConnection)
		"""
		return self._get_attribute('badVersionErrorAction')
	@BadVersionErrorAction.setter
	def BadVersionErrorAction(self, value):
		self._set_attribute('badVersionErrorAction', value)

	@property
	def EchoInterval(self):
		"""Indicates the periodic interval in seconds at which the Interface sends Echo Request Packets applicable if enablePeriodicEcho attribute is set.

		Returns:
			number
		"""
		return self._get_attribute('echoInterval')
	@EchoInterval.setter
	def EchoInterval(self, value):
		self._set_attribute('echoInterval', value)

	@property
	def EchoMultiplier(self):
		"""Indicates the value specified for the selected Timeout option.

		Returns:
			number
		"""
		return self._get_attribute('echoMultiplier')
	@EchoMultiplier.setter
	def EchoMultiplier(self, value):
		self._set_attribute('echoMultiplier', value)

	@property
	def EchoTimeout(self):
		"""Indicates the duration interval of the state machine waiting for echo reply to arrive applicable if echoTimeout is set.

		Returns:
			number
		"""
		return self._get_attribute('echoTimeout')
	@EchoTimeout.setter
	def EchoTimeout(self, value):
		self._set_attribute('echoTimeout', value)

	@property
	def EnableEchoTimeOut(self):
		"""If true, enables echoTimeout field.

		Returns:
			bool
		"""
		return self._get_attribute('enableEchoTimeOut')
	@EnableEchoTimeOut.setter
	def EnableEchoTimeOut(self, value):
		self._set_attribute('enableEchoTimeOut', value)

	@property
	def EnableMultipleLogicalSwitch(self):
		"""if true, we add multiple number of switch per interface

		Returns:
			bool
		"""
		return self._get_attribute('enableMultipleLogicalSwitch')
	@EnableMultipleLogicalSwitch.setter
	def EnableMultipleLogicalSwitch(self, value):
		self._set_attribute('enableMultipleLogicalSwitch', value)

	@property
	def EnablePeriodicEcho(self):
		"""If set enables echoInterval field.

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicEcho')
	@EnablePeriodicEcho.setter
	def EnablePeriodicEcho(self, value):
		self._set_attribute('enablePeriodicEcho', value)

	@property
	def EnablePeriodicLldp(self):
		"""If true, enables Periodic LLDP PacketOut Sending for each Switch Port

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicLldp')
	@EnablePeriodicLldp.setter
	def EnablePeriodicLldp(self, value):
		self._set_attribute('enablePeriodicLldp', value)

	@property
	def Enabled(self):
		"""If set enables the interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FeatureRequestTimeout(self):
		"""Specifies the time after which a feature request will time out , if feature reply is received.

		Returns:
			number
		"""
		return self._get_attribute('featureRequestTimeout')
	@FeatureRequestTimeout.setter
	def FeatureRequestTimeout(self, value):
		self._set_attribute('featureRequestTimeout', value)

	@property
	def FeatureRequestTimeoutAction(self):
		"""Specifies if action should be taken when feature request timeouts.

		Returns:
			number
		"""
		return self._get_attribute('featureRequestTimeoutAction')
	@FeatureRequestTimeoutAction.setter
	def FeatureRequestTimeoutAction(self, value):
		self._set_attribute('featureRequestTimeoutAction', value)

	@property
	def InstallFlowForLldp(self):
		"""If true, installs Flow in Switch for LLDP Packets to be explicitly send to Controller.

		Returns:
			bool
		"""
		return self._get_attribute('installFlowForLldp')
	@InstallFlowForLldp.setter
	def InstallFlowForLldp(self, value):
		self._set_attribute('installFlowForLldp', value)

	@property
	def LldpDestinationMacAddress(self):
		"""Indicates the Destination MAC Address for LLDP Packet Out.

		Returns:
			str
		"""
		return self._get_attribute('lldpDestinationMacAddress')
	@LldpDestinationMacAddress.setter
	def LldpDestinationMacAddress(self, value):
		self._set_attribute('lldpDestinationMacAddress', value)

	@property
	def ModeOfConnection(self):
		"""Indicates the mode of connection used for the Interface.

		Returns:
			str(passive|active|mixed)
		"""
		return self._get_attribute('modeOfConnection')
	@ModeOfConnection.setter
	def ModeOfConnection(self, value):
		self._set_attribute('modeOfConnection', value)

	@property
	def NonHelloMessageStartupAction(self):
		"""Defines what action to take in case an auxiliary connection receives a non-hello message at startup.

		Returns:
			str(auxAcceptConnection|auxSendError)
		"""
		return self._get_attribute('nonHelloMessageStartupAction')
	@NonHelloMessageStartupAction.setter
	def NonHelloMessageStartupAction(self, value):
		self._set_attribute('nonHelloMessageStartupAction', value)

	@property
	def PeriodicLldpInterval(self):
		"""Indicates the Periodic LLDP Packet Out Interval.

		Returns:
			number
		"""
		return self._get_attribute('periodicLldpInterval')
	@PeriodicLldpInterval.setter
	def PeriodicLldpInterval(self, value):
		self._set_attribute('periodicLldpInterval', value)

	@property
	def ProtocolInterfaces(self):
		"""Indicates the name of the protocol interface being used for this OpenFlow configuration.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterfaces')
	@ProtocolInterfaces.setter
	def ProtocolInterfaces(self, value):
		self._set_attribute('protocolInterfaces', value)

	@property
	def SendPortFeatureAtStartup(self):
		"""If true , Port feature request is sent , once OF session is established.

		Returns:
			bool
		"""
		return self._get_attribute('sendPortFeatureAtStartup')
	@SendPortFeatureAtStartup.setter
	def SendPortFeatureAtStartup(self, value):
		self._set_attribute('sendPortFeatureAtStartup', value)

	@property
	def TcpPort(self):
		"""Specify the TCP port for this interface.

		Returns:
			number
		"""
		return self._get_attribute('tcpPort')
	@TcpPort.setter
	def TcpPort(self, value):
		self._set_attribute('tcpPort', value)

	@property
	def TimeOutOption(self):
		"""Indicates the types of timeout options supported.

		Returns:
			str(multiplier|timeOutValue)
		"""
		return self._get_attribute('timeOutOption')
	@TimeOutOption.setter
	def TimeOutOption(self, value):
		self._set_attribute('timeOutOption', value)

	@property
	def TypeOfConnection(self):
		"""Indicates the type of connection used for the Interfaces.

		Returns:
			str(tcp|tls)
		"""
		return self._get_attribute('typeOfConnection')
	@TypeOfConnection.setter
	def TypeOfConnection(self, value):
		self._set_attribute('typeOfConnection', value)

	def add(self, AcceptUnconfiguredChannel=None, AllFlowsDelOnStart=None, AuxiliaryConnectionTimeout=None, BadVersionErrorAction=None, EchoInterval=None, EchoMultiplier=None, EchoTimeout=None, EnableEchoTimeOut=None, EnableMultipleLogicalSwitch=None, EnablePeriodicEcho=None, EnablePeriodicLldp=None, Enabled=None, FeatureRequestTimeout=None, FeatureRequestTimeoutAction=None, InstallFlowForLldp=None, LldpDestinationMacAddress=None, ModeOfConnection=None, NonHelloMessageStartupAction=None, PeriodicLldpInterval=None, ProtocolInterfaces=None, SendPortFeatureAtStartup=None, TcpPort=None, TimeOutOption=None, TypeOfConnection=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AcceptUnconfiguredChannel (bool): If true, un-configured channels are accepted for this interface.
			AllFlowsDelOnStart (bool): If set, Ixia sends out an OpenFlow flow delete message (all wildcard) at startup. This should delete all existing flows in DUT.
			AuxiliaryConnectionTimeout (str(auxReSendFeatureRequest|auxFeatureRequestTerminateConnection)): Period of time after which auxiliary connection will time out , if no messages are received.
			BadVersionErrorAction (str(auxReSendHello|auxTerminateConnection)): Defines what action to take in case an auxiliary connection receives an error of type OFPET_BAD_REQUEST and code OFPBRC_BAD_VERSION.
			EchoInterval (number): Indicates the periodic interval in seconds at which the Interface sends Echo Request Packets applicable if enablePeriodicEcho attribute is set.
			EchoMultiplier (number): Indicates the value specified for the selected Timeout option.
			EchoTimeout (number): Indicates the duration interval of the state machine waiting for echo reply to arrive applicable if echoTimeout is set.
			EnableEchoTimeOut (bool): If true, enables echoTimeout field.
			EnableMultipleLogicalSwitch (bool): if true, we add multiple number of switch per interface
			EnablePeriodicEcho (bool): If set enables echoInterval field.
			EnablePeriodicLldp (bool): If true, enables Periodic LLDP PacketOut Sending for each Switch Port
			Enabled (bool): If set enables the interface.
			FeatureRequestTimeout (number): Specifies the time after which a feature request will time out , if feature reply is received.
			FeatureRequestTimeoutAction (number): Specifies if action should be taken when feature request timeouts.
			InstallFlowForLldp (bool): If true, installs Flow in Switch for LLDP Packets to be explicitly send to Controller.
			LldpDestinationMacAddress (str): Indicates the Destination MAC Address for LLDP Packet Out.
			ModeOfConnection (str(passive|active|mixed)): Indicates the mode of connection used for the Interface.
			NonHelloMessageStartupAction (str(auxAcceptConnection|auxSendError)): Defines what action to take in case an auxiliary connection receives a non-hello message at startup.
			PeriodicLldpInterval (number): Indicates the Periodic LLDP Packet Out Interval.
			ProtocolInterfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): Indicates the name of the protocol interface being used for this OpenFlow configuration.
			SendPortFeatureAtStartup (bool): If true , Port feature request is sent , once OF session is established.
			TcpPort (number): Specify the TCP port for this interface.
			TimeOutOption (str(multiplier|timeOutValue)): Indicates the types of timeout options supported.
			TypeOfConnection (str(tcp|tls)): Indicates the type of connection used for the Interfaces.

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

	def find(self, AcceptUnconfiguredChannel=None, AllFlowsDelOnStart=None, AuxiliaryConnectionTimeout=None, BadVersionErrorAction=None, EchoInterval=None, EchoMultiplier=None, EchoTimeout=None, EnableEchoTimeOut=None, EnableMultipleLogicalSwitch=None, EnablePeriodicEcho=None, EnablePeriodicLldp=None, Enabled=None, FeatureRequestTimeout=None, FeatureRequestTimeoutAction=None, InstallFlowForLldp=None, LldpDestinationMacAddress=None, ModeOfConnection=None, NonHelloMessageStartupAction=None, PeriodicLldpInterval=None, ProtocolInterfaces=None, SendPortFeatureAtStartup=None, TcpPort=None, TimeOutOption=None, TypeOfConnection=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AcceptUnconfiguredChannel (bool): If true, un-configured channels are accepted for this interface.
			AllFlowsDelOnStart (bool): If set, Ixia sends out an OpenFlow flow delete message (all wildcard) at startup. This should delete all existing flows in DUT.
			AuxiliaryConnectionTimeout (str(auxReSendFeatureRequest|auxFeatureRequestTerminateConnection)): Period of time after which auxiliary connection will time out , if no messages are received.
			BadVersionErrorAction (str(auxReSendHello|auxTerminateConnection)): Defines what action to take in case an auxiliary connection receives an error of type OFPET_BAD_REQUEST and code OFPBRC_BAD_VERSION.
			EchoInterval (number): Indicates the periodic interval in seconds at which the Interface sends Echo Request Packets applicable if enablePeriodicEcho attribute is set.
			EchoMultiplier (number): Indicates the value specified for the selected Timeout option.
			EchoTimeout (number): Indicates the duration interval of the state machine waiting for echo reply to arrive applicable if echoTimeout is set.
			EnableEchoTimeOut (bool): If true, enables echoTimeout field.
			EnableMultipleLogicalSwitch (bool): if true, we add multiple number of switch per interface
			EnablePeriodicEcho (bool): If set enables echoInterval field.
			EnablePeriodicLldp (bool): If true, enables Periodic LLDP PacketOut Sending for each Switch Port
			Enabled (bool): If set enables the interface.
			FeatureRequestTimeout (number): Specifies the time after which a feature request will time out , if feature reply is received.
			FeatureRequestTimeoutAction (number): Specifies if action should be taken when feature request timeouts.
			InstallFlowForLldp (bool): If true, installs Flow in Switch for LLDP Packets to be explicitly send to Controller.
			LldpDestinationMacAddress (str): Indicates the Destination MAC Address for LLDP Packet Out.
			ModeOfConnection (str(passive|active|mixed)): Indicates the mode of connection used for the Interface.
			NonHelloMessageStartupAction (str(auxAcceptConnection|auxSendError)): Defines what action to take in case an auxiliary connection receives a non-hello message at startup.
			PeriodicLldpInterval (number): Indicates the Periodic LLDP Packet Out Interval.
			ProtocolInterfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): Indicates the name of the protocol interface being used for this OpenFlow configuration.
			SendPortFeatureAtStartup (bool): If true , Port feature request is sent , once OF session is established.
			TcpPort (number): Specify the TCP port for this interface.
			TimeOutOption (str(multiplier|timeOutValue)): Indicates the types of timeout options supported.
			TypeOfConnection (str(tcp|tls)): Indicates the type of connection used for the Interfaces.

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
