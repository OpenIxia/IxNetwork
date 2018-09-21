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
		"""The interval between AIS messages sent from this CFM bridge.

		Returns:
			str(oneSec|oneMin)
		"""
		return self._get_attribute('aisInterval')
	@AisInterval.setter
	def AisInterval(self, value):
		self._set_attribute('aisInterval', value)

	@property
	def AllowCfmMaidFormatsInY1731(self):
		"""If true, allows to use CFM's MD Name types and Short MA Name types when the Operation Mode is Y.1731.

		Returns:
			bool
		"""
		return self._get_attribute('allowCfmMaidFormatsInY1731')
	@AllowCfmMaidFormatsInY1731.setter
	def AllowCfmMaidFormatsInY1731(self, value):
		self._set_attribute('allowCfmMaidFormatsInY1731', value)

	@property
	def BridgeId(self):
		"""The bridge MAC address.

		Returns:
			str
		"""
		return self._get_attribute('bridgeId')
	@BridgeId.setter
	def BridgeId(self, value):
		self._set_attribute('bridgeId', value)

	@property
	def DelayLearnedErrorString(self):
		"""(read only) The learned error string for the delay measurement.

		Returns:
			str
		"""
		return self._get_attribute('delayLearnedErrorString')

	@property
	def EnableAis(self):
		"""If true, enables the use of AIS messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableAis')
	@EnableAis.setter
	def EnableAis(self, value):
		self._set_attribute('enableAis', value)

	@property
	def EnableOutOfSequenceDetection(self):
		"""If true, enables the detection of out of sequence CCM messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableOutOfSequenceDetection')
	@EnableOutOfSequenceDetection.setter
	def EnableOutOfSequenceDetection(self, value):
		self._set_attribute('enableOutOfSequenceDetection', value)

	@property
	def Enabled(self):
		"""If true, enables the CFM bridge.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Encapsulation(self):
		"""Sets the encapsulation type for the bridge.

		Returns:
			str(ethernet|llcSnap)
		"""
		return self._get_attribute('encapsulation')
	@Encapsulation.setter
	def Encapsulation(self, value):
		self._set_attribute('encapsulation', value)

	@property
	def EtherType(self):
		"""Selects the ether type for the bridge. The options are 0x8902 and 0x88E6.

		Returns:
			number
		"""
		return self._get_attribute('etherType')
	@EtherType.setter
	def EtherType(self, value):
		self._set_attribute('etherType', value)

	@property
	def Function(self):
		"""Determines the CFM function when operationMode is set to Y.1731.

		Returns:
			str(faultManagement|performanceMeasurement)
		"""
		return self._get_attribute('function')
	@Function.setter
	def Function(self, value):
		self._set_attribute('function', value)

	@property
	def GarbageCollectTime(self):
		"""Integer value denotes the interval for holding the expired database. Default 10 seconds.

		Returns:
			number
		"""
		return self._get_attribute('garbageCollectTime')
	@GarbageCollectTime.setter
	def GarbageCollectTime(self, value):
		self._set_attribute('garbageCollectTime', value)

	@property
	def IsAisLearnedInfoRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isAisLearnedInfoRefreshed')

	@property
	def IsCcmLearnedInfoRefreshed(self):
		"""(read only) If true, the CCM learned information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isCcmLearnedInfoRefreshed')

	@property
	def IsDelayLearnedConfigMep(self):
		"""(read only) If true, indicates if the configured MEP for the delay measurement was found.

		Returns:
			bool
		"""
		return self._get_attribute('isDelayLearnedConfigMep')

	@property
	def IsDelayLearnedPacketSent(self):
		"""(read only) If true, indicates the delay packet was sent.

		Returns:
			bool
		"""
		return self._get_attribute('isDelayLearnedPacketSent')

	@property
	def IsDelayMeasurementLearnedInfoRefreshed(self):
		"""(read only) If true, the learned delay information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isDelayMeasurementLearnedInfoRefreshed')

	@property
	def IsLbLearnedConfigMep(self):
		"""(read only) If true, indicates if the configured MEP for the loopback measurement was found.

		Returns:
			bool
		"""
		return self._get_attribute('isLbLearnedConfigMep')

	@property
	def IsLbLearnedPacketSent(self):
		"""(read only) If true, indicates the loopback packet was sent.

		Returns:
			bool
		"""
		return self._get_attribute('isLbLearnedPacketSent')

	@property
	def IsLckLearnedInfoRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isLckLearnedInfoRefreshed')

	@property
	def IsLinkTraceLearnedInfoRefreshed(self):
		"""(read only) If true, the learned link trace information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isLinkTraceLearnedInfoRefreshed')

	@property
	def IsLoopbackLearnedInfoRefreshed(self):
		"""(read only) If true, the learned loopback information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isLoopbackLearnedInfoRefreshed')

	@property
	def IsLossMeasurementLearnedInfoPacketSent(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isLossMeasurementLearnedInfoPacketSent')

	@property
	def IsLossMeasurementLearnedInfoRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isLossMeasurementLearnedInfoRefreshed')

	@property
	def IsLtLearnedConfigMep(self):
		"""(read only) If true, indicates if the configured MEP for the link trace measurement was found.

		Returns:
			bool
		"""
		return self._get_attribute('isLtLearnedConfigMep')

	@property
	def IsLtLearnedPacketSent(self):
		"""(read only) If true, indicates the link trace packet was sent.

		Returns:
			bool
		"""
		return self._get_attribute('isLtLearnedPacketSent')

	@property
	def IsPbbTeCcmLearnedInfoRefreshed(self):
		"""(read only) If true, the learned PBB-TE CCM information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeCcmLearnedInfoRefreshed')

	@property
	def IsPbbTeDelayLearnedConfigMep(self):
		"""(read only) If true, indicates if the configured MEP for the PBB-TE delay measurement was found.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeDelayLearnedConfigMep')

	@property
	def IsPbbTeDelayLearnedInfoRefreshed(self):
		"""(read only) If true, the learned PBB-TE delay information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeDelayLearnedInfoRefreshed')

	@property
	def IsPbbTeDelayLearnedPacketSent(self):
		"""(read only) If true, indicates the PBB-TE delay packet was sent.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeDelayLearnedPacketSent')

	@property
	def IsPbbTeLbLearnedConfigMep(self):
		"""(read only) If true, indicates if the configured MEP for the PBB-TE loopback measurement was found.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeLbLearnedConfigMep')

	@property
	def IsPbbTeLbLearnedInfoRefreshed(self):
		"""(read only) If true, the PBB-TE learned loopback information is current.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeLbLearnedInfoRefreshed')

	@property
	def IsPbbTeLbLearnedPacketSent(self):
		"""(read only) If true, indicates the PBB-TE loopback packet was sent.

		Returns:
			bool
		"""
		return self._get_attribute('isPbbTeLbLearnedPacketSent')

	@property
	def IsPeriodicOamLearnedInfoRefreshed(self):
		"""If true, the periodic OAM learned information is up-to-date.

		Returns:
			bool
		"""
		return self._get_attribute('isPeriodicOamLearnedInfoRefreshed')

	@property
	def IsTstLearnedInfoRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isTstLearnedInfoRefreshed')

	@property
	def LbLearnedErrorString(self):
		"""(read only) The learned error string for the loopback measurement.

		Returns:
			str
		"""
		return self._get_attribute('lbLearnedErrorString')

	@property
	def LossMeasurementLearnedInfoErrorString(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('lossMeasurementLearnedInfoErrorString')

	@property
	def LtLearnedErrorString(self):
		"""(read only) The learned error string for the link trace measurement.

		Returns:
			str
		"""
		return self._get_attribute('ltLearnedErrorString')

	@property
	def OperationMode(self):
		"""Selects the type of CFM to enable.

		Returns:
			str(cfm|y1731|pbbTe)
		"""
		return self._get_attribute('operationMode')
	@OperationMode.setter
	def OperationMode(self, value):
		self._set_attribute('operationMode', value)

	@property
	def PbbTeDelayLearnedErrorString(self):
		"""(read only) The learned error string for the PBB-TE delay measurement.

		Returns:
			str
		"""
		return self._get_attribute('pbbTeDelayLearnedErrorString')

	@property
	def PbbTeLbLearnedErrorString(self):
		"""(read only) The learned error string for the PBB-TE loopback measurement.

		Returns:
			str
		"""
		return self._get_attribute('pbbTeLbLearnedErrorString')

	@property
	def UserBvlan(self):
		"""Sets the bridge filter for PBB-TE learned information for the VLAN.

		Returns:
			str(noVlanId|vlanId|allVlanId)
		"""
		return self._get_attribute('userBvlan')
	@UserBvlan.setter
	def UserBvlan(self, value):
		self._set_attribute('userBvlan', value)

	@property
	def UserBvlanId(self):
		"""Sets the PBB-TE VLAN identifier for filtering learned information.

		Returns:
			number
		"""
		return self._get_attribute('userBvlanId')
	@UserBvlanId.setter
	def UserBvlanId(self, value):
		self._set_attribute('userBvlanId', value)

	@property
	def UserBvlanPriority(self):
		"""Sets the PBB-TE VLAN priority for filtering learned information.

		Returns:
			number
		"""
		return self._get_attribute('userBvlanPriority')
	@UserBvlanPriority.setter
	def UserBvlanPriority(self, value):
		self._set_attribute('userBvlanPriority', value)

	@property
	def UserBvlanTpId(self):
		"""Sets the PBB-TE VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('userBvlanTpId')
	@UserBvlanTpId.setter
	def UserBvlanTpId(self, value):
		self._set_attribute('userBvlanTpId', value)

	@property
	def UserCvlan(self):
		"""Sets the bridge filter for learned information for a single VLAN.

		Returns:
			str(noVlanId|vlanId|allVlanId)
		"""
		return self._get_attribute('userCvlan')
	@UserCvlan.setter
	def UserCvlan(self, value):
		self._set_attribute('userCvlan', value)

	@property
	def UserCvlanId(self):
		"""Sets the single VLAN identifier for filtering learned information.

		Returns:
			number
		"""
		return self._get_attribute('userCvlanId')
	@UserCvlanId.setter
	def UserCvlanId(self, value):
		self._set_attribute('userCvlanId', value)

	@property
	def UserCvlanPriority(self):
		"""Sets the single VLAN priority for filtering learned information.

		Returns:
			number
		"""
		return self._get_attribute('userCvlanPriority')
	@UserCvlanPriority.setter
	def UserCvlanPriority(self, value):
		self._set_attribute('userCvlanPriority', value)

	@property
	def UserCvlanTpId(self):
		"""Sets the single VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('userCvlanTpId')
	@UserCvlanTpId.setter
	def UserCvlanTpId(self, value):
		self._set_attribute('userCvlanTpId', value)

	@property
	def UserDelayMethod(self):
		"""Sets the type of delay method to use.

		Returns:
			str(oneWay|twoWay)
		"""
		return self._get_attribute('userDelayMethod')
	@UserDelayMethod.setter
	def UserDelayMethod(self, value):
		self._set_attribute('userDelayMethod', value)

	@property
	def UserDelayType(self):
		"""Sets the type of delay measurement to use.

		Returns:
			str(dm|dvm)
		"""
		return self._get_attribute('userDelayType')
	@UserDelayType.setter
	def UserDelayType(self, value):
		self._set_attribute('userDelayType', value)

	@property
	def UserDstMacAddress(self):
		"""Filters on the destination MAC address specified.

		Returns:
			str
		"""
		return self._get_attribute('userDstMacAddress')
	@UserDstMacAddress.setter
	def UserDstMacAddress(self, value):
		self._set_attribute('userDstMacAddress', value)

	@property
	def UserDstMepId(self):
		"""Sets the MEP identifier for use with userSelectDstMepById.

		Returns:
			number
		"""
		return self._get_attribute('userDstMepId')
	@UserDstMepId.setter
	def UserDstMepId(self, value):
		self._set_attribute('userDstMepId', value)

	@property
	def UserDstType(self):
		"""The user destination type.

		Returns:
			str(mepMac|mepId|mepMacAll|mepIdAll)
		"""
		return self._get_attribute('userDstType')
	@UserDstType.setter
	def UserDstType(self, value):
		self._set_attribute('userDstType', value)

	@property
	def UserLearnedInfoTimeOut(self):
		"""The interval in millisecond for the learned record to timeout. Default: 5000.

		Returns:
			number
		"""
		return self._get_attribute('userLearnedInfoTimeOut')
	@UserLearnedInfoTimeOut.setter
	def UserLearnedInfoTimeOut(self, value):
		self._set_attribute('userLearnedInfoTimeOut', value)

	@property
	def UserLossMethod(self):
		"""NOT DEFINED

		Returns:
			str(dualEnded|singleEnded)
		"""
		return self._get_attribute('userLossMethod')
	@UserLossMethod.setter
	def UserLossMethod(self, value):
		self._set_attribute('userLossMethod', value)

	@property
	def UserMdLevel(self):
		"""Filters on the specified MD level.

		Returns:
			str(0|1|2|3|4|5|6|7|allMd)
		"""
		return self._get_attribute('userMdLevel')
	@UserMdLevel.setter
	def UserMdLevel(self, value):
		self._set_attribute('userMdLevel', value)

	@property
	def UserPbbTeDelayMethod(self):
		"""Sets the PBB-TE type of delay method to use.

		Returns:
			str(twoWay|oneWay)
		"""
		return self._get_attribute('userPbbTeDelayMethod')
	@UserPbbTeDelayMethod.setter
	def UserPbbTeDelayMethod(self, value):
		self._set_attribute('userPbbTeDelayMethod', value)

	@property
	def UserPbbTeDelayType(self):
		"""Sets the PBB-TE type of delay measurement to use.

		Returns:
			str(dm|dvm)
		"""
		return self._get_attribute('userPbbTeDelayType')
	@UserPbbTeDelayType.setter
	def UserPbbTeDelayType(self, value):
		self._set_attribute('userPbbTeDelayType', value)

	@property
	def UserPeriodicOamType(self):
		"""Sets the type of periodic OAM.

		Returns:
			str(linkTrace|loopback|delayMeasurement|lossMeasurement)
		"""
		return self._get_attribute('userPeriodicOamType')
	@UserPeriodicOamType.setter
	def UserPeriodicOamType(self, value):
		self._set_attribute('userPeriodicOamType', value)

	@property
	def UserSelectDstMepById(self):
		"""If true, filters on the MEP by destination MEP identifier rather than by the MAC address. The MEP identifier is set in userDstMepId.

		Returns:
			bool
		"""
		return self._get_attribute('userSelectDstMepById')
	@UserSelectDstMepById.setter
	def UserSelectDstMepById(self, value):
		self._set_attribute('userSelectDstMepById', value)

	@property
	def UserSelectSrcMepById(self):
		"""If true, filters on the MEP by source MEP identifier rather than by the MAC address. The MEP identifier is set in userSrcMepId.

		Returns:
			bool
		"""
		return self._get_attribute('userSelectSrcMepById')
	@UserSelectSrcMepById.setter
	def UserSelectSrcMepById(self, value):
		self._set_attribute('userSelectSrcMepById', value)

	@property
	def UserSendType(self):
		"""Filters on the the send type.

		Returns:
			str(unicast|multicast)
		"""
		return self._get_attribute('userSendType')
	@UserSendType.setter
	def UserSendType(self, value):
		self._set_attribute('userSendType', value)

	@property
	def UserShortMaName(self):
		"""Filters on the specified Short MA Name.

		Returns:
			str
		"""
		return self._get_attribute('userShortMaName')
	@UserShortMaName.setter
	def UserShortMaName(self, value):
		self._set_attribute('userShortMaName', value)

	@property
	def UserShortMaNameFormat(self):
		"""Filters on the Short MA Name Format.

		Returns:
			str(allFormats|primaryVid|characterString|twoOctetInteger|rfc2685VpnId)
		"""
		return self._get_attribute('userShortMaNameFormat')
	@UserShortMaNameFormat.setter
	def UserShortMaNameFormat(self, value):
		self._set_attribute('userShortMaNameFormat', value)

	@property
	def UserSrcMacAddress(self):
		"""Filters on the specified source MAC address.

		Returns:
			str
		"""
		return self._get_attribute('userSrcMacAddress')
	@UserSrcMacAddress.setter
	def UserSrcMacAddress(self, value):
		self._set_attribute('userSrcMacAddress', value)

	@property
	def UserSrcMepId(self):
		"""Sets the MEP identifier for use with userSelectSrcMepById.

		Returns:
			number
		"""
		return self._get_attribute('userSrcMepId')
	@UserSrcMepId.setter
	def UserSrcMepId(self, value):
		self._set_attribute('userSrcMepId', value)

	@property
	def UserSrcType(self):
		"""The user source type.

		Returns:
			str(mepMac|mepId|mepMacAll|mepIdAll)
		"""
		return self._get_attribute('userSrcType')
	@UserSrcType.setter
	def UserSrcType(self, value):
		self._set_attribute('userSrcType', value)

	@property
	def UserSvlan(self):
		"""Sets the bridge filter for learned information for a stacked VLAN.

		Returns:
			str(noVlanId|vlanId|allVlanId)
		"""
		return self._get_attribute('userSvlan')
	@UserSvlan.setter
	def UserSvlan(self, value):
		self._set_attribute('userSvlan', value)

	@property
	def UserSvlanId(self):
		"""Sets the stacked VLAN identifier for filtering learned information.

		Returns:
			number
		"""
		return self._get_attribute('userSvlanId')
	@UserSvlanId.setter
	def UserSvlanId(self, value):
		self._set_attribute('userSvlanId', value)

	@property
	def UserSvlanPriority(self):
		"""Sets the stacked VLAN priority for filtering learned information.

		Returns:
			number
		"""
		return self._get_attribute('userSvlanPriority')
	@UserSvlanPriority.setter
	def UserSvlanPriority(self, value):
		self._set_attribute('userSvlanPriority', value)

	@property
	def UserSvlanTpId(self):
		"""Sets the stacked VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.

		Returns:
			str
		"""
		return self._get_attribute('userSvlanTpId')
	@UserSvlanTpId.setter
	def UserSvlanTpId(self, value):
		self._set_attribute('userSvlanTpId', value)

	@property
	def UserTransactionId(self):
		"""The transaction identifier for the LTM packet if the configured MEP not found. Default: 1.

		Returns:
			number
		"""
		return self._get_attribute('userTransactionId')
	@UserTransactionId.setter
	def UserTransactionId(self, value):
		self._set_attribute('userTransactionId', value)

	@property
	def UserTtlInterval(self):
		"""Time to live value, in seconds. Default is 64.

		Returns:
			number
		"""
		return self._get_attribute('userTtlInterval')
	@UserTtlInterval.setter
	def UserTtlInterval(self, value):
		self._set_attribute('userTtlInterval', value)

	@property
	def UserUsabilityOption(self):
		"""User Option, one of Manual, One-to-One, One-to-All, All-to-One, All-to-All.

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
			AisInterval (str(oneSec|oneMin)): The interval between AIS messages sent from this CFM bridge.
			AllowCfmMaidFormatsInY1731 (bool): If true, allows to use CFM's MD Name types and Short MA Name types when the Operation Mode is Y.1731.
			BridgeId (str): The bridge MAC address.
			EnableAis (bool): If true, enables the use of AIS messages.
			EnableOutOfSequenceDetection (bool): If true, enables the detection of out of sequence CCM messages.
			Enabled (bool): If true, enables the CFM bridge.
			Encapsulation (str(ethernet|llcSnap)): Sets the encapsulation type for the bridge.
			EtherType (number): Selects the ether type for the bridge. The options are 0x8902 and 0x88E6.
			Function (str(faultManagement|performanceMeasurement)): Determines the CFM function when operationMode is set to Y.1731.
			GarbageCollectTime (number): Integer value denotes the interval for holding the expired database. Default 10 seconds.
			OperationMode (str(cfm|y1731|pbbTe)): Selects the type of CFM to enable.
			UserBvlan (str(noVlanId|vlanId|allVlanId)): Sets the bridge filter for PBB-TE learned information for the VLAN.
			UserBvlanId (number): Sets the PBB-TE VLAN identifier for filtering learned information.
			UserBvlanPriority (number): Sets the PBB-TE VLAN priority for filtering learned information.
			UserBvlanTpId (str): Sets the PBB-TE VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.
			UserCvlan (str(noVlanId|vlanId|allVlanId)): Sets the bridge filter for learned information for a single VLAN.
			UserCvlanId (number): Sets the single VLAN identifier for filtering learned information.
			UserCvlanPriority (number): Sets the single VLAN priority for filtering learned information.
			UserCvlanTpId (str): Sets the single VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.
			UserDelayMethod (str(oneWay|twoWay)): Sets the type of delay method to use.
			UserDelayType (str(dm|dvm)): Sets the type of delay measurement to use.
			UserDstMacAddress (str): Filters on the destination MAC address specified.
			UserDstMepId (number): Sets the MEP identifier for use with userSelectDstMepById.
			UserDstType (str(mepMac|mepId|mepMacAll|mepIdAll)): The user destination type.
			UserLearnedInfoTimeOut (number): The interval in millisecond for the learned record to timeout. Default: 5000.
			UserLossMethod (str(dualEnded|singleEnded)): NOT DEFINED
			UserMdLevel (str(0|1|2|3|4|5|6|7|allMd)): Filters on the specified MD level.
			UserPbbTeDelayMethod (str(twoWay|oneWay)): Sets the PBB-TE type of delay method to use.
			UserPbbTeDelayType (str(dm|dvm)): Sets the PBB-TE type of delay measurement to use.
			UserPeriodicOamType (str(linkTrace|loopback|delayMeasurement|lossMeasurement)): Sets the type of periodic OAM.
			UserSelectDstMepById (bool): If true, filters on the MEP by destination MEP identifier rather than by the MAC address. The MEP identifier is set in userDstMepId.
			UserSelectSrcMepById (bool): If true, filters on the MEP by source MEP identifier rather than by the MAC address. The MEP identifier is set in userSrcMepId.
			UserSendType (str(unicast|multicast)): Filters on the the send type.
			UserShortMaName (str): Filters on the specified Short MA Name.
			UserShortMaNameFormat (str(allFormats|primaryVid|characterString|twoOctetInteger|rfc2685VpnId)): Filters on the Short MA Name Format.
			UserSrcMacAddress (str): Filters on the specified source MAC address.
			UserSrcMepId (number): Sets the MEP identifier for use with userSelectSrcMepById.
			UserSrcType (str(mepMac|mepId|mepMacAll|mepIdAll)): The user source type.
			UserSvlan (str(noVlanId|vlanId|allVlanId)): Sets the bridge filter for learned information for a stacked VLAN.
			UserSvlanId (number): Sets the stacked VLAN identifier for filtering learned information.
			UserSvlanPriority (number): Sets the stacked VLAN priority for filtering learned information.
			UserSvlanTpId (str): Sets the stacked VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.
			UserTransactionId (number): The transaction identifier for the LTM packet if the configured MEP not found. Default: 1.
			UserTtlInterval (number): Time to live value, in seconds. Default is 64.
			UserUsabilityOption (str(manual|oneToOne|oneToAll|allToOne|allToAll)): User Option, one of Manual, One-to-One, One-to-All, All-to-One, All-to-All.

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
			AisInterval (str(oneSec|oneMin)): The interval between AIS messages sent from this CFM bridge.
			AllowCfmMaidFormatsInY1731 (bool): If true, allows to use CFM's MD Name types and Short MA Name types when the Operation Mode is Y.1731.
			BridgeId (str): The bridge MAC address.
			DelayLearnedErrorString (str): (read only) The learned error string for the delay measurement.
			EnableAis (bool): If true, enables the use of AIS messages.
			EnableOutOfSequenceDetection (bool): If true, enables the detection of out of sequence CCM messages.
			Enabled (bool): If true, enables the CFM bridge.
			Encapsulation (str(ethernet|llcSnap)): Sets the encapsulation type for the bridge.
			EtherType (number): Selects the ether type for the bridge. The options are 0x8902 and 0x88E6.
			Function (str(faultManagement|performanceMeasurement)): Determines the CFM function when operationMode is set to Y.1731.
			GarbageCollectTime (number): Integer value denotes the interval for holding the expired database. Default 10 seconds.
			IsAisLearnedInfoRefreshed (bool): NOT DEFINED
			IsCcmLearnedInfoRefreshed (bool): (read only) If true, the CCM learned information is current.
			IsDelayLearnedConfigMep (bool): (read only) If true, indicates if the configured MEP for the delay measurement was found.
			IsDelayLearnedPacketSent (bool): (read only) If true, indicates the delay packet was sent.
			IsDelayMeasurementLearnedInfoRefreshed (bool): (read only) If true, the learned delay information is current.
			IsLbLearnedConfigMep (bool): (read only) If true, indicates if the configured MEP for the loopback measurement was found.
			IsLbLearnedPacketSent (bool): (read only) If true, indicates the loopback packet was sent.
			IsLckLearnedInfoRefreshed (bool): NOT DEFINED
			IsLinkTraceLearnedInfoRefreshed (bool): (read only) If true, the learned link trace information is current.
			IsLoopbackLearnedInfoRefreshed (bool): (read only) If true, the learned loopback information is current.
			IsLossMeasurementLearnedInfoPacketSent (bool): NOT DEFINED
			IsLossMeasurementLearnedInfoRefreshed (bool): NOT DEFINED
			IsLtLearnedConfigMep (bool): (read only) If true, indicates if the configured MEP for the link trace measurement was found.
			IsLtLearnedPacketSent (bool): (read only) If true, indicates the link trace packet was sent.
			IsPbbTeCcmLearnedInfoRefreshed (bool): (read only) If true, the learned PBB-TE CCM information is current.
			IsPbbTeDelayLearnedConfigMep (bool): (read only) If true, indicates if the configured MEP for the PBB-TE delay measurement was found.
			IsPbbTeDelayLearnedInfoRefreshed (bool): (read only) If true, the learned PBB-TE delay information is current.
			IsPbbTeDelayLearnedPacketSent (bool): (read only) If true, indicates the PBB-TE delay packet was sent.
			IsPbbTeLbLearnedConfigMep (bool): (read only) If true, indicates if the configured MEP for the PBB-TE loopback measurement was found.
			IsPbbTeLbLearnedInfoRefreshed (bool): (read only) If true, the PBB-TE learned loopback information is current.
			IsPbbTeLbLearnedPacketSent (bool): (read only) If true, indicates the PBB-TE loopback packet was sent.
			IsPeriodicOamLearnedInfoRefreshed (bool): If true, the periodic OAM learned information is up-to-date.
			IsTstLearnedInfoRefreshed (bool): NOT DEFINED
			LbLearnedErrorString (str): (read only) The learned error string for the loopback measurement.
			LossMeasurementLearnedInfoErrorString (str): NOT DEFINED
			LtLearnedErrorString (str): (read only) The learned error string for the link trace measurement.
			OperationMode (str(cfm|y1731|pbbTe)): Selects the type of CFM to enable.
			PbbTeDelayLearnedErrorString (str): (read only) The learned error string for the PBB-TE delay measurement.
			PbbTeLbLearnedErrorString (str): (read only) The learned error string for the PBB-TE loopback measurement.
			UserBvlan (str(noVlanId|vlanId|allVlanId)): Sets the bridge filter for PBB-TE learned information for the VLAN.
			UserBvlanId (number): Sets the PBB-TE VLAN identifier for filtering learned information.
			UserBvlanPriority (number): Sets the PBB-TE VLAN priority for filtering learned information.
			UserBvlanTpId (str): Sets the PBB-TE VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.
			UserCvlan (str(noVlanId|vlanId|allVlanId)): Sets the bridge filter for learned information for a single VLAN.
			UserCvlanId (number): Sets the single VLAN identifier for filtering learned information.
			UserCvlanPriority (number): Sets the single VLAN priority for filtering learned information.
			UserCvlanTpId (str): Sets the single VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.
			UserDelayMethod (str(oneWay|twoWay)): Sets the type of delay method to use.
			UserDelayType (str(dm|dvm)): Sets the type of delay measurement to use.
			UserDstMacAddress (str): Filters on the destination MAC address specified.
			UserDstMepId (number): Sets the MEP identifier for use with userSelectDstMepById.
			UserDstType (str(mepMac|mepId|mepMacAll|mepIdAll)): The user destination type.
			UserLearnedInfoTimeOut (number): The interval in millisecond for the learned record to timeout. Default: 5000.
			UserLossMethod (str(dualEnded|singleEnded)): NOT DEFINED
			UserMdLevel (str(0|1|2|3|4|5|6|7|allMd)): Filters on the specified MD level.
			UserPbbTeDelayMethod (str(twoWay|oneWay)): Sets the PBB-TE type of delay method to use.
			UserPbbTeDelayType (str(dm|dvm)): Sets the PBB-TE type of delay measurement to use.
			UserPeriodicOamType (str(linkTrace|loopback|delayMeasurement|lossMeasurement)): Sets the type of periodic OAM.
			UserSelectDstMepById (bool): If true, filters on the MEP by destination MEP identifier rather than by the MAC address. The MEP identifier is set in userDstMepId.
			UserSelectSrcMepById (bool): If true, filters on the MEP by source MEP identifier rather than by the MAC address. The MEP identifier is set in userSrcMepId.
			UserSendType (str(unicast|multicast)): Filters on the the send type.
			UserShortMaName (str): Filters on the specified Short MA Name.
			UserShortMaNameFormat (str(allFormats|primaryVid|characterString|twoOctetInteger|rfc2685VpnId)): Filters on the Short MA Name Format.
			UserSrcMacAddress (str): Filters on the specified source MAC address.
			UserSrcMepId (number): Sets the MEP identifier for use with userSelectSrcMepById.
			UserSrcType (str(mepMac|mepId|mepMacAll|mepIdAll)): The user source type.
			UserSvlan (str(noVlanId|vlanId|allVlanId)): Sets the bridge filter for learned information for a stacked VLAN.
			UserSvlanId (number): Sets the stacked VLAN identifier for filtering learned information.
			UserSvlanPriority (number): Sets the stacked VLAN priority for filtering learned information.
			UserSvlanTpId (str): Sets the stacked VLAN TPID for filtering learned information. One of 0x8100, 0x9100, 0x9200, or 0x88A8.
			UserTransactionId (number): The transaction identifier for the LTM packet if the configured MEP not found. Default: 1.
			UserTtlInterval (number): Time to live value, in seconds. Default is 64.
			UserUsabilityOption (str(manual|oneToOne|oneToAll|allToOne|allToAll)): User Option, one of Manual, One-to-One, One-to-All, All-to-One, All-to-All.

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

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshAisLearnedInfo', payload=locals(), response_object=None)

	def RefreshCcmLearnedInfo(self):
		"""Executes the refreshCcmLearnedInfo operation on the server.

		This command is used to refresh the learned CCM information on the bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshCcmLearnedInfo', payload=locals(), response_object=None)

	def RefreshLckLearnedInfo(self):
		"""Executes the refreshLckLearnedInfo operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLckLearnedInfo', payload=locals(), response_object=None)

	def RefreshTstLearnedInfo(self):
		"""Executes the refreshTstLearnedInfo operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshTstLearnedInfo', payload=locals(), response_object=None)

	def StartDelayMeasurement(self):
		"""Executes the startDelayMeasurement operation on the server.

		This command is used to refresh the learned CFM ITU information on this bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartDelayMeasurement', payload=locals(), response_object=None)

	def StartLinkTrace(self):
		"""Executes the startLinkTrace operation on the server.

		This command is used to refresh the learned CFM LT information on this bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartLinkTrace', payload=locals(), response_object=None)

	def StartLoopback(self):
		"""Executes the startLoopback operation on the server.

		This command is used to refresh the learned CFM LB information on this bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartLoopback', payload=locals(), response_object=None)

	def StartLossMeasurement(self):
		"""Executes the startLossMeasurement operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartLossMeasurement', payload=locals(), response_object=None)

	def UpdatePeriodicOamLearnedInfo(self):
		"""Executes the updatePeriodicOamLearnedInfo operation on the server.

		This command updates the periodic OAM learned information on this bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdatePeriodicOamLearnedInfo', payload=locals(), response_object=None)
