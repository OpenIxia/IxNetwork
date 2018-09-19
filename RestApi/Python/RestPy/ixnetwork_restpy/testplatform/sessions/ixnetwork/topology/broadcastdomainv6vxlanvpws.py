from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BroadcastDomainV6VxlanVpws(Base):
	"""The BroadcastDomainV6VxlanVpws class encapsulates a required broadcastDomainV6VxlanVpws node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BroadcastDomainV6VxlanVpws property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'broadcastDomainV6VxlanVpws'

	def __init__(self, parent):
		super(BroadcastDomainV6VxlanVpws, self).__init__(parent)

	@property
	def PnTLVList(self):
		"""An instance of the PnTLVList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pntlvlist.PnTLVList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pntlvlist import PnTLVList
		return PnTLVList(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdRouteLabel(self):
		"""AD Route Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('adRouteLabel')

	@property
	def BVlanId(self):
		"""B VLAN ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bVlanId')

	@property
	def BVlanPriority(self):
		"""B VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bVlanPriority')

	@property
	def BVlanTpid(self):
		"""B VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bVlanTpid')

	@property
	def BackupFlag(self):
		"""Backup Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('backupFlag')

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
	def EnableVlanAwareService(self):
		"""Enable VLAN Aware Service

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableVlanAwareService')

	@property
	def EthernetTagId(self):
		"""Ethernet Tag ID. For VPWS, this acts as VPWS Service ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ethernetTagId')

	@property
	def FxcType(self):
		"""FXC Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fxcType')

	@property
	def GroupAddress(self):
		"""Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddress')

	@property
	def IncludeVpwsL2AttrExtComm(self):
		"""Include VPWS Layer 2 Attributes Extended Community

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeVpwsL2AttrExtComm')

	@property
	def L2Mtu(self):
		"""L2 MTU

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('l2Mtu')

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
	def NoOfMacPools(self):
		"""Number of Mac Pools

		Returns:
			number
		"""
		return self._get_attribute('noOfMacPools')
	@NoOfMacPools.setter
	def NoOfMacPools(self, value):
		self._set_attribute('noOfMacPools', value)

	@property
	def PrimaryPE(self):
		"""Primary PE

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('primaryPE')

	@property
	def RemoteServiceId(self):
		"""Remote Service ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteServiceId')

	@property
	def RequireCW(self):
		"""Require CW

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requireCW')

	@property
	def RootAddress(self):
		"""Root Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddress')

	@property
	def RsvpP2mpId(self):
		"""RSVP P2MP ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsvpP2mpId')

	@property
	def RsvpP2mpIdAsNumber(self):
		"""RSVP P2MP ID as Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsvpP2mpIdAsNumber')

	@property
	def RsvpTunnelId(self):
		"""RSVP Tunnel ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rsvpTunnelId')

	@property
	def SenderAddressPRootNodeAddress(self):
		"""Sender Address/P-Root Node Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('senderAddressPRootNodeAddress')

	@property
	def UsebVlan(self):
		"""Use B-VLAN

		Returns:
			bool
		"""
		return self._get_attribute('usebVlan')
	@UsebVlan.setter
	def UsebVlan(self, value):
		self._set_attribute('usebVlan', value)

	@property
	def VidNormalization(self):
		"""VID Normalization

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vidNormalization')
