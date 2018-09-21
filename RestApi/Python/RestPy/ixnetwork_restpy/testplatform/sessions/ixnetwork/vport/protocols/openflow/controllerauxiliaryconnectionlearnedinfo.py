from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ControllerAuxiliaryConnectionLearnedInfo(Base):
	"""The ControllerAuxiliaryConnectionLearnedInfo class encapsulates a system managed controllerAuxiliaryConnectionLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ControllerAuxiliaryConnectionLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'controllerAuxiliaryConnectionLearnedInfo'

	def __init__(self, parent):
		super(ControllerAuxiliaryConnectionLearnedInfo, self).__init__(parent)

	@property
	def AuxiliaryId(self):
		"""This describes the identifier for auxiliary connections.

		Returns:
			number
		"""
		return self._get_attribute('auxiliaryId')

	@property
	def ConnectionType(self):
		"""Specifies how this controllerPort is connected to another controller (internal/external) or host or there is no connection (noConnection)

		Returns:
			str(tcp|tls|udp)
		"""
		return self._get_attribute('connectionType')

	@property
	def DataPathId(self):
		"""Indicates the datapath ID of the OpenFlow controller.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Indicates the datapath ID of the OpenFlow controller in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def LocalIp(self):
		"""Signifies the local IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def LocalPort(self):
		"""This describes the local port number identifier.

		Returns:
			number
		"""
		return self._get_attribute('localPort')

	@property
	def RemoteIp(self):
		"""This describes the IP address of the remote end of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def RemotePort(self):
		"""This describes the remote port number identifier.

		Returns:
			number
		"""
		return self._get_attribute('remotePort')

	def find(self, AuxiliaryId=None, ConnectionType=None, DataPathId=None, DataPathIdAsHex=None, LocalIp=None, LocalPort=None, RemoteIp=None, RemotePort=None):
		"""Finds and retrieves controllerAuxiliaryConnectionLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve controllerAuxiliaryConnectionLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all controllerAuxiliaryConnectionLearnedInfo data from the server.

		Args:
			AuxiliaryId (number): This describes the identifier for auxiliary connections.
			ConnectionType (str(tcp|tls|udp)): Specifies how this controllerPort is connected to another controller (internal/external) or host or there is no connection (noConnection)
			DataPathId (str): Indicates the datapath ID of the OpenFlow controller.
			DataPathIdAsHex (str): Indicates the datapath ID of the OpenFlow controller in hexadecimal format.
			LocalIp (str): Signifies the local IP address of the selected interface.
			LocalPort (number): This describes the local port number identifier.
			RemoteIp (str): This describes the IP address of the remote end of the OF Channel.
			RemotePort (number): This describes the remote port number identifier.

		Returns:
			self: This instance with matching controllerAuxiliaryConnectionLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of controllerAuxiliaryConnectionLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the controllerAuxiliaryConnectionLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
