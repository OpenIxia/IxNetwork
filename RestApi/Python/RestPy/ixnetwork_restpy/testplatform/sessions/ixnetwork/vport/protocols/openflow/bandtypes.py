from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BandTypes(Base):
	"""The BandTypes class encapsulates a required bandTypes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BandTypes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bandTypes'

	def __init__(self, parent):
		super(BandTypes, self).__init__(parent)

	@property
	def Drop(self):
		"""This indicates that packets which exceed the band rate value are dropped.

		Returns:
			bool
		"""
		return self._get_attribute('drop')
	@Drop.setter
	def Drop(self, value):
		self._set_attribute('drop', value)

	@property
	def DscpRemark(self):
		"""This indicates that the drop precedence of the DSCP field is remarked in the IP header of the packets that exceed the band rate value.

		Returns:
			bool
		"""
		return self._get_attribute('dscpRemark')
	@DscpRemark.setter
	def DscpRemark(self, value):
		self._set_attribute('dscpRemark', value)
