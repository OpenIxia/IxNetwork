from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Connection(Base):
	"""The Connection class encapsulates a system managed connection node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Connection property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'connection'

	def __init__(self, parent):
		super(Connection, self).__init__(parent)

	@property
	def Parameter(self):
		"""An instance of the Parameter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.parameter.Parameter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.parameter import Parameter
		return Parameter(self)

	@property
	def ConnectionId(self):
		"""(Read only) Application library flow connection id.

		Returns:
			number
		"""
		return self._get_attribute('connectionId')

	@property
	def ConnectionParams(self):
		"""(Read only) Names of parameter available on application flow connection.

		Returns:
			list(str)
		"""
		return self._get_attribute('connectionParams')

	@property
	def IsTCP(self):
		"""(Read only) Application library flow connection type - true is the type is TCP, false if it's UDP.

		Returns:
			bool
		"""
		return self._get_attribute('isTCP')

	def find(self, ConnectionId=None, ConnectionParams=None, IsTCP=None):
		"""Finds and retrieves connection data from the server.

		All named parameters support regex and can be used to selectively retrieve connection data from the server.
		By default the find method takes no parameters and will retrieve all connection data from the server.

		Args:
			ConnectionId (number): (Read only) Application library flow connection id.
			ConnectionParams (list(str)): (Read only) Names of parameter available on application flow connection.
			IsTCP (bool): (Read only) Application library flow connection type - true is the type is TCP, false if it's UDP.

		Returns:
			self: This instance with matching connection data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of connection data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the connection data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
