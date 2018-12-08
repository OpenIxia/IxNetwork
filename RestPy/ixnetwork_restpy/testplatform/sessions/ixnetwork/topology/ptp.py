
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


class Ptp(Base):
	"""The Ptp class encapsulates a user managed ptp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ptp property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ptp'

	def __init__(self, parent):
		super(Ptp, self).__init__(parent)

	@property
	def PtpNegBehaveList(self):
		"""An instance of the PtpNegBehaveList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ptpnegbehavelist.PtpNegBehaveList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ptpnegbehavelist import PtpNegBehaveList
		return PtpNegBehaveList(self)._select()

	@property
	def SendgPtpSignalingParams(self):
		"""An instance of the SendgPtpSignalingParams class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sendgptpsignalingparams.SendgPtpSignalingParams)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sendgptpsignalingparams import SendgPtpSignalingParams
		return SendgPtpSignalingParams(self)._select()

	@property
	def AlternateMasterFlag(self):
		"""Select this check box to set the Alternate Master flag in all Announce and Sync messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('alternateMasterFlag')

	@property
	def AnnounceCurrentUtcOffsetValid(self):
		"""Set Announce currentUtcOffsetValid bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceCurrentUtcOffsetValid')

	@property
	def AnnounceDropRate(self):
		"""Percentage rate of the dropped Announce messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceDropRate')

	@property
	def AnnounceFrequencyTraceable(self):
		"""Set Announce frequency traceable bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceFrequencyTraceable')

	@property
	def AnnounceLeap59(self):
		"""Set Announce leap59 bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceLeap59')

	@property
	def AnnounceLeap61(self):
		"""Set Announce leap61 bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceLeap61')

	@property
	def AnnouncePtpTimescale(self):
		"""Set Announce ptpTimescale bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announcePtpTimescale')

	@property
	def AnnounceReceiptTimeout(self):
		"""The number of Announce Intervals that have to pass without receipt of an Announce message to trigger timeout

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceReceiptTimeout')

	@property
	def AnnounceTimeTraceable(self):
		"""Set Announce time traceable bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('announceTimeTraceable')

	@property
	def AvnuMode(self):
		"""AVNU Mode

		Returns:
			str(aVNU_GPTP|aVNU_NA)
		"""
		return self._get_attribute('avnuMode')
	@AvnuMode.setter
	def AvnuMode(self, value):
		self._set_attribute('avnuMode', value)

	@property
	def Bmca(self):
		"""Run the Best Master Clock Algorithm for gPTP (if disabled can use a pre-defined Master or accept messages from any source)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bmca')

	@property
	def ClockAccuracy(self):
		"""Clock accuracy

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clockAccuracy')

	@property
	def ClockClass(self):
		"""Traceability of the time or frequency distributed by the grandmaster clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clockClass')

	@property
	def ClockIdentity(self):
		"""Defines the ClockIdentity to be used by this device

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clockIdentity')

	@property
	def CommunicationMode(self):
		"""Communication mode (unicast/multicast/mixed)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('communicationMode')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def CumulativeScaledRateOffset(self):
		"""Cumulative Scaled Rate Offset field set in the gPTP FollowUp TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cumulativeScaledRateOffset')

	@property
	def CurrentUtcOffset(self):
		"""Set announced Current UTC Offset (seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('currentUtcOffset')

	@property
	def CustomClockId(self):
		"""Use the ClockIdentity configured in the next column instead of MAC based generated one

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('customClockId')

	@property
	def DelayMechanism(self):
		"""Clock delay mechanism

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayMechanism')

	@property
	def DelayReqDropRate(self):
		"""Percentage rate of the dropped (P)DelayReq messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayReqDropRate')

	@property
	def DelayReqOffset(self):
		"""Percentage of the agreed (P)DelayReq Inter-arrival time to schedule between two subsequent DelayReq messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayReqOffset')

	@property
	def DelayReqResidenceTime(self):
		"""Residence time of (P)DelayReq messages through an associated one-step end-to-end transparent clock inserted in the correction field of (P)DelayReq messages sent by this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayReqResidenceTime')

	@property
	def DelayReqSpread(self):
		"""Distribute (P)DelayReq messages in an interval around the targeted Inter-arrival mean time (expressed as a % of targeted mean)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayReqSpread')

	@property
	def DelayRespDropRate(self):
		"""Percentage rate of the dropped DelayResp messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayRespDropRate')

	@property
	def DelayRespReceiptTimeout(self):
		"""DelayResponse Receipt Timeout in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayRespReceiptTimeout')

	@property
	def DelayRespResidenceTime(self):
		"""Residence time of DelayReq messages through an associated two-step end-to-end transparent clock inserted in the correction field of DelayResp messages sent by this clock, or the residence time of PdelayResp messages through an associated one-step end-to-end transparent clock inserted in the correction field of PdelayResp messages sent by this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayRespResidenceTime')

	@property
	def DelayResponseDelay(self):
		"""Additional delay introduced in the DelayResp message (nanoseconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayResponseDelay')

	@property
	def DelayResponseDelayInsertionRate(self):
		"""Percentage rate of the DelayResp messages in which the delay is introduced

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('delayResponseDelayInsertionRate')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Domain(self):
		"""PTP Domain

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domain')

	@property
	def DropMalformed(self):
		"""Drop packets that for which fields like Domain, message rates, Clock Class, Clock Accuracy and Offset Scaled Log Variance are not respecting strict G8275.1 imposed intervals

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dropMalformed')

	@property
	def DropSignalReqAnnounce(self):
		"""Select this check box to drop any Signal Request that contains Announce TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dropSignalReqAnnounce')

	@property
	def DropSignalReqDelayResp(self):
		"""Select this check box to drop any Signal Request that contains DelayResp TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dropSignalReqDelayResp')

	@property
	def DropSignalReqSync(self):
		"""Select this check box to drop any Signal Request that contains Sync TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dropSignalReqSync')

	@property
	def EnableNegativeTesting(self):
		"""Enable Negative Conformance Test

		Returns:
			bool
		"""
		return self._get_attribute('enableNegativeTesting')
	@EnableNegativeTesting.setter
	def EnableNegativeTesting(self, value):
		self._set_attribute('enableNegativeTesting', value)

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FollowUpBadCrcRate(self):
		"""Percentage rate of the bad crc FollowUp messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('followUpBadCrcRate')

	@property
	def FollowUpDelay(self):
		"""Additional delay introduced in the FollowUp message timestamp (ns)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('followUpDelay')

	@property
	def FollowUpDelayInsertionRate(self):
		"""Percentage rate of the FollowUp messages in which the delay is introduced

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('followUpDelayInsertionRate')

	@property
	def FollowUpDropRate(self):
		"""Percentage rate of the dropped FollowUp messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('followUpDropRate')

	@property
	def FollowUpResidenceTime(self):
		"""Master to slave residence of Sync messages through an associated two-step transparent clock inserted in the correction field of FollowUp messages sent by this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('followUpResidenceTime')

	@property
	def Frequency(self):
		"""Frequency(N)

		Returns:
			number
		"""
		return self._get_attribute('frequency')
	@Frequency.setter
	def Frequency(self, value):
		self._set_attribute('frequency', value)

	@property
	def GmTimeBaseIndicator(self):
		"""GM Time Base Indicator field set in the gPTP FollowUp TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('gmTimeBaseIndicator')

	@property
	def GrandmasterIdentity(self):
		"""Defines the ClockIdentity of the Grandmaster behind this device

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('grandmasterIdentity')

	@property
	def GrantDelayRespDurationInterval(self):
		"""Value of DurationField in REQUEST_UNICAST_TRANSMISSION_TLV for DelayResp messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('grantDelayRespDurationInterval')

	@property
	def GrantSyncDurationInterval(self):
		"""Value of DurationField in REQUEST_UNICAST_TRANSMISSION_TLV for Sync messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('grantSyncDurationInterval')

	@property
	def GrantUnicastDurationInterval(self):
		"""Value of DurationField in REQUEST_UNICAST_TRANSMISSION_TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('grantUnicastDurationInterval')

	@property
	def HandleAnnounceTlv(self):
		"""Send and respond to Announce TLV unicast requests in signal messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('handleAnnounceTlv')

	@property
	def HandleCancelTlv(self):
		"""Send and respond to Cancel TLV unicast requests in signal messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('handleCancelTlv')

	@property
	def LastGmPhaseChange(self):
		"""Last GM Phase Change nanoseconds set in the gPTP FollowUp TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lastGmPhaseChange')

	@property
	def LearnPortId(self):
		"""Slave learns Master Port ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('learnPortId')

	@property
	def LogAnnounceInterval(self):
		"""The log mean time interval between successive Announce messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('logAnnounceInterval')

	@property
	def LogDelayReqInterval(self):
		"""The log mean time interval between successive (P)DelayReq messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('logDelayReqInterval')

	@property
	def LogSyncInterval(self):
		"""The log mean time interval between successive Sync messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('logSyncInterval')

	@property
	def MasterClockId(self):
		"""Displays the Clock ID of the directly connected master port (might not necessarily be the Grandmaster of the system). If simulating a Boundary port it will show the configured Clock ID of the emulated Grandmaster.

		Returns:
			list(obj(ixnetwork_restpy.multivalue.Multivalue))
		"""
		return self._get_attribute('masterClockId')

	@property
	def MasterCount(self):
		"""The total number of Unicast masters to be used for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterCount')

	@property
	def MasterIpAddress(self):
		"""Defines the base address to be used for enumerating all the addresses for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterIpAddress')

	@property
	def MasterIpIncrementBy(self):
		"""Defines the increment to be used for enumerating all the addresses for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterIpIncrementBy')

	@property
	def MasterIpv6Address(self):
		"""Defines the base address to be used for enumerating all the addresses for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterIpv6Address')

	@property
	def MasterIpv6IncrementBy(self):
		"""Defines the increment to be used for enumerating all the addresses for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterIpv6IncrementBy')

	@property
	def MasterMacAddress(self):
		"""Defines the base address to be used for enumerating all the addresses for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterMacAddress')

	@property
	def MasterMacIncrementBy(self):
		"""Defines the increment to be used for enumerating all the addresses for this slave

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('masterMacIncrementBy')

	@property
	def MulticastAddress(self):
		"""The destination multicast address for G8275.1: non-forwardable (01:80:C2:00:00:0E, recommended) or forwardable (01:1B:19:00:00:00)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastAddress')

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NanosecondsPerSecond(self):
		"""The number of nanoseconds the emulated clock should effectively count for one second of hardware ticks

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nanosecondsPerSecond')

	@property
	def NotSlave(self):
		"""When enabled for Master clocks it prevents a G8275.1 port from going into Slave state, by ignoring Announce messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('notSlave')

	@property
	def NumberOFMsgs(self):
		"""Messages Count

		Returns:
			number
		"""
		return self._get_attribute('numberOFMsgs')
	@NumberOFMsgs.setter
	def NumberOFMsgs(self, value):
		self._set_attribute('numberOFMsgs', value)

	@property
	def OffsetScaledLogVariance(self):
		"""Static Offset Scaled Log Variance of this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('offsetScaledLogVariance')

	@property
	def OneWay(self):
		"""Do not send Delay Requests

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('oneWay')

	@property
	def PDelayFollowUpDelay(self):
		"""Additional delay introduced in the PdelayResp FollowUp message (ns)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pDelayFollowUpDelay')

	@property
	def PDelayFollowUpDelayInsertionRate(self):
		"""Percentage rate of the PdelayResp FollowUp messages in which the delay is introduced

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pDelayFollowUpDelayInsertionRate')

	@property
	def PDelayFollowUpDropRate(self):
		"""Percentage rate of the dropped PdelayResp FollowUp messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pDelayFollowUpDropRate')

	@property
	def PDelayFollowUpResidenceTime(self):
		"""Total residence time of PdelayReq and PdelayResp messagews through an associated two-step end-to-end transparent clock inserted in the correction field of PdelayRespFollowUp messages sent by this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pDelayFollowUpResidenceTime')

	@property
	def PathTraceTLV(self):
		"""If selected, the master will append a Path Trace TLV to Announce messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pathTraceTLV')

	@property
	def PortNumber(self):
		"""Port number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portNumber')

	@property
	def Priority1(self):
		"""PTP priority1.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priority1')

	@property
	def Priority2(self):
		"""PTP priority2

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priority2')

	@property
	def Profile(self):
		"""The profile used by this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('profile')

	@property
	def PtpState(self):
		"""Displays the current PTP State

		Returns:
			list(str[disabled|faulty|grandmaster|initializing|listening|master|passive|preMaster|slave|transparentGrandmaster|transparentMaster|uncalibrated])
		"""
		return self._get_attribute('ptpState')

	@property
	def RenewalInvited(self):
		"""Set the Renewal Invited flag in Grant Unicast Transmission TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('renewalInvited')

	@property
	def RequestAttempts(self):
		"""How many succesive requests a slave can request before entering into holddown

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestAttempts')

	@property
	def RequestHolddown(self):
		"""Time between succesive requests if denied/timeout for Signal Request

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestHolddown')

	@property
	def RequestInterval(self):
		"""Time between succesive requests if denied/timeout for Signal Request

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestInterval')

	@property
	def ReverseSync(self):
		"""As a slave, periodically send Reverse Sync messages with recovered clock. As a master, calculate the Offset of the Slave reported time to master time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reverseSync')

	@property
	def ReverseSyncIntervalPercent(self):
		"""The percentage of incoming Sync interval to use for Reverse Sync interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reverseSyncIntervalPercent')

	@property
	def Role(self):
		"""The desired role of this clock (Masters may become Slave as per BMCA)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('role')

	@property
	def RxCalibration(self):
		"""The amount of time (in ns) that the Receive side timestamp needs to be offset to allow for error

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rxCalibration')

	@property
	def ScaledLastGmFreqChange(self):
		"""Scaled Last GM Freq Change field set in the gPTP FollowUp TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('scaledLastGmFreqChange')

	@property
	def SendMulticastAnnounce(self):
		"""Send multicast Announce messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendMulticastAnnounce')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[announceReceiptTimeout|delayRespReceiptTimeout|g82651Layer|g82751ClockAccuracy|g82751ClockClass|g82751Domain|g82751Layer|g82751LogVariance|g82751Priority1|g82751Rates|g82751VLANs|gPTPLayer|handleAnnounceTlvUnckecked|multipleP2PResponses|noAnnounce|none|p2PMixedMode|pathTraceDropAnnounce|signalAnnounceTimeout|signalDelayRespTimeout|signalIntervalGrantDelayRespDuration|signalIntervalGrantDuration|signalIntervalGrantSyncDuration|signalSyncTimeout|syncReceiptTimeout|syncReceiptTimeoutgPTP])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SignalInterval(self):
		"""Time between Signal Request messages, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('signalInterval')

	@property
	def SignalUnicastHandling(self):
		"""Signal unicast handling

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('signalUnicastHandling')

	@property
	def SimulateBoundary(self):
		"""Simulate a Grandmaster port behind this clock acting as a Boundary clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('simulateBoundary')

	@property
	def SimulateTransparent(self):
		"""Simulate a transparent clock in front of this master clock.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('simulateTransparent')

	@property
	def SlaveCount(self):
		"""The total number of Unicast slaves to be used for this master.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveCount')

	@property
	def SlaveIpAddress(self):
		"""Defines the base address to be used for enumerating all the addresses for this master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveIpAddress')

	@property
	def SlaveIpIncrementBy(self):
		"""Defines the increment to be used for enumerating all the addresses for this master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveIpIncrementBy')

	@property
	def SlaveIpv6Address(self):
		"""Defines the base address to be used for enumerating all the addresses for this master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveIpv6Address')

	@property
	def SlaveIpv6IncrementBy(self):
		"""Defines the increment to be used for enumerating all the addresses for this master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveIpv6IncrementBy')

	@property
	def SlaveMacAddress(self):
		"""Defines the base address to be used for enumerating all the addresses for this master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveMacAddress')

	@property
	def SlaveMacIncrementBy(self):
		"""Defines the increment to be used for enumerating all the addresses for this master

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('slaveMacIncrementBy')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def StepMode(self):
		"""Clock step mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('stepMode')

	@property
	def StepsRemoved(self):
		"""The Steps Removed field advertised in Announce Messages, representing the number of hops between this emulated Boundary clock and the Grandmaster clock (including it). Valid values: 0 to 65,535

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('stepsRemoved')

	@property
	def StrictGrant(self):
		"""If selected, the master will not grant values that are above maximum offered values

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('strictGrant')

	@property
	def SyncDropRate(self):
		"""Percentage rate of the dropped Sync messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('syncDropRate')

	@property
	def SyncReceiptTimeout(self):
		"""The number of seconds that have to pass without receipt of an Sync message to trigger timeout

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('syncReceiptTimeout')

	@property
	def SyncReceiptTimeoutgPTP(self):
		"""The number of Sync Intervals that have to pass without receipt of an Sync message to trigger timeout

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('syncReceiptTimeoutgPTP')

	@property
	def SyncResidenceTime(self):
		"""Master to slave residence time of Sync messages through an associated one-step transparent clock inserted in the correction field of Sync messages sent by this clock

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('syncResidenceTime')

	@property
	def TimeSource(self):
		"""Time source for the PTP device

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeSource')

	@property
	def TimestampOffset(self):
		"""The initial offset added to the local clock when starting the session

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timestampOffset')

	@property
	def TxCalibration(self):
		"""The amount of time (in ns) that the transmit timestamp of one step messages (Sync, PdelayResp) needs to be adjusted for error

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('txCalibration')

	@property
	def TxTwoStepCalibration(self):
		"""The amount of time (in ns) that the read transmit timestamp of sent messages (two-step Sync, DelayReq, PdelayReq, two-step PdelayResp) needs to be adjusted for error

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('txTwoStepCalibration')

	@property
	def UpdateTime(self):
		"""Clocks in Slave role will correct their time based on received Sync messages

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('updateTime')

	def add(self, AvnuMode=None, ConnectedVia=None, EnableNegativeTesting=None, Frequency=None, Multiplier=None, Name=None, NumberOFMsgs=None, StackedLayers=None):
		"""Adds a new ptp node on the server and retrieves it in this instance.

		Args:
			AvnuMode (str(aVNU_GPTP|aVNU_NA)): AVNU Mode
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			EnableNegativeTesting (bool): Enable Negative Conformance Test
			Frequency (number): Frequency(N)
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOFMsgs (number): Messages Count
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved ptp data using find and the newly added ptp data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ptp data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AvnuMode=None, ConnectedVia=None, Count=None, DescriptiveName=None, EnableNegativeTesting=None, Errors=None, Frequency=None, Multiplier=None, Name=None, NumberOFMsgs=None, PtpState=None, SessionInfo=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves ptp data from the server.

		All named parameters support regex and can be used to selectively retrieve ptp data from the server.
		By default the find method takes no parameters and will retrieve all ptp data from the server.

		Args:
			AvnuMode (str(aVNU_GPTP|aVNU_NA)): AVNU Mode
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableNegativeTesting (bool): Enable Negative Conformance Test
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Frequency (number): Frequency(N)
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOFMsgs (number): Messages Count
			PtpState (list(str[disabled|faulty|grandmaster|initializing|listening|master|passive|preMaster|slave|transparentGrandmaster|transparentMaster|uncalibrated])): Displays the current PTP State
			SessionInfo (list(str[announceReceiptTimeout|delayRespReceiptTimeout|g82651Layer|g82751ClockAccuracy|g82751ClockClass|g82751Domain|g82751Layer|g82751LogVariance|g82751Priority1|g82751Rates|g82751VLANs|gPTPLayer|handleAnnounceTlvUnckecked|multipleP2PResponses|noAnnounce|none|p2PMixedMode|pathTraceDropAnnounce|signalAnnounceTimeout|signalDelayRespTimeout|signalIntervalGrantDelayRespDuration|signalIntervalGrantDuration|signalIntervalGrantSyncDuration|signalSyncTimeout|syncReceiptTimeout|syncReceiptTimeoutgPTP])): Logs additional information about the session state
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching ptp data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ptp data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ptp data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, AlternateMasterFlag=None, AnnounceCurrentUtcOffsetValid=None, AnnounceDropRate=None, AnnounceFrequencyTraceable=None, AnnounceLeap59=None, AnnounceLeap61=None, AnnouncePtpTimescale=None, AnnounceReceiptTimeout=None, AnnounceTimeTraceable=None, Bmca=None, ClockAccuracy=None, ClockClass=None, ClockIdentity=None, CommunicationMode=None, CumulativeScaledRateOffset=None, CurrentUtcOffset=None, CustomClockId=None, DelayMechanism=None, DelayReqDropRate=None, DelayReqOffset=None, DelayReqResidenceTime=None, DelayReqSpread=None, DelayRespDropRate=None, DelayRespReceiptTimeout=None, DelayRespResidenceTime=None, DelayResponseDelay=None, DelayResponseDelayInsertionRate=None, Domain=None, DropMalformed=None, DropSignalReqAnnounce=None, DropSignalReqDelayResp=None, DropSignalReqSync=None, FollowUpBadCrcRate=None, FollowUpDelay=None, FollowUpDelayInsertionRate=None, FollowUpDropRate=None, FollowUpResidenceTime=None, GmTimeBaseIndicator=None, GrandmasterIdentity=None, GrantDelayRespDurationInterval=None, GrantSyncDurationInterval=None, GrantUnicastDurationInterval=None, HandleAnnounceTlv=None, HandleCancelTlv=None, LastGmPhaseChange=None, LearnPortId=None, LogAnnounceInterval=None, LogDelayReqInterval=None, LogSyncInterval=None, MasterClockId=None, MasterCount=None, MasterIpAddress=None, MasterIpIncrementBy=None, MasterIpv6Address=None, MasterIpv6IncrementBy=None, MasterMacAddress=None, MasterMacIncrementBy=None, MulticastAddress=None, NanosecondsPerSecond=None, NotSlave=None, OffsetScaledLogVariance=None, OneWay=None, PDelayFollowUpDelay=None, PDelayFollowUpDelayInsertionRate=None, PDelayFollowUpDropRate=None, PDelayFollowUpResidenceTime=None, PathTraceTLV=None, PortNumber=None, Priority1=None, Priority2=None, Profile=None, RenewalInvited=None, RequestAttempts=None, RequestHolddown=None, RequestInterval=None, ReverseSync=None, ReverseSyncIntervalPercent=None, Role=None, RxCalibration=None, ScaledLastGmFreqChange=None, SendMulticastAnnounce=None, SignalInterval=None, SignalUnicastHandling=None, SimulateBoundary=None, SimulateTransparent=None, SlaveCount=None, SlaveIpAddress=None, SlaveIpIncrementBy=None, SlaveIpv6Address=None, SlaveIpv6IncrementBy=None, SlaveMacAddress=None, SlaveMacIncrementBy=None, StepMode=None, StepsRemoved=None, StrictGrant=None, SyncDropRate=None, SyncReceiptTimeout=None, SyncReceiptTimeoutgPTP=None, SyncResidenceTime=None, TimeSource=None, TimestampOffset=None, TxCalibration=None, TxTwoStepCalibration=None, UpdateTime=None):
		"""Base class infrastructure that gets a list of ptp device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AlternateMasterFlag (str): optional regex of alternateMasterFlag
			AnnounceCurrentUtcOffsetValid (str): optional regex of announceCurrentUtcOffsetValid
			AnnounceDropRate (str): optional regex of announceDropRate
			AnnounceFrequencyTraceable (str): optional regex of announceFrequencyTraceable
			AnnounceLeap59 (str): optional regex of announceLeap59
			AnnounceLeap61 (str): optional regex of announceLeap61
			AnnouncePtpTimescale (str): optional regex of announcePtpTimescale
			AnnounceReceiptTimeout (str): optional regex of announceReceiptTimeout
			AnnounceTimeTraceable (str): optional regex of announceTimeTraceable
			Bmca (str): optional regex of bmca
			ClockAccuracy (str): optional regex of clockAccuracy
			ClockClass (str): optional regex of clockClass
			ClockIdentity (str): optional regex of clockIdentity
			CommunicationMode (str): optional regex of communicationMode
			CumulativeScaledRateOffset (str): optional regex of cumulativeScaledRateOffset
			CurrentUtcOffset (str): optional regex of currentUtcOffset
			CustomClockId (str): optional regex of customClockId
			DelayMechanism (str): optional regex of delayMechanism
			DelayReqDropRate (str): optional regex of delayReqDropRate
			DelayReqOffset (str): optional regex of delayReqOffset
			DelayReqResidenceTime (str): optional regex of delayReqResidenceTime
			DelayReqSpread (str): optional regex of delayReqSpread
			DelayRespDropRate (str): optional regex of delayRespDropRate
			DelayRespReceiptTimeout (str): optional regex of delayRespReceiptTimeout
			DelayRespResidenceTime (str): optional regex of delayRespResidenceTime
			DelayResponseDelay (str): optional regex of delayResponseDelay
			DelayResponseDelayInsertionRate (str): optional regex of delayResponseDelayInsertionRate
			Domain (str): optional regex of domain
			DropMalformed (str): optional regex of dropMalformed
			DropSignalReqAnnounce (str): optional regex of dropSignalReqAnnounce
			DropSignalReqDelayResp (str): optional regex of dropSignalReqDelayResp
			DropSignalReqSync (str): optional regex of dropSignalReqSync
			FollowUpBadCrcRate (str): optional regex of followUpBadCrcRate
			FollowUpDelay (str): optional regex of followUpDelay
			FollowUpDelayInsertionRate (str): optional regex of followUpDelayInsertionRate
			FollowUpDropRate (str): optional regex of followUpDropRate
			FollowUpResidenceTime (str): optional regex of followUpResidenceTime
			GmTimeBaseIndicator (str): optional regex of gmTimeBaseIndicator
			GrandmasterIdentity (str): optional regex of grandmasterIdentity
			GrantDelayRespDurationInterval (str): optional regex of grantDelayRespDurationInterval
			GrantSyncDurationInterval (str): optional regex of grantSyncDurationInterval
			GrantUnicastDurationInterval (str): optional regex of grantUnicastDurationInterval
			HandleAnnounceTlv (str): optional regex of handleAnnounceTlv
			HandleCancelTlv (str): optional regex of handleCancelTlv
			LastGmPhaseChange (str): optional regex of lastGmPhaseChange
			LearnPortId (str): optional regex of learnPortId
			LogAnnounceInterval (str): optional regex of logAnnounceInterval
			LogDelayReqInterval (str): optional regex of logDelayReqInterval
			LogSyncInterval (str): optional regex of logSyncInterval
			MasterClockId (str): optional regex of masterClockId
			MasterCount (str): optional regex of masterCount
			MasterIpAddress (str): optional regex of masterIpAddress
			MasterIpIncrementBy (str): optional regex of masterIpIncrementBy
			MasterIpv6Address (str): optional regex of masterIpv6Address
			MasterIpv6IncrementBy (str): optional regex of masterIpv6IncrementBy
			MasterMacAddress (str): optional regex of masterMacAddress
			MasterMacIncrementBy (str): optional regex of masterMacIncrementBy
			MulticastAddress (str): optional regex of multicastAddress
			NanosecondsPerSecond (str): optional regex of nanosecondsPerSecond
			NotSlave (str): optional regex of notSlave
			OffsetScaledLogVariance (str): optional regex of offsetScaledLogVariance
			OneWay (str): optional regex of oneWay
			PDelayFollowUpDelay (str): optional regex of pDelayFollowUpDelay
			PDelayFollowUpDelayInsertionRate (str): optional regex of pDelayFollowUpDelayInsertionRate
			PDelayFollowUpDropRate (str): optional regex of pDelayFollowUpDropRate
			PDelayFollowUpResidenceTime (str): optional regex of pDelayFollowUpResidenceTime
			PathTraceTLV (str): optional regex of pathTraceTLV
			PortNumber (str): optional regex of portNumber
			Priority1 (str): optional regex of priority1
			Priority2 (str): optional regex of priority2
			Profile (str): optional regex of profile
			RenewalInvited (str): optional regex of renewalInvited
			RequestAttempts (str): optional regex of requestAttempts
			RequestHolddown (str): optional regex of requestHolddown
			RequestInterval (str): optional regex of requestInterval
			ReverseSync (str): optional regex of reverseSync
			ReverseSyncIntervalPercent (str): optional regex of reverseSyncIntervalPercent
			Role (str): optional regex of role
			RxCalibration (str): optional regex of rxCalibration
			ScaledLastGmFreqChange (str): optional regex of scaledLastGmFreqChange
			SendMulticastAnnounce (str): optional regex of sendMulticastAnnounce
			SignalInterval (str): optional regex of signalInterval
			SignalUnicastHandling (str): optional regex of signalUnicastHandling
			SimulateBoundary (str): optional regex of simulateBoundary
			SimulateTransparent (str): optional regex of simulateTransparent
			SlaveCount (str): optional regex of slaveCount
			SlaveIpAddress (str): optional regex of slaveIpAddress
			SlaveIpIncrementBy (str): optional regex of slaveIpIncrementBy
			SlaveIpv6Address (str): optional regex of slaveIpv6Address
			SlaveIpv6IncrementBy (str): optional regex of slaveIpv6IncrementBy
			SlaveMacAddress (str): optional regex of slaveMacAddress
			SlaveMacIncrementBy (str): optional regex of slaveMacIncrementBy
			StepMode (str): optional regex of stepMode
			StepsRemoved (str): optional regex of stepsRemoved
			StrictGrant (str): optional regex of strictGrant
			SyncDropRate (str): optional regex of syncDropRate
			SyncReceiptTimeout (str): optional regex of syncReceiptTimeout
			SyncReceiptTimeoutgPTP (str): optional regex of syncReceiptTimeoutgPTP
			SyncResidenceTime (str): optional regex of syncResidenceTime
			TimeSource (str): optional regex of timeSource
			TimestampOffset (str): optional regex of timestampOffset
			TxCalibration (str): optional regex of txCalibration
			TxTwoStepCalibration (str): optional regex of txTwoStepCalibration
			UpdateTime (str): optional regex of updateTime

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def GPtpSendSignaling(self, LinkDelayInterval, TimeSyncInterval, AnnounceInterval, ComputeNeighborRateRatio, ComputeNeighborPropDelay):
		"""Executes the gPtpSendSignaling operation on the server.

		Send Signaling messages for the selected PTP IEEE 802.1AS items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			LinkDelayInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a linkDelayInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			TimeSyncInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a timeSyncInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			AnnounceInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a announceInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			ComputeNeighborRateRatio (bool): This parameter requires a computeNeighborRateRatio of type kBool
			ComputeNeighborPropDelay (bool): This parameter requires a computeNeighborPropDelay of type kBool

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GPtpSendSignaling', payload=locals(), response_object=None)

	def GPtpSendSignaling(self, LinkDelayInterval, TimeSyncInterval, AnnounceInterval, ComputeNeighborRateRatio, ComputeNeighborPropDelay, SessionIndices):
		"""Executes the gPtpSendSignaling operation on the server.

		Send Signaling messages for the selected PTP IEEE 802.1AS items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			LinkDelayInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a linkDelayInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			TimeSyncInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a timeSyncInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			AnnounceInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a announceInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			ComputeNeighborRateRatio (bool): This parameter requires a computeNeighborRateRatio of type kBool
			ComputeNeighborPropDelay (bool): This parameter requires a computeNeighborPropDelay of type kBool
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GPtpSendSignaling', payload=locals(), response_object=None)

	def GPtpSendSignaling(self, SessionIndices, LinkDelayInterval, TimeSyncInterval, AnnounceInterval, ComputeNeighborRateRatio, ComputeNeighborPropDelay):
		"""Executes the gPtpSendSignaling operation on the server.

		Send Signaling messages for the selected PTP IEEE 802.1AS items.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			SessionIndices (str): This parameter requires a linkDelayInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			LinkDelayInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a timeSyncInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			TimeSyncInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a announceInterval of type kEnumValue=enumOpt-DoNotChange,enumOpt-Initial,enumOpt-Stop,enumOpt-V0_1_per_second_,enumOpt-V1_1_per_2_seconds_,enumOpt-V2_1_per_4_seconds_,enumOpt-V3_1_per_8_seconds_,enumOpt-V4_1_per_16_seconds_,enumOpt-V5_1_per_32_seconds_,enumOpt-V6_1_per_64_seconds_,enumOpt-V7_1_per_128_seconds_,enumOpt-V8_1_per_256_seconds_,enumOpt-V9_1_per_512_seconds_,enumOpt-Vneg1_2_per_second_,enumOpt-Vneg2_4_per_second_,enumOpt-Vneg3_8_per_second_,enumOpt-Vneg4_16_per_second_,enumOpt-Vneg5_32_per_second_,enumOpt-Vneg6_64_per_second_,enumOpt-Vneg7_128_per_second_,enumOpt-Vneg8_256_per_second_,enumOpt-Vneg9_512_per_second_
			AnnounceInterval (str(enumOpt-DoNotChange|enumOpt-Initial|enumOpt-Stop|enumOpt-V0_1_per_second_|enumOpt-V1_1_per_2_seconds_|enumOpt-V2_1_per_4_seconds_|enumOpt-V3_1_per_8_seconds_|enumOpt-V4_1_per_16_seconds_|enumOpt-V5_1_per_32_seconds_|enumOpt-V6_1_per_64_seconds_|enumOpt-V7_1_per_128_seconds_|enumOpt-V8_1_per_256_seconds_|enumOpt-V9_1_per_512_seconds_|enumOpt-Vneg1_2_per_second_|enumOpt-Vneg2_4_per_second_|enumOpt-Vneg3_8_per_second_|enumOpt-Vneg4_16_per_second_|enumOpt-Vneg5_32_per_second_|enumOpt-Vneg6_64_per_second_|enumOpt-Vneg7_128_per_second_|enumOpt-Vneg8_256_per_second_|enumOpt-Vneg9_512_per_second_)): This parameter requires a computeNeighborRateRatio of type kBool
			ComputeNeighborRateRatio (bool): This parameter requires a computeNeighborPropDelay of type kBool
			ComputeNeighborPropDelay (bool): This parameter requires a string of session numbers 1-4;6;7-12

		Returns:
			list(dict(port:str[None|/api/v1/sessions/1/ixnetwork/vport],isSuccess:bool,data:str)): The return value is an array of structures where each structure consists of a /vport object reference, the success of the operation and the returned data of the operation for that /vport. This exec is not asynchronous.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GPtpSendSignaling', payload=locals(), response_object=None)

	def RestartDown(self):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def SendgPtpSignaling(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7):
		"""Executes the sendgPtpSignaling operation on the server.

		Send Signaling messages for the selected PTP IEEE 802.1AS sessions.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the device group for the corresponding device instances whose PTP sessions are used as the source of the signaling messages.
			Arg3 (str(doNotChange|initial|stop|v0_1_per_second_|v1_1_per_2_seconds_|v2_1_per_4_seconds_|v3_1_per_8_seconds_|v4_1_per_16_seconds_|v5_1_per_32_seconds_|v6_1_per_64_seconds_|v7_1_per_128_seconds_|v8_1_per_256_seconds_|v9_1_per_512_seconds_|vneg1_2_per_second_|vneg2_4_per_second_|vneg3_8_per_second_|vneg4_16_per_second_|vneg5_32_per_second_|vneg6_64_per_second_|vneg7_128_per_second_|vneg8_256_per_second_|vneg9_512_per_second_)): Desired linkDelayInterval
			Arg4 (str(doNotChange|initial|stop|v0_1_per_second_|v1_1_per_2_seconds_|v2_1_per_4_seconds_|v3_1_per_8_seconds_|v4_1_per_16_seconds_|v5_1_per_32_seconds_|v6_1_per_64_seconds_|v7_1_per_128_seconds_|v8_1_per_256_seconds_|v9_1_per_512_seconds_|vneg1_2_per_second_|vneg2_4_per_second_|vneg3_8_per_second_|vneg4_16_per_second_|vneg5_32_per_second_|vneg6_64_per_second_|vneg7_128_per_second_|vneg8_256_per_second_|vneg9_512_per_second_)): Desired timeSyncInterval
			Arg5 (str(doNotChange|initial|stop|v0_1_per_second_|v1_1_per_2_seconds_|v2_1_per_4_seconds_|v3_1_per_8_seconds_|v4_1_per_16_seconds_|v5_1_per_32_seconds_|v6_1_per_64_seconds_|v7_1_per_128_seconds_|v8_1_per_256_seconds_|v9_1_per_512_seconds_|vneg1_2_per_second_|vneg2_4_per_second_|vneg3_8_per_second_|vneg4_16_per_second_|vneg5_32_per_second_|vneg6_64_per_second_|vneg7_128_per_second_|vneg8_256_per_second_|vneg9_512_per_second_)): Desired announceInterval
			Arg6 (bool): computeNeighborRateRatio flag
			Arg7 (bool): computeNeighborPropDelay flag

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendgPtpSignaling', payload=locals(), response_object=None)

	def SendgPtpSignaling(self, Arg2, Arg3, Arg4, Arg5, Arg6):
		"""Executes the sendgPtpSignaling operation on the server.

		Send Signaling messages for all PTP IEEE 802.1AS sessions.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(doNotChange|initial|stop|v0_1_per_second_|v1_1_per_2_seconds_|v2_1_per_4_seconds_|v3_1_per_8_seconds_|v4_1_per_16_seconds_|v5_1_per_32_seconds_|v6_1_per_64_seconds_|v7_1_per_128_seconds_|v8_1_per_256_seconds_|v9_1_per_512_seconds_|vneg1_2_per_second_|vneg2_4_per_second_|vneg3_8_per_second_|vneg4_16_per_second_|vneg5_32_per_second_|vneg6_64_per_second_|vneg7_128_per_second_|vneg8_256_per_second_|vneg9_512_per_second_)): Desired linkDelayInterval
			Arg3 (str(doNotChange|initial|stop|v0_1_per_second_|v1_1_per_2_seconds_|v2_1_per_4_seconds_|v3_1_per_8_seconds_|v4_1_per_16_seconds_|v5_1_per_32_seconds_|v6_1_per_64_seconds_|v7_1_per_128_seconds_|v8_1_per_256_seconds_|v9_1_per_512_seconds_|vneg1_2_per_second_|vneg2_4_per_second_|vneg3_8_per_second_|vneg4_16_per_second_|vneg5_32_per_second_|vneg6_64_per_second_|vneg7_128_per_second_|vneg8_256_per_second_|vneg9_512_per_second_)): Desired timeSyncInterval
			Arg4 (str(doNotChange|initial|stop|v0_1_per_second_|v1_1_per_2_seconds_|v2_1_per_4_seconds_|v3_1_per_8_seconds_|v4_1_per_16_seconds_|v5_1_per_32_seconds_|v6_1_per_64_seconds_|v7_1_per_128_seconds_|v8_1_per_256_seconds_|v9_1_per_512_seconds_|vneg1_2_per_second_|vneg2_4_per_second_|vneg3_8_per_second_|vneg4_16_per_second_|vneg5_32_per_second_|vneg6_64_per_second_|vneg7_128_per_second_|vneg8_256_per_second_|vneg9_512_per_second_)): Desired announceInterval
			Arg5 (bool): computeNeighborRateRatio flag
			Arg6 (bool): computeNeighborPropDelay flag

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendgPtpSignaling', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
