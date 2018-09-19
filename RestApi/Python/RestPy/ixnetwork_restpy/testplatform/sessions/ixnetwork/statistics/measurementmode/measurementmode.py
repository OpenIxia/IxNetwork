from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MeasurementMode(Base):
	"""The MeasurementMode class encapsulates a required measurementMode node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeasurementMode property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'measurementMode'

	def __init__(self, parent):
		super(MeasurementMode, self).__init__(parent)

	@property
	def MeasurementMode(self):
		"""Mode of the measurement

		Returns:
			str(cumulativeMode|instantaneousMode|mixedMode)
		"""
		return self._get_attribute('measurementMode')
	@MeasurementMode.setter
	def MeasurementMode(self, value):
		self._set_attribute('measurementMode', value)
