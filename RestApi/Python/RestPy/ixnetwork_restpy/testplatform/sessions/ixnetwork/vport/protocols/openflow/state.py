from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class State(Base):
	"""The State class encapsulates a required state node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the State property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'state'

	def __init__(self, parent):
		super(State, self).__init__(parent)

	@property
	def LinkDown(self):
		"""Indicates that, no physical link is present.

		Returns:
			bool
		"""
		return self._get_attribute('linkDown')
	@LinkDown.setter
	def LinkDown(self, value):
		self._set_attribute('linkDown', value)

	@property
	def StpBlock(self):
		"""Indicates that the port is not part of spanning tree.

		Returns:
			bool
		"""
		return self._get_attribute('stpBlock')
	@StpBlock.setter
	def StpBlock(self, value):
		self._set_attribute('stpBlock', value)

	@property
	def StpForward(self):
		"""Indicates that the port is learning and relaying frames.

		Returns:
			bool
		"""
		return self._get_attribute('stpForward')
	@StpForward.setter
	def StpForward(self, value):
		self._set_attribute('stpForward', value)

	@property
	def StpLearn(self):
		"""Indicates that the port is learning but not relaying frames.

		Returns:
			bool
		"""
		return self._get_attribute('stpLearn')
	@StpLearn.setter
	def StpLearn(self, value):
		self._set_attribute('stpLearn', value)

	@property
	def StpListen(self):
		"""Indicates that the port is not learning or relaying frames.

		Returns:
			bool
		"""
		return self._get_attribute('stpListen')
	@StpListen.setter
	def StpListen(self, value):
		self._set_attribute('stpListen', value)
