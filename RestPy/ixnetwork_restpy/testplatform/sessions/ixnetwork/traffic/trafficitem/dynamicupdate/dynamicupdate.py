from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DynamicUpdate(Base):
	"""The DynamicUpdate class encapsulates a system managed dynamicUpdate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DynamicUpdate property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'dynamicUpdate'

	def __init__(self, parent):
		super(DynamicUpdate, self).__init__(parent)

	@property
	def AvailableDynamicUpdateFields(self):
		"""(Read only) Specifies the available Dynamic Updates support.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableDynamicUpdateFields')

	@property
	def AvailableSessionAwareTrafficFields(self):
		"""(Read only) Specifies the available Kill Bit support.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableSessionAwareTrafficFields')

	@property
	def EnabledDynamicUpdateFields(self):
		"""If true, enables the Dynamic Updates support.

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledDynamicUpdateFields')
	@EnabledDynamicUpdateFields.setter
	def EnabledDynamicUpdateFields(self, value):
		self._set_attribute('enabledDynamicUpdateFields', value)

	@property
	def EnabledDynamicUpdateFieldsDisplayNames(self):
		"""Returns user friendly list of dynamic update fields

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledDynamicUpdateFieldsDisplayNames')

	@property
	def EnabledSessionAwareTrafficFields(self):
		"""If true, enables the Kill Bit support.

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledSessionAwareTrafficFields')
	@EnabledSessionAwareTrafficFields.setter
	def EnabledSessionAwareTrafficFields(self, value):
		self._set_attribute('enabledSessionAwareTrafficFields', value)

	def find(self, AvailableDynamicUpdateFields=None, AvailableSessionAwareTrafficFields=None, EnabledDynamicUpdateFields=None, EnabledDynamicUpdateFieldsDisplayNames=None, EnabledSessionAwareTrafficFields=None):
		"""Finds and retrieves dynamicUpdate data from the server.

		All named parameters support regex and can be used to selectively retrieve dynamicUpdate data from the server.
		By default the find method takes no parameters and will retrieve all dynamicUpdate data from the server.

		Args:
			AvailableDynamicUpdateFields (list(str)): (Read only) Specifies the available Dynamic Updates support.
			AvailableSessionAwareTrafficFields (list(str)): (Read only) Specifies the available Kill Bit support.
			EnabledDynamicUpdateFields (list(str)): If true, enables the Dynamic Updates support.
			EnabledDynamicUpdateFieldsDisplayNames (list(str)): Returns user friendly list of dynamic update fields
			EnabledSessionAwareTrafficFields (list(str)): If true, enables the Kill Bit support.

		Returns:
			self: This instance with matching dynamicUpdate data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dynamicUpdate data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dynamicUpdate data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
