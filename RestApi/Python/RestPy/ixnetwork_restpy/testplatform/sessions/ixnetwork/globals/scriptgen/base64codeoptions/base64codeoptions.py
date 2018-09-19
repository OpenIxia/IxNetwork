from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Base64CodeOptions(Base):
	"""The Base64CodeOptions class encapsulates a required base64CodeOptions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Base64CodeOptions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'base64CodeOptions'

	def __init__(self, parent):
		super(Base64CodeOptions, self).__init__(parent)

	@property
	def IncludeSampleCode(self):
		"""Flag to include sample code

		Returns:
			bool
		"""
		return self._get_attribute('includeSampleCode')
	@IncludeSampleCode.setter
	def IncludeSampleCode(self, value):
		self._set_attribute('includeSampleCode', value)

	@property
	def SampleObjectReferences(self):
		"""A list of object references used to generate sample code

		Returns:
			list(str[None])
		"""
		return self._get_attribute('sampleObjectReferences')
	@SampleObjectReferences.setter
	def SampleObjectReferences(self, value):
		self._set_attribute('sampleObjectReferences', value)
