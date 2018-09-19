from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Type(Base):
	"""The Type class encapsulates a required type node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Type property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'type'

	def __init__(self, parent):
		super(Type, self).__init__(parent)

	@property
	def Object(self):
		"""An instance of the Object class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.object.Object)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.object import Object
		return Object(self)

	@property
	def IsEditable(self):
		"""Indicates whether this is editable or not

		Returns:
			bool
		"""
		return self._get_attribute('isEditable')
	@IsEditable.setter
	def IsEditable(self, value):
		self._set_attribute('isEditable', value)

	@property
	def IsRequired(self):
		"""Indicates whether this is required or not

		Returns:
			bool
		"""
		return self._get_attribute('isRequired')
	@IsRequired.setter
	def IsRequired(self, value):
		self._set_attribute('isRequired', value)

	@property
	def Name(self):
		"""Name of the node

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)
