from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IpVersion(Base):
	"""The IpVersion class encapsulates a required ipVersion node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IpVersion property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ipVersion'

	def __init__(self, parent):
		super(IpVersion, self).__init__(parent)

	@property
	def Count(self):
		"""total number of values

		Returns:
			number
		"""
		return self._get_attribute('count')
