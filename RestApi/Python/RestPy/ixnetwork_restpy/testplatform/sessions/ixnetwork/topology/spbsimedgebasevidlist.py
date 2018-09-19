from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbSimEdgeBaseVidList(Base):
	"""The SpbSimEdgeBaseVidList class encapsulates a required spbSimEdgeBaseVidList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbSimEdgeBaseVidList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'spbSimEdgeBaseVidList'

	def __init__(self, parent):
		super(SpbSimEdgeBaseVidList, self).__init__(parent)

	@property
	def SpbSimEdgeIsidList(self):
		"""An instance of the SpbSimEdgeIsidList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgeisidlist.SpbSimEdgeIsidList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgeisidlist import SpbSimEdgeIsidList
		return SpbSimEdgeIsidList(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BaseVid(self):
		"""Base VID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('baseVid')

	@property
	def BaseVlanPriority(self):
		"""B-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('baseVlanPriority')

	@property
	def BvlanTpid(self):
		"""B-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bvlanTpid')

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
	def EctAlgorithm(self):
		"""ECT AlgorithmType

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ectAlgorithm')

	@property
	def IsidCount(self):
		"""ISID Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('isidCount')
	@IsidCount.setter
	def IsidCount(self, value):
		self._set_attribute('isidCount', value)

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
	def UseFlagBit(self):
		"""Use Flag Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useFlagBit')
