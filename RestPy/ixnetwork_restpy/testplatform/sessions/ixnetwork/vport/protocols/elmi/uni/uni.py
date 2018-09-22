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
		"""This four-octet field indicates the Data Instance value to be sent in transmitted packet. It will be configurable only if Override Data Instance is enabled. By default it is grayed out with default value 0 for UNI-C and 1 for UNI-N. Max 4294967295, Min 0 for UNI-C and 1 for UNI- V. Change of value in this field takes effect when protocol is running.

		Returns:
			number
		"""
		return self._get_attribute('dataInstance')
	@DataInstance.setter
	def DataInstance(self, value):
		self._set_attribute('dataInstance', value)

	@property
	def EnablePollingVerificationTimer(self):
		"""If enabled, it shows the default value.

		Returns:
			bool
		"""
		return self._get_attribute('enablePollingVerificationTimer')
	@EnablePollingVerificationTimer.setter
	def EnablePollingVerificationTimer(self, value):
		self._set_attribute('enablePollingVerificationTimer', value)

	@property
	def Enabled(self):
		"""It signifies whether the protocol is enabled or disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IsEvcStatusLearnedInfoRefreshed(self):
		"""It checks whether the EVC status learned info is refreshed or not.

		Returns:
			bool
		"""
		return self._get_attribute('isEvcStatusLearnedInfoRefreshed')

	@property
	def IsLmiStatusLearnedInfoRefreshed(self):
		"""It checks whether the LMI status learned info is refreshed or not.

		Returns:
			bool
		"""
		return self._get_attribute('isLmiStatusLearnedInfoRefreshed')

	@property
	def IsUniStatusLearnedInfoRefreshed(self):
		"""It checks whether the UNI status learned info is refreshed or not.

		Returns:
			bool
		"""
		return self._get_attribute('isUniStatusLearnedInfoRefreshed')

	@property
	def Mode(self):
		"""It is a type of UNI end point.

		Returns:
			str(uniC|uniN)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def OverrideDataInstance(self):
		"""If enabled, it updates the Data Instance field of Data Instance Information Element (IE). Default is false. Change of value in this field takes effect when protocol is running.

		Returns:
			bool
		"""
		return self._get_attribute('overrideDataInstance')
	@OverrideDataInstance.setter
	def OverrideDataInstance(self, value):
		self._set_attribute('overrideDataInstance', value)

	@property
	def OverrideReceiveSequenceNumber(self):
		"""If enabled, it updates the receive sequence number. This is used for negative testing. Default is false. Change of value in this field takes effect when protocol is running.

		Returns:
			bool
		"""
		return self._get_attribute('overrideReceiveSequenceNumber')
	@OverrideReceiveSequenceNumber.setter
	def OverrideReceiveSequenceNumber(self, value):
		self._set_attribute('overrideReceiveSequenceNumber', value)

	@property
	def OverrideSendSequenceNumber(self):
		"""If enabled, it updates the send sequence number. This is used for negative testing. Default is false. Change of value in this field takes effect when protocol is running.

		Returns:
			bool
		"""
		return self._get_attribute('overrideSendSequenceNumber')
	@OverrideSendSequenceNumber.setter
	def OverrideSendSequenceNumber(self, value):
		self._set_attribute('overrideSendSequenceNumber', value)

	@property
	def PollingCounter(self):
		"""It signifies the full status (status of UNI and all EVCs) polling count. Range is 1- 65k. Default is 360. This is applicable only for UNI-C.

		Returns:
			number
		"""
		return self._get_attribute('pollingCounter')
	@PollingCounter.setter
	def PollingCounter(self, value):
		self._set_attribute('pollingCounter', value)

	@property
	def PollingTimer(self):
		"""The range is 5-30 in seconds. Default is 10 seconds. This is applicable only for UNI-C.

		Returns:
			number
		"""
		return self._get_attribute('pollingTimer')
	@PollingTimer.setter
	def PollingTimer(self, value):
		self._set_attribute('pollingTimer', value)

	@property
	def PollingVerificationTimer(self):
		"""This is applicable only for UNI-N. Range is 5-30 secs. Default is 15 seconds.

		Returns:
			number
		"""
		return self._get_attribute('pollingVerificationTimer')
	@PollingVerificationTimer.setter
	def PollingVerificationTimer(self, value):
		self._set_attribute('pollingVerificationTimer', value)

	@property
	def ProtocolInterface(self):
		"""It signifies the configured protocol interface. User has to select one interface to enable configuring UNI. Until and unless protocol interface is selected user will not be able to configure and enable UNI. Default is unassigned.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

	@property
	def ProtocolVersion(self):
		"""This one-octet field indicates the version supported by the sending entity (UNI-C or UNI-N). Default value is ox1. Max 255, Min - 1.

		Returns:
			number
		"""
		return self._get_attribute('protocolVersion')
	@ProtocolVersion.setter
	def ProtocolVersion(self, value):
		self._set_attribute('protocolVersion', value)

	@property
	def ReceiveSequenceNumber(self):
		"""This one-octet field indicates the sequence number to be sent in the 'Receive Sequence Number' in transmitted packet. It will be configurable only if Override Receive Sequence Number is enabled. Default value of this field is 0. Max 255, Min - 0 Change of value in this field takes effect when protocol is running.

		Returns:
			number
		"""
		return self._get_attribute('receiveSequenceNumber')
	@ReceiveSequenceNumber.setter
	def ReceiveSequenceNumber(self, value):
		self._set_attribute('receiveSequenceNumber', value)

	@property
	def SendSequenceNumber(self):
		"""This one-octet field indicates the sequence number to be sent in the 'Send Sequence Number' field in transmitted packet. It will be configurable only if Override Send Sequence Number is enabled. Default value of this field is 0. Max 255, Min - 0 Change of value in this field takes effect when protocol is running.

		Returns:
			number
		"""
		return self._get_attribute('sendSequenceNumber')
	@SendSequenceNumber.setter
	def SendSequenceNumber(self, value):
		self._set_attribute('sendSequenceNumber', value)

	@property
	def StatusCounter(self):
		"""It signifies the count of consecutive errors. Range is 2 10. Default is 4.

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
			DataInstance (number): This four-octet field indicates the Data Instance value to be sent in transmitted packet. It will be configurable only if Override Data Instance is enabled. By default it is grayed out with default value 0 for UNI-C and 1 for UNI-N. Max 4294967295, Min 0 for UNI-C and 1 for UNI- V. Change of value in this field takes effect when protocol is running.
			EnablePollingVerificationTimer (bool): If enabled, it shows the default value.
			Enabled (bool): It signifies whether the protocol is enabled or disabled.
			Mode (str(uniC|uniN)): It is a type of UNI end point.
			OverrideDataInstance (bool): If enabled, it updates the Data Instance field of Data Instance Information Element (IE). Default is false. Change of value in this field takes effect when protocol is running.
			OverrideReceiveSequenceNumber (bool): If enabled, it updates the receive sequence number. This is used for negative testing. Default is false. Change of value in this field takes effect when protocol is running.
			OverrideSendSequenceNumber (bool): If enabled, it updates the send sequence number. This is used for negative testing. Default is false. Change of value in this field takes effect when protocol is running.
			PollingCounter (number): It signifies the full status (status of UNI and all EVCs) polling count. Range is 1- 65k. Default is 360. This is applicable only for UNI-C.
			PollingTimer (number): The range is 5-30 in seconds. Default is 10 seconds. This is applicable only for UNI-C.
			PollingVerificationTimer (number): This is applicable only for UNI-N. Range is 5-30 secs. Default is 15 seconds.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): It signifies the configured protocol interface. User has to select one interface to enable configuring UNI. Until and unless protocol interface is selected user will not be able to configure and enable UNI. Default is unassigned.
			ProtocolVersion (number): This one-octet field indicates the version supported by the sending entity (UNI-C or UNI-N). Default value is ox1. Max 255, Min - 1.
			ReceiveSequenceNumber (number): This one-octet field indicates the sequence number to be sent in the 'Receive Sequence Number' in transmitted packet. It will be configurable only if Override Receive Sequence Number is enabled. Default value of this field is 0. Max 255, Min - 0 Change of value in this field takes effect when protocol is running.
			SendSequenceNumber (number): This one-octet field indicates the sequence number to be sent in the 'Send Sequence Number' field in transmitted packet. It will be configurable only if Override Send Sequence Number is enabled. Default value of this field is 0. Max 255, Min - 0 Change of value in this field takes effect when protocol is running.
			StatusCounter (number): It signifies the count of consecutive errors. Range is 2 10. Default is 4.

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
			DataInstance (number): This four-octet field indicates the Data Instance value to be sent in transmitted packet. It will be configurable only if Override Data Instance is enabled. By default it is grayed out with default value 0 for UNI-C and 1 for UNI-N. Max 4294967295, Min 0 for UNI-C and 1 for UNI- V. Change of value in this field takes effect when protocol is running.
			EnablePollingVerificationTimer (bool): If enabled, it shows the default value.
			Enabled (bool): It signifies whether the protocol is enabled or disabled.
			IsEvcStatusLearnedInfoRefreshed (bool): It checks whether the EVC status learned info is refreshed or not.
			IsLmiStatusLearnedInfoRefreshed (bool): It checks whether the LMI status learned info is refreshed or not.
			IsUniStatusLearnedInfoRefreshed (bool): It checks whether the UNI status learned info is refreshed or not.
			Mode (str(uniC|uniN)): It is a type of UNI end point.
			OverrideDataInstance (bool): If enabled, it updates the Data Instance field of Data Instance Information Element (IE). Default is false. Change of value in this field takes effect when protocol is running.
			OverrideReceiveSequenceNumber (bool): If enabled, it updates the receive sequence number. This is used for negative testing. Default is false. Change of value in this field takes effect when protocol is running.
			OverrideSendSequenceNumber (bool): If enabled, it updates the send sequence number. This is used for negative testing. Default is false. Change of value in this field takes effect when protocol is running.
			PollingCounter (number): It signifies the full status (status of UNI and all EVCs) polling count. Range is 1- 65k. Default is 360. This is applicable only for UNI-C.
			PollingTimer (number): The range is 5-30 in seconds. Default is 10 seconds. This is applicable only for UNI-C.
			PollingVerificationTimer (number): This is applicable only for UNI-N. Range is 5-30 secs. Default is 15 seconds.
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): It signifies the configured protocol interface. User has to select one interface to enable configuring UNI. Until and unless protocol interface is selected user will not be able to configure and enable UNI. Default is unassigned.
			ProtocolVersion (number): This one-octet field indicates the version supported by the sending entity (UNI-C or UNI-N). Default value is ox1. Max 255, Min - 1.
			ReceiveSequenceNumber (number): This one-octet field indicates the sequence number to be sent in the 'Receive Sequence Number' in transmitted packet. It will be configurable only if Override Receive Sequence Number is enabled. Default value of this field is 0. Max 255, Min - 0 Change of value in this field takes effect when protocol is running.
			SendSequenceNumber (number): This one-octet field indicates the sequence number to be sent in the 'Send Sequence Number' field in transmitted packet. It will be configurable only if Override Send Sequence Number is enabled. Default value of this field is 0. Max 255, Min - 0 Change of value in this field takes effect when protocol is running.
			StatusCounter (number): It signifies the count of consecutive errors. Range is 2 10. Default is 4.

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

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=uni)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshEvcStatusLearnedInfo', payload=locals(), response_object=None)

	def RefreshLmiStatusLearnedInfo(self):
		"""Executes the refreshLmiStatusLearnedInfo operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=uni)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLmiStatusLearnedInfo', payload=locals(), response_object=None)

	def RefreshUniStatusLearnedInfo(self):
		"""Executes the refreshUniStatusLearnedInfo operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=uni)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshUniStatusLearnedInfo', payload=locals(), response_object=None)
