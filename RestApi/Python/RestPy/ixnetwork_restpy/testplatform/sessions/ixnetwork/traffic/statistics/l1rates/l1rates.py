from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class L1Rates(Base):
	"""The L1Rates class encapsulates a required l1Rates node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the L1Rates property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'l1Rates'

	def __init__(self, parent):
		super(L1Rates, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables layer 1 rates

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
