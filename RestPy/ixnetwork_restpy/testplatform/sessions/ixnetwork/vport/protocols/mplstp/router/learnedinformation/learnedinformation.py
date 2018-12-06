
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


class LearnedInformation(Base):
	"""The LearnedInformation class encapsulates a required learnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedInformation'

	def __init__(self, parent):
		super(LearnedInformation, self).__init__(parent)

	@property
	def DmLearnedInfo(self):
		"""An instance of the DmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.dmlearnedinfo.dmlearnedinfo.DmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.dmlearnedinfo.dmlearnedinfo import DmLearnedInfo
		return DmLearnedInfo(self)

	@property
	def GeneralLearnedInfo(self):
		"""An instance of the GeneralLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.generallearnedinfo.generallearnedinfo.GeneralLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.generallearnedinfo.generallearnedinfo import GeneralLearnedInfo
		return GeneralLearnedInfo(self)

	@property
	def LmLearnedInfo(self):
		"""An instance of the LmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.lmlearnedinfo.lmlearnedinfo.LmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.lmlearnedinfo.lmlearnedinfo import LmLearnedInfo
		return LmLearnedInfo(self)

	@property
	def PingLearnedInfo(self):
		"""An instance of the PingLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.pinglearnedinfo.pinglearnedinfo.PingLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.pinglearnedinfo.pinglearnedinfo import PingLearnedInfo
		return PingLearnedInfo(self)

	@property
	def TraceRouteLearnedInfo(self):
		"""An instance of the TraceRouteLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.traceroutelearnedinfo.traceroutelearnedinfo.TraceRouteLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.learnedinformation.traceroutelearnedinfo.traceroutelearnedinfo import TraceRouteLearnedInfo
		return TraceRouteLearnedInfo(self)

	@property
	def AlarmTrigger(self):
		"""

		Returns:
			str(clear|start)
		"""
		return self._get_attribute('alarmTrigger')
	@AlarmTrigger.setter
	def AlarmTrigger(self, value):
		self._set_attribute('alarmTrigger', value)

	@property
	def AlarmType(self):
		"""

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('alarmType')
	@AlarmType.setter
	def AlarmType(self, value):
		self._set_attribute('alarmType', value)

	@property
	def ApsTriggerType(self):
		"""

		Returns:
			str(clear|forcedSwitch|manualSwitchToProtect|manualSwitchToWorking|lockout|exercise|freeze)
		"""
		return self._get_attribute('apsTriggerType')
	@ApsTriggerType.setter
	def ApsTriggerType(self, value):
		self._set_attribute('apsTriggerType', value)

	@property
	def CccvPauseTriggerOption(self):
		"""

		Returns:
			str(tx|rx|txRx)
		"""
		return self._get_attribute('cccvPauseTriggerOption')
	@CccvPauseTriggerOption.setter
	def CccvPauseTriggerOption(self, value):
		self._set_attribute('cccvPauseTriggerOption', value)

	@property
	def CccvResumeTriggerOption(self):
		"""

		Returns:
			str(tx|rx|txRx)
		"""
		return self._get_attribute('cccvResumeTriggerOption')
	@CccvResumeTriggerOption.setter
	def CccvResumeTriggerOption(self, value):
		self._set_attribute('cccvResumeTriggerOption', value)

	@property
	def ChangeSessionParameters(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('changeSessionParameters')
	@ChangeSessionParameters.setter
	def ChangeSessionParameters(self, value):
		self._set_attribute('changeSessionParameters', value)

	@property
	def ClearMisconnectivityDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('clearMisconnectivityDefect')
	@ClearMisconnectivityDefect.setter
	def ClearMisconnectivityDefect(self, value):
		self._set_attribute('clearMisconnectivityDefect', value)

	@property
	def CounterType(self):
		"""

		Returns:
			str(32Bit|64Bit)
		"""
		return self._get_attribute('counterType')
	@CounterType.setter
	def CounterType(self, value):
		self._set_attribute('counterType', value)

	@property
	def DmInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmInterval')
	@DmInterval.setter
	def DmInterval(self, value):
		self._set_attribute('dmInterval', value)

	@property
	def DmIterations(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmIterations')
	@DmIterations.setter
	def DmIterations(self, value):
		self._set_attribute('dmIterations', value)

	@property
	def DmMode(self):
		"""

		Returns:
			str(noResponseExpected|responseExpected)
		"""
		return self._get_attribute('dmMode')
	@DmMode.setter
	def DmMode(self, value):
		self._set_attribute('dmMode', value)

	@property
	def DmPadLen(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmPadLen')
	@DmPadLen.setter
	def DmPadLen(self, value):
		self._set_attribute('dmPadLen', value)

	@property
	def DmRequestPaddedReply(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('dmRequestPaddedReply')
	@DmRequestPaddedReply.setter
	def DmRequestPaddedReply(self, value):
		self._set_attribute('dmRequestPaddedReply', value)

	@property
	def DmTimeFormat(self):
		"""

		Returns:
			str(ieee|ntp)
		"""
		return self._get_attribute('dmTimeFormat')
	@DmTimeFormat.setter
	def DmTimeFormat(self, value):
		self._set_attribute('dmTimeFormat', value)

	@property
	def DmTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmTrafficClass')
	@DmTrafficClass.setter
	def DmTrafficClass(self, value):
		self._set_attribute('dmTrafficClass', value)

	@property
	def DmType(self):
		"""

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('dmType')
	@DmType.setter
	def DmType(self, value):
		self._set_attribute('dmType', value)

	@property
	def EnableAlarm(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAlarm')
	@EnableAlarm.setter
	def EnableAlarm(self, value):
		self._set_attribute('enableAlarm', value)

	@property
	def EnableAlarmAis(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAlarmAis')
	@EnableAlarmAis.setter
	def EnableAlarmAis(self, value):
		self._set_attribute('enableAlarmAis', value)

	@property
	def EnableAlarmFastClear(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAlarmFastClear')
	@EnableAlarmFastClear.setter
	def EnableAlarmFastClear(self, value):
		self._set_attribute('enableAlarmFastClear', value)

	@property
	def EnableAlarmLck(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAlarmLck')
	@EnableAlarmLck.setter
	def EnableAlarmLck(self, value):
		self._set_attribute('enableAlarmLck', value)

	@property
	def EnableAlarmSetLdi(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAlarmSetLdi')
	@EnableAlarmSetLdi.setter
	def EnableAlarmSetLdi(self, value):
		self._set_attribute('enableAlarmSetLdi', value)

	@property
	def EnableApsTrigger(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableApsTrigger')
	@EnableApsTrigger.setter
	def EnableApsTrigger(self, value):
		self._set_attribute('enableApsTrigger', value)

	@property
	def EnableCccvPause(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCccvPause')
	@EnableCccvPause.setter
	def EnableCccvPause(self, value):
		self._set_attribute('enableCccvPause', value)

	@property
	def EnableCccvResume(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCccvResume')
	@EnableCccvResume.setter
	def EnableCccvResume(self, value):
		self._set_attribute('enableCccvResume', value)

	@property
	def EnableDmTrigger(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDmTrigger')
	@EnableDmTrigger.setter
	def EnableDmTrigger(self, value):
		self._set_attribute('enableDmTrigger', value)

	@property
	def EnableLmTrigger(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLmTrigger')
	@EnableLmTrigger.setter
	def EnableLmTrigger(self, value):
		self._set_attribute('enableLmTrigger', value)

	@property
	def EnableLspPing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPing')
	@EnableLspPing.setter
	def EnableLspPing(self, value):
		self._set_attribute('enableLspPing', value)

	@property
	def EnableLspPingFecStackValidation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPingFecStackValidation')
	@EnableLspPingFecStackValidation.setter
	def EnableLspPingFecStackValidation(self, value):
		self._set_attribute('enableLspPingFecStackValidation', value)

	@property
	def EnableLspPingValidateReversePath(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPingValidateReversePath')
	@EnableLspPingValidateReversePath.setter
	def EnableLspPingValidateReversePath(self, value):
		self._set_attribute('enableLspPingValidateReversePath', value)

	@property
	def EnableLspTraceRoute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspTraceRoute')
	@EnableLspTraceRoute.setter
	def EnableLspTraceRoute(self, value):
		self._set_attribute('enableLspTraceRoute', value)

	@property
	def EnableLspTraceRouteFecStackValidation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspTraceRouteFecStackValidation')
	@EnableLspTraceRouteFecStackValidation.setter
	def EnableLspTraceRouteFecStackValidation(self, value):
		self._set_attribute('enableLspTraceRouteFecStackValidation', value)

	@property
	def EnablePwStatusClear(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePwStatusClear')
	@EnablePwStatusClear.setter
	def EnablePwStatusClear(self, value):
		self._set_attribute('enablePwStatusClear', value)

	@property
	def EnablePwStatusFault(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePwStatusFault')
	@EnablePwStatusFault.setter
	def EnablePwStatusFault(self, value):
		self._set_attribute('enablePwStatusFault', value)

	@property
	def IsDmLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDmLearnedInformationRefreshed')

	@property
	def IsGeneralLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isGeneralLearnedInformationRefreshed')

	@property
	def IsLmLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLmLearnedInformationRefreshed')

	@property
	def IsPingLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPingLearnedInformationRefreshed')

	@property
	def IsTraceRouteLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isTraceRouteLearnedInformationRefreshed')

	@property
	def LastDmResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lastDmResponseTimeout')
	@LastDmResponseTimeout.setter
	def LastDmResponseTimeout(self, value):
		self._set_attribute('lastDmResponseTimeout', value)

	@property
	def LastLmResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lastLmResponseTimeout')
	@LastLmResponseTimeout.setter
	def LastLmResponseTimeout(self, value):
		self._set_attribute('lastLmResponseTimeout', value)

	@property
	def LmInitialRxValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmInitialRxValue')
	@LmInitialRxValue.setter
	def LmInitialRxValue(self, value):
		self._set_attribute('lmInitialRxValue', value)

	@property
	def LmInitialTxValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmInitialTxValue')
	@LmInitialTxValue.setter
	def LmInitialTxValue(self, value):
		self._set_attribute('lmInitialTxValue', value)

	@property
	def LmInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmInterval')
	@LmInterval.setter
	def LmInterval(self, value):
		self._set_attribute('lmInterval', value)

	@property
	def LmIterations(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmIterations')
	@LmIterations.setter
	def LmIterations(self, value):
		self._set_attribute('lmIterations', value)

	@property
	def LmMode(self):
		"""

		Returns:
			str(responseExpected|noResponseExpected)
		"""
		return self._get_attribute('lmMode')
	@LmMode.setter
	def LmMode(self, value):
		self._set_attribute('lmMode', value)

	@property
	def LmRxStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmRxStep')
	@LmRxStep.setter
	def LmRxStep(self, value):
		self._set_attribute('lmRxStep', value)

	@property
	def LmTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmTrafficClass')
	@LmTrafficClass.setter
	def LmTrafficClass(self, value):
		self._set_attribute('lmTrafficClass', value)

	@property
	def LmTxStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmTxStep')
	@LmTxStep.setter
	def LmTxStep(self, value):
		self._set_attribute('lmTxStep', value)

	@property
	def LmType(self):
		"""

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('lmType')
	@LmType.setter
	def LmType(self, value):
		self._set_attribute('lmType', value)

	@property
	def LspPingEncapsulationType(self):
		"""

		Returns:
			str(GAch|UDP over IP over GAch)
		"""
		return self._get_attribute('lspPingEncapsulationType')
	@LspPingEncapsulationType.setter
	def LspPingEncapsulationType(self, value):
		self._set_attribute('lspPingEncapsulationType', value)

	@property
	def LspPingResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspPingResponseTimeout')
	@LspPingResponseTimeout.setter
	def LspPingResponseTimeout(self, value):
		self._set_attribute('lspPingResponseTimeout', value)

	@property
	def LspPingTtlValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspPingTtlValue')
	@LspPingTtlValue.setter
	def LspPingTtlValue(self, value):
		self._set_attribute('lspPingTtlValue', value)

	@property
	def LspTraceRouteEncapsulationType(self):
		"""

		Returns:
			str(GAch|UDP over IP over GAch)
		"""
		return self._get_attribute('lspTraceRouteEncapsulationType')
	@LspTraceRouteEncapsulationType.setter
	def LspTraceRouteEncapsulationType(self, value):
		self._set_attribute('lspTraceRouteEncapsulationType', value)

	@property
	def LspTraceRouteResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspTraceRouteResponseTimeout')
	@LspTraceRouteResponseTimeout.setter
	def LspTraceRouteResponseTimeout(self, value):
		self._set_attribute('lspTraceRouteResponseTimeout', value)

	@property
	def LspTraceRouteTtlLimit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspTraceRouteTtlLimit')
	@LspTraceRouteTtlLimit.setter
	def LspTraceRouteTtlLimit(self, value):
		self._set_attribute('lspTraceRouteTtlLimit', value)

	@property
	def MinRxInterval(self):
		"""

		Returns:
			str(10|100|1000|10000|3.33|60000|600000)
		"""
		return self._get_attribute('minRxInterval')
	@MinRxInterval.setter
	def MinRxInterval(self, value):
		self._set_attribute('minRxInterval', value)

	@property
	def MinTxInterval(self):
		"""

		Returns:
			str(10|100|1000|10000|3.33|60000|600000)
		"""
		return self._get_attribute('minTxInterval')
	@MinTxInterval.setter
	def MinTxInterval(self, value):
		self._set_attribute('minTxInterval', value)

	@property
	def MisconnectivityDefect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('misconnectivityDefect')
	@MisconnectivityDefect.setter
	def MisconnectivityDefect(self, value):
		self._set_attribute('misconnectivityDefect', value)

	@property
	def MisconnectivityDefectOption(self):
		"""

		Returns:
			str(unexpectedMepId|unexpectedYourDiscriminator)
		"""
		return self._get_attribute('misconnectivityDefectOption')
	@MisconnectivityDefectOption.setter
	def MisconnectivityDefectOption(self, value):
		self._set_attribute('misconnectivityDefectOption', value)

	@property
	def OnDemandCvDownstreamAddressType(self):
		"""

		Returns:
			str(ipv4Numbered|ipv4Unnumbered|nonIp)
		"""
		return self._get_attribute('onDemandCvDownstreamAddressType')
	@OnDemandCvDownstreamAddressType.setter
	def OnDemandCvDownstreamAddressType(self, value):
		self._set_attribute('onDemandCvDownstreamAddressType', value)

	@property
	def OnDemandCvDownstreamIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('onDemandCvDownstreamIpAddress')
	@OnDemandCvDownstreamIpAddress.setter
	def OnDemandCvDownstreamIpAddress(self, value):
		self._set_attribute('onDemandCvDownstreamIpAddress', value)

	@property
	def OnDemandCvDsIflag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvDsIflag')
	@OnDemandCvDsIflag.setter
	def OnDemandCvDsIflag(self, value):
		self._set_attribute('onDemandCvDsIflag', value)

	@property
	def OnDemandCvDsNflag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvDsNflag')
	@OnDemandCvDsNflag.setter
	def OnDemandCvDsNflag(self, value):
		self._set_attribute('onDemandCvDsNflag', value)

	@property
	def OnDemandCvEgressIfNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvEgressIfNumber')
	@OnDemandCvEgressIfNumber.setter
	def OnDemandCvEgressIfNumber(self, value):
		self._set_attribute('onDemandCvEgressIfNumber', value)

	@property
	def OnDemandCvIncludeDestinationIdentifierTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvIncludeDestinationIdentifierTlv')
	@OnDemandCvIncludeDestinationIdentifierTlv.setter
	def OnDemandCvIncludeDestinationIdentifierTlv(self, value):
		self._set_attribute('onDemandCvIncludeDestinationIdentifierTlv', value)

	@property
	def OnDemandCvIncludeDetailedDownstreamMappingTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvIncludeDetailedDownstreamMappingTlv')
	@OnDemandCvIncludeDetailedDownstreamMappingTlv.setter
	def OnDemandCvIncludeDetailedDownstreamMappingTlv(self, value):
		self._set_attribute('onDemandCvIncludeDetailedDownstreamMappingTlv', value)

	@property
	def OnDemandCvIncludeDownstreamMappingTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvIncludeDownstreamMappingTlv')
	@OnDemandCvIncludeDownstreamMappingTlv.setter
	def OnDemandCvIncludeDownstreamMappingTlv(self, value):
		self._set_attribute('onDemandCvIncludeDownstreamMappingTlv', value)

	@property
	def OnDemandCvIncludePadTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvIncludePadTlv')
	@OnDemandCvIncludePadTlv.setter
	def OnDemandCvIncludePadTlv(self, value):
		self._set_attribute('onDemandCvIncludePadTlv', value)

	@property
	def OnDemandCvIncludeReplyTosByteTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvIncludeReplyTosByteTlv')
	@OnDemandCvIncludeReplyTosByteTlv.setter
	def OnDemandCvIncludeReplyTosByteTlv(self, value):
		self._set_attribute('onDemandCvIncludeReplyTosByteTlv', value)

	@property
	def OnDemandCvIncludeSourceIdentifierTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('onDemandCvIncludeSourceIdentifierTlv')
	@OnDemandCvIncludeSourceIdentifierTlv.setter
	def OnDemandCvIncludeSourceIdentifierTlv(self, value):
		self._set_attribute('onDemandCvIncludeSourceIdentifierTlv', value)

	@property
	def OnDemandCvIngressIfNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvIngressIfNumber')
	@OnDemandCvIngressIfNumber.setter
	def OnDemandCvIngressIfNumber(self, value):
		self._set_attribute('onDemandCvIngressIfNumber', value)

	@property
	def OnDemandCvNumberedDownstreamInterfaceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('onDemandCvNumberedDownstreamInterfaceAddress')
	@OnDemandCvNumberedDownstreamInterfaceAddress.setter
	def OnDemandCvNumberedDownstreamInterfaceAddress(self, value):
		self._set_attribute('onDemandCvNumberedDownstreamInterfaceAddress', value)

	@property
	def OnDemandCvPadTlvFirstOctet(self):
		"""

		Returns:
			str(drop|copy)
		"""
		return self._get_attribute('onDemandCvPadTlvFirstOctet')
	@OnDemandCvPadTlvFirstOctet.setter
	def OnDemandCvPadTlvFirstOctet(self, value):
		self._set_attribute('onDemandCvPadTlvFirstOctet', value)

	@property
	def OnDemandCvPadTlvLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvPadTlvLength')
	@OnDemandCvPadTlvLength.setter
	def OnDemandCvPadTlvLength(self, value):
		self._set_attribute('onDemandCvPadTlvLength', value)

	@property
	def OnDemandCvTosByte(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvTosByte')
	@OnDemandCvTosByte.setter
	def OnDemandCvTosByte(self, value):
		self._set_attribute('onDemandCvTosByte', value)

	@property
	def OnDemandCvUnnumberedDownstreamInterfaceAddress(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvUnnumberedDownstreamInterfaceAddress')
	@OnDemandCvUnnumberedDownstreamInterfaceAddress.setter
	def OnDemandCvUnnumberedDownstreamInterfaceAddress(self, value):
		self._set_attribute('onDemandCvUnnumberedDownstreamInterfaceAddress', value)

	@property
	def Periodicity(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('periodicity')
	@Periodicity.setter
	def Periodicity(self, value):
		self._set_attribute('periodicity', value)

	@property
	def PwStatusClearLabelTtl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusClearLabelTtl')
	@PwStatusClearLabelTtl.setter
	def PwStatusClearLabelTtl(self, value):
		self._set_attribute('pwStatusClearLabelTtl', value)

	@property
	def PwStatusClearTransmitInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusClearTransmitInterval')
	@PwStatusClearTransmitInterval.setter
	def PwStatusClearTransmitInterval(self, value):
		self._set_attribute('pwStatusClearTransmitInterval', value)

	@property
	def PwStatusCode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusCode')
	@PwStatusCode.setter
	def PwStatusCode(self, value):
		self._set_attribute('pwStatusCode', value)

	@property
	def PwStatusFaultLabelTtl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusFaultLabelTtl')
	@PwStatusFaultLabelTtl.setter
	def PwStatusFaultLabelTtl(self, value):
		self._set_attribute('pwStatusFaultLabelTtl', value)

	@property
	def PwStatusFaultTransmitInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusFaultTransmitInterval')
	@PwStatusFaultTransmitInterval.setter
	def PwStatusFaultTransmitInterval(self, value):
		self._set_attribute('pwStatusFaultTransmitInterval', value)

	def ClearRecordsForTrigger(self):
		"""Executes the clearRecordsForTrigger operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=learnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearRecordsForTrigger', payload=locals(), response_object=None)

	def RefreshLearnedInformation(self):
		"""Executes the refreshLearnedInformation operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=learnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInformation', payload=locals(), response_object=None)

	def Trigger(self):
		"""Executes the trigger operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=learnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Trigger', payload=locals(), response_object=None)
