from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Connector(Base):
	"""The Connector class encapsulates a user managed connector node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Connector property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'connector'

	def __init__(self, parent):
		super(Connector, self).__init__(parent)

	@property
	def ConnectedTo(self):
		"""Scenario element this connector is connecting to

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*)
		"""
		return self._get_attribute('connectedTo')
	@ConnectedTo.setter
	def ConnectedTo(self, value):
		self._set_attribute('connectedTo', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def PropagateMultiplier(self):
		"""The Connector will propagate the multiplicity of destination back to the source and its parent NetworkElementSet

		Returns:
			bool
		"""
		return self._get_attribute('propagateMultiplier')

	def add(self, ConnectedTo=None):
		"""Adds a new connector node on the server and retrieves it in this instance.

		Args:
			ConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*)): Scenario element this connector is connecting to

		Returns:
			self: This instance with all currently retrieved connector data using find and the newly added connector data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the connector data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedTo=None, Count=None, PropagateMultiplier=None):
		"""Finds and retrieves connector data from the server.

		All named parameters support regex and can be used to selectively retrieve connector data from the server.
		By default the find method takes no parameters and will retrieve all connector data from the server.

		Args:
			ConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*)): Scenario element this connector is connecting to
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			PropagateMultiplier (bool): The Connector will propagate the multiplicity of destination back to the source and its parent NetworkElementSet

		Returns:
			self: This instance with matching connector data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of connector data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the connector data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
