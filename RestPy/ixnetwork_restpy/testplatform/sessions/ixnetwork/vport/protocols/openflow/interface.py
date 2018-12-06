
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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('acceptUnconfiguredChannel')
	@AcceptUnconfiguredChannel.setter
	def AcceptUnconfiguredChannel(self, value):
		self._set_attribute('acceptUnconfiguredChannel', value)

	@property
	def AllFlowsDelOnStart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('allFlowsDelOnStart')
	@AllFlowsDelOnStart.setter
	def AllFlowsDelOnStart(self, value):
		self._set_attribute('allFlowsDelOnStart', value)

	@property
	def AuxiliaryConnectionTimeout(self):
		"""

		Returns:
			str(auxReSendFeatureRequest|auxFeatureRequestTerminateConnection)
		"""
		return self._get_attribute('auxiliaryConnectionTimeout')
	@AuxiliaryConnectionTimeout.setter
	def AuxiliaryConnectionTimeout(self, value):
		self._set_attribute('auxiliaryConnectionTimeout', value)

	@property
	def BadVersionErrorAction(self):
		"""

		Returns:
			str(auxReSendHello|auxTerminateConnection)
		"""
		return self._get_attribute('badVersionErrorAction')
	@BadVersionErrorAction.setter
	def BadVersionErrorAction(self, value):
		self._set_attribute('badVersionErrorAction', value)

	@property
	def EchoInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoInterval')
	@EchoInterval.setter
	def EchoInterval(self, value):
		self._set_attribute('echoInterval', value)

	@property
	def EchoMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoMultiplier')
	@EchoMultiplier.setter
	def EchoMultiplier(self, value):
		self._set_attribute('echoMultiplier', value)

	@property
	def EchoTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoTimeout')
	@EchoTimeout.setter
	def EchoTimeout(self, value):
		self._set_attribute('echoTimeout', value)

	@property
	def EnableEchoTimeOut(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableEchoTimeOut')
	@EnableEchoTimeOut.setter
	def EnableEchoTimeOut(self, value):
		self._set_attribute('enableEchoTimeOut', value)

	@property
	def EnableMultipleLogicalSwitch(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMultipleLogicalSwitch')
	@EnableMultipleLogicalSwitch.setter
	def EnableMultipleLogicalSwitch(self, value):
		self._set_attribute('enableMultipleLogicalSwitch', value)

	@property
	def EnablePeriodicEcho(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicEcho')
	@EnablePeriodicEcho.setter
	def EnablePeriodicEcho(self, value):
		self._set_attribute('enablePeriodicEcho', value)

	@property
	def EnablePeriodicLldp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicLldp')
	@EnablePeriodicLldp.setter
	def EnablePeriodicLldp(self, value):
		self._set_attribute('enablePeriodicLldp', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FeatureRequestTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('featureRequestTimeout')
	@FeatureRequestTimeout.setter
	def FeatureRequestTimeout(self, value):
		self._set_attribute('featureRequestTimeout', value)

	@property
	def FeatureRequestTimeoutAction(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('featureRequestTimeoutAction')
	@FeatureRequestTimeoutAction.setter
	def FeatureRequestTimeoutAction(self, value):
		self._set_attribute('featureRequestTimeoutAction', value)

	@property
	def InstallFlowForLldp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('installFlowForLldp')
	@InstallFlowForLldp.setter
	def InstallFlowForLldp(self, value):
		self._set_attribute('installFlowForLldp', value)

	@property
	def LldpDestinationMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lldpDestinationMacAddress')
	@LldpDestinationMacAddress.setter
	def LldpDestinationMacAddress(self, value):
		self._set_attribute('lldpDestinationMacAddress', value)

	@property
	def ModeOfConnection(self):
		"""

		Returns:
			str(passive|active|mixed)
		"""
		return self._get_attribute('modeOfConnection')
	@ModeOfConnection.setter
	def ModeOfConnection(self, value):
		self._set_attribute('modeOfConnection', value)

	@property
	def NonHelloMessageStartupAction(self):
		"""

		Returns:
			str(auxAcceptConnection|auxSendError)
		"""
		return self._get_attribute('nonHelloMessageStartupAction')
	@NonHelloMessageStartupAction.setter
	def NonHelloMessageStartupAction(self, value):
		self._set_attribute('nonHelloMessageStartupAction', value)

	@property
	def PeriodicLldpInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('periodicLldpInterval')
	@PeriodicLldpInterval.setter
	def PeriodicLldpInterval(self, value):
		self._set_attribute('periodicLldpInterval', value)

	@property
	def ProtocolInterfaces(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterfaces')
	@ProtocolInterfaces.setter
	def ProtocolInterfaces(self, value):
		self._set_attribute('protocolInterfaces', value)

	@property
	def SendPortFeatureAtStartup(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendPortFeatureAtStartup')
	@SendPortFeatureAtStartup.setter
	def SendPortFeatureAtStartup(self, value):
		self._set_attribute('sendPortFeatureAtStartup', value)

	@property
	def TcpPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tcpPort')
	@TcpPort.setter
	def TcpPort(self, value):
		self._set_attribute('tcpPort', value)

	@property
	def TimeOutOption(self):
		"""

		Returns:
			str(multiplier|timeOutValue)
		"""
		return self._get_attribute('timeOutOption')
	@TimeOutOption.setter
	def TimeOutOption(self, value):
		self._set_attribute('timeOutOption', value)

	@property
	def TypeOfConnection(self):
		"""

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
			AcceptUnconfiguredChannel (bool): 
			AllFlowsDelOnStart (bool): 
			AuxiliaryConnectionTimeout (str(auxReSendFeatureRequest|auxFeatureRequestTerminateConnection)): 
			BadVersionErrorAction (str(auxReSendHello|auxTerminateConnection)): 
			EchoInterval (number): 
			EchoMultiplier (number): 
			EchoTimeout (number): 
			EnableEchoTimeOut (bool): 
			EnableMultipleLogicalSwitch (bool): 
			EnablePeriodicEcho (bool): 
			EnablePeriodicLldp (bool): 
			Enabled (bool): 
			FeatureRequestTimeout (number): 
			FeatureRequestTimeoutAction (number): 
			InstallFlowForLldp (bool): 
			LldpDestinationMacAddress (str): 
			ModeOfConnection (str(passive|active|mixed)): 
			NonHelloMessageStartupAction (str(auxAcceptConnection|auxSendError)): 
			PeriodicLldpInterval (number): 
			ProtocolInterfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			SendPortFeatureAtStartup (bool): 
			TcpPort (number): 
			TimeOutOption (str(multiplier|timeOutValue)): 
			TypeOfConnection (str(tcp|tls)): 

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
			AcceptUnconfiguredChannel (bool): 
			AllFlowsDelOnStart (bool): 
			AuxiliaryConnectionTimeout (str(auxReSendFeatureRequest|auxFeatureRequestTerminateConnection)): 
			BadVersionErrorAction (str(auxReSendHello|auxTerminateConnection)): 
			EchoInterval (number): 
			EchoMultiplier (number): 
			EchoTimeout (number): 
			EnableEchoTimeOut (bool): 
			EnableMultipleLogicalSwitch (bool): 
			EnablePeriodicEcho (bool): 
			EnablePeriodicLldp (bool): 
			Enabled (bool): 
			FeatureRequestTimeout (number): 
			FeatureRequestTimeoutAction (number): 
			InstallFlowForLldp (bool): 
			LldpDestinationMacAddress (str): 
			ModeOfConnection (str(passive|active|mixed)): 
			NonHelloMessageStartupAction (str(auxAcceptConnection|auxSendError)): 
			PeriodicLldpInterval (number): 
			ProtocolInterfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			SendPortFeatureAtStartup (bool): 
			TcpPort (number): 
			TimeOutOption (str(multiplier|timeOutValue)): 
			TypeOfConnection (str(tcp|tls)): 

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
