from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpaqueRouteRange(Base):
	"""The OpaqueRouteRange class encapsulates a user managed opaqueRouteRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpaqueRouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'opaqueRouteRange'

	def __init__(self, parent):
		super(OpaqueRouteRange, self).__init__(parent)

	@property
	def __id__(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('__id__')
	@__id__.setter
	def __id__(self, value):
		self._set_attribute('__id__', value)

	@property
	def Enabled(self):
		"""Appends the local AsNumber.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ImportedFile(self):
		"""Location of the route import file.

		Returns:
			str
		"""
		return self._get_attribute('importedFile')
	@ImportedFile.setter
	def ImportedFile(self, value):
		self._set_attribute('importedFile', value)

	@property
	def NextHopAsIs(self):
		"""If true, it takes the next Hop AsIs.

		Returns:
			bool
		"""
		return self._get_attribute('nextHopAsIs')
	@NextHopAsIs.setter
	def NextHopAsIs(self, value):
		self._set_attribute('nextHopAsIs', value)

	@property
	def NumberOfRoutes(self):
		"""Total number of opaque routes.

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoutes')
	@NumberOfRoutes.setter
	def NumberOfRoutes(self, value):
		self._set_attribute('numberOfRoutes', value)

	@property
	def SendMultiExitDiscovery(self):
		"""If true, sends a Multi Exit Discriminator attribute with the indicated value.

		Returns:
			bool
		"""
		return self._get_attribute('sendMultiExitDiscovery')
	@SendMultiExitDiscovery.setter
	def SendMultiExitDiscovery(self, value):
		self._set_attribute('sendMultiExitDiscovery', value)

	@property
	def Status(self):
		"""Indicates the status of the imported file.

		Returns:
			str
		"""
		return self._get_attribute('status')

	def add(self, __id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None):
		"""Adds a new opaqueRouteRange node on the server and retrieves it in this instance.

		Args:
			__id__ (str): NOT DEFINED
			Enabled (bool): Appends the local AsNumber.
			ImportedFile (str): Location of the route import file.
			NextHopAsIs (bool): If true, it takes the next Hop AsIs.
			NumberOfRoutes (number): Total number of opaque routes.
			SendMultiExitDiscovery (bool): If true, sends a Multi Exit Discriminator attribute with the indicated value.

		Returns:
			self: This instance with all currently retrieved opaqueRouteRange data using find and the newly added opaqueRouteRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the opaqueRouteRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, __id__=None, Enabled=None, ImportedFile=None, NextHopAsIs=None, NumberOfRoutes=None, SendMultiExitDiscovery=None, Status=None):
		"""Finds and retrieves opaqueRouteRange data from the server.

		All named parameters support regex and can be used to selectively retrieve opaqueRouteRange data from the server.
		By default the find method takes no parameters and will retrieve all opaqueRouteRange data from the server.

		Args:
			__id__ (str): NOT DEFINED
			Enabled (bool): Appends the local AsNumber.
			ImportedFile (str): Location of the route import file.
			NextHopAsIs (bool): If true, it takes the next Hop AsIs.
			NumberOfRoutes (number): Total number of opaque routes.
			SendMultiExitDiscovery (bool): If true, sends a Multi Exit Discriminator attribute with the indicated value.
			Status (str): Indicates the status of the imported file.

		Returns:
			self: This instance with matching opaqueRouteRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of opaqueRouteRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the opaqueRouteRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ApplyOpaqueRouteRange(self):
		"""Executes the applyOpaqueRouteRange operation on the server.

		This function allows to Apply the route range information on the opaque route block.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=opaqueRouteRange)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ApplyOpaqueRouteRange', payload=locals(), response_object=None)
