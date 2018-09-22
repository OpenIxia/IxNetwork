from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LdpLeafRangeV4(Base):
	"""The LdpLeafRangeV4 class encapsulates a required ldpLeafRangeV4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LdpLeafRangeV4 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ldpLeafRangeV4'

	def __init__(self, parent):
		super(LdpLeafRangeV4, self).__init__(parent)

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
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def GroupAddressV4(self):
		"""IPv4 Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressV4')

	@property
	def GroupAddressV6(self):
		"""IPv6 Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressV6')

	@property
	def GroupCountPerLsp(self):
		"""Group Count per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCountPerLsp')

	@property
	def LSPType(self):
		"""LSP Type

		Returns:
			str(p2MP)
		"""
		return self._get_attribute('lSPType')
	@LSPType.setter
	def LSPType(self, value):
		self._set_attribute('lSPType', value)

	@property
	def LabelValueStart(self):
		"""Label Value Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelValueStart')

	@property
	def LabelValueStep(self):
		"""Label Value Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelValueStep')

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

	def ActivateLeafRange(self):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ActivateLeafRange', payload=locals(), response_object=None)

	def ActivateLeafRange(self, SessionIndices):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ActivateLeafRange', payload=locals(), response_object=None)

	def ActivateLeafRange(self, SessionIndices):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ActivateLeafRange', payload=locals(), response_object=None)

	def ActivateLeafRange(self, Arg2):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ActivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('DeactivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, SessionIndices):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('DeactivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, SessionIndices):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('DeactivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, Arg2):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DeactivateLeafRange', payload=locals(), response_object=None)
