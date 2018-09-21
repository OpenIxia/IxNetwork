from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PacketInMaskMaster(Base):
	"""The PacketInMaskMaster class encapsulates a required packetInMaskMaster node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PacketInMaskMaster property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'packetInMaskMaster'

	def __init__(self, parent):
		super(PacketInMaskMaster, self).__init__(parent)

	@property
	def Action(self):
		"""Action explicitly output to controller.

		Returns:
			bool
		"""
		return self._get_attribute('action')
	@Action.setter
	def Action(self, value):
		self._set_attribute('action', value)

	@property
	def InvalidTtl(self):
		"""This indicates that a packet with an invalid IP TTL or MPLS TTL was rejected by the OpenFlow pipeline and passed to the controller.

		Returns:
			bool
		"""
		return self._get_attribute('invalidTtl')
	@InvalidTtl.setter
	def InvalidTtl(self, value):
		self._set_attribute('invalidTtl', value)

	@property
	def NoMatch(self):
		"""This indicates that a packet with no matching flow (table-miss flow entry) is passed to the controller.

		Returns:
			bool
		"""
		return self._get_attribute('noMatch')
	@NoMatch.setter
	def NoMatch(self, value):
		self._set_attribute('noMatch', value)
