from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Flapping(Base):
	"""The Flapping class encapsulates a required flapping node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Flapping property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flapping'

	def __init__(self, parent):
		super(Flapping, self).__init__(parent)

	@property
	def DownTime(self):
		"""During route flapping operation, the amount of time that the route ranges are withdrawn/down.

		Returns:
			number
		"""
		return self._get_attribute('downTime')
	@DownTime.setter
	def DownTime(self, value):
		self._set_attribute('downTime', value)

	@property
	def EnablePartialFlap(self):
		"""If enabled, only a specified range of routes is flapped.

		Returns:
			bool
		"""
		return self._get_attribute('enablePartialFlap')
	@EnablePartialFlap.setter
	def EnablePartialFlap(self, value):
		self._set_attribute('enablePartialFlap', value)

	@property
	def Enabled(self):
		"""If true, enables route flapping.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def RoutesToFlapFrom(self):
		"""The first route in the route range to be flapped.

		Returns:
			number
		"""
		return self._get_attribute('routesToFlapFrom')
	@RoutesToFlapFrom.setter
	def RoutesToFlapFrom(self, value):
		self._set_attribute('routesToFlapFrom', value)

	@property
	def RoutesToFlapTo(self):
		"""The last route in the route range to be flapped.

		Returns:
			number
		"""
		return self._get_attribute('routesToFlapTo')
	@RoutesToFlapTo.setter
	def RoutesToFlapTo(self, value):
		self._set_attribute('routesToFlapTo', value)

	@property
	def UpTime(self):
		"""During the route flapping operation, the amount of time that the route ranges are up.

		Returns:
			number
		"""
		return self._get_attribute('upTime')
	@UpTime.setter
	def UpTime(self, value):
		self._set_attribute('upTime', value)
