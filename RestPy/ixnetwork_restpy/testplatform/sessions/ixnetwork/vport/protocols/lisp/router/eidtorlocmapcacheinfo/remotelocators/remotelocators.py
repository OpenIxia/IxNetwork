from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RemoteLocators(Base):
	"""The RemoteLocators class encapsulates a system managed remoteLocators node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RemoteLocators property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'remoteLocators'

	def __init__(self, parent):
		super(RemoteLocators, self).__init__(parent)

	@property
	def MPriority(self):
		"""It gives details about the m priority (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('mPriority')

	@property
	def MWeight(self):
		"""It gives details about the m weight (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('mWeight')

	@property
	def Priority(self):
		"""It gives details about the priority (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('priority')

	@property
	def RemoteLocator(self):
		"""It gives details about the remote locators (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('remoteLocator')

	@property
	def RemoteLocatorAfi(self):
		"""It gives details about the remote locators Afi (Read-Only)

		Returns:
			str
		"""
		return self._get_attribute('remoteLocatorAfi')

	@property
	def RlocFlagL(self):
		"""It gives details about the rLoc Flag L (Read-Only)

		Returns:
			bool
		"""
		return self._get_attribute('rlocFlagL')

	@property
	def RlocFlagP(self):
		"""It gives details about the rLoc FlagP (Read-Only)

		Returns:
			bool
		"""
		return self._get_attribute('rlocFlagP')

	@property
	def RlocFlagR(self):
		"""If True, It gives details about the rLoc Flag R (Read-Only)

		Returns:
			bool
		"""
		return self._get_attribute('rlocFlagR')

	@property
	def Weight(self):
		"""It gives details about the weight (Read-Only)

		Returns:
			number
		"""
		return self._get_attribute('weight')

	def find(self, MPriority=None, MWeight=None, Priority=None, RemoteLocator=None, RemoteLocatorAfi=None, RlocFlagL=None, RlocFlagP=None, RlocFlagR=None, Weight=None):
		"""Finds and retrieves remoteLocators data from the server.

		All named parameters support regex and can be used to selectively retrieve remoteLocators data from the server.
		By default the find method takes no parameters and will retrieve all remoteLocators data from the server.

		Args:
			MPriority (number): It gives details about the m priority (Read-Only)
			MWeight (number): It gives details about the m weight (Read-Only)
			Priority (number): It gives details about the priority (Read-Only)
			RemoteLocator (str): It gives details about the remote locators (Read-Only)
			RemoteLocatorAfi (str): It gives details about the remote locators Afi (Read-Only)
			RlocFlagL (bool): It gives details about the rLoc Flag L (Read-Only)
			RlocFlagP (bool): It gives details about the rLoc FlagP (Read-Only)
			RlocFlagR (bool): If True, It gives details about the rLoc Flag R (Read-Only)
			Weight (number): It gives details about the weight (Read-Only)

		Returns:
			self: This instance with matching remoteLocators data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of remoteLocators data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the remoteLocators data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
