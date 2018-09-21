from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GroupCapabilities(Base):
	"""The GroupCapabilities class encapsulates a required groupCapabilities node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupCapabilities property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'groupCapabilities'

	def __init__(self, parent):
		super(GroupCapabilities, self).__init__(parent)

	@property
	def Chaining(self):
		"""Chaining groups.

		Returns:
			bool
		"""
		return self._get_attribute('chaining')
	@Chaining.setter
	def Chaining(self, value):
		self._set_attribute('chaining', value)

	@property
	def ChainingChecks(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('chainingChecks')
	@ChainingChecks.setter
	def ChainingChecks(self, value):
		self._set_attribute('chainingChecks', value)

	@property
	def SelectLiveness(self):
		"""Liveness for select groups.

		Returns:
			bool
		"""
		return self._get_attribute('selectLiveness')
	@SelectLiveness.setter
	def SelectLiveness(self, value):
		self._set_attribute('selectLiveness', value)

	@property
	def SelectWeight(self):
		"""Weight for select groups.

		Returns:
			bool
		"""
		return self._get_attribute('selectWeight')
	@SelectWeight.setter
	def SelectWeight(self, value):
		self._set_attribute('selectWeight', value)
