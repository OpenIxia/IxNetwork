
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


class Msti(Base):
	"""The Msti class encapsulates a user managed msti node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Msti property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'msti'

	def __init__(self, parent):
		super(Msti, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def LearnedInterface(self):
		"""An instance of the LearnedInterface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinterface.learnedinterface.LearnedInterface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.learnedinterface.learnedinterface import LearnedInterface
		return LearnedInterface(self)

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
	def InternalRootPathCost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('internalRootPathCost')
	@InternalRootPathCost.setter
	def InternalRootPathCost(self, value):
		self._set_attribute('internalRootPathCost', value)

	@property
	def Mac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mac')
	@Mac.setter
	def Mac(self, value):
		self._set_attribute('mac', value)

	@property
	def MstiHops(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mstiHops')
	@MstiHops.setter
	def MstiHops(self, value):
		self._set_attribute('mstiHops', value)

	@property
	def MstiId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mstiId')
	@MstiId.setter
	def MstiId(self, value):
		self._set_attribute('mstiId', value)

	@property
	def MstiName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mstiName')
	@MstiName.setter
	def MstiName(self, value):
		self._set_attribute('mstiName', value)

	@property
	def PortPriority(self):
		"""

		Returns:
			str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)
		"""
		return self._get_attribute('portPriority')
	@PortPriority.setter
	def PortPriority(self, value):
		self._set_attribute('portPriority', value)

	@property
	def Priority(self):
		"""

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def UpdateRequired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')
	@UpdateRequired.setter
	def UpdateRequired(self, value):
		self._set_attribute('updateRequired', value)

	@property
	def VlanStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanStart')
	@VlanStart.setter
	def VlanStart(self, value):
		self._set_attribute('vlanStart', value)

	@property
	def VlanStop(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanStop')
	@VlanStop.setter
	def VlanStop(self, value):
		self._set_attribute('vlanStop', value)

	def add(self, Enabled=None, InternalRootPathCost=None, Mac=None, MstiHops=None, MstiId=None, MstiName=None, PortPriority=None, Priority=None, UpdateRequired=None, VlanStart=None, VlanStop=None):
		"""Adds a new msti node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			InternalRootPathCost (number): 
			Mac (str): 
			MstiHops (number): 
			MstiId (number): 
			MstiName (str): 
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): 
			Priority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			UpdateRequired (bool): 
			VlanStart (number): 
			VlanStop (number): 

		Returns:
			self: This instance with all currently retrieved msti data using find and the newly added msti data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the msti data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InternalRootPathCost=None, Mac=None, MstiHops=None, MstiId=None, MstiName=None, PortPriority=None, Priority=None, UpdateRequired=None, VlanStart=None, VlanStop=None):
		"""Finds and retrieves msti data from the server.

		All named parameters support regex and can be used to selectively retrieve msti data from the server.
		By default the find method takes no parameters and will retrieve all msti data from the server.

		Args:
			Enabled (bool): 
			InternalRootPathCost (number): 
			Mac (str): 
			MstiHops (number): 
			MstiId (number): 
			MstiName (str): 
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): 
			Priority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): 
			UpdateRequired (bool): 
			VlanStart (number): 
			VlanStop (number): 

		Returns:
			self: This instance with matching msti data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of msti data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the msti data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def TopologyChange(self):
		"""Executes the topologyChange operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('TopologyChange', payload=locals(), response_object=None)

	def UpdateParameters(self):
		"""Executes the updateParameters operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
