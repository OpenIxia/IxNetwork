from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchHostRangeHopsLearnedInfo(Base):
	"""The SwitchHostRangeHopsLearnedInfo class encapsulates a system managed switchHostRangeHopsLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchHostRangeHopsLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchHostRangeHopsLearnedInfo'

	def __init__(self, parent):
		super(SwitchHostRangeHopsLearnedInfo, self).__init__(parent)

	@property
	def Action(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('action')

	@property
	def DestinationHostMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationHostMac')

	@property
	def InputPort(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('inputPort')

	@property
	def InputTimeInMs(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('inputTimeInMs')

	@property
	def OutputPort(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def OutputTimeInMs(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('outputTimeInMs')

	@property
	def SourceHostMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('sourceHostMac')

	@property
	def SwitchDataPathId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('switchDataPathId')

	@property
	def SwitchIp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('switchIp')

	def find(self, Action=None, DestinationHostMac=None, InputPort=None, InputTimeInMs=None, OutputPort=None, OutputTimeInMs=None, SourceHostMac=None, SwitchDataPathId=None, SwitchIp=None):
		"""Finds and retrieves switchHostRangeHopsLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchHostRangeHopsLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchHostRangeHopsLearnedInfo data from the server.

		Args:
			Action (str): NOT DEFINED
			DestinationHostMac (str): NOT DEFINED
			InputPort (number): NOT DEFINED
			InputTimeInMs (number): NOT DEFINED
			OutputPort (number): NOT DEFINED
			OutputTimeInMs (number): NOT DEFINED
			SourceHostMac (str): NOT DEFINED
			SwitchDataPathId (number): NOT DEFINED
			SwitchIp (str): NOT DEFINED

		Returns:
			self: This instance with matching switchHostRangeHopsLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchHostRangeHopsLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchHostRangeHopsLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
