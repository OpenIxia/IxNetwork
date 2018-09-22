from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AppErrors(Base):
	"""The AppErrors class encapsulates a system managed appErrors node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AppErrors property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'appErrors'

	def __init__(self, parent):
		super(AppErrors, self).__init__(parent)

	@property
	def Error(self):
		"""An instance of the Error class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.error.Error)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.error import Error
		return Error(self)

	@property
	def ErrorCount(self):
		"""Total number of errors

		Returns:
			number
		"""
		return self._get_attribute('errorCount')

	@property
	def LastModified(self):
		"""Time of latest logged error or warning

		Returns:
			str
		"""
		return self._get_attribute('lastModified')

	@property
	def WarningCount(self):
		"""Total number of warnings

		Returns:
			number
		"""
		return self._get_attribute('warningCount')

	def find(self, ErrorCount=None, LastModified=None, WarningCount=None):
		"""Finds and retrieves appErrors data from the server.

		All named parameters support regex and can be used to selectively retrieve appErrors data from the server.
		By default the find method takes no parameters and will retrieve all appErrors data from the server.

		Args:
			ErrorCount (number): Total number of errors
			LastModified (str): Time of latest logged error or warning
			WarningCount (number): Total number of warnings

		Returns:
			self: This instance with matching appErrors data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of appErrors data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the appErrors data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
