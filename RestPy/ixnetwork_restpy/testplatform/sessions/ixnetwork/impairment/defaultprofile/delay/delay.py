from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Delay(Base):
	"""The Delay class encapsulates a required delay node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Delay property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'delay'

	def __init__(self, parent):
		super(Delay, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, delay packets.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Units(self):
		"""Specify the units for the delay value.

		Returns:
			str(kilometers|kKilometers|kMicroseconds|kMilliseconds|kSeconds|microseconds|milliseconds|seconds)
		"""
		return self._get_attribute('units')
	@Units.setter
	def Units(self, value):
		self._set_attribute('units', value)

	@property
	def Value(self):
		"""Time to delay each packet.

		Returns:
			number
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
