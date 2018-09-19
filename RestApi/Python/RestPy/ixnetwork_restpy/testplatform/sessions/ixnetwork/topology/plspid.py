from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PlspId(Base):
	"""The PlspId class encapsulates a required plspId node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PlspId property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'plspId'

	def __init__(self, parent):
		super(PlspId, self).__init__(parent)

	@property
	def Count(self):
		"""total number of values

		Returns:
			number
		"""
		return self._get_attribute('count')
