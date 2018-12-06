
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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('echoConfigureSrcIp')
	@EchoConfigureSrcIp.setter
	def EchoConfigureSrcIp(self, value):
		self._set_attribute('echoConfigureSrcIp', value)

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
	def EchoSrcIpv4Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('echoSrcIpv4Address')
	@EchoSrcIpv4Address.setter
	def EchoSrcIpv4Address(self, value):
		self._set_attribute('echoSrcIpv4Address', value)

	@property
	def EchoSrcIpv6Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('echoSrcIpv6Address')
	@EchoSrcIpv6Address.setter
	def EchoSrcIpv6Address(self, value):
		self._set_attribute('echoSrcIpv6Address', value)

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
	def EchoTxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoTxInterval')
	@EchoTxInterval.setter
	def EchoTxInterval(self, value):
		self._set_attribute('echoTxInterval', value)

	@property
	def EnableCtrlPlaneIndependent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCtrlPlaneIndependent')
	@EnableCtrlPlaneIndependent.setter
	def EnableCtrlPlaneIndependent(self, value):
		self._set_attribute('enableCtrlPlaneIndependent', value)

	@property
	def EnableDemandMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDemandMode')
	@EnableDemandMode.setter
	def EnableDemandMode(self, value):
		self._set_attribute('enableDemandMode', value)

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
	def FlapTxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flapTxInterval')
	@FlapTxInterval.setter
	def FlapTxInterval(self, value):
		self._set_attribute('flapTxInterval', value)

	@property
	def InterfaceId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def IpDifferentiatedServiceField(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipDifferentiatedServiceField')
	@IpDifferentiatedServiceField.setter
	def IpDifferentiatedServiceField(self, value):
		self._set_attribute('ipDifferentiatedServiceField', value)

	@property
	def MinRxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minRxInterval')
	@MinRxInterval.setter
	def MinRxInterval(self, value):
		self._set_attribute('minRxInterval', value)

	@property
	def Multiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def PollInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pollInterval')
	@PollInterval.setter
	def PollInterval(self, value):
		self._set_attribute('pollInterval', value)

	@property
	def TxInterval(self):
		"""

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
			EchoConfigureSrcIp (bool): 
			EchoInterval (number): 
			EchoSrcIpv4Address (str): 
			EchoSrcIpv6Address (str): 
			EchoTimeout (number): 
			EchoTxInterval (number): 
			EnableCtrlPlaneIndependent (bool): 
			EnableDemandMode (bool): 
			Enabled (bool): 
			FlapTxInterval (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IpDifferentiatedServiceField (number): 
			MinRxInterval (number): 
			Multiplier (number): 
			PollInterval (number): 
			TxInterval (number): 

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
			EchoConfigureSrcIp (bool): 
			EchoInterval (number): 
			EchoSrcIpv4Address (str): 
			EchoSrcIpv6Address (str): 
			EchoTimeout (number): 
			EchoTxInterval (number): 
			EnableCtrlPlaneIndependent (bool): 
			EnableDemandMode (bool): 
			Enabled (bool): 
			FlapTxInterval (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IpDifferentiatedServiceField (number): 
			MinRxInterval (number): 
			Multiplier (number): 
			PollInterval (number): 
			TxInterval (number): 

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

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)
