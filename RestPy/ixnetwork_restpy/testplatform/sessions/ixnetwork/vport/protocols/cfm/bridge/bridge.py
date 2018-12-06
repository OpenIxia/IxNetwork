
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


class Bridge(Base):
	"""The Bridge class encapsulates a user managed bridge node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bridge property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bridge'

	def __init__(self, parent):
		super(Bridge, self).__init__(parent)

	@property
	def AisLearnedInfo(self):
		"""An instance of the AisLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.aislearnedinfo.aislearnedinfo.AisLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.aislearnedinfo.aislearnedinfo import AisLearnedInfo
		return AisLearnedInfo(self)

	@property
	def CcmLearnedInfo(self):
		"""An instance of the CcmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.ccmlearnedinfo.ccmlearnedinfo.CcmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.ccmlearnedinfo.ccmlearnedinfo import CcmLearnedInfo
		return CcmLearnedInfo(self)

	@property
	def CustomTlvs(self):
		"""An instance of the CustomTlvs class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.customtlvs.customtlvs.CustomTlvs)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.customtlvs.customtlvs import CustomTlvs
		return CustomTlvs(self)

	@property
	def DelayLearnedInfo(self):
		"""An instance of the DelayLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.delaylearnedinfo.delaylearnedinfo.DelayLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.delaylearnedinfo.delaylearnedinfo import DelayLearnedInfo
		return DelayLearnedInfo(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.interface.interface import Interface
		return Interface(self)

	@property
	def LbLearnedInfo(self):
		"""An instance of the LbLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.lblearnedinfo.lblearnedinfo.LbLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.lblearnedinfo.lblearnedinfo import LbLearnedInfo
		return LbLearnedInfo(self)

	@property
	def LckLearnedInfo(self):
		"""An instance of the LckLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.lcklearnedinfo.lcklearnedinfo.LckLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.lcklearnedinfo.lcklearnedinfo import LckLearnedInfo
		return LckLearnedInfo(self)

	@property
	def Link(self):
		"""An instance of the Link class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.link.link.Link)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.link.link import Link
		return Link(self)

	@property
	def LossLearnedInfo(self):
		"""An instance of the LossLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.losslearnedinfo.losslearnedinfo.LossLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.losslearnedinfo.losslearnedinfo import LossLearnedInfo
		return LossLearnedInfo(self)

	@property
	def LtLearnedInfo(self):
		"""An instance of the LtLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.ltlearnedinfo.ltlearnedinfo.LtLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.ltlearnedinfo.ltlearnedinfo import LtLearnedInfo
		return LtLearnedInfo(self)

	@property
	def MdLevel(self):
		"""An instance of the MdLevel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.mdlevel.mdlevel.MdLevel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.mdlevel.mdlevel import MdLevel
		return MdLevel(self)

	@property
	def Mp(self):
		"""An instance of the Mp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.mp.mp.Mp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.mp.mp import Mp
		return Mp(self)

	@property
	def PbbTeCcmLearnedInfo(self):
		"""An instance of the PbbTeCcmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteccmlearnedinfo.pbbteccmlearnedinfo.PbbTeCcmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteccmlearnedinfo.pbbteccmlearnedinfo import PbbTeCcmLearnedInfo
		return PbbTeCcmLearnedInfo(self)

	@property
	def PbbTeDelayLearnedInfo(self):
		"""An instance of the PbbTeDelayLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbtedelaylearnedinfo.pbbtedelaylearnedinfo.PbbTeDelayLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbtedelaylearnedinfo.pbbtedelaylearnedinfo import PbbTeDelayLearnedInfo
		return PbbTeDelayLearnedInfo(self)

	@property
	def PbbTeLbLearnedInfo(self):
		"""An instance of the PbbTeLbLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbtelblearnedinfo.pbbtelblearnedinfo.PbbTeLbLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbtelblearnedinfo.pbbtelblearnedinfo import PbbTeLbLearnedInfo
		return PbbTeLbLearnedInfo(self)

	@property
	def PbbTeLtLearnedInfo(self):
		"""An instance of the PbbTeLtLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteltlearnedinfo.pbbteltlearnedinfo.PbbTeLtLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteltlearnedinfo.pbbteltlearnedinfo import PbbTeLtLearnedInfo
		return PbbTeLtLearnedInfo(self)

	@property
	def PbbTePeriodicOamDmLearnedInfo(self):
		"""An instance of the PbbTePeriodicOamDmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamdmlearnedinfo.pbbteperiodicoamdmlearnedinfo.PbbTePeriodicOamDmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamdmlearnedinfo.pbbteperiodicoamdmlearnedinfo import PbbTePeriodicOamDmLearnedInfo
		return PbbTePeriodicOamDmLearnedInfo(self)

	@property
	def PbbTePeriodicOamLbLearnedInfo(self):
		"""An instance of the PbbTePeriodicOamLbLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamlblearnedinfo.pbbteperiodicoamlblearnedinfo.PbbTePeriodicOamLbLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamlblearnedinfo.pbbteperiodicoamlblearnedinfo import PbbTePeriodicOamLbLearnedInfo
		return PbbTePeriodicOamLbLearnedInfo(self)

	@property
	def PbbTePeriodicOamLtLearnedInfo(self):
		"""An instance of the PbbTePeriodicOamLtLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamltlearnedinfo.pbbteperiodicoamltlearnedinfo.PbbTePeriodicOamLtLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.pbbteperiodicoamltlearnedinfo.pbbteperiodicoamltlearnedinfo import PbbTePeriodicOamLtLearnedInfo
		return PbbTePeriodicOamLtLearnedInfo(self)

	@property
	def PeriodicOamDmLearnedInfo(self):
		"""An instance of the PeriodicOamDmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamdmlearnedinfo.periodicoamdmlearnedinfo.PeriodicOamDmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamdmlearnedinfo.periodicoamdmlearnedinfo import PeriodicOamDmLearnedInfo
		return PeriodicOamDmLearnedInfo(self)

	@property
	def PeriodicOamLbLearnedInfo(self):
		"""An instance of the PeriodicOamLbLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamlblearnedinfo.periodicoamlblearnedinfo.PeriodicOamLbLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamlblearnedinfo.periodicoamlblearnedinfo import PeriodicOamLbLearnedInfo
		return PeriodicOamLbLearnedInfo(self)

	@property
	def PeriodicOamLmLearnedInfo(self):
		"""An instance of the PeriodicOamLmLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamlmlearnedinfo.periodicoamlmlearnedinfo.PeriodicOamLmLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamlmlearnedinfo.periodicoamlmlearnedinfo import PeriodicOamLmLearnedInfo
		return PeriodicOamLmLearnedInfo(self)

	@property
	def PeriodicOamLtLearnedInfo(self):
		"""An instance of the PeriodicOamLtLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamltlearnedinfo.periodicoamltlearnedinfo.PeriodicOamLtLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.periodicoamltlearnedinfo.periodicoamltlearnedinfo import PeriodicOamLtLearnedInfo
		return PeriodicOamLtLearnedInfo(self)

	@property
	def Trunk(self):
		"""An instance of the Trunk class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.trunk.trunk.Trunk)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.trunk.trunk import Trunk
		return Trunk(self)

	@property
	def TstLearnedInfo(self):
		"""An instance of the TstLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.tstlearnedinfo.tstlearnedinfo.TstLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.tstlearnedinfo.tstlearnedinfo import TstLearnedInfo
		return TstLearnedInfo(self)

	@property
	def Vlans(self):
		"""An instance of the Vlans class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.vlans.vlans.Vlans)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.cfm.bridge.vlans.vlans import Vlans
		return Vlans(self)

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
	def AllowCfmMaidFormatsInY1731(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('allowCfmMaidFormatsInY1731')
	@AllowCfmMaidFormatsInY1731.setter
	def AllowCfmMaidFormatsInY1731(self, value):
		self._set_attribute('allowCfmMaidFormatsInY1731', value)

	@property
	def BridgeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bridgeId')
	@BridgeId.setter
	def BridgeId(self, value):
		self._set_attribute('bridgeId', value)

	@property
	def DelayLearnedErrorString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('delayLearnedErrorString')

	@property
	def EnableAis(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAis')
	@EnableAis.setter
	def EnableAis(self, value):
		self._set_attribute('enableAis', value)

	@property
	def EnableOutOfSequenceDetection(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOutOfSequenceDetection')
	@EnableOutOfSequenceDetection.setter
	def EnableOutOfSequenceDetection(self, value):
		self._set_attribute('enableOutOfSequenceDetection', value)

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
	def Encapsulation(self):
		"""

		Returns:
			str(ethernet|llcSnap)
		"""
		return self._get_attribute('encapsulation')
	@Encapsulation.setter
	def Encapsulation(self, value):
		self._set_attribute('encapsulation', value)

	@property
	def EtherType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('etherType')
	@EtherType.setter
	def EtherType(self, value):
		self._set_attribute('etherType', value)

	@property
	def Function(self):
		"""

		Returns:
			str(faultManagement|performanceMeasurement)
		"""
		return self._get_attribute('function')
	@Function.setter
	def Function(self, value):
		self._set_attribute('function', value)

	@property
	def GarbageCollectTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('garbageCollectTime')
	@GarbageCollectTime.setter
	def GarbageCollectTime(self, value):
		self._set_attribute('garbageCollectTime', value)

	@property
	def IsAisLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isAisLearnedInfoRefreshed')

	@property
	def IsCcmLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isCcmLearnedInfoRefreshed')

	@property
	def IsDelayLearnedConfigMep(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDelayLearnedConfigMep')

	@property
	def IsDelayLearnedPacketSent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDelayLearnedPacketSent')

	@property
	def IsDelayMeasurementLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDelayMeasurementLearnedInfoRefreshed')

	@property
	def IsLbLearnedConfigMep(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLbLearnedConfigMep')

	@property
	def IsLbLearnedPacketSent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLbLearnedPacketSent')

	@property
	def IsLckLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLckLearnedInfoRefreshed')

	@property
	def IsLinkTraceLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLinkTraceLearnedInfoRefreshed')

	@property
	def IsLoopbackLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLoopbackLearnedInfoRefreshed')

	@property
	def IsLossMeasurementLearnedInfoPacketSent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLossMeasurementLearnedInfoPacketSent')

	@property
	def IsLossMeasurementLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLossMeasurementLearnedInfoRefreshed')

	@property
	def IsLtLearnedConfigMep(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLtLearnedConfigMep')

	@property
	def IsLtLearnedPacketSent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLtLearnedPacketSent')

	@property
	def IsPbbTeCcmLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeCcmLearnedInfoRefreshed')

	@property
	def IsPbbTeDelayLearnedConfigMep(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeDelayLearnedConfigMep')

	@property
	def IsPbbTeDelayLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeDelayLearnedInfoRefreshed')

	@property
	def IsPbbTeDelayLearnedPacketSent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeDelayLearnedPacketSent')

	@property
	def IsPbbTeLbLearnedConfigMep(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeLbLearnedConfigMep')

	@property
	def IsPbbTeLbLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeLbLearnedInfoRefreshed')

	@property
	def IsPbbTeLbLearnedPacketSent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeLbLearnedPacketSent')

	@property
	def IsPeriodicOamLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPeriodicOamLearnedInfoRefreshed')

	@property
	def IsTstLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isTstLearnedInfoRefreshed')

	@property
	def LbLearnedErrorString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lbLearnedErrorString')

	@property
	def LossMeasurementLearnedInfoErrorString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lossMeasurementLearnedInfoErrorString')

	@property
	def LtLearnedErrorString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ltLearnedErrorString')

	@property
	def OperationMode(self):
		"""

		Returns:
			str(cfm|y1731|pbbTe)
		"""
		return self._get_attribute('operationMode')
	@OperationMode.setter
	def OperationMode(self, value):
		self._set_attribute('operationMode', value)

	@property
	def PbbTeDelayLearnedErrorString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbTeDelayLearnedErrorString')

	@property
	def PbbTeLbLearnedErrorString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pbbTeLbLearnedErrorString')

	@property
	def UserBvlan(self):
		"""

		Returns:
			str(noVlanId|vlanId|allVlanId)
		"""
		return self._get_attribute('userBvlan')
	@UserBvlan.setter
	def UserBvlan(self, value):
		self._set_attribute('userBvlan', value)

	@property
	def UserBvlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userBvlanId')
	@UserBvlanId.setter
	def UserBvlanId(self, value):
		self._set_attribute('userBvlanId', value)

	@property
	def UserBvlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userBvlanPriority')
	@UserBvlanPriority.setter
	def UserBvlanPriority(self, value):
		self._set_attribute('userBvlanPriority', value)

	@property
	def UserBvlanTpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userBvlanTpId')
	@UserBvlanTpId.setter
	def UserBvlanTpId(self, value):
		self._set_attribute('userBvlanTpId', value)

	@property
	def UserCvlan(self):
		"""

		Returns:
			str(noVlanId|vlanId|allVlanId)
		"""
		return self._get_attribute('userCvlan')
	@UserCvlan.setter
	def UserCvlan(self, value):
		self._set_attribute('userCvlan', value)

	@property
	def UserCvlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userCvlanId')
	@UserCvlanId.setter
	def UserCvlanId(self, value):
		self._set_attribute('userCvlanId', value)

	@property
	def UserCvlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userCvlanPriority')
	@UserCvlanPriority.setter
	def UserCvlanPriority(self, value):
		self._set_attribute('userCvlanPriority', value)

	@property
	def UserCvlanTpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userCvlanTpId')
	@UserCvlanTpId.setter
	def UserCvlanTpId(self, value):
		self._set_attribute('userCvlanTpId', value)

	@property
	def UserDelayMethod(self):
		"""

		Returns:
			str(oneWay|twoWay)
		"""
		return self._get_attribute('userDelayMethod')
	@UserDelayMethod.setter
	def UserDelayMethod(self, value):
		self._set_attribute('userDelayMethod', value)

	@property
	def UserDelayType(self):
		"""

		Returns:
			str(dm|dvm)
		"""
		return self._get_attribute('userDelayType')
	@UserDelayType.setter
	def UserDelayType(self, value):
		self._set_attribute('userDelayType', value)

	@property
	def UserDstMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userDstMacAddress')
	@UserDstMacAddress.setter
	def UserDstMacAddress(self, value):
		self._set_attribute('userDstMacAddress', value)

	@property
	def UserDstMepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userDstMepId')
	@UserDstMepId.setter
	def UserDstMepId(self, value):
		self._set_attribute('userDstMepId', value)

	@property
	def UserDstType(self):
		"""

		Returns:
			str(mepMac|mepId|mepMacAll|mepIdAll)
		"""
		return self._get_attribute('userDstType')
	@UserDstType.setter
	def UserDstType(self, value):
		self._set_attribute('userDstType', value)

	@property
	def UserLearnedInfoTimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userLearnedInfoTimeOut')
	@UserLearnedInfoTimeOut.setter
	def UserLearnedInfoTimeOut(self, value):
		self._set_attribute('userLearnedInfoTimeOut', value)

	@property
	def UserLossMethod(self):
		"""

		Returns:
			str(dualEnded|singleEnded)
		"""
		return self._get_attribute('userLossMethod')
	@UserLossMethod.setter
	def UserLossMethod(self, value):
		self._set_attribute('userLossMethod', value)

	@property
	def UserMdLevel(self):
		"""

		Returns:
			str(0|1|2|3|4|5|6|7|allMd)
		"""
		return self._get_attribute('userMdLevel')
	@UserMdLevel.setter
	def UserMdLevel(self, value):
		self._set_attribute('userMdLevel', value)

	@property
	def UserPbbTeDelayMethod(self):
		"""

		Returns:
			str(twoWay|oneWay)
		"""
		return self._get_attribute('userPbbTeDelayMethod')
	@UserPbbTeDelayMethod.setter
	def UserPbbTeDelayMethod(self, value):
		self._set_attribute('userPbbTeDelayMethod', value)

	@property
	def UserPbbTeDelayType(self):
		"""

		Returns:
			str(dm|dvm)
		"""
		return self._get_attribute('userPbbTeDelayType')
	@UserPbbTeDelayType.setter
	def UserPbbTeDelayType(self, value):
		self._set_attribute('userPbbTeDelayType', value)

	@property
	def UserPeriodicOamType(self):
		"""

		Returns:
			str(linkTrace|loopback|delayMeasurement|lossMeasurement)
		"""
		return self._get_attribute('userPeriodicOamType')
	@UserPeriodicOamType.setter
	def UserPeriodicOamType(self, value):
		self._set_attribute('userPeriodicOamType', value)

	@property
	def UserSelectDstMepById(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('userSelectDstMepById')
	@UserSelectDstMepById.setter
	def UserSelectDstMepById(self, value):
		self._set_attribute('userSelectDstMepById', value)

	@property
	def UserSelectSrcMepById(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('userSelectSrcMepById')
	@UserSelectSrcMepById.setter
	def UserSelectSrcMepById(self, value):
		self._set_attribute('userSelectSrcMepById', value)

	@property
	def UserSendType(self):
		"""

		Returns:
			str(unicast|multicast)
		"""
		return self._get_attribute('userSendType')
	@UserSendType.setter
	def UserSendType(self, value):
		self._set_attribute('userSendType', value)

	@property
	def UserShortMaName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userShortMaName')
	@UserShortMaName.setter
	def UserShortMaName(self, value):
		self._set_attribute('userShortMaName', value)

	@property
	def UserShortMaNameFormat(self):
		"""

		Returns:
			str(allFormats|primaryVid|characterString|twoOctetInteger|rfc2685VpnId)
		"""
		return self._get_attribute('userShortMaNameFormat')
	@UserShortMaNameFormat.setter
	def UserShortMaNameFormat(self, value):
		self._set_attribute('userShortMaNameFormat', value)

	@property
	def UserSrcMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userSrcMacAddress')
	@UserSrcMacAddress.setter
	def UserSrcMacAddress(self, value):
		self._set_attribute('userSrcMacAddress', value)

	@property
	def UserSrcMepId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userSrcMepId')
	@UserSrcMepId.setter
	def UserSrcMepId(self, value):
		self._set_attribute('userSrcMepId', value)

	@property
	def UserSrcType(self):
		"""

		Returns:
			str(mepMac|mepId|mepMacAll|mepIdAll)
		"""
		return self._get_attribute('userSrcType')
	@UserSrcType.setter
	def UserSrcType(self, value):
		self._set_attribute('userSrcType', value)

	@property
	def UserSvlan(self):
		"""

		Returns:
			str(noVlanId|vlanId|allVlanId)
		"""
		return self._get_attribute('userSvlan')
	@UserSvlan.setter
	def UserSvlan(self, value):
		self._set_attribute('userSvlan', value)

	@property
	def UserSvlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userSvlanId')
	@UserSvlanId.setter
	def UserSvlanId(self, value):
		self._set_attribute('userSvlanId', value)

	@property
	def UserSvlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userSvlanPriority')
	@UserSvlanPriority.setter
	def UserSvlanPriority(self, value):
		self._set_attribute('userSvlanPriority', value)

	@property
	def UserSvlanTpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('userSvlanTpId')
	@UserSvlanTpId.setter
	def UserSvlanTpId(self, value):
		self._set_attribute('userSvlanTpId', value)

	@property
	def UserTransactionId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userTransactionId')
	@UserTransactionId.setter
	def UserTransactionId(self, value):
		self._set_attribute('userTransactionId', value)

	@property
	def UserTtlInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('userTtlInterval')
	@UserTtlInterval.setter
	def UserTtlInterval(self, value):
		self._set_attribute('userTtlInterval', value)

	@property
	def UserUsabilityOption(self):
		"""

		Returns:
			str(manual|oneToOne|oneToAll|allToOne|allToAll)
		"""
		return self._get_attribute('userUsabilityOption')
	@UserUsabilityOption.setter
	def UserUsabilityOption(self, value):
		self._set_attribute('userUsabilityOption', value)

	def add(self, AisInterval=None, AllowCfmMaidFormatsInY1731=None, BridgeId=None, EnableAis=None, EnableOutOfSequenceDetection=None, Enabled=None, Encapsulation=None, EtherType=None, Function=None, GarbageCollectTime=None, OperationMode=None, UserBvlan=None, UserBvlanId=None, UserBvlanPriority=None, UserBvlanTpId=None, UserCvlan=None, UserCvlanId=None, UserCvlanPriority=None, UserCvlanTpId=None, UserDelayMethod=None, UserDelayType=None, UserDstMacAddress=None, UserDstMepId=None, UserDstType=None, UserLearnedInfoTimeOut=None, UserLossMethod=None, UserMdLevel=None, UserPbbTeDelayMethod=None, UserPbbTeDelayType=None, UserPeriodicOamType=None, UserSelectDstMepById=None, UserSelectSrcMepById=None, UserSendType=None, UserShortMaName=None, UserShortMaNameFormat=None, UserSrcMacAddress=None, UserSrcMepId=None, UserSrcType=None, UserSvlan=None, UserSvlanId=None, UserSvlanPriority=None, UserSvlanTpId=None, UserTransactionId=None, UserTtlInterval=None, UserUsabilityOption=None):
		"""Adds a new bridge node on the server and retrieves it in this instance.

		Args:
			AisInterval (str(oneSec|oneMin)): 
			AllowCfmMaidFormatsInY1731 (bool): 
			BridgeId (str): 
			EnableAis (bool): 
			EnableOutOfSequenceDetection (bool): 
			Enabled (bool): 
			Encapsulation (str(ethernet|llcSnap)): 
			EtherType (number): 
			Function (str(faultManagement|performanceMeasurement)): 
			GarbageCollectTime (number): 
			OperationMode (str(cfm|y1731|pbbTe)): 
			UserBvlan (str(noVlanId|vlanId|allVlanId)): 
			UserBvlanId (number): 
			UserBvlanPriority (number): 
			UserBvlanTpId (str): 
			UserCvlan (str(noVlanId|vlanId|allVlanId)): 
			UserCvlanId (number): 
			UserCvlanPriority (number): 
			UserCvlanTpId (str): 
			UserDelayMethod (str(oneWay|twoWay)): 
			UserDelayType (str(dm|dvm)): 
			UserDstMacAddress (str): 
			UserDstMepId (number): 
			UserDstType (str(mepMac|mepId|mepMacAll|mepIdAll)): 
			UserLearnedInfoTimeOut (number): 
			UserLossMethod (str(dualEnded|singleEnded)): 
			UserMdLevel (str(0|1|2|3|4|5|6|7|allMd)): 
			UserPbbTeDelayMethod (str(twoWay|oneWay)): 
			UserPbbTeDelayType (str(dm|dvm)): 
			UserPeriodicOamType (str(linkTrace|loopback|delayMeasurement|lossMeasurement)): 
			UserSelectDstMepById (bool): 
			UserSelectSrcMepById (bool): 
			UserSendType (str(unicast|multicast)): 
			UserShortMaName (str): 
			UserShortMaNameFormat (str(allFormats|primaryVid|characterString|twoOctetInteger|rfc2685VpnId)): 
			UserSrcMacAddress (str): 
			UserSrcMepId (number): 
			UserSrcType (str(mepMac|mepId|mepMacAll|mepIdAll)): 
			UserSvlan (str(noVlanId|vlanId|allVlanId)): 
			UserSvlanId (number): 
			UserSvlanPriority (number): 
			UserSvlanTpId (str): 
			UserTransactionId (number): 
			UserTtlInterval (number): 
			UserUsabilityOption (str(manual|oneToOne|oneToAll|allToOne|allToAll)): 

		Returns:
			self: This instance with all currently retrieved bridge data using find and the newly added bridge data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bridge data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AisInterval=None, AllowCfmMaidFormatsInY1731=None, BridgeId=None, DelayLearnedErrorString=None, EnableAis=None, EnableOutOfSequenceDetection=None, Enabled=None, Encapsulation=None, EtherType=None, Function=None, GarbageCollectTime=None, IsAisLearnedInfoRefreshed=None, IsCcmLearnedInfoRefreshed=None, IsDelayLearnedConfigMep=None, IsDelayLearnedPacketSent=None, IsDelayMeasurementLearnedInfoRefreshed=None, IsLbLearnedConfigMep=None, IsLbLearnedPacketSent=None, IsLckLearnedInfoRefreshed=None, IsLinkTraceLearnedInfoRefreshed=None, IsLoopbackLearnedInfoRefreshed=None, IsLossMeasurementLearnedInfoPacketSent=None, IsLossMeasurementLearnedInfoRefreshed=None, IsLtLearnedConfigMep=None, IsLtLearnedPacketSent=None, IsPbbTeCcmLearnedInfoRefreshed=None, IsPbbTeDelayLearnedConfigMep=None, IsPbbTeDelayLearnedInfoRefreshed=None, IsPbbTeDelayLearnedPacketSent=None, IsPbbTeLbLearnedConfigMep=None, IsPbbTeLbLearnedInfoRefreshed=None, IsPbbTeLbLearnedPacketSent=None, IsPeriodicOamLearnedInfoRefreshed=None, IsTstLearnedInfoRefreshed=None, LbLearnedErrorString=None, LossMeasurementLearnedInfoErrorString=None, LtLearnedErrorString=None, OperationMode=None, PbbTeDelayLearnedErrorString=None, PbbTeLbLearnedErrorString=None, UserBvlan=None, UserBvlanId=None, UserBvlanPriority=None, UserBvlanTpId=None, UserCvlan=None, UserCvlanId=None, UserCvlanPriority=None, UserCvlanTpId=None, UserDelayMethod=None, UserDelayType=None, UserDstMacAddress=None, UserDstMepId=None, UserDstType=None, UserLearnedInfoTimeOut=None, UserLossMethod=None, UserMdLevel=None, UserPbbTeDelayMethod=None, UserPbbTeDelayType=None, UserPeriodicOamType=None, UserSelectDstMepById=None, UserSelectSrcMepById=None, UserSendType=None, UserShortMaName=None, UserShortMaNameFormat=None, UserSrcMacAddress=None, UserSrcMepId=None, UserSrcType=None, UserSvlan=None, UserSvlanId=None, UserSvlanPriority=None, UserSvlanTpId=None, UserTransactionId=None, UserTtlInterval=None, UserUsabilityOption=None):
		"""Finds and retrieves bridge data from the server.

		All named parameters support regex and can be used to selectively retrieve bridge data from the server.
		By default the find method takes no parameters and will retrieve all bridge data from the server.

		Args:
			AisInterval (str(oneSec|oneMin)): 
			AllowCfmMaidFormatsInY1731 (bool): 
			BridgeId (str): 
			DelayLearnedErrorString (str): 
			EnableAis (bool): 
			EnableOutOfSequenceDetection (bool): 
			Enabled (bool): 
			Encapsulation (str(ethernet|llcSnap)): 
			EtherType (number): 
			Function (str(faultManagement|performanceMeasurement)): 
			GarbageCollectTime (number): 
			IsAisLearnedInfoRefreshed (bool): 
			IsCcmLearnedInfoRefreshed (bool): 
			IsDelayLearnedConfigMep (bool): 
			IsDelayLearnedPacketSent (bool): 
			IsDelayMeasurementLearnedInfoRefreshed (bool): 
			IsLbLearnedConfigMep (bool): 
			IsLbLearnedPacketSent (bool): 
			IsLckLearnedInfoRefreshed (bool): 
			IsLinkTraceLearnedInfoRefreshed (bool): 
			IsLoopbackLearnedInfoRefreshed (bool): 
			IsLossMeasurementLearnedInfoPacketSent (bool): 
			IsLossMeasurementLearnedInfoRefreshed (bool): 
			IsLtLearnedConfigMep (bool): 
			IsLtLearnedPacketSent (bool): 
			IsPbbTeCcmLearnedInfoRefreshed (bool): 
			IsPbbTeDelayLearnedConfigMep (bool): 
			IsPbbTeDelayLearnedInfoRefreshed (bool): 
			IsPbbTeDelayLearnedPacketSent (bool): 
			IsPbbTeLbLearnedConfigMep (bool): 
			IsPbbTeLbLearnedInfoRefreshed (bool): 
			IsPbbTeLbLearnedPacketSent (bool): 
			IsPeriodicOamLearnedInfoRefreshed (bool): 
			IsTstLearnedInfoRefreshed (bool): 
			LbLearnedErrorString (str): 
			LossMeasurementLearnedInfoErrorString (str): 
			LtLearnedErrorString (str): 
			OperationMode (str(cfm|y1731|pbbTe)): 
			PbbTeDelayLearnedErrorString (str): 
			PbbTeLbLearnedErrorString (str): 
			UserBvlan (str(noVlanId|vlanId|allVlanId)): 
			UserBvlanId (number): 
			UserBvlanPriority (number): 
			UserBvlanTpId (str): 
			UserCvlan (str(noVlanId|vlanId|allVlanId)): 
			UserCvlanId (number): 
			UserCvlanPriority (number): 
			UserCvlanTpId (str): 
			UserDelayMethod (str(oneWay|twoWay)): 
			UserDelayType (str(dm|dvm)): 
			UserDstMacAddress (str): 
			UserDstMepId (number): 
			UserDstType (str(mepMac|mepId|mepMacAll|mepIdAll)): 
			UserLearnedInfoTimeOut (number): 
			UserLossMethod (str(dualEnded|singleEnded)): 
			UserMdLevel (str(0|1|2|3|4|5|6|7|allMd)): 
			UserPbbTeDelayMethod (str(twoWay|oneWay)): 
			UserPbbTeDelayType (str(dm|dvm)): 
			UserPeriodicOamType (str(linkTrace|loopback|delayMeasurement|lossMeasurement)): 
			UserSelectDstMepById (bool): 
			UserSelectSrcMepById (bool): 
			UserSendType (str(unicast|multicast)): 
			UserShortMaName (str): 
			UserShortMaNameFormat (str(allFormats|primaryVid|characterString|twoOctetInteger|rfc2685VpnId)): 
			UserSrcMacAddress (str): 
			UserSrcMepId (number): 
			UserSrcType (str(mepMac|mepId|mepMacAll|mepIdAll)): 
			UserSvlan (str(noVlanId|vlanId|allVlanId)): 
			UserSvlanId (number): 
			UserSvlanPriority (number): 
			UserSvlanTpId (str): 
			UserTransactionId (number): 
			UserTtlInterval (number): 
			UserUsabilityOption (str(manual|oneToOne|oneToAll|allToOne|allToAll)): 

		Returns:
			self: This instance with matching bridge data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bridge data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bridge data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshAisLearnedInfo(self):
		"""Executes the refreshAisLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshAisLearnedInfo', payload=locals(), response_object=None)

	def RefreshCcmLearnedInfo(self):
		"""Executes the refreshCcmLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshCcmLearnedInfo', payload=locals(), response_object=None)

	def RefreshLckLearnedInfo(self):
		"""Executes the refreshLckLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLckLearnedInfo', payload=locals(), response_object=None)

	def RefreshTstLearnedInfo(self):
		"""Executes the refreshTstLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshTstLearnedInfo', payload=locals(), response_object=None)

	def StartDelayMeasurement(self):
		"""Executes the startDelayMeasurement operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartDelayMeasurement', payload=locals(), response_object=None)

	def StartLinkTrace(self):
		"""Executes the startLinkTrace operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartLinkTrace', payload=locals(), response_object=None)

	def StartLoopback(self):
		"""Executes the startLoopback operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartLoopback', payload=locals(), response_object=None)

	def StartLossMeasurement(self):
		"""Executes the startLossMeasurement operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartLossMeasurement', payload=locals(), response_object=None)

	def UpdatePeriodicOamLearnedInfo(self):
		"""Executes the updatePeriodicOamLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdatePeriodicOamLearnedInfo', payload=locals(), response_object=None)
