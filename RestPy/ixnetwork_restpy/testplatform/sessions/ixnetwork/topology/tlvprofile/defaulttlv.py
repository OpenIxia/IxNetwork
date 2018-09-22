from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DefaultTlv(Base):
	"""The DefaultTlv class encapsulates a system managed defaultTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DefaultTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'defaultTlv'

	def __init__(self, parent):
		super(DefaultTlv, self).__init__(parent)

	@property
	def Value(self):
		"""An instance of the Value class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.value.Value)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.value import Value
		return Value(self)._select()

	@property
	def AvailableIncludeInMessages(self):
		"""A list of available messages which are used in the includeInMessages attribute

		Returns:
			list(str)
		"""
		return self._get_attribute('availableIncludeInMessages')

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
	def EnablePerSession(self):
		"""Enable TLV per session

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePerSession')

	@property
	def IncludeInMessages(self):
		"""Include the TLV in these protocol messages

		Returns:
			list(str)
		"""
		return self._get_attribute('includeInMessages')
	@IncludeInMessages.setter
	def IncludeInMessages(self, value):
		self._set_attribute('includeInMessages', value)

	@property
	def IsEnabled(self):
		"""Enables/disables this tlv

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

	def find(self, AvailableIncludeInMessages=None, Description=None, IncludeInMessages=None, IsEnabled=None, Name=None):
		"""Finds and retrieves defaultTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve defaultTlv data from the server.
		By default the find method takes no parameters and will retrieve all defaultTlv data from the server.

		Args:
			AvailableIncludeInMessages (list(str)): A list of available messages which are used in the includeInMessages attribute
			Description (str): Description of the tlv
			IncludeInMessages (list(str)): Include the TLV in these protocol messages
			IsEnabled (bool): Enables/disables this tlv
			Name (str): Name of the tlv

		Returns:
			self: This instance with matching defaultTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of defaultTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the defaultTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
