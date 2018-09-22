from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ErroredFrameTlv(Base):
	"""The ErroredFrameTlv class encapsulates a required erroredFrameTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ErroredFrameTlv property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'erroredFrameTlv'

	def __init__(self, parent):
		super(ErroredFrameTlv, self).__init__(parent)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Frames(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('frames')
	@Frames.setter
	def Frames(self, value):
		self._set_attribute('frames', value)

	@property
	def Threshold(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('threshold')
	@Threshold.setter
	def Threshold(self, value):
		self._set_attribute('threshold', value)

	@property
	def Window(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('window')
	@Window.setter
	def Window(self, value):
		self._set_attribute('window', value)
