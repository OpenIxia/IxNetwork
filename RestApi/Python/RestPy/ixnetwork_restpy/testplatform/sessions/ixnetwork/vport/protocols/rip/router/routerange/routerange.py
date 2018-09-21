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
		"""The first network address to be used in creating this route range. Note: Multicast and loopback addresses are not supported in this IPv4 route range implementation.

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

	@property
	def MaskWidth(self):
		"""The network mask to be applied to the networkIpAddress to yield the non-host part of the address. A value of 0 means there is no subnet address.

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def Metric(self):
		"""The total metric cost for these routes. The valid range is from 1 to 16 (inclusive). A value of 16 means that the destination is not reachable, and that route will be removed from service.

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def NextHop(self):
		"""The immediate next hop IP address on the way to the destination address.

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NoOfRoutes(self):
		"""The number of networks to be generated for this route range, based on the network address plus the network mask.

		Returns:
			number
		"""
		return self._get_attribute('noOfRoutes')
	@NoOfRoutes.setter
	def NoOfRoutes(self, value):
		self._set_attribute('noOfRoutes', value)

	@property
	def RouteTag(self):
		"""An arbitrary value associated with the routes in this range. It is used to provide a means for distinguishing internal versus external RIP routes.

		Returns:
			number
		"""
		return self._get_attribute('routeTag')
	@RouteTag.setter
	def RouteTag(self, value):
		self._set_attribute('routeTag', value)

	def add(self, Enabled=None, FirstRoute=None, MaskWidth=None, Metric=None, NextHop=None, NoOfRoutes=None, RouteTag=None):
		"""Adds a new routeRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the use of this route range for the simulated router.
			FirstRoute (str): The first network address to be used in creating this route range. Note: Multicast and loopback addresses are not supported in this IPv4 route range implementation.
			MaskWidth (number): The network mask to be applied to the networkIpAddress to yield the non-host part of the address. A value of 0 means there is no subnet address.
			Metric (number): The total metric cost for these routes. The valid range is from 1 to 16 (inclusive). A value of 16 means that the destination is not reachable, and that route will be removed from service.
			NextHop (str): The immediate next hop IP address on the way to the destination address.
			NoOfRoutes (number): The number of networks to be generated for this route range, based on the network address plus the network mask.
			RouteTag (number): An arbitrary value associated with the routes in this range. It is used to provide a means for distinguishing internal versus external RIP routes.

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

	def find(self, Enabled=None, FirstRoute=None, MaskWidth=None, Metric=None, NextHop=None, NoOfRoutes=None, RouteTag=None):
		"""Finds and retrieves routeRange data from the server.

		All named parameters support regex and can be used to selectively retrieve routeRange data from the server.
		By default the find method takes no parameters and will retrieve all routeRange data from the server.

		Args:
			Enabled (bool): Enables the use of this route range for the simulated router.
			FirstRoute (str): The first network address to be used in creating this route range. Note: Multicast and loopback addresses are not supported in this IPv4 route range implementation.
			MaskWidth (number): The network mask to be applied to the networkIpAddress to yield the non-host part of the address. A value of 0 means there is no subnet address.
			Metric (number): The total metric cost for these routes. The valid range is from 1 to 16 (inclusive). A value of 16 means that the destination is not reachable, and that route will be removed from service.
			NextHop (str): The immediate next hop IP address on the way to the destination address.
			NoOfRoutes (number): The number of networks to be generated for this route range, based on the network address plus the network mask.
			RouteTag (number): An arbitrary value associated with the routes in this range. It is used to provide a means for distinguishing internal versus external RIP routes.

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
