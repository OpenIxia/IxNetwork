from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PingLearnedInfo(Base):
	"""The PingLearnedInfo class encapsulates a system managed pingLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PingLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pingLearnedInfo'

	def __init__(self, parent):
		super(PingLearnedInfo, self).__init__(parent)

	@property
	def ErrorTlvType(self):
		"""This signifies Error TLV if it is received in lsp ping echo reply message.

		Returns:
			number
		"""
		return self._get_attribute('errorTlvType')

	@property
	def IncomingLabelOuterInner(self):
		"""This signifies the incoming label information.

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def InterfaceLabelStackTlvInterface(self):
		"""This Signifies the inclusion of the Interface Id within Interface and Label Stack TLV in received lsp ping echo reply message.

		Returns:
			number
		"""
		return self._get_attribute('interfaceLabelStackTlvInterface')

	@property
	def InterfaceLabelStackTlvIpAddress(self):
		"""This Signifies the inclusion of the IP Address within Interface and Label Stack TLV in received lsp ping echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvIpAddress')

	@property
	def InterfaceLabelStackTlvLabels(self):
		"""This signifies the label stack in Interface and Label Stack TLV received in lsp ping echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('interfaceLabelStackTlvLabels')

	@property
	def OutgoingLabelOuterInner(self):
		"""This signifies the Outgoing Label information.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def Reachability(self):
		"""This specifies whether the queried MEP could be reached or not, Yes or No.

		Returns:
			bool
		"""
		return self._get_attribute('reachability')

	@property
	def ReturnCode(self):
		"""This signifies the value of the return code in the Echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('returnCode')

	@property
	def ReturnSubcode(self):
		"""This signifies the value of the return sub-code in the Echo reply message.

		Returns:
			number
		"""
		return self._get_attribute('returnSubcode')

	@property
	def ReversePathVerificationCode(self):
		"""This Signifies the reverse path verification code received in the lsp ping echo reply message.

		Returns:
			str
		"""
		return self._get_attribute('reversePathVerificationCode')

	@property
	def Rtt(self):
		"""This signifies the Round Trip Time.

		Returns:
			str
		"""
		return self._get_attribute('rtt')

	@property
	def SenderHandle(self):
		"""This signifies the sender handle information.

		Returns:
			number
		"""
		return self._get_attribute('senderHandle')

	@property
	def SequenceNumber(self):
		"""This signifies the sequence number for the ping learned information.

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')

	@property
	def Type(self):
		"""This signifies the type of the learned info.

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, ErrorTlvType=None, IncomingLabelOuterInner=None, InterfaceLabelStackTlvInterface=None, InterfaceLabelStackTlvIpAddress=None, InterfaceLabelStackTlvLabels=None, OutgoingLabelOuterInner=None, Reachability=None, ReturnCode=None, ReturnSubcode=None, ReversePathVerificationCode=None, Rtt=None, SenderHandle=None, SequenceNumber=None, Type=None):
		"""Finds and retrieves pingLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve pingLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all pingLearnedInfo data from the server.

		Args:
			ErrorTlvType (number): This signifies Error TLV if it is received in lsp ping echo reply message.
			IncomingLabelOuterInner (str): This signifies the incoming label information.
			InterfaceLabelStackTlvInterface (number): This Signifies the inclusion of the Interface Id within Interface and Label Stack TLV in received lsp ping echo reply message.
			InterfaceLabelStackTlvIpAddress (str): This Signifies the inclusion of the IP Address within Interface and Label Stack TLV in received lsp ping echo reply message.
			InterfaceLabelStackTlvLabels (str): This signifies the label stack in Interface and Label Stack TLV received in lsp ping echo reply message.
			OutgoingLabelOuterInner (str): This signifies the Outgoing Label information.
			Reachability (bool): This specifies whether the queried MEP could be reached or not, Yes or No.
			ReturnCode (str): This signifies the value of the return code in the Echo reply message.
			ReturnSubcode (number): This signifies the value of the return sub-code in the Echo reply message.
			ReversePathVerificationCode (str): This Signifies the reverse path verification code received in the lsp ping echo reply message.
			Rtt (str): This signifies the Round Trip Time.
			SenderHandle (number): This signifies the sender handle information.
			SequenceNumber (number): This signifies the sequence number for the ping learned information.
			Type (str): This signifies the type of the learned info.

		Returns:
			self: This instance with matching pingLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pingLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pingLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
