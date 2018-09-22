from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AuxiliaryConnection(Base):
	"""The AuxiliaryConnection class encapsulates a user managed auxiliaryConnection node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AuxiliaryConnection property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'auxiliaryConnection'

	def __init__(self, parent):
		super(AuxiliaryConnection, self).__init__(parent)

	@property
	def AuxiliaryId(self):
		"""Indicates the Id of the auxiliary connection.

		Returns:
			number
		"""
		return self._get_attribute('auxiliaryId')
	@AuxiliaryId.setter
	def AuxiliaryId(self, value):
		self._set_attribute('auxiliaryId', value)

	@property
	def ConnectionType(self):
		"""Specifies how this switchPort is connected to another switch (internal/external) or host or there is no connection (noConnection)

		Returns:
			str(tcp|tls|udp)
		"""
		return self._get_attribute('connectionType')
	@ConnectionType.setter
	def ConnectionType(self, value):
		self._set_attribute('connectionType', value)

	@property
	def Enable(self):
		"""If true, the object is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enable')
	@Enable.setter
	def Enable(self, value):
		self._set_attribute('enable', value)

	@property
	def UdpSourcePortNumber(self):
		"""Specify the UDP source port number. The default value is 0. This field is available only if the Connection Type specified is UDP.

		Returns:
			number
		"""
		return self._get_attribute('udpSourcePortNumber')
	@UdpSourcePortNumber.setter
	def UdpSourcePortNumber(self, value):
		self._set_attribute('udpSourcePortNumber', value)

	def add(self, AuxiliaryId=None, ConnectionType=None, Enable=None, UdpSourcePortNumber=None):
		"""Adds a new auxiliaryConnection node on the server and retrieves it in this instance.

		Args:
			AuxiliaryId (number): Indicates the Id of the auxiliary connection.
			ConnectionType (str(tcp|tls|udp)): Specifies how this switchPort is connected to another switch (internal/external) or host or there is no connection (noConnection)
			Enable (bool): If true, the object is enabled.
			UdpSourcePortNumber (number): Specify the UDP source port number. The default value is 0. This field is available only if the Connection Type specified is UDP.

		Returns:
			self: This instance with all currently retrieved auxiliaryConnection data using find and the newly added auxiliaryConnection data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the auxiliaryConnection data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AuxiliaryId=None, ConnectionType=None, Enable=None, UdpSourcePortNumber=None):
		"""Finds and retrieves auxiliaryConnection data from the server.

		All named parameters support regex and can be used to selectively retrieve auxiliaryConnection data from the server.
		By default the find method takes no parameters and will retrieve all auxiliaryConnection data from the server.

		Args:
			AuxiliaryId (number): Indicates the Id of the auxiliary connection.
			ConnectionType (str(tcp|tls|udp)): Specifies how this switchPort is connected to another switch (internal/external) or host or there is no connection (noConnection)
			Enable (bool): If true, the object is enabled.
			UdpSourcePortNumber (number): Specify the UDP source port number. The default value is 0. This field is available only if the Connection Type specified is UDP.

		Returns:
			self: This instance with matching auxiliaryConnection data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of auxiliaryConnection data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the auxiliaryConnection data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
