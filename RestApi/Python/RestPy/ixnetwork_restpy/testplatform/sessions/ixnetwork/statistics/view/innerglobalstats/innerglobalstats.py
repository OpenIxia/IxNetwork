from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InnerGlobalStats(Base):
	"""The InnerGlobalStats class encapsulates a required innerGlobalStats node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InnerGlobalStats property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'innerGlobalStats'

	def __init__(self, parent):
		super(InnerGlobalStats, self).__init__(parent)

	@property
	def ColumnCaptions(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('columnCaptions')

	@property
	def RowValues(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('rowValues')
