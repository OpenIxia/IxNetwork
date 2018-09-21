from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OrganizationSpecificEventTlv(Base):
	"""The OrganizationSpecificEventTlv class encapsulates a required organizationSpecificEventTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OrganizationSpecificEventTlv property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'organizationSpecificEventTlv'

	def __init__(self, parent):
		super(OrganizationSpecificEventTlv, self).__init__(parent)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Oui(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('oui')
	@Oui.setter
	def Oui(self, value):
		self._set_attribute('oui', value)

	@property
	def Value(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)
