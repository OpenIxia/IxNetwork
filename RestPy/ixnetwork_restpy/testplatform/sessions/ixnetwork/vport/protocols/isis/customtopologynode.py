
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


class CustomTopologyNode(Base):
	"""The CustomTopologyNode class encapsulates a user managed customTopologyNode node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyNode property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyNode'

	def __init__(self, parent):
		super(CustomTopologyNode, self).__init__(parent)

	@property
	def CustomNetworkTopologyLinks(self):
		"""An instance of the CustomNetworkTopologyLinks class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customnetworktopologylinks.CustomNetworkTopologyLinks)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customnetworktopologylinks import CustomNetworkTopologyLinks
		return CustomNetworkTopologyLinks(self)

	@property
	def BridgePriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bridgePriority')
	@BridgePriority.setter
	def BridgePriority(self, value):
		self._set_attribute('bridgePriority', value)

	@property
	def EdgeBridge(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('edgeBridge')
	@EdgeBridge.setter
	def EdgeBridge(self, value):
		self._set_attribute('edgeBridge', value)

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
	def Nickname(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('nickname')
	@Nickname.setter
	def Nickname(self, value):
		self._set_attribute('nickname', value)

	@property
	def Priority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def SpSrcId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('spSrcId')
	@SpSrcId.setter
	def SpSrcId(self, value):
		self._set_attribute('spSrcId', value)

	def add(self, BridgePriority=None, EdgeBridge=None, Enabled=None, Nickname=None, Priority=None, SpSrcId=None):
		"""Adds a new customTopologyNode node on the server and retrieves it in this instance.

		Args:
			BridgePriority (number): 
			EdgeBridge (bool): 
			Enabled (bool): 
			Nickname (number): 
			Priority (number): 
			SpSrcId (number): 

		Returns:
			self: This instance with all currently retrieved customTopologyNode data using find and the newly added customTopologyNode data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyNode data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BridgePriority=None, EdgeBridge=None, Enabled=None, Nickname=None, Priority=None, SpSrcId=None):
		"""Finds and retrieves customTopologyNode data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyNode data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyNode data from the server.

		Args:
			BridgePriority (number): 
			EdgeBridge (bool): 
			Enabled (bool): 
			Nickname (number): 
			Priority (number): 
			SpSrcId (number): 

		Returns:
			self: This instance with matching customTopologyNode data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyNode data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyNode data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
