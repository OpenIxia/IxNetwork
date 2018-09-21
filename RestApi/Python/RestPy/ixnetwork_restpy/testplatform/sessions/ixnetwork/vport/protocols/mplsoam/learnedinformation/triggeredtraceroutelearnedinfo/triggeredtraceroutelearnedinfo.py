from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TriggeredTracerouteLearnedInfo(Base):
	"""The TriggeredTracerouteLearnedInfo class encapsulates a system managed triggeredTracerouteLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TriggeredTracerouteLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'triggeredTracerouteLearnedInfo'

	def __init__(self, parent):
		super(TriggeredTracerouteLearnedInfo, self).__init__(parent)

	@property
	def Hops(self):
		"""An instance of the Hops class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.triggeredtraceroutelearnedinfo.hops.hops.Hops)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mplsoam.learnedinformation.triggeredtraceroutelearnedinfo.hops.hops import Hops
		return Hops(self)

	@property
	def Fec(self):
		"""This signifies the FEC component.

		Returns:
			str
		"""
		return self._get_attribute('fec')

	@property
	def Hops(self):
		"""This signifies the number of LSP hops.

		Returns:
			str
		"""
		return self._get_attribute('hops')

	@property
	def IncomingLabelStack(self):
		"""This signifies the information is sent to the MPLS-OAM module which is used for validation of FEC stack received in an echo request. This is the assigned labels stack by the Ixia router and bfd/ping messages are expected to be received from DUT with this stack values. The outer value corresponds to the PSN Tunnel Label and the inner value corresponds to the PW label.

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelStack')

	@property
	def NumberOfReplyingHops(self):
		"""This signifies the total number of replying LSP hops.

		Returns:
			number
		"""
		return self._get_attribute('numberOfReplyingHops')

	@property
	def OutgoingLabelStack(self):
		"""This signifies the information is sent to the MPLS-OAM module which is used for validation of FEC outgoing Label stack that is received in an echo request.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelStack')

	@property
	def Reachability(self):
		"""This signifies whether the LSP is reachable with a proper return code or not. If the return code is not set to 3, in the received reply message or if there is no reply message that is received, then the field will show unreachable.

		Returns:
			str
		"""
		return self._get_attribute('reachability')

	@property
	def SenderHandle(self):
		"""This signifies the sender handle details.

		Returns:
			number
		"""
		return self._get_attribute('senderHandle')

	def find(self, Fec=None, Hops=None, IncomingLabelStack=None, NumberOfReplyingHops=None, OutgoingLabelStack=None, Reachability=None, SenderHandle=None):
		"""Finds and retrieves triggeredTracerouteLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve triggeredTracerouteLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all triggeredTracerouteLearnedInfo data from the server.

		Args:
			Fec (str): This signifies the FEC component.
			Hops (str): This signifies the number of LSP hops.
			IncomingLabelStack (str): This signifies the information is sent to the MPLS-OAM module which is used for validation of FEC stack received in an echo request. This is the assigned labels stack by the Ixia router and bfd/ping messages are expected to be received from DUT with this stack values. The outer value corresponds to the PSN Tunnel Label and the inner value corresponds to the PW label.
			NumberOfReplyingHops (number): This signifies the total number of replying LSP hops.
			OutgoingLabelStack (str): This signifies the information is sent to the MPLS-OAM module which is used for validation of FEC outgoing Label stack that is received in an echo request.
			Reachability (str): This signifies whether the LSP is reachable with a proper return code or not. If the return code is not set to 3, in the received reply message or if there is no reply message that is received, then the field will show unreachable.
			SenderHandle (number): This signifies the sender handle details.

		Returns:
			self: This instance with matching triggeredTracerouteLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of triggeredTracerouteLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the triggeredTracerouteLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
