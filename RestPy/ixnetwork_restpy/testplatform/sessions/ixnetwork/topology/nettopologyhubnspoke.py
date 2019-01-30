
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


class NetTopologyHubNSpoke(Base):
	"""The NetTopologyHubNSpoke class encapsulates a user managed netTopologyHubNSpoke node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetTopologyHubNSpoke property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'netTopologyHubNSpoke'

	def __init__(self, parent):
		super(NetTopologyHubNSpoke, self).__init__(parent)

	@property
	def EnableLevel2Spokes(self):
		"""Enable Level 2 Spokes

		Returns:
			bool
		"""
		return self._get_attribute('enableLevel2Spokes')
	@EnableLevel2Spokes.setter
	def EnableLevel2Spokes(self, value):
		self._set_attribute('enableLevel2Spokes', value)

	@property
	def IncludeEntryPoint(self):
		"""if true, entry node belongs to ring topology, otherwise it is outside of ring

		Returns:
			bool
		"""
		return self._get_attribute('includeEntryPoint')
	@IncludeEntryPoint.setter
	def IncludeEntryPoint(self, value):
		self._set_attribute('includeEntryPoint', value)

	@property
	def LinkMultiplier(self):
		"""number of links between two nodes

		Returns:
			number
		"""
		return self._get_attribute('linkMultiplier')
	@LinkMultiplier.setter
	def LinkMultiplier(self, value):
		self._set_attribute('linkMultiplier', value)

	@property
	def NumberOfFirstLevelSpokes(self):
		"""Number of First Level Spokes

		Returns:
			number
		"""
		return self._get_attribute('numberOfFirstLevelSpokes')
	@NumberOfFirstLevelSpokes.setter
	def NumberOfFirstLevelSpokes(self, value):
		self._set_attribute('numberOfFirstLevelSpokes', value)

	@property
	def NumberOfSecondLevelSpokes(self):
		"""Number of Second Level Spokes

		Returns:
			number
		"""
		return self._get_attribute('numberOfSecondLevelSpokes')
	@NumberOfSecondLevelSpokes.setter
	def NumberOfSecondLevelSpokes(self, value):
		self._set_attribute('numberOfSecondLevelSpokes', value)

	def add(self, EnableLevel2Spokes=None, IncludeEntryPoint=None, LinkMultiplier=None, NumberOfFirstLevelSpokes=None, NumberOfSecondLevelSpokes=None):
		"""Adds a new netTopologyHubNSpoke node on the server and retrieves it in this instance.

		Args:
			EnableLevel2Spokes (bool): Enable Level 2 Spokes
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			NumberOfFirstLevelSpokes (number): Number of First Level Spokes
			NumberOfSecondLevelSpokes (number): Number of Second Level Spokes

		Returns:
			self: This instance with all currently retrieved netTopologyHubNSpoke data using find and the newly added netTopologyHubNSpoke data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the netTopologyHubNSpoke data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableLevel2Spokes=None, IncludeEntryPoint=None, LinkMultiplier=None, NumberOfFirstLevelSpokes=None, NumberOfSecondLevelSpokes=None):
		"""Finds and retrieves netTopologyHubNSpoke data from the server.

		All named parameters support regex and can be used to selectively retrieve netTopologyHubNSpoke data from the server.
		By default the find method takes no parameters and will retrieve all netTopologyHubNSpoke data from the server.

		Args:
			EnableLevel2Spokes (bool): Enable Level 2 Spokes
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			NumberOfFirstLevelSpokes (number): Number of First Level Spokes
			NumberOfSecondLevelSpokes (number): Number of Second Level Spokes

		Returns:
			self: This instance with matching netTopologyHubNSpoke data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of netTopologyHubNSpoke data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the netTopologyHubNSpoke data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
