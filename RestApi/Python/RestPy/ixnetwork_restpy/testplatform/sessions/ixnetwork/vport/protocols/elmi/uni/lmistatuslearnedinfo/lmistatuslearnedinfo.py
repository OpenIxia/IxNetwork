from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LmiStatusLearnedInfo(Base):
	"""The LmiStatusLearnedInfo class encapsulates a system managed lmiStatusLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LmiStatusLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'lmiStatusLearnedInfo'

	def __init__(self, parent):
		super(LmiStatusLearnedInfo, self).__init__(parent)

	@property
	def DataInstance(self):
		"""This four-octet field indicates the Data Instance value to be sent in transmitted packet. It will be configurable only if Override Data Instance is enabled. By default it is grayed out with default value 0x0 for UNI-C and 0x1 for UNI-N. Max 4 octet max value, Min 0/1. Change of value in this field takes effect when protocol is running.

		Returns:
			number
		"""
		return self._get_attribute('dataInstance')

	@property
	def DuplicatedIe(self):
		"""Type of out of sequence IE received : count of out of sequence IE received.

		Returns:
			str
		"""
		return self._get_attribute('duplicatedIe')

	@property
	def InvalidEvcReferenceId(self):
		"""Invalid EVC reference Id.

		Returns:
			str
		"""
		return self._get_attribute('invalidEvcReferenceId')

	@property
	def InvalidMandatoryIe(self):
		"""Type of invalid mandatory IE : count of invalid mandatory IE.

		Returns:
			str
		"""
		return self._get_attribute('invalidMandatoryIe')

	@property
	def InvalidMsgType(self):
		"""It signfies the invalid message type.

		Returns:
			str
		"""
		return self._get_attribute('invalidMsgType')

	@property
	def InvalidNonMandatoryIe(self):
		"""Type of invalid non mandatory IE : count of invalid non mandatory IE

		Returns:
			str
		"""
		return self._get_attribute('invalidNonMandatoryIe')

	@property
	def InvalidProtocolVersion(self):
		"""Invalid protocol version in received ELMI message.

		Returns:
			str
		"""
		return self._get_attribute('invalidProtocolVersion')

	@property
	def LmiStatus(self):
		"""It signifies the LMI status value.

		Returns:
			str
		"""
		return self._get_attribute('lmiStatus')

	@property
	def MandatoryIeMissing(self):
		"""Type of mandatory IE missing : count of mandatory IE missing.

		Returns:
			str
		"""
		return self._get_attribute('mandatoryIeMissing')

	@property
	def OutOfSequenceIe(self):
		"""Type of out of sequence IE received : count of out of sequence IE recieved

		Returns:
			str
		"""
		return self._get_attribute('outOfSequenceIe')

	@property
	def ProtocolVersion(self):
		"""This one-octet field indicates the version supported by the sending

		Returns:
			number
		"""
		return self._get_attribute('protocolVersion')

	@property
	def ReceiveSequenceNumber(self):
		"""The value of Receive Sequence Number in received ELMI message.

		Returns:
			number
		"""
		return self._get_attribute('receiveSequenceNumber')

	@property
	def SendSequenceNumber(self):
		"""The value of Send Sequence Number in received ELMI message.

		Returns:
			number
		"""
		return self._get_attribute('sendSequenceNumber')

	@property
	def ShortMsgCounter(self):
		"""It signifies the short message counter value.

		Returns:
			number
		"""
		return self._get_attribute('shortMsgCounter')

	@property
	def UnexpectedIe(self):
		"""Type of unexpected IE : count of unexpected IE.

		Returns:
			str
		"""
		return self._get_attribute('unexpectedIe')

	@property
	def UnrecognizedIe(self):
		"""Type of unrecognized IE : count of unrecognized IE.

		Returns:
			str
		"""
		return self._get_attribute('unrecognizedIe')

	def find(self, DataInstance=None, DuplicatedIe=None, InvalidEvcReferenceId=None, InvalidMandatoryIe=None, InvalidMsgType=None, InvalidNonMandatoryIe=None, InvalidProtocolVersion=None, LmiStatus=None, MandatoryIeMissing=None, OutOfSequenceIe=None, ProtocolVersion=None, ReceiveSequenceNumber=None, SendSequenceNumber=None, ShortMsgCounter=None, UnexpectedIe=None, UnrecognizedIe=None):
		"""Finds and retrieves lmiStatusLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve lmiStatusLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all lmiStatusLearnedInfo data from the server.

		Args:
			DataInstance (number): This four-octet field indicates the Data Instance value to be sent in transmitted packet. It will be configurable only if Override Data Instance is enabled. By default it is grayed out with default value 0x0 for UNI-C and 0x1 for UNI-N. Max 4 octet max value, Min 0/1. Change of value in this field takes effect when protocol is running.
			DuplicatedIe (str): Type of out of sequence IE received : count of out of sequence IE received.
			InvalidEvcReferenceId (str): Invalid EVC reference Id.
			InvalidMandatoryIe (str): Type of invalid mandatory IE : count of invalid mandatory IE.
			InvalidMsgType (str): It signfies the invalid message type.
			InvalidNonMandatoryIe (str): Type of invalid non mandatory IE : count of invalid non mandatory IE
			InvalidProtocolVersion (str): Invalid protocol version in received ELMI message.
			LmiStatus (str): It signifies the LMI status value.
			MandatoryIeMissing (str): Type of mandatory IE missing : count of mandatory IE missing.
			OutOfSequenceIe (str): Type of out of sequence IE received : count of out of sequence IE recieved
			ProtocolVersion (number): This one-octet field indicates the version supported by the sending
			ReceiveSequenceNumber (number): The value of Receive Sequence Number in received ELMI message.
			SendSequenceNumber (number): The value of Send Sequence Number in received ELMI message.
			ShortMsgCounter (number): It signifies the short message counter value.
			UnexpectedIe (str): Type of unexpected IE : count of unexpected IE.
			UnrecognizedIe (str): Type of unrecognized IE : count of unrecognized IE.

		Returns:
			self: This instance with matching lmiStatusLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lmiStatusLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lmiStatusLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
