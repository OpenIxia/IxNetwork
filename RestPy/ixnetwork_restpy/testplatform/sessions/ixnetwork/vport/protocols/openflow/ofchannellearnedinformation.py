
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


class OfChannelLearnedInformation(Base):
	"""The OfChannelLearnedInformation class encapsulates a system managed ofChannelLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelLearnedInformation'

	def __init__(self, parent):
		super(OfChannelLearnedInformation, self).__init__(parent)

	@property
	def ControllerAuxiliaryConnectionLearnedInfo(self):
		"""An instance of the ControllerAuxiliaryConnectionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllerauxiliaryconnectionlearnedinfo.ControllerAuxiliaryConnectionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllerauxiliaryconnectionlearnedinfo import ControllerAuxiliaryConnectionLearnedInfo
		return ControllerAuxiliaryConnectionLearnedInfo(self)

	@property
	def OfChannelPortsLearnedInformation(self):
		"""An instance of the OfChannelPortsLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportslearnedinformation.OfChannelPortsLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportslearnedinformation import OfChannelPortsLearnedInformation
		return OfChannelPortsLearnedInformation(self)

	@property
	def ActionsSupported(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionsSupported')

	@property
	def Capabilities(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('capabilities')

	@property
	def DataPathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def FlowRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowRate')

	@property
	def GenerationId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('generationId')

	@property
	def LastErrorCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastErrorCode')

	@property
	def LastErrorType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastErrorType')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def LocalPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localPortNumber')

	@property
	def MaxBufferSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxBufferSize')

	@property
	def NegotiatedVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfErrorsReceived(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfErrorsReceived')

	@property
	def NumberOfPorts(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def NumberOfTables(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfTables')

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def RemotePortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remotePortNumber')

	@property
	def ReplyState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def Role(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def SessionType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sessionType')

	def find(self, ActionsSupported=None, Capabilities=None, DataPathId=None, DataPathIdAsHex=None, FlowRate=None, GenerationId=None, LastErrorCode=None, LastErrorType=None, LocalIp=None, LocalPortNumber=None, MaxBufferSize=None, NegotiatedVersion=None, NumberOfErrorsReceived=None, NumberOfPorts=None, NumberOfTables=None, RemoteIp=None, RemotePortNumber=None, ReplyState=None, Role=None, SessionType=None):
		"""Finds and retrieves ofChannelLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelLearnedInformation data from the server.

		Args:
			ActionsSupported (str): 
			Capabilities (str): 
			DataPathId (str): 
			DataPathIdAsHex (str): 
			FlowRate (number): 
			GenerationId (str): 
			LastErrorCode (str): 
			LastErrorType (str): 
			LocalIp (str): 
			LocalPortNumber (number): 
			MaxBufferSize (number): 
			NegotiatedVersion (number): 
			NumberOfErrorsReceived (number): 
			NumberOfPorts (number): 
			NumberOfTables (number): 
			RemoteIp (str): 
			RemotePortNumber (number): 
			ReplyState (str): 
			Role (str): 
			SessionType (str): 

		Returns:
			self: This instance with matching ofChannelLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannelLearnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)

	def ConfigureOfChannel(self):
		"""Executes the configureOfChannel operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannelLearnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ConfigureOfChannel', payload=locals(), response_object=None)
