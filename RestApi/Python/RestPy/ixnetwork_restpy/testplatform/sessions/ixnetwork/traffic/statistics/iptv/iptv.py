from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Iptv(Base):
	"""The Iptv class encapsulates a required iptv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Iptv property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'iptv'

	def __init__(self, parent):
		super(Iptv, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, enables IPTV

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
