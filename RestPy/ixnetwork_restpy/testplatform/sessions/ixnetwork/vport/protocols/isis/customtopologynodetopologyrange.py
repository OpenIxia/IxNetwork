from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologyNodeTopologyRange(Base):
	"""The CustomTopologyNodeTopologyRange class encapsulates a user managed customTopologyNodeTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologyNodeTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologyNodeTopologyRange'

	def __init__(self, parent):
		super(CustomTopologyNodeTopologyRange, self).__init__(parent)

	@property
	def CustomTopologyInterestedVlanRange(self):
		"""An instance of the CustomTopologyInterestedVlanRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopologyinterestedvlanrange.CustomTopologyInterestedVlanRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.customtopologyinterestedvlanrange import CustomTopologyInterestedVlanRange
		return CustomTopologyInterestedVlanRange(self)

	@property
	def NicknameCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('nicknameCount')
	@NicknameCount.setter
	def NicknameCount(self, value):
		self._set_attribute('nicknameCount', value)

	@property
	def NodeNicknameIncrement(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('nodeNicknameIncrement')
	@NodeNicknameIncrement.setter
	def NodeNicknameIncrement(self, value):
		self._set_attribute('nodeNicknameIncrement', value)

	@property
	def NumberOftreesToCompute(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('numberOftreesToCompute')
	@NumberOftreesToCompute.setter
	def NumberOftreesToCompute(self, value):
		self._set_attribute('numberOftreesToCompute', value)

	@property
	def StartNickname(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('startNickname')
	@StartNickname.setter
	def StartNickname(self, value):
		self._set_attribute('startNickname', value)

	def add(self, NicknameCount=None, NodeNicknameIncrement=None, NumberOftreesToCompute=None, StartNickname=None):
		"""Adds a new customTopologyNodeTopologyRange node on the server and retrieves it in this instance.

		Args:
			NicknameCount (number): NOT DEFINED
			NodeNicknameIncrement (number): NOT DEFINED
			NumberOftreesToCompute (number): NOT DEFINED
			StartNickname (number): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologyNodeTopologyRange data using find and the newly added customTopologyNodeTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologyNodeTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, NicknameCount=None, NodeNicknameIncrement=None, NumberOftreesToCompute=None, StartNickname=None):
		"""Finds and retrieves customTopologyNodeTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologyNodeTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologyNodeTopologyRange data from the server.

		Args:
			NicknameCount (number): NOT DEFINED
			NodeNicknameIncrement (number): NOT DEFINED
			NumberOftreesToCompute (number): NOT DEFINED
			StartNickname (number): NOT DEFINED

		Returns:
			self: This instance with matching customTopologyNodeTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologyNodeTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologyNodeTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
