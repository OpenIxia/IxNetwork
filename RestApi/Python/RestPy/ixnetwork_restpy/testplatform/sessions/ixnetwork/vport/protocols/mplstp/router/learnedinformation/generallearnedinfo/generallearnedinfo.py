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
		"""This signifies the number of AIS frames received.

		Returns:
			number
		"""
		return self._get_attribute('aisRx')

	@property
	def AisState(self):
		"""This signifies the state of AIS, either Clear or Fault.

		Returns:
			str
		"""
		return self._get_attribute('aisState')

	@property
	def AisTx(self):
		"""This signifies the number of AIS frames transmitted.

		Returns:
			number
		"""
		return self._get_attribute('aisTx')

	@property
	def AlarmTypeAis(self):
		"""This signifies the type of the AIS alarm, either ietf or y1731.

		Returns:
			str
		"""
		return self._get_attribute('alarmTypeAis')

	@property
	def AlarmTypeLck(self):
		"""This signifies the type of the LCK alarm, either ietf or y1731.

		Returns:
			str
		"""
		return self._get_attribute('alarmTypeLck')

	@property
	def ApsLocalDataPath(self):
		"""This signifies the path of the APS local data.

		Returns:
			str(working|protect|na)
		"""
		return self._get_attribute('apsLocalDataPath')

	@property
	def ApsLocalFaultPath(self):
		"""This signifies the path of the APS local fault.

		Returns:
			str(working|protect|both|none|na)
		"""
		return self._get_attribute('apsLocalFaultPath')

	@property
	def ApsLocalState(self):
		"""This signifies the APS local state information.

		Returns:
			str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)
		"""
		return self._get_attribute('apsLocalState')

	@property
	def ApsRemoteDataPath(self):
		"""This signifies the path of the APS remote data.

		Returns:
			str(protect|na|working)
		"""
		return self._get_attribute('apsRemoteDataPath')

	@property
	def ApsRemoteFaultPath(self):
		"""This signifies the path of the APS remote fault.

		Returns:
			str(na|working|protect|both|none)
		"""
		return self._get_attribute('apsRemoteFaultPath')

	@property
	def ApsRemoteRequestState(self):
		"""This signifies the APS remote request state information.

		Returns:
			str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)
		"""
		return self._get_attribute('apsRemoteRequestState')

	@property
	def ContinuityCheckLocalState(self):
		"""This signifies the status of the Continuity Check Local State.

		Returns:
			str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)
		"""
		return self._get_attribute('continuityCheckLocalState')

	@property
	def ContinuityCheckRemoteState(self):
		"""This signifies the status of the Continuity Check Remote State.

		Returns:
			str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)
		"""
		return self._get_attribute('continuityCheckRemoteState')

	@property
	def ContinuityCheckRxInterval(self):
		"""This Signifies the CC Rx Interval configured on the source side.

		Returns:
			number
		"""
		return self._get_attribute('continuityCheckRxInterval')

	@property
	def ContinuityCheckTxInterval(self):
		"""This Signifies the Negotiated CC Tx Interval on the source side.

		Returns:
			number
		"""
		return self._get_attribute('continuityCheckTxInterval')

	@property
	def IncomingLabelOuterInner(self):
		"""This signifies the incoming label information.

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def LastAlarmDuration(self):
		"""This signifies the duration for how long the LSP/PW was in fault state.

		Returns:
			str
		"""
		return self._get_attribute('lastAlarmDuration')

	@property
	def LckRx(self):
		"""This signifies the number of LCK frames received.

		Returns:
			number
		"""
		return self._get_attribute('lckRx')

	@property
	def LckState(self):
		"""This signifies the state of LCK, either Clear or Fault.

		Returns:
			str
		"""
		return self._get_attribute('lckState')

	@property
	def LckTx(self):
		"""This signifies the number of LCK frames transmitted.

		Returns:
			number
		"""
		return self._get_attribute('lckTx')

	@property
	def Ldi(self):
		"""This signifies the state of the LDI bit, either NA or Set.

		Returns:
			str
		"""
		return self._get_attribute('ldi')

	@property
	def LocalPwStatus(self):
		"""This signifies the local PW status.

		Returns:
			str
		"""
		return self._get_attribute('localPwStatus')

	@property
	def OutgoingLabelOuterInner(self):
		"""This signifies the Outgoing Label information.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def RemoteDefectIndication(self):
		"""This Signifies the Defect Indication received in the cc message from remote port if any.

		Returns:
			str
		"""
		return self._get_attribute('remoteDefectIndication')

	@property
	def RemotePwStatus(self):
		"""This signifies the remote PW status.

		Returns:
			str
		"""
		return self._get_attribute('remotePwStatus')

	@property
	def Role(self):
		"""This signifies the selection of this option to filter according to the following roles None,Protect and Working.

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def TimeSinceLastAlarm(self):
		"""This signifies the time elapsed since the LSP/PW has recovered from the last fault state.

		Returns:
			str
		"""
		return self._get_attribute('timeSinceLastAlarm')

	@property
	def Type(self):
		"""This signifies the selection of this option to filter according to the following types LSP and PW.

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, AisRx=None, AisState=None, AisTx=None, AlarmTypeAis=None, AlarmTypeLck=None, ApsLocalDataPath=None, ApsLocalFaultPath=None, ApsLocalState=None, ApsRemoteDataPath=None, ApsRemoteFaultPath=None, ApsRemoteRequestState=None, ContinuityCheckLocalState=None, ContinuityCheckRemoteState=None, ContinuityCheckRxInterval=None, ContinuityCheckTxInterval=None, IncomingLabelOuterInner=None, LastAlarmDuration=None, LckRx=None, LckState=None, LckTx=None, Ldi=None, LocalPwStatus=None, OutgoingLabelOuterInner=None, RemoteDefectIndication=None, RemotePwStatus=None, Role=None, TimeSinceLastAlarm=None, Type=None):
		"""Finds and retrieves generalLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve generalLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all generalLearnedInfo data from the server.

		Args:
			AisRx (number): This signifies the number of AIS frames received.
			AisState (str): This signifies the state of AIS, either Clear or Fault.
			AisTx (number): This signifies the number of AIS frames transmitted.
			AlarmTypeAis (str): This signifies the type of the AIS alarm, either ietf or y1731.
			AlarmTypeLck (str): This signifies the type of the LCK alarm, either ietf or y1731.
			ApsLocalDataPath (str(working|protect|na)): This signifies the path of the APS local data.
			ApsLocalFaultPath (str(working|protect|both|none|na)): This signifies the path of the APS local fault.
			ApsLocalState (str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)): This signifies the APS local state information.
			ApsRemoteDataPath (str(protect|na|working)): This signifies the path of the APS remote data.
			ApsRemoteFaultPath (str(na|working|protect|both|none)): This signifies the path of the APS remote fault.
			ApsRemoteRequestState (str(na|apsNoRequest|apsLockoutOfProtection|apsSignalFailOnWorking|apsManualSwitch|apsWaitToRestore|apsDoNotRevert|apsExercise|apsReverseRequest|pscNormal|pscUnavailable|pscProtectingAdmin|pscProtectingFailure|pscWaitToRevert|pscDoNotRevert|apsSignalFailOnProtection|apsForceSwitch)): This signifies the APS remote request state information.
			ContinuityCheckLocalState (str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)): This signifies the status of the Continuity Check Local State.
			ContinuityCheckRemoteState (str(na|bfdDown|bfdInit|bfdUp|y1731Down|y1731Init|y1731Up)): This signifies the status of the Continuity Check Remote State.
			ContinuityCheckRxInterval (number): This Signifies the CC Rx Interval configured on the source side.
			ContinuityCheckTxInterval (number): This Signifies the Negotiated CC Tx Interval on the source side.
			IncomingLabelOuterInner (str): This signifies the incoming label information.
			LastAlarmDuration (str): This signifies the duration for how long the LSP/PW was in fault state.
			LckRx (number): This signifies the number of LCK frames received.
			LckState (str): This signifies the state of LCK, either Clear or Fault.
			LckTx (number): This signifies the number of LCK frames transmitted.
			Ldi (str): This signifies the state of the LDI bit, either NA or Set.
			LocalPwStatus (str): This signifies the local PW status.
			OutgoingLabelOuterInner (str): This signifies the Outgoing Label information.
			RemoteDefectIndication (str): This Signifies the Defect Indication received in the cc message from remote port if any.
			RemotePwStatus (str): This signifies the remote PW status.
			Role (str): This signifies the selection of this option to filter according to the following roles None,Protect and Working.
			TimeSinceLastAlarm (str): This signifies the time elapsed since the LSP/PW has recovered from the last fault state.
			Type (str): This signifies the selection of this option to filter according to the following types LSP and PW.

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

		This signifies the record added for trigger settings.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=generalLearnedInfo)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
