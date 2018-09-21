from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interface(Base):
	"""The Interface class encapsulates a user managed interface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables this particular RIPng interface.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def InterfaceId(self):
		"""The assigned interface ID.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceMetric(self):
		"""The value of the metric assigned to this particular interface. This value is added to the RIPng routing metric before transmission on this interface. It allows metrics for routes with the same standard RIPng routing metric to be identified by the particular interface.The default value is'0. Care should be taken so the combined metric value for a route does not exceed 15. A combined metric of 16 or above indicates that the route is unreachable.

		Returns:
			number
		"""
		return self._get_attribute('interfaceMetric')
	@InterfaceMetric.setter
	def InterfaceMetric(self, value):
		self._set_attribute('interfaceMetric', value)

	@property
	def ResponseMode(self):
		"""The response mode of the RIPng interface.

		Returns:
			str(splitHorizon|noSplitHorizon|poisonReverse)
		"""
		return self._get_attribute('responseMode')
	@ResponseMode.setter
	def ResponseMode(self, value):
		self._set_attribute('responseMode', value)

	def add(self, Enabled=None, InterfaceId=None, InterfaceMetric=None, ResponseMode=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables this particular RIPng interface.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The assigned interface ID.
			InterfaceMetric (number): The value of the metric assigned to this particular interface. This value is added to the RIPng routing metric before transmission on this interface. It allows metrics for routes with the same standard RIPng routing metric to be identified by the particular interface.The default value is'0. Care should be taken so the combined metric value for a route does not exceed 15. A combined metric of 16 or above indicates that the route is unreachable.
			ResponseMode (str(splitHorizon|noSplitHorizon|poisonReverse)): The response mode of the RIPng interface.

		Returns:
			self: This instance with all currently retrieved interface data using find and the newly added interface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InterfaceId=None, InterfaceMetric=None, ResponseMode=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			Enabled (bool): Enables this particular RIPng interface.
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The assigned interface ID.
			InterfaceMetric (number): The value of the metric assigned to this particular interface. This value is added to the RIPng routing metric before transmission on this interface. It allows metrics for routes with the same standard RIPng routing metric to be identified by the particular interface.The default value is'0. Care should be taken so the combined metric value for a route does not exceed 15. A combined metric of 16 or above indicates that the route is unreachable.
			ResponseMode (str(splitHorizon|noSplitHorizon|poisonReverse)): The response mode of the RIPng interface.

		Returns:
			self: This instance with matching interface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
