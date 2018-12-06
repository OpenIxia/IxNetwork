
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


class SenderRange(Base):
	"""The SenderRange class encapsulates a user managed senderRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SenderRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'senderRange'

	def __init__(self, parent):
		super(SenderRange, self).__init__(parent)

	@property
	def TunnelHeadToLeaf(self):
		"""An instance of the TunnelHeadToLeaf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtoleaf.TunnelHeadToLeaf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtoleaf import TunnelHeadToLeaf
		return TunnelHeadToLeaf(self)

	@property
	def TunnelHeadTrafficEndPoint(self):
		"""An instance of the TunnelHeadTrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtrafficendpoint.TunnelHeadTrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelheadtrafficendpoint import TunnelHeadTrafficEndPoint
		return TunnelHeadTrafficEndPoint(self)

	@property
	def AutoGenerateSessionName(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoGenerateSessionName')
	@AutoGenerateSessionName.setter
	def AutoGenerateSessionName(self, value):
		self._set_attribute('autoGenerateSessionName', value)

	@property
	def BackupLspIdPoolStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('backupLspIdPoolStart')
	@BackupLspIdPoolStart.setter
	def BackupLspIdPoolStart(self, value):
		self._set_attribute('backupLspIdPoolStart', value)

	@property
	def Bandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def BandwidthProtectionDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('bandwidthProtectionDesired')
	@BandwidthProtectionDesired.setter
	def BandwidthProtectionDesired(self, value):
		self._set_attribute('bandwidthProtectionDesired', value)

	@property
	def EnableBfdMpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdMpls')
	@EnableBfdMpls.setter
	def EnableBfdMpls(self, value):
		self._set_attribute('enableBfdMpls', value)

	@property
	def EnableFastReroute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFastReroute')
	@EnableFastReroute.setter
	def EnableFastReroute(self, value):
		self._set_attribute('enableFastReroute', value)

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
	def EnablePathReoptimization(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePathReoptimization')
	@EnablePathReoptimization.setter
	def EnablePathReoptimization(self, value):
		self._set_attribute('enablePathReoptimization', value)

	@property
	def EnablePeriodicReEvaluationRequest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePeriodicReEvaluationRequest')
	@EnablePeriodicReEvaluationRequest.setter
	def EnablePeriodicReEvaluationRequest(self, value):
		self._set_attribute('enablePeriodicReEvaluationRequest', value)

	@property
	def EnableResourceAffinities(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableResourceAffinities')
	@EnableResourceAffinities.setter
	def EnableResourceAffinities(self, value):
		self._set_attribute('enableResourceAffinities', value)

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
	def ExcludeAny(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('excludeAny')
	@ExcludeAny.setter
	def ExcludeAny(self, value):
		self._set_attribute('excludeAny', value)

	@property
	def FastRerouteBandwidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteBandwidth')
	@FastRerouteBandwidth.setter
	def FastRerouteBandwidth(self, value):
		self._set_attribute('fastRerouteBandwidth', value)

	@property
	def FastRerouteDetour(self):
		"""

		Returns:
			list(dict(arg1:str,arg2:str))
		"""
		return self._get_attribute('fastRerouteDetour')
	@FastRerouteDetour.setter
	def FastRerouteDetour(self, value):
		self._set_attribute('fastRerouteDetour', value)

	@property
	def FastRerouteExcludeAny(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteExcludeAny')
	@FastRerouteExcludeAny.setter
	def FastRerouteExcludeAny(self, value):
		self._set_attribute('fastRerouteExcludeAny', value)

	@property
	def FastRerouteFacilityBackupDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fastRerouteFacilityBackupDesired')
	@FastRerouteFacilityBackupDesired.setter
	def FastRerouteFacilityBackupDesired(self, value):
		self._set_attribute('fastRerouteFacilityBackupDesired', value)

	@property
	def FastRerouteHoldingPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteHoldingPriority')
	@FastRerouteHoldingPriority.setter
	def FastRerouteHoldingPriority(self, value):
		self._set_attribute('fastRerouteHoldingPriority', value)

	@property
	def FastRerouteHopLimit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteHopLimit')
	@FastRerouteHopLimit.setter
	def FastRerouteHopLimit(self, value):
		self._set_attribute('fastRerouteHopLimit', value)

	@property
	def FastRerouteIncludeAll(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteIncludeAll')
	@FastRerouteIncludeAll.setter
	def FastRerouteIncludeAll(self, value):
		self._set_attribute('fastRerouteIncludeAll', value)

	@property
	def FastRerouteIncludeAny(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteIncludeAny')
	@FastRerouteIncludeAny.setter
	def FastRerouteIncludeAny(self, value):
		self._set_attribute('fastRerouteIncludeAny', value)

	@property
	def FastRerouteOne2OneBackupDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fastRerouteOne2OneBackupDesired')
	@FastRerouteOne2OneBackupDesired.setter
	def FastRerouteOne2OneBackupDesired(self, value):
		self._set_attribute('fastRerouteOne2OneBackupDesired', value)

	@property
	def FastRerouteSendDetour(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fastRerouteSendDetour')
	@FastRerouteSendDetour.setter
	def FastRerouteSendDetour(self, value):
		self._set_attribute('fastRerouteSendDetour', value)

	@property
	def FastRerouteSetupPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fastRerouteSetupPriority')
	@FastRerouteSetupPriority.setter
	def FastRerouteSetupPriority(self, value):
		self._set_attribute('fastRerouteSetupPriority', value)

	@property
	def HoldingPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('holdingPriority')
	@HoldingPriority.setter
	def HoldingPriority(self, value):
		self._set_attribute('holdingPriority', value)

	@property
	def IncludeAll(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('includeAll')
	@IncludeAll.setter
	def IncludeAll(self, value):
		self._set_attribute('includeAll', value)

	@property
	def IncludeAny(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('includeAny')
	@IncludeAny.setter
	def IncludeAny(self, value):
		self._set_attribute('includeAny', value)

	@property
	def IpCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipCount')
	@IpCount.setter
	def IpCount(self, value):
		self._set_attribute('ipCount', value)

	@property
	def IpStart(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipStart')
	@IpStart.setter
	def IpStart(self, value):
		self._set_attribute('ipStart', value)

	@property
	def LabelRecordingDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('labelRecordingDesired')
	@LabelRecordingDesired.setter
	def LabelRecordingDesired(self, value):
		self._set_attribute('labelRecordingDesired', value)

	@property
	def LocalProtectionDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('localProtectionDesired')
	@LocalProtectionDesired.setter
	def LocalProtectionDesired(self, value):
		self._set_attribute('localProtectionDesired', value)

	@property
	def LspIdCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspIdCount')
	@LspIdCount.setter
	def LspIdCount(self, value):
		self._set_attribute('lspIdCount', value)

	@property
	def LspIdStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lspIdStart')
	@LspIdStart.setter
	def LspIdStart(self, value):
		self._set_attribute('lspIdStart', value)

	@property
	def MaximumPacketSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumPacketSize')
	@MaximumPacketSize.setter
	def MaximumPacketSize(self, value):
		self._set_attribute('maximumPacketSize', value)

	@property
	def MinimumPolicedUnit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minimumPolicedUnit')
	@MinimumPolicedUnit.setter
	def MinimumPolicedUnit(self, value):
		self._set_attribute('minimumPolicedUnit', value)

	@property
	def NodeProtectionDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('nodeProtectionDesired')
	@NodeProtectionDesired.setter
	def NodeProtectionDesired(self, value):
		self._set_attribute('nodeProtectionDesired', value)

	@property
	def PathTearTlv(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('pathTearTlv')
	@PathTearTlv.setter
	def PathTearTlv(self, value):
		self._set_attribute('pathTearTlv', value)

	@property
	def PathTlv(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('pathTlv')
	@PathTlv.setter
	def PathTlv(self, value):
		self._set_attribute('pathTlv', value)

	@property
	def PeakDataRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('peakDataRate')
	@PeakDataRate.setter
	def PeakDataRate(self, value):
		self._set_attribute('peakDataRate', value)

	@property
	def ReEvaluationRequestInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('reEvaluationRequestInterval')
	@ReEvaluationRequestInterval.setter
	def ReEvaluationRequestInterval(self, value):
		self._set_attribute('reEvaluationRequestInterval', value)

	@property
	def RefreshInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('refreshInterval')
	@RefreshInterval.setter
	def RefreshInterval(self, value):
		self._set_attribute('refreshInterval', value)

	@property
	def SeStyleDesired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('seStyleDesired')
	@SeStyleDesired.setter
	def SeStyleDesired(self, value):
		self._set_attribute('seStyleDesired', value)

	@property
	def SessionName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sessionName')
	@SessionName.setter
	def SessionName(self, value):
		self._set_attribute('sessionName', value)

	@property
	def SetupPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('setupPriority')
	@SetupPriority.setter
	def SetupPriority(self, value):
		self._set_attribute('setupPriority', value)

	@property
	def TimeoutMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timeoutMultiplier')
	@TimeoutMultiplier.setter
	def TimeoutMultiplier(self, value):
		self._set_attribute('timeoutMultiplier', value)

	@property
	def TokenBucketRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tokenBucketRate')
	@TokenBucketRate.setter
	def TokenBucketRate(self, value):
		self._set_attribute('tokenBucketRate', value)

	@property
	def TokenBucketSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tokenBucketSize')
	@TokenBucketSize.setter
	def TokenBucketSize(self, value):
		self._set_attribute('tokenBucketSize', value)

	def add(self, AutoGenerateSessionName=None, BackupLspIdPoolStart=None, Bandwidth=None, BandwidthProtectionDesired=None, EnableBfdMpls=None, EnableFastReroute=None, EnableLspPing=None, EnablePathReoptimization=None, EnablePeriodicReEvaluationRequest=None, EnableResourceAffinities=None, Enabled=None, ExcludeAny=None, FastRerouteBandwidth=None, FastRerouteDetour=None, FastRerouteExcludeAny=None, FastRerouteFacilityBackupDesired=None, FastRerouteHoldingPriority=None, FastRerouteHopLimit=None, FastRerouteIncludeAll=None, FastRerouteIncludeAny=None, FastRerouteOne2OneBackupDesired=None, FastRerouteSendDetour=None, FastRerouteSetupPriority=None, HoldingPriority=None, IncludeAll=None, IncludeAny=None, IpCount=None, IpStart=None, LabelRecordingDesired=None, LocalProtectionDesired=None, LspIdCount=None, LspIdStart=None, MaximumPacketSize=None, MinimumPolicedUnit=None, NodeProtectionDesired=None, PathTearTlv=None, PathTlv=None, PeakDataRate=None, ReEvaluationRequestInterval=None, RefreshInterval=None, SeStyleDesired=None, SessionName=None, SetupPriority=None, TimeoutMultiplier=None, TokenBucketRate=None, TokenBucketSize=None):
		"""Adds a new senderRange node on the server and retrieves it in this instance.

		Args:
			AutoGenerateSessionName (bool): 
			BackupLspIdPoolStart (number): 
			Bandwidth (number): 
			BandwidthProtectionDesired (bool): 
			EnableBfdMpls (bool): 
			EnableFastReroute (bool): 
			EnableLspPing (bool): 
			EnablePathReoptimization (bool): 
			EnablePeriodicReEvaluationRequest (bool): 
			EnableResourceAffinities (bool): 
			Enabled (bool): 
			ExcludeAny (number): 
			FastRerouteBandwidth (number): 
			FastRerouteDetour (list(dict(arg1:str,arg2:str))): 
			FastRerouteExcludeAny (number): 
			FastRerouteFacilityBackupDesired (bool): 
			FastRerouteHoldingPriority (number): 
			FastRerouteHopLimit (number): 
			FastRerouteIncludeAll (number): 
			FastRerouteIncludeAny (number): 
			FastRerouteOne2OneBackupDesired (bool): 
			FastRerouteSendDetour (bool): 
			FastRerouteSetupPriority (number): 
			HoldingPriority (number): 
			IncludeAll (number): 
			IncludeAny (number): 
			IpCount (number): 
			IpStart (str): 
			LabelRecordingDesired (bool): 
			LocalProtectionDesired (bool): 
			LspIdCount (number): 
			LspIdStart (number): 
			MaximumPacketSize (number): 
			MinimumPolicedUnit (number): 
			NodeProtectionDesired (bool): 
			PathTearTlv (list(dict(arg1:number,arg2:number,arg3:str))): 
			PathTlv (list(dict(arg1:number,arg2:number,arg3:str))): 
			PeakDataRate (number): 
			ReEvaluationRequestInterval (number): 
			RefreshInterval (number): 
			SeStyleDesired (bool): 
			SessionName (str): 
			SetupPriority (number): 
			TimeoutMultiplier (number): 
			TokenBucketRate (number): 
			TokenBucketSize (number): 

		Returns:
			self: This instance with all currently retrieved senderRange data using find and the newly added senderRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the senderRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoGenerateSessionName=None, BackupLspIdPoolStart=None, Bandwidth=None, BandwidthProtectionDesired=None, EnableBfdMpls=None, EnableFastReroute=None, EnableLspPing=None, EnablePathReoptimization=None, EnablePeriodicReEvaluationRequest=None, EnableResourceAffinities=None, Enabled=None, ExcludeAny=None, FastRerouteBandwidth=None, FastRerouteDetour=None, FastRerouteExcludeAny=None, FastRerouteFacilityBackupDesired=None, FastRerouteHoldingPriority=None, FastRerouteHopLimit=None, FastRerouteIncludeAll=None, FastRerouteIncludeAny=None, FastRerouteOne2OneBackupDesired=None, FastRerouteSendDetour=None, FastRerouteSetupPriority=None, HoldingPriority=None, IncludeAll=None, IncludeAny=None, IpCount=None, IpStart=None, LabelRecordingDesired=None, LocalProtectionDesired=None, LspIdCount=None, LspIdStart=None, MaximumPacketSize=None, MinimumPolicedUnit=None, NodeProtectionDesired=None, PathTearTlv=None, PathTlv=None, PeakDataRate=None, ReEvaluationRequestInterval=None, RefreshInterval=None, SeStyleDesired=None, SessionName=None, SetupPriority=None, TimeoutMultiplier=None, TokenBucketRate=None, TokenBucketSize=None):
		"""Finds and retrieves senderRange data from the server.

		All named parameters support regex and can be used to selectively retrieve senderRange data from the server.
		By default the find method takes no parameters and will retrieve all senderRange data from the server.

		Args:
			AutoGenerateSessionName (bool): 
			BackupLspIdPoolStart (number): 
			Bandwidth (number): 
			BandwidthProtectionDesired (bool): 
			EnableBfdMpls (bool): 
			EnableFastReroute (bool): 
			EnableLspPing (bool): 
			EnablePathReoptimization (bool): 
			EnablePeriodicReEvaluationRequest (bool): 
			EnableResourceAffinities (bool): 
			Enabled (bool): 
			ExcludeAny (number): 
			FastRerouteBandwidth (number): 
			FastRerouteDetour (list(dict(arg1:str,arg2:str))): 
			FastRerouteExcludeAny (number): 
			FastRerouteFacilityBackupDesired (bool): 
			FastRerouteHoldingPriority (number): 
			FastRerouteHopLimit (number): 
			FastRerouteIncludeAll (number): 
			FastRerouteIncludeAny (number): 
			FastRerouteOne2OneBackupDesired (bool): 
			FastRerouteSendDetour (bool): 
			FastRerouteSetupPriority (number): 
			HoldingPriority (number): 
			IncludeAll (number): 
			IncludeAny (number): 
			IpCount (number): 
			IpStart (str): 
			LabelRecordingDesired (bool): 
			LocalProtectionDesired (bool): 
			LspIdCount (number): 
			LspIdStart (number): 
			MaximumPacketSize (number): 
			MinimumPolicedUnit (number): 
			NodeProtectionDesired (bool): 
			PathTearTlv (list(dict(arg1:number,arg2:number,arg3:str))): 
			PathTlv (list(dict(arg1:number,arg2:number,arg3:str))): 
			PeakDataRate (number): 
			ReEvaluationRequestInterval (number): 
			RefreshInterval (number): 
			SeStyleDesired (bool): 
			SessionName (str): 
			SetupPriority (number): 
			TimeoutMultiplier (number): 
			TokenBucketRate (number): 
			TokenBucketSize (number): 

		Returns:
			self: This instance with matching senderRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of senderRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the senderRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def DoMakeBeforeBreak(self):
		"""Executes the doMakeBeforeBreak operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=senderRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DoMakeBeforeBreak', payload=locals(), response_object=None)

	def SendReEvaluationRequest(self):
		"""Executes the sendReEvaluationRequest operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=senderRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendReEvaluationRequest', payload=locals(), response_object=None)
