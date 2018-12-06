
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
		"""

		Returns:
			number
		"""
		return self._get_attribute('activeTime')
	@ActiveTime.setter
	def ActiveTime(self, value):
		self._set_attribute('activeTime', value)

	@property
	def AsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('asNumber')
	@AsNumber.setter
	def AsNumber(self, value):
		self._set_attribute('asNumber', value)

	@property
	def DiscardLearnedRoutes(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedRoutes')
	@DiscardLearnedRoutes.setter
	def DiscardLearnedRoutes(self, value):
		self._set_attribute('discardLearnedRoutes', value)

	@property
	def EigrpAddressFamily(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('eigrpAddressFamily')
	@EigrpAddressFamily.setter
	def EigrpAddressFamily(self, value):
		self._set_attribute('eigrpAddressFamily', value)

	@property
	def EigrpMajorVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eigrpMajorVersion')
	@EigrpMajorVersion.setter
	def EigrpMajorVersion(self, value):
		self._set_attribute('eigrpMajorVersion', value)

	@property
	def EigrpMinorVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eigrpMinorVersion')
	@EigrpMinorVersion.setter
	def EigrpMinorVersion(self, value):
		self._set_attribute('eigrpMinorVersion', value)

	@property
	def EnablePiggyBack(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePiggyBack')
	@EnablePiggyBack.setter
	def EnablePiggyBack(self, value):
		self._set_attribute('enablePiggyBack', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IosMajorVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iosMajorVersion')
	@IosMajorVersion.setter
	def IosMajorVersion(self, value):
		self._set_attribute('iosMajorVersion', value)

	@property
	def IosMinorVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iosMinorVersion')
	@IosMinorVersion.setter
	def IosMinorVersion(self, value):
		self._set_attribute('iosMinorVersion', value)

	@property
	def IsRefreshComplete(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('isRefreshComplete')

	@property
	def K1(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('k1')
	@K1.setter
	def K1(self, value):
		self._set_attribute('k1', value)

	@property
	def K2(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('k2')
	@K2.setter
	def K2(self, value):
		self._set_attribute('k2', value)

	@property
	def K3(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('k3')
	@K3.setter
	def K3(self, value):
		self._set_attribute('k3', value)

	@property
	def K4(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('k4')
	@K4.setter
	def K4(self, value):
		self._set_attribute('k4', value)

	@property
	def K5(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('k5')
	@K5.setter
	def K5(self, value):
		self._set_attribute('k5', value)

	@property
	def RouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def TrafficGroupId(self):
		"""

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
			ActiveTime (number): 
			AsNumber (number): 
			DiscardLearnedRoutes (bool): 
			EigrpAddressFamily (str(ipv4|ipv6)): 
			EigrpMajorVersion (number): 
			EigrpMinorVersion (number): 
			EnablePiggyBack (bool): 
			Enabled (bool): 
			IosMajorVersion (number): 
			IosMinorVersion (number): 
			K1 (number): 
			K2 (number): 
			K3 (number): 
			K4 (number): 
			K5 (number): 
			RouterId (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

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
			ActiveTime (number): 
			AsNumber (number): 
			DiscardLearnedRoutes (bool): 
			EigrpAddressFamily (str(ipv4|ipv6)): 
			EigrpMajorVersion (number): 
			EigrpMinorVersion (number): 
			EnablePiggyBack (bool): 
			Enabled (bool): 
			IosMajorVersion (number): 
			IosMinorVersion (number): 
			IsRefreshComplete (number): 
			K1 (number): 
			K2 (number): 
			K3 (number): 
			K4 (number): 
			K5 (number): 
			RouterId (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

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

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
