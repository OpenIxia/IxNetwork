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
	def Bandwidth(self):
		"""The minimum amount of bandwidth available on this link, in Kbps. The valid range is 1 to 4294967295. (default = 10,000 Kbps)

		Returns:
			number
		"""
		return self._get_attribute('bandwidth')
	@Bandwidth.setter
	def Bandwidth(self, value):
		self._set_attribute('bandwidth', value)

	@property
	def Delay(self):
		"""The total of delays on the path to the route/network, in microseconds. The valid range is 0 to 4294967295. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('delay')
	@Delay.setter
	def Delay(self, value):
		self._set_attribute('delay', value)

	@property
	def DestCount(self):
		"""(Available only if Packing is enabled.) If packing is enabled, it indicates the maximum number of destinations that can be packed into a single Internal/External TLV. A value of 0 means that maximum possible packing will be used, which depends on the MTU of the link. The valid range is 0 to 255. (default = 90)

		Returns:
			number
		"""
		return self._get_attribute('destCount')
	@DestCount.setter
	def DestCount(self, value):
		self._set_attribute('destCount', value)

	@property
	def EnablePacking(self):
		"""Enables packing of multiple destinations into a single Internal/External TLV. If disabled, only one destination will be packed into a single Internal/External TLV. (default = enabled)

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def Enabled(self):
		"""Enables the route range. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstRoute(self):
		"""The first route of the route range, in IPv4/IPv6 dotted decimal format. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('firstRoute')
	@FirstRoute.setter
	def FirstRoute(self, value):
		self._set_attribute('firstRoute', value)

	@property
	def Flag(self):
		"""(Available only for External route ranges.) The origin of the advertised route.

		Returns:
			str(externalRoute|candidateDefault)
		"""
		return self._get_attribute('flag')
	@Flag.setter
	def Flag(self, value):
		self._set_attribute('flag', value)

	@property
	def HopCount(self):
		"""The number of hops on the way to the destination address. The valid range is 0 to 255. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('hopCount')
	@HopCount.setter
	def HopCount(self, value):
		self._set_attribute('hopCount', value)

	@property
	def Load(self):
		"""The amount of load on the link. The valid range is 0 to 255. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('load')
	@Load.setter
	def Load(self, value):
		self._set_attribute('load', value)

	@property
	def Mask(self):
		"""The network mask width for the route range (in bits). The valid range is from 0 to 32 bits. (default = 24)

		Returns:
			number
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def Metric(self):
		"""(Available only for External route ranges.) The EIGRP vector metric for the cost of the path to this route/network. The valid range is 1 to 4294967295. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('metric')
	@Metric.setter
	def Metric(self, value):
		self._set_attribute('metric', value)

	@property
	def Mtu(self):
		"""The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def NextHop(self):
		"""The immediate next hop IP address on the way to the destination address, in IPv4/IPv6 dotted decimal format. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('nextHop')
	@NextHop.setter
	def NextHop(self, value):
		self._set_attribute('nextHop', value)

	@property
	def NomberOfRoutes(self):
		"""The number of routes to be generated for this route range, based on the network address plus the network mask. The valid range is 1 to 16777215. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('nomberOfRoutes')
	@NomberOfRoutes.setter
	def NomberOfRoutes(self, value):
		self._set_attribute('nomberOfRoutes', value)

	@property
	def NumberOfRoutes(self):
		"""The number of routes to be generated for this route range, based on the network address plus the network mask. The valid range is 1 to 16777215. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('numberOfRoutes')
	@NumberOfRoutes.setter
	def NumberOfRoutes(self, value):
		self._set_attribute('numberOfRoutes', value)

	@property
	def OriginatingAs(self):
		"""(Available only for External route ranges.) The external AS where this route was originated. The valid range is 1 to 4294967295. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('originatingAs')
	@OriginatingAs.setter
	def OriginatingAs(self, value):
		self._set_attribute('originatingAs', value)

	@property
	def ProtocolId(self):
		"""(Available only for External route ranges.) The external protocol where the route was originated, if applicable.

		Returns:
			str(igrp|enhancedIgrp|static|rip|hello|ospf|isis|egp|bgp|idrp|connected)
		"""
		return self._get_attribute('protocolId')
	@ProtocolId.setter
	def ProtocolId(self, value):
		self._set_attribute('protocolId', value)

	@property
	def Reliability(self):
		"""The reliability factor. The valid range is 0 to 255 (100% reliable). (default = 255)

		Returns:
			number
		"""
		return self._get_attribute('reliability')
	@Reliability.setter
	def Reliability(self, value):
		self._set_attribute('reliability', value)

	@property
	def RouteTag(self):
		"""(Available only for External route ranges.) An administrative tag applied to the route when it is redistributed between EIGRP and an external protocol, to prevent routing loops. Used as a route mapping filter. The valid range is 0 to 4294967295. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('routeTag')
	@RouteTag.setter
	def RouteTag(self, value):
		self._set_attribute('routeTag', value)

	@property
	def Source(self):
		"""(Available only for External route ranges.) The IPv4 address for the external source of the route information, in dotted decimal format. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('source')
	@Source.setter
	def Source(self, value):
		self._set_attribute('source', value)

	@property
	def Type(self):
		"""The type of route range: internal or external to the AS.

		Returns:
			str(external|internal)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, Bandwidth=None, Delay=None, DestCount=None, EnablePacking=None, Enabled=None, FirstRoute=None, Flag=None, HopCount=None, Load=None, Mask=None, Metric=None, Mtu=None, NextHop=None, NomberOfRoutes=None, NumberOfRoutes=None, OriginatingAs=None, ProtocolId=None, Reliability=None, RouteTag=None, Source=None, Type=None):
		"""Adds a new routeRange node on the server and retrieves it in this instance.

		Args:
			Bandwidth (number): The minimum amount of bandwidth available on this link, in Kbps. The valid range is 1 to 4294967295. (default = 10,000 Kbps)
			Delay (number): The total of delays on the path to the route/network, in microseconds. The valid range is 0 to 4294967295. (default = 0)
			DestCount (number): (Available only if Packing is enabled.) If packing is enabled, it indicates the maximum number of destinations that can be packed into a single Internal/External TLV. A value of 0 means that maximum possible packing will be used, which depends on the MTU of the link. The valid range is 0 to 255. (default = 90)
			EnablePacking (bool): Enables packing of multiple destinations into a single Internal/External TLV. If disabled, only one destination will be packed into a single Internal/External TLV. (default = enabled)
			Enabled (bool): Enables the route range. (default = disabled)
			FirstRoute (str): The first route of the route range, in IPv4/IPv6 dotted decimal format. (default = 0.0.0.0)
			Flag (str(externalRoute|candidateDefault)): (Available only for External route ranges.) The origin of the advertised route.
			HopCount (number): The number of hops on the way to the destination address. The valid range is 0 to 255. (default = 0)
			Load (number): The amount of load on the link. The valid range is 0 to 255. (default = 0)
			Mask (number): The network mask width for the route range (in bits). The valid range is from 0 to 32 bits. (default = 24)
			Metric (number): (Available only for External route ranges.) The EIGRP vector metric for the cost of the path to this route/network. The valid range is 1 to 4294967295. (default = 1)
			Mtu (number): The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)
			NextHop (str): The immediate next hop IP address on the way to the destination address, in IPv4/IPv6 dotted decimal format. (default = 0.0.0.0)
			NomberOfRoutes (number): The number of routes to be generated for this route range, based on the network address plus the network mask. The valid range is 1 to 16777215. (default = 1)
			NumberOfRoutes (number): The number of routes to be generated for this route range, based on the network address plus the network mask. The valid range is 1 to 16777215. (default = 1)
			OriginatingAs (number): (Available only for External route ranges.) The external AS where this route was originated. The valid range is 1 to 4294967295. (default = 1)
			ProtocolId (str(igrp|enhancedIgrp|static|rip|hello|ospf|isis|egp|bgp|idrp|connected)): (Available only for External route ranges.) The external protocol where the route was originated, if applicable.
			Reliability (number): The reliability factor. The valid range is 0 to 255 (100% reliable). (default = 255)
			RouteTag (number): (Available only for External route ranges.) An administrative tag applied to the route when it is redistributed between EIGRP and an external protocol, to prevent routing loops. Used as a route mapping filter. The valid range is 0 to 4294967295. (default = 0)
			Source (str): (Available only for External route ranges.) The IPv4 address for the external source of the route information, in dotted decimal format. (default = 0.0.0.0)
			Type (str(external|internal)): The type of route range: internal or external to the AS.

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

	def find(self, Bandwidth=None, Delay=None, DestCount=None, EnablePacking=None, Enabled=None, FirstRoute=None, Flag=None, HopCount=None, Load=None, Mask=None, Metric=None, Mtu=None, NextHop=None, NomberOfRoutes=None, NumberOfRoutes=None, OriginatingAs=None, ProtocolId=None, Reliability=None, RouteTag=None, Source=None, Type=None):
		"""Finds and retrieves routeRange data from the server.

		All named parameters support regex and can be used to selectively retrieve routeRange data from the server.
		By default the find method takes no parameters and will retrieve all routeRange data from the server.

		Args:
			Bandwidth (number): The minimum amount of bandwidth available on this link, in Kbps. The valid range is 1 to 4294967295. (default = 10,000 Kbps)
			Delay (number): The total of delays on the path to the route/network, in microseconds. The valid range is 0 to 4294967295. (default = 0)
			DestCount (number): (Available only if Packing is enabled.) If packing is enabled, it indicates the maximum number of destinations that can be packed into a single Internal/External TLV. A value of 0 means that maximum possible packing will be used, which depends on the MTU of the link. The valid range is 0 to 255. (default = 90)
			EnablePacking (bool): Enables packing of multiple destinations into a single Internal/External TLV. If disabled, only one destination will be packed into a single Internal/External TLV. (default = enabled)
			Enabled (bool): Enables the route range. (default = disabled)
			FirstRoute (str): The first route of the route range, in IPv4/IPv6 dotted decimal format. (default = 0.0.0.0)
			Flag (str(externalRoute|candidateDefault)): (Available only for External route ranges.) The origin of the advertised route.
			HopCount (number): The number of hops on the way to the destination address. The valid range is 0 to 255. (default = 0)
			Load (number): The amount of load on the link. The valid range is 0 to 255. (default = 0)
			Mask (number): The network mask width for the route range (in bits). The valid range is from 0 to 32 bits. (default = 24)
			Metric (number): (Available only for External route ranges.) The EIGRP vector metric for the cost of the path to this route/network. The valid range is 1 to 4294967295. (default = 1)
			Mtu (number): The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)
			NextHop (str): The immediate next hop IP address on the way to the destination address, in IPv4/IPv6 dotted decimal format. (default = 0.0.0.0)
			NomberOfRoutes (number): The number of routes to be generated for this route range, based on the network address plus the network mask. The valid range is 1 to 16777215. (default = 1)
			NumberOfRoutes (number): The number of routes to be generated for this route range, based on the network address plus the network mask. The valid range is 1 to 16777215. (default = 1)
			OriginatingAs (number): (Available only for External route ranges.) The external AS where this route was originated. The valid range is 1 to 4294967295. (default = 1)
			ProtocolId (str(igrp|enhancedIgrp|static|rip|hello|ospf|isis|egp|bgp|idrp|connected)): (Available only for External route ranges.) The external protocol where the route was originated, if applicable.
			Reliability (number): The reliability factor. The valid range is 0 to 255 (100% reliable). (default = 255)
			RouteTag (number): (Available only for External route ranges.) An administrative tag applied to the route when it is redistributed between EIGRP and an external protocol, to prevent routing loops. Used as a route mapping filter. The valid range is 0 to 4294967295. (default = 0)
			Source (str): (Available only for External route ranges.) The IPv4 address for the external source of the route information, in dotted decimal format. (default = 0.0.0.0)
			Type (str(external|internal)): The type of route range: internal or external to the AS.

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
