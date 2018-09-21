from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ReceivedLabel(Base):
	"""The ReceivedLabel class encapsulates a system managed receivedLabel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ReceivedLabel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'receivedLabel'

	def __init__(self, parent):
		super(ReceivedLabel, self).__init__(parent)

	@property
	def CurrentLspOrSubLspUpTime(self):
		"""Indicates the re-optimization time per LSP/Sub LSP in port level.

		Returns:
			number
		"""
		return self._get_attribute('currentLspOrSubLspUpTime')

	@property
	def DestinationIp(self):
		"""The destination router's IP address.

		Returns:
			str
		"""
		return self._get_attribute('destinationIp')

	@property
	def Label(self):
		"""Label value received from the DUT for the LSP/Tunnel ID, in response to a Label Request from the Ixia-emulated router.

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LeafIp(self):
		"""IP of the leaf range.

		Returns:
			str
		"""
		return self._get_attribute('leafIp')

	@property
	def LspId(self):
		"""A unique LSP tunnel ID.

		Returns:
			number
		"""
		return self._get_attribute('lspId')

	@property
	def LspOrSubLspSetupTime(self):
		"""Indicates the set up time per LSP/Sub LSP in port level.

		Returns:
			number
		"""
		return self._get_attribute('lspOrSubLspSetupTime')

	@property
	def ReservationState(self):
		"""The reservation state after there is a graceful restart. This is not applicable for Ingress and will be equal to None.

		Returns:
			str
		"""
		return self._get_attribute('reservationState')

	@property
	def SourceIp(self):
		"""The source router's IP address.

		Returns:
			str
		"""
		return self._get_attribute('sourceIp')

	@property
	def TunnelId(self):
		"""A unique tunnel ID.

		Returns:
			number
		"""
		return self._get_attribute('tunnelId')

	@property
	def Type(self):
		"""Tunnel type, one of P2P or P2MP.

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, CurrentLspOrSubLspUpTime=None, DestinationIp=None, Label=None, LeafIp=None, LspId=None, LspOrSubLspSetupTime=None, ReservationState=None, SourceIp=None, TunnelId=None, Type=None):
		"""Finds and retrieves receivedLabel data from the server.

		All named parameters support regex and can be used to selectively retrieve receivedLabel data from the server.
		By default the find method takes no parameters and will retrieve all receivedLabel data from the server.

		Args:
			CurrentLspOrSubLspUpTime (number): Indicates the re-optimization time per LSP/Sub LSP in port level.
			DestinationIp (str): The destination router's IP address.
			Label (number): Label value received from the DUT for the LSP/Tunnel ID, in response to a Label Request from the Ixia-emulated router.
			LeafIp (str): IP of the leaf range.
			LspId (number): A unique LSP tunnel ID.
			LspOrSubLspSetupTime (number): Indicates the set up time per LSP/Sub LSP in port level.
			ReservationState (str): The reservation state after there is a graceful restart. This is not applicable for Ingress and will be equal to None.
			SourceIp (str): The source router's IP address.
			TunnelId (number): A unique tunnel ID.
			Type (str): Tunnel type, one of P2P or P2MP.

		Returns:
			self: This instance with matching receivedLabel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of receivedLabel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the receivedLabel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
