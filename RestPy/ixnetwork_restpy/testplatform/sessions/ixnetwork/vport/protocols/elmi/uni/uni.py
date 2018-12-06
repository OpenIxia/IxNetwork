
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


class Uni(Base):
	"""The Uni class encapsulates a user managed uni node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Uni property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'uni'

	def __init__(self, parent):
		super(Uni, self).__init__(parent)

	@property
	def Evc(self):
		"""An instance of the Evc class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.evc.Evc)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.evc import Evc
		return Evc(self)

	@property
	def EvcStatusLearnedInfo(self):
		"""An instance of the EvcStatusLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evcstatuslearnedinfo.evcstatuslearnedinfo.EvcStatusLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evcstatuslearnedinfo.evcstatuslearnedinfo import EvcStatusLearnedInfo
		return EvcStatusLearnedInfo(self)

	@property
	def LmiStatusLearnedInfo(self):
		"""An instance of the LmiStatusLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.lmistatuslearnedinfo.lmistatuslearnedinfo.LmiStatusLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.lmistatuslearnedinfo.lmistatuslearnedinfo import LmiStatusLearnedInfo
		return LmiStatusLearnedInfo(self)

	@property
	def UniStatus(self):
		"""An instance of the UniStatus class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.unistatus.unistatus.UniStatus)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.unistatus.unistatus import UniStatus
		return UniStatus(self)

	@property
	def UniStatusLearnedInfo(self):
		"""An instance of the UniStatusLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.unistatuslearnedinfo.unistatuslearnedinfo.UniStatusLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.unistatuslearnedinfo.unistatuslearnedinfo import UniStatusLearnedInfo
		return UniStatusLearnedInfo(self)

	@property
	def DataInstance(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataInstance')
	@DataInstance.setter
	def DataInstance(self, value):
		self._set_attribute('dataInstance', value)

	@property
	def EnablePollingVerificationTimer(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePollingVerificationTimer')
	@EnablePollingVerificationTimer.setter
	def EnablePollingVerificationTimer(self, value):
		self._set_attribute('enablePollingVerificationTimer', value)

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
	def IsEvcStatusLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isEvcStatusLearnedInfoRefreshed')

	@property
	def IsLmiStatusLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLmiStatusLearnedInfoRefreshed')

	@property
	def IsUniStatusLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isUniStatusLearnedInfoRefreshed')

	@property
	def Mode(self):
		"""

		Returns:
			str(uniC|uniN)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def OverrideDataInstance(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideDataInstance')
	@OverrideDataInstance.setter
	def OverrideDataInstance(self, value):
		self._set_attribute('overrideDataInstance', value)

	@property
	def OverrideReceiveSequenceNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideReceiveSequenceNumber')
	@OverrideReceiveSequenceNumber.setter
	def OverrideReceiveSequenceNumber(self, value):
		self._set_attribute('overrideReceiveSequenceNumber', value)

	@property
	def OverrideSendSequenceNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideSendSequenceNumber')
	@OverrideSendSequenceNumber.setter
	def OverrideSendSequenceNumber(self, value):
		self._set_attribute('overrideSendSequenceNumber', value)

	@property
	def PollingCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pollingCounter')
	@PollingCounter.setter
	def PollingCounter(self, value):
		self._set_attribute('pollingCounter', value)

	@property
	def PollingTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pollingTimer')
	@PollingTimer.setter
	def PollingTimer(self, value):
		self._set_attribute('pollingTimer', value)

	@property
	def PollingVerificationTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pollingVerificationTimer')
	@PollingVerificationTimer.setter
	def PollingVerificationTimer(self, value):
		self._set_attribute('pollingVerificationTimer', value)

	@property
	def ProtocolInterface(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def ProtocolVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('protocolVersion')
	@ProtocolVersion.setter
	def ProtocolVersion(self, value):
		self._set_attribute('protocolVersion', value)

	@property
	def ReceiveSequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('receiveSequenceNumber')
	@ReceiveSequenceNumber.setter
	def ReceiveSequenceNumber(self, value):
		self._set_attribute('receiveSequenceNumber', value)

	@property
	def SendSequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sendSequenceNumber')
	@SendSequenceNumber.setter
	def SendSequenceNumber(self, value):
		self._set_attribute('sendSequenceNumber', value)

	@property
	def StatusCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('statusCounter')
	@StatusCounter.setter
	def StatusCounter(self, value):
		self._set_attribute('statusCounter', value)

	def add(self, DataInstance=None, EnablePollingVerificationTimer=None, Enabled=None, Mode=None, OverrideDataInstance=None, OverrideReceiveSequenceNumber=None, OverrideSendSequenceNumber=None, PollingCounter=None, PollingTimer=None, PollingVerificationTimer=None, ProtocolInterface=None, ProtocolVersion=None, ReceiveSequenceNumber=None, SendSequenceNumber=None, StatusCounter=None):
		"""Adds a new uni node on the server and retrieves it in this instance.

		Args:
			DataInstance (number): 
			EnablePollingVerificationTimer (bool): 
			Enabled (bool): 
			Mode (str(uniC|uniN)): 
			OverrideDataInstance (bool): 
			OverrideReceiveSequenceNumber (bool): 
			OverrideSendSequenceNumber (bool): 
			PollingCounter (number): 
			PollingTimer (number): 
			PollingVerificationTimer (number): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			ProtocolVersion (number): 
			ReceiveSequenceNumber (number): 
			SendSequenceNumber (number): 
			StatusCounter (number): 

		Returns:
			self: This instance with all currently retrieved uni data using find and the newly added uni data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the uni data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DataInstance=None, EnablePollingVerificationTimer=None, Enabled=None, IsEvcStatusLearnedInfoRefreshed=None, IsLmiStatusLearnedInfoRefreshed=None, IsUniStatusLearnedInfoRefreshed=None, Mode=None, OverrideDataInstance=None, OverrideReceiveSequenceNumber=None, OverrideSendSequenceNumber=None, PollingCounter=None, PollingTimer=None, PollingVerificationTimer=None, ProtocolInterface=None, ProtocolVersion=None, ReceiveSequenceNumber=None, SendSequenceNumber=None, StatusCounter=None):
		"""Finds and retrieves uni data from the server.

		All named parameters support regex and can be used to selectively retrieve uni data from the server.
		By default the find method takes no parameters and will retrieve all uni data from the server.

		Args:
			DataInstance (number): 
			EnablePollingVerificationTimer (bool): 
			Enabled (bool): 
			IsEvcStatusLearnedInfoRefreshed (bool): 
			IsLmiStatusLearnedInfoRefreshed (bool): 
			IsUniStatusLearnedInfoRefreshed (bool): 
			Mode (str(uniC|uniN)): 
			OverrideDataInstance (bool): 
			OverrideReceiveSequenceNumber (bool): 
			OverrideSendSequenceNumber (bool): 
			PollingCounter (number): 
			PollingTimer (number): 
			PollingVerificationTimer (number): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			ProtocolVersion (number): 
			ReceiveSequenceNumber (number): 
			SendSequenceNumber (number): 
			StatusCounter (number): 

		Returns:
			self: This instance with matching uni data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of uni data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the uni data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshEvcStatusLearnedInfo(self):
		"""Executes the refreshEvcStatusLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=uni)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshEvcStatusLearnedInfo', payload=locals(), response_object=None)

	def RefreshLmiStatusLearnedInfo(self):
		"""Executes the refreshLmiStatusLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=uni)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLmiStatusLearnedInfo', payload=locals(), response_object=None)

	def RefreshUniStatusLearnedInfo(self):
		"""Executes the refreshUniStatusLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=uni)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshUniStatusLearnedInfo', payload=locals(), response_object=None)
