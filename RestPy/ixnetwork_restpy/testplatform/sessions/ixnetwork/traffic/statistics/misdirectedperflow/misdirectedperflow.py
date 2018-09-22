from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MisdirectedPerFlow(Base):
	"""The MisdirectedPerFlow class encapsulates a required misdirectedPerFlow node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MisdirectedPerFlow property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'misdirectedPerFlow'

	def __init__(self, parent):
		super(MisdirectedPerFlow, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true then misdirected per flow statistics will be enabled

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
