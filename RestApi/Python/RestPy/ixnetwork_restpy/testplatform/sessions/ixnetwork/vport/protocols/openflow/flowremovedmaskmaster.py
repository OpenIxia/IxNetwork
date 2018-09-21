from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowRemovedMaskMaster(Base):
	"""The FlowRemovedMaskMaster class encapsulates a required flowRemovedMaskMaster node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowRemovedMaskMaster property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flowRemovedMaskMaster'

	def __init__(self, parent):
		super(FlowRemovedMaskMaster, self).__init__(parent)

	@property
	def Delete(self):
		"""This indicates that flow entry is evicted by a delete Flow Mod message.

		Returns:
			bool
		"""
		return self._get_attribute('delete')
	@Delete.setter
	def Delete(self, value):
		self._set_attribute('delete', value)

	@property
	def GroupDelete(self):
		"""This indicates that the group is removed.

		Returns:
			bool
		"""
		return self._get_attribute('groupDelete')
	@GroupDelete.setter
	def GroupDelete(self, value):
		self._set_attribute('groupDelete', value)

	@property
	def HardTimeout(self):
		"""This indicates that Flow idle time exceeded hard timeout.

		Returns:
			bool
		"""
		return self._get_attribute('hardTimeout')
	@HardTimeout.setter
	def HardTimeout(self, value):
		self._set_attribute('hardTimeout', value)

	@property
	def IdleTimeout(self):
		"""This indicates that Flow idle time exceeded idle timeout.

		Returns:
			bool
		"""
		return self._get_attribute('idleTimeout')
	@IdleTimeout.setter
	def IdleTimeout(self, value):
		self._set_attribute('idleTimeout', value)
