from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LabelSpace(Base):
	"""The LabelSpace class encapsulates a required labelSpace node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LabelSpace property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'labelSpace'

	def __init__(self, parent):
		super(LabelSpace, self).__init__(parent)

	@property
	def End(self):
		"""The last label value available in the label space (range).

		Returns:
			number
		"""
		return self._get_attribute('end')
	@End.setter
	def End(self, value):
		self._set_attribute('end', value)

	@property
	def LabelId(self):
		"""The identifier for the label space.

		Returns:
			number
		"""
		return self._get_attribute('labelId')
	@LabelId.setter
	def LabelId(self, value):
		self._set_attribute('labelId', value)

	@property
	def Mode(self):
		"""Sets the Label mode.

		Returns:
			str(fixedLabel|incrementLabel)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def Start(self):
		"""The first label value available in the label space (range). The default is 16.

		Returns:
			number
		"""
		return self._get_attribute('start')
	@Start.setter
	def Start(self, value):
		self._set_attribute('start', value)

	@property
	def Step(self):
		"""The value to add for creating each additional label value.

		Returns:
			number
		"""
		return self._get_attribute('step')
	@Step.setter
	def Step(self, value):
		self._set_attribute('step', value)
