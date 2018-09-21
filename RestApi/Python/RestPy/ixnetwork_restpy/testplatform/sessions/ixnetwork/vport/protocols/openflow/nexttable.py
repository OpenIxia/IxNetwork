from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NextTable(Base):
	"""The NextTable class encapsulates a required nextTable node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NextTable property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'nextTable'

	def __init__(self, parent):
		super(NextTable, self).__init__(parent)

	@property
	def TableId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('tableId')
	@TableId.setter
	def TableId(self, value):
		self._set_attribute('tableId', value)

	@property
	def TableIdMiss(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('tableIdMiss')
	@TableIdMiss.setter
	def TableIdMiss(self, value):
		self._set_attribute('tableIdMiss', value)
