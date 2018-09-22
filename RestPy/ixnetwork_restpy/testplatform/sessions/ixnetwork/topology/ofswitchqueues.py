from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfSwitchQueues(Base):
	"""The OfSwitchQueues class encapsulates a required ofSwitchQueues node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfSwitchQueues property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ofSwitchQueues'

	def __init__(self, parent):
		super(OfSwitchQueues, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def MaxRate(self):
		"""Specify the maximum data rate guaranteed.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxRate')

	@property
	def MinRate(self):
		"""Specify the minimum data rate guaranteed.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minRate')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def ParentPort(self):
		"""Parent port index.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('parentPort')

	@property
	def QueueId(self):
		"""Specify the queue identifier for the packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('queueId')

	@property
	def QueueProperty(self):
		"""Configure the queue property from the options

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('queueProperty')

	@property
	def SwitchIndex(self):
		"""Index of the OF Switch.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('switchIndex')
