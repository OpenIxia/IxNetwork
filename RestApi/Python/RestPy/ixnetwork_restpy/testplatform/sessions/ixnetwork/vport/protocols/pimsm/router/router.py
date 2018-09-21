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
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.interface import Interface
		return Interface(self)

	@property
	def DataMdtInterval(self):
		"""The time interval, in seconds, between transmissions of Data MDT Join TLV messages by the source PE Router. (default = 60)

		Returns:
			number
		"""
		return self._get_attribute('dataMdtInterval')
	@DataMdtInterval.setter
	def DataMdtInterval(self, value):
		self._set_attribute('dataMdtInterval', value)

	@property
	def DataMdtTimeOut(self):
		"""The Data MDT hold time, in seconds. If a PE router connected to a receiver does not receive a Data MDT Join TLV message within this time period, it will leave the Data MDT group. (default = 180)

		Returns:
			number
		"""
		return self._get_attribute('dataMdtTimeOut')
	@DataMdtTimeOut.setter
	def DataMdtTimeOut(self, value):
		self._set_attribute('dataMdtTimeOut', value)

	@property
	def DrPriority(self):
		"""The Designated Router (DR) priority, used for DR election.

		Returns:
			number
		"""
		return self._get_attribute('drPriority')
	@DrPriority.setter
	def DrPriority(self, value):
		self._set_attribute('drPriority', value)

	@property
	def Enabled(self):
		"""Enables or disables the router's simulation.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def JoinPruneHoldTime(self):
		"""The amount of time that neighbor routers should hold a received Join state.

		Returns:
			number
		"""
		return self._get_attribute('joinPruneHoldTime')
	@JoinPruneHoldTime.setter
	def JoinPruneHoldTime(self, value):
		self._set_attribute('joinPruneHoldTime', value)

	@property
	def JoinPruneInterval(self):
		"""The interval between transmitted Join/Prune messages.

		Returns:
			number
		"""
		return self._get_attribute('joinPruneInterval')
	@JoinPruneInterval.setter
	def JoinPruneInterval(self, value):
		self._set_attribute('joinPruneInterval', value)

	@property
	def RouterId(self):
		"""The ID of the router, in IPv4 format.

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def RpDiscoveryMode(self):
		"""Sets the discovery mode of the router.

		Returns:
			str(manual|auto)
		"""
		return self._get_attribute('rpDiscoveryMode')
	@RpDiscoveryMode.setter
	def RpDiscoveryMode(self, value):
		self._set_attribute('rpDiscoveryMode', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this emulated router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, DataMdtInterval=None, DataMdtTimeOut=None, DrPriority=None, Enabled=None, JoinPruneHoldTime=None, JoinPruneInterval=None, RouterId=None, RpDiscoveryMode=None, TrafficGroupId=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			DataMdtInterval (number): The time interval, in seconds, between transmissions of Data MDT Join TLV messages by the source PE Router. (default = 60)
			DataMdtTimeOut (number): The Data MDT hold time, in seconds. If a PE router connected to a receiver does not receive a Data MDT Join TLV message within this time period, it will leave the Data MDT group. (default = 180)
			DrPriority (number): The Designated Router (DR) priority, used for DR election.
			Enabled (bool): Enables or disables the router's simulation.
			JoinPruneHoldTime (number): The amount of time that neighbor routers should hold a received Join state.
			JoinPruneInterval (number): The interval between transmitted Join/Prune messages.
			RouterId (str): The ID of the router, in IPv4 format.
			RpDiscoveryMode (str(manual|auto)): Sets the discovery mode of the router.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this emulated router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

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

	def find(self, DataMdtInterval=None, DataMdtTimeOut=None, DrPriority=None, Enabled=None, JoinPruneHoldTime=None, JoinPruneInterval=None, RouterId=None, RpDiscoveryMode=None, TrafficGroupId=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			DataMdtInterval (number): The time interval, in seconds, between transmissions of Data MDT Join TLV messages by the source PE Router. (default = 60)
			DataMdtTimeOut (number): The Data MDT hold time, in seconds. If a PE router connected to a receiver does not receive a Data MDT Join TLV message within this time period, it will leave the Data MDT group. (default = 180)
			DrPriority (number): The Designated Router (DR) priority, used for DR election.
			Enabled (bool): Enables or disables the router's simulation.
			JoinPruneHoldTime (number): The amount of time that neighbor routers should hold a received Join state.
			JoinPruneInterval (number): The interval between transmitted Join/Prune messages.
			RouterId (str): The ID of the router, in IPv4 format.
			RpDiscoveryMode (str(manual|auto)): Sets the discovery mode of the router.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this emulated router is assigned, for the purpose of creating traffic streams among source/destination members of the group.

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
