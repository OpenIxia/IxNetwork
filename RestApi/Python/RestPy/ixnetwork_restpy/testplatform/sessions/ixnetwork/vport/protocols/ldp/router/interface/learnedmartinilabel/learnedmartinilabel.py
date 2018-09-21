from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedMartiniLabel(Base):
	"""The LearnedMartiniLabel class encapsulates a system managed learnedMartiniLabel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedMartiniLabel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedMartiniLabel'

	def __init__(self, parent):
		super(LearnedMartiniLabel, self).__init__(parent)

	@property
	def CBit(self):
		"""If enabled, sets the C-Bit (flag). It is the highest order bit in the VC Type field. If the bit is set, it indicates the presence of a control word on this VC.

		Returns:
			bool
		"""
		return self._get_attribute('cBit')

	@property
	def Cas(self):
		"""Indicates the CAS value.

		Returns:
			str(e1Trunk|t1EsfTrunk|t1SfTrunk)
		"""
		return self._get_attribute('cas')

	@property
	def CemOption(self):
		"""The value of the CEM option.

		Returns:
			number
		"""
		return self._get_attribute('cemOption')

	@property
	def CemPayloadBytes(self):
		"""(For Circuit Emulation Service over MPLS/CEM). The length of the CEM payload (in bytes).

		Returns:
			number
		"""
		return self._get_attribute('cemPayloadBytes')

	@property
	def Description(self):
		"""An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def DisCeAddress(self):
		"""If the L2 interface type for the VC whose learned information is seen is IP, this field indicates the learned IP address of the remote end CE of the IP vrtual circuit.

		Returns:
			str
		"""
		return self._get_attribute('disCeAddress')

	@property
	def Frequency(self):
		"""Indicates the frequency.

		Returns:
			number
		"""
		return self._get_attribute('frequency')

	@property
	def GroupId(self):
		"""An arbitrary 32-bit value used to identify a group of VCs.

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def IncludeRtpHeader(self):
		"""If enables, includes the RTP information in the header.

		Returns:
			bool
		"""
		return self._get_attribute('includeRtpHeader')

	@property
	def Label(self):
		"""The label value added to the packet(s) by the upstream LDP peer.

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LabelSpaceId(self):
		"""(2 octets) Identifies the set of labels that will be used. Part of the LDP identifier.

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceId')

	@property
	def LocalPwSubStatus(self):
		"""It reflects the status carried in the PW status notification received from the peer.

		Returns:
			number
		"""
		return self._get_attribute('localPwSubStatus')

	@property
	def MaxAtmCell(self):
		"""The maximum number of ATM Cells which may be concatenated and sent in a single MPLS frame. This parameter is part of the FEC element.

		Returns:
			number
		"""
		return self._get_attribute('maxAtmCell')

	@property
	def Mtu(self):
		"""(in octets) The 2-octet value for the maximum Transmission Unit (MTU).

		Returns:
			number
		"""
		return self._get_attribute('mtu')

	@property
	def PayloadSize(self):
		"""Indicates the payload size.

		Returns:
			number
		"""
		return self._get_attribute('payloadSize')

	@property
	def PayloadType(self):
		"""The payload type.

		Returns:
			number
		"""
		return self._get_attribute('payloadType')

	@property
	def Peer(self):
		"""The RID of the upstream LDP peer. Part of the LSR ID. It must be globally unique. It forms the first 4 octets of the 6-octet LDP identifier.

		Returns:
			str
		"""
		return self._get_attribute('peer')

	@property
	def PeerPwSubStatus(self):
		"""It reflects the status carried in the PW status last sent to the peer.

		Returns:
			number
		"""
		return self._get_attribute('peerPwSubStatus')

	@property
	def PwState(self):
		"""The PseudoWire State - either Up or Down. For the PseudoWire to be Up (Up status), the VC ID, VC Type, and Peer must match.If the Enable VC Group Matching (on PseudoWire Status) option is enabled for the router, the VC Group ID must also be matched for the PseudoWire State to be Up.

		Returns:
			bool
		"""
		return self._get_attribute('pwState')

	@property
	def Sp(self):
		"""Indicates the SP value.

		Returns:
			str(hexVal1|hexVal2|hexVal3|hexVal4)
		"""
		return self._get_attribute('sp')

	@property
	def Ssrc(self):
		"""Indicates the SSRC value.

		Returns:
			number
		"""
		return self._get_attribute('ssrc')

	@property
	def TdmBitrate(self):
		"""The tdm bit rate.

		Returns:
			number
		"""
		return self._get_attribute('tdmBitrate')

	@property
	def TimestampMode(self):
		"""Indicates the timestamp mode.

		Returns:
			str(absolute|differential)
		"""
		return self._get_attribute('timestampMode')

	@property
	def VcId(self):
		"""The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).

		Returns:
			number
		"""
		return self._get_attribute('vcId')

	@property
	def VcType(self):
		"""The type of L2 VC depends on the Layer 2 protocol types.

		Returns:
			str(frameRelay|atmaal5|atmxCell|vlan|ethernet|hdlc|ppp|cem|atmvcc|atmvpc|ip|satopE1|satopT1|satopE3|satopT3|cesoPsnBasic|cesoPsnCas|frameRelayRfc4619)
		"""
		return self._get_attribute('vcType')

	def find(self, CBit=None, Cas=None, CemOption=None, CemPayloadBytes=None, Description=None, DisCeAddress=None, Frequency=None, GroupId=None, IncludeRtpHeader=None, Label=None, LabelSpaceId=None, LocalPwSubStatus=None, MaxAtmCell=None, Mtu=None, PayloadSize=None, PayloadType=None, Peer=None, PeerPwSubStatus=None, PwState=None, Sp=None, Ssrc=None, TdmBitrate=None, TimestampMode=None, VcId=None, VcType=None):
		"""Finds and retrieves learnedMartiniLabel data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedMartiniLabel data from the server.
		By default the find method takes no parameters and will retrieve all learnedMartiniLabel data from the server.

		Args:
			CBit (bool): If enabled, sets the C-Bit (flag). It is the highest order bit in the VC Type field. If the bit is set, it indicates the presence of a control word on this VC.
			Cas (str(e1Trunk|t1EsfTrunk|t1SfTrunk)): Indicates the CAS value.
			CemOption (number): The value of the CEM option.
			CemPayloadBytes (number): (For Circuit Emulation Service over MPLS/CEM). The length of the CEM payload (in bytes).
			Description (str): An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.
			DisCeAddress (str): If the L2 interface type for the VC whose learned information is seen is IP, this field indicates the learned IP address of the remote end CE of the IP vrtual circuit.
			Frequency (number): Indicates the frequency.
			GroupId (number): An arbitrary 32-bit value used to identify a group of VCs.
			IncludeRtpHeader (bool): If enables, includes the RTP information in the header.
			Label (number): The label value added to the packet(s) by the upstream LDP peer.
			LabelSpaceId (number): (2 octets) Identifies the set of labels that will be used. Part of the LDP identifier.
			LocalPwSubStatus (number): It reflects the status carried in the PW status notification received from the peer.
			MaxAtmCell (number): The maximum number of ATM Cells which may be concatenated and sent in a single MPLS frame. This parameter is part of the FEC element.
			Mtu (number): (in octets) The 2-octet value for the maximum Transmission Unit (MTU).
			PayloadSize (number): Indicates the payload size.
			PayloadType (number): The payload type.
			Peer (str): The RID of the upstream LDP peer. Part of the LSR ID. It must be globally unique. It forms the first 4 octets of the 6-octet LDP identifier.
			PeerPwSubStatus (number): It reflects the status carried in the PW status last sent to the peer.
			PwState (bool): The PseudoWire State - either Up or Down. For the PseudoWire to be Up (Up status), the VC ID, VC Type, and Peer must match.If the Enable VC Group Matching (on PseudoWire Status) option is enabled for the router, the VC Group ID must also be matched for the PseudoWire State to be Up.
			Sp (str(hexVal1|hexVal2|hexVal3|hexVal4)): Indicates the SP value.
			Ssrc (number): Indicates the SSRC value.
			TdmBitrate (number): The tdm bit rate.
			TimestampMode (str(absolute|differential)): Indicates the timestamp mode.
			VcId (number): The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).
			VcType (str(frameRelay|atmaal5|atmxCell|vlan|ethernet|hdlc|ppp|cem|atmvcc|atmvpc|ip|satopE1|satopT1|satopE3|satopT3|cesoPsnBasic|cesoPsnCas|frameRelayRfc4619)): The type of L2 VC depends on the Layer 2 protocol types.

		Returns:
			self: This instance with matching learnedMartiniLabel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedMartiniLabel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedMartiniLabel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
