from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Hypervisor(Base):
	"""The Hypervisor class encapsulates a user managed hypervisor node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Hypervisor property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'hypervisor'

	def __init__(self, parent):
		super(Hypervisor, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true the hypervisor is enabled

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Password(self):
		"""Represents the hypervisor password

		Returns:
			str
		"""
		return self._get_attribute('password')
	@Password.setter
	def Password(self, value):
		self._set_attribute('password', value)

	@property
	def ServerIp(self):
		"""Represents the hypervisor Ip

		Returns:
			str
		"""
		return self._get_attribute('serverIp')
	@ServerIp.setter
	def ServerIp(self, value):
		self._set_attribute('serverIp', value)

	@property
	def Type(self):
		"""Represents the hypervisor host type

		Returns:
			str(qemu|vCenter|vmware)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def User(self):
		"""Represents the hypervisor username

		Returns:
			str
		"""
		return self._get_attribute('user')
	@User.setter
	def User(self, value):
		self._set_attribute('user', value)

	def add(self, Enabled=None, Password=None, ServerIp=None, Type=None, User=None):
		"""Adds a new hypervisor node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true the hypervisor is enabled
			Password (str): Represents the hypervisor password
			ServerIp (str): Represents the hypervisor Ip
			Type (str(qemu|vCenter|vmware)): Represents the hypervisor host type
			User (str): Represents the hypervisor username

		Returns:
			self: This instance with all currently retrieved hypervisor data using find and the newly added hypervisor data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the hypervisor data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, Password=None, ServerIp=None, Type=None, User=None):
		"""Finds and retrieves hypervisor data from the server.

		All named parameters support regex and can be used to selectively retrieve hypervisor data from the server.
		By default the find method takes no parameters and will retrieve all hypervisor data from the server.

		Args:
			Enabled (bool): If true the hypervisor is enabled
			Password (str): Represents the hypervisor password
			ServerIp (str): Represents the hypervisor Ip
			Type (str(qemu|vCenter|vmware)): Represents the hypervisor host type
			User (str): Represents the hypervisor username

		Returns:
			self: This instance with matching hypervisor data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of hypervisor data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the hypervisor data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
