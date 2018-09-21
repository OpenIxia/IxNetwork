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
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ripng.router.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ripng.router.interface.interface import Interface
		return Interface(self)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ripng.router.routerange.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ripng.router.routerange.routerange import RouteRange
		return RouteRange(self)

	@property
	def EnableInterfaceMetric(self):
		"""Enables the use of the RIPng interface metric. This user-assigned metric is added to the normal routing metric.

		Returns:
			bool
		"""
		return self._get_attribute('enableInterfaceMetric')
	@EnableInterfaceMetric.setter
	def EnableInterfaceMetric(self, value):
		self._set_attribute('enableInterfaceMetric', value)

	@property
	def Enabled(self):
		"""Enables the RIPing interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ReceiveType(self):
		"""Determines how the emulated RIPng router will handle received RIPng update messages.

		Returns:
			str(ignore|store)
		"""
		return self._get_attribute('receiveType')
	@ReceiveType.setter
	def ReceiveType(self, value):
		self._set_attribute('receiveType', value)

	@property
	def RouterId(self):
		"""The assigned router ID. The default is 1.

		Returns:
			number
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

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
		"""In seconds) Triggered events, such as sending of unsolicited response messages, are spaced at timed intervals.

		Returns:
			number
		"""
		return self._get_attribute('updateInterval')
	@UpdateInterval.setter
	def UpdateInterval(self, value):
		self._set_attribute('updateInterval', value)

	@property
	def UpdateIntervalOffset(self):
		"""(In seconds) To avoid synchronization of the update messages sent by all routers, the update interval is incremented/decremented by a small random time.

		Returns:
			number
		"""
		return self._get_attribute('updateIntervalOffset')
	@UpdateIntervalOffset.setter
	def UpdateIntervalOffset(self, value):
		self._set_attribute('updateIntervalOffset', value)

	def add(self, EnableInterfaceMetric=None, Enabled=None, ReceiveType=None, RouterId=None, TrafficGroupId=None, UpdateInterval=None, UpdateIntervalOffset=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			EnableInterfaceMetric (bool): Enables the use of the RIPng interface metric. This user-assigned metric is added to the normal routing metric.
			Enabled (bool): Enables the RIPing interface.
			ReceiveType (str(ignore|store)): Determines how the emulated RIPng router will handle received RIPng update messages.
			RouterId (number): The assigned router ID. The default is 1.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			UpdateInterval (number): In seconds) Triggered events, such as sending of unsolicited response messages, are spaced at timed intervals.
			UpdateIntervalOffset (number): (In seconds) To avoid synchronization of the update messages sent by all routers, the update interval is incremented/decremented by a small random time.

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

	def find(self, EnableInterfaceMetric=None, Enabled=None, ReceiveType=None, RouterId=None, TrafficGroupId=None, UpdateInterval=None, UpdateIntervalOffset=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			EnableInterfaceMetric (bool): Enables the use of the RIPng interface metric. This user-assigned metric is added to the normal routing metric.
			Enabled (bool): Enables the RIPing interface.
			ReceiveType (str(ignore|store)): Determines how the emulated RIPng router will handle received RIPng update messages.
			RouterId (number): The assigned router ID. The default is 1.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			UpdateInterval (number): In seconds) Triggered events, such as sending of unsolicited response messages, are spaced at timed intervals.
			UpdateIntervalOffset (number): (In seconds) To avoid synchronization of the update messages sent by all routers, the update interval is incremented/decremented by a small random time.

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
