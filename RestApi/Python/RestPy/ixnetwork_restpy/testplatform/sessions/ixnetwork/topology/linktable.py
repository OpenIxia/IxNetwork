from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LinkTable(Base):
	"""The LinkTable class encapsulates a required linkTable node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkTable property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'linkTable'

	def __init__(self, parent):
		super(LinkTable, self).__init__(parent)

	@property
	def FromNodeIndex(self):
		"""from node index.

		Returns:
			list(str)
		"""
		return self._get_attribute('fromNodeIndex')
	@FromNodeIndex.setter
	def FromNodeIndex(self, value):
		self._set_attribute('fromNodeIndex', value)

	@property
	def ToNodeIndex(self):
		"""to node index.

		Returns:
			list(str)
		"""
		return self._get_attribute('toNodeIndex')
	@ToNodeIndex.setter
	def ToNodeIndex(self, value):
		self._set_attribute('toNodeIndex', value)
