from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EgressRxCondition(Base):
	"""The EgressRxCondition class encapsulates a required egressRxCondition node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EgressRxCondition property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'egressRxCondition'

	def __init__(self, parent):
		super(EgressRxCondition, self).__init__(parent)

	@property
	def Operator(self):
		"""The logical operation to be performed.

		Returns:
			str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

	@property
	def Values(self):
		"""Value to be matched for the condition.

		Returns:
			list(number)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)
