from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MatchAction(Base):
	"""The MatchAction class encapsulates a user managed matchAction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MatchAction property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'matchAction'

	def __init__(self, parent):
		super(MatchAction, self).__init__(parent)

	@property
	def Instructions(self):
		"""An instance of the Instructions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instructions.Instructions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instructions import Instructions
		return Instructions(self)._select()

	@property
	def MatchCriteria(self):
		"""An instance of the MatchCriteria class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.matchcriteria.MatchCriteria)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.matchcriteria import MatchCriteria
		return MatchCriteria(self)._select()

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Description(self):
		"""Description of the field.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DisplayName(self):
		"""Display name used by GUI.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def IsEditable(self):
		"""Information on the requirement of the field.

		Returns:
			bool
		"""
		return self._get_attribute('isEditable')
	@IsEditable.setter
	def IsEditable(self, value):
		self._set_attribute('isEditable', value)

	@property
	def IsEnabled(self):
		"""Enables disables the field.

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def IsRequired(self):
		"""Information on the requirement of the field.

		Returns:
			bool
		"""
		return self._get_attribute('isRequired')
	@IsRequired.setter
	def IsRequired(self, value):
		self._set_attribute('isRequired', value)

	@property
	def Name(self):
		"""Name of packet field

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def add(self, Description=None, IsEditable=None, IsEnabled=None, IsRequired=None, Name=None):
		"""Adds a new matchAction node on the server and retrieves it in this instance.

		Args:
			Description (str): Description of the field.
			IsEditable (bool): Information on the requirement of the field.
			IsEnabled (bool): Enables disables the field.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of packet field

		Returns:
			self: This instance with all currently retrieved matchAction data using find and the newly added matchAction data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the matchAction data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, Description=None, DisplayName=None, IsEditable=None, IsEnabled=None, IsRequired=None, Name=None):
		"""Finds and retrieves matchAction data from the server.

		All named parameters support regex and can be used to selectively retrieve matchAction data from the server.
		By default the find method takes no parameters and will retrieve all matchAction data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			Description (str): Description of the field.
			DisplayName (str): Display name used by GUI.
			IsEditable (bool): Information on the requirement of the field.
			IsEnabled (bool): Enables disables the field.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of packet field

		Returns:
			self: This instance with matching matchAction data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of matchAction data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the matchAction data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
