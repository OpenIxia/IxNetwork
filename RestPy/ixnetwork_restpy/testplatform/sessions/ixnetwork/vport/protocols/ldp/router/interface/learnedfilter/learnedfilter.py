from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedFilter(Base):
	"""The LearnedFilter class encapsulates a required learnedFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedFilter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedFilter'

	def __init__(self, parent):
		super(LearnedFilter, self).__init__(parent)

	@property
	def EnableFilter(self):
		"""Enables the use of the LDP learned labels filter.

		Returns:
			bool
		"""
		return self._get_attribute('enableFilter')
	@EnableFilter.setter
	def EnableFilter(self, value):
		self._set_attribute('enableFilter', value)

	@property
	def EnableIpv4FecAddress(self):
		"""If enabled, uses the network address associated with the FEC.

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv4FecAddress')
	@EnableIpv4FecAddress.setter
	def EnableIpv4FecAddress(self, value):
		self._set_attribute('enableIpv4FecAddress', value)

	@property
	def EnableIpv4FecMask(self):
		"""(FEC Mask Match must be enabled for this option to be active.)

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv4FecMask')
	@EnableIpv4FecMask.setter
	def EnableIpv4FecMask(self, value):
		self._set_attribute('enableIpv4FecMask', value)

	@property
	def EnableIpv4RootAddress(self):
		"""If enabled, it signifies the IP version 4 root address.

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv4RootAddress')
	@EnableIpv4RootAddress.setter
	def EnableIpv4RootAddress(self, value):
		self._set_attribute('enableIpv4RootAddress', value)

	@property
	def EnableLabel(self):
		"""If enabled, uses the label value added to the packet(s) by the upstream LDP peer.

		Returns:
			bool
		"""
		return self._get_attribute('enableLabel')
	@EnableLabel.setter
	def EnableLabel(self, value):
		self._set_attribute('enableLabel', value)

	@property
	def EnableMartiniDescription(self):
		"""An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniDescription')
	@EnableMartiniDescription.setter
	def EnableMartiniDescription(self, value):
		self._set_attribute('enableMartiniDescription', value)

	@property
	def EnableMartiniGroupId(self):
		"""An arbitrary 32-bit value used to identify a group of VCs.

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniGroupId')
	@EnableMartiniGroupId.setter
	def EnableMartiniGroupId(self, value):
		self._set_attribute('enableMartiniGroupId', value)

	@property
	def EnableMartiniVcId(self):
		"""The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniVcId')
	@EnableMartiniVcId.setter
	def EnableMartiniVcId(self, value):
		self._set_attribute('enableMartiniVcId', value)

	@property
	def EnableMartiniVcType(self):
		"""Enables the type of martini virtual circuit.

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniVcType')
	@EnableMartiniVcType.setter
	def EnableMartiniVcType(self, value):
		self._set_attribute('enableMartiniVcType', value)

	@property
	def EnablePeerAddress(self):
		"""Uses the IP address of the LDP peer.

		Returns:
			bool
		"""
		return self._get_attribute('enablePeerAddress')
	@EnablePeerAddress.setter
	def EnablePeerAddress(self, value):
		self._set_attribute('enablePeerAddress', value)

	@property
	def EnablePeerMask(self):
		"""(Peer address must be enabled for this option to be active.) If enabled, uses the number of bits in the mask for the peer's IP address for a loose match.

		Returns:
			bool
		"""
		return self._get_attribute('enablePeerMask')
	@EnablePeerMask.setter
	def EnablePeerMask(self, value):
		self._set_attribute('enablePeerMask', value)

	@property
	def Ipv4FecAddress(self):
		"""The IPv4 address component of the FEC. (default = 0.0.0.0)

		Returns:
			str
		"""
		return self._get_attribute('ipv4FecAddress')
	@Ipv4FecAddress.setter
	def Ipv4FecAddress(self, value):
		self._set_attribute('ipv4FecAddress', value)

	@property
	def Ipv4FecMask(self):
		"""The prefix length of the network IPv4 address. (default = 24)

		Returns:
			number
		"""
		return self._get_attribute('ipv4FecMask')
	@Ipv4FecMask.setter
	def Ipv4FecMask(self, value):
		self._set_attribute('ipv4FecMask', value)

	@property
	def Ipv4FecMaskMatch(self):
		"""FEC Mask Match must be enabled for this option to be active.

		Returns:
			str(exactMatch|looseMatch)
		"""
		return self._get_attribute('ipv4FecMaskMatch')
	@Ipv4FecMaskMatch.setter
	def Ipv4FecMaskMatch(self, value):
		self._set_attribute('ipv4FecMaskMatch', value)

	@property
	def Label(self):
		"""The first label to be assigned to the FEC.

		Returns:
			number
		"""
		return self._get_attribute('label')
	@Label.setter
	def Label(self, value):
		self._set_attribute('label', value)

	@property
	def MartiniDescription(self):
		"""An optional user-defined interface description. It may be used with ALL VC types. Valid length is 0 to 80 octets.

		Returns:
			str
		"""
		return self._get_attribute('martiniDescription')
	@MartiniDescription.setter
	def MartiniDescription(self, value):
		self._set_attribute('martiniDescription', value)

	@property
	def MartiniGroupId(self):
		"""An arbitrary 32-bit value used to identify a group of VCs.

		Returns:
			number
		"""
		return self._get_attribute('martiniGroupId')
	@MartiniGroupId.setter
	def MartiniGroupId(self, value):
		self._set_attribute('martiniGroupId', value)

	@property
	def MartiniVcId(self):
		"""The 32-bit VC connection identifier. Used with the VC type to identify a specific VC (for VC types 0x0001 to 0x000B).

		Returns:
			number
		"""
		return self._get_attribute('martiniVcId')
	@MartiniVcId.setter
	def MartiniVcId(self, value):
		self._set_attribute('martiniVcId', value)

	@property
	def MartiniVcType(self):
		"""The type of L2 VC depends on the Layer 2 protocol types.

		Returns:
			str(frameRelay|atmaal5|atmxCell|vlan|ethernet|hdlc|ppp|cem|atmvcc|atmvpc|ip)
		"""
		return self._get_attribute('martiniVcType')
	@MartiniVcType.setter
	def MartiniVcType(self, value):
		self._set_attribute('martiniVcType', value)

	@property
	def PeerAddress(self):
		"""If enabled, uses the IP address of the LDP peer.

		Returns:
			str
		"""
		return self._get_attribute('peerAddress')
	@PeerAddress.setter
	def PeerAddress(self, value):
		self._set_attribute('peerAddress', value)

	@property
	def PeerMask(self):
		"""(Peer Address must be enabled for this option to be active.) If enabled, uses the number of bits in the mask for the peer's IP address for a loose match.

		Returns:
			number
		"""
		return self._get_attribute('peerMask')
	@PeerMask.setter
	def PeerMask(self, value):
		self._set_attribute('peerMask', value)

	@property
	def RootAddress(self):
		"""Indicates the root address.

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')
	@RootAddress.setter
	def RootAddress(self, value):
		self._set_attribute('rootAddress', value)
