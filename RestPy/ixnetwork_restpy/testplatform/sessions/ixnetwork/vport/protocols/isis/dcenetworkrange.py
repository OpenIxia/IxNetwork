
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


class DceNetworkRange(Base):
	"""The DceNetworkRange class encapsulates a user managed dceNetworkRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceNetworkRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceNetworkRange'

	def __init__(self, parent):
		super(DceNetworkRange, self).__init__(parent)

	@property
	def DceNodeIpv4Groups(self):
		"""An instance of the DceNodeIpv4Groups class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodeipv4groups.DceNodeIpv4Groups)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodeipv4groups import DceNodeIpv4Groups
		return DceNodeIpv4Groups(self)

	@property
	def DceNodeIpv6Groups(self):
		"""An instance of the DceNodeIpv6Groups class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodeipv6groups.DceNodeIpv6Groups)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodeipv6groups import DceNodeIpv6Groups
		return DceNodeIpv6Groups(self)

	@property
	def DceNodeMacGroups(self):
		"""An instance of the DceNodeMacGroups class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodemacgroups.DceNodeMacGroups)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodemacgroups import DceNodeMacGroups
		return DceNodeMacGroups(self)

	@property
	def DceNodeTopologyRange(self):
		"""An instance of the DceNodeTopologyRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodetopologyrange.DceNodeTopologyRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dcenodetopologyrange import DceNodeTopologyRange
		return DceNodeTopologyRange(self)

	@property
	def DceOutsideLinks(self):
		"""An instance of the DceOutsideLinks class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dceoutsidelinks.DceOutsideLinks)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dceoutsidelinks import DceOutsideLinks
		return DceOutsideLinks(self)

	@property
	def TrillNodeMacRanges(self):
		"""An instance of the TrillNodeMacRanges class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillnodemacranges.TrillNodeMacRanges)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillnodemacranges import TrillNodeMacRanges
		return TrillNodeMacRanges(self)

	@property
	def AdvertiseNetworkRange(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('advertiseNetworkRange')
	@AdvertiseNetworkRange.setter
	def AdvertiseNetworkRange(self, value):
		self._set_attribute('advertiseNetworkRange', value)

	@property
	def BroadcastRootPriorityStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('broadcastRootPriorityStep')
	@BroadcastRootPriorityStep.setter
	def BroadcastRootPriorityStep(self, value):
		self._set_attribute('broadcastRootPriorityStep', value)

	@property
	def CapabilityRouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('capabilityRouterId')
	@CapabilityRouterId.setter
	def CapabilityRouterId(self, value):
		self._set_attribute('capabilityRouterId', value)

	@property
	def EnableHostName(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHostName')
	@EnableHostName.setter
	def EnableHostName(self, value):
		self._set_attribute('enableHostName', value)

	@property
	def EnableMultiTopology(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMultiTopology')
	@EnableMultiTopology.setter
	def EnableMultiTopology(self, value):
		self._set_attribute('enableMultiTopology', value)

	@property
	def EntryCol(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('entryCol')
	@EntryCol.setter
	def EntryCol(self, value):
		self._set_attribute('entryCol', value)

	@property
	def EntryRow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

	@property
	def HostNamePrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('hostNamePrefix')
	@HostNamePrefix.setter
	def HostNamePrefix(self, value):
		self._set_attribute('hostNamePrefix', value)

	@property
	def InterfaceMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceMetric')
	@InterfaceMetric.setter
	def InterfaceMetric(self, value):
		self._set_attribute('interfaceMetric', value)

	@property
	def LinkType(self):
		"""

		Returns:
			str(pointToPoint|broadcast)
		"""
		return self._get_attribute('linkType')

	@property
	def NoOfCols(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfCols')
	@NoOfCols.setter
	def NoOfCols(self, value):
		self._set_attribute('noOfCols', value)

	@property
	def NoOfRows(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def NumberOfMultiDestinationTrees(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfMultiDestinationTrees')
	@NumberOfMultiDestinationTrees.setter
	def NumberOfMultiDestinationTrees(self, value):
		self._set_attribute('numberOfMultiDestinationTrees', value)

	@property
	def StartBroadcastRootPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startBroadcastRootPriority')
	@StartBroadcastRootPriority.setter
	def StartBroadcastRootPriority(self, value):
		self._set_attribute('startBroadcastRootPriority', value)

	@property
	def StartSwitchId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startSwitchId')
	@StartSwitchId.setter
	def StartSwitchId(self, value):
		self._set_attribute('startSwitchId', value)

	@property
	def StartSystemId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startSystemId')
	@StartSystemId.setter
	def StartSystemId(self, value):
		self._set_attribute('startSystemId', value)

	@property
	def SwitchIdPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchIdPriority')
	@SwitchIdPriority.setter
	def SwitchIdPriority(self, value):
		self._set_attribute('switchIdPriority', value)

	@property
	def SwitchIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('switchIdStep')
	@SwitchIdStep.setter
	def SwitchIdStep(self, value):
		self._set_attribute('switchIdStep', value)

	@property
	def SystemIdIncrementBy(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('systemIdIncrementBy')
	@SystemIdIncrementBy.setter
	def SystemIdIncrementBy(self, value):
		self._set_attribute('systemIdIncrementBy', value)

	def add(self, AdvertiseNetworkRange=None, BroadcastRootPriorityStep=None, CapabilityRouterId=None, EnableHostName=None, EnableMultiTopology=None, EntryCol=None, EntryRow=None, HostNamePrefix=None, InterfaceMetric=None, NoOfCols=None, NoOfRows=None, NumberOfMultiDestinationTrees=None, StartBroadcastRootPriority=None, StartSwitchId=None, StartSystemId=None, SwitchIdPriority=None, SwitchIdStep=None, SystemIdIncrementBy=None):
		"""Adds a new dceNetworkRange node on the server and retrieves it in this instance.

		Args:
			AdvertiseNetworkRange (bool): 
			BroadcastRootPriorityStep (number): 
			CapabilityRouterId (str): 
			EnableHostName (bool): 
			EnableMultiTopology (bool): 
			EntryCol (number): 
			EntryRow (number): 
			HostNamePrefix (str): 
			InterfaceMetric (number): 
			NoOfCols (number): 
			NoOfRows (number): 
			NumberOfMultiDestinationTrees (number): 
			StartBroadcastRootPriority (number): 
			StartSwitchId (number): 
			StartSystemId (str): 
			SwitchIdPriority (number): 
			SwitchIdStep (number): 
			SystemIdIncrementBy (str): 

		Returns:
			self: This instance with all currently retrieved dceNetworkRange data using find and the newly added dceNetworkRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceNetworkRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertiseNetworkRange=None, BroadcastRootPriorityStep=None, CapabilityRouterId=None, EnableHostName=None, EnableMultiTopology=None, EntryCol=None, EntryRow=None, HostNamePrefix=None, InterfaceMetric=None, LinkType=None, NoOfCols=None, NoOfRows=None, NumberOfMultiDestinationTrees=None, StartBroadcastRootPriority=None, StartSwitchId=None, StartSystemId=None, SwitchIdPriority=None, SwitchIdStep=None, SystemIdIncrementBy=None):
		"""Finds and retrieves dceNetworkRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceNetworkRange data from the server.
		By default the find method takes no parameters and will retrieve all dceNetworkRange data from the server.

		Args:
			AdvertiseNetworkRange (bool): 
			BroadcastRootPriorityStep (number): 
			CapabilityRouterId (str): 
			EnableHostName (bool): 
			EnableMultiTopology (bool): 
			EntryCol (number): 
			EntryRow (number): 
			HostNamePrefix (str): 
			InterfaceMetric (number): 
			LinkType (str(pointToPoint|broadcast)): 
			NoOfCols (number): 
			NoOfRows (number): 
			NumberOfMultiDestinationTrees (number): 
			StartBroadcastRootPriority (number): 
			StartSwitchId (number): 
			StartSystemId (str): 
			SwitchIdPriority (number): 
			SwitchIdStep (number): 
			SystemIdIncrementBy (str): 

		Returns:
			self: This instance with matching dceNetworkRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceNetworkRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceNetworkRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
