from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Router(Base):
	"""The Router class encapsulates a user managed router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'router'

	def __init__(self, parent):
		super(Router, self).__init__(parent)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.eigrp.router.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.eigrp.router.interface.interface import Interface
		return Interface(self)

	@property
	def LearnedRoute(self):
		"""An instance of the LearnedRoute class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.eigrp.router.learnedroute.learnedroute.LearnedRoute)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.eigrp.router.learnedroute.learnedroute import LearnedRoute
		return LearnedRoute(self)

	@property
	def RouteRange(self):
		"""An instance of the RouteRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.eigrp.router.routerange.routerange.RouteRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.eigrp.router.routerange.routerange import RouteRange
		return RouteRange(self)

	@property
	def ActiveTime(self):
		"""It determines the maximum time (in minutes) for which a route learned from a neighbor will be active in the topology table, if the neighbor stops sending Hellos. The valid range is 1 to 4294967295. (default = 3 minutes)

		Returns:
			number
		"""
		return self._get_attribute('activeTime')
	@ActiveTime.setter
	def ActiveTime(self, value):
		self._set_attribute('activeTime', value)

	@property
	def AsNumber(self):
		"""The identifier of the Autonomous System (AS) where this emulated EIGRP router is located. The valid range is 1 to 4294967295. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('asNumber')
	@AsNumber.setter
	def AsNumber(self, value):
		self._set_attribute('asNumber', value)

	@property
	def DiscardLearnedRoutes(self):
		"""If enabled, routes learned by emulated EIGRP Routers on this port will be discarded (not stored).

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedRoutes')
	@DiscardLearnedRoutes.setter
	def DiscardLearnedRoutes(self, value):
		self._set_attribute('discardLearnedRoutes', value)

	@property
	def EigrpAddressFamily(self):
		"""It denotes IP address type, one of IPv4 or IPv6 (Default is IPv4)

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('eigrpAddressFamily')
	@EigrpAddressFamily.setter
	def EigrpAddressFamily(self, value):
		self._set_attribute('eigrpAddressFamily', value)

	@property
	def EigrpMajorVersion(self):
		"""The major version level of the EIGRP software. The valid range is 0 to 255. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('eigrpMajorVersion')
	@EigrpMajorVersion.setter
	def EigrpMajorVersion(self, value):
		self._set_attribute('eigrpMajorVersion', value)

	@property
	def EigrpMinorVersion(self):
		"""The minor version level of the EIGRP software. The valid range is 0 to 255. (default = 2).

		Returns:
			number
		"""
		return self._get_attribute('eigrpMinorVersion')
	@EigrpMinorVersion.setter
	def EigrpMinorVersion(self, value):
		self._set_attribute('eigrpMinorVersion', value)

	@property
	def EnablePiggyBack(self):
		"""If enabled, then EIGRP will piggyback an acknowledgement for the initial update with any unicast packet sent to the neighbor, instead of directly sending a separate acknowledgement packet to the neighbor.

		Returns:
			bool
		"""
		return self._get_attribute('enablePiggyBack')
	@EnablePiggyBack.setter
	def EnablePiggyBack(self, value):
		self._set_attribute('enablePiggyBack', value)

	@property
	def Enabled(self):
		"""Enables the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IosMajorVersion(self):
		"""The major version level of the referenced software. The valid range is 0 to 255. (default = 12)

		Returns:
			number
		"""
		return self._get_attribute('iosMajorVersion')
	@IosMajorVersion.setter
	def IosMajorVersion(self, value):
		self._set_attribute('iosMajorVersion', value)

	@property
	def IosMinorVersion(self):
		"""The major version level of the referenced software. The valid range is 0 to 255. (default = 3)

		Returns:
			number
		"""
		return self._get_attribute('iosMinorVersion')
	@IosMinorVersion.setter
	def IosMinorVersion(self, value):
		self._set_attribute('iosMinorVersion', value)

	@property
	def IsRefreshComplete(self):
		"""If true, the routes have been refreshed.

		Returns:
			number
		"""
		return self._get_attribute('isRefreshComplete')

	@property
	def K1(self):
		"""Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('k1')
	@K1.setter
	def K1(self, value):
		self._set_attribute('k1', value)

	@property
	def K2(self):
		"""Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('k2')
	@K2.setter
	def K2(self, value):
		self._set_attribute('k2', value)

	@property
	def K3(self):
		"""Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 1)

		Returns:
			number
		"""
		return self._get_attribute('k3')
	@K3.setter
	def K3(self, value):
		self._set_attribute('k3', value)

	@property
	def K4(self):
		"""Advanced parameter, only used in condition checking for establishing neighbor relationship.The valid range is 0 to 255. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('k4')
	@K4.setter
	def K4(self, value):
		self._set_attribute('k4', value)

	@property
	def K5(self):
		"""Advanced parameter, only used in condition checking for establishing neighbor relationship.The valid range is 0 to 255. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('k5')
	@K5.setter
	def K5(self, value):
		self._set_attribute('k5', value)

	@property
	def RouterId(self):
		"""This is an IP-formatted string. Its default value is dependent on card/port type.

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, ActiveTime=None, AsNumber=None, DiscardLearnedRoutes=None, EigrpAddressFamily=None, EigrpMajorVersion=None, EigrpMinorVersion=None, EnablePiggyBack=None, Enabled=None, IosMajorVersion=None, IosMinorVersion=None, K1=None, K2=None, K3=None, K4=None, K5=None, RouterId=None, TrafficGroupId=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			ActiveTime (number): It determines the maximum time (in minutes) for which a route learned from a neighbor will be active in the topology table, if the neighbor stops sending Hellos. The valid range is 1 to 4294967295. (default = 3 minutes)
			AsNumber (number): The identifier of the Autonomous System (AS) where this emulated EIGRP router is located. The valid range is 1 to 4294967295. (default = 1)
			DiscardLearnedRoutes (bool): If enabled, routes learned by emulated EIGRP Routers on this port will be discarded (not stored).
			EigrpAddressFamily (str(ipv4|ipv6)): It denotes IP address type, one of IPv4 or IPv6 (Default is IPv4)
			EigrpMajorVersion (number): The major version level of the EIGRP software. The valid range is 0 to 255. (default = 1)
			EigrpMinorVersion (number): The minor version level of the EIGRP software. The valid range is 0 to 255. (default = 2).
			EnablePiggyBack (bool): If enabled, then EIGRP will piggyback an acknowledgement for the initial update with any unicast packet sent to the neighbor, instead of directly sending a separate acknowledgement packet to the neighbor.
			Enabled (bool): Enables the simulated router.
			IosMajorVersion (number): The major version level of the referenced software. The valid range is 0 to 255. (default = 12)
			IosMinorVersion (number): The major version level of the referenced software. The valid range is 0 to 255. (default = 3)
			K1 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 1)
			K2 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 0)
			K3 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 1)
			K4 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship.The valid range is 0 to 255. (default = 0)
			K5 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship.The valid range is 0 to 255. (default = 0)
			RouterId (str): This is an IP-formatted string. Its default value is dependent on card/port type.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the router data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActiveTime=None, AsNumber=None, DiscardLearnedRoutes=None, EigrpAddressFamily=None, EigrpMajorVersion=None, EigrpMinorVersion=None, EnablePiggyBack=None, Enabled=None, IosMajorVersion=None, IosMinorVersion=None, IsRefreshComplete=None, K1=None, K2=None, K3=None, K4=None, K5=None, RouterId=None, TrafficGroupId=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			ActiveTime (number): It determines the maximum time (in minutes) for which a route learned from a neighbor will be active in the topology table, if the neighbor stops sending Hellos. The valid range is 1 to 4294967295. (default = 3 minutes)
			AsNumber (number): The identifier of the Autonomous System (AS) where this emulated EIGRP router is located. The valid range is 1 to 4294967295. (default = 1)
			DiscardLearnedRoutes (bool): If enabled, routes learned by emulated EIGRP Routers on this port will be discarded (not stored).
			EigrpAddressFamily (str(ipv4|ipv6)): It denotes IP address type, one of IPv4 or IPv6 (Default is IPv4)
			EigrpMajorVersion (number): The major version level of the EIGRP software. The valid range is 0 to 255. (default = 1)
			EigrpMinorVersion (number): The minor version level of the EIGRP software. The valid range is 0 to 255. (default = 2).
			EnablePiggyBack (bool): If enabled, then EIGRP will piggyback an acknowledgement for the initial update with any unicast packet sent to the neighbor, instead of directly sending a separate acknowledgement packet to the neighbor.
			Enabled (bool): Enables the simulated router.
			IosMajorVersion (number): The major version level of the referenced software. The valid range is 0 to 255. (default = 12)
			IosMinorVersion (number): The major version level of the referenced software. The valid range is 0 to 255. (default = 3)
			IsRefreshComplete (number): If true, the routes have been refreshed.
			K1 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 1)
			K2 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 0)
			K3 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship. The valid range is 0 to 255. (default = 1)
			K4 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship.The valid range is 0 to 255. (default = 0)
			K5 (number): Advanced parameter, only used in condition checking for establishing neighbor relationship.The valid range is 0 to 255. (default = 0)
			RouterId (str): This is an IP-formatted string. Its default value is dependent on card/port type.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with matching router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		This exec refreshes the EIGRP learned information from the DUT.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
