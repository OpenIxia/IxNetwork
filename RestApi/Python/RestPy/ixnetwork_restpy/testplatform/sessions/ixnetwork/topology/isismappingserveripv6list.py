from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisMappingServerIPV6List(Base):
	"""The IsisMappingServerIPV6List class encapsulates a required isisMappingServerIPV6List node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IsisMappingServerIPV6List property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'isisMappingServerIPV6List'

	def __init__(self, parent):
		super(IsisMappingServerIPV6List, self).__init__(parent)

	@property
	def AFlag(self):
		"""Attached flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('aFlag')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Algorithm(self):
		"""Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('algorithm')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DFlag(self):
		"""When the SID/Label Binding TLV is leaked from level-2 to level-1, this flag MUST be set, else it should be clear

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dFlag')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EFlag(self):
		"""Explicit NULL flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlag')

	@property
	def FECPrefix(self):
		"""IPv6 FEC Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fECPrefix')

	@property
	def LFlag(self):
		"""Local Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def LastFECAddress(self):
		"""Last IPv6 FEC Address

		Returns:
			list(str)
		"""
		return self._get_attribute('lastFECAddress')

	@property
	def MFlag(self):
		"""Mirror Context flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mFlag')

	@property
	def NFlag(self):
		"""N Flag: Indicates the nodal prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nFlag')

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
	def PFlag(self):
		"""P Flag: Indicates that to reach to a prefix, this router would be penultimate hop.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlag')

	@property
	def PrefixLength(self):
		"""Length of the IPv4 FEC prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def RFlag(self):
		"""Redistribution flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rFlag')

	@property
	def Range(self):
		"""This the count of continuous FEC IPv6 prefixes and their respective continuous SID/labels

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('range')

	@property
	def SFlag(self):
		"""Enabling this flag lets the SID/Label Binding TLV to get flooded across the entire routing domain, else this TLV should not be leaked between levels

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sFlag')

	@property
	def StartSIDLabel(self):
		"""Starting value of SID/ Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startSIDLabel')

	@property
	def VFlag(self):
		"""Value Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

	@property
	def Weight(self):
		"""Weight

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')

	def Advertise(self, Arg2):
		"""Executes the advertise operation on the server.

		Advertise the V6 Mapping Server Range TLVs

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Advertise', payload=locals(), response_object=None)

	def Withdraw(self, Arg2):
		"""Executes the withdraw operation on the server.

		Withdraw the V6 Mapping Server Range TLVs

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Withdraw', payload=locals(), response_object=None)
