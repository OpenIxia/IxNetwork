
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


class MapServerCacheInfo(Base):
	"""The MapServerCacheInfo class encapsulates a system managed mapServerCacheInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MapServerCacheInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'mapServerCacheInfo'

	def __init__(self, parent):
		super(MapServerCacheInfo, self).__init__(parent)

	@property
	def RemoteLocators(self):
		"""An instance of the RemoteLocators class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.mapservercacheinfo.remotelocators.remotelocators.RemoteLocators)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.mapservercacheinfo.remotelocators.remotelocators import RemoteLocators
		return RemoteLocators(self)

	@property
	def Action(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('action')

	@property
	def EidPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eidPrefix')

	@property
	def EidPrefixAfi(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('eidPrefixAfi')

	@property
	def EidPrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eidPrefixLength')

	@property
	def EtrIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('etrIp')

	@property
	def ExpiresAfter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('expiresAfter')

	@property
	def InstanceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('instanceId')

	@property
	def Ipv4ErrorMapRegisterRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4ErrorMapRegisterRx')

	@property
	def Ipv4MapNotifyTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapNotifyTx')

	@property
	def Ipv4MapRegisterRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRegisterRx')

	@property
	def Ipv4MapRequestDropped(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRequestDropped')

	@property
	def Ipv6ErrorMapRegisterRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6ErrorMapRegisterRx')

	@property
	def Ipv6MapNotifyTx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapNotifyTx')

	@property
	def Ipv6MapRegisterRx(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRegisterRx')

	@property
	def Ipv6MapRequestDropped(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRequestDropped')

	@property
	def Key(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('key')

	@property
	def MapVersionNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mapVersionNumber')

	@property
	def ProxyMapReply(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('proxyMapReply')

	@property
	def WantMapNotify(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('wantMapNotify')

	def find(self, Action=None, EidPrefix=None, EidPrefixAfi=None, EidPrefixLength=None, EtrIp=None, ExpiresAfter=None, InstanceId=None, Ipv4ErrorMapRegisterRx=None, Ipv4MapNotifyTx=None, Ipv4MapRegisterRx=None, Ipv4MapRequestDropped=None, Ipv6ErrorMapRegisterRx=None, Ipv6MapNotifyTx=None, Ipv6MapRegisterRx=None, Ipv6MapRequestDropped=None, Key=None, MapVersionNumber=None, ProxyMapReply=None, WantMapNotify=None):
		"""Finds and retrieves mapServerCacheInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve mapServerCacheInfo data from the server.
		By default the find method takes no parameters and will retrieve all mapServerCacheInfo data from the server.

		Args:
			Action (str): 
			EidPrefix (str): 
			EidPrefixAfi (str): 
			EidPrefixLength (number): 
			EtrIp (str): 
			ExpiresAfter (str): 
			InstanceId (number): 
			Ipv4ErrorMapRegisterRx (number): 
			Ipv4MapNotifyTx (number): 
			Ipv4MapRegisterRx (number): 
			Ipv4MapRequestDropped (number): 
			Ipv6ErrorMapRegisterRx (number): 
			Ipv6MapNotifyTx (number): 
			Ipv6MapRegisterRx (number): 
			Ipv6MapRequestDropped (number): 
			Key (str): 
			MapVersionNumber (number): 
			ProxyMapReply (bool): 
			WantMapNotify (bool): 

		Returns:
			self: This instance with matching mapServerCacheInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of mapServerCacheInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the mapServerCacheInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
