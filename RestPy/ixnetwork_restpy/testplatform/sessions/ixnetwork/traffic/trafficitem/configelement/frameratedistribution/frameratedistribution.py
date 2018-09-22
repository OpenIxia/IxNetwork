from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FrameRateDistribution(Base):
	"""The FrameRateDistribution class encapsulates a required frameRateDistribution node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FrameRateDistribution property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'frameRateDistribution'

	def __init__(self, parent):
		super(FrameRateDistribution, self).__init__(parent)

	@property
	def PortDistribution(self):
		"""At the port level, apply the target configuration transmission rate for each encapsulation.

		Returns:
			str(applyRateToAll|splitRateEvenly)
		"""
		return self._get_attribute('portDistribution')
	@PortDistribution.setter
	def PortDistribution(self, value):
		self._set_attribute('portDistribution', value)

	@property
	def StreamDistribution(self):
		"""At the flow group level, apply the target rate of each port.

		Returns:
			str(applyRateToAll|splitRateEvenly)
		"""
		return self._get_attribute('streamDistribution')
	@StreamDistribution.setter
	def StreamDistribution(self, value):
		self._set_attribute('streamDistribution', value)
