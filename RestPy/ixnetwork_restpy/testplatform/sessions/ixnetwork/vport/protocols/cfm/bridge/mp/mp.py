
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


class Mp(Base):
	"""The Mp class encapsulates a user managed mp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Mp property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'mp'

	def __init__(self, parent):
		super(Mp, self).__init__(parent)

	@property
	def AddCcmCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addCcmCustomTlvs')
	@AddCcmCustomTlvs.setter
	def AddCcmCustomTlvs(self, value):
		self._set_attribute('addCcmCustomTlvs', value)

	@property
	def AddDataTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addDataTlv')
	@AddDataTlv.setter
	def AddDataTlv(self, value):
		self._set_attribute('addDataTlv', value)

	@property
	def AddInterfaceStatusTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addInterfaceStatusTlv')
	@AddInterfaceStatusTlv.setter
	def AddInterfaceStatusTlv(self, value):
		self._set_attribute('addInterfaceStatusTlv', value)

	@property
	def AddLbmCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addLbmCustomTlvs')
	@AddLbmCustomTlvs.setter
	def AddLbmCustomTlvs(self, value):
		self._set_attribute('addLbmCustomTlvs', value)

	@property
	def AddLbrCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addLbrCustomTlvs')
	@AddLbrCustomTlvs.setter
	def AddLbrCustomTlvs(self, value):
		self._set_attribute('addLbrCustomTlvs', value)

	@property
	def AddLmmCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addLmmCustomTlvs')
	@AddLmmCustomTlvs.setter
	def AddLmmCustomTlvs(self, value):
		self._set_attribute('addLmmCustomTlvs', value)

	@property
	def AddLmrCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addLmrCustomTlvs')
	@AddLmrCustomTlvs.setter
	def AddLmrCustomTlvs(self, value):
		self._set_attribute('addLmrCustomTlvs', value)

	@property
	def AddLtmCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addLtmCustomTlvs')
	@AddLtmCustomTlvs.setter
	def AddLtmCustomTlvs(self, value):
		self._set_attribute('addLtmCustomTlvs', value)

	@property
	def AddLtrCustomTlvs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addLtrCustomTlvs')
	@AddLtrCustomTlvs.setter
	def AddLtrCustomTlvs(self, value):
		self._set_attribute('addLtrCustomTlvs', value)

	@property
	def AddOrganizationSpecificTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addOrganizationSpecificTlv')
	@AddOrganizationSpecificTlv.setter
	def AddOrganizationSpecificTlv(self, value):
		self._set_attribute('addOrganizationSpecificTlv', value)

	@property
	def AddPortStatusTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addPortStatusTlv')
	@AddPortStatusTlv.setter
	def AddPortStatusTlv(self, value):
		self._set_attribute('addPortStatusTlv', value)

	@property
	def AddSenderIdTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('addSenderIdTlv')
	@AddSenderIdTlv.setter
	def AddSenderIdTlv(self, value):
		self._set_attribute('addSenderIdTlv', value)

	@property
	def AisEnableUnicastMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('aisEnableUnicastMac')
	@AisEnableUnicastMac.setter
	def AisEnableUnicastMac(self, value):
		self._set_attribute('aisEnableUnicastMac', value)

	@property
	def AisInterval(self):
		"""

		Returns:
			str(oneSec|oneMin)
		"""
		return self._get_attribute('aisInterval')
	@AisInterval.setter
	def AisInterval(self, value):
		self._set_attribute('aisInterval', value)

	@property
	def AisMode(self):
		"""

		Returns:
			str(auto|start|stop)
		"""
		return self._get_attribute('aisMode')
	@AisMode.setter
	def AisMode(self, value):
		self._set_attribute('aisMode', value)

	@property
	def AisPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('aisPriority')
	@AisPriority.setter
	def AisPriority(self, value):
		self._set_attribute('aisPriority', value)

	@property
	def AisUnicastMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('aisUnicastMac')
	@AisUnicastMac.setter
	def AisUnicastMac(self, value):
		self._set_attribute('aisUnicastMac', value)

	@property
	def AutoDmAllDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoDmAllDestination')
	@AutoDmAllDestination.setter
	def AutoDmAllDestination(self, value):
		self._set_attribute('autoDmAllDestination', value)

	@property
	def AutoDmDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('autoDmDestination')
	@AutoDmDestination.setter
	def AutoDmDestination(self, value):
		self._set_attribute('autoDmDestination', value)

	@property
	def AutoDmIteration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoDmIteration')
	@AutoDmIteration.setter
	def AutoDmIteration(self, value):
		self._set_attribute('autoDmIteration', value)

	@property
	def AutoDmTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoDmTimeout')
	@AutoDmTimeout.setter
	def AutoDmTimeout(self, value):
		self._set_attribute('autoDmTimeout', value)

	@property
	def AutoDmTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoDmTimer')
	@AutoDmTimer.setter
	def AutoDmTimer(self, value):
		self._set_attribute('autoDmTimer', value)

	@property
	def AutoLbAllDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoLbAllDestination')
	@AutoLbAllDestination.setter
	def AutoLbAllDestination(self, value):
		self._set_attribute('autoLbAllDestination', value)

	@property
	def AutoLbDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('autoLbDestination')
	@AutoLbDestination.setter
	def AutoLbDestination(self, value):
		self._set_attribute('autoLbDestination', value)

	@property
	def AutoLbIteration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLbIteration')
	@AutoLbIteration.setter
	def AutoLbIteration(self, value):
		self._set_attribute('autoLbIteration', value)

	@property
	def AutoLbTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLbTimeout')
	@AutoLbTimeout.setter
	def AutoLbTimeout(self, value):
		self._set_attribute('autoLbTimeout', value)

	@property
	def AutoLbTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLbTimer')
	@AutoLbTimer.setter
	def AutoLbTimer(self, value):
		self._set_attribute('autoLbTimer', value)

	@property
	def AutoLmIteration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLmIteration')
	@AutoLmIteration.setter
	def AutoLmIteration(self, value):
		self._set_attribute('autoLmIteration', value)

	@property
	def AutoLmTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLmTimeout')
	@AutoLmTimeout.setter
	def AutoLmTimeout(self, value):
		self._set_attribute('autoLmTimeout', value)

	@property
	def AutoLmTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLmTimer')
	@AutoLmTimer.setter
	def AutoLmTimer(self, value):
		self._set_attribute('autoLmTimer', value)

	@property
	def AutoLtAllDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoLtAllDestination')
	@AutoLtAllDestination.setter
	def AutoLtAllDestination(self, value):
		self._set_attribute('autoLtAllDestination', value)

	@property
	def AutoLtDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('autoLtDestination')
	@AutoLtDestination.setter
	def AutoLtDestination(self, value):
		self._set_attribute('autoLtDestination', value)

	@property
	def AutoLtIteration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLtIteration')
	@AutoLtIteration.setter
	def AutoLtIteration(self, value):
		self._set_attribute('autoLtIteration', value)

	@property
	def AutoLtTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLtTimeout')
	@AutoLtTimeout.setter
	def AutoLtTimeout(self, value):
		self._set_attribute('autoLtTimeout', value)

	@property
	def AutoLtTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('autoLtTimer')
	@AutoLtTimer.setter
	def AutoLtTimer(self, value):
		self._set_attribute('autoLtTimer', value)

	@property
	def CciInterval(self):
		"""

		Returns:
			str(3.33msec|10msec|100msec|1sec|10sec|1min|10min)
		"""
		return self._get_attribute('cciInterval')
	@CciInterval.setter
	def CciInterval(self, value):
		self._set_attribute('cciInterval', value)

	@property
	def CcmLmmTxFcf(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmLmmTxFcf')
	@CcmLmmTxFcf.setter
	def CcmLmmTxFcf(self, value):
		self._set_attribute('ccmLmmTxFcf', value)

	@property
	def CcmLmmTxFcfStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmLmmTxFcfStep')
	@CcmLmmTxFcfStep.setter
	def CcmLmmTxFcfStep(self, value):
		self._set_attribute('ccmLmmTxFcfStep', value)

	@property
	def CcmPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmPriority')
	@CcmPriority.setter
	def CcmPriority(self, value):
		self._set_attribute('ccmPriority', value)

	@property
	def CcmRxFcb(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmRxFcb')
	@CcmRxFcb.setter
	def CcmRxFcb(self, value):
		self._set_attribute('ccmRxFcb', value)

	@property
	def CcmRxFcbStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ccmRxFcbStep')
	@CcmRxFcbStep.setter
	def CcmRxFcbStep(self, value):
		self._set_attribute('ccmRxFcbStep', value)

	@property
	def ChassisId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('chassisId')
	@ChassisId.setter
	def ChassisId(self, value):
		self._set_attribute('chassisId', value)

	@property
	def ChassisIdLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('chassisIdLength')
	@ChassisIdLength.setter
	def ChassisIdLength(self, value):
		self._set_attribute('chassisIdLength', value)

	@property
	def ChassisIdSubType(self):
		"""

		Returns:
			str(chassisComponent|interfaceAlias|portComponent|macAddress|networkAddress|interfaceName|locallyAssigned)
		"""
		return self._get_attribute('chassisIdSubType')
	@ChassisIdSubType.setter
	def ChassisIdSubType(self, value):
		self._set_attribute('chassisIdSubType', value)

	@property
	def DataTlvLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataTlvLength')
	@DataTlvLength.setter
	def DataTlvLength(self, value):
		self._set_attribute('dataTlvLength', value)

	@property
	def DataTlvValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataTlvValue')
	@DataTlvValue.setter
	def DataTlvValue(self, value):
		self._set_attribute('dataTlvValue', value)

	@property
	def DmMethod(self):
		"""

		Returns:
			str(twoWay|oneWay)
		"""
		return self._get_attribute('dmMethod')
	@DmMethod.setter
	def DmMethod(self, value):
		self._set_attribute('dmMethod', value)

	@property
	def DmPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmPriority')
	@DmPriority.setter
	def DmPriority(self, value):
		self._set_attribute('dmPriority', value)

	@property
	def DmmPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmmPriority')
	@DmmPriority.setter
	def DmmPriority(self, value):
		self._set_attribute('dmmPriority', value)

	@property
	def EnableAisRx(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAisRx')
	@EnableAisRx.setter
	def EnableAisRx(self, value):
		self._set_attribute('enableAisRx', value)

	@property
	def EnableAutoDm(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoDm')
	@EnableAutoDm.setter
	def EnableAutoDm(self, value):
		self._set_attribute('enableAutoDm', value)

	@property
	def EnableAutoLb(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoLb')
	@EnableAutoLb.setter
	def EnableAutoLb(self, value):
		self._set_attribute('enableAutoLb', value)

	@property
	def EnableAutoLm(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoLm')
	@EnableAutoLm.setter
	def EnableAutoLm(self, value):
		self._set_attribute('enableAutoLm', value)

	@property
	def EnableAutoLt(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoLt')
	@EnableAutoLt.setter
	def EnableAutoLt(self, value):
		self._set_attribute('enableAutoLt', value)

	@property
	def EnableLckRx(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLckRx')
	@EnableLckRx.setter
	def EnableLckRx(self, value):
		self._set_attribute('enableLckRx', value)

	@property
	def EnableLmCounterUpdate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLmCounterUpdate')
	@EnableLmCounterUpdate.setter
	def EnableLmCounterUpdate(self, value):
		self._set_attribute('enableLmCounterUpdate', value)

	@property
	def EnableTstRx(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableTstRx')
	@EnableTstRx.setter
	def EnableTstRx(self, value):
		self._set_attribute('enableTstRx', value)

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
	def InterRemoteMepRxIncrementStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interRemoteMepRxIncrementStep')
	@InterRemoteMepRxIncrementStep.setter
	def InterRemoteMepRxIncrementStep(self, value):
		self._set_attribute('interRemoteMepRxIncrementStep', value)

	@property
	def InterRemoteMepTxIncrementStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interRemoteMepTxIncrementStep')
	@InterRemoteMepTxIncrementStep.setter
	def InterRemoteMepTxIncrementStep(self, value):
		self._set_attribute('interRemoteMepTxIncrementStep', value)

	@property
	def LbmPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lbmPriority')
	@LbmPriority.setter
	def LbmPriority(self, value):
		self._set_attribute('lbmPriority', value)

	@property
	def LckEnableUnicastMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('lckEnableUnicastMac')
	@LckEnableUnicastMac.setter
	def LckEnableUnicastMac(self, value):
		self._set_attribute('lckEnableUnicastMac', value)

	@property
	def LckInterval(self):
		"""

		Returns:
			str(oneSec|oneMin)
		"""
		return self._get_attribute('lckInterval')
	@LckInterval.setter
	def LckInterval(self, value):
		self._set_attribute('lckInterval', value)

	@property
	def LckMode(self):
		"""

		Returns:
			str(auto|start|stop)
		"""
		return self._get_attribute('lckMode')
	@LckMode.setter
	def LckMode(self, value):
		self._set_attribute('lckMode', value)

	@property
	def LckPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lckPriority')
	@LckPriority.setter
	def LckPriority(self, value):
		self._set_attribute('lckPriority', value)

	@property
	def LckSupportAisGeneration(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('lckSupportAisGeneration')
	@LckSupportAisGeneration.setter
	def LckSupportAisGeneration(self, value):
		self._set_attribute('lckSupportAisGeneration', value)

	@property
	def LckUnicastMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lckUnicastMac')
	@LckUnicastMac.setter
	def LckUnicastMac(self, value):
		self._set_attribute('lckUnicastMac', value)

	@property
	def LmAllRemoteMeps(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('lmAllRemoteMeps')
	@LmAllRemoteMeps.setter
	def LmAllRemoteMeps(self, value):
		self._set_attribute('lmAllRemoteMeps', value)

	@property
	def LmDestinationMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lmDestinationMacAddress')
	@LmDestinationMacAddress.setter
	def LmDestinationMacAddress(self, value):
		self._set_attribute('lmDestinationMacAddress', value)

	@property
	def LmMethod(self):
		"""

		Returns:
			str(singleEnded|dualEnded)
		"""
		return self._get_attribute('lmMethod')
	@LmMethod.setter
	def LmMethod(self, value):
		self._set_attribute('lmMethod', value)

	@property
	def LmmPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmmPriority')
	@LmmPriority.setter
	def LmmPriority(self, value):
		self._set_attribute('lmmPriority', value)

	@property
	def LmrPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmrPriority')
	@LmrPriority.setter
	def LmrPriority(self, value):
		self._set_attribute('lmrPriority', value)

	@property
	def LmrRxFcf(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmrRxFcf')
	@LmrRxFcf.setter
	def LmrRxFcf(self, value):
		self._set_attribute('lmrRxFcf', value)

	@property
	def LmrRxFcfStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lmrRxFcfStep')
	@LmrRxFcfStep.setter
	def LmrRxFcfStep(self, value):
		self._set_attribute('lmrRxFcfStep', value)

	@property
	def LtmPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ltmPriority')
	@LtmPriority.setter
	def LtmPriority(self, value):
		self._set_attribute('ltmPriority', value)

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
	def ManagementAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('managementAddress')
	@ManagementAddress.setter
	def ManagementAddress(self, value):
		self._set_attribute('managementAddress', value)

	@property
	def ManagementAddressDomain(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('managementAddressDomain')
	@ManagementAddressDomain.setter
	def ManagementAddressDomain(self, value):
		self._set_attribute('managementAddressDomain', value)

	@property
	def ManagementAddressDomainLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('managementAddressDomainLength')
	@ManagementAddressDomainLength.setter
	def ManagementAddressDomainLength(self, value):
		self._set_attribute('managementAddressDomainLength', value)

	@property
	def ManagementAddressLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('managementAddressLength')
	@ManagementAddressLength.setter
	def ManagementAddressLength(self, value):
		self._set_attribute('managementAddressLength', value)

	@property
	def MdLevel(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mdLevel)
		"""
		return self._get_attribute('mdLevel')
	@MdLevel.setter
	def MdLevel(self, value):
		self._set_attribute('mdLevel', value)

	@property
	def MegId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('megId')
	@MegId.setter
	def MegId(self, value):
		self._set_attribute('megId', value)

	@property
	def MegIdFormat(self):
		"""

		Returns:
			str(iccBasedFormat|primaryVid|characterString|2octetInteger|rfc2685VpnId)
		"""
		return self._get_attribute('megIdFormat')
	@MegIdFormat.setter
	def MegIdFormat(self, value):
		self._set_attribute('megIdFormat', value)

	@property
	def MepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mepId')
	@MepId.setter
	def MepId(self, value):
		self._set_attribute('mepId', value)

	@property
	def MipId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mipId')
	@MipId.setter
	def MipId(self, value):
		self._set_attribute('mipId', value)

	@property
	def MpType(self):
		"""

		Returns:
			str(mip|mep)
		"""
		return self._get_attribute('mpType')
	@MpType.setter
	def MpType(self, value):
		self._set_attribute('mpType', value)

	@property
	def OrganizationSpecificTlvLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('organizationSpecificTlvLength')
	@OrganizationSpecificTlvLength.setter
	def OrganizationSpecificTlvLength(self, value):
		self._set_attribute('organizationSpecificTlvLength', value)

	@property
	def OrganizationSpecificTlvValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('organizationSpecificTlvValue')
	@OrganizationSpecificTlvValue.setter
	def OrganizationSpecificTlvValue(self, value):
		self._set_attribute('organizationSpecificTlvValue', value)

	@property
	def OverrideVlanPriority(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideVlanPriority')
	@OverrideVlanPriority.setter
	def OverrideVlanPriority(self, value):
		self._set_attribute('overrideVlanPriority', value)

	@property
	def Rdi(self):
		"""

		Returns:
			str(auto|on|off)
		"""
		return self._get_attribute('rdi')
	@Rdi.setter
	def Rdi(self, value):
		self._set_attribute('rdi', value)

	@property
	def ShortMaName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('shortMaName')
	@ShortMaName.setter
	def ShortMaName(self, value):
		self._set_attribute('shortMaName', value)

	@property
	def ShortMaNameFormat(self):
		"""

		Returns:
			str(primaryVid|characterString|2octetInteger|rfc2685VpnId)
		"""
		return self._get_attribute('shortMaNameFormat')
	@ShortMaNameFormat.setter
	def ShortMaNameFormat(self, value):
		self._set_attribute('shortMaNameFormat', value)

	@property
	def TstEnableUnicastMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tstEnableUnicastMac')
	@TstEnableUnicastMac.setter
	def TstEnableUnicastMac(self, value):
		self._set_attribute('tstEnableUnicastMac', value)

	@property
	def TstIncrPacketLength(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tstIncrPacketLength')
	@TstIncrPacketLength.setter
	def TstIncrPacketLength(self, value):
		self._set_attribute('tstIncrPacketLength', value)

	@property
	def TstIncrPacketLengthStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tstIncrPacketLengthStep')
	@TstIncrPacketLengthStep.setter
	def TstIncrPacketLengthStep(self, value):
		self._set_attribute('tstIncrPacketLengthStep', value)

	@property
	def TstInitialPatternValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tstInitialPatternValue')
	@TstInitialPatternValue.setter
	def TstInitialPatternValue(self, value):
		self._set_attribute('tstInitialPatternValue', value)

	@property
	def TstInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tstInterval')
	@TstInterval.setter
	def TstInterval(self, value):
		self._set_attribute('tstInterval', value)

	@property
	def TstMode(self):
		"""

		Returns:
			str(start|stop)
		"""
		return self._get_attribute('tstMode')
	@TstMode.setter
	def TstMode(self, value):
		self._set_attribute('tstMode', value)

	@property
	def TstOverwriteSequenceNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tstOverwriteSequenceNumber')
	@TstOverwriteSequenceNumber.setter
	def TstOverwriteSequenceNumber(self, value):
		self._set_attribute('tstOverwriteSequenceNumber', value)

	@property
	def TstPacketLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tstPacketLength')
	@TstPacketLength.setter
	def TstPacketLength(self, value):
		self._set_attribute('tstPacketLength', value)

	@property
	def TstPatternType(self):
		"""

		Returns:
			str(nullSignalWithoutCrc32|nullSignalWithCrc32|prbs2311WithoutCrc32|prbs2311WithCrc32)
		"""
		return self._get_attribute('tstPatternType')
	@TstPatternType.setter
	def TstPatternType(self, value):
		self._set_attribute('tstPatternType', value)

	@property
	def TstPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tstPriority')
	@TstPriority.setter
	def TstPriority(self, value):
		self._set_attribute('tstPriority', value)

	@property
	def TstSequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tstSequenceNumber')
	@TstSequenceNumber.setter
	def TstSequenceNumber(self, value):
		self._set_attribute('tstSequenceNumber', value)

	@property
	def TstTestType(self):
		"""

		Returns:
			str(inService|outOfService)
		"""
		return self._get_attribute('tstTestType')
	@TstTestType.setter
	def TstTestType(self, value):
		self._set_attribute('tstTestType', value)

	@property
	def TstUnicastMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tstUnicastMac')
	@TstUnicastMac.setter
	def TstUnicastMac(self, value):
		self._set_attribute('tstUnicastMac', value)

	@property
	def Ttl(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ttl')
	@Ttl.setter
	def Ttl(self, value):
		self._set_attribute('ttl', value)

	@property
	def Vlan(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlans)
		"""
		return self._get_attribute('vlan')
	@Vlan.setter
	def Vlan(self, value):
		self._set_attribute('vlan', value)

	def add(self, AddCcmCustomTlvs=None, AddDataTlv=None, AddInterfaceStatusTlv=None, AddLbmCustomTlvs=None, AddLbrCustomTlvs=None, AddLmmCustomTlvs=None, AddLmrCustomTlvs=None, AddLtmCustomTlvs=None, AddLtrCustomTlvs=None, AddOrganizationSpecificTlv=None, AddPortStatusTlv=None, AddSenderIdTlv=None, AisEnableUnicastMac=None, AisInterval=None, AisMode=None, AisPriority=None, AisUnicastMac=None, AutoDmAllDestination=None, AutoDmDestination=None, AutoDmIteration=None, AutoDmTimeout=None, AutoDmTimer=None, AutoLbAllDestination=None, AutoLbDestination=None, AutoLbIteration=None, AutoLbTimeout=None, AutoLbTimer=None, AutoLmIteration=None, AutoLmTimeout=None, AutoLmTimer=None, AutoLtAllDestination=None, AutoLtDestination=None, AutoLtIteration=None, AutoLtTimeout=None, AutoLtTimer=None, CciInterval=None, CcmLmmTxFcf=None, CcmLmmTxFcfStep=None, CcmPriority=None, CcmRxFcb=None, CcmRxFcbStep=None, ChassisId=None, ChassisIdLength=None, ChassisIdSubType=None, DataTlvLength=None, DataTlvValue=None, DmMethod=None, DmPriority=None, DmmPriority=None, EnableAisRx=None, EnableAutoDm=None, EnableAutoLb=None, EnableAutoLm=None, EnableAutoLt=None, EnableLckRx=None, EnableLmCounterUpdate=None, EnableTstRx=None, Enabled=None, InterRemoteMepRxIncrementStep=None, InterRemoteMepTxIncrementStep=None, LbmPriority=None, LckEnableUnicastMac=None, LckInterval=None, LckMode=None, LckPriority=None, LckSupportAisGeneration=None, LckUnicastMac=None, LmAllRemoteMeps=None, LmDestinationMacAddress=None, LmMethod=None, LmmPriority=None, LmrPriority=None, LmrRxFcf=None, LmrRxFcfStep=None, LtmPriority=None, MacAddress=None, ManagementAddress=None, ManagementAddressDomain=None, ManagementAddressDomainLength=None, ManagementAddressLength=None, MdLevel=None, MegId=None, MegIdFormat=None, MepId=None, MipId=None, MpType=None, OrganizationSpecificTlvLength=None, OrganizationSpecificTlvValue=None, OverrideVlanPriority=None, Rdi=None, ShortMaName=None, ShortMaNameFormat=None, TstEnableUnicastMac=None, TstIncrPacketLength=None, TstIncrPacketLengthStep=None, TstInitialPatternValue=None, TstInterval=None, TstMode=None, TstOverwriteSequenceNumber=None, TstPacketLength=None, TstPatternType=None, TstPriority=None, TstSequenceNumber=None, TstTestType=None, TstUnicastMac=None, Ttl=None, Vlan=None):
		"""Adds a new mp node on the server and retrieves it in this instance.

		Args:
			AddCcmCustomTlvs (bool): 
			AddDataTlv (bool): 
			AddInterfaceStatusTlv (bool): 
			AddLbmCustomTlvs (bool): 
			AddLbrCustomTlvs (bool): 
			AddLmmCustomTlvs (bool): 
			AddLmrCustomTlvs (bool): 
			AddLtmCustomTlvs (bool): 
			AddLtrCustomTlvs (bool): 
			AddOrganizationSpecificTlv (bool): 
			AddPortStatusTlv (bool): 
			AddSenderIdTlv (bool): 
			AisEnableUnicastMac (bool): 
			AisInterval (str(oneSec|oneMin)): 
			AisMode (str(auto|start|stop)): 
			AisPriority (number): 
			AisUnicastMac (str): 
			AutoDmAllDestination (bool): 
			AutoDmDestination (str): 
			AutoDmIteration (number): 
			AutoDmTimeout (number): 
			AutoDmTimer (number): 
			AutoLbAllDestination (bool): 
			AutoLbDestination (str): 
			AutoLbIteration (number): 
			AutoLbTimeout (number): 
			AutoLbTimer (number): 
			AutoLmIteration (number): 
			AutoLmTimeout (number): 
			AutoLmTimer (number): 
			AutoLtAllDestination (bool): 
			AutoLtDestination (str): 
			AutoLtIteration (number): 
			AutoLtTimeout (number): 
			AutoLtTimer (number): 
			CciInterval (str(3.33msec|10msec|100msec|1sec|10sec|1min|10min)): 
			CcmLmmTxFcf (number): 
			CcmLmmTxFcfStep (number): 
			CcmPriority (number): 
			CcmRxFcb (number): 
			CcmRxFcbStep (number): 
			ChassisId (str): 
			ChassisIdLength (number): 
			ChassisIdSubType (str(chassisComponent|interfaceAlias|portComponent|macAddress|networkAddress|interfaceName|locallyAssigned)): 
			DataTlvLength (number): 
			DataTlvValue (str): 
			DmMethod (str(twoWay|oneWay)): 
			DmPriority (number): 
			DmmPriority (number): 
			EnableAisRx (bool): 
			EnableAutoDm (bool): 
			EnableAutoLb (bool): 
			EnableAutoLm (bool): 
			EnableAutoLt (bool): 
			EnableLckRx (bool): 
			EnableLmCounterUpdate (bool): 
			EnableTstRx (bool): 
			Enabled (bool): 
			InterRemoteMepRxIncrementStep (number): 
			InterRemoteMepTxIncrementStep (number): 
			LbmPriority (number): 
			LckEnableUnicastMac (bool): 
			LckInterval (str(oneSec|oneMin)): 
			LckMode (str(auto|start|stop)): 
			LckPriority (number): 
			LckSupportAisGeneration (bool): 
			LckUnicastMac (str): 
			LmAllRemoteMeps (bool): 
			LmDestinationMacAddress (str): 
			LmMethod (str(singleEnded|dualEnded)): 
			LmmPriority (number): 
			LmrPriority (number): 
			LmrRxFcf (number): 
			LmrRxFcfStep (number): 
			LtmPriority (number): 
			MacAddress (str): 
			ManagementAddress (str): 
			ManagementAddressDomain (str): 
			ManagementAddressDomainLength (number): 
			ManagementAddressLength (number): 
			MdLevel (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mdLevel)): 
			MegId (str): 
			MegIdFormat (str(iccBasedFormat|primaryVid|characterString|2octetInteger|rfc2685VpnId)): 
			MepId (number): 
			MipId (number): 
			MpType (str(mip|mep)): 
			OrganizationSpecificTlvLength (number): 
			OrganizationSpecificTlvValue (str): 
			OverrideVlanPriority (bool): 
			Rdi (str(auto|on|off)): 
			ShortMaName (str): 
			ShortMaNameFormat (str(primaryVid|characterString|2octetInteger|rfc2685VpnId)): 
			TstEnableUnicastMac (bool): 
			TstIncrPacketLength (bool): 
			TstIncrPacketLengthStep (number): 
			TstInitialPatternValue (number): 
			TstInterval (number): 
			TstMode (str(start|stop)): 
			TstOverwriteSequenceNumber (bool): 
			TstPacketLength (number): 
			TstPatternType (str(nullSignalWithoutCrc32|nullSignalWithCrc32|prbs2311WithoutCrc32|prbs2311WithCrc32)): 
			TstPriority (number): 
			TstSequenceNumber (number): 
			TstTestType (str(inService|outOfService)): 
			TstUnicastMac (str): 
			Ttl (number): 
			Vlan (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlans)): 

		Returns:
			self: This instance with all currently retrieved mp data using find and the newly added mp data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the mp data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddCcmCustomTlvs=None, AddDataTlv=None, AddInterfaceStatusTlv=None, AddLbmCustomTlvs=None, AddLbrCustomTlvs=None, AddLmmCustomTlvs=None, AddLmrCustomTlvs=None, AddLtmCustomTlvs=None, AddLtrCustomTlvs=None, AddOrganizationSpecificTlv=None, AddPortStatusTlv=None, AddSenderIdTlv=None, AisEnableUnicastMac=None, AisInterval=None, AisMode=None, AisPriority=None, AisUnicastMac=None, AutoDmAllDestination=None, AutoDmDestination=None, AutoDmIteration=None, AutoDmTimeout=None, AutoDmTimer=None, AutoLbAllDestination=None, AutoLbDestination=None, AutoLbIteration=None, AutoLbTimeout=None, AutoLbTimer=None, AutoLmIteration=None, AutoLmTimeout=None, AutoLmTimer=None, AutoLtAllDestination=None, AutoLtDestination=None, AutoLtIteration=None, AutoLtTimeout=None, AutoLtTimer=None, CciInterval=None, CcmLmmTxFcf=None, CcmLmmTxFcfStep=None, CcmPriority=None, CcmRxFcb=None, CcmRxFcbStep=None, ChassisId=None, ChassisIdLength=None, ChassisIdSubType=None, DataTlvLength=None, DataTlvValue=None, DmMethod=None, DmPriority=None, DmmPriority=None, EnableAisRx=None, EnableAutoDm=None, EnableAutoLb=None, EnableAutoLm=None, EnableAutoLt=None, EnableLckRx=None, EnableLmCounterUpdate=None, EnableTstRx=None, Enabled=None, InterRemoteMepRxIncrementStep=None, InterRemoteMepTxIncrementStep=None, LbmPriority=None, LckEnableUnicastMac=None, LckInterval=None, LckMode=None, LckPriority=None, LckSupportAisGeneration=None, LckUnicastMac=None, LmAllRemoteMeps=None, LmDestinationMacAddress=None, LmMethod=None, LmmPriority=None, LmrPriority=None, LmrRxFcf=None, LmrRxFcfStep=None, LtmPriority=None, MacAddress=None, ManagementAddress=None, ManagementAddressDomain=None, ManagementAddressDomainLength=None, ManagementAddressLength=None, MdLevel=None, MegId=None, MegIdFormat=None, MepId=None, MipId=None, MpType=None, OrganizationSpecificTlvLength=None, OrganizationSpecificTlvValue=None, OverrideVlanPriority=None, Rdi=None, ShortMaName=None, ShortMaNameFormat=None, TstEnableUnicastMac=None, TstIncrPacketLength=None, TstIncrPacketLengthStep=None, TstInitialPatternValue=None, TstInterval=None, TstMode=None, TstOverwriteSequenceNumber=None, TstPacketLength=None, TstPatternType=None, TstPriority=None, TstSequenceNumber=None, TstTestType=None, TstUnicastMac=None, Ttl=None, Vlan=None):
		"""Finds and retrieves mp data from the server.

		All named parameters support regex and can be used to selectively retrieve mp data from the server.
		By default the find method takes no parameters and will retrieve all mp data from the server.

		Args:
			AddCcmCustomTlvs (bool): 
			AddDataTlv (bool): 
			AddInterfaceStatusTlv (bool): 
			AddLbmCustomTlvs (bool): 
			AddLbrCustomTlvs (bool): 
			AddLmmCustomTlvs (bool): 
			AddLmrCustomTlvs (bool): 
			AddLtmCustomTlvs (bool): 
			AddLtrCustomTlvs (bool): 
			AddOrganizationSpecificTlv (bool): 
			AddPortStatusTlv (bool): 
			AddSenderIdTlv (bool): 
			AisEnableUnicastMac (bool): 
			AisInterval (str(oneSec|oneMin)): 
			AisMode (str(auto|start|stop)): 
			AisPriority (number): 
			AisUnicastMac (str): 
			AutoDmAllDestination (bool): 
			AutoDmDestination (str): 
			AutoDmIteration (number): 
			AutoDmTimeout (number): 
			AutoDmTimer (number): 
			AutoLbAllDestination (bool): 
			AutoLbDestination (str): 
			AutoLbIteration (number): 
			AutoLbTimeout (number): 
			AutoLbTimer (number): 
			AutoLmIteration (number): 
			AutoLmTimeout (number): 
			AutoLmTimer (number): 
			AutoLtAllDestination (bool): 
			AutoLtDestination (str): 
			AutoLtIteration (number): 
			AutoLtTimeout (number): 
			AutoLtTimer (number): 
			CciInterval (str(3.33msec|10msec|100msec|1sec|10sec|1min|10min)): 
			CcmLmmTxFcf (number): 
			CcmLmmTxFcfStep (number): 
			CcmPriority (number): 
			CcmRxFcb (number): 
			CcmRxFcbStep (number): 
			ChassisId (str): 
			ChassisIdLength (number): 
			ChassisIdSubType (str(chassisComponent|interfaceAlias|portComponent|macAddress|networkAddress|interfaceName|locallyAssigned)): 
			DataTlvLength (number): 
			DataTlvValue (str): 
			DmMethod (str(twoWay|oneWay)): 
			DmPriority (number): 
			DmmPriority (number): 
			EnableAisRx (bool): 
			EnableAutoDm (bool): 
			EnableAutoLb (bool): 
			EnableAutoLm (bool): 
			EnableAutoLt (bool): 
			EnableLckRx (bool): 
			EnableLmCounterUpdate (bool): 
			EnableTstRx (bool): 
			Enabled (bool): 
			InterRemoteMepRxIncrementStep (number): 
			InterRemoteMepTxIncrementStep (number): 
			LbmPriority (number): 
			LckEnableUnicastMac (bool): 
			LckInterval (str(oneSec|oneMin)): 
			LckMode (str(auto|start|stop)): 
			LckPriority (number): 
			LckSupportAisGeneration (bool): 
			LckUnicastMac (str): 
			LmAllRemoteMeps (bool): 
			LmDestinationMacAddress (str): 
			LmMethod (str(singleEnded|dualEnded)): 
			LmmPriority (number): 
			LmrPriority (number): 
			LmrRxFcf (number): 
			LmrRxFcfStep (number): 
			LtmPriority (number): 
			MacAddress (str): 
			ManagementAddress (str): 
			ManagementAddressDomain (str): 
			ManagementAddressDomainLength (number): 
			ManagementAddressLength (number): 
			MdLevel (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mdLevel)): 
			MegId (str): 
			MegIdFormat (str(iccBasedFormat|primaryVid|characterString|2octetInteger|rfc2685VpnId)): 
			MepId (number): 
			MipId (number): 
			MpType (str(mip|mep)): 
			OrganizationSpecificTlvLength (number): 
			OrganizationSpecificTlvValue (str): 
			OverrideVlanPriority (bool): 
			Rdi (str(auto|on|off)): 
			ShortMaName (str): 
			ShortMaNameFormat (str(primaryVid|characterString|2octetInteger|rfc2685VpnId)): 
			TstEnableUnicastMac (bool): 
			TstIncrPacketLength (bool): 
			TstIncrPacketLengthStep (number): 
			TstInitialPatternValue (number): 
			TstInterval (number): 
			TstMode (str(start|stop)): 
			TstOverwriteSequenceNumber (bool): 
			TstPacketLength (number): 
			TstPatternType (str(nullSignalWithoutCrc32|nullSignalWithCrc32|prbs2311WithoutCrc32|prbs2311WithCrc32)): 
			TstPriority (number): 
			TstSequenceNumber (number): 
			TstTestType (str(inService|outOfService)): 
			TstUnicastMac (str): 
			Ttl (number): 
			Vlan (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlans)): 

		Returns:
			self: This instance with matching mp data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of mp data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the mp data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
