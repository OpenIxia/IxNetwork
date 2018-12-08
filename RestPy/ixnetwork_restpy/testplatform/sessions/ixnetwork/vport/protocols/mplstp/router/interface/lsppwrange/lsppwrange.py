
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


class LspPwRange(Base):
	"""The LspPwRange class encapsulates a user managed lspPwRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LspPwRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'lspPwRange'

	def __init__(self, parent):
		super(LspPwRange, self).__init__(parent)

	@property
	def AlarmTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('alarmTrafficClass')
	@AlarmTrafficClass.setter
	def AlarmTrafficClass(self, value):
		self._set_attribute('alarmTrafficClass', value)

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
	def ApsTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('apsTrafficClass')
	@ApsTrafficClass.setter
	def ApsTrafficClass(self, value):
		self._set_attribute('apsTrafficClass', value)

	@property
	def ApsType(self):
		"""

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('apsType')
	@ApsType.setter
	def ApsType(self, value):
		self._set_attribute('apsType', value)

	@property
	def CccvInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cccvInterval')
	@CccvInterval.setter
	def CccvInterval(self, value):
		self._set_attribute('cccvInterval', value)

	@property
	def CccvTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cccvTrafficClass')
	@CccvTrafficClass.setter
	def CccvTrafficClass(self, value):
		self._set_attribute('cccvTrafficClass', value)

	@property
	def CccvType(self):
		"""

		Returns:
			str(bfdCc|bfdCccv|y1731|none)
		"""
		return self._get_attribute('cccvType')
	@CccvType.setter
	def CccvType(self, value):
		self._set_attribute('cccvType', value)

	@property
	def Description(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DestAcId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destAcId')
	@DestAcId.setter
	def DestAcId(self, value):
		self._set_attribute('destAcId', value)

	@property
	def DestAcIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destAcIdStep')
	@DestAcIdStep.setter
	def DestAcIdStep(self, value):
		self._set_attribute('destAcIdStep', value)

	@property
	def DestGlobalId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destGlobalId')
	@DestGlobalId.setter
	def DestGlobalId(self, value):
		self._set_attribute('destGlobalId', value)

	@property
	def DestLspNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destLspNumber')
	@DestLspNumber.setter
	def DestLspNumber(self, value):
		self._set_attribute('destLspNumber', value)

	@property
	def DestLspNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destLspNumberStep')
	@DestLspNumberStep.setter
	def DestLspNumberStep(self, value):
		self._set_attribute('destLspNumberStep', value)

	@property
	def DestMepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destMepId')
	@DestMepId.setter
	def DestMepId(self, value):
		self._set_attribute('destMepId', value)

	@property
	def DestMepIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destMepIdStep')
	@DestMepIdStep.setter
	def DestMepIdStep(self, value):
		self._set_attribute('destMepIdStep', value)

	@property
	def DestNodeId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destNodeId')
	@DestNodeId.setter
	def DestNodeId(self, value):
		self._set_attribute('destNodeId', value)

	@property
	def DestTunnelNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destTunnelNumber')
	@DestTunnelNumber.setter
	def DestTunnelNumber(self, value):
		self._set_attribute('destTunnelNumber', value)

	@property
	def DestTunnelNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destTunnelNumberStep')
	@DestTunnelNumberStep.setter
	def DestTunnelNumberStep(self, value):
		self._set_attribute('destTunnelNumberStep', value)

	@property
	def DestVplsIdAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAsNumber')
	@DestVplsIdAsNumber.setter
	def DestVplsIdAsNumber(self, value):
		self._set_attribute('destVplsIdAsNumber', value)

	@property
	def DestVplsIdAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAsNumberStep')
	@DestVplsIdAsNumberStep.setter
	def DestVplsIdAsNumberStep(self, value):
		self._set_attribute('destVplsIdAsNumberStep', value)

	@property
	def DestVplsIdAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAssignedNumber')
	@DestVplsIdAssignedNumber.setter
	def DestVplsIdAssignedNumber(self, value):
		self._set_attribute('destVplsIdAssignedNumber', value)

	@property
	def DestVplsIdAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAssignedNumberStep')
	@DestVplsIdAssignedNumberStep.setter
	def DestVplsIdAssignedNumberStep(self, value):
		self._set_attribute('destVplsIdAssignedNumberStep', value)

	@property
	def DestVplsIdIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destVplsIdIpAddress')
	@DestVplsIdIpAddress.setter
	def DestVplsIdIpAddress(self, value):
		self._set_attribute('destVplsIdIpAddress', value)

	@property
	def DestVplsIdIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destVplsIdIpAddressStep')
	@DestVplsIdIpAddressStep.setter
	def DestVplsIdIpAddressStep(self, value):
		self._set_attribute('destVplsIdIpAddressStep', value)

	@property
	def DestVplsIdType(self):
		"""

		Returns:
			str(asNumber|ipAddress|asNumber4Bytes)
		"""
		return self._get_attribute('destVplsIdType')
	@DestVplsIdType.setter
	def DestVplsIdType(self, value):
		self._set_attribute('destVplsIdType', value)

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
	def EnableVlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

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
	def IpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpAddressMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipAddressMask')
	@IpAddressMask.setter
	def IpAddressMask(self, value):
		self._set_attribute('ipAddressMask', value)

	@property
	def IpAddressStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipAddressStep')
	@IpAddressStep.setter
	def IpAddressStep(self, value):
		self._set_attribute('ipAddressStep', value)

	@property
	def IpHostPerLsp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipHostPerLsp')
	@IpHostPerLsp.setter
	def IpHostPerLsp(self, value):
		self._set_attribute('ipHostPerLsp', value)

	@property
	def IpType(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def LmCounterType(self):
		"""

		Returns:
			str(32Bit|64Bit)
		"""
		return self._get_attribute('lmCounterType')
	@LmCounterType.setter
	def LmCounterType(self, value):
		self._set_attribute('lmCounterType', value)

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
	def LspIncomingLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspIncomingLabel')
	@LspIncomingLabel.setter
	def LspIncomingLabel(self, value):
		self._set_attribute('lspIncomingLabel', value)

	@property
	def LspIncomingLabelStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspIncomingLabelStep')
	@LspIncomingLabelStep.setter
	def LspIncomingLabelStep(self, value):
		self._set_attribute('lspIncomingLabelStep', value)

	@property
	def LspOutgoingLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspOutgoingLabel')
	@LspOutgoingLabel.setter
	def LspOutgoingLabel(self, value):
		self._set_attribute('lspOutgoingLabel', value)

	@property
	def LspOutgoingLabelStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspOutgoingLabelStep')
	@LspOutgoingLabelStep.setter
	def LspOutgoingLabelStep(self, value):
		self._set_attribute('lspOutgoingLabelStep', value)

	@property
	def MacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MacPerPw(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('macPerPw')
	@MacPerPw.setter
	def MacPerPw(self, value):
		self._set_attribute('macPerPw', value)

	@property
	def MegIdIntegerStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('megIdIntegerStep')
	@MegIdIntegerStep.setter
	def MegIdIntegerStep(self, value):
		self._set_attribute('megIdIntegerStep', value)

	@property
	def MegIdPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('megIdPrefix')
	@MegIdPrefix.setter
	def MegIdPrefix(self, value):
		self._set_attribute('megIdPrefix', value)

	@property
	def MegLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('megLevel')
	@MegLevel.setter
	def MegLevel(self, value):
		self._set_attribute('megLevel', value)

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
	def MinTxInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minTxInterval')
	@MinTxInterval.setter
	def MinTxInterval(self, value):
		self._set_attribute('minTxInterval', value)

	@property
	def NumberOfLsp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfLsp')
	@NumberOfLsp.setter
	def NumberOfLsp(self, value):
		self._set_attribute('numberOfLsp', value)

	@property
	def NumberOfPwPerLsp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfPwPerLsp')
	@NumberOfPwPerLsp.setter
	def NumberOfPwPerLsp(self, value):
		self._set_attribute('numberOfPwPerLsp', value)

	@property
	def OnDemandCvTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvTrafficClass')
	@OnDemandCvTrafficClass.setter
	def OnDemandCvTrafficClass(self, value):
		self._set_attribute('onDemandCvTrafficClass', value)

	@property
	def PeerLspOrPwRange(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)
		"""
		return self._get_attribute('peerLspOrPwRange')
	@PeerLspOrPwRange.setter
	def PeerLspOrPwRange(self, value):
		self._set_attribute('peerLspOrPwRange', value)

	@property
	def PeerNestedLspPwRange(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)
		"""
		return self._get_attribute('peerNestedLspPwRange')
	@PeerNestedLspPwRange.setter
	def PeerNestedLspPwRange(self, value):
		self._set_attribute('peerNestedLspPwRange', value)

	@property
	def PwIncomingLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwIncomingLabel')
	@PwIncomingLabel.setter
	def PwIncomingLabel(self, value):
		self._set_attribute('pwIncomingLabel', value)

	@property
	def PwIncomingLabelStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwIncomingLabelStep')
	@PwIncomingLabelStep.setter
	def PwIncomingLabelStep(self, value):
		self._set_attribute('pwIncomingLabelStep', value)

	@property
	def PwIncomingLabelStepAcrossLsp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwIncomingLabelStepAcrossLsp')
	@PwIncomingLabelStepAcrossLsp.setter
	def PwIncomingLabelStepAcrossLsp(self, value):
		self._set_attribute('pwIncomingLabelStepAcrossLsp', value)

	@property
	def PwOutgoingLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwOutgoingLabel')
	@PwOutgoingLabel.setter
	def PwOutgoingLabel(self, value):
		self._set_attribute('pwOutgoingLabel', value)

	@property
	def PwOutgoingLabelStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwOutgoingLabelStep')
	@PwOutgoingLabelStep.setter
	def PwOutgoingLabelStep(self, value):
		self._set_attribute('pwOutgoingLabelStep', value)

	@property
	def PwOutgoingLabelStepAcrossLsp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwOutgoingLabelStepAcrossLsp')
	@PwOutgoingLabelStepAcrossLsp.setter
	def PwOutgoingLabelStepAcrossLsp(self, value):
		self._set_attribute('pwOutgoingLabelStepAcrossLsp', value)

	@property
	def PwStatusFaultReplyInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusFaultReplyInterval')
	@PwStatusFaultReplyInterval.setter
	def PwStatusFaultReplyInterval(self, value):
		self._set_attribute('pwStatusFaultReplyInterval', value)

	@property
	def PwStatusTrafficClass(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pwStatusTrafficClass')
	@PwStatusTrafficClass.setter
	def PwStatusTrafficClass(self, value):
		self._set_attribute('pwStatusTrafficClass', value)

	@property
	def RangeRole(self):
		"""

		Returns:
			str(none|working|protect)
		"""
		return self._get_attribute('rangeRole')
	@RangeRole.setter
	def RangeRole(self, value):
		self._set_attribute('rangeRole', value)

	@property
	def RepeatMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('repeatMac')
	@RepeatMac.setter
	def RepeatMac(self, value):
		self._set_attribute('repeatMac', value)

	@property
	def Revertive(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('revertive')
	@Revertive.setter
	def Revertive(self, value):
		self._set_attribute('revertive', value)

	@property
	def SkipZeroVlanId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('skipZeroVlanId')
	@SkipZeroVlanId.setter
	def SkipZeroVlanId(self, value):
		self._set_attribute('skipZeroVlanId', value)

	@property
	def SrcAcId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcAcId')
	@SrcAcId.setter
	def SrcAcId(self, value):
		self._set_attribute('srcAcId', value)

	@property
	def SrcAcIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcAcIdStep')
	@SrcAcIdStep.setter
	def SrcAcIdStep(self, value):
		self._set_attribute('srcAcIdStep', value)

	@property
	def SrcGlobalId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcGlobalId')
	@SrcGlobalId.setter
	def SrcGlobalId(self, value):
		self._set_attribute('srcGlobalId', value)

	@property
	def SrcLspNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcLspNumber')
	@SrcLspNumber.setter
	def SrcLspNumber(self, value):
		self._set_attribute('srcLspNumber', value)

	@property
	def SrcLspNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcLspNumberStep')
	@SrcLspNumberStep.setter
	def SrcLspNumberStep(self, value):
		self._set_attribute('srcLspNumberStep', value)

	@property
	def SrcMepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcMepId')
	@SrcMepId.setter
	def SrcMepId(self, value):
		self._set_attribute('srcMepId', value)

	@property
	def SrcMepIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcMepIdStep')
	@SrcMepIdStep.setter
	def SrcMepIdStep(self, value):
		self._set_attribute('srcMepIdStep', value)

	@property
	def SrcNodeId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcNodeId')
	@SrcNodeId.setter
	def SrcNodeId(self, value):
		self._set_attribute('srcNodeId', value)

	@property
	def SrcTunnelNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcTunnelNumber')
	@SrcTunnelNumber.setter
	def SrcTunnelNumber(self, value):
		self._set_attribute('srcTunnelNumber', value)

	@property
	def SrcTunnelNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcTunnelNumberStep')
	@SrcTunnelNumberStep.setter
	def SrcTunnelNumberStep(self, value):
		self._set_attribute('srcTunnelNumberStep', value)

	@property
	def SrcVplsIdAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAsNumber')
	@SrcVplsIdAsNumber.setter
	def SrcVplsIdAsNumber(self, value):
		self._set_attribute('srcVplsIdAsNumber', value)

	@property
	def SrcVplsIdAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAsNumberStep')
	@SrcVplsIdAsNumberStep.setter
	def SrcVplsIdAsNumberStep(self, value):
		self._set_attribute('srcVplsIdAsNumberStep', value)

	@property
	def SrcVplsIdAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAssignedNumber')
	@SrcVplsIdAssignedNumber.setter
	def SrcVplsIdAssignedNumber(self, value):
		self._set_attribute('srcVplsIdAssignedNumber', value)

	@property
	def SrcVplsIdAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAssignedNumberStep')
	@SrcVplsIdAssignedNumberStep.setter
	def SrcVplsIdAssignedNumberStep(self, value):
		self._set_attribute('srcVplsIdAssignedNumberStep', value)

	@property
	def SrcVplsIdIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('srcVplsIdIpAddress')
	@SrcVplsIdIpAddress.setter
	def SrcVplsIdIpAddress(self, value):
		self._set_attribute('srcVplsIdIpAddress', value)

	@property
	def SrcVplsIdIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('srcVplsIdIpAddressStep')
	@SrcVplsIdIpAddressStep.setter
	def SrcVplsIdIpAddressStep(self, value):
		self._set_attribute('srcVplsIdIpAddressStep', value)

	@property
	def SrcVplsIdType(self):
		"""

		Returns:
			str(asNumber|ipAddress|asNumber4Bytes)
		"""
		return self._get_attribute('srcVplsIdType')
	@SrcVplsIdType.setter
	def SrcVplsIdType(self, value):
		self._set_attribute('srcVplsIdType', value)

	@property
	def SupportSlowStart(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportSlowStart')
	@SupportSlowStart.setter
	def SupportSlowStart(self, value):
		self._set_attribute('supportSlowStart', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def TypeOfProtectionSwitching(self):
		"""

		Returns:
			str(1+1Unidirectional|1:1Bidirectional|1+1Bidirectional)
		"""
		return self._get_attribute('typeOfProtectionSwitching')
	@TypeOfProtectionSwitching.setter
	def TypeOfProtectionSwitching(self, value):
		self._set_attribute('typeOfProtectionSwitching', value)

	@property
	def TypeOfRange(self):
		"""

		Returns:
			str(lsp|pw|nestedLspPw)
		"""
		return self._get_attribute('typeOfRange')
	@TypeOfRange.setter
	def TypeOfRange(self, value):
		self._set_attribute('typeOfRange', value)

	@property
	def VlanCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanIncrementMode(self):
		"""

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('vlanIncrementMode')
	@VlanIncrementMode.setter
	def VlanIncrementMode(self, value):
		self._set_attribute('vlanIncrementMode', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	@property
	def VlanTpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanTpId')
	@VlanTpId.setter
	def VlanTpId(self, value):
		self._set_attribute('vlanTpId', value)

	@property
	def WaitToRevertTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('waitToRevertTime')
	@WaitToRevertTime.setter
	def WaitToRevertTime(self, value):
		self._set_attribute('waitToRevertTime', value)

	def add(self, AlarmTrafficClass=None, AlarmType=None, ApsTrafficClass=None, ApsType=None, CccvInterval=None, CccvTrafficClass=None, CccvType=None, Description=None, DestAcId=None, DestAcIdStep=None, DestGlobalId=None, DestLspNumber=None, DestLspNumberStep=None, DestMepId=None, DestMepIdStep=None, DestNodeId=None, DestTunnelNumber=None, DestTunnelNumberStep=None, DestVplsIdAsNumber=None, DestVplsIdAsNumberStep=None, DestVplsIdAssignedNumber=None, DestVplsIdAssignedNumberStep=None, DestVplsIdIpAddress=None, DestVplsIdIpAddressStep=None, DestVplsIdType=None, DmTimeFormat=None, DmTrafficClass=None, DmType=None, EnableVlan=None, Enabled=None, IpAddress=None, IpAddressMask=None, IpAddressStep=None, IpHostPerLsp=None, IpType=None, LmCounterType=None, LmInitialRxValue=None, LmInitialTxValue=None, LmRxStep=None, LmTrafficClass=None, LmTxStep=None, LmType=None, LspIncomingLabel=None, LspIncomingLabelStep=None, LspOutgoingLabel=None, LspOutgoingLabelStep=None, MacAddress=None, MacPerPw=None, MegIdIntegerStep=None, MegIdPrefix=None, MegLevel=None, MinRxInterval=None, MinTxInterval=None, NumberOfLsp=None, NumberOfPwPerLsp=None, OnDemandCvTrafficClass=None, PeerLspOrPwRange=None, PeerNestedLspPwRange=None, PwIncomingLabel=None, PwIncomingLabelStep=None, PwIncomingLabelStepAcrossLsp=None, PwOutgoingLabel=None, PwOutgoingLabelStep=None, PwOutgoingLabelStepAcrossLsp=None, PwStatusFaultReplyInterval=None, PwStatusTrafficClass=None, RangeRole=None, RepeatMac=None, Revertive=None, SkipZeroVlanId=None, SrcAcId=None, SrcAcIdStep=None, SrcGlobalId=None, SrcLspNumber=None, SrcLspNumberStep=None, SrcMepId=None, SrcMepIdStep=None, SrcNodeId=None, SrcTunnelNumber=None, SrcTunnelNumberStep=None, SrcVplsIdAsNumber=None, SrcVplsIdAsNumberStep=None, SrcVplsIdAssignedNumber=None, SrcVplsIdAssignedNumberStep=None, SrcVplsIdIpAddress=None, SrcVplsIdIpAddressStep=None, SrcVplsIdType=None, SupportSlowStart=None, TrafficGroupId=None, TypeOfProtectionSwitching=None, TypeOfRange=None, VlanCount=None, VlanId=None, VlanIncrementMode=None, VlanPriority=None, VlanTpId=None, WaitToRevertTime=None):
		"""Adds a new lspPwRange node on the server and retrieves it in this instance.

		Args:
			AlarmTrafficClass (number): 
			AlarmType (str(ietf|y1731)): 
			ApsTrafficClass (number): 
			ApsType (str(ietf|y1731)): 
			CccvInterval (number): 
			CccvTrafficClass (number): 
			CccvType (str(bfdCc|bfdCccv|y1731|none)): 
			Description (str): 
			DestAcId (number): 
			DestAcIdStep (number): 
			DestGlobalId (number): 
			DestLspNumber (number): 
			DestLspNumberStep (number): 
			DestMepId (number): 
			DestMepIdStep (number): 
			DestNodeId (number): 
			DestTunnelNumber (number): 
			DestTunnelNumberStep (number): 
			DestVplsIdAsNumber (number): 
			DestVplsIdAsNumberStep (number): 
			DestVplsIdAssignedNumber (number): 
			DestVplsIdAssignedNumberStep (number): 
			DestVplsIdIpAddress (str): 
			DestVplsIdIpAddressStep (str): 
			DestVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): 
			DmTimeFormat (str(ieee|ntp)): 
			DmTrafficClass (number): 
			DmType (str(ietf|y1731)): 
			EnableVlan (bool): 
			Enabled (bool): 
			IpAddress (str): 
			IpAddressMask (number): 
			IpAddressStep (number): 
			IpHostPerLsp (number): 
			IpType (str(ipv4|ipv6)): 
			LmCounterType (str(32Bit|64Bit)): 
			LmInitialRxValue (number): 
			LmInitialTxValue (number): 
			LmRxStep (number): 
			LmTrafficClass (number): 
			LmTxStep (number): 
			LmType (str(ietf|y1731)): 
			LspIncomingLabel (number): 
			LspIncomingLabelStep (number): 
			LspOutgoingLabel (number): 
			LspOutgoingLabelStep (number): 
			MacAddress (str): 
			MacPerPw (number): 
			MegIdIntegerStep (number): 
			MegIdPrefix (str): 
			MegLevel (number): 
			MinRxInterval (number): 
			MinTxInterval (number): 
			NumberOfLsp (number): 
			NumberOfPwPerLsp (number): 
			OnDemandCvTrafficClass (number): 
			PeerLspOrPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): 
			PeerNestedLspPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): 
			PwIncomingLabel (number): 
			PwIncomingLabelStep (number): 
			PwIncomingLabelStepAcrossLsp (number): 
			PwOutgoingLabel (number): 
			PwOutgoingLabelStep (number): 
			PwOutgoingLabelStepAcrossLsp (number): 
			PwStatusFaultReplyInterval (number): 
			PwStatusTrafficClass (number): 
			RangeRole (str(none|working|protect)): 
			RepeatMac (bool): 
			Revertive (bool): 
			SkipZeroVlanId (bool): 
			SrcAcId (number): 
			SrcAcIdStep (number): 
			SrcGlobalId (number): 
			SrcLspNumber (number): 
			SrcLspNumberStep (number): 
			SrcMepId (number): 
			SrcMepIdStep (number): 
			SrcNodeId (number): 
			SrcTunnelNumber (number): 
			SrcTunnelNumberStep (number): 
			SrcVplsIdAsNumber (number): 
			SrcVplsIdAsNumberStep (number): 
			SrcVplsIdAssignedNumber (number): 
			SrcVplsIdAssignedNumberStep (number): 
			SrcVplsIdIpAddress (str): 
			SrcVplsIdIpAddressStep (str): 
			SrcVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): 
			SupportSlowStart (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TypeOfProtectionSwitching (str(1+1Unidirectional|1:1Bidirectional|1+1Bidirectional)): 
			TypeOfRange (str(lsp|pw|nestedLspPw)): 
			VlanCount (number): 
			VlanId (str): 
			VlanIncrementMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			VlanPriority (str): 
			VlanTpId (str): 
			WaitToRevertTime (number): 

		Returns:
			self: This instance with all currently retrieved lspPwRange data using find and the newly added lspPwRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the lspPwRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AlarmTrafficClass=None, AlarmType=None, ApsTrafficClass=None, ApsType=None, CccvInterval=None, CccvTrafficClass=None, CccvType=None, Description=None, DestAcId=None, DestAcIdStep=None, DestGlobalId=None, DestLspNumber=None, DestLspNumberStep=None, DestMepId=None, DestMepIdStep=None, DestNodeId=None, DestTunnelNumber=None, DestTunnelNumberStep=None, DestVplsIdAsNumber=None, DestVplsIdAsNumberStep=None, DestVplsIdAssignedNumber=None, DestVplsIdAssignedNumberStep=None, DestVplsIdIpAddress=None, DestVplsIdIpAddressStep=None, DestVplsIdType=None, DmTimeFormat=None, DmTrafficClass=None, DmType=None, EnableVlan=None, Enabled=None, IpAddress=None, IpAddressMask=None, IpAddressStep=None, IpHostPerLsp=None, IpType=None, LmCounterType=None, LmInitialRxValue=None, LmInitialTxValue=None, LmRxStep=None, LmTrafficClass=None, LmTxStep=None, LmType=None, LspIncomingLabel=None, LspIncomingLabelStep=None, LspOutgoingLabel=None, LspOutgoingLabelStep=None, MacAddress=None, MacPerPw=None, MegIdIntegerStep=None, MegIdPrefix=None, MegLevel=None, MinRxInterval=None, MinTxInterval=None, NumberOfLsp=None, NumberOfPwPerLsp=None, OnDemandCvTrafficClass=None, PeerLspOrPwRange=None, PeerNestedLspPwRange=None, PwIncomingLabel=None, PwIncomingLabelStep=None, PwIncomingLabelStepAcrossLsp=None, PwOutgoingLabel=None, PwOutgoingLabelStep=None, PwOutgoingLabelStepAcrossLsp=None, PwStatusFaultReplyInterval=None, PwStatusTrafficClass=None, RangeRole=None, RepeatMac=None, Revertive=None, SkipZeroVlanId=None, SrcAcId=None, SrcAcIdStep=None, SrcGlobalId=None, SrcLspNumber=None, SrcLspNumberStep=None, SrcMepId=None, SrcMepIdStep=None, SrcNodeId=None, SrcTunnelNumber=None, SrcTunnelNumberStep=None, SrcVplsIdAsNumber=None, SrcVplsIdAsNumberStep=None, SrcVplsIdAssignedNumber=None, SrcVplsIdAssignedNumberStep=None, SrcVplsIdIpAddress=None, SrcVplsIdIpAddressStep=None, SrcVplsIdType=None, SupportSlowStart=None, TrafficGroupId=None, TypeOfProtectionSwitching=None, TypeOfRange=None, VlanCount=None, VlanId=None, VlanIncrementMode=None, VlanPriority=None, VlanTpId=None, WaitToRevertTime=None):
		"""Finds and retrieves lspPwRange data from the server.

		All named parameters support regex and can be used to selectively retrieve lspPwRange data from the server.
		By default the find method takes no parameters and will retrieve all lspPwRange data from the server.

		Args:
			AlarmTrafficClass (number): 
			AlarmType (str(ietf|y1731)): 
			ApsTrafficClass (number): 
			ApsType (str(ietf|y1731)): 
			CccvInterval (number): 
			CccvTrafficClass (number): 
			CccvType (str(bfdCc|bfdCccv|y1731|none)): 
			Description (str): 
			DestAcId (number): 
			DestAcIdStep (number): 
			DestGlobalId (number): 
			DestLspNumber (number): 
			DestLspNumberStep (number): 
			DestMepId (number): 
			DestMepIdStep (number): 
			DestNodeId (number): 
			DestTunnelNumber (number): 
			DestTunnelNumberStep (number): 
			DestVplsIdAsNumber (number): 
			DestVplsIdAsNumberStep (number): 
			DestVplsIdAssignedNumber (number): 
			DestVplsIdAssignedNumberStep (number): 
			DestVplsIdIpAddress (str): 
			DestVplsIdIpAddressStep (str): 
			DestVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): 
			DmTimeFormat (str(ieee|ntp)): 
			DmTrafficClass (number): 
			DmType (str(ietf|y1731)): 
			EnableVlan (bool): 
			Enabled (bool): 
			IpAddress (str): 
			IpAddressMask (number): 
			IpAddressStep (number): 
			IpHostPerLsp (number): 
			IpType (str(ipv4|ipv6)): 
			LmCounterType (str(32Bit|64Bit)): 
			LmInitialRxValue (number): 
			LmInitialTxValue (number): 
			LmRxStep (number): 
			LmTrafficClass (number): 
			LmTxStep (number): 
			LmType (str(ietf|y1731)): 
			LspIncomingLabel (number): 
			LspIncomingLabelStep (number): 
			LspOutgoingLabel (number): 
			LspOutgoingLabelStep (number): 
			MacAddress (str): 
			MacPerPw (number): 
			MegIdIntegerStep (number): 
			MegIdPrefix (str): 
			MegLevel (number): 
			MinRxInterval (number): 
			MinTxInterval (number): 
			NumberOfLsp (number): 
			NumberOfPwPerLsp (number): 
			OnDemandCvTrafficClass (number): 
			PeerLspOrPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): 
			PeerNestedLspPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): 
			PwIncomingLabel (number): 
			PwIncomingLabelStep (number): 
			PwIncomingLabelStepAcrossLsp (number): 
			PwOutgoingLabel (number): 
			PwOutgoingLabelStep (number): 
			PwOutgoingLabelStepAcrossLsp (number): 
			PwStatusFaultReplyInterval (number): 
			PwStatusTrafficClass (number): 
			RangeRole (str(none|working|protect)): 
			RepeatMac (bool): 
			Revertive (bool): 
			SkipZeroVlanId (bool): 
			SrcAcId (number): 
			SrcAcIdStep (number): 
			SrcGlobalId (number): 
			SrcLspNumber (number): 
			SrcLspNumberStep (number): 
			SrcMepId (number): 
			SrcMepIdStep (number): 
			SrcNodeId (number): 
			SrcTunnelNumber (number): 
			SrcTunnelNumberStep (number): 
			SrcVplsIdAsNumber (number): 
			SrcVplsIdAsNumberStep (number): 
			SrcVplsIdAssignedNumber (number): 
			SrcVplsIdAssignedNumberStep (number): 
			SrcVplsIdIpAddress (str): 
			SrcVplsIdIpAddressStep (str): 
			SrcVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): 
			SupportSlowStart (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			TypeOfProtectionSwitching (str(1+1Unidirectional|1:1Bidirectional|1+1Bidirectional)): 
			TypeOfRange (str(lsp|pw|nestedLspPw)): 
			VlanCount (number): 
			VlanId (str): 
			VlanIncrementMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			VlanPriority (str): 
			VlanTpId (str): 
			WaitToRevertTime (number): 

		Returns:
			self: This instance with matching lspPwRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lspPwRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lspPwRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
