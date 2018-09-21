from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInterface(Base):
	"""The LearnedInterface class encapsulates a user managed learnedInterface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInterface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'learnedInterface'

	def __init__(self, parent):
		super(LearnedInterface, self).__init__(parent)

	@property
	def DesignatedMac(self):
		"""(Read-only) The 6-byte MAC Address of the advertised designated MSTP bridge on the LAN segment.

		Returns:
			str
		"""
		return self._get_attribute('designatedMac')

	@property
	def DesignatedPortId(self):
		"""(Read-only) The port ID of the advertised eesignated MSTP bridge's port on the LAN segment.

		Returns:
			number
		"""
		return self._get_attribute('designatedPortId')

	@property
	def DesignatedPriority(self):
		"""(Read-only) The priority of the advertised designated MSTP bridge on the LAN segment.

		Returns:
			number
		"""
		return self._get_attribute('designatedPriority')

	@property
	def InterfaceDesc(self):
		"""(Read-only) The descriptive identifier of this advertised protocol interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceDesc')

	@property
	def InterfaceRole(self):
		"""(Read-only) The role of the advertised interface. One of the following options: Disabled, Root, Designated, Alternate, or Backup.

		Returns:
			str
		"""
		return self._get_attribute('interfaceRole')

	@property
	def InterfaceState(self):
		"""(Read-only) The state of the advertised interface. One of the following options: Discarding (discarding MAC), Learning (MAC frame learning), or Forwarding (forwarding MAC frames).

		Returns:
			str
		"""
		return self._get_attribute('interfaceState')

	def add(self):
		"""Adds a new learnedInterface node on the server and retrieves it in this instance.

		Returns:
			self: This instance with all currently retrieved learnedInterface data using find and the newly added learnedInterface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the learnedInterface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DesignatedMac=None, DesignatedPortId=None, DesignatedPriority=None, InterfaceDesc=None, InterfaceRole=None, InterfaceState=None):
		"""Finds and retrieves learnedInterface data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedInterface data from the server.
		By default the find method takes no parameters and will retrieve all learnedInterface data from the server.

		Args:
			DesignatedMac (str): (Read-only) The 6-byte MAC Address of the advertised designated MSTP bridge on the LAN segment.
			DesignatedPortId (number): (Read-only) The port ID of the advertised eesignated MSTP bridge's port on the LAN segment.
			DesignatedPriority (number): (Read-only) The priority of the advertised designated MSTP bridge on the LAN segment.
			InterfaceDesc (str): (Read-only) The descriptive identifier of this advertised protocol interface.
			InterfaceRole (str): (Read-only) The role of the advertised interface. One of the following options: Disabled, Root, Designated, Alternate, or Backup.
			InterfaceState (str): (Read-only) The state of the advertised interface. One of the following options: Discarding (discarding MAC), Learning (MAC frame learning), or Forwarding (forwarding MAC frames).

		Returns:
			self: This instance with matching learnedInterface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedInterface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedInterface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
