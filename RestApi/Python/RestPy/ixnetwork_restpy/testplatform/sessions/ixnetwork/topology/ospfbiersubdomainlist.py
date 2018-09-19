from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OspfBierSubDomainList(Base):
	"""The OspfBierSubDomainList class encapsulates a required ospfBierSubDomainList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OspfBierSubDomainList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ospfBierSubDomainList'

	def __init__(self, parent):
		super(OspfBierSubDomainList, self).__init__(parent)

	@property
	def OspfBierBSObjectList(self):
		"""An instance of the OspfBierBSObjectList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfbierbsobjectlist.OspfBierBSObjectList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfbierbsobjectlist import OspfBierBSObjectList
		return OspfBierBSObjectList(self)

	@property
	def BFRId(self):
		"""BFR Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRId')

	@property
	def Bar(self):
		"""BIER Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('Bar')

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
	def Ipa(self):
		"""IPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipa')

	@property
	def MtId(self):
		"""Multi-Topology ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mtId')

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
	def NumberOfBSLen(self):
		"""Number of Supported BS Len

		Returns:
			number
		"""
		return self._get_attribute('numberOfBSLen')
	@NumberOfBSLen.setter
	def NumberOfBSLen(self, value):
		self._set_attribute('numberOfBSLen', value)

	@property
	def SubDomainId(self):
		"""Sub Domain Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subDomainId')
