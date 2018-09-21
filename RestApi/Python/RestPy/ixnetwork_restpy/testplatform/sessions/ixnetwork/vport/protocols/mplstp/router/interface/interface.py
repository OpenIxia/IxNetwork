from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Interface(Base):
	"""The Interface class encapsulates a user managed interface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def LspPwRange(self):
		"""An instance of the LspPwRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.interface.lsppwrange.lsppwrange.LspPwRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplstp.router.interface.lsppwrange.lsppwrange import LspPwRange
		return LspPwRange(self)

	@property
	def DutMacAddress(self):
		"""This signifies the MAC address of the DUT.

		Returns:
			str
		"""
		return self._get_attribute('dutMacAddress')
	@DutMacAddress.setter
	def DutMacAddress(self, value):
		self._set_attribute('dutMacAddress', value)

	@property
	def Enabled(self):
		"""This signifies the enablement of the use of this interface for the simulated router.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Interfaces(self):
		"""This signifies the Interface that has been assigned for this range.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	def add(self, DutMacAddress=None, Enabled=None, Interfaces=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			DutMacAddress (str): This signifies the MAC address of the DUT.
			Enabled (bool): This signifies the enablement of the use of this interface for the simulated router.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This signifies the Interface that has been assigned for this range.

		Returns:
			self: This instance with all currently retrieved interface data using find and the newly added interface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DutMacAddress=None, Enabled=None, Interfaces=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			DutMacAddress (str): This signifies the MAC address of the DUT.
			Enabled (bool): This signifies the enablement of the use of this interface for the simulated router.
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): This signifies the Interface that has been assigned for this range.

		Returns:
			self: This instance with matching interface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
