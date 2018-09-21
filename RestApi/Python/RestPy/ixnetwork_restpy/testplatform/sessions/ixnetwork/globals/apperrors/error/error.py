from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Error(Base):
	"""The Error class encapsulates a system managed error node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Error property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'error'

	def __init__(self, parent):
		super(Error, self).__init__(parent)

	@property
	def Instance(self):
		"""An instance of the Instance class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.instance.instance.Instance)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.instance.instance import Instance
		return Instance(self)

	@property
	def Description(self):
		"""The description of the error

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def ErrorCode(self):
		"""The error code of the error

		Returns:
			number
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorLevel(self):
		"""The error level of the error

		Returns:
			str(kAnalysis|kCount|kError|kMessage|kWarning)
		"""
		return self._get_attribute('errorLevel')

	@property
	def InstanceCount(self):
		"""The number of instances of the error

		Returns:
			number
		"""
		return self._get_attribute('instanceCount')

	@property
	def LastModified(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastModified')

	@property
	def Name(self):
		"""The name of the error

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Provider(self):
		"""The error provider of the error

		Returns:
			str
		"""
		return self._get_attribute('provider')

	@property
	def SourceColumns(self):
		"""If the error content originated from an xml meta file, these are the source column names if any for this error.

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceColumns')

	@property
	def SourceColumnsDisplayName(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceColumnsDisplayName')

	def find(self, Description=None, ErrorCode=None, ErrorLevel=None, InstanceCount=None, LastModified=None, Name=None, Provider=None, SourceColumns=None, SourceColumnsDisplayName=None):
		"""Finds and retrieves error data from the server.

		All named parameters support regex and can be used to selectively retrieve error data from the server.
		By default the find method takes no parameters and will retrieve all error data from the server.

		Args:
			Description (str): The description of the error
			ErrorCode (number): The error code of the error
			ErrorLevel (str(kAnalysis|kCount|kError|kMessage|kWarning)): The error level of the error
			InstanceCount (number): The number of instances of the error
			LastModified (str): 
			Name (str): The name of the error
			Provider (str): The error provider of the error
			SourceColumns (list(str)): If the error content originated from an xml meta file, these are the source column names if any for this error.
			SourceColumnsDisplayName (list(str)): 

		Returns:
			self: This instance with matching error data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of error data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the error data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
