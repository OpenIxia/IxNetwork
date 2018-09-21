from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Router(Base):
	"""The Router class encapsulates a user managed router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'router'

	def __init__(self, parent):
		super(Router, self).__init__(parent)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rip.router.routerange.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rip.router.routerange.routerange import RouteRange
		return RouteRange(self)

	@property
	def AuthorizationPassword(self):
		"""If enableAuthorization is set, this is the 16-character password to be used. Only simple password authentication is supported.

		Returns:
			str
		"""
		return self._get_attribute('authorizationPassword')
	@AuthorizationPassword.setter
	def AuthorizationPassword(self, value):
		self._set_attribute('authorizationPassword', value)

	@property
	def EnableAuthorization(self):
		"""Indicates whether authorization is included in update messages.

		Returns:
			bool
		"""
		return self._get_attribute('enableAuthorization')
	@EnableAuthorization.setter
	def EnableAuthorization(self, value):
		self._set_attribute('enableAuthorization', value)

	@property
	def Enabled(self):
		"""Enables or disables the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterfaceId(self):
		"""The ID associated with the simulated interface.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def ReceiveType(self):
		"""Filters the RIP version of messages this router will receive.

		Returns:
			str(receiveVersion1|receiveVersion2|receiveVersion1And2)
		"""
		return self._get_attribute('receiveType')
	@ReceiveType.setter
	def ReceiveType(self, value):
		self._set_attribute('receiveType', value)

	@property
	def ResponseMode(self):
		"""Controls the manner in which received routes are repeated back to their source. The modes are split horizon, no split horizon, and split horizon with poison reverse.

		Returns:
			str(default|splitHorizon|poisonReverse|splitHorizonSpaceSaver|silent)
		"""
		return self._get_attribute('responseMode')
	@ResponseMode.setter
	def ResponseMode(self, value):
		self._set_attribute('responseMode', value)

	@property
	def SendType(self):
		"""The method for sending RIP packets.

		Returns:
			str(multicast|broadcastV1|broadcastV2)
		"""
		return self._get_attribute('sendType')
	@SendType.setter
	def SendType(self, value):
		self._set_attribute('sendType', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def UpdateInterval(self):
		"""The time, in seconds, between transmitted update messages.

		Returns:
			number
		"""
		return self._get_attribute('updateInterval')
	@UpdateInterval.setter
	def UpdateInterval(self, value):
		self._set_attribute('updateInterval', value)

	@property
	def UpdateIntervalOffset(self):
		"""A random percentage of the time value, expressed in seconds, is added to or subtracted from the update interval to stagger the transmission of messages.

		Returns:
			number
		"""
		return self._get_attribute('updateIntervalOffset')
	@UpdateIntervalOffset.setter
	def UpdateIntervalOffset(self, value):
		self._set_attribute('updateIntervalOffset', value)

	def add(self, AuthorizationPassword=None, EnableAuthorization=None, Enabled=None, InterfaceId=None, ReceiveType=None, ResponseMode=None, SendType=None, TrafficGroupId=None, UpdateInterval=None, UpdateIntervalOffset=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			AuthorizationPassword (str): If enableAuthorization is set, this is the 16-character password to be used. Only simple password authentication is supported.
			EnableAuthorization (bool): Indicates whether authorization is included in update messages.
			Enabled (bool): Enables or disables the simulated router.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The ID associated with the simulated interface.
			ReceiveType (str(receiveVersion1|receiveVersion2|receiveVersion1And2)): Filters the RIP version of messages this router will receive.
			ResponseMode (str(default|splitHorizon|poisonReverse|splitHorizonSpaceSaver|silent)): Controls the manner in which received routes are repeated back to their source. The modes are split horizon, no split horizon, and split horizon with poison reverse.
			SendType (str(multicast|broadcastV1|broadcastV2)): The method for sending RIP packets.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			UpdateInterval (number): The time, in seconds, between transmitted update messages.
			UpdateIntervalOffset (number): A random percentage of the time value, expressed in seconds, is added to or subtracted from the update interval to stagger the transmission of messages.

		Returns:
			self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the router data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AuthorizationPassword=None, EnableAuthorization=None, Enabled=None, InterfaceId=None, ReceiveType=None, ResponseMode=None, SendType=None, TrafficGroupId=None, UpdateInterval=None, UpdateIntervalOffset=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			AuthorizationPassword (str): If enableAuthorization is set, this is the 16-character password to be used. Only simple password authentication is supported.
			EnableAuthorization (bool): Indicates whether authorization is included in update messages.
			Enabled (bool): Enables or disables the simulated router.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The ID associated with the simulated interface.
			ReceiveType (str(receiveVersion1|receiveVersion2|receiveVersion1And2)): Filters the RIP version of messages this router will receive.
			ResponseMode (str(default|splitHorizon|poisonReverse|splitHorizonSpaceSaver|silent)): Controls the manner in which received routes are repeated back to their source. The modes are split horizon, no split horizon, and split horizon with poison reverse.
			SendType (str(multicast|broadcastV1|broadcastV2)): The method for sending RIP packets.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			UpdateInterval (number): The time, in seconds, between transmitted update messages.
			UpdateIntervalOffset (number): A random percentage of the time value, expressed in seconds, is added to or subtracted from the update interval to stagger the transmission of messages.

		Returns:
			self: This instance with matching router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
