from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MultipleJoinLeaveLatency(Base):
	"""The MultipleJoinLeaveLatency class encapsulates a required multipleJoinLeaveLatency node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MultipleJoinLeaveLatency property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'multipleJoinLeaveLatency'

	def __init__(self, parent):
		super(MultipleJoinLeaveLatency, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true enables multiple join leave latency.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
