from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Community(Base):
	"""The Community class encapsulates a required community node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Community property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'community'

	def __init__(self, parent):
		super(Community, self).__init__(parent)

	@property
	def Val(self):
		"""The value of the community attribute.

		Returns:
			list(number)
		"""
		return self._get_attribute('val')
	@Val.setter
	def Val(self, value):
		self._set_attribute('val', value)
