from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Prbs(Base):
	"""The Prbs class encapsulates a required prbs node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Prbs property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'prbs'

	def __init__(self, parent):
		super(Prbs, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables and fetches Pseudo-Random Bit Sequence (PRBS) statistics

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
