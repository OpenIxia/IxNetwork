from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Value(Base):
	"""The Value class encapsulates a required value node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Value property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'value'

	def __init__(self, parent):
		super(Value, self).__init__(parent)

	@property
	def Object(self):
		"""An instance of the Object class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object.Object)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.object import Object
		return Object(self)

	@property
	def Name(self):
		"""The name of the object

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)
