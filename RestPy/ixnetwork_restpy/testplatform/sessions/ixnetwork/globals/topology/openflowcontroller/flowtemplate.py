from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowTemplate(Base):
	"""The FlowTemplate class encapsulates a user managed flowTemplate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowTemplate property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowTemplate'

	def __init__(self, parent):
		super(FlowTemplate, self).__init__(parent)

	@property
	def MatchAction(self):
		"""An instance of the MatchAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.matchaction.MatchAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.matchaction import MatchAction
		return MatchAction(self)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def SavedInVersion(self):
		"""The cpf version of the session

		Returns:
			str
		"""
		return self._get_attribute('savedInVersion')
	@SavedInVersion.setter
	def SavedInVersion(self, value):
		self._set_attribute('savedInVersion', value)

	def add(self, Name=None, SavedInVersion=None):
		"""Adds a new flowTemplate node on the server and retrieves it in this instance.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SavedInVersion (str): The cpf version of the session

		Returns:
			self: This instance with all currently retrieved flowTemplate data using find and the newly added flowTemplate data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowTemplate data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, DescriptiveName=None, Name=None, SavedInVersion=None):
		"""Finds and retrieves flowTemplate data from the server.

		All named parameters support regex and can be used to selectively retrieve flowTemplate data from the server.
		By default the find method takes no parameters and will retrieve all flowTemplate data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SavedInVersion (str): The cpf version of the session

		Returns:
			self: This instance with matching flowTemplate data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowTemplate data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowTemplate data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
