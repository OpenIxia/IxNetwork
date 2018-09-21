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
		"""Enables the selected route range.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstRoute(self):
		"""The IPv6 address of the first route/network to be generated for this RIPng route range.

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

	@property
	def MaskWidth(self):
		"""The network mask to be used when generating routes This value indicates the number of bits, counting from the MSB (at the left end), that will comprise the network part of the IPv6 address. The remainder of the address will indicate the host part of the address. The default mask width is 64 bits.

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def Metric(self):
		"""The current metric cost to reach the destination. A value between 0 and 15. A value of 16 indicates that the destination is unreachable. (The RIPng Interface Metric is added to this value.)

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def NextHop(self):
		"""(For use in the Next Hop RTE.)The link-local IPv6 address of the next hop router. The value 0:0:0:0:0:0:0:0 indicates that the next hop router should be the originator of the RIPng route advertisement. (This router is the Next Hop.)

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NumberOfRoute(self):
		"""The total number of routes to be included in this route range.

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoute')
	@NumberOfRoute.setter
	def NumberOfRoute(self, value):
		self._set_attribute('numberOfRoute', value)

	@property
	def RouteTag(self):
		"""A route attribute advertised with a route: internal vs. external. For external routes, the route tag can be the AS from which the routes were learned or an arbitrary, assigned integer value.

		Returns:
			number
		"""
		return self._get_attribute('routeTag')
	@RouteTag.setter
	def RouteTag(self, value):
		self._set_attribute('routeTag', value)

	@property
	def Step(self):
		"""The increment step value to be used when creating additional routes/network addresses.

		Returns:
			number
		"""
		return self._get_attribute('step')
	@Step.setter
	def Step(self, value):
		self._set_attribute('step', value)

	def add(self, Enabled=None, FirstRoute=None, MaskWidth=None, Metric=None, NextHop=None, NumberOfRoute=None, RouteTag=None, Step=None):
		"""Adds a new routeRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables the selected route range.
			FirstRoute (str): The IPv6 address of the first route/network to be generated for this RIPng route range.
			MaskWidth (number): The network mask to be used when generating routes This value indicates the number of bits, counting from the MSB (at the left end), that will comprise the network part of the IPv6 address. The remainder of the address will indicate the host part of the address. The default mask width is 64 bits.
			Metric (number): The current metric cost to reach the destination. A value between 0 and 15. A value of 16 indicates that the destination is unreachable. (The RIPng Interface Metric is added to this value.)
			NextHop (str): (For use in the Next Hop RTE.)The link-local IPv6 address of the next hop router. The value 0:0:0:0:0:0:0:0 indicates that the next hop router should be the originator of the RIPng route advertisement. (This router is the Next Hop.)
			NumberOfRoute (number): The total number of routes to be included in this route range.
			RouteTag (number): A route attribute advertised with a route: internal vs. external. For external routes, the route tag can be the AS from which the routes were learned or an arbitrary, assigned integer value.
			Step (number): The increment step value to be used when creating additional routes/network addresses.

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

	def find(self, Enabled=None, FirstRoute=None, MaskWidth=None, Metric=None, NextHop=None, NumberOfRoute=None, RouteTag=None, Step=None):
		"""Finds and retrieves routeRange data from the server.

		All named parameters support regex and can be used to selectively retrieve routeRange data from the server.
		By default the find method takes no parameters and will retrieve all routeRange data from the server.

		Args:
			Enabled (bool): Enables the selected route range.
			FirstRoute (str): The IPv6 address of the first route/network to be generated for this RIPng route range.
			MaskWidth (number): The network mask to be used when generating routes This value indicates the number of bits, counting from the MSB (at the left end), that will comprise the network part of the IPv6 address. The remainder of the address will indicate the host part of the address. The default mask width is 64 bits.
			Metric (number): The current metric cost to reach the destination. A value between 0 and 15. A value of 16 indicates that the destination is unreachable. (The RIPng Interface Metric is added to this value.)
			NextHop (str): (For use in the Next Hop RTE.)The link-local IPv6 address of the next hop router. The value 0:0:0:0:0:0:0:0 indicates that the next hop router should be the originator of the RIPng route advertisement. (This router is the Next Hop.)
			NumberOfRoute (number): The total number of routes to be included in this route range.
			RouteTag (number): A route attribute advertised with a route: internal vs. external. For external routes, the route tag can be the AS from which the routes were learned or an arbitrary, assigned integer value.
			Step (number): The increment step value to be used when creating additional routes/network addresses.

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
