from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IxVmCard(Base):
	"""The IxVmCard class encapsulates a user managed ixVmCard node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IxVmCard property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ixVmCard'

	def __init__(self, parent):
		super(IxVmCard, self).__init__(parent)

	@property
	def IxVmPort(self):
		"""An instance of the IxVmPort class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.ixvmcard.ixvmport.ixvmport.IxVmPort)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.ixvmcard.ixvmport.ixvmport import IxVmPort
		return IxVmPort(self)

	@property
	def CardId(self):
		"""Represents slot on the chassis

		Returns:
			str
		"""
		return self._get_attribute('cardId')
	@CardId.setter
	def CardId(self, value):
		self._set_attribute('cardId', value)

	@property
	def CardName(self):
		"""Represents the card name

		Returns:
			str
		"""
		return self._get_attribute('cardName')
	@CardName.setter
	def CardName(self, value):
		self._set_attribute('cardName', value)

	@property
	def CardState(self):
		"""Represents the card state

		Returns:
			str(cardDisconnected|cardIpInUse|cardOK|cardRemoved|cardUnableToConnect|cardUnitialized|cardUnknownError|cardUnsynchronized|cardVersionMismatch)
		"""
		return self._get_attribute('cardState')

	@property
	def KeepAliveTimeout(self):
		"""Represents the keepalive timeout

		Returns:
			number
		"""
		return self._get_attribute('keepAliveTimeout')
	@KeepAliveTimeout.setter
	def KeepAliveTimeout(self, value):
		self._set_attribute('keepAliveTimeout', value)

	@property
	def ManagementIp(self):
		"""Represents the management Ip

		Returns:
			str
		"""
		return self._get_attribute('managementIp')
	@ManagementIp.setter
	def ManagementIp(self, value):
		self._set_attribute('managementIp', value)

	def add(self, CardId=None, CardName=None, KeepAliveTimeout=None, ManagementIp=None):
		"""Adds a new ixVmCard node on the server and retrieves it in this instance.

		Args:
			CardId (str): Represents slot on the chassis
			CardName (str): Represents the card name
			KeepAliveTimeout (number): Represents the keepalive timeout
			ManagementIp (str): Represents the management Ip

		Returns:
			self: This instance with all currently retrieved ixVmCard data using find and the newly added ixVmCard data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ixVmCard data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CardId=None, CardName=None, CardState=None, KeepAliveTimeout=None, ManagementIp=None):
		"""Finds and retrieves ixVmCard data from the server.

		All named parameters support regex and can be used to selectively retrieve ixVmCard data from the server.
		By default the find method takes no parameters and will retrieve all ixVmCard data from the server.

		Args:
			CardId (str): Represents slot on the chassis
			CardName (str): Represents the card name
			CardState (str(cardDisconnected|cardIpInUse|cardOK|cardRemoved|cardUnableToConnect|cardUnitialized|cardUnknownError|cardUnsynchronized|cardVersionMismatch)): Represents the card state
			KeepAliveTimeout (number): Represents the keepalive timeout
			ManagementIp (str): Represents the management Ip

		Returns:
			self: This instance with matching ixVmCard data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ixVmCard data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ixVmCard data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
