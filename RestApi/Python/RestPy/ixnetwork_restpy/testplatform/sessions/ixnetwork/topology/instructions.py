from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Instructions(Base):
	"""The Instructions class encapsulates a required instructions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Instructions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'instructions'

	def __init__(self, parent):
		super(Instructions, self).__init__(parent)

	@property
	def Instruction(self):
		"""An instance of the Instruction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction.Instruction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.instruction import Instruction
		return Instruction(self)

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

	def AddInstruction(self, Arg2):
		"""Executes the addInstruction operation on the server.

		Adds Instruction item in profile.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddInstruction', payload=locals(), response_object=None)
