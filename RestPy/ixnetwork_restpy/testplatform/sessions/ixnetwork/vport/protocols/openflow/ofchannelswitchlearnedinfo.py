
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


class OfChannelSwitchLearnedInfo(Base):
	"""The OfChannelSwitchLearnedInfo class encapsulates a system managed ofChannelSwitchLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelSwitchLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelSwitchLearnedInfo'

	def __init__(self, parent):
		super(OfChannelSwitchLearnedInfo, self).__init__(parent)

	@property
	def OfChannelPortsSwitchLearnedInfo(self):
		"""An instance of the OfChannelPortsSwitchLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportsswitchlearnedinfo.OfChannelPortsSwitchLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportsswitchlearnedinfo import OfChannelPortsSwitchLearnedInfo
		return OfChannelPortsSwitchLearnedInfo(self)

	@property
	def OfChannelSessionPeersLearnedInformation(self):
		"""An instance of the OfChannelSessionPeersLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelsessionpeerslearnedinformation.OfChannelSessionPeersLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelsessionpeerslearnedinformation import OfChannelSessionPeersLearnedInformation
		return OfChannelSessionPeersLearnedInformation(self)

	@property
	def ActionsSupported(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionsSupported')

	@property
	def AveragePacketInReplyDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('averagePacketInReplyDelay')
	@AveragePacketInReplyDelay.setter
	def AveragePacketInReplyDelay(self, value):
		self._set_attribute('averagePacketInReplyDelay', value)

	@property
	def Capabilities(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('capabilities')

	@property
	def ConfigFlags(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('configFlags')

	@property
	def ConfiguredPacketInReplyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('configuredPacketInReplyCount')
	@ConfiguredPacketInReplyCount.setter
	def ConfiguredPacketInReplyCount(self, value):
		self._set_attribute('configuredPacketInReplyCount', value)

	@property
	def ConfiguredPacketInSentCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('configuredPacketInSentCount')
	@ConfiguredPacketInSentCount.setter
	def ConfiguredPacketInSentCount(self, value):
		self._set_attribute('configuredPacketInSentCount', value)

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
			number
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
	def MaxBufferSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxBufferSize')

	@property
	def MaxPacketInBytes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxPacketInBytes')

	@property
	def NegotiatedVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfAuxiliaryConnection(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfAuxiliaryConnection')
	@NumberOfAuxiliaryConnection.setter
	def NumberOfAuxiliaryConnection(self, value):
		self._set_attribute('numberOfAuxiliaryConnection', value)

	@property
	def NumberOfErrorsSent(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfErrorsSent')

	@property
	def NumberOfPorts(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def NumberofTable(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberofTable')

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
	@RemotePortNumber.setter
	def RemotePortNumber(self, value):
		self._set_attribute('remotePortNumber', value)

	@property
	def SessionType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sessionType')

	def find(self, ActionsSupported=None, AveragePacketInReplyDelay=None, Capabilities=None, ConfigFlags=None, ConfiguredPacketInReplyCount=None, ConfiguredPacketInSentCount=None, DataPathId=None, DataPathIdAsHex=None, FlowRate=None, GenerationId=None, LastErrorCode=None, LastErrorType=None, LocalIp=None, MaxBufferSize=None, MaxPacketInBytes=None, NegotiatedVersion=None, NumberOfAuxiliaryConnection=None, NumberOfErrorsSent=None, NumberOfPorts=None, NumberofTable=None, RemoteIp=None, RemotePortNumber=None, SessionType=None):
		"""Finds and retrieves ofChannelSwitchLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelSwitchLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelSwitchLearnedInfo data from the server.

		Args:
			ActionsSupported (str): 
			AveragePacketInReplyDelay (number): 
			Capabilities (str): 
			ConfigFlags (str): 
			ConfiguredPacketInReplyCount (number): 
			ConfiguredPacketInSentCount (number): 
			DataPathId (str): 
			DataPathIdAsHex (str): 
			FlowRate (number): 
			GenerationId (number): 
			LastErrorCode (str): 
			LastErrorType (str): 
			LocalIp (str): 
			MaxBufferSize (number): 
			MaxPacketInBytes (number): 
			NegotiatedVersion (number): 
			NumberOfAuxiliaryConnection (number): 
			NumberOfErrorsSent (number): 
			NumberOfPorts (number): 
			NumberofTable (number): 
			RemoteIp (str): 
			RemotePortNumber (number): 
			SessionType (str): 

		Returns:
			self: This instance with matching ofChannelSwitchLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelSwitchLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelSwitchLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannelSwitchLearnedInfo)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
