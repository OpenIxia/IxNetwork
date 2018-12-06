
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


class Bgp(Base):
	"""The Bgp class encapsulates a required bgp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bgp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgp'

	def __init__(self, parent):
		super(Bgp, self).__init__(parent)

	@property
	def NeighborRange(self):
		"""An instance of the NeighborRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.neighborrange.NeighborRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.neighborrange import NeighborRange
		return NeighborRange(self)

	@property
	def AutoFillUpDutIp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoFillUpDutIp')
	@AutoFillUpDutIp.setter
	def AutoFillUpDutIp(self, value):
		self._set_attribute('autoFillUpDutIp', value)

	@property
	def DisableReceivedUpdateValidation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('disableReceivedUpdateValidation')
	@DisableReceivedUpdateValidation.setter
	def DisableReceivedUpdateValidation(self, value):
		self._set_attribute('disableReceivedUpdateValidation', value)

	@property
	def EVpnAfi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eVpnAfi')
	@EVpnAfi.setter
	def EVpnAfi(self, value):
		self._set_attribute('eVpnAfi', value)

	@property
	def EVpnSafi(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eVpnSafi')
	@EVpnSafi.setter
	def EVpnSafi(self, value):
		self._set_attribute('eVpnSafi', value)

	@property
	def EnableAdVplsPrefixLengthInBits(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAdVplsPrefixLengthInBits')
	@EnableAdVplsPrefixLengthInBits.setter
	def EnableAdVplsPrefixLengthInBits(self, value):
		self._set_attribute('enableAdVplsPrefixLengthInBits', value)

	@property
	def EnableExternalActiveConnect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableExternalActiveConnect')
	@EnableExternalActiveConnect.setter
	def EnableExternalActiveConnect(self, value):
		self._set_attribute('enableExternalActiveConnect', value)

	@property
	def EnableInternalActiveConnect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableInternalActiveConnect')
	@EnableInternalActiveConnect.setter
	def EnableInternalActiveConnect(self, value):
		self._set_attribute('enableInternalActiveConnect', value)

	@property
	def EnableLabelExchangeOverLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLabelExchangeOverLsp')
	@EnableLabelExchangeOverLsp.setter
	def EnableLabelExchangeOverLsp(self, value):
		self._set_attribute('enableLabelExchangeOverLsp', value)

	@property
	def EnableVpnLabelExchangeOverLsp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVpnLabelExchangeOverLsp')
	@EnableVpnLabelExchangeOverLsp.setter
	def EnableVpnLabelExchangeOverLsp(self, value):
		self._set_attribute('enableVpnLabelExchangeOverLsp', value)

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
	def EsImportRouteTargetSubType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('esImportRouteTargetSubType')
	@EsImportRouteTargetSubType.setter
	def EsImportRouteTargetSubType(self, value):
		self._set_attribute('esImportRouteTargetSubType', value)

	@property
	def EsImportRouteTargetType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('esImportRouteTargetType')
	@EsImportRouteTargetType.setter
	def EsImportRouteTargetType(self, value):
		self._set_attribute('esImportRouteTargetType', value)

	@property
	def EsiLabelExtendedCommunitySubType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('esiLabelExtendedCommunitySubType')
	@EsiLabelExtendedCommunitySubType.setter
	def EsiLabelExtendedCommunitySubType(self, value):
		self._set_attribute('esiLabelExtendedCommunitySubType', value)

	@property
	def EsiLabelExtendedCommunityType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('esiLabelExtendedCommunityType')
	@EsiLabelExtendedCommunityType.setter
	def EsiLabelExtendedCommunityType(self, value):
		self._set_attribute('esiLabelExtendedCommunityType', value)

	@property
	def EvpnIpAddressLengthUnit(self):
		"""

		Returns:
			str(bit|byte)
		"""
		return self._get_attribute('evpnIpAddressLengthUnit')
	@EvpnIpAddressLengthUnit.setter
	def EvpnIpAddressLengthUnit(self, value):
		self._set_attribute('evpnIpAddressLengthUnit', value)

	@property
	def ExternalRetries(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('externalRetries')
	@ExternalRetries.setter
	def ExternalRetries(self, value):
		self._set_attribute('externalRetries', value)

	@property
	def ExternalRetryDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('externalRetryDelay')
	@ExternalRetryDelay.setter
	def ExternalRetryDelay(self, value):
		self._set_attribute('externalRetryDelay', value)

	@property
	def InternalRetries(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('internalRetries')
	@InternalRetries.setter
	def InternalRetries(self, value):
		self._set_attribute('internalRetries', value)

	@property
	def InternalRetryDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('internalRetryDelay')
	@InternalRetryDelay.setter
	def InternalRetryDelay(self, value):
		self._set_attribute('internalRetryDelay', value)

	@property
	def MacMobilityExtendedCommunitySubType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('macMobilityExtendedCommunitySubType')
	@MacMobilityExtendedCommunitySubType.setter
	def MacMobilityExtendedCommunitySubType(self, value):
		self._set_attribute('macMobilityExtendedCommunitySubType', value)

	@property
	def MacMobilityExtendedCommunityType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('macMobilityExtendedCommunityType')
	@MacMobilityExtendedCommunityType.setter
	def MacMobilityExtendedCommunityType(self, value):
		self._set_attribute('macMobilityExtendedCommunityType', value)

	@property
	def MldpP2mpFecType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mldpP2mpFecType')
	@MldpP2mpFecType.setter
	def MldpP2mpFecType(self, value):
		self._set_attribute('mldpP2mpFecType', value)

	@property
	def RunningState(self):
		"""

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def Tester4ByteAsForIbgp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tester4ByteAsForIbgp')
	@Tester4ByteAsForIbgp.setter
	def Tester4ByteAsForIbgp(self, value):
		self._set_attribute('tester4ByteAsForIbgp', value)

	@property
	def TesterAsForIbgp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('testerAsForIbgp')
	@TesterAsForIbgp.setter
	def TesterAsForIbgp(self, value):
		self._set_attribute('testerAsForIbgp', value)

	@property
	def TriggerVplsPwInitiation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('triggerVplsPwInitiation')
	@TriggerVplsPwInitiation.setter
	def TriggerVplsPwInitiation(self, value):
		self._set_attribute('triggerVplsPwInitiation', value)

	@property
	def VrfRouteImportExtendedCommunitySubType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vrfRouteImportExtendedCommunitySubType')
	@VrfRouteImportExtendedCommunitySubType.setter
	def VrfRouteImportExtendedCommunitySubType(self, value):
		self._set_attribute('vrfRouteImportExtendedCommunitySubType', value)

	def Start(self):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bgp)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bgp)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
