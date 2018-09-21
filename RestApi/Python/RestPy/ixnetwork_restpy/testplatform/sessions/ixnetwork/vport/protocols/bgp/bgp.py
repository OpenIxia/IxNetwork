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
		"""If true, automatically fills up the IP of the DUT

		Returns:
			bool
		"""
		return self._get_attribute('autoFillUpDutIp')
	@AutoFillUpDutIp.setter
	def AutoFillUpDutIp(self, value):
		self._set_attribute('autoFillUpDutIp', value)

	@property
	def DisableReceivedUpdateValidation(self):
		"""If true, disables any update validation request from the DUT.

		Returns:
			bool
		"""
		return self._get_attribute('disableReceivedUpdateValidation')
	@DisableReceivedUpdateValidation.setter
	def DisableReceivedUpdateValidation(self, value):
		self._set_attribute('disableReceivedUpdateValidation', value)

	@property
	def EVpnAfi(self):
		"""AFI to support EVPN. Default value is 25. Minimum valus is 0 and maximum value is 0xFFFF

		Returns:
			number
		"""
		return self._get_attribute('eVpnAfi')
	@EVpnAfi.setter
	def EVpnAfi(self, value):
		self._set_attribute('eVpnAfi', value)

	@property
	def EVpnSafi(self):
		"""SAFI to support EVPN. Default value is 70. Minimum valus is 0 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('eVpnSafi')
	@EVpnSafi.setter
	def EVpnSafi(self, value):
		self._set_attribute('eVpnSafi', value)

	@property
	def EnableAdVplsPrefixLengthInBits(self):
		"""If true, enables the AdVpls length in bits.

		Returns:
			bool
		"""
		return self._get_attribute('enableAdVplsPrefixLengthInBits')
	@EnableAdVplsPrefixLengthInBits.setter
	def EnableAdVplsPrefixLengthInBits(self, value):
		self._set_attribute('enableAdVplsPrefixLengthInBits', value)

	@property
	def EnableExternalActiveConnect(self):
		"""Causes a HELLO message to be actively sent when BGP testing starts.

		Returns:
			bool
		"""
		return self._get_attribute('enableExternalActiveConnect')
	@EnableExternalActiveConnect.setter
	def EnableExternalActiveConnect(self, value):
		self._set_attribute('enableExternalActiveConnect', value)

	@property
	def EnableInternalActiveConnect(self):
		"""Causes a HELLO message to be actively sent when BGP testing starts.

		Returns:
			bool
		"""
		return self._get_attribute('enableInternalActiveConnect')
	@EnableInternalActiveConnect.setter
	def EnableInternalActiveConnect(self, value):
		self._set_attribute('enableInternalActiveConnect', value)

	@property
	def EnableLabelExchangeOverLsp(self):
		"""Enables the ability to exchange labels over LSP for VPNs.

		Returns:
			bool
		"""
		return self._get_attribute('enableLabelExchangeOverLsp')
	@EnableLabelExchangeOverLsp.setter
	def EnableLabelExchangeOverLsp(self, value):
		self._set_attribute('enableLabelExchangeOverLsp', value)

	@property
	def EnableVpnLabelExchangeOverLsp(self):
		"""If true, enables the exchange of VPN exchange over LSP

		Returns:
			bool
		"""
		return self._get_attribute('enableVpnLabelExchangeOverLsp')
	@EnableVpnLabelExchangeOverLsp.setter
	def EnableVpnLabelExchangeOverLsp(self, value):
		self._set_attribute('enableVpnLabelExchangeOverLsp', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of this emulated BGP router in the emulated BGP network. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EsImportRouteTargetSubType(self):
		"""This is a new transitive Route Target extended community carried with the Ethernet Segment route in EVPN. When used, it enables all the PEs connected to the same multi-homed site to import the Ethernet Segment routes. Default value is 2. Minimum value is 1 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('esImportRouteTargetSubType')
	@EsImportRouteTargetSubType.setter
	def EsImportRouteTargetSubType(self, value):
		self._set_attribute('esImportRouteTargetSubType', value)

	@property
	def EsImportRouteTargetType(self):
		"""This is a new transitive Route Target extended community carried with the Ethernet Segment route in EVPN. When used, it enables all the PEs connected to the same multi-homed site to import the Ethernet Segment routes. Default value is 6. Minimum value is 1 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('esImportRouteTargetType')
	@EsImportRouteTargetType.setter
	def EsImportRouteTargetType(self, value):
		self._set_attribute('esImportRouteTargetType', value)

	@property
	def EsiLabelExtendedCommunitySubType(self):
		"""This is a new transitive extended community in EVPN. It may be advertised along with Ethernet Auto-Discovery routes and it enables split-horizon procedures for multi-homed sites. Default value is 1. Minimum value is 1 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('esiLabelExtendedCommunitySubType')
	@EsiLabelExtendedCommunitySubType.setter
	def EsiLabelExtendedCommunitySubType(self, value):
		self._set_attribute('esiLabelExtendedCommunitySubType', value)

	@property
	def EsiLabelExtendedCommunityType(self):
		"""This is a new transitive extended community in EVPN. It may be advertised along with Ethernet Auto-Discovery routes and it enables split-horizon procedures for multi-homed sites. Default value is 6. Minimum value is 1 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('esiLabelExtendedCommunityType')
	@EsiLabelExtendedCommunityType.setter
	def EsiLabelExtendedCommunityType(self, value):
		self._set_attribute('esiLabelExtendedCommunityType', value)

	@property
	def EvpnIpAddressLengthUnit(self):
		"""The unit of the IP address length field in MAC Advertisement route packet, can be bits or bytes

		Returns:
			str(bit|byte)
		"""
		return self._get_attribute('evpnIpAddressLengthUnit')
	@EvpnIpAddressLengthUnit.setter
	def EvpnIpAddressLengthUnit(self, value):
		self._set_attribute('evpnIpAddressLengthUnit', value)

	@property
	def ExternalRetries(self):
		"""The number of times to attempt an OPEN connection with the DUT router(s) before giving up.

		Returns:
			number
		"""
		return self._get_attribute('externalRetries')
	@ExternalRetries.setter
	def ExternalRetries(self, value):
		self._set_attribute('externalRetries', value)

	@property
	def ExternalRetryDelay(self):
		"""When retries are necessary, the delay between retries.

		Returns:
			number
		"""
		return self._get_attribute('externalRetryDelay')
	@ExternalRetryDelay.setter
	def ExternalRetryDelay(self, value):
		self._set_attribute('externalRetryDelay', value)

	@property
	def InternalRetries(self):
		"""The number of times to attempt an OPEN connection with the DUT router(s) before giving up.

		Returns:
			number
		"""
		return self._get_attribute('internalRetries')
	@InternalRetries.setter
	def InternalRetries(self, value):
		self._set_attribute('internalRetries', value)

	@property
	def InternalRetryDelay(self):
		"""When retries are necessary, the delay between retries.

		Returns:
			number
		"""
		return self._get_attribute('internalRetryDelay')
	@InternalRetryDelay.setter
	def InternalRetryDelay(self, value):
		self._set_attribute('internalRetryDelay', value)

	@property
	def MacMobilityExtendedCommunitySubType(self):
		"""This is a new transitive extended community used in EVPN. It may be advertised along with MAC Advertisement routes to support MAC mobility. Default value is 0. Minimum value is 0 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('macMobilityExtendedCommunitySubType')
	@MacMobilityExtendedCommunitySubType.setter
	def MacMobilityExtendedCommunitySubType(self, value):
		self._set_attribute('macMobilityExtendedCommunitySubType', value)

	@property
	def MacMobilityExtendedCommunityType(self):
		"""This is a new transitive extended community used in EVPN. It may be advertised along with MAC Advertisement routes to support MAC mobility. Default value is 6. Minimum value is 1 and maximum value is 0xFF.

		Returns:
			number
		"""
		return self._get_attribute('macMobilityExtendedCommunityType')
	@MacMobilityExtendedCommunityType.setter
	def MacMobilityExtendedCommunityType(self, value):
		self._set_attribute('macMobilityExtendedCommunityType', value)

	@property
	def MldpP2mpFecType(self):
		"""The MLDP P2MP FEC type value in hexadecimal.LOCAL EXECS

		Returns:
			number
		"""
		return self._get_attribute('mldpP2mpFecType')
	@MldpP2mpFecType.setter
	def MldpP2mpFecType(self, value):
		self._set_attribute('mldpP2mpFecType', value)

	@property
	def RunningState(self):
		"""The current running state of the BGP server.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def Tester4ByteAsForIbgp(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('tester4ByteAsForIbgp')
	@Tester4ByteAsForIbgp.setter
	def Tester4ByteAsForIbgp(self, value):
		self._set_attribute('tester4ByteAsForIbgp', value)

	@property
	def TesterAsForIbgp(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('testerAsForIbgp')
	@TesterAsForIbgp.setter
	def TesterAsForIbgp(self, value):
		self._set_attribute('testerAsForIbgp', value)

	@property
	def TriggerVplsPwInitiation(self):
		"""Enable to initiate a trigger a VPLS PW initation that is a BGP-LDP communication.

		Returns:
			bool
		"""
		return self._get_attribute('triggerVplsPwInitiation')
	@TriggerVplsPwInitiation.setter
	def TriggerVplsPwInitiation(self, value):
		self._set_attribute('triggerVplsPwInitiation', value)

	@property
	def VrfRouteImportExtendedCommunitySubType(self):
		"""Extended Community Sub Type to be used in VRF Route Import Extended Community.

		Returns:
			number
		"""
		return self._get_attribute('vrfRouteImportExtendedCommunitySubType')
	@VrfRouteImportExtendedCommunitySubType.setter
	def VrfRouteImportExtendedCommunitySubType(self, value):
		self._set_attribute('vrfRouteImportExtendedCommunitySubType', value)

	def Start(self):
		"""Executes the start operation on the server.

		This function allows to Start BGP on a group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bgp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This function allows to Stop BGP on a group of ports simultaneously.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bgp)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
