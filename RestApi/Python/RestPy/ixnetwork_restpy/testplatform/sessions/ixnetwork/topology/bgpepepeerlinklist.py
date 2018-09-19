from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpEpePeerLinkList(Base):
	"""The BgpEpePeerLinkList class encapsulates a required bgpEpePeerLinkList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpEpePeerLinkList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpEpePeerLinkList'

	def __init__(self, parent):
		super(BgpEpePeerLinkList, self).__init__(parent)

	@property
	def TlvProfile(self):
		"""An instance of the TlvProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlvprofile.TlvProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlvprofile import TlvProfile
		return TlvProfile(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BBit(self):
		"""B-Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bBit')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnableLinkAddress(self):
		"""Enable Link Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLinkAddress')

	@property
	def EnableLinkIdentifier(self):
		"""Enable Link Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLinkIdentifier')

	@property
	def EnablePeerAdjSid(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePeerAdjSid')

	@property
	def LBit(self):
		"""Local Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lBit')

	@property
	def LinkAddressType(self):
		"""Link Address Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkAddressType')

	@property
	def LinkLocalIdentifier(self):
		"""Link Local Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkLocalIdentifier')

	@property
	def LinkNumber(self):
		"""EPE Link Number For Reference

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkNumber')

	@property
	def LinkRemoteIdentifier(self):
		"""Link Remote Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkRemoteIdentifier')

	@property
	def LocalIpv4LinkAddress(self):
		"""Local IPv4 Link Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localIpv4LinkAddress')

	@property
	def LocalIpv6LinkAddress(self):
		"""Local IPv6 Link Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localIpv6LinkAddress')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def OtherBits(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('otherBits')

	@property
	def PBit(self):
		"""P-Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pBit')

	@property
	def PeerName(self):
		"""Peer Name For Reference

		Returns:
			list(str)
		"""
		return self._get_attribute('peerName')

	@property
	def RemoteIpv4LinkAddress(self):
		"""Remote IPv4 Link Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIpv4LinkAddress')

	@property
	def RemoteIpv6LinkAddress(self):
		"""Remote IPv6 Link Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIpv6LinkAddress')

	@property
	def Reserved(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reserved')

	@property
	def SidIndex(self):
		"""SID/Index

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidIndex')

	@property
	def SidIndexValue(self):
		"""SID or Index Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidIndexValue')

	@property
	def VBit(self):
		"""Value Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vBit')

	@property
	def Weight(self):
		"""Weight of the SID for the purpose of load balancing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')
