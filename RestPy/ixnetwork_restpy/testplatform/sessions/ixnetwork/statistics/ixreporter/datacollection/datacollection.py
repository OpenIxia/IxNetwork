from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DataCollection(Base):
	"""The DataCollection class encapsulates a required dataCollection node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DataCollection property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dataCollection'

	def __init__(self, parent):
		super(DataCollection, self).__init__(parent)

	@property
	def Enable(self):
		"""If it is true, enables collection of data

		Returns:
			bool
		"""
		return self._get_attribute('Enable')
	@Enable.setter
	def Enable(self, value):
		self._set_attribute('Enable', value)

	@property
	def LastRunId(self):
		"""Specifies the identifier for last run.

		Returns:
			number
		"""
		return self._get_attribute('LastRunId')
