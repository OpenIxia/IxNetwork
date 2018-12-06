
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


class GeneralLearnedInfo(Base):
	"""The GeneralLearnedInfo class encapsulates a system managed generalLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GeneralLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'generalLearnedInfo'

	def __init__(self, parent):
		super(GeneralLearnedInfo, self).__init__(parent)

	@property
	def AisRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('aisRx')

	@property
	def AisState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('aisState')

	@property
	def AisTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('aisTx')

	@property
	def AlarmTypeAis(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('alarmTypeAis')

	@property
	def AlarmTypeLck(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('alarmTypeLck')

	@property
	def ApsLocalDataPath(self):
		"""

		Returns:
			str(working|protect|na)
		"""
		return self._get_attribute('apsLocalDataPath')

	@property
	def ApsLocalFaultPath(self):
		"""

		Returns:
			str(working|protect|both|none|na)
		"""
		return self._get_attribute('apsLocalFaultPath')

	@property
	def ApsLocalState(self):
		"""

		Returns:
			str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)
		"""
		return self._get_attribute('apsLocalState')

	@property
	def ApsRemoteDataPath(self):
		"""

		Returns:
			str(protect|na|working)
		"""
		return self._get_attribute('apsRemoteDataPath')

	@property
	def ApsRemoteFaultPath(self):
		"""

		Returns:
			str(na|working|protect|both|none)
		"""
		return self._get_attribute('apsRemoteFaultPath')

	@property
	def ApsRemoteRequestState(self):
		"""

		Returns:
			str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)
		"""
		return self._get_attribute('apsRemoteRequestState')

	@property
	def ContinuityCheckLocalState(self):
		"""

		Returns:
			str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)
		"""
		return self._get_attribute('continuityCheckLocalState')

	@property
	def ContinuityCheckRemoteState(self):
		"""

		Returns:
			str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)
		"""
		return self._get_attribute('continuityCheckRemoteState')

	@property
	def ContinuityCheckRxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('continuityCheckRxInterval')

	@property
	def ContinuityCheckTxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('continuityCheckTxInterval')

	@property
	def IncomingLabelOuterInner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def LastAlarmDuration(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastAlarmDuration')

	@property
	def LckRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lckRx')

	@property
	def LckState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lckState')

	@property
	def LckTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lckTx')

	@property
	def Ldi(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ldi')

	@property
	def LocalPwStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localPwStatus')

	@property
	def OutgoingLabelOuterInner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def RemoteDefectIndication(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteDefectIndication')

	@property
	def RemotePwStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remotePwStatus')

	@property
	def Role(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def TimeSinceLastAlarm(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('timeSinceLastAlarm')

	@property
	def Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, AisRx=None, AisState=None, AisTx=None, AlarmTypeAis=None, AlarmTypeLck=None, ApsLocalDataPath=None, ApsLocalFaultPath=None, ApsLocalState=None, ApsRemoteDataPath=None, ApsRemoteFaultPath=None, ApsRemoteRequestState=None, ContinuityCheckLocalState=None, ContinuityCheckRemoteState=None, ContinuityCheckRxInterval=None, ContinuityCheckTxInterval=None, IncomingLabelOuterInner=None, LastAlarmDuration=None, LckRx=None, LckState=None, LckTx=None, Ldi=None, LocalPwStatus=None, OutgoingLabelOuterInner=None, RemoteDefectIndication=None, RemotePwStatus=None, Role=None, TimeSinceLastAlarm=None, Type=None):
		"""Finds and retrieves generalLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve generalLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all generalLearnedInfo data from the server.

		Args:
			AisRx (number): 
			AisState (str): 
			AisTx (number): 
			AlarmTypeAis (str): 
			AlarmTypeLck (str): 
			ApsLocalDataPath (str(working|protect|na)): 
			ApsLocalFaultPath (str(working|protect|both|none|na)): 
			ApsLocalState (str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)): 
			ApsRemoteDataPath (str(protect|na|working)): 
			ApsRemoteFaultPath (str(na|working|protect|both|none)): 
			ApsRemoteRequestState (str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)): 
			ContinuityCheckLocalState (str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)): 
			ContinuityCheckRemoteState (str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)): 
			ContinuityCheckRxInterval (number): 
			ContinuityCheckTxInterval (number): 
			IncomingLabelOuterInner (str): 
			LastAlarmDuration (str): 
			LckRx (number): 
			LckState (str): 
			LckTx (number): 
			Ldi (str): 
			LocalPwStatus (str): 
			OutgoingLabelOuterInner (str): 
			RemoteDefectIndication (str): 
			RemotePwStatus (str): 
			Role (str): 
			TimeSinceLastAlarm (str): 
			Type (str): 

		Returns:
			self: This instance with matching generalLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of generalLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the generalLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=generalLearnedInfo)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
