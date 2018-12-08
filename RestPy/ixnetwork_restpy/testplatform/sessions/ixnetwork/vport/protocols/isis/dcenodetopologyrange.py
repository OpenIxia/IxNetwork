
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
		"""

		Returns:
			number
		"""
		return self._get_attribute('broadcastPriority')
	@BroadcastPriority.setter
	def BroadcastPriority(self, value):
		self._set_attribute('broadcastPriority', value)

	@property
	def IncludeL2Topology(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeL2Topology')
	@IncludeL2Topology.setter
	def IncludeL2Topology(self, value):
		self._set_attribute('includeL2Topology', value)

	@property
	def InternodeNicknameIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('internodeNicknameIncrement')
	@InternodeNicknameIncrement.setter
	def InternodeNicknameIncrement(self, value):
		self._set_attribute('internodeNicknameIncrement', value)

	@property
	def NicknameCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nicknameCount')
	@NicknameCount.setter
	def NicknameCount(self, value):
		self._set_attribute('nicknameCount', value)

	@property
	def NoOfTreesToCompute(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfTreesToCompute')
	@NoOfTreesToCompute.setter
	def NoOfTreesToCompute(self, value):
		self._set_attribute('noOfTreesToCompute', value)

	@property
	def StartNickname(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startNickname')
	@StartNickname.setter
	def StartNickname(self, value):
		self._set_attribute('startNickname', value)

	@property
	def TopologyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('topologyCount')
	@TopologyCount.setter
	def TopologyCount(self, value):
		self._set_attribute('topologyCount', value)

	@property
	def TopologyId(self):
		"""

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
			BroadcastPriority (number): 
			IncludeL2Topology (bool): 
			InternodeNicknameIncrement (number): 
			NicknameCount (number): 
			NoOfTreesToCompute (number): 
			StartNickname (number): 
			TopologyCount (number): 
			TopologyId (number): 

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
			BroadcastPriority (number): 
			IncludeL2Topology (bool): 
			InternodeNicknameIncrement (number): 
			NicknameCount (number): 
			NoOfTreesToCompute (number): 
			StartNickname (number): 
			TopologyCount (number): 
			TopologyId (number): 

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
