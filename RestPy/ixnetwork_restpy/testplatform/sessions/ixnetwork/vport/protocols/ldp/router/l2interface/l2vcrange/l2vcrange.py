from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class L2VcRange(Base):
	"""The L2VcRange class encapsulates a user managed l2VcRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the L2VcRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'l2VcRange'

	def __init__(self, parent):
		super(L2VcRange, self).__init__(parent)

	@property
	def L2MacVlanRange(self):
		"""An instance of the L2MacVlanRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.l2interface.l2vcrange.l2macvlanrange.l2macvlanrange.L2MacVlanRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.l2interface.l2vcrange.l2macvlanrange.l2macvlanrange import L2MacVlanRange
		return L2MacVlanRange(self)._select()

	@property
	def L2VcIpRange(self):
		"""An instance of the L2VcIpRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.l2interface.l2vcrange.l2vciprange.l2vciprange.L2VcIpRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.l2interface.l2vcrange.l2vciprange.l2vciprange import L2VcIpRange
		return L2VcIpRange(self)._select()

	@property
	def CapableOfReassembly(self):
		"""If enabled, makes the interface capable of reassembly.

		Returns:
			bool
		"""
		return self._get_attribute('capableOfReassembly')
	@CapableOfReassembly.setter
	def CapableOfReassembly(self, value):
		self._set_attribute('capableOfReassembly', value)

	@property
	def Cas(self):
		"""It signifies the CAS value.

		Returns:
			str(e1Trunk|t1EsfTrunk|t1SfTrunk)
		"""
		return self._get_attribute('cas')
	@Cas.setter
	def Cas(self, value):
		self._set_attribute('cas', value)

	@property
	def CeIpAddress(self):
		"""The IP address of attached CE endpoint. If IP Type is set to Ipv4, then the default is 0.0.0.0, and if the IP type is set to Ipv6, then the default is 0:0:0:0:0:0:0:0.

		Returns:
			str
		"""
		return self._get_attribute('ceIpAddress')
	@CeIpAddress.setter
	def CeIpAddress(self, value):
		self._set_attribute('ceIpAddress', value)

	@property
	def CemOption(self):
		"""The value of the CEM option.

		Returns:
			number
		"""
		return self._get_attribute('cemOption')
	@CemOption.setter
	def CemOption(self, value):
		self._set_attribute('cemOption', value)

	@property
	def CemPayload(self):
		"""If enabled, indicates that there is a Circuit Emulation Service over MPLS (CEM) payload.

		Returns:
			number
		"""
		return self._get_attribute('cemPayload')
	@CemPayload.setter
	def CemPayload(self, value):
		self._set_attribute('cemPayload', value)

	@property
	def Count(self):
		"""(In octets) The 8-bit VC information Length field. It indicates the length of the (2-octet) VC ID field plus combined length of all of the parameters in the VC FEC element.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Description(self):
		"""An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DoNotExpandIntoVcs(self):
		"""If true, the VC ranges do not expand into individual VCs.

		Returns:
			bool
		"""
		return self._get_attribute('doNotExpandIntoVcs')
	@DoNotExpandIntoVcs.setter
	def DoNotExpandIntoVcs(self, value):
		self._set_attribute('doNotExpandIntoVcs', value)

	@property
	def DownInterval(self):
		"""Time interval for which the PW status will remain down. (Default= 60 seconds)

		Returns:
			number
		"""
		return self._get_attribute('downInterval')
	@DownInterval.setter
	def DownInterval(self, value):
		self._set_attribute('downInterval', value)

	@property
	def DownStartInterval(self):
		"""The duration in time after session becomes up and a notification message being sent to make the session down. (Default= 30 seconds)

		Returns:
			number
		"""
		return self._get_attribute('downStartInterval')
	@DownStartInterval.setter
	def DownStartInterval(self, value):
		self._set_attribute('downStartInterval', value)

	@property
	def EnableBfdIpUdpCv(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdIpUdpCv')
	@EnableBfdIpUdpCv.setter
	def EnableBfdIpUdpCv(self, value):
		self._set_attribute('enableBfdIpUdpCv', value)

	@property
	def EnableBfdPwAchCv(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdPwAchCv')
	@EnableBfdPwAchCv.setter
	def EnableBfdPwAchCv(self, value):
		self._set_attribute('enableBfdPwAchCv', value)

	@property
	def EnableCBit(self):
		"""Controls generation of the control word.

		Returns:
			bool
		"""
		return self._get_attribute('enableCBit')
	@EnableCBit.setter
	def EnableCBit(self, value):
		self._set_attribute('enableCBit', value)

	@property
	def EnableCccvNegotiation(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableCccvNegotiation')
	@EnableCccvNegotiation.setter
	def EnableCccvNegotiation(self, value):
		self._set_attribute('enableCccvNegotiation', value)

	@property
	def EnableCemOption(self):
		"""Enable the Circuit Emulation over MPLS option, for encapsulation of TDM signals.

		Returns:
			bool
		"""
		return self._get_attribute('enableCemOption')
	@EnableCemOption.setter
	def EnableCemOption(self, value):
		self._set_attribute('enableCemOption', value)

	@property
	def EnableCemPayload(self):
		"""Enable the Circuit Emulation over MPLS payload.

		Returns:
			bool
		"""
		return self._get_attribute('enableCemPayload')
	@EnableCemPayload.setter
	def EnableCemPayload(self, value):
		self._set_attribute('enableCemPayload', value)

	@property
	def EnableDescriptionPresent(self):
		"""If enabled, indicates that an optional interface description is present.

		Returns:
			bool
		"""
		return self._get_attribute('enableDescriptionPresent')
	@EnableDescriptionPresent.setter
	def EnableDescriptionPresent(self, value):
		self._set_attribute('enableDescriptionPresent', value)

	@property
	def EnableLspPingCv(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPingCv')
	@EnableLspPingCv.setter
	def EnableLspPingCv(self, value):
		self._set_attribute('enableLspPingCv', value)

	@property
	def EnableMaxAtmPresent(self):
		"""Enables the generation of an interface parameter field with the maximum number of concatenated ATM cells. (default = 0)

		Returns:
			bool
		"""
		return self._get_attribute('enableMaxAtmPresent')
	@EnableMaxAtmPresent.setter
	def EnableMaxAtmPresent(self, value):
		self._set_attribute('enableMaxAtmPresent', value)

	@property
	def EnableMtuPresent(self):
		"""This attribute enables the generation of an MTU interface parameter field.

		Returns:
			bool
		"""
		return self._get_attribute('enableMtuPresent')
	@EnableMtuPresent.setter
	def EnableMtuPresent(self, value):
		self._set_attribute('enableMtuPresent', value)

	@property
	def EnablePacking(self):
		"""(For L2 VC FEC ranges and in Unsolicited Label Distribution Mode ONLY.) If enabled, L2 VC FEC ranges will be aggregated within a single LDP PDU to conserve bandwidth and processing.

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def EnablePwAchCc(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enablePwAchCc')
	@EnablePwAchCc.setter
	def EnablePwAchCc(self, value):
		self._set_attribute('enablePwAchCc', value)

	@property
	def EnablePwStatusTlv(self):
		"""If checked, this enables the use of PW status TLV in notification messages to notify the PW status.

		Returns:
			bool
		"""
		return self._get_attribute('enablePwStatusTlv')
	@EnablePwStatusTlv.setter
	def EnablePwStatusTlv(self, value):
		self._set_attribute('enablePwStatusTlv', value)

	@property
	def EnableRouterAlertCc(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableRouterAlertCc')
	@EnableRouterAlertCc.setter
	def EnableRouterAlertCc(self, value):
		self._set_attribute('enableRouterAlertCc', value)

	@property
	def Enabled(self):
		"""Enables use of this VC range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FecType(self):
		"""The FEC type. The options are: PW Id FEC 0x80, Generalized Id FEC 0x81 VPLS.

		Returns:
			str(pwIdFec|generalizedIdFecVpls)
		"""
		return self._get_attribute('fecType')
	@FecType.setter
	def FecType(self, value):
		self._set_attribute('fecType', value)

	@property
	def Frequency(self):
		"""It is the frequency.

		Returns:
			number
		"""
		return self._get_attribute('frequency')
	@Frequency.setter
	def Frequency(self, value):
		self._set_attribute('frequency', value)

	@property
	def IncludeRtpHeader(self):
		"""If true, includes the RTP header.

		Returns:
			bool
		"""
		return self._get_attribute('includeRtpHeader')
	@IncludeRtpHeader.setter
	def IncludeRtpHeader(self, value):
		self._set_attribute('includeRtpHeader', value)

	@property
	def IncludeSsrc(self):
		"""If true, enables SSRC.

		Returns:
			bool
		"""
		return self._get_attribute('includeSsrc')
	@IncludeSsrc.setter
	def IncludeSsrc(self, value):
		self._set_attribute('includeSsrc', value)

	@property
	def IncludeTdmBitrate(self):
		"""If true, enables TDM bit rate.

		Returns:
			bool
		"""
		return self._get_attribute('includeTdmBitrate')
	@IncludeTdmBitrate.setter
	def IncludeTdmBitrate(self, value):
		self._set_attribute('includeTdmBitrate', value)

	@property
	def IncludeTdmOption(self):
		"""If true, includes the TDM option.

		Returns:
			bool
		"""
		return self._get_attribute('includeTdmOption')
	@IncludeTdmOption.setter
	def IncludeTdmOption(self, value):
		self._set_attribute('includeTdmOption', value)

	@property
	def IncludeTdmPayload(self):
		"""If true, enables TDM payload.

		Returns:
			bool
		"""
		return self._get_attribute('includeTdmPayload')
	@IncludeTdmPayload.setter
	def IncludeTdmPayload(self, value):
		self._set_attribute('includeTdmPayload', value)

	@property
	def IpType(self):
		"""The type (IPv4 or IPv6) of the neighbor.

		Returns:
			number
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def LabelMode(self):
		"""Indicates whether the same label or incrementing labels should be used in the VC ranges.

		Returns:
			str(none|increment)
		"""
		return self._get_attribute('labelMode')
	@LabelMode.setter
	def LabelMode(self, value):
		self._set_attribute('labelMode', value)

	@property
	def LabelStart(self):
		"""The first label in the range of labels. The default is 16.

		Returns:
			number
		"""
		return self._get_attribute('labelStart')
	@LabelStart.setter
	def LabelStart(self, value):
		self._set_attribute('labelStart', value)

	@property
	def MaxNumberOfAtmCells(self):
		"""The maximum number of ATM cells which may be concatenated and sent in a single MPLS frame. This parameter is part of the FEC element.

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfAtmCells')
	@MaxNumberOfAtmCells.setter
	def MaxNumberOfAtmCells(self, value):
		self._set_attribute('maxNumberOfAtmCells', value)

	@property
	def Mtu(self):
		"""(in octets) The 2-octet value for the maximum Transmission Unit (MTU).

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def PayloadType(self):
		"""It is the payload type.

		Returns:
			number
		"""
		return self._get_attribute('payloadType')
	@PayloadType.setter
	def PayloadType(self, value):
		self._set_attribute('payloadType', value)

	@property
	def PeerAddress(self):
		"""The IPv4 address of the LDP router which is the peer for this VC range.

		Returns:
			str
		"""
		return self._get_attribute('peerAddress')
	@PeerAddress.setter
	def PeerAddress(self, value):
		self._set_attribute('peerAddress', value)

	@property
	def ProvisioningModel(self):
		"""Editable dropdown to denote the Provisioning Model.

		Returns:
			str(manualConfiguration|bgpAutoDiscovery)
		"""
		return self._get_attribute('provisioningModel')
	@ProvisioningModel.setter
	def ProvisioningModel(self, value):
		self._set_attribute('provisioningModel', value)

	@property
	def PwStatusCode(self):
		"""This is an editable dropdown to denote the PW status. This field is editable. The range is from 0x00000001 - 0xFFFFFFFF.

		Returns:
			number
		"""
		return self._get_attribute('pwStatusCode')
	@PwStatusCode.setter
	def PwStatusCode(self, value):
		self._set_attribute('pwStatusCode', value)

	@property
	def RepeatCount(self):
		"""The number of times to repeat the above processes. The default is 1.

		Returns:
			number
		"""
		return self._get_attribute('repeatCount')
	@RepeatCount.setter
	def RepeatCount(self, value):
		self._set_attribute('repeatCount', value)

	@property
	def SendPwStatus(self):
		"""If checked, it signifies whether to send a notification message with a PW status for the corresponding PW.

		Returns:
			bool
		"""
		return self._get_attribute('sendPwStatus')
	@SendPwStatus.setter
	def SendPwStatus(self, value):
		self._set_attribute('sendPwStatus', value)

	@property
	def SourceAiiAsIp(self):
		"""The IP address.

		Returns:
			str
		"""
		return self._get_attribute('sourceAiiAsIp')
	@SourceAiiAsIp.setter
	def SourceAiiAsIp(self, value):
		self._set_attribute('sourceAiiAsIp', value)

	@property
	def SourceAiiAsNumber(self):
		"""The numerical value indicating the AS of the Source AII.

		Returns:
			number
		"""
		return self._get_attribute('sourceAiiAsNumber')
	@SourceAiiAsNumber.setter
	def SourceAiiAsNumber(self, value):
		self._set_attribute('sourceAiiAsNumber', value)

	@property
	def SourceAiiType(self):
		"""Editable dropdown. The options are: AS, IP.

		Returns:
			str(number|ipAddress)
		"""
		return self._get_attribute('sourceAiiType')
	@SourceAiiType.setter
	def SourceAiiType(self, value):
		self._set_attribute('sourceAiiType', value)

	@property
	def Sp(self):
		"""It signifies the SP value.

		Returns:
			str(hexVal0|hexVal1|hexVal2|hexVal3)
		"""
		return self._get_attribute('sp')
	@Sp.setter
	def Sp(self, value):
		self._set_attribute('sp', value)

	@property
	def Ssrc(self):
		"""Indicates the SSRC value.

		Returns:
			number
		"""
		return self._get_attribute('ssrc')
	@Ssrc.setter
	def Ssrc(self, value):
		self._set_attribute('ssrc', value)

	@property
	def Step(self):
		"""The number to increment the peer address by.

		Returns:
			number
		"""
		return self._get_attribute('step')
	@Step.setter
	def Step(self, value):
		self._set_attribute('step', value)

	@property
	def TargetAiiAsIp(self):
		"""The IP address of the Target AII.

		Returns:
			str
		"""
		return self._get_attribute('targetAiiAsIp')
	@TargetAiiAsIp.setter
	def TargetAiiAsIp(self, value):
		self._set_attribute('targetAiiAsIp', value)

	@property
	def TargetAiiAsNumber(self):
		"""The numerical value of the Target AII.

		Returns:
			number
		"""
		return self._get_attribute('targetAiiAsNumber')
	@TargetAiiAsNumber.setter
	def TargetAiiAsNumber(self, value):
		self._set_attribute('targetAiiAsNumber', value)

	@property
	def TargetAiiType(self):
		"""Editable dropdown. The options are: AS, IP.

		Returns:
			str(number|ipAddress)
		"""
		return self._get_attribute('targetAiiType')
	@TargetAiiType.setter
	def TargetAiiType(self, value):
		self._set_attribute('targetAiiType', value)

	@property
	def TdmBitrate(self):
		"""The tdm bit rate.

		Returns:
			number
		"""
		return self._get_attribute('tdmBitrate')
	@TdmBitrate.setter
	def TdmBitrate(self, value):
		self._set_attribute('tdmBitrate', value)

	@property
	def TdmDataSize(self):
		"""Indicates the TDM data size.

		Returns:
			number
		"""
		return self._get_attribute('tdmDataSize')
	@TdmDataSize.setter
	def TdmDataSize(self, value):
		self._set_attribute('tdmDataSize', value)

	@property
	def TimestampMode(self):
		"""The time stamp mode.

		Returns:
			str(absolute|differential)
		"""
		return self._get_attribute('timestampMode')
	@TimestampMode.setter
	def TimestampMode(self, value):
		self._set_attribute('timestampMode', value)

	@property
	def UpInterval(self):
		"""Time interval for which the same process to be repeated. (Default = 30 sec)

		Returns:
			number
		"""
		return self._get_attribute('upInterval')
	@UpInterval.setter
	def UpInterval(self, value):
		self._set_attribute('upInterval', value)

	@property
	def VcId(self):
		"""The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).

		Returns:
			number
		"""
		return self._get_attribute('vcId')
	@VcId.setter
	def VcId(self, value):
		self._set_attribute('vcId', value)

	@property
	def VcIdStep(self):
		"""The increment step to be added to each additional VC ID in the range of VC IDs.

		Returns:
			number
		"""
		return self._get_attribute('vcIdStep')
	@VcIdStep.setter
	def VcIdStep(self, value):
		self._set_attribute('vcIdStep', value)

	@property
	def VplsIdAsNumber(self):
		"""The 2 byte unsigned integer value indicating the VPLS ID AS Number.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumber')
	@VplsIdAsNumber.setter
	def VplsIdAsNumber(self, value):
		self._set_attribute('vplsIdAsNumber', value)

	@property
	def VplsIdAsNumberStep(self):
		"""The 2 byte unsigned integer value indicating the VPLS ID AS Number Step.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumberStep')
	@VplsIdAsNumberStep.setter
	def VplsIdAsNumberStep(self, value):
		self._set_attribute('vplsIdAsNumberStep', value)

	@property
	def VplsIdAssignedNumber(self):
		"""The 2 or 4 byte unsigned integer value dependent on the vplsIdType

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumber')
	@VplsIdAssignedNumber.setter
	def VplsIdAssignedNumber(self, value):
		self._set_attribute('vplsIdAssignedNumber', value)

	@property
	def VplsIdAssignedNumberStep(self):
		"""The 2 or 4 byte unsigned integer value dependent on the vplsIdType.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumberStep')
	@VplsIdAssignedNumberStep.setter
	def VplsIdAssignedNumberStep(self, value):
		self._set_attribute('vplsIdAssignedNumberStep', value)

	@property
	def VplsIdCount(self):
		"""The 4 byte unsigned integer indicating the VPLS ID Count.

		Returns:
			number
		"""
		return self._get_attribute('vplsIdCount')
	@VplsIdCount.setter
	def VplsIdCount(self, value):
		self._set_attribute('vplsIdCount', value)

	@property
	def VplsIdIpAddress(self):
		"""The IP address of the VPLS Id.

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddress')
	@VplsIdIpAddress.setter
	def VplsIdIpAddress(self, value):
		self._set_attribute('vplsIdIpAddress', value)

	@property
	def VplsIdIpAddressStep(self):
		"""The IP address of the VPLS Id.

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddressStep')
	@VplsIdIpAddressStep.setter
	def VplsIdIpAddressStep(self, value):
		self._set_attribute('vplsIdIpAddressStep', value)

	@property
	def VplsIdType(self):
		"""Editable dropdown. The options are: AS, IP.

		Returns:
			str(asNumber|ipAddress)
		"""
		return self._get_attribute('vplsIdType')
	@VplsIdType.setter
	def VplsIdType(self, value):
		self._set_attribute('vplsIdType', value)

	def add(self, CapableOfReassembly=None, Cas=None, CeIpAddress=None, CemOption=None, CemPayload=None, Count=None, Description=None, DoNotExpandIntoVcs=None, DownInterval=None, DownStartInterval=None, EnableBfdIpUdpCv=None, EnableBfdPwAchCv=None, EnableCBit=None, EnableCccvNegotiation=None, EnableCemOption=None, EnableCemPayload=None, EnableDescriptionPresent=None, EnableLspPingCv=None, EnableMaxAtmPresent=None, EnableMtuPresent=None, EnablePacking=None, EnablePwAchCc=None, EnablePwStatusTlv=None, EnableRouterAlertCc=None, Enabled=None, FecType=None, Frequency=None, IncludeRtpHeader=None, IncludeSsrc=None, IncludeTdmBitrate=None, IncludeTdmOption=None, IncludeTdmPayload=None, IpType=None, LabelMode=None, LabelStart=None, MaxNumberOfAtmCells=None, Mtu=None, PayloadType=None, PeerAddress=None, ProvisioningModel=None, PwStatusCode=None, RepeatCount=None, SendPwStatus=None, SourceAiiAsIp=None, SourceAiiAsNumber=None, SourceAiiType=None, Sp=None, Ssrc=None, Step=None, TargetAiiAsIp=None, TargetAiiAsNumber=None, TargetAiiType=None, TdmBitrate=None, TdmDataSize=None, TimestampMode=None, UpInterval=None, VcId=None, VcIdStep=None, VplsIdAsNumber=None, VplsIdAsNumberStep=None, VplsIdAssignedNumber=None, VplsIdAssignedNumberStep=None, VplsIdCount=None, VplsIdIpAddress=None, VplsIdIpAddressStep=None, VplsIdType=None):
		"""Adds a new l2VcRange node on the server and retrieves it in this instance.

		Args:
			CapableOfReassembly (bool): If enabled, makes the interface capable of reassembly.
			Cas (str(e1Trunk|t1EsfTrunk|t1SfTrunk)): It signifies the CAS value.
			CeIpAddress (str): The IP address of attached CE endpoint. If IP Type is set to Ipv4, then the default is 0.0.0.0, and if the IP type is set to Ipv6, then the default is 0:0:0:0:0:0:0:0.
			CemOption (number): The value of the CEM option.
			CemPayload (number): If enabled, indicates that there is a Circuit Emulation Service over MPLS (CEM) payload.
			Count (number): (In octets) The 8-bit VC information Length field. It indicates the length of the (2-octet) VC ID field plus combined length of all of the parameters in the VC FEC element.
			Description (str): An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.
			DoNotExpandIntoVcs (bool): If true, the VC ranges do not expand into individual VCs.
			DownInterval (number): Time interval for which the PW status will remain down. (Default= 60 seconds)
			DownStartInterval (number): The duration in time after session becomes up and a notification message being sent to make the session down. (Default= 30 seconds)
			EnableBfdIpUdpCv (bool): NOT DEFINED
			EnableBfdPwAchCv (bool): NOT DEFINED
			EnableCBit (bool): Controls generation of the control word.
			EnableCccvNegotiation (bool): NOT DEFINED
			EnableCemOption (bool): Enable the Circuit Emulation over MPLS option, for encapsulation of TDM signals.
			EnableCemPayload (bool): Enable the Circuit Emulation over MPLS payload.
			EnableDescriptionPresent (bool): If enabled, indicates that an optional interface description is present.
			EnableLspPingCv (bool): NOT DEFINED
			EnableMaxAtmPresent (bool): Enables the generation of an interface parameter field with the maximum number of concatenated ATM cells. (default = 0)
			EnableMtuPresent (bool): This attribute enables the generation of an MTU interface parameter field.
			EnablePacking (bool): (For L2 VC FEC ranges and in Unsolicited Label Distribution Mode ONLY.) If enabled, L2 VC FEC ranges will be aggregated within a single LDP PDU to conserve bandwidth and processing.
			EnablePwAchCc (bool): NOT DEFINED
			EnablePwStatusTlv (bool): If checked, this enables the use of PW status TLV in notification messages to notify the PW status.
			EnableRouterAlertCc (bool): NOT DEFINED
			Enabled (bool): Enables use of this VC range.
			FecType (str(pwIdFec|generalizedIdFecVpls)): The FEC type. The options are: PW Id FEC 0x80, Generalized Id FEC 0x81 VPLS.
			Frequency (number): It is the frequency.
			IncludeRtpHeader (bool): If true, includes the RTP header.
			IncludeSsrc (bool): If true, enables SSRC.
			IncludeTdmBitrate (bool): If true, enables TDM bit rate.
			IncludeTdmOption (bool): If true, includes the TDM option.
			IncludeTdmPayload (bool): If true, enables TDM payload.
			IpType (number): The type (IPv4 or IPv6) of the neighbor.
			LabelMode (str(none|increment)): Indicates whether the same label or incrementing labels should be used in the VC ranges.
			LabelStart (number): The first label in the range of labels. The default is 16.
			MaxNumberOfAtmCells (number): The maximum number of ATM cells which may be concatenated and sent in a single MPLS frame. This parameter is part of the FEC element.
			Mtu (number): (in octets) The 2-octet value for the maximum Transmission Unit (MTU).
			PayloadType (number): It is the payload type.
			PeerAddress (str): The IPv4 address of the LDP router which is the peer for this VC range.
			ProvisioningModel (str(manualConfiguration|bgpAutoDiscovery)): Editable dropdown to denote the Provisioning Model.
			PwStatusCode (number): This is an editable dropdown to denote the PW status. This field is editable. The range is from 0x00000001 - 0xFFFFFFFF.
			RepeatCount (number): The number of times to repeat the above processes. The default is 1.
			SendPwStatus (bool): If checked, it signifies whether to send a notification message with a PW status for the corresponding PW.
			SourceAiiAsIp (str): The IP address.
			SourceAiiAsNumber (number): The numerical value indicating the AS of the Source AII.
			SourceAiiType (str(number|ipAddress)): Editable dropdown. The options are: AS, IP.
			Sp (str(hexVal0|hexVal1|hexVal2|hexVal3)): It signifies the SP value.
			Ssrc (number): Indicates the SSRC value.
			Step (number): The number to increment the peer address by.
			TargetAiiAsIp (str): The IP address of the Target AII.
			TargetAiiAsNumber (number): The numerical value of the Target AII.
			TargetAiiType (str(number|ipAddress)): Editable dropdown. The options are: AS, IP.
			TdmBitrate (number): The tdm bit rate.
			TdmDataSize (number): Indicates the TDM data size.
			TimestampMode (str(absolute|differential)): The time stamp mode.
			UpInterval (number): Time interval for which the same process to be repeated. (Default = 30 sec)
			VcId (number): The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).
			VcIdStep (number): The increment step to be added to each additional VC ID in the range of VC IDs.
			VplsIdAsNumber (number): The 2 byte unsigned integer value indicating the VPLS ID AS Number.
			VplsIdAsNumberStep (number): The 2 byte unsigned integer value indicating the VPLS ID AS Number Step.
			VplsIdAssignedNumber (number): The 2 or 4 byte unsigned integer value dependent on the vplsIdType
			VplsIdAssignedNumberStep (number): The 2 or 4 byte unsigned integer value dependent on the vplsIdType.
			VplsIdCount (number): The 4 byte unsigned integer indicating the VPLS ID Count.
			VplsIdIpAddress (str): The IP address of the VPLS Id.
			VplsIdIpAddressStep (str): The IP address of the VPLS Id.
			VplsIdType (str(asNumber|ipAddress)): Editable dropdown. The options are: AS, IP.

		Returns:
			self: This instance with all currently retrieved l2VcRange data using find and the newly added l2VcRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the l2VcRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CapableOfReassembly=None, Cas=None, CeIpAddress=None, CemOption=None, CemPayload=None, Count=None, Description=None, DoNotExpandIntoVcs=None, DownInterval=None, DownStartInterval=None, EnableBfdIpUdpCv=None, EnableBfdPwAchCv=None, EnableCBit=None, EnableCccvNegotiation=None, EnableCemOption=None, EnableCemPayload=None, EnableDescriptionPresent=None, EnableLspPingCv=None, EnableMaxAtmPresent=None, EnableMtuPresent=None, EnablePacking=None, EnablePwAchCc=None, EnablePwStatusTlv=None, EnableRouterAlertCc=None, Enabled=None, FecType=None, Frequency=None, IncludeRtpHeader=None, IncludeSsrc=None, IncludeTdmBitrate=None, IncludeTdmOption=None, IncludeTdmPayload=None, IpType=None, LabelMode=None, LabelStart=None, MaxNumberOfAtmCells=None, Mtu=None, PayloadType=None, PeerAddress=None, ProvisioningModel=None, PwStatusCode=None, RepeatCount=None, SendPwStatus=None, SourceAiiAsIp=None, SourceAiiAsNumber=None, SourceAiiType=None, Sp=None, Ssrc=None, Step=None, TargetAiiAsIp=None, TargetAiiAsNumber=None, TargetAiiType=None, TdmBitrate=None, TdmDataSize=None, TimestampMode=None, UpInterval=None, VcId=None, VcIdStep=None, VplsIdAsNumber=None, VplsIdAsNumberStep=None, VplsIdAssignedNumber=None, VplsIdAssignedNumberStep=None, VplsIdCount=None, VplsIdIpAddress=None, VplsIdIpAddressStep=None, VplsIdType=None):
		"""Finds and retrieves l2VcRange data from the server.

		All named parameters support regex and can be used to selectively retrieve l2VcRange data from the server.
		By default the find method takes no parameters and will retrieve all l2VcRange data from the server.

		Args:
			CapableOfReassembly (bool): If enabled, makes the interface capable of reassembly.
			Cas (str(e1Trunk|t1EsfTrunk|t1SfTrunk)): It signifies the CAS value.
			CeIpAddress (str): The IP address of attached CE endpoint. If IP Type is set to Ipv4, then the default is 0.0.0.0, and if the IP type is set to Ipv6, then the default is 0:0:0:0:0:0:0:0.
			CemOption (number): The value of the CEM option.
			CemPayload (number): If enabled, indicates that there is a Circuit Emulation Service over MPLS (CEM) payload.
			Count (number): (In octets) The 8-bit VC information Length field. It indicates the length of the (2-octet) VC ID field plus combined length of all of the parameters in the VC FEC element.
			Description (str): An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.
			DoNotExpandIntoVcs (bool): If true, the VC ranges do not expand into individual VCs.
			DownInterval (number): Time interval for which the PW status will remain down. (Default= 60 seconds)
			DownStartInterval (number): The duration in time after session becomes up and a notification message being sent to make the session down. (Default= 30 seconds)
			EnableBfdIpUdpCv (bool): NOT DEFINED
			EnableBfdPwAchCv (bool): NOT DEFINED
			EnableCBit (bool): Controls generation of the control word.
			EnableCccvNegotiation (bool): NOT DEFINED
			EnableCemOption (bool): Enable the Circuit Emulation over MPLS option, for encapsulation of TDM signals.
			EnableCemPayload (bool): Enable the Circuit Emulation over MPLS payload.
			EnableDescriptionPresent (bool): If enabled, indicates that an optional interface description is present.
			EnableLspPingCv (bool): NOT DEFINED
			EnableMaxAtmPresent (bool): Enables the generation of an interface parameter field with the maximum number of concatenated ATM cells. (default = 0)
			EnableMtuPresent (bool): This attribute enables the generation of an MTU interface parameter field.
			EnablePacking (bool): (For L2 VC FEC ranges and in Unsolicited Label Distribution Mode ONLY.) If enabled, L2 VC FEC ranges will be aggregated within a single LDP PDU to conserve bandwidth and processing.
			EnablePwAchCc (bool): NOT DEFINED
			EnablePwStatusTlv (bool): If checked, this enables the use of PW status TLV in notification messages to notify the PW status.
			EnableRouterAlertCc (bool): NOT DEFINED
			Enabled (bool): Enables use of this VC range.
			FecType (str(pwIdFec|generalizedIdFecVpls)): The FEC type. The options are: PW Id FEC 0x80, Generalized Id FEC 0x81 VPLS.
			Frequency (number): It is the frequency.
			IncludeRtpHeader (bool): If true, includes the RTP header.
			IncludeSsrc (bool): If true, enables SSRC.
			IncludeTdmBitrate (bool): If true, enables TDM bit rate.
			IncludeTdmOption (bool): If true, includes the TDM option.
			IncludeTdmPayload (bool): If true, enables TDM payload.
			IpType (number): The type (IPv4 or IPv6) of the neighbor.
			LabelMode (str(none|increment)): Indicates whether the same label or incrementing labels should be used in the VC ranges.
			LabelStart (number): The first label in the range of labels. The default is 16.
			MaxNumberOfAtmCells (number): The maximum number of ATM cells which may be concatenated and sent in a single MPLS frame. This parameter is part of the FEC element.
			Mtu (number): (in octets) The 2-octet value for the maximum Transmission Unit (MTU).
			PayloadType (number): It is the payload type.
			PeerAddress (str): The IPv4 address of the LDP router which is the peer for this VC range.
			ProvisioningModel (str(manualConfiguration|bgpAutoDiscovery)): Editable dropdown to denote the Provisioning Model.
			PwStatusCode (number): This is an editable dropdown to denote the PW status. This field is editable. The range is from 0x00000001 - 0xFFFFFFFF.
			RepeatCount (number): The number of times to repeat the above processes. The default is 1.
			SendPwStatus (bool): If checked, it signifies whether to send a notification message with a PW status for the corresponding PW.
			SourceAiiAsIp (str): The IP address.
			SourceAiiAsNumber (number): The numerical value indicating the AS of the Source AII.
			SourceAiiType (str(number|ipAddress)): Editable dropdown. The options are: AS, IP.
			Sp (str(hexVal0|hexVal1|hexVal2|hexVal3)): It signifies the SP value.
			Ssrc (number): Indicates the SSRC value.
			Step (number): The number to increment the peer address by.
			TargetAiiAsIp (str): The IP address of the Target AII.
			TargetAiiAsNumber (number): The numerical value of the Target AII.
			TargetAiiType (str(number|ipAddress)): Editable dropdown. The options are: AS, IP.
			TdmBitrate (number): The tdm bit rate.
			TdmDataSize (number): Indicates the TDM data size.
			TimestampMode (str(absolute|differential)): The time stamp mode.
			UpInterval (number): Time interval for which the same process to be repeated. (Default = 30 sec)
			VcId (number): The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).
			VcIdStep (number): The increment step to be added to each additional VC ID in the range of VC IDs.
			VplsIdAsNumber (number): The 2 byte unsigned integer value indicating the VPLS ID AS Number.
			VplsIdAsNumberStep (number): The 2 byte unsigned integer value indicating the VPLS ID AS Number Step.
			VplsIdAssignedNumber (number): The 2 or 4 byte unsigned integer value dependent on the vplsIdType
			VplsIdAssignedNumberStep (number): The 2 or 4 byte unsigned integer value dependent on the vplsIdType.
			VplsIdCount (number): The 4 byte unsigned integer indicating the VPLS ID Count.
			VplsIdIpAddress (str): The IP address of the VPLS Id.
			VplsIdIpAddressStep (str): The IP address of the VPLS Id.
			VplsIdType (str(asNumber|ipAddress)): Editable dropdown. The options are: AS, IP.

		Returns:
			self: This instance with matching l2VcRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of l2VcRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the l2VcRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
