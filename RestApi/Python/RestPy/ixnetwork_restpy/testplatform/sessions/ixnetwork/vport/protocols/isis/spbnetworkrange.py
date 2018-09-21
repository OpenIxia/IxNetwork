from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbNetworkRange(Base):
	"""The SpbNetworkRange class encapsulates a user managed spbNetworkRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbNetworkRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbNetworkRange'

	def __init__(self, parent):
		super(SpbNetworkRange, self).__init__(parent)

	@property
	def SpbOutsideLinks(self):
		"""An instance of the SpbOutsideLinks class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spboutsidelinks.SpbOutsideLinks)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spboutsidelinks import SpbOutsideLinks
		return SpbOutsideLinks(self)

	@property
	def SpbmNodeTopologyRange(self):
		"""An instance of the SpbmNodeTopologyRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodetopologyrange.SpbmNodeTopologyRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodetopologyrange import SpbmNodeTopologyRange
		return SpbmNodeTopologyRange(self)

	@property
	def EnableAdvertiseNetworkRange(self):
		"""If true, this SPB ISIS Network Range is advertised.

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvertiseNetworkRange')
	@EnableAdvertiseNetworkRange.setter
	def EnableAdvertiseNetworkRange(self, value):
		self._set_attribute('enableAdvertiseNetworkRange', value)

	@property
	def EnableHostName(self):
		"""If true, the host name of the router is activated.

		Returns:
			bool
		"""
		return self._get_attribute('enableHostName')
	@EnableHostName.setter
	def EnableHostName(self, value):
		self._set_attribute('enableHostName', value)

	@property
	def EntryColumn(self):
		"""The value is used in combination to specify which virtual router in the Network Range is connected to the current ISIS L2/L3 Router.

		Returns:
			number
		"""
		return self._get_attribute('entryColumn')
	@EntryColumn.setter
	def EntryColumn(self, value):
		self._set_attribute('entryColumn', value)

	@property
	def EntryRow(self):
		"""The value is used in combination to specify which virtual router in the Network Range is connected to the current ISIS L2/L3 Router.

		Returns:
			number
		"""
		return self._get_attribute('entryRow')
	@EntryRow.setter
	def EntryRow(self, value):
		self._set_attribute('entryRow', value)

	@property
	def HostNamePrefix(self):
		"""The host name prefix information.

		Returns:
			str
		"""
		return self._get_attribute('hostNamePrefix')
	@HostNamePrefix.setter
	def HostNamePrefix(self, value):
		self._set_attribute('hostNamePrefix', value)

	@property
	def InterfaceMetric(self):
		"""The metric cost associated with this emulated SPB ISIS router.

		Returns:
			number
		"""
		return self._get_attribute('interfaceMetric')
	@InterfaceMetric.setter
	def InterfaceMetric(self, value):
		self._set_attribute('interfaceMetric', value)

	@property
	def NoOfColumns(self):
		"""The value is used in combination to create a matrix (grid) for an emulated network range of the following size: The # Rows multiplied the # Cols = Number of routers in this Network Range. (For example, 3 Rows x 3 Columns = 9 Routers).

		Returns:
			number
		"""
		return self._get_attribute('noOfColumns')
	@NoOfColumns.setter
	def NoOfColumns(self, value):
		self._set_attribute('noOfColumns', value)

	@property
	def NoOfRows(self):
		"""The value is used in combination to create a matrix (grid) for an emulated network range of the following size: The # Rows multiplied the # Cols = Number of routers in this Network Range. (For example, 3 Rows x 3 Columns = 9 Routers).

		Returns:
			number
		"""
		return self._get_attribute('noOfRows')
	@NoOfRows.setter
	def NoOfRows(self, value):
		self._set_attribute('noOfRows', value)

	@property
	def StartSystemId(self):
		"""The System ID assigned to the starting SPB ISIS router in this network range. The default is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('startSystemId')
	@StartSystemId.setter
	def StartSystemId(self, value):
		self._set_attribute('startSystemId', value)

	@property
	def SystemIdIncrementBy(self):
		"""This is used when more than one router is to be emulated. The increment value is added to the previous System ID for each additional emulated router in this network range.

		Returns:
			str
		"""
		return self._get_attribute('systemIdIncrementBy')
	@SystemIdIncrementBy.setter
	def SystemIdIncrementBy(self, value):
		self._set_attribute('systemIdIncrementBy', value)

	def add(self, EnableAdvertiseNetworkRange=None, EnableHostName=None, EntryColumn=None, EntryRow=None, HostNamePrefix=None, InterfaceMetric=None, NoOfColumns=None, NoOfRows=None, StartSystemId=None, SystemIdIncrementBy=None):
		"""Adds a new spbNetworkRange node on the server and retrieves it in this instance.

		Args:
			EnableAdvertiseNetworkRange (bool): If true, this SPB ISIS Network Range is advertised.
			EnableHostName (bool): If true, the host name of the router is activated.
			EntryColumn (number): The value is used in combination to specify which virtual router in the Network Range is connected to the current ISIS L2/L3 Router.
			EntryRow (number): The value is used in combination to specify which virtual router in the Network Range is connected to the current ISIS L2/L3 Router.
			HostNamePrefix (str): The host name prefix information.
			InterfaceMetric (number): The metric cost associated with this emulated SPB ISIS router.
			NoOfColumns (number): The value is used in combination to create a matrix (grid) for an emulated network range of the following size: The # Rows multiplied the # Cols = Number of routers in this Network Range. (For example, 3 Rows x 3 Columns = 9 Routers).
			NoOfRows (number): The value is used in combination to create a matrix (grid) for an emulated network range of the following size: The # Rows multiplied the # Cols = Number of routers in this Network Range. (For example, 3 Rows x 3 Columns = 9 Routers).
			StartSystemId (str): The System ID assigned to the starting SPB ISIS router in this network range. The default is 00 00 00 00 00 00.
			SystemIdIncrementBy (str): This is used when more than one router is to be emulated. The increment value is added to the previous System ID for each additional emulated router in this network range.

		Returns:
			self: This instance with all currently retrieved spbNetworkRange data using find and the newly added spbNetworkRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbNetworkRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableAdvertiseNetworkRange=None, EnableHostName=None, EntryColumn=None, EntryRow=None, HostNamePrefix=None, InterfaceMetric=None, NoOfColumns=None, NoOfRows=None, StartSystemId=None, SystemIdIncrementBy=None):
		"""Finds and retrieves spbNetworkRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbNetworkRange data from the server.
		By default the find method takes no parameters and will retrieve all spbNetworkRange data from the server.

		Args:
			EnableAdvertiseNetworkRange (bool): If true, this SPB ISIS Network Range is advertised.
			EnableHostName (bool): If true, the host name of the router is activated.
			EntryColumn (number): The value is used in combination to specify which virtual router in the Network Range is connected to the current ISIS L2/L3 Router.
			EntryRow (number): The value is used in combination to specify which virtual router in the Network Range is connected to the current ISIS L2/L3 Router.
			HostNamePrefix (str): The host name prefix information.
			InterfaceMetric (number): The metric cost associated with this emulated SPB ISIS router.
			NoOfColumns (number): The value is used in combination to create a matrix (grid) for an emulated network range of the following size: The # Rows multiplied the # Cols = Number of routers in this Network Range. (For example, 3 Rows x 3 Columns = 9 Routers).
			NoOfRows (number): The value is used in combination to create a matrix (grid) for an emulated network range of the following size: The # Rows multiplied the # Cols = Number of routers in this Network Range. (For example, 3 Rows x 3 Columns = 9 Routers).
			StartSystemId (str): The System ID assigned to the starting SPB ISIS router in this network range. The default is 00 00 00 00 00 00.
			SystemIdIncrementBy (str): This is used when more than one router is to be emulated. The increment value is added to the previous System ID for each additional emulated router in this network range.

		Returns:
			self: This instance with matching spbNetworkRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbNetworkRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbNetworkRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
