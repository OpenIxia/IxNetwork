from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ppp(Base):
	"""The Ppp class encapsulates a required ppp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ppp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ppp'

	def __init__(self, parent):
		super(Ppp, self).__init__(parent)

	@property
	def ConfigurationRetries(self):
		"""The number of additional PPP configuration requests to send before beginning the termination process (if the peer is not properly acknowledging them). The default is 9 requests.

		Returns:
			number
		"""
		return self._get_attribute('configurationRetries')
	@ConfigurationRetries.setter
	def ConfigurationRetries(self, value):
		self._set_attribute('configurationRetries', value)

	@property
	def EnableAccmNegotiation(self):
		"""Enables negotiation of Asynchronous Control Character Mask (ACCM).

		Returns:
			bool
		"""
		return self._get_attribute('enableAccmNegotiation')
	@EnableAccmNegotiation.setter
	def EnableAccmNegotiation(self, value):
		self._set_attribute('enableAccmNegotiation', value)

	@property
	def EnableIpV4(self):
		"""Enables the IPv4 Network Control Protocol (IPCP).

		Returns:
			bool
		"""
		return self._get_attribute('enableIpV4')
	@EnableIpV4.setter
	def EnableIpV4(self, value):
		self._set_attribute('enableIpV4', value)

	@property
	def EnableIpV6(self):
		"""Enables the IPv6 Network Control Protocol (IPCP).

		Returns:
			bool
		"""
		return self._get_attribute('enableIpV6')
	@EnableIpV6.setter
	def EnableIpV6(self, value):
		self._set_attribute('enableIpV6', value)

	@property
	def EnableLqm(self):
		"""Enables Link Quality Monitoring (LQM) on the link.

		Returns:
			bool
		"""
		return self._get_attribute('enableLqm')
	@EnableLqm.setter
	def EnableLqm(self, value):
		self._set_attribute('enableLqm', value)

	@property
	def EnableMpls(self):
		"""Enables MPLS on the link.

		Returns:
			bool
		"""
		return self._get_attribute('enableMpls')
	@EnableMpls.setter
	def EnableMpls(self, value):
		self._set_attribute('enableMpls', value)

	@property
	def EnableOsi(self):
		"""Enables the Open System Interconnection (OSI) Network Layer Control Protocol (OSINLCP).

		Returns:
			bool
		"""
		return self._get_attribute('enableOsi')
	@EnableOsi.setter
	def EnableOsi(self, value):
		self._set_attribute('enableOsi', value)

	@property
	def Enabled(self):
		"""If true, enables PPP for the POS port.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def LocalIpAddress(self):
		"""The local port's requested IPv4 address. This address is sent by the local peer to the remote peer, as a Configuration Option in an IPCP Configuration Request packet. The default is 0.0.0.1.

		Returns:
			str
		"""
		return self._get_attribute('localIpAddress')
	@LocalIpAddress.setter
	def LocalIpAddress(self, value):
		self._set_attribute('localIpAddress', value)

	@property
	def LocalIpV6IdType(self):
		"""The type of Interface Identifier (IID). It is a Configuration Options sent in the Configuration Request packet. A globally unique, non-zero Interface Identifier is preferred.

		Returns:
			str(ipV6|lastNegotiated|macBased|random)
		"""
		return self._get_attribute('localIpV6IdType')
	@LocalIpV6IdType.setter
	def LocalIpV6IdType(self, value):
		self._set_attribute('localIpV6IdType', value)

	@property
	def LocalIpV6Iid(self):
		"""(a 64-bit/8-octet value) The IPv6 Interface Identifier. It MUST be unique on the link.

		Returns:
			str
		"""
		return self._get_attribute('localIpV6Iid')
	@LocalIpV6Iid.setter
	def LocalIpV6Iid(self, value):
		self._set_attribute('localIpV6Iid', value)

	@property
	def LocalIpV6MacBasedIid(self):
		"""(a 48-bit/6-octet value) The MAC Interface Identifier. It MUST be unique on the link.

		Returns:
			str
		"""
		return self._get_attribute('localIpV6MacBasedIid')
	@LocalIpV6MacBasedIid.setter
	def LocalIpV6MacBasedIid(self, value):
		self._set_attribute('localIpV6MacBasedIid', value)

	@property
	def LocalIpV6NegotiationMode(self):
		"""Before the negotiation of the Interface Identifier (IID), the node chooses a tentative Interface Identifier.

		Returns:
			str(localMay|localMust|peerMust)
		"""
		return self._get_attribute('localIpV6NegotiationMode')
	@LocalIpV6NegotiationMode.setter
	def LocalIpV6NegotiationMode(self, value):
		self._set_attribute('localIpV6NegotiationMode', value)

	@property
	def LqmReportInterval(self):
		"""The number of seconds between Link Quality Monitoring (LQM) reports.

		Returns:
			number
		"""
		return self._get_attribute('lqmReportInterval')
	@LqmReportInterval.setter
	def LqmReportInterval(self, value):
		self._set_attribute('lqmReportInterval', value)

	@property
	def PeerIpV6IdType(self):
		"""The type of Interface Identifier (IID). It is a Configuration Options sent in the Configuration Request packet. A globally unique, non-zero Interface Identifier is preferred.

		Returns:
			str(ipV6|lastNegotiated|macBased|random)
		"""
		return self._get_attribute('peerIpV6IdType')
	@PeerIpV6IdType.setter
	def PeerIpV6IdType(self, value):
		self._set_attribute('peerIpV6IdType', value)

	@property
	def PeerIpV6Iid(self):
		"""(a 64-bit/8-octet value) The IPv6 Interface Identifier. It MUST be unique on the link.

		Returns:
			str
		"""
		return self._get_attribute('peerIpV6Iid')
	@PeerIpV6Iid.setter
	def PeerIpV6Iid(self, value):
		self._set_attribute('peerIpV6Iid', value)

	@property
	def PeerIpV6MacBasedIid(self):
		"""(a 48-bit/6-octet value) The MAC Interface Identifier. It MUST be unique on the link.

		Returns:
			str
		"""
		return self._get_attribute('peerIpV6MacBasedIid')
	@PeerIpV6MacBasedIid.setter
	def PeerIpV6MacBasedIid(self, value):
		self._set_attribute('peerIpV6MacBasedIid', value)

	@property
	def PeerIpV6NegotiationMode(self):
		"""Before the negotiation of the Interface Identifier (IID), the node chooses a tentative Interface Identifier.

		Returns:
			str(localMust|peerMay|peerMust)
		"""
		return self._get_attribute('peerIpV6NegotiationMode')
	@PeerIpV6NegotiationMode.setter
	def PeerIpV6NegotiationMode(self, value):
		self._set_attribute('peerIpV6NegotiationMode', value)

	@property
	def PppLinkState(self):
		"""(Read-only) Indicates the current port link state. If PPP is enabled, the fully operational link state is indicated as PPP Up.

		Returns:
			str
		"""
		return self._get_attribute('pppLinkState')

	@property
	def RetryTimeout(self):
		"""The time, in seconds, between retransmissions of successive configuration or termination requests. The default is 8 seconds.

		Returns:
			number
		"""
		return self._get_attribute('retryTimeout')
	@RetryTimeout.setter
	def RetryTimeout(self, value):
		self._set_attribute('retryTimeout', value)

	@property
	def RxAlignment(self):
		"""The byte alignment desired for Receive, in bytes. The default is 0 bytes.

		Returns:
			number
		"""
		return self._get_attribute('rxAlignment')
	@RxAlignment.setter
	def RxAlignment(self, value):
		self._set_attribute('rxAlignment', value)

	@property
	def RxMaxReceiveUnit(self):
		"""The maximum transmit frame size desired, in bytes. The default is 65,535 bytes.

		Returns:
			number
		"""
		return self._get_attribute('rxMaxReceiveUnit')
	@RxMaxReceiveUnit.setter
	def RxMaxReceiveUnit(self, value):
		self._set_attribute('rxMaxReceiveUnit', value)

	@property
	def TxAlignment(self):
		"""The byte alignment desired for Transmit, in bytes. The default is 0 bytes.

		Returns:
			number
		"""
		return self._get_attribute('txAlignment')
	@TxAlignment.setter
	def TxAlignment(self, value):
		self._set_attribute('txAlignment', value)

	@property
	def TxMaxReceiveUnit(self):
		"""The maximum transmit frame size desired, in bytes. The default is 65,535 bytes.

		Returns:
			number
		"""
		return self._get_attribute('txMaxReceiveUnit')
	@TxMaxReceiveUnit.setter
	def TxMaxReceiveUnit(self, value):
		self._set_attribute('txMaxReceiveUnit', value)

	@property
	def UseMagicNumber(self):
		"""If enabled, magic number handling is enabled for negotiation and usage. The magic number is used primarily to detect looped connections.

		Returns:
			bool
		"""
		return self._get_attribute('useMagicNumber')
	@UseMagicNumber.setter
	def UseMagicNumber(self, value):
		self._set_attribute('useMagicNumber', value)
