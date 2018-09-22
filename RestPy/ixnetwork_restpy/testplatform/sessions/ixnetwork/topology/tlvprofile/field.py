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
	def Restriction(self):
		"""An instance of the Restriction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.restriction.Restriction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.restriction import Restriction
		return Restriction(self)

	@property
	def Description(self):
		"""Description of the tlv

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def Encoding(self):
		"""Encoding of the tlv value, any change will result in the value being reset

		Returns:
			str(bool|decimal|fcid|float|hex|ipv4|ipv6|mac|string|varLenHex)
		"""
		return self._get_attribute('encoding')
	@Encoding.setter
	def Encoding(self, value):
		self._set_attribute('encoding', value)

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
	def IsEnabled(self):
		"""Enables/disables this field

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def Name(self):
		"""Name of the tlv

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def Size(self):
		"""Size of the tlv value in bits/bytes based on sizeType, any change will result in the value being reset

		Returns:
			number
		"""
		return self._get_attribute('size')
	@Size.setter
	def Size(self, value):
		self._set_attribute('size', value)

	@property
	def SizeType(self):
		"""Size type of the tlv value, any change will result in the value being reset

		Returns:
			str(bit|byte)
		"""
		return self._get_attribute('sizeType')
	@SizeType.setter
	def SizeType(self, value):
		self._set_attribute('sizeType', value)

	@property
	def Value(self):
		"""Value represented as a multivalue object

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('value')

	def find(self, Description=None, Encoding=None, IsEditable=None, IsEnabled=None, Name=None, Size=None, SizeType=None):
		"""Finds and retrieves field data from the server.

		All named parameters support regex and can be used to selectively retrieve field data from the server.
		By default the find method takes no parameters and will retrieve all field data from the server.

		Args:
			Description (str): Description of the tlv
			Encoding (str(bool|decimal|fcid|float|hex|ipv4|ipv6|mac|string|varLenHex)): Encoding of the tlv value, any change will result in the value being reset
			IsEditable (bool): Indicates whether this is editable or not
			IsEnabled (bool): Enables/disables this field
			Name (str): Name of the tlv
			Size (number): Size of the tlv value in bits/bytes based on sizeType, any change will result in the value being reset
			SizeType (str(bit|byte)): Size type of the tlv value, any change will result in the value being reset

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
