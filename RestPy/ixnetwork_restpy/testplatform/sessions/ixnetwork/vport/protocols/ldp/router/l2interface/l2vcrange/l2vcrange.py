
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
		"""

		Returns:
			bool
		"""
		return self._get_attribute('capableOfReassembly')
	@CapableOfReassembly.setter
	def CapableOfReassembly(self, value):
		self._set_attribute('capableOfReassembly', value)

	@property
	def Cas(self):
		"""

		Returns:
			str(e1Trunk|t1EsfTrunk|t1SfTrunk)
		"""
		return self._get_attribute('cas')
	@Cas.setter
	def Cas(self, value):
		self._set_attribute('cas', value)

	@property
	def CeIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ceIpAddress')
	@CeIpAddress.setter
	def CeIpAddress(self, value):
		self._set_attribute('ceIpAddress', value)

	@property
	def CemOption(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cemOption')
	@CemOption.setter
	def CemOption(self, value):
		self._set_attribute('cemOption', value)

	@property
	def CemPayload(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cemPayload')
	@CemPayload.setter
	def CemPayload(self, value):
		self._set_attribute('cemPayload', value)

	@property
	def Count(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

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
	def DoNotExpandIntoVcs(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('doNotExpandIntoVcs')
	@DoNotExpandIntoVcs.setter
	def DoNotExpandIntoVcs(self, value):
		self._set_attribute('doNotExpandIntoVcs', value)

	@property
	def DownInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('downInterval')
	@DownInterval.setter
	def DownInterval(self, value):
		self._set_attribute('downInterval', value)

	@property
	def DownStartInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('downStartInterval')
	@DownStartInterval.setter
	def DownStartInterval(self, value):
		self._set_attribute('downStartInterval', value)

	@property
	def EnableBfdIpUdpCv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdIpUdpCv')
	@EnableBfdIpUdpCv.setter
	def EnableBfdIpUdpCv(self, value):
		self._set_attribute('enableBfdIpUdpCv', value)

	@property
	def EnableBfdPwAchCv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdPwAchCv')
	@EnableBfdPwAchCv.setter
	def EnableBfdPwAchCv(self, value):
		self._set_attribute('enableBfdPwAchCv', value)

	@property
	def EnableCBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCBit')
	@EnableCBit.setter
	def EnableCBit(self, value):
		self._set_attribute('enableCBit', value)

	@property
	def EnableCccvNegotiation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCccvNegotiation')
	@EnableCccvNegotiation.setter
	def EnableCccvNegotiation(self, value):
		self._set_attribute('enableCccvNegotiation', value)

	@property
	def EnableCemOption(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCemOption')
	@EnableCemOption.setter
	def EnableCemOption(self, value):
		self._set_attribute('enableCemOption', value)

	@property
	def EnableCemPayload(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCemPayload')
	@EnableCemPayload.setter
	def EnableCemPayload(self, value):
		self._set_attribute('enableCemPayload', value)

	@property
	def EnableDescriptionPresent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDescriptionPresent')
	@EnableDescriptionPresent.setter
	def EnableDescriptionPresent(self, value):
		self._set_attribute('enableDescriptionPresent', value)

	@property
	def EnableLspPingCv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLspPingCv')
	@EnableLspPingCv.setter
	def EnableLspPingCv(self, value):
		self._set_attribute('enableLspPingCv', value)

	@property
	def EnableMaxAtmPresent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMaxAtmPresent')
	@EnableMaxAtmPresent.setter
	def EnableMaxAtmPresent(self, value):
		self._set_attribute('enableMaxAtmPresent', value)

	@property
	def EnableMtuPresent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMtuPresent')
	@EnableMtuPresent.setter
	def EnableMtuPresent(self, value):
		self._set_attribute('enableMtuPresent', value)

	@property
	def EnablePacking(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def EnablePwAchCc(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePwAchCc')
	@EnablePwAchCc.setter
	def EnablePwAchCc(self, value):
		self._set_attribute('enablePwAchCc', value)

	@property
	def EnablePwStatusTlv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePwStatusTlv')
	@EnablePwStatusTlv.setter
	def EnablePwStatusTlv(self, value):
		self._set_attribute('enablePwStatusTlv', value)

	@property
	def EnableRouterAlertCc(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRouterAlertCc')
	@EnableRouterAlertCc.setter
	def EnableRouterAlertCc(self, value):
		self._set_attribute('enableRouterAlertCc', value)

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
	def FecType(self):
		"""

		Returns:
			str(pwIdFec|generalizedIdFecVpls)
		"""
		return self._get_attribute('fecType')
	@FecType.setter
	def FecType(self, value):
		self._set_attribute('fecType', value)

	@property
	def Frequency(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('frequency')
	@Frequency.setter
	def Frequency(self, value):
		self._set_attribute('frequency', value)

	@property
	def IncludeRtpHeader(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeRtpHeader')
	@IncludeRtpHeader.setter
	def IncludeRtpHeader(self, value):
		self._set_attribute('includeRtpHeader', value)

	@property
	def IncludeSsrc(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeSsrc')
	@IncludeSsrc.setter
	def IncludeSsrc(self, value):
		self._set_attribute('includeSsrc', value)

	@property
	def IncludeTdmBitrate(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTdmBitrate')
	@IncludeTdmBitrate.setter
	def IncludeTdmBitrate(self, value):
		self._set_attribute('includeTdmBitrate', value)

	@property
	def IncludeTdmOption(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTdmOption')
	@IncludeTdmOption.setter
	def IncludeTdmOption(self, value):
		self._set_attribute('includeTdmOption', value)

	@property
	def IncludeTdmPayload(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTdmPayload')
	@IncludeTdmPayload.setter
	def IncludeTdmPayload(self, value):
		self._set_attribute('includeTdmPayload', value)

	@property
	def IpType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipType')
	@IpType.setter
	def IpType(self, value):
		self._set_attribute('ipType', value)

	@property
	def LabelMode(self):
		"""

		Returns:
			str(none|increment)
		"""
		return self._get_attribute('labelMode')
	@LabelMode.setter
	def LabelMode(self, value):
		self._set_attribute('labelMode', value)

	@property
	def LabelStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelStart')
	@LabelStart.setter
	def LabelStart(self, value):
		self._set_attribute('labelStart', value)

	@property
	def MaxNumberOfAtmCells(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfAtmCells')
	@MaxNumberOfAtmCells.setter
	def MaxNumberOfAtmCells(self, value):
		self._set_attribute('maxNumberOfAtmCells', value)

	@property
	def Mtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def PayloadType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('payloadType')
	@PayloadType.setter
	def PayloadType(self, value):
		self._set_attribute('payloadType', value)

	@property
	def PeerAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerAddress')
	@PeerAddress.setter
	def PeerAddress(self, value):
		self._set_attribute('peerAddress', value)

	@property
	def ProvisioningModel(self):
		"""

		Returns:
			str(manualConfiguration|bgpAutoDiscovery)
		"""
		return self._get_attribute('provisioningModel')
	@ProvisioningModel.setter
	def ProvisioningModel(self, value):
		self._set_attribute('provisioningModel', value)

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
	def RepeatCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('repeatCount')
	@RepeatCount.setter
	def RepeatCount(self, value):
		self._set_attribute('repeatCount', value)

	@property
	def SendPwStatus(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendPwStatus')
	@SendPwStatus.setter
	def SendPwStatus(self, value):
		self._set_attribute('sendPwStatus', value)

	@property
	def SourceAiiAsIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAiiAsIp')
	@SourceAiiAsIp.setter
	def SourceAiiAsIp(self, value):
		self._set_attribute('sourceAiiAsIp', value)

	@property
	def SourceAiiAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceAiiAsNumber')
	@SourceAiiAsNumber.setter
	def SourceAiiAsNumber(self, value):
		self._set_attribute('sourceAiiAsNumber', value)

	@property
	def SourceAiiType(self):
		"""

		Returns:
			str(number|ipAddress)
		"""
		return self._get_attribute('sourceAiiType')
	@SourceAiiType.setter
	def SourceAiiType(self, value):
		self._set_attribute('sourceAiiType', value)

	@property
	def Sp(self):
		"""

		Returns:
			str(hexVal0|hexVal1|hexVal2|hexVal3)
		"""
		return self._get_attribute('sp')
	@Sp.setter
	def Sp(self, value):
		self._set_attribute('sp', value)

	@property
	def Ssrc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ssrc')
	@Ssrc.setter
	def Ssrc(self, value):
		self._set_attribute('ssrc', value)

	@property
	def Step(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('step')
	@Step.setter
	def Step(self, value):
		self._set_attribute('step', value)

	@property
	def TargetAiiAsIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('targetAiiAsIp')
	@TargetAiiAsIp.setter
	def TargetAiiAsIp(self, value):
		self._set_attribute('targetAiiAsIp', value)

	@property
	def TargetAiiAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('targetAiiAsNumber')
	@TargetAiiAsNumber.setter
	def TargetAiiAsNumber(self, value):
		self._set_attribute('targetAiiAsNumber', value)

	@property
	def TargetAiiType(self):
		"""

		Returns:
			str(number|ipAddress)
		"""
		return self._get_attribute('targetAiiType')
	@TargetAiiType.setter
	def TargetAiiType(self, value):
		self._set_attribute('targetAiiType', value)

	@property
	def TdmBitrate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tdmBitrate')
	@TdmBitrate.setter
	def TdmBitrate(self, value):
		self._set_attribute('tdmBitrate', value)

	@property
	def TdmDataSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tdmDataSize')
	@TdmDataSize.setter
	def TdmDataSize(self, value):
		self._set_attribute('tdmDataSize', value)

	@property
	def TimestampMode(self):
		"""

		Returns:
			str(absolute|differential)
		"""
		return self._get_attribute('timestampMode')
	@TimestampMode.setter
	def TimestampMode(self, value):
		self._set_attribute('timestampMode', value)

	@property
	def UpInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('upInterval')
	@UpInterval.setter
	def UpInterval(self, value):
		self._set_attribute('upInterval', value)

	@property
	def VcId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vcId')
	@VcId.setter
	def VcId(self, value):
		self._set_attribute('vcId', value)

	@property
	def VcIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vcIdStep')
	@VcIdStep.setter
	def VcIdStep(self, value):
		self._set_attribute('vcIdStep', value)

	@property
	def VplsIdAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumber')
	@VplsIdAsNumber.setter
	def VplsIdAsNumber(self, value):
		self._set_attribute('vplsIdAsNumber', value)

	@property
	def VplsIdAsNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAsNumberStep')
	@VplsIdAsNumberStep.setter
	def VplsIdAsNumberStep(self, value):
		self._set_attribute('vplsIdAsNumberStep', value)

	@property
	def VplsIdAssignedNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumber')
	@VplsIdAssignedNumber.setter
	def VplsIdAssignedNumber(self, value):
		self._set_attribute('vplsIdAssignedNumber', value)

	@property
	def VplsIdAssignedNumberStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdAssignedNumberStep')
	@VplsIdAssignedNumberStep.setter
	def VplsIdAssignedNumberStep(self, value):
		self._set_attribute('vplsIdAssignedNumberStep', value)

	@property
	def VplsIdCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vplsIdCount')
	@VplsIdCount.setter
	def VplsIdCount(self, value):
		self._set_attribute('vplsIdCount', value)

	@property
	def VplsIdIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddress')
	@VplsIdIpAddress.setter
	def VplsIdIpAddress(self, value):
		self._set_attribute('vplsIdIpAddress', value)

	@property
	def VplsIdIpAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vplsIdIpAddressStep')
	@VplsIdIpAddressStep.setter
	def VplsIdIpAddressStep(self, value):
		self._set_attribute('vplsIdIpAddressStep', value)

	@property
	def VplsIdType(self):
		"""

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
			CapableOfReassembly (bool): 
			Cas (str(e1Trunk|t1EsfTrunk|t1SfTrunk)): 
			CeIpAddress (str): 
			CemOption (number): 
			CemPayload (number): 
			Count (number): 
			Description (str): 
			DoNotExpandIntoVcs (bool): 
			DownInterval (number): 
			DownStartInterval (number): 
			EnableBfdIpUdpCv (bool): 
			EnableBfdPwAchCv (bool): 
			EnableCBit (bool): 
			EnableCccvNegotiation (bool): 
			EnableCemOption (bool): 
			EnableCemPayload (bool): 
			EnableDescriptionPresent (bool): 
			EnableLspPingCv (bool): 
			EnableMaxAtmPresent (bool): 
			EnableMtuPresent (bool): 
			EnablePacking (bool): 
			EnablePwAchCc (bool): 
			EnablePwStatusTlv (bool): 
			EnableRouterAlertCc (bool): 
			Enabled (bool): 
			FecType (str(pwIdFec|generalizedIdFecVpls)): 
			Frequency (number): 
			IncludeRtpHeader (bool): 
			IncludeSsrc (bool): 
			IncludeTdmBitrate (bool): 
			IncludeTdmOption (bool): 
			IncludeTdmPayload (bool): 
			IpType (number): 
			LabelMode (str(none|increment)): 
			LabelStart (number): 
			MaxNumberOfAtmCells (number): 
			Mtu (number): 
			PayloadType (number): 
			PeerAddress (str): 
			ProvisioningModel (str(manualConfiguration|bgpAutoDiscovery)): 
			PwStatusCode (number): 
			RepeatCount (number): 
			SendPwStatus (bool): 
			SourceAiiAsIp (str): 
			SourceAiiAsNumber (number): 
			SourceAiiType (str(number|ipAddress)): 
			Sp (str(hexVal0|hexVal1|hexVal2|hexVal3)): 
			Ssrc (number): 
			Step (number): 
			TargetAiiAsIp (str): 
			TargetAiiAsNumber (number): 
			TargetAiiType (str(number|ipAddress)): 
			TdmBitrate (number): 
			TdmDataSize (number): 
			TimestampMode (str(absolute|differential)): 
			UpInterval (number): 
			VcId (number): 
			VcIdStep (number): 
			VplsIdAsNumber (number): 
			VplsIdAsNumberStep (number): 
			VplsIdAssignedNumber (number): 
			VplsIdAssignedNumberStep (number): 
			VplsIdCount (number): 
			VplsIdIpAddress (str): 
			VplsIdIpAddressStep (str): 
			VplsIdType (str(asNumber|ipAddress)): 

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
			CapableOfReassembly (bool): 
			Cas (str(e1Trunk|t1EsfTrunk|t1SfTrunk)): 
			CeIpAddress (str): 
			CemOption (number): 
			CemPayload (number): 
			Count (number): 
			Description (str): 
			DoNotExpandIntoVcs (bool): 
			DownInterval (number): 
			DownStartInterval (number): 
			EnableBfdIpUdpCv (bool): 
			EnableBfdPwAchCv (bool): 
			EnableCBit (bool): 
			EnableCccvNegotiation (bool): 
			EnableCemOption (bool): 
			EnableCemPayload (bool): 
			EnableDescriptionPresent (bool): 
			EnableLspPingCv (bool): 
			EnableMaxAtmPresent (bool): 
			EnableMtuPresent (bool): 
			EnablePacking (bool): 
			EnablePwAchCc (bool): 
			EnablePwStatusTlv (bool): 
			EnableRouterAlertCc (bool): 
			Enabled (bool): 
			FecType (str(pwIdFec|generalizedIdFecVpls)): 
			Frequency (number): 
			IncludeRtpHeader (bool): 
			IncludeSsrc (bool): 
			IncludeTdmBitrate (bool): 
			IncludeTdmOption (bool): 
			IncludeTdmPayload (bool): 
			IpType (number): 
			LabelMode (str(none|increment)): 
			LabelStart (number): 
			MaxNumberOfAtmCells (number): 
			Mtu (number): 
			PayloadType (number): 
			PeerAddress (str): 
			ProvisioningModel (str(manualConfiguration|bgpAutoDiscovery)): 
			PwStatusCode (number): 
			RepeatCount (number): 
			SendPwStatus (bool): 
			SourceAiiAsIp (str): 
			SourceAiiAsNumber (number): 
			SourceAiiType (str(number|ipAddress)): 
			Sp (str(hexVal0|hexVal1|hexVal2|hexVal3)): 
			Ssrc (number): 
			Step (number): 
			TargetAiiAsIp (str): 
			TargetAiiAsNumber (number): 
			TargetAiiType (str(number|ipAddress)): 
			TdmBitrate (number): 
			TdmDataSize (number): 
			TimestampMode (str(absolute|differential)): 
			UpInterval (number): 
			VcId (number): 
			VcIdStep (number): 
			VplsIdAsNumber (number): 
			VplsIdAsNumberStep (number): 
			VplsIdAssignedNumber (number): 
			VplsIdAssignedNumberStep (number): 
			VplsIdCount (number): 
			VplsIdIpAddress (str): 
			VplsIdIpAddressStep (str): 
			VplsIdType (str(asNumber|ipAddress)): 

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
