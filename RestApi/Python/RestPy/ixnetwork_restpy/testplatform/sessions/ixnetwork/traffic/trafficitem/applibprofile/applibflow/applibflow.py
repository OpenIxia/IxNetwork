from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AppLibFlow(Base):
	"""The AppLibFlow class encapsulates a system managed appLibFlow node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AppLibFlow property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'appLibFlow'

	def __init__(self, parent):
		super(AppLibFlow, self).__init__(parent)

	@property
	def Connection(self):
		"""An instance of the Connection class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.connection.Connection)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.connection import Connection
		return Connection(self)

	@property
	def Parameter(self):
		"""An instance of the Parameter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.parameter.parameter.Parameter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.parameter.parameter import Parameter
		return Parameter(self)

	@property
	def ConfigId(self):
		"""The internal config id asociated with this flow.

		Returns:
			number
		"""
		return self._get_attribute('configId')

	@property
	def ConnectionCount(self):
		"""Number of connections in this flow.

		Returns:
			number
		"""
		return self._get_attribute('connectionCount')

	@property
	def Description(self):
		"""Brief description of what the flow does.

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def FlowId(self):
		"""The identifier of the flow.

		Returns:
			str
		"""
		return self._get_attribute('flowId')

	@property
	def FlowSize(self):
		"""The size of the flow in bytes.

		Returns:
			number
		"""
		return self._get_attribute('flowSize')

	@property
	def Name(self):
		"""the name of the Flow.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Parameters(self):
		"""Array containing configurable parameters per flow.

		Returns:
			list(str)
		"""
		return self._get_attribute('parameters')

	@property
	def Percentage(self):
		"""The amount of traffic generated for this flows.

		Returns:
			number
		"""
		return self._get_attribute('percentage')
	@Percentage.setter
	def Percentage(self, value):
		self._set_attribute('percentage', value)

	def find(self, ConfigId=None, ConnectionCount=None, Description=None, FlowId=None, FlowSize=None, Name=None, Parameters=None, Percentage=None):
		"""Finds and retrieves appLibFlow data from the server.

		All named parameters support regex and can be used to selectively retrieve appLibFlow data from the server.
		By default the find method takes no parameters and will retrieve all appLibFlow data from the server.

		Args:
			ConfigId (number): The internal config id asociated with this flow.
			ConnectionCount (number): Number of connections in this flow.
			Description (str): Brief description of what the flow does.
			FlowId (str): The identifier of the flow.
			FlowSize (number): The size of the flow in bytes.
			Name (str): the name of the Flow.
			Parameters (list(str)): Array containing configurable parameters per flow.
			Percentage (number): The amount of traffic generated for this flows.

		Returns:
			self: This instance with matching appLibFlow data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of appLibFlow data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the appLibFlow data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
