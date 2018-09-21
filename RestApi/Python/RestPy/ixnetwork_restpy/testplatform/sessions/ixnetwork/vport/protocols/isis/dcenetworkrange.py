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
		"""If true, this DCE ISIS Network Range is advertised.

		Returns:
			bool
		"""
		return self._get_attribute('advertiseNetworkRange')
	@AdvertiseNetworkRange.setter
	def AdvertiseNetworkRange(self, value):
		self._set_attribute('advertiseNetworkRange', value)

	@property
	def BroadcastRootPriorityStep(self):
		"""The increment step of the Broadcast Root Priority of this emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('broadcastRootPriorityStep')
	@BroadcastRootPriorityStep.setter
	def BroadcastRootPriorityStep(self, value):
		self._set_attribute('broadcastRootPriorityStep', value)

	@property
	def CapabilityRouterId(self):
		"""The IP address format of Capability Router.

		Returns:
			str
		"""
		return self._get_attribute('capabilityRouterId')
	@CapabilityRouterId.setter
	def CapabilityRouterId(self, value):
		self._set_attribute('capabilityRouterId', value)

	@property
	def EnableHostName(self):
		"""If true, the given dynamic host name is transmitted in all the packets sent from this router.

		Returns:
			bool
		"""
		return self._get_attribute('enableHostName')
	@EnableHostName.setter
	def EnableHostName(self, value):
		self._set_attribute('enableHostName', value)

	@property
	def EnableMultiTopology(self):
		"""Enables more than one topology (distribution tree) corresponding to the given R bridge.

		Returns:
			bool
		"""
		return self._get_attribute('enableMultiTopology')
	@EnableMultiTopology.setter
	def EnableMultiTopology(self, value):
		self._set_attribute('enableMultiTopology', value)

	@property
	def EntryCol(self):
		"""The value in this field is used in combination with entry row to specify which 'virtual' router in the Network Range is connected to the current ISIS L2/L3 Router.

		Returns:
			number
		"""
		return self._get_attribute('entryCol')
	@EntryCol.setter
	def EntryCol(self, value):
		self._set_attribute('entryCol', value)

	@property
	def EntryRow(self):
		"""The value in this field is used in combination with entry column to specify which 'virtual' router in the Network Range is connected to the current ISIS L2/L3 Router.

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

	@property
	def HostNamePrefix(self):
		"""Allows to add a prefix to the generated host name of this router. When host name prefix is provided, the generated host name is appended by -1 for the first router and subsequently increased by 1 for each router.

		Returns:
			str
		"""
		return self._get_attribute('hostNamePrefix')
	@HostNamePrefix.setter
	def HostNamePrefix(self, value):
		self._set_attribute('hostNamePrefix', value)

	@property
	def InterfaceMetric(self):
		"""The metric cost associated with this emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('interfaceMetric')
	@InterfaceMetric.setter
	def InterfaceMetric(self, value):
		self._set_attribute('interfaceMetric', value)

	@property
	def LinkType(self):
		"""For DCE ISIS emulation type, the type of network link is set to Point-Point and made read-only.

		Returns:
			str(pointToPoint|broadcast)
		"""
		return self._get_attribute('linkType')

	@property
	def NoOfCols(self):
		"""The value in this field is used in combination with number of rows to create a matrix (grid) for a network range.

		Returns:
			number
		"""
		return self._get_attribute('noOfCols')
	@NoOfCols.setter
	def NoOfCols(self, value):
		self._set_attribute('noOfCols', value)

	@property
	def NoOfRows(self):
		"""The value in this field is used in combination with number of columns to create a matrix (grid) for a network range.

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def NumberOfMultiDestinationTrees(self):
		"""The number of Multi-Destination Trees for the DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMultiDestinationTrees')
	@NumberOfMultiDestinationTrees.setter
	def NumberOfMultiDestinationTrees(self, value):
		self._set_attribute('numberOfMultiDestinationTrees', value)

	@property
	def StartBroadcastRootPriority(self):
		"""The starting value of the Broadcast Root Priority of this DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('startBroadcastRootPriority')
	@StartBroadcastRootPriority.setter
	def StartBroadcastRootPriority(self, value):
		self._set_attribute('startBroadcastRootPriority', value)

	@property
	def StartSwitchId(self):
		"""The Switch ID of this emulated DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('startSwitchId')
	@StartSwitchId.setter
	def StartSwitchId(self, value):
		self._set_attribute('startSwitchId', value)

	@property
	def StartSystemId(self):
		"""The System ID assigned to the starting DCE ISIS router in this network range.

		Returns:
			str
		"""
		return self._get_attribute('startSystemId')
	@StartSystemId.setter
	def StartSystemId(self, value):
		self._set_attribute('startSystemId', value)

	@property
	def SwitchIdPriority(self):
		"""The Switch ID priority of this DCE ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('switchIdPriority')
	@SwitchIdPriority.setter
	def SwitchIdPriority(self, value):
		self._set_attribute('switchIdPriority', value)

	@property
	def SwitchIdStep(self):
		"""The increment value by which the Switch ID of the DCE ISIS router increases.

		Returns:
			number
		"""
		return self._get_attribute('switchIdStep')
	@SwitchIdStep.setter
	def SwitchIdStep(self, value):
		self._set_attribute('switchIdStep', value)

	@property
	def SystemIdIncrementBy(self):
		"""The incremented System ID used when more than one router is emulated. The increment value is added to the previous System ID for each additional emulated router in this network range.

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
			AdvertiseNetworkRange (bool): If true, this DCE ISIS Network Range is advertised.
			BroadcastRootPriorityStep (number): The increment step of the Broadcast Root Priority of this emulated DCE ISIS router.
			CapabilityRouterId (str): The IP address format of Capability Router.
			EnableHostName (bool): If true, the given dynamic host name is transmitted in all the packets sent from this router.
			EnableMultiTopology (bool): Enables more than one topology (distribution tree) corresponding to the given R bridge.
			EntryCol (number): The value in this field is used in combination with entry row to specify which 'virtual' router in the Network Range is connected to the current ISIS L2/L3 Router.
			EntryRow (number): The value in this field is used in combination with entry column to specify which 'virtual' router in the Network Range is connected to the current ISIS L2/L3 Router.
			HostNamePrefix (str): Allows to add a prefix to the generated host name of this router. When host name prefix is provided, the generated host name is appended by -1 for the first router and subsequently increased by 1 for each router.
			InterfaceMetric (number): The metric cost associated with this emulated DCE ISIS router.
			NoOfCols (number): The value in this field is used in combination with number of rows to create a matrix (grid) for a network range.
			NoOfRows (number): The value in this field is used in combination with number of columns to create a matrix (grid) for a network range.
			NumberOfMultiDestinationTrees (number): The number of Multi-Destination Trees for the DCE ISIS router.
			StartBroadcastRootPriority (number): The starting value of the Broadcast Root Priority of this DCE ISIS router.
			StartSwitchId (number): The Switch ID of this emulated DCE ISIS router.
			StartSystemId (str): The System ID assigned to the starting DCE ISIS router in this network range.
			SwitchIdPriority (number): The Switch ID priority of this DCE ISIS router.
			SwitchIdStep (number): The increment value by which the Switch ID of the DCE ISIS router increases.
			SystemIdIncrementBy (str): The incremented System ID used when more than one router is emulated. The increment value is added to the previous System ID for each additional emulated router in this network range.

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
			AdvertiseNetworkRange (bool): If true, this DCE ISIS Network Range is advertised.
			BroadcastRootPriorityStep (number): The increment step of the Broadcast Root Priority of this emulated DCE ISIS router.
			CapabilityRouterId (str): The IP address format of Capability Router.
			EnableHostName (bool): If true, the given dynamic host name is transmitted in all the packets sent from this router.
			EnableMultiTopology (bool): Enables more than one topology (distribution tree) corresponding to the given R bridge.
			EntryCol (number): The value in this field is used in combination with entry row to specify which 'virtual' router in the Network Range is connected to the current ISIS L2/L3 Router.
			EntryRow (number): The value in this field is used in combination with entry column to specify which 'virtual' router in the Network Range is connected to the current ISIS L2/L3 Router.
			HostNamePrefix (str): Allows to add a prefix to the generated host name of this router. When host name prefix is provided, the generated host name is appended by -1 for the first router and subsequently increased by 1 for each router.
			InterfaceMetric (number): The metric cost associated with this emulated DCE ISIS router.
			LinkType (str(pointToPoint|broadcast)): For DCE ISIS emulation type, the type of network link is set to Point-Point and made read-only.
			NoOfCols (number): The value in this field is used in combination with number of rows to create a matrix (grid) for a network range.
			NoOfRows (number): The value in this field is used in combination with number of columns to create a matrix (grid) for a network range.
			NumberOfMultiDestinationTrees (number): The number of Multi-Destination Trees for the DCE ISIS router.
			StartBroadcastRootPriority (number): The starting value of the Broadcast Root Priority of this DCE ISIS router.
			StartSwitchId (number): The Switch ID of this emulated DCE ISIS router.
			StartSystemId (str): The System ID assigned to the starting DCE ISIS router in this network range.
			SwitchIdPriority (number): The Switch ID priority of this DCE ISIS router.
			SwitchIdStep (number): The increment value by which the Switch ID of the DCE ISIS router increases.
			SystemIdIncrementBy (str): The incremented System ID used when more than one router is emulated. The increment value is added to the previous System ID for each additional emulated router in this network range.

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
