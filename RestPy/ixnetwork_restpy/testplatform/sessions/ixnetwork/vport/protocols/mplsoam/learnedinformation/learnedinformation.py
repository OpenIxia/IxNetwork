
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
	"""The LearnedInformation class encapsulates a system managed learnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedInformation'

	def __init__(self, parent):
		super(LearnedInformation, self).__init__(parent)

	@property
	def GeneralLearnedInfo(self):
		"""An instance of the GeneralLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.generallearnedinfo.generallearnedinfo.GeneralLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.generallearnedinfo.generallearnedinfo import GeneralLearnedInfo
		return GeneralLearnedInfo(self)

	@property
	def TriggeredPingLearnedInfo(self):
		"""An instance of the TriggeredPingLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.triggeredpinglearnedinfo.triggeredpinglearnedinfo.TriggeredPingLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.triggeredpinglearnedinfo.triggeredpinglearnedinfo import TriggeredPingLearnedInfo
		return TriggeredPingLearnedInfo(self)

	@property
	def TriggeredTracerouteLearnedInfo(self):
		"""An instance of the TriggeredTracerouteLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.triggeredtraceroutelearnedinfo.triggeredtraceroutelearnedinfo.TriggeredTracerouteLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.triggeredtraceroutelearnedinfo.triggeredtraceroutelearnedinfo import TriggeredTracerouteLearnedInfo
		return TriggeredTracerouteLearnedInfo(self)

	@property
	def DestinationAddressIpv4(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationAddressIpv4')
	@DestinationAddressIpv4.setter
	def DestinationAddressIpv4(self, value):
		self._set_attribute('destinationAddressIpv4', value)

	@property
	def DownstreamAddressType(self):
		"""

		Returns:
			str(ipv4Numbered|ipv4UnNumbered)
		"""
		return self._get_attribute('downstreamAddressType')
	@DownstreamAddressType.setter
	def DownstreamAddressType(self, value):
		self._set_attribute('downstreamAddressType', value)

	@property
	def DownstreamInterfaceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downstreamInterfaceAddress')
	@DownstreamInterfaceAddress.setter
	def DownstreamInterfaceAddress(self, value):
		self._set_attribute('downstreamInterfaceAddress', value)

	@property
	def DownstreamIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('downstreamIpAddress')
	@DownstreamIpAddress.setter
	def DownstreamIpAddress(self, value):
		self._set_attribute('downstreamIpAddress', value)

	@property
	def EchoResponseTimeoutMs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('echoResponseTimeoutMs')
	@EchoResponseTimeoutMs.setter
	def EchoResponseTimeoutMs(self, value):
		self._set_attribute('echoResponseTimeoutMs', value)

	@property
	def EnableAdvance(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvance')
	@EnableAdvance.setter
	def EnableAdvance(self, value):
		self._set_attribute('enableAdvance', value)

	@property
	def EnableDsiFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDsiFlag')
	@EnableDsiFlag.setter
	def EnableDsiFlag(self, value):
		self._set_attribute('enableDsiFlag', value)

	@property
	def EnableDsnFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDsnFlag')
	@EnableDsnFlag.setter
	def EnableDsnFlag(self, value):
		self._set_attribute('enableDsnFlag', value)

	@property
	def EnableFecValidation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFecValidation')
	@EnableFecValidation.setter
	def EnableFecValidation(self, value):
		self._set_attribute('enableFecValidation', value)

	@property
	def EnableIncludeDownstreamMappingTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeDownstreamMappingTlv')
	@EnableIncludeDownstreamMappingTlv.setter
	def EnableIncludeDownstreamMappingTlv(self, value):
		self._set_attribute('enableIncludeDownstreamMappingTlv', value)

	@property
	def EnableIncludePadTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludePadTlv')
	@EnableIncludePadTlv.setter
	def EnableIncludePadTlv(self, value):
		self._set_attribute('enableIncludePadTlv', value)

	@property
	def EnableIncludeVendorEnterpriseNumberTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncludeVendorEnterpriseNumberTlv')
	@EnableIncludeVendorEnterpriseNumberTlv.setter
	def EnableIncludeVendorEnterpriseNumberTlv(self, value):
		self._set_attribute('enableIncludeVendorEnterpriseNumberTlv', value)

	@property
	def EnablePauseResumeBfdPduTrigger(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePauseResumeBfdPduTrigger')
	@EnablePauseResumeBfdPduTrigger.setter
	def EnablePauseResumeBfdPduTrigger(self, value):
		self._set_attribute('enablePauseResumeBfdPduTrigger', value)

	@property
	def EnablePauseResumeReplyTrigger(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePauseResumeReplyTrigger')
	@EnablePauseResumeReplyTrigger.setter
	def EnablePauseResumeReplyTrigger(self, value):
		self._set_attribute('enablePauseResumeReplyTrigger', value)

	@property
	def EnableSendTriggeredPing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggeredPing')
	@EnableSendTriggeredPing.setter
	def EnableSendTriggeredPing(self, value):
		self._set_attribute('enableSendTriggeredPing', value)

	@property
	def EnableSendTriggeredTraceroute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggeredTraceroute')
	@EnableSendTriggeredTraceroute.setter
	def EnableSendTriggeredTraceroute(self, value):
		self._set_attribute('enableSendTriggeredTraceroute', value)

	@property
	def EnableSetResetEchoReplyCodeTrigger(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSetResetEchoReplyCodeTrigger')
	@EnableSetResetEchoReplyCodeTrigger.setter
	def EnableSetResetEchoReplyCodeTrigger(self, value):
		self._set_attribute('enableSetResetEchoReplyCodeTrigger', value)

	@property
	def IsGeneralLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isGeneralLearnedInformationRefreshed')

	@property
	def IsTriggeredPingLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isTriggeredPingLearnedInformationRefreshed')

	@property
	def IsTriggeredTraceRouteLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isTriggeredTraceRouteLearnedInformationRefreshed')

	@property
	def PadTlvFirstOctetOptions(self):
		"""

		Returns:
			str(dropPadTlvFromReply|copyPadTlvToReply)
		"""
		return self._get_attribute('padTlvFirstOctetOptions')
	@PadTlvFirstOctetOptions.setter
	def PadTlvFirstOctetOptions(self, value):
		self._set_attribute('padTlvFirstOctetOptions', value)

	@property
	def PadTlvLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('padTlvLength')
	@PadTlvLength.setter
	def PadTlvLength(self, value):
		self._set_attribute('padTlvLength', value)

	@property
	def PauseResumeBfdPduTriggerOption(self):
		"""

		Returns:
			str(pause|resume)
		"""
		return self._get_attribute('pauseResumeBfdPduTriggerOption')
	@PauseResumeBfdPduTriggerOption.setter
	def PauseResumeBfdPduTriggerOption(self, value):
		self._set_attribute('pauseResumeBfdPduTriggerOption', value)

	@property
	def PauseResumeReplyTriggerOption(self):
		"""

		Returns:
			str(pause|resume)
		"""
		return self._get_attribute('pauseResumeReplyTriggerOption')
	@PauseResumeReplyTriggerOption.setter
	def PauseResumeReplyTriggerOption(self, value):
		self._set_attribute('pauseResumeReplyTriggerOption', value)

	@property
	def ReplyMode(self):
		"""

		Returns:
			str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)
		"""
		return self._get_attribute('replyMode')
	@ReplyMode.setter
	def ReplyMode(self, value):
		self._set_attribute('replyMode', value)

	@property
	def ReturnCodeOption(self):
		"""

		Returns:
			str(noReturnCode|malformedEchoRequestReceived|oneOrMoreOfTheTlvsWasNotUnderstood|replyingRouterIsAnEgressForTheFecAtStackDepthRsc|replyingRouterHasNoMappingForTheFecAtStackDepthRsc|downstreamMappingMismatch|upstreamInterfaceIndexUnknown|lspPingReserved|labelSwitchedAtStackDepthRsc|labelSwitchedButNoMplsForwardingAtStackDepthRsc|mappingForThisFecIsNotTheGivenLabelAtStackDepthRsc|noLabelEntryAtStackDepthRsc|protocolNotAssociatedWithInterfaceatFecStackDepthRsc|prematureTerminationOfPingDueToLabelStackShrinkingToSingleLabel)
		"""
		return self._get_attribute('returnCodeOption')
	@ReturnCodeOption.setter
	def ReturnCodeOption(self, value):
		self._set_attribute('returnCodeOption', value)

	@property
	def ReturnSubCode(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('returnSubCode')
	@ReturnSubCode.setter
	def ReturnSubCode(self, value):
		self._set_attribute('returnSubCode', value)

	@property
	def TriggerOptions(self):
		"""

		Returns:
			str(tx|rx|txRx)
		"""
		return self._get_attribute('triggerOptions')
	@TriggerOptions.setter
	def TriggerOptions(self, value):
		self._set_attribute('triggerOptions', value)

	@property
	def TriggerType(self):
		"""

		Returns:
			str(resetToNormalReply|forceReplyCode)
		"""
		return self._get_attribute('triggerType')
	@TriggerType.setter
	def TriggerType(self, value):
		self._set_attribute('triggerType', value)

	@property
	def TtlLimit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ttlLimit')
	@TtlLimit.setter
	def TtlLimit(self, value):
		self._set_attribute('ttlLimit', value)

	@property
	def VendorEnterpriseNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vendorEnterpriseNumber')
	@VendorEnterpriseNumber.setter
	def VendorEnterpriseNumber(self, value):
		self._set_attribute('vendorEnterpriseNumber', value)

	def find(self, DestinationAddressIpv4=None, DownstreamAddressType=None, DownstreamInterfaceAddress=None, DownstreamIpAddress=None, EchoResponseTimeoutMs=None, EnableAdvance=None, EnableDsiFlag=None, EnableDsnFlag=None, EnableFecValidation=None, EnableIncludeDownstreamMappingTlv=None, EnableIncludePadTlv=None, EnableIncludeVendorEnterpriseNumberTlv=None, EnablePauseResumeBfdPduTrigger=None, EnablePauseResumeReplyTrigger=None, EnableSendTriggeredPing=None, EnableSendTriggeredTraceroute=None, EnableSetResetEchoReplyCodeTrigger=None, IsGeneralLearnedInformationRefreshed=None, IsTriggeredPingLearnedInformationRefreshed=None, IsTriggeredTraceRouteLearnedInformationRefreshed=None, PadTlvFirstOctetOptions=None, PadTlvLength=None, PauseResumeBfdPduTriggerOption=None, PauseResumeReplyTriggerOption=None, ReplyMode=None, ReturnCodeOption=None, ReturnSubCode=None, TriggerOptions=None, TriggerType=None, TtlLimit=None, VendorEnterpriseNumber=None):
		"""Finds and retrieves learnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all learnedInformation data from the server.

		Args:
			DestinationAddressIpv4 (str): 
			DownstreamAddressType (str(ipv4Numbered|ipv4UnNumbered)): 
			DownstreamInterfaceAddress (str): 
			DownstreamIpAddress (str): 
			EchoResponseTimeoutMs (number): 
			EnableAdvance (bool): 
			EnableDsiFlag (bool): 
			EnableDsnFlag (bool): 
			EnableFecValidation (bool): 
			EnableIncludeDownstreamMappingTlv (bool): 
			EnableIncludePadTlv (bool): 
			EnableIncludeVendorEnterpriseNumberTlv (bool): 
			EnablePauseResumeBfdPduTrigger (bool): 
			EnablePauseResumeReplyTrigger (bool): 
			EnableSendTriggeredPing (bool): 
			EnableSendTriggeredTraceroute (bool): 
			EnableSetResetEchoReplyCodeTrigger (bool): 
			IsGeneralLearnedInformationRefreshed (bool): 
			IsTriggeredPingLearnedInformationRefreshed (bool): 
			IsTriggeredTraceRouteLearnedInformationRefreshed (bool): 
			PadTlvFirstOctetOptions (str(dropPadTlvFromReply|copyPadTlvToReply)): 
			PadTlvLength (number): 
			PauseResumeBfdPduTriggerOption (str(pause|resume)): 
			PauseResumeReplyTriggerOption (str(pause|resume)): 
			ReplyMode (str(doNotReply|replyViaIpv4Ipv6UdpPacket|replyViaIpv4Ipv6UdpPacketWithRouterAlert|replyViaApplicationLevelControlChannel)): 
			ReturnCodeOption (str(noReturnCode|malformedEchoRequestReceived|oneOrMoreOfTheTlvsWasNotUnderstood|replyingRouterIsAnEgressForTheFecAtStackDepthRsc|replyingRouterHasNoMappingForTheFecAtStackDepthRsc|downstreamMappingMismatch|upstreamInterfaceIndexUnknown|lspPingReserved|labelSwitchedAtStackDepthRsc|labelSwitchedButNoMplsForwardingAtStackDepthRsc|mappingForThisFecIsNotTheGivenLabelAtStackDepthRsc|noLabelEntryAtStackDepthRsc|protocolNotAssociatedWithInterfaceatFecStackDepthRsc|prematureTerminationOfPingDueToLabelStackShrinkingToSingleLabel)): 
			ReturnSubCode (number): 
			TriggerOptions (str(tx|rx|txRx)): 
			TriggerType (str(resetToNormalReply|forceReplyCode)): 
			TtlLimit (number): 
			VendorEnterpriseNumber (number): 

		Returns:
			self: This instance with matching learnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

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
			number: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Trigger', payload=locals(), response_object=None)
