from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MapServerResolver(Base):
	"""The MapServerResolver class encapsulates a user managed mapServerResolver node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MapServerResolver property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'mapServerResolver'

	def __init__(self, parent):
		super(MapServerResolver, self).__init__(parent)

	@property
	def AuthenticationAlgorithm(self):
		"""It gives details about the authentication algorithm

		Returns:
			str(sha-1-96|sha-128-256)
		"""
		return self._get_attribute('authenticationAlgorithm')
	@AuthenticationAlgorithm.setter
	def AuthenticationAlgorithm(self, value):
		self._set_attribute('authenticationAlgorithm', value)

	@property
	def Enabled(self):
		"""If true, it enables the protocol

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExternalMsmrAddress(self):
		"""It gives details about the external Msmr address

		Returns:
			str
		"""
		return self._get_attribute('externalMsmrAddress')
	@ExternalMsmrAddress.setter
	def ExternalMsmrAddress(self, value):
		self._set_attribute('externalMsmrAddress', value)

	@property
	def Family(self):
		"""It gives details about the ip family it represents

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('family')
	@Family.setter
	def Family(self, value):
		self._set_attribute('family', value)

	@property
	def InternalIxiaMsmrRouter(self):
		"""It gives details about the internal ixia msmr router

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)
		"""
		return self._get_attribute('internalIxiaMsmrRouter')
	@InternalIxiaMsmrRouter.setter
	def InternalIxiaMsmrRouter(self, value):
		self._set_attribute('internalIxiaMsmrRouter', value)

	@property
	def Key(self):
		"""it gives details about the key

		Returns:
			str
		"""
		return self._get_attribute('key')
	@Key.setter
	def Key(self, value):
		self._set_attribute('key', value)

	@property
	def MsmrLocation(self):
		"""It details about the msmr location

		Returns:
			str(internal|external)
		"""
		return self._get_attribute('msmrLocation')
	@MsmrLocation.setter
	def MsmrLocation(self, value):
		self._set_attribute('msmrLocation', value)

	@property
	def Type(self):
		"""It gives details about the type

		Returns:
			str(ms|mr|msmr)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, AuthenticationAlgorithm=None, Enabled=None, ExternalMsmrAddress=None, Family=None, InternalIxiaMsmrRouter=None, Key=None, MsmrLocation=None, Type=None):
		"""Adds a new mapServerResolver node on the server and retrieves it in this instance.

		Args:
			AuthenticationAlgorithm (str(sha-1-96|sha-128-256)): It gives details about the authentication algorithm
			Enabled (bool): If true, it enables the protocol
			ExternalMsmrAddress (str): It gives details about the external Msmr address
			Family (str(ipv4|ipv6)): It gives details about the ip family it represents
			InternalIxiaMsmrRouter (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): It gives details about the internal ixia msmr router
			Key (str): it gives details about the key
			MsmrLocation (str(internal|external)): It details about the msmr location
			Type (str(ms|mr|msmr)): It gives details about the type

		Returns:
			self: This instance with all currently retrieved mapServerResolver data using find and the newly added mapServerResolver data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the mapServerResolver data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AuthenticationAlgorithm=None, Enabled=None, ExternalMsmrAddress=None, Family=None, InternalIxiaMsmrRouter=None, Key=None, MsmrLocation=None, Type=None):
		"""Finds and retrieves mapServerResolver data from the server.

		All named parameters support regex and can be used to selectively retrieve mapServerResolver data from the server.
		By default the find method takes no parameters and will retrieve all mapServerResolver data from the server.

		Args:
			AuthenticationAlgorithm (str(sha-1-96|sha-128-256)): It gives details about the authentication algorithm
			Enabled (bool): If true, it enables the protocol
			ExternalMsmrAddress (str): It gives details about the external Msmr address
			Family (str(ipv4|ipv6)): It gives details about the ip family it represents
			InternalIxiaMsmrRouter (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=router)): It gives details about the internal ixia msmr router
			Key (str): it gives details about the key
			MsmrLocation (str(internal|external)): It details about the msmr location
			Type (str(ms|mr|msmr)): It gives details about the type

		Returns:
			self: This instance with matching mapServerResolver data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of mapServerResolver data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the mapServerResolver data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
