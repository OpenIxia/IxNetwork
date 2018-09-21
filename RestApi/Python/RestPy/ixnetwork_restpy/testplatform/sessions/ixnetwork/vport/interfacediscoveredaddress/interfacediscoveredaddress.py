from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterfaceDiscoveredAddress(Base):
	"""The InterfaceDiscoveredAddress class encapsulates a required interfaceDiscoveredAddress node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InterfaceDiscoveredAddress property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interfaceDiscoveredAddress'

	def __init__(self, parent):
		super(InterfaceDiscoveredAddress, self).__init__(parent)

	@property
	def Description(self):
		"""Shows description of the interface.

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def IpAddress(self):
		"""Shows IP address of the interface.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
