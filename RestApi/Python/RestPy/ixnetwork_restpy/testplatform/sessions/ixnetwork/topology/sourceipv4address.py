from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SourceIpv4Address(Base):
	"""The SourceIpv4Address class encapsulates a required sourceIpv4Address node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SourceIpv4Address property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'sourceIpv4Address'

	def __init__(self, parent):
		super(SourceIpv4Address, self).__init__(parent)

	@property
	def Count(self):
		"""total number of values

		Returns:
			number
		"""
		return self._get_attribute('count')
