from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TableModificationTriggerAttributes(Base):
	"""The TableModificationTriggerAttributes class encapsulates a required tableModificationTriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TableModificationTriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'tableModificationTriggerAttributes'

	def __init__(self, parent):
		super(TableModificationTriggerAttributes, self).__init__(parent)

	@property
	def AllTables(self):
		"""To apply the change to all tables.

		Returns:
			bool
		"""
		return self._get_attribute('allTables')
	@AllTables.setter
	def AllTables(self, value):
		self._set_attribute('allTables', value)

	@property
	def Config(self):
		"""2.Type the value of the Config.

		Returns:
			number
		"""
		return self._get_attribute('config')
	@Config.setter
	def Config(self, value):
		self._set_attribute('config', value)
