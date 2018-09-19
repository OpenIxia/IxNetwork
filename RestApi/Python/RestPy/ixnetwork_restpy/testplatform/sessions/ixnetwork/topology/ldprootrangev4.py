from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LdpRootRangeV4(Base):
	"""The LdpRootRangeV4 class encapsulates a required ldpRootRangeV4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LdpRootRangeV4 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ldpRootRangeV4'

	def __init__(self, parent):
		super(LdpRootRangeV4, self).__init__(parent)

	@property
	def LdpTLVList(self):
		"""An instance of the LdpTLVList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptlvlist.LdpTLVList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptlvlist import LdpTLVList
		return LdpTLVList(self)

	@property
	def ContinuousIncrementOVAcrossRoot(self):
		"""Continuous Increment Opaque Value Across Root

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('continuousIncrementOVAcrossRoot')

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
	def FilterOnGroupAddress(self):
		"""If selected, all the LSPs will belong to the same set of groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterOnGroupAddress')

	@property
	def GroupCountPerLSP(self):
		"""Group Count Per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCountPerLSP')

	@property
	def LspCountPerRoot(self):
		"""LSP Count Per Root

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspCountPerRoot')

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
	def NumberOfTLVs(self):
		"""Number Of TLVs

		Returns:
			number
		"""
		return self._get_attribute('numberOfTLVs')
	@NumberOfTLVs.setter
	def NumberOfTLVs(self, value):
		self._set_attribute('numberOfTLVs', value)

	@property
	def RootAddress(self):
		"""Root Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddress')

	@property
	def RootAddressCount(self):
		"""Root Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddressCount')

	@property
	def RootAddressStep(self):
		"""Root Address Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddressStep')

	@property
	def SourceAddressV4(self):
		"""IPv4 Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressV4')

	@property
	def SourceAddressV6(self):
		"""IPv6 Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressV6')

	@property
	def SourceCountPerLSP(self):
		"""Source Count Per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceCountPerLSP')

	@property
	def StartGroupAddressV4(self):
		"""Start Group Address(V4)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressV4')

	@property
	def StartGroupAddressV6(self):
		"""Start Group Address(V6)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressV6')
