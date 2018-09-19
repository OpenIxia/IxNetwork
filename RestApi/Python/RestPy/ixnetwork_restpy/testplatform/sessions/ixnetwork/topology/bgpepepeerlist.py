from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpEpePeerList(Base):
	"""The BgpEpePeerList class encapsulates a required bgpEpePeerList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpEpePeerList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bgpEpePeerList'

	def __init__(self, parent):
		super(BgpEpePeerList, self).__init__(parent)

	@property
	def BgpEpePeerLinkList(self):
		"""An instance of the BgpEpePeerLinkList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpepepeerlinklist.BgpEpePeerLinkList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpepepeerlinklist import BgpEpePeerLinkList
		return BgpEpePeerLinkList(self)._select()

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
	def BgpLocalRouterId(self):
		"""BGP Router ID for Local Node Descriptor

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpLocalRouterId')

	@property
	def BgpRemoteRouterId(self):
		"""BGP Router ID for Remote Node Descriptor

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bgpRemoteRouterId')

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
	def EnablePeerNodeSid(self):
		"""

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePeerNodeSid')

	@property
	def LBit(self):
		"""Local Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lBit')

	@property
	def LocalAsn(self):
		"""Local ASN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localAsn')

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
	def NoOflinks(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOflinks')
	@NoOflinks.setter
	def NoOflinks(self, value):
		self._set_attribute('noOflinks', value)

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
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerName')

	@property
	def PeerSetGroup(self):
		"""Peer Set Group

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerSetGroup')

	@property
	def RemoteAsn(self):
		"""Remote ASN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteAsn')

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
	def UseLocalConfedId(self):
		"""Use Local Confederation identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useLocalConfedId')

	@property
	def UseRemoteConfedId(self):
		"""Use Remote Confederation identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useRemoteConfedId')

	@property
	def VBit(self):
		"""Value Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vBit')

	@property
	def Weight(self):
		"""Weight of SID for Load Balancing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')
