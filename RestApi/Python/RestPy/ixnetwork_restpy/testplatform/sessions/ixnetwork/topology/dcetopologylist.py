from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DceTopologyList(Base):
	"""The DceTopologyList class encapsulates a required dceTopologyList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceTopologyList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dceTopologyList'

	def __init__(self, parent):
		super(DceTopologyList, self).__init__(parent)

	@property
	def InterestedVlanList(self):
		"""An instance of the InterestedVlanList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interestedvlanlist.InterestedVlanList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interestedvlanlist import InterestedVlanList
		return InterestedVlanList(self)._select()

	@property
	def NicknameRecordList(self):
		"""An instance of the NicknameRecordList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nicknamerecordlist.NicknameRecordList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nicknamerecordlist import NicknameRecordList
		return NicknameRecordList(self)._select()

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
	def EnableFTAG(self):
		"""Enable FTAG

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFTAG')

	@property
	def InterestedVlanRangeCount(self):
		"""Interested VLAN Range Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('interestedVlanRangeCount')
	@InterestedVlanRangeCount.setter
	def InterestedVlanRangeCount(self, value):
		self._set_attribute('interestedVlanRangeCount', value)

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
	def NicknameCount(self):
		"""Nickname Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('nicknameCount')
	@NicknameCount.setter
	def NicknameCount(self, value):
		self._set_attribute('nicknameCount', value)

	@property
	def NoOfTreesToCompute(self):
		"""No. of Trees to Compute

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('noOfTreesToCompute')

	@property
	def StartFTAGValue(self):
		"""Start FTAG Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startFTAGValue')

	@property
	def TopologyId(self):
		"""Topology Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('topologyId')
