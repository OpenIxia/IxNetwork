from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RemoteIpv4Address(Base):
	"""The RemoteIpv4Address class encapsulates a required remoteIpv4Address node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RemoteIpv4Address property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'remoteIpv4Address'

	def __init__(self, parent):
		super(RemoteIpv4Address, self).__init__(parent)

	@property
	def Count(self):
		"""total number of values

		Returns:
			number
		"""
		return self._get_attribute('count')
