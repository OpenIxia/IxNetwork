from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInfo(Base):
	"""The LearnedInfo class encapsulates a required learnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedInfo'

	def __init__(self, parent):
		super(LearnedInfo, self).__init__(parent)

	@property
	def DesignatedCost(self):
		"""Root Path Cost. The administrative cost for the shortest path from this bridge to the Root bridge. A 4-byte unsigned integer. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('designatedCost')

	@property
	def DesignatedMac(self):
		"""(Read-only) The 6-byte MAC address of the designated bridge on the LAN segment.

		Returns:
			str
		"""
		return self._get_attribute('designatedMac')

	@property
	def DesignatedPortId(self):
		"""(Read-only) The port ID of the designated bridge's designated port on the LAN segment.

		Returns:
			number
		"""
		return self._get_attribute('designatedPortId')

	@property
	def DesignatedPriority(self):
		"""(Read-only) The priority of the designated bridge on the LAN segment.

		Returns:
			number
		"""
		return self._get_attribute('designatedPriority')

	@property
	def InterfaceDesc(self):
		"""(Read-only) The descriptive identifier of the protocol interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceDesc')

	@property
	def InterfaceRole(self):
		"""(Read-only) The role of the Interface. One of the following options: Disabled, Root, Designated, Alternate, or Backup.

		Returns:
			str
		"""
		return self._get_attribute('interfaceRole')

	@property
	def InterfaceState(self):
		"""Read-only) The state of the interface. One of the following options: Discarding, learning, or forwarding.

		Returns:
			str
		"""
		return self._get_attribute('interfaceState')

	@property
	def RootMac(self):
		"""(Read-only) The 6-byte MAC address of the root bridge.

		Returns:
			str
		"""
		return self._get_attribute('rootMac')

	@property
	def RootPriority(self):
		"""(Read-only) The priority of the root bridge.

		Returns:
			number
		"""
		return self._get_attribute('rootPriority')
