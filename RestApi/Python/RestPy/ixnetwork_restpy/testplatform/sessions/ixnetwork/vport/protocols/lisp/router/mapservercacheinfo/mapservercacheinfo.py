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
		"""It gives details about the action (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('action')

	@property
	def EidPrefix(self):
		"""It gives details about the eid prefix (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('eidPrefix')

	@property
	def EidPrefixAfi(self):
		"""It gives details about the eid prefix Afi (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('eidPrefixAfi')

	@property
	def EidPrefixLength(self):
		"""It gives details about the eid prefix Length (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('eidPrefixLength')

	@property
	def EtrIp(self):
		"""It gives details about the etrlp (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('etrIp')

	@property
	def ExpiresAfter(self):
		"""It gives details about the expiration details (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('expiresAfter')

	@property
	def InstanceId(self):
		"""It gives details about the instance id (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('instanceId')

	@property
	def Ipv4ErrorMapRegisterRx(self):
		"""It gives details about the ipv4 Error Map register at receivers end (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv4ErrorMapRegisterRx')

	@property
	def Ipv4MapNotifyTx(self):
		"""It gives details about the ipv4 Map notify at transmitters end (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapNotifyTx')

	@property
	def Ipv4MapRegisterRx(self):
		"""It gives details about the ipv4 Map register at receivers end (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRegisterRx')

	@property
	def Ipv4MapRequestDropped(self):
		"""It gives details about the ipv4 Map Request dropped (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv4MapRequestDropped')

	@property
	def Ipv6ErrorMapRegisterRx(self):
		"""It gives details about the ipv6 Error Map register at receivers end (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv6ErrorMapRegisterRx')

	@property
	def Ipv6MapNotifyTx(self):
		"""It gives details about the ipv6 Map notify at transmitters end (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapNotifyTx')

	@property
	def Ipv6MapRegisterRx(self):
		"""It gives details about the ipv6 Map register at receivers end (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRegisterRx')

	@property
	def Ipv6MapRequestDropped(self):
		"""It gives details about the ipv6 Map Request dropped (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('ipv6MapRequestDropped')

	@property
	def Key(self):
		"""It gives details about the key (Read-only)

		Returns:
			str
		"""
		return self._get_attribute('key')

	@property
	def MapVersionNumber(self):
		"""It gives details map version number

		Returns:
			number
		"""
		return self._get_attribute('mapVersionNumber')

	@property
	def ProxyMapReply(self):
		"""It gives details about the proxy map reply(Read-Only)

		Returns:
			bool
		"""
		return self._get_attribute('proxyMapReply')

	@property
	def WantMapNotify(self):
		"""It gives details about the Map notify

		Returns:
			bool
		"""
		return self._get_attribute('wantMapNotify')

	def find(self, Action=None, EidPrefix=None, EidPrefixAfi=None, EidPrefixLength=None, EtrIp=None, ExpiresAfter=None, InstanceId=None, Ipv4ErrorMapRegisterRx=None, Ipv4MapNotifyTx=None, Ipv4MapRegisterRx=None, Ipv4MapRequestDropped=None, Ipv6ErrorMapRegisterRx=None, Ipv6MapNotifyTx=None, Ipv6MapRegisterRx=None, Ipv6MapRequestDropped=None, Key=None, MapVersionNumber=None, ProxyMapReply=None, WantMapNotify=None):
		"""Finds and retrieves mapServerCacheInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve mapServerCacheInfo data from the server.
		By default the find method takes no parameters and will retrieve all mapServerCacheInfo data from the server.

		Args:
			Action (str): It gives details about the action (Read-Only)
			EidPrefix (str): It gives details about the eid prefix (Read-Only)
			EidPrefixAfi (str): It gives details about the eid prefix Afi (Read-Only)
			EidPrefixLength (number): It gives details about the eid prefix Length (Read-Only)
			EtrIp (str): It gives details about the etrlp (Read-Only)
			ExpiresAfter (str): It gives details about the expiration details (Read-Only)
			InstanceId (number): It gives details about the instance id (Read-Only)
			Ipv4ErrorMapRegisterRx (number): It gives details about the ipv4 Error Map register at receivers end (Read-Only)
			Ipv4MapNotifyTx (number): It gives details about the ipv4 Map notify at transmitters end (Read-Only)
			Ipv4MapRegisterRx (number): It gives details about the ipv4 Map register at receivers end (Read-Only)
			Ipv4MapRequestDropped (number): It gives details about the ipv4 Map Request dropped (Read-Only)
			Ipv6ErrorMapRegisterRx (number): It gives details about the ipv6 Error Map register at receivers end (Read-Only)
			Ipv6MapNotifyTx (number): It gives details about the ipv6 Map notify at transmitters end (Read-Only)
			Ipv6MapRegisterRx (number): It gives details about the ipv6 Map register at receivers end (Read-Only)
			Ipv6MapRequestDropped (number): It gives details about the ipv6 Map Request dropped (Read-Only)
			Key (str): It gives details about the key (Read-only)
			MapVersionNumber (number): It gives details map version number
			ProxyMapReply (bool): It gives details about the proxy map reply(Read-Only)
			WantMapNotify (bool): It gives details about the Map notify

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
