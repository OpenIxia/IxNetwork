from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RsvpP2PEgressLsps(Base):
	"""The RsvpP2PEgressLsps class encapsulates a required rsvpP2PEgressLsps node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpP2PEgressLsps property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rsvpP2PEgressLsps'

	def __init__(self, parent):
		super(RsvpP2PEgressLsps, self).__init__(parent)

	@property
	def RsvpRROSubObjectsList(self):
		"""An instance of the RsvpRROSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvprrosubobjectslist.RsvpRROSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvprrosubobjectslist import RsvpRROSubObjectsList
		return RsvpRROSubObjectsList(self)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnableFixedLabelForReservations(self):
		"""Enable Fixed Label For Reservations

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFixedLabelForReservations')

	@property
	def EnableReplyingLspPing(self):
		"""Enable Replying To Lsp Ping

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableReplyingLspPing')

	@property
	def EndPointIpv6(self):
		"""Destination IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('endPointIpv6')

	@property
	def ForwardLspSelfPing(self):
		"""Forward LSP Self Ping

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('forwardLspSelfPing')

	@property
	def InitialLspSelfPingDropCount(self):
		"""Initial LSP Self Ping Drop Count.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initialLspSelfPingDropCount')

	@property
	def IpTTLDecrementCount(self):
		"""IP TTL Decrement Count.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipTTLDecrementCount')

	@property
	def LabelValue(self):
		"""Label Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelValue')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

	@property
	def LspSelfPingIPDSCP(self):
		"""LSP Self Ping IP DSCP.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspSelfPingIPDSCP')

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
	def NumberOfRroSubObjects(self):
		"""Number Of RRO Sub-Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfRroSubObjects')
	@NumberOfRroSubObjects.setter
	def NumberOfRroSubObjects(self, value):
		self._set_attribute('numberOfRroSubObjects', value)

	@property
	def ReflectRro(self):
		"""Reflect RRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectRro')

	@property
	def RefreshInterval(self):
		"""Refresh Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('refreshInterval')

	@property
	def ReservationStyle(self):
		"""Reservation Style

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reservationStyle')

	@property
	def RetainLspSelfPingDSCP(self):
		"""Retain LSP Self Ping DSCP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('retainLspSelfPingDSCP')

	@property
	def SendReservationConfirmation(self):
		"""Send Reservation Confirmation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendReservationConfirmation')

	@property
	def State(self):
		"""State

		Returns:
			list(str[down|none|notStarted|up])
		"""
		return self._get_attribute('state')

	@property
	def TimeoutMultiplier(self):
		"""Timeout Multiplier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutMultiplier')

	def Start(self):
		"""Executes the start operation on the server.

		Activate/Enable selected Tunnel Tail Ranges

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

		Activate/Enable selected Tunnel Tail Ranges

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

		Activate/Enable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		Start

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Tunnel Tail Ranges

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

		Deactivate/Disable selected Tunnel Tail Ranges

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

		Deactivate/Disable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		Stop

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
