from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TestInspector(Base):
	"""The TestInspector class encapsulates a required testInspector node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TestInspector property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'testInspector'

	def __init__(self, parent):
		super(TestInspector, self).__init__(parent)

	@property
	def Statistic(self):
		"""An instance of the Statistic class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.testinspector.statistic.statistic.Statistic)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.testinspector.statistic.statistic import Statistic
		return Statistic(self)

	@property
	def EnableTestInspector(self):
		"""Enable/Disable Test Inspector

		Returns:
			bool
		"""
		return self._get_attribute('enableTestInspector')
	@EnableTestInspector.setter
	def EnableTestInspector(self, value):
		self._set_attribute('enableTestInspector', value)

	@property
	def PollingInterval(self):
		"""Polling Interval

		Returns:
			number
		"""
		return self._get_attribute('pollingInterval')
	@PollingInterval.setter
	def PollingInterval(self, value):
		self._set_attribute('pollingInterval', value)
