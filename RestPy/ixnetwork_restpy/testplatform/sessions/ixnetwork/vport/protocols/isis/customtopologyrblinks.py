from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologyRbLinks(Base):
	"""The CustomTopologyRbLinks class encapsulates a user managed customTopologyRbLinks node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyRbLinks property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyRbLinks'

	def __init__(self, parent):
		super(CustomTopologyRbLinks, self).__init__(parent)

	@property
	def Enabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def LinkMetric(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')
	@LinkMetric.setter
	def LinkMetric(self, value):
		self._set_attribute('linkMetric', value)

	@property
	def LinkNodeSystemId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('linkNodeSystemId')
	@LinkNodeSystemId.setter
	def LinkNodeSystemId(self, value):
		self._set_attribute('linkNodeSystemId', value)

	def add(self, Enabled=None, LinkMetric=None, LinkNodeSystemId=None):
		"""Adds a new customTopologyRbLinks node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): NOT DEFINED
			LinkMetric (number): NOT DEFINED
			LinkNodeSystemId (str): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologyRbLinks data using find and the newly added customTopologyRbLinks data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyRbLinks data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, LinkMetric=None, LinkNodeSystemId=None):
		"""Finds and retrieves customTopologyRbLinks data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyRbLinks data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyRbLinks data from the server.

		Args:
			Enabled (bool): NOT DEFINED
			LinkMetric (number): NOT DEFINED
			LinkNodeSystemId (str): NOT DEFINED

		Returns:
			self: This instance with matching customTopologyRbLinks data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyRbLinks data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyRbLinks data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
