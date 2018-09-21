from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class UserLsaGroup(Base):
	"""The UserLsaGroup class encapsulates a user managed userLsaGroup node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the UserLsaGroup property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'userLsaGroup'

	def __init__(self, parent):
		super(UserLsaGroup, self).__init__(parent)

	@property
	def UserLsa(self):
		"""An instance of the UserLsa class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.userlsa.UserLsa)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ospf.userlsa import UserLsa
		return UserLsa(self)

	@property
	def AreaId(self):
		"""The area ID for the LSA group. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('areaId')
	@AreaId.setter
	def AreaId(self, value):
		self._set_attribute('areaId', value)

	@property
	def Description(self):
		"""A commentary description for the user LSA group.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def Enabled(self):
		"""Enables the use of this router in the simulated OSPF network.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	def add(self, AreaId=None, Description=None, Enabled=None):
		"""Adds a new userLsaGroup node on the server and retrieves it in this instance.

		Args:
			AreaId (number): The area ID for the LSA group. (default = 0)
			Description (str): A commentary description for the user LSA group.
			Enabled (bool): Enables the use of this router in the simulated OSPF network.

		Returns:
			self: This instance with all currently retrieved userLsaGroup data using find and the newly added userLsaGroup data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the userLsaGroup data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AreaId=None, Description=None, Enabled=None):
		"""Finds and retrieves userLsaGroup data from the server.

		All named parameters support regex and can be used to selectively retrieve userLsaGroup data from the server.
		By default the find method takes no parameters and will retrieve all userLsaGroup data from the server.

		Args:
			AreaId (number): The area ID for the LSA group. (default = 0)
			Description (str): A commentary description for the user LSA group.
			Enabled (bool): Enables the use of this router in the simulated OSPF network.

		Returns:
			self: This instance with matching userLsaGroup data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of userLsaGroup data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the userLsaGroup data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
