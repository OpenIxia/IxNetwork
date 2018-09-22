from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv4NodeId(Base):
	"""The Ipv4NodeId class encapsulates a required ipv4NodeId node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4NodeId property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ipv4NodeId'

	def __init__(self, parent):
		super(Ipv4NodeId, self).__init__(parent)

	@property
	def Count(self):
		"""total number of values

		Returns:
			number
		"""
		return self._get_attribute('count')
