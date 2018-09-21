from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LmLearnedInfo(Base):
	"""The LmLearnedInfo class encapsulates a system managed lmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'lmLearnedInfo'

	def __init__(self, parent):
		super(LmLearnedInfo, self).__init__(parent)

	@property
	def IncomingLabelOuterInner(self):
		"""This signifies the incoming label information.

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def LastLmResponseDutRx(self):
		"""This signifies the value of the DUT Rx counter in the last LM Response received.

		Returns:
			number
		"""
		return self._get_attribute('lastLmResponseDutRx')

	@property
	def LastLmResponseDutTx(self):
		"""This signifies the value of the DUT Tx counter in the last LM Response received.

		Returns:
			number
		"""
		return self._get_attribute('lastLmResponseDutTx')

	@property
	def LastLmResponseMyTx(self):
		"""This signifies the value of the My Tx counter in the last LM Response received.

		Returns:
			number
		"""
		return self._get_attribute('lastLmResponseMyTx')

	@property
	def LmQueriesSent(self):
		"""This signifies the number of LM queries sent.

		Returns:
			number
		"""
		return self._get_attribute('lmQueriesSent')

	@property
	def LmRemoteUsing64Bit(self):
		"""This specifies whether the remote end is using 64bit counter or not.

		Returns:
			bool
		"""
		return self._get_attribute('lmRemoteUsing64Bit')

	@property
	def LmResponsesReceived(self):
		"""This signifies the number of LM responses received.

		Returns:
			number
		"""
		return self._get_attribute('lmResponsesReceived')

	@property
	def OutgoingLabelOuterInner(self):
		"""This signifies the Outgoing Label information.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def Type(self):
		"""This signifies the Selection of this option to filter according to the following types LSP and PW.

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, IncomingLabelOuterInner=None, LastLmResponseDutRx=None, LastLmResponseDutTx=None, LastLmResponseMyTx=None, LmQueriesSent=None, LmRemoteUsing64Bit=None, LmResponsesReceived=None, OutgoingLabelOuterInner=None, Type=None):
		"""Finds and retrieves lmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve lmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all lmLearnedInfo data from the server.

		Args:
			IncomingLabelOuterInner (str): This signifies the incoming label information.
			LastLmResponseDutRx (number): This signifies the value of the DUT Rx counter in the last LM Response received.
			LastLmResponseDutTx (number): This signifies the value of the DUT Tx counter in the last LM Response received.
			LastLmResponseMyTx (number): This signifies the value of the My Tx counter in the last LM Response received.
			LmQueriesSent (number): This signifies the number of LM queries sent.
			LmRemoteUsing64Bit (bool): This specifies whether the remote end is using 64bit counter or not.
			LmResponsesReceived (number): This signifies the number of LM responses received.
			OutgoingLabelOuterInner (str): This signifies the Outgoing Label information.
			Type (str): This signifies the Selection of this option to filter according to the following types LSP and PW.

		Returns:
			self: This instance with matching lmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
