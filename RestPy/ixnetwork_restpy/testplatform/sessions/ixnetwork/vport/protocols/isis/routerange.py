from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RouteRange(Base):
	"""The RouteRange class encapsulates a user managed routeRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RouteRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'routeRange'

	def __init__(self, parent):
		super(RouteRange, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables the use of this route range for the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstRoute(self):
		"""The first route of the route range, in IPv4 dotted decimal format. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

	@property
	def IsRedistributed(self):
		"""Sets the Up/Down (Redistribution) bit defined for TLVs 128 and 130 by RFC 2966. It is used for domain-wide advertisement of prefix information.

		Returns:
			bool
		"""
		return self._get_attribute('isRedistributed')
	@IsRedistributed.setter
	def IsRedistributed(self, value):
		self._set_attribute('isRedistributed', value)

	@property
	def MaskWidth(self):
		"""The network mask width for the route range (in bits). The valid range is from 0 to 32 bits. (default = 24)

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def Metric(self):
		"""The user-defined metric associated with this route range.

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def NumberOfRoutes(self):
		"""The number of routes to be generated for this route range.

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoutes')
	@NumberOfRoutes.setter
	def NumberOfRoutes(self, value):
		self._set_attribute('numberOfRoutes', value)

	@property
	def RouteOrigin(self):
		"""The origin of the advertised route - internal or external to the ISIS area.

		Returns:
			bool
		"""
		return self._get_attribute('routeOrigin')
	@RouteOrigin.setter
	def RouteOrigin(self, value):
		self._set_attribute('routeOrigin', value)

	@property
	def Type(self):
		"""The IP type of the route range for the ISIS router.

		Returns:
			str(ipAny|ipv4|ipv6)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, Enabled=None, FirstRoute=None, IsRedistributed=None, MaskWidth=None, Metric=None, NumberOfRoutes=None, RouteOrigin=None, Type=None):
		"""Adds a new routeRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the use of this route range for the simulated router.
			FirstRoute (str): The first route of the route range, in IPv4 dotted decimal format. (default = 0.0.0.0)
			IsRedistributed (bool): Sets the Up/Down (Redistribution) bit defined for TLVs 128 and 130 by RFC 2966. It is used for domain-wide advertisement of prefix information.
			MaskWidth (number): The network mask width for the route range (in bits). The valid range is from 0 to 32 bits. (default = 24)
			Metric (number): The user-defined metric associated with this route range.
			NumberOfRoutes (number): The number of routes to be generated for this route range.
			RouteOrigin (bool): The origin of the advertised route - internal or external to the ISIS area.
			Type (str(ipAny|ipv4|ipv6)): The IP type of the route range for the ISIS router.

		Returns:
			self: This instance with all currently retrieved routeRange data using find and the newly added routeRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the routeRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, FirstRoute=None, IsRedistributed=None, MaskWidth=None, Metric=None, NumberOfRoutes=None, RouteOrigin=None, Type=None):
		"""Finds and retrieves routeRange data from the server.

		All named parameters support regex and can be used to selectively retrieve routeRange data from the server.
		By default the find method takes no parameters and will retrieve all routeRange data from the server.

		Args:
			Enabled (bool): Enables the use of this route range for the simulated router.
			FirstRoute (str): The first route of the route range, in IPv4 dotted decimal format. (default = 0.0.0.0)
			IsRedistributed (bool): Sets the Up/Down (Redistribution) bit defined for TLVs 128 and 130 by RFC 2966. It is used for domain-wide advertisement of prefix information.
			MaskWidth (number): The network mask width for the route range (in bits). The valid range is from 0 to 32 bits. (default = 24)
			Metric (number): The user-defined metric associated with this route range.
			NumberOfRoutes (number): The number of routes to be generated for this route range.
			RouteOrigin (bool): The origin of the advertised route - internal or external to the ISIS area.
			Type (str(ipAny|ipv4|ipv6)): The IP type of the route range for the ISIS router.

		Returns:
			self: This instance with matching routeRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of routeRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the routeRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
