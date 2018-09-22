from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrillOamPing(Base):
	"""The TrillOamPing class encapsulates a system managed trillOamPing node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrillOamPing property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'trillOamPing'

	def __init__(self, parent):
		super(TrillOamPing, self).__init__(parent)

	@property
	def DestinationNickname(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('destinationNickname')

	@property
	def IncomingPort(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('incomingPort')

	@property
	def NextHop(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('nextHop')

	@property
	def OutgoingPort(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('outgoingPort')

	@property
	def OutgoingPortMtu(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('outgoingPortMtu')

	@property
	def PreviousHop(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('previousHop')

	@property
	def ResponseTime(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('responseTime')

	@property
	def SequenceNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def SourceNickname(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sourceNickname')

	@property
	def Status(self):
		"""NOT DEFINED

		Returns:
			str(Failure|Success)
		"""
		return self._get_attribute('status')

	def find(self, DestinationNickname=None, IncomingPort=None, NextHop=None, OutgoingPort=None, OutgoingPortMtu=None, PreviousHop=None, ResponseTime=None, SequenceNumber=None, SourceNickname=None, Status=None):
		"""Finds and retrieves trillOamPing data from the server.

		All named parameters support regex and can be used to selectively retrieve trillOamPing data from the server.
		By default the find method takes no parameters and will retrieve all trillOamPing data from the server.

		Args:
			DestinationNickname (number): NOT DEFINED
			IncomingPort (number): NOT DEFINED
			NextHop (number): NOT DEFINED
			OutgoingPort (number): NOT DEFINED
			OutgoingPortMtu (number): NOT DEFINED
			PreviousHop (number): NOT DEFINED
			ResponseTime (number): NOT DEFINED
			SequenceNumber (number): NOT DEFINED
			SourceNickname (number): NOT DEFINED
			Status (str(Failure|Success)): NOT DEFINED

		Returns:
			self: This instance with matching trillOamPing data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trillOamPing data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trillOamPing data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
