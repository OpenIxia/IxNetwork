from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceNodeTopologyRange(Base):
	"""The DceNodeTopologyRange class encapsulates a user managed dceNodeTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceNodeTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceNodeTopologyRange'

	def __init__(self, parent):
		super(DceNodeTopologyRange, self).__init__(parent)

	@property
	def DceNodeInterestedVlanRange(self):
		"""An instance of the DceNodeInterestedVlanRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodeinterestedvlanrange.DceNodeInterestedVlanRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodeinterestedvlanrange import DceNodeInterestedVlanRange
		return DceNodeInterestedVlanRange(self)

	@property
	def BroadcastPriority(self):
		"""Sets the priority in which the topology is broadcast.

		Returns:
			number
		"""
		return self._get_attribute('broadcastPriority')
	@BroadcastPriority.setter
	def BroadcastPriority(self, value):
		self._set_attribute('broadcastPriority', value)

	@property
	def IncludeL2Topology(self):
		"""If true, includes the L2 topology.

		Returns:
			bool
		"""
		return self._get_attribute('includeL2Topology')
	@IncludeL2Topology.setter
	def IncludeL2Topology(self, value):
		self._set_attribute('includeL2Topology', value)

	@property
	def InternodeNicknameIncrement(self):
		"""The increment step to be used for creating the internode increment.

		Returns:
			number
		"""
		return self._get_attribute('internodeNicknameIncrement')
	@InternodeNicknameIncrement.setter
	def InternodeNicknameIncrement(self, value):
		self._set_attribute('internodeNicknameIncrement', value)

	@property
	def NicknameCount(self):
		"""The count of the nickname.

		Returns:
			number
		"""
		return self._get_attribute('nicknameCount')
	@NicknameCount.setter
	def NicknameCount(self, value):
		self._set_attribute('nicknameCount', value)

	@property
	def NoOfTreesToCompute(self):
		"""The number of trees to compute.

		Returns:
			number
		"""
		return self._get_attribute('noOfTreesToCompute')
	@NoOfTreesToCompute.setter
	def NoOfTreesToCompute(self, value):
		self._set_attribute('noOfTreesToCompute', value)

	@property
	def StartNickname(self):
		"""If true, uses the nickname.

		Returns:
			number
		"""
		return self._get_attribute('startNickname')
	@StartNickname.setter
	def StartNickname(self, value):
		self._set_attribute('startNickname', value)

	@property
	def TopologyCount(self):
		"""The count of the topology.

		Returns:
			number
		"""
		return self._get_attribute('topologyCount')
	@TopologyCount.setter
	def TopologyCount(self, value):
		self._set_attribute('topologyCount', value)

	@property
	def TopologyId(self):
		"""The unique identification number of the topology range.

		Returns:
			number
		"""
		return self._get_attribute('topologyId')
	@TopologyId.setter
	def TopologyId(self, value):
		self._set_attribute('topologyId', value)

	def add(self, BroadcastPriority=None, IncludeL2Topology=None, InternodeNicknameIncrement=None, NicknameCount=None, NoOfTreesToCompute=None, StartNickname=None, TopologyCount=None, TopologyId=None):
		"""Adds a new dceNodeTopologyRange node on the server and retrieves it in this instance.

		Args:
			BroadcastPriority (number): Sets the priority in which the topology is broadcast.
			IncludeL2Topology (bool): If true, includes the L2 topology.
			InternodeNicknameIncrement (number): The increment step to be used for creating the internode increment.
			NicknameCount (number): The count of the nickname.
			NoOfTreesToCompute (number): The number of trees to compute.
			StartNickname (number): If true, uses the nickname.
			TopologyCount (number): The count of the topology.
			TopologyId (number): The unique identification number of the topology range.

		Returns:
			self: This instance with all currently retrieved dceNodeTopologyRange data using find and the newly added dceNodeTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceNodeTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BroadcastPriority=None, IncludeL2Topology=None, InternodeNicknameIncrement=None, NicknameCount=None, NoOfTreesToCompute=None, StartNickname=None, TopologyCount=None, TopologyId=None):
		"""Finds and retrieves dceNodeTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceNodeTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all dceNodeTopologyRange data from the server.

		Args:
			BroadcastPriority (number): Sets the priority in which the topology is broadcast.
			IncludeL2Topology (bool): If true, includes the L2 topology.
			InternodeNicknameIncrement (number): The increment step to be used for creating the internode increment.
			NicknameCount (number): The count of the nickname.
			NoOfTreesToCompute (number): The number of trees to compute.
			StartNickname (number): If true, uses the nickname.
			TopologyCount (number): The count of the topology.
			TopologyId (number): The unique identification number of the topology range.

		Returns:
			self: This instance with matching dceNodeTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceNodeTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceNodeTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
