from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TargetPeer(Base):
	"""The TargetPeer class encapsulates a user managed targetPeer node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TargetPeer property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'targetPeer'

	def __init__(self, parent):
		super(TargetPeer, self).__init__(parent)

	@property
	def Authentication(self):
		"""The cryptographic authentication type used by the targeted peer; one of: NULL (no authentication) or MD5. When MD5 is used, an md5Key must be configured by the user.

		Returns:
			str(null|md5)
		"""
		return self._get_attribute('authentication')
	@Authentication.setter
	def Authentication(self, value):
		self._set_attribute('authentication', value)

	@property
	def Enabled(self):
		"""Enables the use of this targeted peer.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InitiateTargetedHello(self):
		"""If true, the target peer is set a hello message exclusively.

		Returns:
			bool
		"""
		return self._get_attribute('initiateTargetedHello')
	@InitiateTargetedHello.setter
	def InitiateTargetedHello(self, value):
		self._set_attribute('initiateTargetedHello', value)

	@property
	def IpAddress(self):
		"""The IP address of the targeted peer.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
	@IpAddress.setter
	def IpAddress(self, value):
		self._set_attribute('ipAddress', value)

	@property
	def Md5Key(self):
		"""Used with MD5 authentication. A user-defined string; maximum = 255 characters.

		Returns:
			str
		"""
		return self._get_attribute('md5Key')
	@Md5Key.setter
	def Md5Key(self, value):
		self._set_attribute('md5Key', value)

	def add(self, Authentication=None, Enabled=None, InitiateTargetedHello=None, IpAddress=None, Md5Key=None):
		"""Adds a new targetPeer node on the server and retrieves it in this instance.

		Args:
			Authentication (str(null|md5)): The cryptographic authentication type used by the targeted peer; one of: NULL (no authentication) or MD5. When MD5 is used, an md5Key must be configured by the user.
			Enabled (bool): Enables the use of this targeted peer.
			InitiateTargetedHello (bool): If true, the target peer is set a hello message exclusively.
			IpAddress (str): The IP address of the targeted peer.
			Md5Key (str): Used with MD5 authentication. A user-defined string; maximum = 255 characters.

		Returns:
			self: This instance with all currently retrieved targetPeer data using find and the newly added targetPeer data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the targetPeer data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Authentication=None, Enabled=None, InitiateTargetedHello=None, IpAddress=None, Md5Key=None):
		"""Finds and retrieves targetPeer data from the server.

		All named parameters support regex and can be used to selectively retrieve targetPeer data from the server.
		By default the find method takes no parameters and will retrieve all targetPeer data from the server.

		Args:
			Authentication (str(null|md5)): The cryptographic authentication type used by the targeted peer; one of: NULL (no authentication) or MD5. When MD5 is used, an md5Key must be configured by the user.
			Enabled (bool): Enables the use of this targeted peer.
			InitiateTargetedHello (bool): If true, the target peer is set a hello message exclusively.
			IpAddress (str): The IP address of the targeted peer.
			Md5Key (str): Used with MD5 authentication. A user-defined string; maximum = 255 characters.

		Returns:
			self: This instance with matching targetPeer data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of targetPeer data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the targetPeer data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
