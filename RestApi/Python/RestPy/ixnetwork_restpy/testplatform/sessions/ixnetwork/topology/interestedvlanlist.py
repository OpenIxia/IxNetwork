from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterestedVlanList(Base):
	"""The InterestedVlanList class encapsulates a required interestedVlanList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InterestedVlanList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interestedVlanList'

	def __init__(self, parent):
		super(InterestedVlanList, self).__init__(parent)

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
	def IncludeInLSP(self):
		"""Include in LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeInLSP')

	@property
	def IncludeInMGroupPDU(self):
		"""Include in MGROUP-PDU

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeInMGroupPDU')

	@property
	def M4BitEnabled(self):
		"""M4 Bit Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('m4BitEnabled')

	@property
	def M6BitEnabled(self):
		"""M6 Bit Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('m6BitEnabled')

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
	def Nickname(self):
		"""Nickname

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nickname')

	@property
	def NoOfSpanningTreeRoots(self):
		"""No. of Spanning Tree Roots

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('noOfSpanningTreeRoots')

	@property
	def StartSpanningTreeRootBridgeId(self):
		"""Start Spanning Tree Root Bridge ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startSpanningTreeRootBridgeId')

	@property
	def StartVlanId(self):
		"""Start Vlan Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startVlanId')

	@property
	def VlanCount(self):
		"""Vlan Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanCount')

	@property
	def VlanIdIncr(self):
		"""Vlan Id Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanIdIncr')
