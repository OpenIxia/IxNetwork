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
		"""This signifies the Alarm Traffic Class for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('alarmTrafficClass')
	@AlarmTrafficClass.setter
	def AlarmTrafficClass(self, value):
		self._set_attribute('alarmTrafficClass', value)

	@property
	def AlarmType(self):
		"""This signifies the Alarm Type. Possible values include IETF and Y.1731.

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('alarmType')
	@AlarmType.setter
	def AlarmType(self, value):
		self._set_attribute('alarmType', value)

	@property
	def ApsTrafficClass(self):
		"""This signifies the Traffic Class of the APS message.

		Returns:
			number
		"""
		return self._get_attribute('apsTrafficClass')
	@ApsTrafficClass.setter
	def ApsTrafficClass(self, value):
		self._set_attribute('apsTrafficClass', value)

	@property
	def ApsType(self):
		"""This signifies the APS type. Possible values include IETF and Y.1731.

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('apsType')
	@ApsType.setter
	def ApsType(self, value):
		self._set_attribute('apsType', value)

	@property
	def CccvInterval(self):
		"""This signifies the CCCV Interval in milliseconds.If cccv type is bfd then this field will take any value between 3-600000, if cccv type is y1731 then cccv interval can be configured to values available in the drop down menu.

		Returns:
			number
		"""
		return self._get_attribute('cccvInterval')
	@CccvInterval.setter
	def CccvInterval(self, value):
		self._set_attribute('cccvInterval', value)

	@property
	def CccvTrafficClass(self):
		"""This signifies the CCCV Traffic Class.

		Returns:
			number
		"""
		return self._get_attribute('cccvTrafficClass')
	@CccvTrafficClass.setter
	def CccvTrafficClass(self, value):
		self._set_attribute('cccvTrafficClass', value)

	@property
	def CccvType(self):
		"""This signifies the CCCV Type. Possible values include BFD CC, Y.1731 and None.

		Returns:
			str(bfdCc|bfdCccv|y1731|none)
		"""
		return self._get_attribute('cccvType')
	@CccvType.setter
	def CccvType(self, value):
		self._set_attribute('cccvType', value)

	@property
	def Description(self):
		"""This signifies the description of the range.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DestAcId(self):
		"""This signifies the destination AC id. This is the ac id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.

		Returns:
			number
		"""
		return self._get_attribute('destAcId')
	@DestAcId.setter
	def DestAcId(self, value):
		self._set_attribute('destAcId', value)

	@property
	def DestAcIdStep(self):
		"""This signifies the destination AC id step value.

		Returns:
			number
		"""
		return self._get_attribute('destAcIdStep')
	@DestAcIdStep.setter
	def DestAcIdStep(self, value):
		self._set_attribute('destAcIdStep', value)

	@property
	def DestGlobalId(self):
		"""This signifies the global id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.

		Returns:
			number
		"""
		return self._get_attribute('destGlobalId')
	@DestGlobalId.setter
	def DestGlobalId(self, value):
		self._set_attribute('destGlobalId', value)

	@property
	def DestLspNumber(self):
		"""This signifies the lsp number that is expected on the peer, if there is a mismatch with the one configured on the peer LSP or PW, On Demand Ping and On Demand Traceroute will result in failure.

		Returns:
			number
		"""
		return self._get_attribute('destLspNumber')
	@DestLspNumber.setter
	def DestLspNumber(self, value):
		self._set_attribute('destLspNumber', value)

	@property
	def DestLspNumberStep(self):
		"""This signifies the source LSP Number step value.

		Returns:
			number
		"""
		return self._get_attribute('destLspNumberStep')
	@DestLspNumberStep.setter
	def DestLspNumberStep(self, value):
		self._set_attribute('destLspNumberStep', value)

	@property
	def DestMepId(self):
		"""This signifies the destination MEP Id.

		Returns:
			number
		"""
		return self._get_attribute('destMepId')
	@DestMepId.setter
	def DestMepId(self, value):
		self._set_attribute('destMepId', value)

	@property
	def DestMepIdStep(self):
		"""This signifies the Destination MEP Id step value in integer.

		Returns:
			number
		"""
		return self._get_attribute('destMepIdStep')
	@DestMepIdStep.setter
	def DestMepIdStep(self, value):
		self._set_attribute('destMepIdStep', value)

	@property
	def DestNodeId(self):
		"""This signifies the destination node id. This is the node id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.

		Returns:
			number
		"""
		return self._get_attribute('destNodeId')
	@DestNodeId.setter
	def DestNodeId(self, value):
		self._set_attribute('destNodeId', value)

	@property
	def DestTunnelNumber(self):
		"""This signifies the tunnel number that is expected on the peer, if there is a mismatch with the one configured on the peer LSP or PW, On Demand Ping and On Demand Traceroute will result in failure.

		Returns:
			number
		"""
		return self._get_attribute('destTunnelNumber')
	@DestTunnelNumber.setter
	def DestTunnelNumber(self, value):
		self._set_attribute('destTunnelNumber', value)

	@property
	def DestTunnelNumberStep(self):
		"""This signifies the destination tunnel number step value.

		Returns:
			number
		"""
		return self._get_attribute('destTunnelNumberStep')
	@DestTunnelNumberStep.setter
	def DestTunnelNumberStep(self, value):
		self._set_attribute('destTunnelNumberStep', value)

	@property
	def DestVplsIdAsNumber(self):
		"""This signifies the AS Number configured as Source VPLS Id AS Number when VPLS Id type is set as asNumber or asNumber4Bytes. If it is asNumber then the max AS Number can be 65535 and when it is asNumber4Bytes the max value can be 4294967295.

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAsNumber')
	@DestVplsIdAsNumber.setter
	def DestVplsIdAsNumber(self, value):
		self._set_attribute('destVplsIdAsNumber', value)

	@property
	def DestVplsIdAsNumberStep(self):
		"""This signifies the step of destination vpls id AS number by which the AS number will be incremented if there are multiple LSP/PW in the range.

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAsNumberStep')
	@DestVplsIdAsNumberStep.setter
	def DestVplsIdAsNumberStep(self, value):
		self._set_attribute('destVplsIdAsNumberStep', value)

	@property
	def DestVplsIdAssignedNumber(self):
		"""This signifies the destination VPLS Id Assigned Number. If the VPLS Id type is configured as either ipAddress or asNumber4Bytes then the max Assigned Number can be 65535 and when it is asNumber, the max value can be 4294967295.

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAssignedNumber')
	@DestVplsIdAssignedNumber.setter
	def DestVplsIdAssignedNumber(self, value):
		self._set_attribute('destVplsIdAssignedNumber', value)

	@property
	def DestVplsIdAssignedNumberStep(self):
		"""This signifies the step of Assigned number by which the number is incremented if there are multiple LSP/PW in the range.

		Returns:
			number
		"""
		return self._get_attribute('destVplsIdAssignedNumberStep')
	@DestVplsIdAssignedNumberStep.setter
	def DestVplsIdAssignedNumberStep(self, value):
		self._set_attribute('destVplsIdAssignedNumberStep', value)

	@property
	def DestVplsIdIpAddress(self):
		"""This specifies the IP Address configured as destination VPLS Id IP Address when VPLS Id type is set as ipAddress.

		Returns:
			str
		"""
		return self._get_attribute('destVplsIdIpAddress')
	@DestVplsIdIpAddress.setter
	def DestVplsIdIpAddress(self, value):
		self._set_attribute('destVplsIdIpAddress', value)

	@property
	def DestVplsIdIpAddressStep(self):
		"""This signifies the step of ip address by which the ip address will be incremented if there are multiple LSP/PW in the range.

		Returns:
			str
		"""
		return self._get_attribute('destVplsIdIpAddressStep')
	@DestVplsIdIpAddressStep.setter
	def DestVplsIdIpAddressStep(self, value):
		self._set_attribute('destVplsIdIpAddressStep', value)

	@property
	def DestVplsIdType(self):
		"""This signifies the destination VplsId type.

		Returns:
			str(asNumber|ipAddress|asNumber4Bytes)
		"""
		return self._get_attribute('destVplsIdType')
	@DestVplsIdType.setter
	def DestVplsIdType(self, value):
		self._set_attribute('destVplsIdType', value)

	@property
	def DmTimeFormat(self):
		"""This signifies the DM Time Format. Possible values include IEEE and NTP.

		Returns:
			str(ieee|ntp)
		"""
		return self._get_attribute('dmTimeFormat')
	@DmTimeFormat.setter
	def DmTimeFormat(self, value):
		self._set_attribute('dmTimeFormat', value)

	@property
	def DmTrafficClass(self):
		"""This signifies the DM Traffic Class for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('dmTrafficClass')
	@DmTrafficClass.setter
	def DmTrafficClass(self, value):
		self._set_attribute('dmTrafficClass', value)

	@property
	def DmType(self):
		"""This signifies the DM Type. Possible values include IETF and Y.1731.

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('dmType')
	@DmType.setter
	def DmType(self, value):
		self._set_attribute('dmType', value)

	@property
	def EnableVlan(self):
		"""If true, the MAC Traffic will have a vlan header.

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def Enabled(self):
		"""This signifies the enablement of this LSP PW Range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IpAddress(self):
		"""This signifies the IP address.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def IpAddressMask(self):
		"""This signifies the IP Address Mask.

		Returns:
			number
		"""
		return self._get_attribute('ipAddressMask')
	@IpAddressMask.setter
	def IpAddressMask(self, value):
		self._set_attribute('ipAddressMask', value)

	@property
	def IpAddressStep(self):
		"""This signifies the IP Address Step Value.

		Returns:
			number
		"""
		return self._get_attribute('ipAddressStep')
	@IpAddressStep.setter
	def IpAddressStep(self, value):
		self._set_attribute('ipAddressStep', value)

	@property
	def IpHostPerLsp(self):
		"""This signifies the total number of IP hosts per lsp.

		Returns:
			number
		"""
		return self._get_attribute('ipHostPerLsp')
	@IpHostPerLsp.setter
	def IpHostPerLsp(self, value):
		self._set_attribute('ipHostPerLsp', value)

	@property
	def IpType(self):
		"""This signifies the IP Type. Possible values include IPv4 and IPv6.

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def LmCounterType(self):
		"""This signifies the LM Counter Type. Possible values include 32 Bit and 64 Bit.

		Returns:
			str(32Bit|64Bit)
		"""
		return self._get_attribute('lmCounterType')
	@LmCounterType.setter
	def LmCounterType(self, value):
		self._set_attribute('lmCounterType', value)

	@property
	def LmInitialRxValue(self):
		"""This signifies the LM Initial Rx value for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('lmInitialRxValue')
	@LmInitialRxValue.setter
	def LmInitialRxValue(self, value):
		self._set_attribute('lmInitialRxValue', value)

	@property
	def LmInitialTxValue(self):
		"""This signifies the LM Initial Tx value for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('lmInitialTxValue')
	@LmInitialTxValue.setter
	def LmInitialTxValue(self, value):
		self._set_attribute('lmInitialTxValue', value)

	@property
	def LmRxStep(self):
		"""This signifies the LM Rx step value for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('lmRxStep')
	@LmRxStep.setter
	def LmRxStep(self, value):
		self._set_attribute('lmRxStep', value)

	@property
	def LmTrafficClass(self):
		"""This signifies the LM Traffic Class.

		Returns:
			number
		"""
		return self._get_attribute('lmTrafficClass')
	@LmTrafficClass.setter
	def LmTrafficClass(self, value):
		self._set_attribute('lmTrafficClass', value)

	@property
	def LmTxStep(self):
		"""This signifies the LM Tx Step value for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('lmTxStep')
	@LmTxStep.setter
	def LmTxStep(self, value):
		self._set_attribute('lmTxStep', value)

	@property
	def LmType(self):
		"""This signifies the LM Type. Possible values include IETF and Y.1731.

		Returns:
			str(ietf|y1731)
		"""
		return self._get_attribute('lmType')
	@LmType.setter
	def LmType(self, value):
		self._set_attribute('lmType', value)

	@property
	def LspIncomingLabel(self):
		"""This signifies the LSP Incoming label value. All mpls-tp packets are expected to be received with this LSP label value, if there is a mismatch of this value with the peer's outgoing LSP label value, cccv sessions will not come up.

		Returns:
			number
		"""
		return self._get_attribute('lspIncomingLabel')
	@LspIncomingLabel.setter
	def LspIncomingLabel(self, value):
		self._set_attribute('lspIncomingLabel', value)

	@property
	def LspIncomingLabelStep(self):
		"""This signifies the LSP Incoming Label Step value.

		Returns:
			number
		"""
		return self._get_attribute('lspIncomingLabelStep')
	@LspIncomingLabelStep.setter
	def LspIncomingLabelStep(self, value):
		self._set_attribute('lspIncomingLabelStep', value)

	@property
	def LspOutgoingLabel(self):
		"""This signifies the LSP Outgoing Label value. All mpls-tp packets are transmitted with this LSP label from the port.

		Returns:
			number
		"""
		return self._get_attribute('lspOutgoingLabel')
	@LspOutgoingLabel.setter
	def LspOutgoingLabel(self, value):
		self._set_attribute('lspOutgoingLabel', value)

	@property
	def LspOutgoingLabelStep(self):
		"""This signifies the LSP Outgoing Label Step value.

		Returns:
			number
		"""
		return self._get_attribute('lspOutgoingLabelStep')
	@LspOutgoingLabelStep.setter
	def LspOutgoingLabelStep(self, value):
		self._set_attribute('lspOutgoingLabelStep', value)

	@property
	def MacAddress(self):
		"""This signifies the starting MAC address of the range, this will be used for traffic generation.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MacPerPw(self):
		"""This signifies the number of MACs behind each PW, these are the MACs that are used for traffic generation.

		Returns:
			number
		"""
		return self._get_attribute('macPerPw')
	@MacPerPw.setter
	def MacPerPw(self, value):
		self._set_attribute('macPerPw', value)

	@property
	def MegIdIntegerStep(self):
		"""This signifies the MEG Id step value in integer.

		Returns:
			number
		"""
		return self._get_attribute('megIdIntegerStep')
	@MegIdIntegerStep.setter
	def MegIdIntegerStep(self, value):
		self._set_attribute('megIdIntegerStep', value)

	@property
	def MegIdPrefix(self):
		"""This signifies the prefix for the MEG Id.

		Returns:
			str
		"""
		return self._get_attribute('megIdPrefix')
	@MegIdPrefix.setter
	def MegIdPrefix(self, value):
		self._set_attribute('megIdPrefix', value)

	@property
	def MegLevel(self):
		"""This signifies the peer range of the nested LSP PW value.

		Returns:
			number
		"""
		return self._get_attribute('megLevel')
	@MegLevel.setter
	def MegLevel(self, value):
		self._set_attribute('megLevel', value)

	@property
	def MinRxInterval(self):
		"""This signifies the CCCV minimum receive interval of cc messages, in milliseconds. Not valid for cccv type y1731.

		Returns:
			number
		"""
		return self._get_attribute('minRxInterval')
	@MinRxInterval.setter
	def MinRxInterval(self, value):
		self._set_attribute('minRxInterval', value)

	@property
	def MinTxInterval(self):
		"""This signifies the CCCV minimum transmit interval of cc messages, in milliseconds. Valid for all types of cccv.

		Returns:
			number
		"""
		return self._get_attribute('minTxInterval')
	@MinTxInterval.setter
	def MinTxInterval(self, value):
		self._set_attribute('minTxInterval', value)

	@property
	def NumberOfLsp(self):
		"""This signifies the total number of LSPs for this range.

		Returns:
			number
		"""
		return self._get_attribute('numberOfLsp')
	@NumberOfLsp.setter
	def NumberOfLsp(self, value):
		self._set_attribute('numberOfLsp', value)

	@property
	def NumberOfPwPerLsp(self):
		"""This signifies the total number of PWs per LSP.

		Returns:
			number
		"""
		return self._get_attribute('numberOfPwPerLsp')
	@NumberOfPwPerLsp.setter
	def NumberOfPwPerLsp(self, value):
		self._set_attribute('numberOfPwPerLsp', value)

	@property
	def OnDemandCvTrafficClass(self):
		"""This signifies the On Demand CV Traffic Class for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('onDemandCvTrafficClass')
	@OnDemandCvTrafficClass.setter
	def OnDemandCvTrafficClass(self, value):
		self._set_attribute('onDemandCvTrafficClass', value)

	@property
	def PeerLspOrPwRange(self):
		"""This signifies the type of Peer LSP Or PW Range.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)
		"""
		return self._get_attribute('peerLspOrPwRange')
	@PeerLspOrPwRange.setter
	def PeerLspOrPwRange(self, value):
		self._set_attribute('peerLspOrPwRange', value)

	@property
	def PeerNestedLspPwRange(self):
		"""This signifies the peer range of the nested LSP PW value.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)
		"""
		return self._get_attribute('peerNestedLspPwRange')
	@PeerNestedLspPwRange.setter
	def PeerNestedLspPwRange(self, value):
		self._set_attribute('peerNestedLspPwRange', value)

	@property
	def PwIncomingLabel(self):
		"""This signifies the PW Incoming Label value. All mpls-tp packets are expected to be received with this PW label value, if there is a mismatch of this value with the peer's outgoing PW label value, cccv sessions will not come up.

		Returns:
			number
		"""
		return self._get_attribute('pwIncomingLabel')
	@PwIncomingLabel.setter
	def PwIncomingLabel(self, value):
		self._set_attribute('pwIncomingLabel', value)

	@property
	def PwIncomingLabelStep(self):
		"""This signifies the PW Incoming Label Step value.

		Returns:
			number
		"""
		return self._get_attribute('pwIncomingLabelStep')
	@PwIncomingLabelStep.setter
	def PwIncomingLabelStep(self, value):
		self._set_attribute('pwIncomingLabelStep', value)

	@property
	def PwIncomingLabelStepAcrossLsp(self):
		"""This signifies the PW Incoming Label Step value across LSPs.

		Returns:
			number
		"""
		return self._get_attribute('pwIncomingLabelStepAcrossLsp')
	@PwIncomingLabelStepAcrossLsp.setter
	def PwIncomingLabelStepAcrossLsp(self, value):
		self._set_attribute('pwIncomingLabelStepAcrossLsp', value)

	@property
	def PwOutgoingLabel(self):
		"""This signifies the PW Outgoing Label value. All mpls-tp packets are transmitted with this PW label from the port.

		Returns:
			number
		"""
		return self._get_attribute('pwOutgoingLabel')
	@PwOutgoingLabel.setter
	def PwOutgoingLabel(self, value):
		self._set_attribute('pwOutgoingLabel', value)

	@property
	def PwOutgoingLabelStep(self):
		"""This signifies the PW Outgoing Label Step value.

		Returns:
			number
		"""
		return self._get_attribute('pwOutgoingLabelStep')
	@PwOutgoingLabelStep.setter
	def PwOutgoingLabelStep(self, value):
		self._set_attribute('pwOutgoingLabelStep', value)

	@property
	def PwOutgoingLabelStepAcrossLsp(self):
		"""This signifies the PW Outgoing Label Step value across LSPs.

		Returns:
			number
		"""
		return self._get_attribute('pwOutgoingLabelStepAcrossLsp')
	@PwOutgoingLabelStepAcrossLsp.setter
	def PwOutgoingLabelStepAcrossLsp(self, value):
		self._set_attribute('pwOutgoingLabelStepAcrossLsp', value)

	@property
	def PwStatusFaultReplyInterval(self):
		"""This signifies the PW Status Fault Reply Interval in seconds.

		Returns:
			number
		"""
		return self._get_attribute('pwStatusFaultReplyInterval')
	@PwStatusFaultReplyInterval.setter
	def PwStatusFaultReplyInterval(self, value):
		self._set_attribute('pwStatusFaultReplyInterval', value)

	@property
	def PwStatusTrafficClass(self):
		"""This signifies the PW Status Traffic Class for LSP PW Range.

		Returns:
			number
		"""
		return self._get_attribute('pwStatusTrafficClass')
	@PwStatusTrafficClass.setter
	def PwStatusTrafficClass(self, value):
		self._set_attribute('pwStatusTrafficClass', value)

	@property
	def RangeRole(self):
		"""This signifies the role of the range. Possible values include None, Working and Protect.

		Returns:
			str(none|working|protect)
		"""
		return self._get_attribute('rangeRole')
	@RangeRole.setter
	def RangeRole(self, value):
		self._set_attribute('rangeRole', value)

	@property
	def RepeatMac(self):
		"""If true, and the Count is greater than 1, the same address value will be repeated for all MAC addresses within a PW.

		Returns:
			bool
		"""
		return self._get_attribute('repeatMac')
	@RepeatMac.setter
	def RepeatMac(self, value):
		self._set_attribute('repeatMac', value)

	@property
	def Revertive(self):
		"""This signifies the switching mode, whether revertive or non-revertive.

		Returns:
			bool
		"""
		return self._get_attribute('revertive')
	@Revertive.setter
	def Revertive(self, value):
		self._set_attribute('revertive', value)

	@property
	def SkipZeroVlanId(self):
		"""This signifies the VLAN Id 0 will not be used for any MAC.

		Returns:
			bool
		"""
		return self._get_attribute('skipZeroVlanId')
	@SkipZeroVlanId.setter
	def SkipZeroVlanId(self, value):
		self._set_attribute('skipZeroVlanId', value)

	@property
	def SrcAcId(self):
		"""This signifies the AC Id that is carried in the Echo Request message that is transmitted from this port.

		Returns:
			number
		"""
		return self._get_attribute('srcAcId')
	@SrcAcId.setter
	def SrcAcId(self, value):
		self._set_attribute('srcAcId', value)

	@property
	def SrcAcIdStep(self):
		"""This signifies the source AC id step value.

		Returns:
			number
		"""
		return self._get_attribute('srcAcIdStep')
	@SrcAcIdStep.setter
	def SrcAcIdStep(self, value):
		self._set_attribute('srcAcIdStep', value)

	@property
	def SrcGlobalId(self):
		"""This signifies the source global id. This is the global id that is carried in the Echo Request message that is transmitted from this port.

		Returns:
			number
		"""
		return self._get_attribute('srcGlobalId')
	@SrcGlobalId.setter
	def SrcGlobalId(self, value):
		self._set_attribute('srcGlobalId', value)

	@property
	def SrcLspNumber(self):
		"""This signifies the lsp number that is carried in the Echo Request message that is transmitted from this port.

		Returns:
			number
		"""
		return self._get_attribute('srcLspNumber')
	@SrcLspNumber.setter
	def SrcLspNumber(self, value):
		self._set_attribute('srcLspNumber', value)

	@property
	def SrcLspNumberStep(self):
		"""This signifies the source LSP Number step value.

		Returns:
			number
		"""
		return self._get_attribute('srcLspNumberStep')
	@SrcLspNumberStep.setter
	def SrcLspNumberStep(self, value):
		self._set_attribute('srcLspNumberStep', value)

	@property
	def SrcMepId(self):
		"""This signifies the source MEP Id.

		Returns:
			number
		"""
		return self._get_attribute('srcMepId')
	@SrcMepId.setter
	def SrcMepId(self, value):
		self._set_attribute('srcMepId', value)

	@property
	def SrcMepIdStep(self):
		"""This signifies the Source MEP Id step value in integer.

		Returns:
			number
		"""
		return self._get_attribute('srcMepIdStep')
	@SrcMepIdStep.setter
	def SrcMepIdStep(self, value):
		self._set_attribute('srcMepIdStep', value)

	@property
	def SrcNodeId(self):
		"""This signifies the node id that is carried in the Echo Request message that is transmitted from this port.

		Returns:
			number
		"""
		return self._get_attribute('srcNodeId')
	@SrcNodeId.setter
	def SrcNodeId(self, value):
		self._set_attribute('srcNodeId', value)

	@property
	def SrcTunnelNumber(self):
		"""This signifies the tunnel number that is carried in the Echo Request message that is transmitted from this port.

		Returns:
			number
		"""
		return self._get_attribute('srcTunnelNumber')
	@SrcTunnelNumber.setter
	def SrcTunnelNumber(self, value):
		self._set_attribute('srcTunnelNumber', value)

	@property
	def SrcTunnelNumberStep(self):
		"""This signifies the source tunnel number step value.

		Returns:
			number
		"""
		return self._get_attribute('srcTunnelNumberStep')
	@SrcTunnelNumberStep.setter
	def SrcTunnelNumberStep(self, value):
		self._set_attribute('srcTunnelNumberStep', value)

	@property
	def SrcVplsIdAsNumber(self):
		"""This signifies the AS Number configured as Source VPLS Id AS Number when VPLS Id type is set as asNumber or asNumber4Bytes. If it is asNumber then the max AS Number can be 65535 and when it is asNumber4Bytes the max value can be 4294967295.

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAsNumber')
	@SrcVplsIdAsNumber.setter
	def SrcVplsIdAsNumber(self, value):
		self._set_attribute('srcVplsIdAsNumber', value)

	@property
	def SrcVplsIdAsNumberStep(self):
		"""This signifies the step of AS number by which the number is incremented if there are multiple LSP/PW in the range.

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAsNumberStep')
	@SrcVplsIdAsNumberStep.setter
	def SrcVplsIdAsNumberStep(self, value):
		self._set_attribute('srcVplsIdAsNumberStep', value)

	@property
	def SrcVplsIdAssignedNumber(self):
		"""This signifies the source VPLS Id Assigned Number. If the VPLS Id type is configured as either ipAddress or asNumber4Bytes then the max Assigned Number can be 65535 and when it is asNumber the max value can be 4294967295.

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAssignedNumber')
	@SrcVplsIdAssignedNumber.setter
	def SrcVplsIdAssignedNumber(self, value):
		self._set_attribute('srcVplsIdAssignedNumber', value)

	@property
	def SrcVplsIdAssignedNumberStep(self):
		"""This specifies the step of Assigned number by which the number is incremented if there are multiple LSP/PW in the range.

		Returns:
			number
		"""
		return self._get_attribute('srcVplsIdAssignedNumberStep')
	@SrcVplsIdAssignedNumberStep.setter
	def SrcVplsIdAssignedNumberStep(self, value):
		self._set_attribute('srcVplsIdAssignedNumberStep', value)

	@property
	def SrcVplsIdIpAddress(self):
		"""This signifies the IP Address configured as Source VPLS Id IP Address when VPLS Id type is set as ipAddress.

		Returns:
			str
		"""
		return self._get_attribute('srcVplsIdIpAddress')
	@SrcVplsIdIpAddress.setter
	def SrcVplsIdIpAddress(self, value):
		self._set_attribute('srcVplsIdIpAddress', value)

	@property
	def SrcVplsIdIpAddressStep(self):
		"""This signifies the step of ip address by which it is incremented if there are multiple LSP/PW in the range.

		Returns:
			str
		"""
		return self._get_attribute('srcVplsIdIpAddressStep')
	@SrcVplsIdIpAddressStep.setter
	def SrcVplsIdIpAddressStep(self, value):
		self._set_attribute('srcVplsIdIpAddressStep', value)

	@property
	def SrcVplsIdType(self):
		"""This specifies the source VplsId type.

		Returns:
			str(asNumber|ipAddress|asNumber4Bytes)
		"""
		return self._get_attribute('srcVplsIdType')
	@SrcVplsIdType.setter
	def SrcVplsIdType(self, value):
		self._set_attribute('srcVplsIdType', value)

	@property
	def SupportSlowStart(self):
		"""This signifies the Support Slow Start. This field is valid only for cccv type bfd and grayed out for y1731. If this is enabled then cccv interval for the peer is not matched for bfd session establishment.

		Returns:
			bool
		"""
		return self._get_attribute('supportSlowStart')
	@SupportSlowStart.setter
	def SupportSlowStart(self, value):
		self._set_attribute('supportSlowStart', value)

	@property
	def TrafficGroupId(self):
		"""This signifies the Traffic Group Id.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def TypeOfProtectionSwitching(self):
		"""This signifies different types of protection switching mechanism.

		Returns:
			str(1+1Unidirectional|1:1Bidirectional|1+1Bidirectional)
		"""
		return self._get_attribute('typeOfProtectionSwitching')
	@TypeOfProtectionSwitching.setter
	def TypeOfProtectionSwitching(self, value):
		self._set_attribute('typeOfProtectionSwitching', value)

	@property
	def TypeOfRange(self):
		"""This signifies the type of range. Possible values include LSP, PW and Nested PW and LSP.

		Returns:
			str(lsp|pw|nestedLspPw)
		"""
		return self._get_attribute('typeOfRange')
	@TypeOfRange.setter
	def TypeOfRange(self, value):
		self._set_attribute('typeOfRange', value)

	@property
	def VlanCount(self):
		"""This signifies the number of VLANs configured for this MAC Range.

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""This signifies the VLAN option is enabled for the current MAC Range and a VLAN Id may be added to the packet, to identify the VLAN that the packet belongs to.

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanIncrementMode(self):
		"""This signifies the mode that defines how the VLAN will be incremented across MACs.

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('vlanIncrementMode')
	@VlanIncrementMode.setter
	def VlanIncrementMode(self, value):
		self._set_attribute('vlanIncrementMode', value)

	@property
	def VlanPriority(self):
		"""This signifies the user priority of the VLAN tag. This may have a value from 0 through 7.

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	@property
	def VlanTpId(self):
		"""This signifies the EtherType that identifies the protocol header that follows the VLAN header.

		Returns:
			str
		"""
		return self._get_attribute('vlanTpId')
	@VlanTpId.setter
	def VlanTpId(self, value):
		self._set_attribute('vlanTpId', value)

	@property
	def WaitToRevertTime(self):
		"""This signifies the duration after which data traffic will be switched from protect to working path once working path has recovered from signal fail. This is configurable only if Revertive is checked.

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
			AlarmTrafficClass (number): This signifies the Alarm Traffic Class for LSP PW Range.
			AlarmType (str(ietf|y1731)): This signifies the Alarm Type. Possible values include IETF and Y.1731.
			ApsTrafficClass (number): This signifies the Traffic Class of the APS message.
			ApsType (str(ietf|y1731)): This signifies the APS type. Possible values include IETF and Y.1731.
			CccvInterval (number): This signifies the CCCV Interval in milliseconds.If cccv type is bfd then this field will take any value between 3-600000, if cccv type is y1731 then cccv interval can be configured to values available in the drop down menu.
			CccvTrafficClass (number): This signifies the CCCV Traffic Class.
			CccvType (str(bfdCc|bfdCccv|y1731|none)): This signifies the CCCV Type. Possible values include BFD CC, Y.1731 and None.
			Description (str): This signifies the description of the range.
			DestAcId (number): This signifies the destination AC id. This is the ac id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestAcIdStep (number): This signifies the destination AC id step value.
			DestGlobalId (number): This signifies the global id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestLspNumber (number): This signifies the lsp number that is expected on the peer, if there is a mismatch with the one configured on the peer LSP or PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestLspNumberStep (number): This signifies the source LSP Number step value.
			DestMepId (number): This signifies the destination MEP Id.
			DestMepIdStep (number): This signifies the Destination MEP Id step value in integer.
			DestNodeId (number): This signifies the destination node id. This is the node id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestTunnelNumber (number): This signifies the tunnel number that is expected on the peer, if there is a mismatch with the one configured on the peer LSP or PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestTunnelNumberStep (number): This signifies the destination tunnel number step value.
			DestVplsIdAsNumber (number): This signifies the AS Number configured as Source VPLS Id AS Number when VPLS Id type is set as asNumber or asNumber4Bytes. If it is asNumber then the max AS Number can be 65535 and when it is asNumber4Bytes the max value can be 4294967295.
			DestVplsIdAsNumberStep (number): This signifies the step of destination vpls id AS number by which the AS number will be incremented if there are multiple LSP/PW in the range.
			DestVplsIdAssignedNumber (number): This signifies the destination VPLS Id Assigned Number. If the VPLS Id type is configured as either ipAddress or asNumber4Bytes then the max Assigned Number can be 65535 and when it is asNumber, the max value can be 4294967295.
			DestVplsIdAssignedNumberStep (number): This signifies the step of Assigned number by which the number is incremented if there are multiple LSP/PW in the range.
			DestVplsIdIpAddress (str): This specifies the IP Address configured as destination VPLS Id IP Address when VPLS Id type is set as ipAddress.
			DestVplsIdIpAddressStep (str): This signifies the step of ip address by which the ip address will be incremented if there are multiple LSP/PW in the range.
			DestVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): This signifies the destination VplsId type.
			DmTimeFormat (str(ieee|ntp)): This signifies the DM Time Format. Possible values include IEEE and NTP.
			DmTrafficClass (number): This signifies the DM Traffic Class for LSP PW Range.
			DmType (str(ietf|y1731)): This signifies the DM Type. Possible values include IETF and Y.1731.
			EnableVlan (bool): If true, the MAC Traffic will have a vlan header.
			Enabled (bool): This signifies the enablement of this LSP PW Range.
			IpAddress (str): This signifies the IP address.
			IpAddressMask (number): This signifies the IP Address Mask.
			IpAddressStep (number): This signifies the IP Address Step Value.
			IpHostPerLsp (number): This signifies the total number of IP hosts per lsp.
			IpType (str(ipv4|ipv6)): This signifies the IP Type. Possible values include IPv4 and IPv6.
			LmCounterType (str(32Bit|64Bit)): This signifies the LM Counter Type. Possible values include 32 Bit and 64 Bit.
			LmInitialRxValue (number): This signifies the LM Initial Rx value for LSP PW Range.
			LmInitialTxValue (number): This signifies the LM Initial Tx value for LSP PW Range.
			LmRxStep (number): This signifies the LM Rx step value for LSP PW Range.
			LmTrafficClass (number): This signifies the LM Traffic Class.
			LmTxStep (number): This signifies the LM Tx Step value for LSP PW Range.
			LmType (str(ietf|y1731)): This signifies the LM Type. Possible values include IETF and Y.1731.
			LspIncomingLabel (number): This signifies the LSP Incoming label value. All mpls-tp packets are expected to be received with this LSP label value, if there is a mismatch of this value with the peer's outgoing LSP label value, cccv sessions will not come up.
			LspIncomingLabelStep (number): This signifies the LSP Incoming Label Step value.
			LspOutgoingLabel (number): This signifies the LSP Outgoing Label value. All mpls-tp packets are transmitted with this LSP label from the port.
			LspOutgoingLabelStep (number): This signifies the LSP Outgoing Label Step value.
			MacAddress (str): This signifies the starting MAC address of the range, this will be used for traffic generation.
			MacPerPw (number): This signifies the number of MACs behind each PW, these are the MACs that are used for traffic generation.
			MegIdIntegerStep (number): This signifies the MEG Id step value in integer.
			MegIdPrefix (str): This signifies the prefix for the MEG Id.
			MegLevel (number): This signifies the peer range of the nested LSP PW value.
			MinRxInterval (number): This signifies the CCCV minimum receive interval of cc messages, in milliseconds. Not valid for cccv type y1731.
			MinTxInterval (number): This signifies the CCCV minimum transmit interval of cc messages, in milliseconds. Valid for all types of cccv.
			NumberOfLsp (number): This signifies the total number of LSPs for this range.
			NumberOfPwPerLsp (number): This signifies the total number of PWs per LSP.
			OnDemandCvTrafficClass (number): This signifies the On Demand CV Traffic Class for LSP PW Range.
			PeerLspOrPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): This signifies the type of Peer LSP Or PW Range.
			PeerNestedLspPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): This signifies the peer range of the nested LSP PW value.
			PwIncomingLabel (number): This signifies the PW Incoming Label value. All mpls-tp packets are expected to be received with this PW label value, if there is a mismatch of this value with the peer's outgoing PW label value, cccv sessions will not come up.
			PwIncomingLabelStep (number): This signifies the PW Incoming Label Step value.
			PwIncomingLabelStepAcrossLsp (number): This signifies the PW Incoming Label Step value across LSPs.
			PwOutgoingLabel (number): This signifies the PW Outgoing Label value. All mpls-tp packets are transmitted with this PW label from the port.
			PwOutgoingLabelStep (number): This signifies the PW Outgoing Label Step value.
			PwOutgoingLabelStepAcrossLsp (number): This signifies the PW Outgoing Label Step value across LSPs.
			PwStatusFaultReplyInterval (number): This signifies the PW Status Fault Reply Interval in seconds.
			PwStatusTrafficClass (number): This signifies the PW Status Traffic Class for LSP PW Range.
			RangeRole (str(none|working|protect)): This signifies the role of the range. Possible values include None, Working and Protect.
			RepeatMac (bool): If true, and the Count is greater than 1, the same address value will be repeated for all MAC addresses within a PW.
			Revertive (bool): This signifies the switching mode, whether revertive or non-revertive.
			SkipZeroVlanId (bool): This signifies the VLAN Id 0 will not be used for any MAC.
			SrcAcId (number): This signifies the AC Id that is carried in the Echo Request message that is transmitted from this port.
			SrcAcIdStep (number): This signifies the source AC id step value.
			SrcGlobalId (number): This signifies the source global id. This is the global id that is carried in the Echo Request message that is transmitted from this port.
			SrcLspNumber (number): This signifies the lsp number that is carried in the Echo Request message that is transmitted from this port.
			SrcLspNumberStep (number): This signifies the source LSP Number step value.
			SrcMepId (number): This signifies the source MEP Id.
			SrcMepIdStep (number): This signifies the Source MEP Id step value in integer.
			SrcNodeId (number): This signifies the node id that is carried in the Echo Request message that is transmitted from this port.
			SrcTunnelNumber (number): This signifies the tunnel number that is carried in the Echo Request message that is transmitted from this port.
			SrcTunnelNumberStep (number): This signifies the source tunnel number step value.
			SrcVplsIdAsNumber (number): This signifies the AS Number configured as Source VPLS Id AS Number when VPLS Id type is set as asNumber or asNumber4Bytes. If it is asNumber then the max AS Number can be 65535 and when it is asNumber4Bytes the max value can be 4294967295.
			SrcVplsIdAsNumberStep (number): This signifies the step of AS number by which the number is incremented if there are multiple LSP/PW in the range.
			SrcVplsIdAssignedNumber (number): This signifies the source VPLS Id Assigned Number. If the VPLS Id type is configured as either ipAddress or asNumber4Bytes then the max Assigned Number can be 65535 and when it is asNumber the max value can be 4294967295.
			SrcVplsIdAssignedNumberStep (number): This specifies the step of Assigned number by which the number is incremented if there are multiple LSP/PW in the range.
			SrcVplsIdIpAddress (str): This signifies the IP Address configured as Source VPLS Id IP Address when VPLS Id type is set as ipAddress.
			SrcVplsIdIpAddressStep (str): This signifies the step of ip address by which it is incremented if there are multiple LSP/PW in the range.
			SrcVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): This specifies the source VplsId type.
			SupportSlowStart (bool): This signifies the Support Slow Start. This field is valid only for cccv type bfd and grayed out for y1731. If this is enabled then cccv interval for the peer is not matched for bfd session establishment.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): This signifies the Traffic Group Id.
			TypeOfProtectionSwitching (str(1+1Unidirectional|1:1Bidirectional|1+1Bidirectional)): This signifies different types of protection switching mechanism.
			TypeOfRange (str(lsp|pw|nestedLspPw)): This signifies the type of range. Possible values include LSP, PW and Nested PW and LSP.
			VlanCount (number): This signifies the number of VLANs configured for this MAC Range.
			VlanId (str): This signifies the VLAN option is enabled for the current MAC Range and a VLAN Id may be added to the packet, to identify the VLAN that the packet belongs to.
			VlanIncrementMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): This signifies the mode that defines how the VLAN will be incremented across MACs.
			VlanPriority (str): This signifies the user priority of the VLAN tag. This may have a value from 0 through 7.
			VlanTpId (str): This signifies the EtherType that identifies the protocol header that follows the VLAN header.
			WaitToRevertTime (number): This signifies the duration after which data traffic will be switched from protect to working path once working path has recovered from signal fail. This is configurable only if Revertive is checked.

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
			AlarmTrafficClass (number): This signifies the Alarm Traffic Class for LSP PW Range.
			AlarmType (str(ietf|y1731)): This signifies the Alarm Type. Possible values include IETF and Y.1731.
			ApsTrafficClass (number): This signifies the Traffic Class of the APS message.
			ApsType (str(ietf|y1731)): This signifies the APS type. Possible values include IETF and Y.1731.
			CccvInterval (number): This signifies the CCCV Interval in milliseconds.If cccv type is bfd then this field will take any value between 3-600000, if cccv type is y1731 then cccv interval can be configured to values available in the drop down menu.
			CccvTrafficClass (number): This signifies the CCCV Traffic Class.
			CccvType (str(bfdCc|bfdCccv|y1731|none)): This signifies the CCCV Type. Possible values include BFD CC, Y.1731 and None.
			Description (str): This signifies the description of the range.
			DestAcId (number): This signifies the destination AC id. This is the ac id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestAcIdStep (number): This signifies the destination AC id step value.
			DestGlobalId (number): This signifies the global id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestLspNumber (number): This signifies the lsp number that is expected on the peer, if there is a mismatch with the one configured on the peer LSP or PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestLspNumberStep (number): This signifies the source LSP Number step value.
			DestMepId (number): This signifies the destination MEP Id.
			DestMepIdStep (number): This signifies the Destination MEP Id step value in integer.
			DestNodeId (number): This signifies the destination node id. This is the node id that is expected on the peer, if there is a mismatch with the one configured on the peer LSP/PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestTunnelNumber (number): This signifies the tunnel number that is expected on the peer, if there is a mismatch with the one configured on the peer LSP or PW, On Demand Ping and On Demand Traceroute will result in failure.
			DestTunnelNumberStep (number): This signifies the destination tunnel number step value.
			DestVplsIdAsNumber (number): This signifies the AS Number configured as Source VPLS Id AS Number when VPLS Id type is set as asNumber or asNumber4Bytes. If it is asNumber then the max AS Number can be 65535 and when it is asNumber4Bytes the max value can be 4294967295.
			DestVplsIdAsNumberStep (number): This signifies the step of destination vpls id AS number by which the AS number will be incremented if there are multiple LSP/PW in the range.
			DestVplsIdAssignedNumber (number): This signifies the destination VPLS Id Assigned Number. If the VPLS Id type is configured as either ipAddress or asNumber4Bytes then the max Assigned Number can be 65535 and when it is asNumber, the max value can be 4294967295.
			DestVplsIdAssignedNumberStep (number): This signifies the step of Assigned number by which the number is incremented if there are multiple LSP/PW in the range.
			DestVplsIdIpAddress (str): This specifies the IP Address configured as destination VPLS Id IP Address when VPLS Id type is set as ipAddress.
			DestVplsIdIpAddressStep (str): This signifies the step of ip address by which the ip address will be incremented if there are multiple LSP/PW in the range.
			DestVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): This signifies the destination VplsId type.
			DmTimeFormat (str(ieee|ntp)): This signifies the DM Time Format. Possible values include IEEE and NTP.
			DmTrafficClass (number): This signifies the DM Traffic Class for LSP PW Range.
			DmType (str(ietf|y1731)): This signifies the DM Type. Possible values include IETF and Y.1731.
			EnableVlan (bool): If true, the MAC Traffic will have a vlan header.
			Enabled (bool): This signifies the enablement of this LSP PW Range.
			IpAddress (str): This signifies the IP address.
			IpAddressMask (number): This signifies the IP Address Mask.
			IpAddressStep (number): This signifies the IP Address Step Value.
			IpHostPerLsp (number): This signifies the total number of IP hosts per lsp.
			IpType (str(ipv4|ipv6)): This signifies the IP Type. Possible values include IPv4 and IPv6.
			LmCounterType (str(32Bit|64Bit)): This signifies the LM Counter Type. Possible values include 32 Bit and 64 Bit.
			LmInitialRxValue (number): This signifies the LM Initial Rx value for LSP PW Range.
			LmInitialTxValue (number): This signifies the LM Initial Tx value for LSP PW Range.
			LmRxStep (number): This signifies the LM Rx step value for LSP PW Range.
			LmTrafficClass (number): This signifies the LM Traffic Class.
			LmTxStep (number): This signifies the LM Tx Step value for LSP PW Range.
			LmType (str(ietf|y1731)): This signifies the LM Type. Possible values include IETF and Y.1731.
			LspIncomingLabel (number): This signifies the LSP Incoming label value. All mpls-tp packets are expected to be received with this LSP label value, if there is a mismatch of this value with the peer's outgoing LSP label value, cccv sessions will not come up.
			LspIncomingLabelStep (number): This signifies the LSP Incoming Label Step value.
			LspOutgoingLabel (number): This signifies the LSP Outgoing Label value. All mpls-tp packets are transmitted with this LSP label from the port.
			LspOutgoingLabelStep (number): This signifies the LSP Outgoing Label Step value.
			MacAddress (str): This signifies the starting MAC address of the range, this will be used for traffic generation.
			MacPerPw (number): This signifies the number of MACs behind each PW, these are the MACs that are used for traffic generation.
			MegIdIntegerStep (number): This signifies the MEG Id step value in integer.
			MegIdPrefix (str): This signifies the prefix for the MEG Id.
			MegLevel (number): This signifies the peer range of the nested LSP PW value.
			MinRxInterval (number): This signifies the CCCV minimum receive interval of cc messages, in milliseconds. Not valid for cccv type y1731.
			MinTxInterval (number): This signifies the CCCV minimum transmit interval of cc messages, in milliseconds. Valid for all types of cccv.
			NumberOfLsp (number): This signifies the total number of LSPs for this range.
			NumberOfPwPerLsp (number): This signifies the total number of PWs per LSP.
			OnDemandCvTrafficClass (number): This signifies the On Demand CV Traffic Class for LSP PW Range.
			PeerLspOrPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): This signifies the type of Peer LSP Or PW Range.
			PeerNestedLspPwRange (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=lspPwRange)): This signifies the peer range of the nested LSP PW value.
			PwIncomingLabel (number): This signifies the PW Incoming Label value. All mpls-tp packets are expected to be received with this PW label value, if there is a mismatch of this value with the peer's outgoing PW label value, cccv sessions will not come up.
			PwIncomingLabelStep (number): This signifies the PW Incoming Label Step value.
			PwIncomingLabelStepAcrossLsp (number): This signifies the PW Incoming Label Step value across LSPs.
			PwOutgoingLabel (number): This signifies the PW Outgoing Label value. All mpls-tp packets are transmitted with this PW label from the port.
			PwOutgoingLabelStep (number): This signifies the PW Outgoing Label Step value.
			PwOutgoingLabelStepAcrossLsp (number): This signifies the PW Outgoing Label Step value across LSPs.
			PwStatusFaultReplyInterval (number): This signifies the PW Status Fault Reply Interval in seconds.
			PwStatusTrafficClass (number): This signifies the PW Status Traffic Class for LSP PW Range.
			RangeRole (str(none|working|protect)): This signifies the role of the range. Possible values include None, Working and Protect.
			RepeatMac (bool): If true, and the Count is greater than 1, the same address value will be repeated for all MAC addresses within a PW.
			Revertive (bool): This signifies the switching mode, whether revertive or non-revertive.
			SkipZeroVlanId (bool): This signifies the VLAN Id 0 will not be used for any MAC.
			SrcAcId (number): This signifies the AC Id that is carried in the Echo Request message that is transmitted from this port.
			SrcAcIdStep (number): This signifies the source AC id step value.
			SrcGlobalId (number): This signifies the source global id. This is the global id that is carried in the Echo Request message that is transmitted from this port.
			SrcLspNumber (number): This signifies the lsp number that is carried in the Echo Request message that is transmitted from this port.
			SrcLspNumberStep (number): This signifies the source LSP Number step value.
			SrcMepId (number): This signifies the source MEP Id.
			SrcMepIdStep (number): This signifies the Source MEP Id step value in integer.
			SrcNodeId (number): This signifies the node id that is carried in the Echo Request message that is transmitted from this port.
			SrcTunnelNumber (number): This signifies the tunnel number that is carried in the Echo Request message that is transmitted from this port.
			SrcTunnelNumberStep (number): This signifies the source tunnel number step value.
			SrcVplsIdAsNumber (number): This signifies the AS Number configured as Source VPLS Id AS Number when VPLS Id type is set as asNumber or asNumber4Bytes. If it is asNumber then the max AS Number can be 65535 and when it is asNumber4Bytes the max value can be 4294967295.
			SrcVplsIdAsNumberStep (number): This signifies the step of AS number by which the number is incremented if there are multiple LSP/PW in the range.
			SrcVplsIdAssignedNumber (number): This signifies the source VPLS Id Assigned Number. If the VPLS Id type is configured as either ipAddress or asNumber4Bytes then the max Assigned Number can be 65535 and when it is asNumber the max value can be 4294967295.
			SrcVplsIdAssignedNumberStep (number): This specifies the step of Assigned number by which the number is incremented if there are multiple LSP/PW in the range.
			SrcVplsIdIpAddress (str): This signifies the IP Address configured as Source VPLS Id IP Address when VPLS Id type is set as ipAddress.
			SrcVplsIdIpAddressStep (str): This signifies the step of ip address by which it is incremented if there are multiple LSP/PW in the range.
			SrcVplsIdType (str(asNumber|ipAddress|asNumber4Bytes)): This specifies the source VplsId type.
			SupportSlowStart (bool): This signifies the Support Slow Start. This field is valid only for cccv type bfd and grayed out for y1731. If this is enabled then cccv interval for the peer is not matched for bfd session establishment.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): This signifies the Traffic Group Id.
			TypeOfProtectionSwitching (str(1+1Unidirectional|1:1Bidirectional|1+1Bidirectional)): This signifies different types of protection switching mechanism.
			TypeOfRange (str(lsp|pw|nestedLspPw)): This signifies the type of range. Possible values include LSP, PW and Nested PW and LSP.
			VlanCount (number): This signifies the number of VLANs configured for this MAC Range.
			VlanId (str): This signifies the VLAN option is enabled for the current MAC Range and a VLAN Id may be added to the packet, to identify the VLAN that the packet belongs to.
			VlanIncrementMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): This signifies the mode that defines how the VLAN will be incremented across MACs.
			VlanPriority (str): This signifies the user priority of the VLAN tag. This may have a value from 0 through 7.
			VlanTpId (str): This signifies the EtherType that identifies the protocol header that follows the VLAN header.
			WaitToRevertTime (number): This signifies the duration after which data traffic will be switched from protect to working path once working path has recovered from signal fail. This is configurable only if Revertive is checked.

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
