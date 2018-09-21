from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class QueueProperty(Base):
	"""The QueueProperty class encapsulates a required queueProperty node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the QueueProperty property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'queueProperty'

	def __init__(self, parent):
		super(QueueProperty, self).__init__(parent)

	@property
	def MinimumDataRateGuaranteed(self):
		"""If true, indicates that a minimum data rate is guaranteed.

		Returns:
			bool
		"""
		return self._get_attribute('minimumDataRateGuaranteed')
	@MinimumDataRateGuaranteed.setter
	def MinimumDataRateGuaranteed(self, value):
		self._set_attribute('minimumDataRateGuaranteed', value)

	@property
	def None(self):
		"""If true, indicates that no property is defined for the queue.

		Returns:
			bool
		"""
		return self._get_attribute('none')
	@None.setter
	def None(self, value):
		self._set_attribute('none', value)
