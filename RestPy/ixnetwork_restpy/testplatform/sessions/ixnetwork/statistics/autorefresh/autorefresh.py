from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AutoRefresh(Base):
	"""The AutoRefresh class encapsulates a required autoRefresh node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AutoRefresh property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'autoRefresh'

	def __init__(self, parent):
		super(AutoRefresh, self).__init__(parent)

	@property
	def Enabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def MinRefreshInterval(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('minRefreshInterval')
	@MinRefreshInterval.setter
	def MinRefreshInterval(self, value):
		self._set_attribute('minRefreshInterval', value)
