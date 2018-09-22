from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetworkRange(Base):
	"""The NetworkRange class encapsulates a user managed networkRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetworkRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'networkRange'

	def __init__(self, parent):
		super(NetworkRange, self).__init__(parent)

	@property
	def EntryTe(self):
		"""An instance of the EntryTe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.entryte.EntryTe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.entryte import EntryTe
		return EntryTe(self)._select()

	@property
	def RangeTe(self):
		"""An instance of the RangeTe class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.rangete.RangeTe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.rangete import RangeTe
		return RangeTe(self)._select()

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
	def Enabled(self):
		"""If enabled, this route range will be advertised by the nodes in the network range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EntryCol(self):
		"""The simulated router is connected to a router in the grid at a particular row and column location. This option is the column number. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('entryCol')
	@EntryCol.setter
	def EntryCol(self, value):
		self._set_attribute('entryCol', value)

	@property
	def EntryRow(self):
		"""The simulated router is connected to a router in the grid at a particular row and column location. This option is the row number. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

	@property
	def GridNodeRoutes(self):
		"""The set of advertised networks within the grid to be included in isisGrid.

		Returns:
			list(dict(arg1:bool,arg2:str[ipAny|ipv4|ipv6],arg3:str,arg4:number,arg5:number,arg6:number,arg7:number,arg8:bool,arg9:bool,arg10:number))
		"""
		return self._get_attribute('gridNodeRoutes')
	@GridNodeRoutes.setter
	def GridNodeRoutes(self, value):
		self._set_attribute('gridNodeRoutes', value)

	@property
	def GridOutsideExLinks(self):
		"""NOT DEFINED

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str,arg4:list[dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number)],arg5:str,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number))
		"""
		return self._get_attribute('gridOutsideExLinks')
	@GridOutsideExLinks.setter
	def GridOutsideExLinks(self, value):
		self._set_attribute('gridOutsideExLinks', value)

	@property
	def GridOutsideLinks(self):
		"""Sets up the outside links between an ISIS grid and another ISIS grid.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str,arg4:str,arg5:number,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number))
		"""
		return self._get_attribute('gridOutsideLinks')
	@GridOutsideLinks.setter
	def GridOutsideLinks(self, value):
		self._set_attribute('gridOutsideLinks', value)

	@property
	def HostNamePrefix(self):
		"""Allows to add a host name to this network range. The name prefix is appended by row ID and column ID in .<rowid>.<colid> combination as per the router placed in the emulated network grid behind the Ixia port.

		Returns:
			str
		"""
		return self._get_attribute('hostNamePrefix')
	@HostNamePrefix.setter
	def HostNamePrefix(self, value):
		self._set_attribute('hostNamePrefix', value)

	@property
	def InterfaceIps(self):
		"""The interface IP information for the simulated network.

		Returns:
			list(dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number))
		"""
		return self._get_attribute('interfaceIps')
	@InterfaceIps.setter
	def InterfaceIps(self, value):
		self._set_attribute('interfaceIps', value)

	@property
	def InterfaceMetric(self):
		"""The metric cost associated with this emulated ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('interfaceMetric')
	@InterfaceMetric.setter
	def InterfaceMetric(self, value):
		self._set_attribute('interfaceMetric', value)

	@property
	def Ipv6MtMetric(self):
		"""This metric is same as the Interface Metric. If enabled, it allows you to enter data.

		Returns:
			number
		"""
		return self._get_attribute('ipv6MtMetric')
	@Ipv6MtMetric.setter
	def Ipv6MtMetric(self, value):
		self._set_attribute('ipv6MtMetric', value)

	@property
	def LinkType(self):
		"""The type of network link for this emulated ISIS router.

		Returns:
			str(pointToPoint|broadcast)
		"""
		return self._get_attribute('linkType')
	@LinkType.setter
	def LinkType(self, value):
		self._set_attribute('linkType', value)

	@property
	def NoOfCols(self):
		"""The number of columns in the simulated grid. (default = 3)

		Returns:
			number
		"""
		return self._get_attribute('noOfCols')
	@NoOfCols.setter
	def NoOfCols(self, value):
		self._set_attribute('noOfCols', value)

	@property
	def NoOfRows(self):
		"""The number of rows in the simulated grid. (default = 3)

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def RouterId(self):
		"""The router ID for the first emulated ISIS router in this network range.

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def RouterIdIncrement(self):
		"""The increment step to be used for creating the router IDs for the emulated ISIS routers in this network range.

		Returns:
			str
		"""
		return self._get_attribute('routerIdIncrement')
	@RouterIdIncrement.setter
	def RouterIdIncrement(self, value):
		self._set_attribute('routerIdIncrement', value)

	@property
	def TePaths(self):
		"""Adds a Traffic Engineering (TE) Path to the list.

		Returns:
			list(dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:bool,arg8:str,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number,arg17:number,arg18:number,arg19:number))
		"""
		return self._get_attribute('tePaths')
	@TePaths.setter
	def TePaths(self, value):
		self._set_attribute('tePaths', value)

	@property
	def UseWideMetric(self):
		"""Enables the use of extended reachability (wide) metrics (defined to support TE): 32-bits wide for IP reachability (IP routes) and 24-bits wide for IS reachability (IS neighbors). If TE is enabled, Wide Metrics will be enabled automatically. The Wide Metrics may be used without enabling TE, however.

		Returns:
			bool
		"""
		return self._get_attribute('useWideMetric')
	@UseWideMetric.setter
	def UseWideMetric(self, value):
		self._set_attribute('useWideMetric', value)

	def add(self, EnableHostName=None, Enabled=None, EntryCol=None, EntryRow=None, GridNodeRoutes=None, GridOutsideExLinks=None, GridOutsideLinks=None, HostNamePrefix=None, InterfaceIps=None, InterfaceMetric=None, Ipv6MtMetric=None, LinkType=None, NoOfCols=None, NoOfRows=None, RouterId=None, RouterIdIncrement=None, TePaths=None, UseWideMetric=None):
		"""Adds a new networkRange node on the server and retrieves it in this instance.

		Args:
			EnableHostName (bool): If true, the given dynamic host name is transmitted in all the packets sent from this router.
			Enabled (bool): If enabled, this route range will be advertised by the nodes in the network range.
			EntryCol (number): The simulated router is connected to a router in the grid at a particular row and column location. This option is the column number. (default = 1)
			EntryRow (number): The simulated router is connected to a router in the grid at a particular row and column location. This option is the row number. (default = 1)
			GridNodeRoutes (list(dict(arg1:bool,arg2:str[ipAny|ipv4|ipv6],arg3:str,arg4:number,arg5:number,arg6:number,arg7:number,arg8:bool,arg9:bool,arg10:number))): The set of advertised networks within the grid to be included in isisGrid.
			GridOutsideExLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:list[dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number)],arg5:str,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number))): NOT DEFINED
			GridOutsideLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:str,arg5:number,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number))): Sets up the outside links between an ISIS grid and another ISIS grid.
			HostNamePrefix (str): Allows to add a host name to this network range. The name prefix is appended by row ID and column ID in .<rowid>.<colid> combination as per the router placed in the emulated network grid behind the Ixia port.
			InterfaceIps (list(dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number))): The interface IP information for the simulated network.
			InterfaceMetric (number): The metric cost associated with this emulated ISIS router.
			Ipv6MtMetric (number): This metric is same as the Interface Metric. If enabled, it allows you to enter data.
			LinkType (str(pointToPoint|broadcast)): The type of network link for this emulated ISIS router.
			NoOfCols (number): The number of columns in the simulated grid. (default = 3)
			NoOfRows (number): The number of rows in the simulated grid. (default = 3)
			RouterId (str): The router ID for the first emulated ISIS router in this network range.
			RouterIdIncrement (str): The increment step to be used for creating the router IDs for the emulated ISIS routers in this network range.
			TePaths (list(dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:bool,arg8:str,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number,arg17:number,arg18:number,arg19:number))): Adds a Traffic Engineering (TE) Path to the list.
			UseWideMetric (bool): Enables the use of extended reachability (wide) metrics (defined to support TE): 32-bits wide for IP reachability (IP routes) and 24-bits wide for IS reachability (IS neighbors). If TE is enabled, Wide Metrics will be enabled automatically. The Wide Metrics may be used without enabling TE, however.

		Returns:
			self: This instance with all currently retrieved networkRange data using find and the newly added networkRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the networkRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableHostName=None, Enabled=None, EntryCol=None, EntryRow=None, GridNodeRoutes=None, GridOutsideExLinks=None, GridOutsideLinks=None, HostNamePrefix=None, InterfaceIps=None, InterfaceMetric=None, Ipv6MtMetric=None, LinkType=None, NoOfCols=None, NoOfRows=None, RouterId=None, RouterIdIncrement=None, TePaths=None, UseWideMetric=None):
		"""Finds and retrieves networkRange data from the server.

		All named parameters support regex and can be used to selectively retrieve networkRange data from the server.
		By default the find method takes no parameters and will retrieve all networkRange data from the server.

		Args:
			EnableHostName (bool): If true, the given dynamic host name is transmitted in all the packets sent from this router.
			Enabled (bool): If enabled, this route range will be advertised by the nodes in the network range.
			EntryCol (number): The simulated router is connected to a router in the grid at a particular row and column location. This option is the column number. (default = 1)
			EntryRow (number): The simulated router is connected to a router in the grid at a particular row and column location. This option is the row number. (default = 1)
			GridNodeRoutes (list(dict(arg1:bool,arg2:str[ipAny|ipv4|ipv6],arg3:str,arg4:number,arg5:number,arg6:number,arg7:number,arg8:bool,arg9:bool,arg10:number))): The set of advertised networks within the grid to be included in isisGrid.
			GridOutsideExLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:list[dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number)],arg5:str,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number))): NOT DEFINED
			GridOutsideLinks (list(dict(arg1:number,arg2:number,arg3:str,arg4:str,arg5:number,arg6:number,arg7:number,arg8:number,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number))): Sets up the outside links between an ISIS grid and another ISIS grid.
			HostNamePrefix (str): Allows to add a host name to this network range. The name prefix is appended by row ID and column ID in .<rowid>.<colid> combination as per the router placed in the emulated network grid behind the Ixia port.
			InterfaceIps (list(dict(arg1:str[ipAny|ipv4|ipv6],arg2:str,arg3:number))): The interface IP information for the simulated network.
			InterfaceMetric (number): The metric cost associated with this emulated ISIS router.
			Ipv6MtMetric (number): This metric is same as the Interface Metric. If enabled, it allows you to enter data.
			LinkType (str(pointToPoint|broadcast)): The type of network link for this emulated ISIS router.
			NoOfCols (number): The number of columns in the simulated grid. (default = 3)
			NoOfRows (number): The number of rows in the simulated grid. (default = 3)
			RouterId (str): The router ID for the first emulated ISIS router in this network range.
			RouterIdIncrement (str): The increment step to be used for creating the router IDs for the emulated ISIS routers in this network range.
			TePaths (list(dict(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number,arg7:bool,arg8:str,arg9:number,arg10:number,arg11:number,arg12:number,arg13:number,arg14:number,arg15:number,arg16:number,arg17:number,arg18:number,arg19:number))): Adds a Traffic Engineering (TE) Path to the list.
			UseWideMetric (bool): Enables the use of extended reachability (wide) metrics (defined to support TE): 32-bits wide for IP reachability (IP routes) and 24-bits wide for IS reachability (IS neighbors). If TE is enabled, Wide Metrics will be enabled automatically. The Wide Metrics may be used without enabling TE, however.

		Returns:
			self: This instance with matching networkRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of networkRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the networkRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
