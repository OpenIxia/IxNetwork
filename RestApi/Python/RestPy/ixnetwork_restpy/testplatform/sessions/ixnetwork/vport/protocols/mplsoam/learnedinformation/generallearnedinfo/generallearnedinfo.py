from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GeneralLearnedInfo(Base):
	"""The GeneralLearnedInfo class encapsulates a system managed generalLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GeneralLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'generalLearnedInfo'

	def __init__(self, parent):
		super(GeneralLearnedInfo, self).__init__(parent)

	@property
	def AverageRtt(self):
		"""This signifies the average Round Trip Time.

		Returns:
			str
		"""
		return self._get_attribute('averageRtt')

	@property
	def BfdSessionMyState(self):
		"""This signifies the window provides read-only information about the state of BFD interface on the specified emulated router.

		Returns:
			str
		"""
		return self._get_attribute('bfdSessionMyState')

	@property
	def BfdSessionPeerState(self):
		"""This signifies the state of the far side of the BFD session, either active or not.

		Returns:
			str
		"""
		return self._get_attribute('bfdSessionPeerState')

	@property
	def CcInUse(self):
		"""This signifies the Continuity Check in use. The values are RA, PW-ACH, or TTL Exp.

		Returns:
			str
		"""
		return self._get_attribute('ccInUse')

	@property
	def CvInUse(self):
		"""This signifies the Connectivity Verification in use. The values are LSP Ping, BFD IP/UDP, or LSP Ping.

		Returns:
			str
		"""
		return self._get_attribute('cvInUse')

	@property
	def Fec(self):
		"""This signifies the FEC component.

		Returns:
			str
		"""
		return self._get_attribute('fec')

	@property
	def IncomingLabelStack(self):
		"""This signifies the BGP sends the assigned labels information to this MPLS OAM module which is used for validation of FEC stack received in an echo request.

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelStack')

	@property
	def IncomingLspLabel(self):
		"""This signifies the incoming LSP label value.

		Returns:
			str
		"""
		return self._get_attribute('incomingLspLabel')

	@property
	def IncomingPwLabel(self):
		"""This signifies the incoming PW label value.

		Returns:
			str
		"""
		return self._get_attribute('incomingPwLabel')

	@property
	def LspPingReachability(self):
		"""This signifies the specification of whether the queried LSP Ping could be reached or not.

		Returns:
			str
		"""
		return self._get_attribute('lspPingReachability')

	@property
	def MaxRtt(self):
		"""This signifies the specification of the maximum Round Trip Time.

		Returns:
			str
		"""
		return self._get_attribute('maxRtt')

	@property
	def MinRtt(self):
		"""This signifies the specification of the minimum Round Trip Time.

		Returns:
			str
		"""
		return self._get_attribute('minRtt')

	@property
	def MyDiscriminator(self):
		"""This signifies the discriminator for the session on this interface.

		Returns:
			number
		"""
		return self._get_attribute('myDiscriminator')

	@property
	def MyIpAddress(self):
		"""This signifies the IP address for this interface.

		Returns:
			str
		"""
		return self._get_attribute('myIpAddress')

	@property
	def OutgoingLabelStack(self):
		"""This signifies the BGP sends the assigned labels information to this MPLS OAM module which is used for validation of FEC outgoing Label stack that is received in an echo request.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelStack')

	@property
	def OutgoingLspLabel(self):
		"""This signifies the outgoing LSP label value.

		Returns:
			str
		"""
		return self._get_attribute('outgoingLspLabel')

	@property
	def OutgoingPwLabel(self):
		"""This signifies the outgoing PW label value.

		Returns:
			str
		"""
		return self._get_attribute('outgoingPwLabel')

	@property
	def PeerDiscriminator(self):
		"""This signifies the discriminator for the far side of the session.

		Returns:
			number
		"""
		return self._get_attribute('peerDiscriminator')

	@property
	def PeerIpAddress(self):
		"""This signifies the learnt IP address for the session.

		Returns:
			str
		"""
		return self._get_attribute('peerIpAddress')

	@property
	def PingAttempts(self):
		"""This signifies the specification of the number of ping attempts.

		Returns:
			number
		"""
		return self._get_attribute('pingAttempts')

	@property
	def PingFailures(self):
		"""This signifies the specification of the number of ping failures.

		Returns:
			number
		"""
		return self._get_attribute('pingFailures')

	@property
	def PingReplyTx(self):
		"""This signifies the specification of the number of ping reply transmitted at regular intervals.

		Returns:
			number
		"""
		return self._get_attribute('pingReplyTx')

	@property
	def PingRequestRx(self):
		"""This signifies the specification of the number of ping request received at regular intervals.

		Returns:
			number
		"""
		return self._get_attribute('pingRequestRx')

	@property
	def PingSuccess(self):
		"""This signifies the specification of the rate of ping success.

		Returns:
			number
		"""
		return self._get_attribute('pingSuccess')

	@property
	def ReceivedMinRxInterval(self):
		"""This signifies the minimum receive interval, in milliseconds, for the far side of the session.

		Returns:
			number
		"""
		return self._get_attribute('receivedMinRxInterval')

	@property
	def ReceivedMultiplier(self):
		"""This signifies the number of received negotiated transmit intervals when multiplied by this value, provides the detection time for the interface.

		Returns:
			number
		"""
		return self._get_attribute('receivedMultiplier')

	@property
	def ReceivedPeerFlags(self):
		"""This signifies the number of peer generated flags received.

		Returns:
			str
		"""
		return self._get_attribute('receivedPeerFlags')

	@property
	def ReceivedTxInterval(self):
		"""This signifies the minimum transmit interval, in milliseconds, for the far side of the session.

		Returns:
			number
		"""
		return self._get_attribute('receivedTxInterval')

	@property
	def ReturnCode(self):
		"""This signifies the return code value.

		Returns:
			str
		"""
		return self._get_attribute('returnCode')

	@property
	def ReturnSubcode(self):
		"""This signifies the return subcode value.

		Returns:
			number
		"""
		return self._get_attribute('returnSubcode')

	@property
	def SignalingProtocol(self):
		"""This signifies the options for signaling protocol are BGP, LDP, RSVP.

		Returns:
			str
		"""
		return self._get_attribute('signalingProtocol')

	@property
	def TunnelEndpointType(self):
		"""This signifies the tunnel endpoint type options include Ingress, Egress, Bi-directional.

		Returns:
			str
		"""
		return self._get_attribute('tunnelEndpointType')

	@property
	def TunnelType(self):
		"""This signifies the tunnel type options include LSP and PW.

		Returns:
			str
		"""
		return self._get_attribute('tunnelType')

	def find(self, AverageRtt=None, BfdSessionMyState=None, BfdSessionPeerState=None, CcInUse=None, CvInUse=None, Fec=None, IncomingLabelStack=None, IncomingLspLabel=None, IncomingPwLabel=None, LspPingReachability=None, MaxRtt=None, MinRtt=None, MyDiscriminator=None, MyIpAddress=None, OutgoingLabelStack=None, OutgoingLspLabel=None, OutgoingPwLabel=None, PeerDiscriminator=None, PeerIpAddress=None, PingAttempts=None, PingFailures=None, PingReplyTx=None, PingRequestRx=None, PingSuccess=None, ReceivedMinRxInterval=None, ReceivedMultiplier=None, ReceivedPeerFlags=None, ReceivedTxInterval=None, ReturnCode=None, ReturnSubcode=None, SignalingProtocol=None, TunnelEndpointType=None, TunnelType=None):
		"""Finds and retrieves generalLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve generalLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all generalLearnedInfo data from the server.

		Args:
			AverageRtt (str): This signifies the average Round Trip Time.
			BfdSessionMyState (str): This signifies the window provides read-only information about the state of BFD interface on the specified emulated router.
			BfdSessionPeerState (str): This signifies the state of the far side of the BFD session, either active or not.
			CcInUse (str): This signifies the Continuity Check in use. The values are RA, PW-ACH, or TTL Exp.
			CvInUse (str): This signifies the Connectivity Verification in use. The values are LSP Ping, BFD IP/UDP, or LSP Ping.
			Fec (str): This signifies the FEC component.
			IncomingLabelStack (str): This signifies the BGP sends the assigned labels information to this MPLS OAM module which is used for validation of FEC stack received in an echo request.
			IncomingLspLabel (str): This signifies the incoming LSP label value.
			IncomingPwLabel (str): This signifies the incoming PW label value.
			LspPingReachability (str): This signifies the specification of whether the queried LSP Ping could be reached or not.
			MaxRtt (str): This signifies the specification of the maximum Round Trip Time.
			MinRtt (str): This signifies the specification of the minimum Round Trip Time.
			MyDiscriminator (number): This signifies the discriminator for the session on this interface.
			MyIpAddress (str): This signifies the IP address for this interface.
			OutgoingLabelStack (str): This signifies the BGP sends the assigned labels information to this MPLS OAM module which is used for validation of FEC outgoing Label stack that is received in an echo request.
			OutgoingLspLabel (str): This signifies the outgoing LSP label value.
			OutgoingPwLabel (str): This signifies the outgoing PW label value.
			PeerDiscriminator (number): This signifies the discriminator for the far side of the session.
			PeerIpAddress (str): This signifies the learnt IP address for the session.
			PingAttempts (number): This signifies the specification of the number of ping attempts.
			PingFailures (number): This signifies the specification of the number of ping failures.
			PingReplyTx (number): This signifies the specification of the number of ping reply transmitted at regular intervals.
			PingRequestRx (number): This signifies the specification of the number of ping request received at regular intervals.
			PingSuccess (number): This signifies the specification of the rate of ping success.
			ReceivedMinRxInterval (number): This signifies the minimum receive interval, in milliseconds, for the far side of the session.
			ReceivedMultiplier (number): This signifies the number of received negotiated transmit intervals when multiplied by this value, provides the detection time for the interface.
			ReceivedPeerFlags (str): This signifies the number of peer generated flags received.
			ReceivedTxInterval (number): This signifies the minimum transmit interval, in milliseconds, for the far side of the session.
			ReturnCode (str): This signifies the return code value.
			ReturnSubcode (number): This signifies the return subcode value.
			SignalingProtocol (str): This signifies the options for signaling protocol are BGP, LDP, RSVP.
			TunnelEndpointType (str): This signifies the tunnel endpoint type options include Ingress, Egress, Bi-directional.
			TunnelType (str): This signifies the tunnel type options include LSP and PW.

		Returns:
			self: This instance with matching generalLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of generalLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the generalLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		This signifies the record added for trigger settings.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=generalLearnedInfo)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
