from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DestinationRange(Base):
	"""The DestinationRange class encapsulates a user managed destinationRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DestinationRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'destinationRange'

	def __init__(self, parent):
		super(DestinationRange, self).__init__(parent)

	@property
	def Egress(self):
		"""An instance of the Egress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.egress.Egress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.egress import Egress
		return Egress(self)._select()

	@property
	def Ingress(self):
		"""An instance of the Ingress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.ingress.Ingress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.ingress import Ingress
		return Ingress(self)._select()

	@property
	def TunnelLeafRange(self):
		"""An instance of the TunnelLeafRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelleafrange.TunnelLeafRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunnelleafrange import TunnelLeafRange
		return TunnelLeafRange(self)

	@property
	def TunnelTailTrafficEndPoint(self):
		"""An instance of the TunnelTailTrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunneltailtrafficendpoint.TunnelTailTrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.tunneltailtrafficendpoint import TunnelTailTrafficEndPoint
		return TunnelTailTrafficEndPoint(self)

	@property
	def Behavior(self):
		"""Indicates whether the destination range corresponds to an Ingress or Egress router.

		Returns:
			str(ingress|egress)
		"""
		return self._get_attribute('behavior')
	@Behavior.setter
	def Behavior(self, value):
		self._set_attribute('behavior', value)

	@property
	def EmulationType(self):
		"""The emulation type selected, the values being RSVP-TE, RSVP-TE P2MP.

		Returns:
			str(reserved|rsvpTe|rsvpTeP2mP)
		"""
		return self._get_attribute('emulationType')
	@EmulationType.setter
	def EmulationType(self, value):
		self._set_attribute('emulationType', value)

	@property
	def EnableReplyingLspPing(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableReplyingLspPing')
	@EnableReplyingLspPing.setter
	def EnableReplyingLspPing(self, value):
		self._set_attribute('enableReplyingLspPing', value)

	@property
	def Enabled(self):
		"""Enables or disables the use of the destination range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IpAddressFrom(self):
		"""The IP address of the first destination router.

		Returns:
			str
		"""
		return self._get_attribute('ipAddressFrom')
	@IpAddressFrom.setter
	def IpAddressFrom(self, value):
		self._set_attribute('ipAddressFrom', value)

	@property
	def IpCount(self):
		"""The number of destination routers. Each router's address is one greater than the previous one's.

		Returns:
			number
		"""
		return self._get_attribute('ipCount')
	@IpCount.setter
	def IpCount(self, value):
		self._set_attribute('ipCount', value)

	@property
	def IsConnectedIpAppended(self):
		"""Append the connected IP as RRO/SRRO subobject at the end of the RRo/SRRO list in the packet.

		Returns:
			bool
		"""
		return self._get_attribute('isConnectedIpAppended')
	@IsConnectedIpAppended.setter
	def IsConnectedIpAppended(self, value):
		self._set_attribute('isConnectedIpAppended', value)

	@property
	def IsHeadIpPrepended(self):
		"""If true, prepend the tunnel head IP as a RRO/SERO subobject at the beginning of the RRO/SRRO list in the packet.

		Returns:
			bool
		"""
		return self._get_attribute('isHeadIpPrepended')
	@IsHeadIpPrepended.setter
	def IsHeadIpPrepended(self, value):
		self._set_attribute('isHeadIpPrepended', value)

	@property
	def IsLeafIpPrepended(self):
		"""If true, prepend the tunnel leaf IP as a RRO/SRRO subobject at the beginning of the RRO/SRRO list in the packet.

		Returns:
			bool
		"""
		return self._get_attribute('isLeafIpPrepended')
	@IsLeafIpPrepended.setter
	def IsLeafIpPrepended(self, value):
		self._set_attribute('isLeafIpPrepended', value)

	@property
	def IsSendingAsRro(self):
		"""If true, send this as a RRO. True only if emulation type is RSVP-TE P2MP.

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsRro')
	@IsSendingAsRro.setter
	def IsSendingAsRro(self, value):
		self._set_attribute('isSendingAsRro', value)

	@property
	def IsSendingAsSrro(self):
		"""If true, send this as a SRRO. Note that both Send as RRO and Send as SRRO can be selected at the same time if so required by the user. True only if emulation type is RSVP-TE P2MP.

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsSrro')
	@IsSendingAsSrro.setter
	def IsSendingAsSrro(self, value):
		self._set_attribute('isSendingAsSrro', value)

	@property
	def P2mpId(self):
		"""The P2MP id represented in IP address format.

		Returns:
			str
		"""
		return self._get_attribute('p2mpId')
	@P2mpId.setter
	def P2mpId(self, value):
		self._set_attribute('p2mpId', value)

	def add(self, Behavior=None, EmulationType=None, EnableReplyingLspPing=None, Enabled=None, IpAddressFrom=None, IpCount=None, IsConnectedIpAppended=None, IsHeadIpPrepended=None, IsLeafIpPrepended=None, IsSendingAsRro=None, IsSendingAsSrro=None, P2mpId=None):
		"""Adds a new destinationRange node on the server and retrieves it in this instance.

		Args:
			Behavior (str(ingress|egress)): Indicates whether the destination range corresponds to an Ingress or Egress router.
			EmulationType (str(reserved|rsvpTe|rsvpTeP2mP)): The emulation type selected, the values being RSVP-TE, RSVP-TE P2MP.
			EnableReplyingLspPing (bool): NOT DEFINED
			Enabled (bool): Enables or disables the use of the destination range.
			IpAddressFrom (str): The IP address of the first destination router.
			IpCount (number): The number of destination routers. Each router's address is one greater than the previous one's.
			IsConnectedIpAppended (bool): Append the connected IP as RRO/SRRO subobject at the end of the RRo/SRRO list in the packet.
			IsHeadIpPrepended (bool): If true, prepend the tunnel head IP as a RRO/SERO subobject at the beginning of the RRO/SRRO list in the packet.
			IsLeafIpPrepended (bool): If true, prepend the tunnel leaf IP as a RRO/SRRO subobject at the beginning of the RRO/SRRO list in the packet.
			IsSendingAsRro (bool): If true, send this as a RRO. True only if emulation type is RSVP-TE P2MP.
			IsSendingAsSrro (bool): If true, send this as a SRRO. Note that both Send as RRO and Send as SRRO can be selected at the same time if so required by the user. True only if emulation type is RSVP-TE P2MP.
			P2mpId (str): The P2MP id represented in IP address format.

		Returns:
			self: This instance with all currently retrieved destinationRange data using find and the newly added destinationRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the destinationRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Behavior=None, EmulationType=None, EnableReplyingLspPing=None, Enabled=None, IpAddressFrom=None, IpCount=None, IsConnectedIpAppended=None, IsHeadIpPrepended=None, IsLeafIpPrepended=None, IsSendingAsRro=None, IsSendingAsSrro=None, P2mpId=None):
		"""Finds and retrieves destinationRange data from the server.

		All named parameters support regex and can be used to selectively retrieve destinationRange data from the server.
		By default the find method takes no parameters and will retrieve all destinationRange data from the server.

		Args:
			Behavior (str(ingress|egress)): Indicates whether the destination range corresponds to an Ingress or Egress router.
			EmulationType (str(reserved|rsvpTe|rsvpTeP2mP)): The emulation type selected, the values being RSVP-TE, RSVP-TE P2MP.
			EnableReplyingLspPing (bool): NOT DEFINED
			Enabled (bool): Enables or disables the use of the destination range.
			IpAddressFrom (str): The IP address of the first destination router.
			IpCount (number): The number of destination routers. Each router's address is one greater than the previous one's.
			IsConnectedIpAppended (bool): Append the connected IP as RRO/SRRO subobject at the end of the RRo/SRRO list in the packet.
			IsHeadIpPrepended (bool): If true, prepend the tunnel head IP as a RRO/SERO subobject at the beginning of the RRO/SRRO list in the packet.
			IsLeafIpPrepended (bool): If true, prepend the tunnel leaf IP as a RRO/SRRO subobject at the beginning of the RRO/SRRO list in the packet.
			IsSendingAsRro (bool): If true, send this as a RRO. True only if emulation type is RSVP-TE P2MP.
			IsSendingAsSrro (bool): If true, send this as a SRRO. Note that both Send as RRO and Send as SRRO can be selected at the same time if so required by the user. True only if emulation type is RSVP-TE P2MP.
			P2mpId (str): The P2MP id represented in IP address format.

		Returns:
			self: This instance with matching destinationRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of destinationRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the destinationRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
