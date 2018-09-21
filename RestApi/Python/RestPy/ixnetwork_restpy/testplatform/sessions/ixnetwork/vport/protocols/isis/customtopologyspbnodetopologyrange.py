from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologySpbNodeTopologyRange(Base):
	"""The CustomTopologySpbNodeTopologyRange class encapsulates a user managed customTopologySpbNodeTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologySpbNodeTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologySpbNodeTopologyRange'

	def __init__(self, parent):
		super(CustomTopologySpbNodeTopologyRange, self).__init__(parent)

	@property
	def CustomTopologySpbNodeBaseVidRange(self):
		"""An instance of the CustomTopologySpbNodeBaseVidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopologyspbnodebasevidrange.CustomTopologySpbNodeBaseVidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopologyspbnodebasevidrange import CustomTopologySpbNodeBaseVidRange
		return CustomTopologySpbNodeBaseVidRange(self)

	@property
	def CistExternalRootCost(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('cistExternalRootCost')
	@CistExternalRootCost.setter
	def CistExternalRootCost(self, value):
		self._set_attribute('cistExternalRootCost', value)

	@property
	def CistRootIdentifier(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('cistRootIdentifier')
	@CistRootIdentifier.setter
	def CistRootIdentifier(self, value):
		self._set_attribute('cistRootIdentifier', value)

	@property
	def EnableVbit(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableVbit')
	@EnableVbit.setter
	def EnableVbit(self, value):
		self._set_attribute('enableVbit', value)

	@property
	def NoOfPorts(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('noOfPorts')
	@NoOfPorts.setter
	def NoOfPorts(self, value):
		self._set_attribute('noOfPorts', value)

	@property
	def PortIdentifier(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('portIdentifier')
	@PortIdentifier.setter
	def PortIdentifier(self, value):
		self._set_attribute('portIdentifier', value)

	def add(self, CistExternalRootCost=None, CistRootIdentifier=None, EnableVbit=None, NoOfPorts=None, PortIdentifier=None):
		"""Adds a new customTopologySpbNodeTopologyRange node on the server and retrieves it in this instance.

		Args:
			CistExternalRootCost (number): NOT DEFINED
			CistRootIdentifier (str): NOT DEFINED
			EnableVbit (bool): NOT DEFINED
			NoOfPorts (number): NOT DEFINED
			PortIdentifier (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologySpbNodeTopologyRange data using find and the newly added customTopologySpbNodeTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologySpbNodeTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CistExternalRootCost=None, CistRootIdentifier=None, EnableVbit=None, NoOfPorts=None, PortIdentifier=None):
		"""Finds and retrieves customTopologySpbNodeTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologySpbNodeTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologySpbNodeTopologyRange data from the server.

		Args:
			CistExternalRootCost (number): NOT DEFINED
			CistRootIdentifier (str): NOT DEFINED
			EnableVbit (bool): NOT DEFINED
			NoOfPorts (number): NOT DEFINED
			PortIdentifier (number): NOT DEFINED

		Returns:
			self: This instance with matching customTopologySpbNodeTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologySpbNodeTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologySpbNodeTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
