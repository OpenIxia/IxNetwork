from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LnsAuthCredentials(Base):
	"""The LnsAuthCredentials class encapsulates a required lnsAuthCredentials node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LnsAuthCredentials property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'lnsAuthCredentials'

	def __init__(self, parent):
		super(LnsAuthCredentials, self).__init__(parent)

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
	def LacHostName(self):
		"""LAC Hostname used for tunnel authentication.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lacHostName')

	@property
	def LacSecret(self):
		"""Secret value used for tunnel authentication.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lacSecret')

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
