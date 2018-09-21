from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrillMacUnicast(Base):
	"""The TrillMacUnicast class encapsulates a system managed trillMacUnicast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrillMacUnicast property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'trillMacUnicast'

	def __init__(self, parent):
		super(TrillMacUnicast, self).__init__(parent)

	@property
	def Age(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('age')

	@property
	def HostName(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('hostName')

	@property
	def LspId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('lspId')

	@property
	def SequenceNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def UnicastMacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('unicastMacAddress')

	@property
	def VlanId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	def find(self, Age=None, HostName=None, LspId=None, SequenceNumber=None, UnicastMacAddress=None, VlanId=None):
		"""Finds and retrieves trillMacUnicast data from the server.

		All named parameters support regex and can be used to selectively retrieve trillMacUnicast data from the server.
		By default the find method takes no parameters and will retrieve all trillMacUnicast data from the server.

		Args:
			Age (number): NOT DEFINED
			HostName (str): NOT DEFINED
			LspId (str): NOT DEFINED
			SequenceNumber (number): NOT DEFINED
			UnicastMacAddress (str): NOT DEFINED
			VlanId (number): NOT DEFINED

		Returns:
			self: This instance with matching trillMacUnicast data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of trillMacUnicast data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the trillMacUnicast data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
