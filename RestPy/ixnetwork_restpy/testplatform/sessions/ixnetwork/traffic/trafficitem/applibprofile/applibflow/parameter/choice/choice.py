from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Choice(Base):
	"""The Choice class encapsulates a system managed choice node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Choice property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'choice'

	def __init__(self, parent):
		super(Choice, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter choice default value.

		Returns:
			str
		"""
		return self._get_attribute('default')

	@property
	def SupportedValues(self):
		"""(Read only) Parameter supported choice values.

		Returns:
			list(str)
		"""
		return self._get_attribute('supportedValues')

	@property
	def Value(self):
		"""Parameter choice selected value.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def find(self, Default=None, SupportedValues=None, Value=None):
		"""Finds and retrieves choice data from the server.

		All named parameters support regex and can be used to selectively retrieve choice data from the server.
		By default the find method takes no parameters and will retrieve all choice data from the server.

		Args:
			Default (str): (Read only) Parameter choice default value.
			SupportedValues (list(str)): (Read only) Parameter supported choice values.
			Value (str): Parameter choice selected value.

		Returns:
			self: This instance with matching choice data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of choice data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the choice data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
