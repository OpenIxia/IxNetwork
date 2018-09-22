from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interfaces(Base):
	"""The Interfaces class encapsulates a required interfaces node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interfaces property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interfaces'

	def __init__(self, parent):
		super(Interfaces, self).__init__(parent)

	@property
	def ArpOnLinkup(self):
		"""If true, automatically enables ARP and PING when the interfaces is associated with a port.

		Returns:
			bool
		"""
		return self._get_attribute('arpOnLinkup')
	@ArpOnLinkup.setter
	def ArpOnLinkup(self, value):
		self._set_attribute('arpOnLinkup', value)

	@property
	def NsOnLinkup(self):
		"""If true, automatically enables NS when the interfaces is associated with a port.

		Returns:
			bool
		"""
		return self._get_attribute('nsOnLinkup')
	@NsOnLinkup.setter
	def NsOnLinkup(self, value):
		self._set_attribute('nsOnLinkup', value)

	@property
	def SendSingleArpPerGateway(self):
		"""If true, only a single ARP is sent via each defined gateway address.

		Returns:
			bool
		"""
		return self._get_attribute('sendSingleArpPerGateway')
	@SendSingleArpPerGateway.setter
	def SendSingleArpPerGateway(self, value):
		self._set_attribute('sendSingleArpPerGateway', value)

	@property
	def SendSingleNsPerGateway(self):
		"""If true, only a single NS is sent via each defined gateway address.

		Returns:
			bool
		"""
		return self._get_attribute('sendSingleNsPerGateway')
	@SendSingleNsPerGateway.setter
	def SendSingleNsPerGateway(self, value):
		self._set_attribute('sendSingleNsPerGateway', value)
