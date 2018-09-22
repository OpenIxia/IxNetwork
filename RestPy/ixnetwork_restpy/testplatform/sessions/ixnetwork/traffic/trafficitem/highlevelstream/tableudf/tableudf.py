from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TableUdf(Base):
	"""The TableUdf class encapsulates a system managed tableUdf node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TableUdf property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tableUdf'

	def __init__(self, parent):
		super(TableUdf, self).__init__(parent)

	@property
	def Column(self):
		"""An instance of the Column class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.column.column.Column)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.column.column import Column
		return Column(self)

	@property
	def Enabled(self):
		"""If enabled, enables the UDF table for this flow group if it is supported.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	def find(self, Enabled=None):
		"""Finds and retrieves tableUdf data from the server.

		All named parameters support regex and can be used to selectively retrieve tableUdf data from the server.
		By default the find method takes no parameters and will retrieve all tableUdf data from the server.

		Args:
			Enabled (bool): If enabled, enables the UDF table for this flow group if it is supported.

		Returns:
			self: This instance with matching tableUdf data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tableUdf data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tableUdf data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
