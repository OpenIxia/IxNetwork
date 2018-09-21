from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchFlow131TriggerAttributes(Base):
	"""The SwitchFlow131TriggerAttributes class encapsulates a required switchFlow131TriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchFlow131TriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'switchFlow131TriggerAttributes'

	def __init__(self, parent):
		super(SwitchFlow131TriggerAttributes, self).__init__(parent)

	@property
	def OutGroup(self):
		"""This describes the out group value. It requires matching entries to include this as an output group.

		Returns:
			number
		"""
		return self._get_attribute('outGroup')
	@OutGroup.setter
	def OutGroup(self, value):
		self._set_attribute('outGroup', value)

	@property
	def OutGroupInputMode(self):
		"""This describes the input mode of the out group value.

		Returns:
			str(allGroups|anyGroup|outGroupCustom)
		"""
		return self._get_attribute('outGroupInputMode')
	@OutGroupInputMode.setter
	def OutGroupInputMode(self, value):
		self._set_attribute('outGroupInputMode', value)

	@property
	def OutPort(self):
		"""This describes the out port value. It requires matching entries to include this as an output port.

		Returns:
			number
		"""
		return self._get_attribute('outPort')
	@OutPort.setter
	def OutPort(self, value):
		self._set_attribute('outPort', value)

	@property
	def OutPortInputMode(self):
		"""This describes the input mode of the out port value.

		Returns:
			str(ofppInPort|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal|ofppAny|outPortCustom)
		"""
		return self._get_attribute('outPortInputMode')
	@OutPortInputMode.setter
	def OutPortInputMode(self, value):
		self._set_attribute('outPortInputMode', value)

	@property
	def TableId(self):
		"""This describes the table identifier. It indicates the next table in the packet processing pipeline.

		Returns:
			number
		"""
		return self._get_attribute('tableId')
	@TableId.setter
	def TableId(self, value):
		self._set_attribute('tableId', value)

	@property
	def TableIdInputMode(self):
		"""This describes the input mode of the Table Identifier.

		Returns:
			str(allTables|emergency|custom)
		"""
		return self._get_attribute('tableIdInputMode')
	@TableIdInputMode.setter
	def TableIdInputMode(self, value):
		self._set_attribute('tableIdInputMode', value)
