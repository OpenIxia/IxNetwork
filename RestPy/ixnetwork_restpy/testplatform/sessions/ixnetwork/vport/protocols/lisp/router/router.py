
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
	def EidToRlocMapCacheInfo(self):
		"""An instance of the EidToRlocMapCacheInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.eidtorlocmapcacheinfo.eidtorlocmapcacheinfo.EidToRlocMapCacheInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.eidtorlocmapcacheinfo.eidtorlocmapcacheinfo import EidToRlocMapCacheInfo
		return EidToRlocMapCacheInfo(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.interface.interface import Interface
		return Interface(self)

	@property
	def LispInstance(self):
		"""An instance of the LispInstance class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.lispinstance.LispInstance)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.lispinstance import LispInstance
		return LispInstance(self)

	@property
	def MapServerCacheInfo(self):
		"""An instance of the MapServerCacheInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.mapservercacheinfo.mapservercacheinfo.MapServerCacheInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.mapservercacheinfo.mapservercacheinfo import MapServerCacheInfo
		return MapServerCacheInfo(self)

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
	def InstanceIdForEidToRlocMapCacheRefresh(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instanceIdForEidToRlocMapCacheRefresh')
	@InstanceIdForEidToRlocMapCacheRefresh.setter
	def InstanceIdForEidToRlocMapCacheRefresh(self, value):
		self._set_attribute('instanceIdForEidToRlocMapCacheRefresh', value)

	@property
	def InstanceIdForMapServerCacheRefresh(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instanceIdForMapServerCacheRefresh')
	@InstanceIdForMapServerCacheRefresh.setter
	def InstanceIdForMapServerCacheRefresh(self, value):
		self._set_attribute('instanceIdForMapServerCacheRefresh', value)

	@property
	def IsEidToRlocMapCacheInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isEidToRlocMapCacheInfoRefreshed')

	@property
	def IsEidToRlocMapCacheRefreshAllInstances(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isEidToRlocMapCacheRefreshAllInstances')
	@IsEidToRlocMapCacheRefreshAllInstances.setter
	def IsEidToRlocMapCacheRefreshAllInstances(self, value):
		self._set_attribute('isEidToRlocMapCacheRefreshAllInstances', value)

	@property
	def IsMapServerCacheInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isMapServerCacheInfoRefreshed')

	@property
	def IsMapServerCacheRefreshAllInstances(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isMapServerCacheRefreshAllInstances')
	@IsMapServerCacheRefreshAllInstances.setter
	def IsMapServerCacheRefreshAllInstances(self, value):
		self._set_attribute('isMapServerCacheRefreshAllInstances', value)

	@property
	def MappingServiceMode(self):
		"""

		Returns:
			str(standAlone|alt|na)
		"""
		return self._get_attribute('mappingServiceMode')
	@MappingServiceMode.setter
	def MappingServiceMode(self, value):
		self._set_attribute('mappingServiceMode', value)

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
	def TunnelRouterMode(self):
		"""

		Returns:
			str(itr|etr|xtr|msmr)
		"""
		return self._get_attribute('tunnelRouterMode')
	@TunnelRouterMode.setter
	def TunnelRouterMode(self, value):
		self._set_attribute('tunnelRouterMode', value)

	def add(self, Enabled=None, InstanceIdForEidToRlocMapCacheRefresh=None, InstanceIdForMapServerCacheRefresh=None, IsEidToRlocMapCacheRefreshAllInstances=None, IsMapServerCacheRefreshAllInstances=None, MappingServiceMode=None, RouterId=None, TunnelRouterMode=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			InstanceIdForEidToRlocMapCacheRefresh (number): 
			InstanceIdForMapServerCacheRefresh (number): 
			IsEidToRlocMapCacheRefreshAllInstances (bool): 
			IsMapServerCacheRefreshAllInstances (bool): 
			MappingServiceMode (str(standAlone|alt|na)): 
			RouterId (str): 
			TunnelRouterMode (str(itr|etr|xtr|msmr)): 

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

	def find(self, Enabled=None, InstanceIdForEidToRlocMapCacheRefresh=None, InstanceIdForMapServerCacheRefresh=None, IsEidToRlocMapCacheInfoRefreshed=None, IsEidToRlocMapCacheRefreshAllInstances=None, IsMapServerCacheInfoRefreshed=None, IsMapServerCacheRefreshAllInstances=None, MappingServiceMode=None, RouterId=None, TunnelRouterMode=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			Enabled (bool): 
			InstanceIdForEidToRlocMapCacheRefresh (number): 
			InstanceIdForMapServerCacheRefresh (number): 
			IsEidToRlocMapCacheInfoRefreshed (bool): 
			IsEidToRlocMapCacheRefreshAllInstances (bool): 
			IsMapServerCacheInfoRefreshed (bool): 
			IsMapServerCacheRefreshAllInstances (bool): 
			MappingServiceMode (str(standAlone|alt|na)): 
			RouterId (str): 
			TunnelRouterMode (str(itr|etr|xtr|msmr)): 

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
