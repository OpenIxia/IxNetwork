from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""The Field class encapsulates a system managed field node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Field property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

	@property
	def __id__(self):
		"""An alphanumeric string that defines the internal field ID.

		Returns:
			str
		"""
		return self._get_attribute('__id__')

	@property
	def DisplayName(self):
		"""It is used to get the name of the particular field as available in the protocol template.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def FieldTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldTypeId')

	@property
	def Length(self):
		"""It is used to get the length of the field in bits.

		Returns:
			number
		"""
		return self._get_attribute('length')

	@property
	def Trackable(self):
		"""The trackable fields.

		Returns:
			bool
		"""
		return self._get_attribute('trackable')

	def find(self, __id__=None, DisplayName=None, FieldTypeId=None, Length=None, Trackable=None):
		"""Finds and retrieves field data from the server.

		All named parameters support regex and can be used to selectively retrieve field data from the server.
		By default the find method takes no parameters and will retrieve all field data from the server.

		Args:
			__id__ (str): An alphanumeric string that defines the internal field ID.
			DisplayName (str): It is used to get the name of the particular field as available in the protocol template.
			FieldTypeId (str): 
			Length (number): It is used to get the length of the field in bits.
			Trackable (bool): The trackable fields.

		Returns:
			self: This instance with matching field data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of field data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the field data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
