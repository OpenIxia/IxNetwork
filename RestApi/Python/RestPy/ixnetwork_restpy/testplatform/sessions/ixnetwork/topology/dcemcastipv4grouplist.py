from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceMCastIpv4GroupList(Base):
	"""The DceMCastIpv4GroupList class encapsulates a required dceMCastIpv4GroupList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceMCastIpv4GroupList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dceMCastIpv4GroupList'

	def __init__(self, parent):
		super(DceMCastIpv4GroupList, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def InterGrpUcastAddrIncr(self):
		"""Inter-Group Source Address Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interGrpUcastAddrIncr')

	@property
	def McastAddrCnt(self):
		"""Multicast Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mcastAddrCnt')

	@property
	def McastAddrIncr(self):
		"""Multicast Address Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mcastAddrIncr')

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
	def SrcGrpMapping(self):
		"""Source-Group Mapping

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srcGrpMapping')

	@property
	def StartMcastAddr(self):
		"""Start Multicast Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startMcastAddr')

	@property
	def StartUcastAddr(self):
		"""Start Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startUcastAddr')

	@property
	def TopologyId(self):
		"""Topology/Nickname

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('topologyId')

	@property
	def UcastAddrIncr(self):
		"""Source Address Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ucastAddrIncr')

	@property
	def UcastSrcCnt(self):
		"""# Sources per Multicast Group

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ucastSrcCnt')

	@property
	def VlanId(self):
		"""Vlan Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanId')
