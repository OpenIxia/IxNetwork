from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CfmCcmLearnedInfoFilters(Base):
	"""The CfmCcmLearnedInfoFilters class encapsulates a required cfmCcmLearnedInfoFilters node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CfmCcmLearnedInfoFilters property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'cfmCcmLearnedInfoFilters'

	def __init__(self, parent):
		super(CfmCcmLearnedInfoFilters, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AllDestinationMep(self):
		"""All Destination MEP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allDestinationMep')

	@property
	def AllSourceMep(self):
		"""All Source MEP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allSourceMep')

	@property
	def AllcVlan(self):
		"""All C-VLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allcVlan')

	@property
	def AllmdmgLevel(self):
		"""All MD/MEG Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allmdmgLevel')

	@property
	def AllsVlan(self):
		"""All S-VLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allsVlan')

	@property
	def AllshortMaName(self):
		"""All Short MA Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allshortMaName')

	@property
	def AllshortMaNameFormatType(self):
		"""All Short MA Name Format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allshortMaNameFormatType')

	@property
	def CVlanIdLi(self):
		"""C-VLAN ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cVlanIdLi')

	@property
	def CVlanLi(self):
		"""C-VLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cVlanLi')

	@property
	def CVlanPriorityLi(self):
		"""C-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cVlanPriorityLi')

	@property
	def CVlanPriorityLiccm(self):
		"""C-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cVlanPriorityLiccm')

	@property
	def CVlanTpidLi(self):
		"""C-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cVlanTpidLi')

	@property
	def CVlanTpidLiccm(self):
		"""C-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cVlanTpidLiccm')

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
	def DestinationMpMac(self):
		"""Destination MP MAC

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destinationMpMac')

	@property
	def EnableAllcVlan(self):
		"""All C-VLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAllcVlan')

	@property
	def EnableAllsVlan(self):
		"""All S-VLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAllsVlan')

	@property
	def EnableLtLearnedInfoOptions(self):
		"""Filter LT Learned Info Options

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLtLearnedInfoOptions')

	@property
	def EnableccmLeanredInfo(self):
		"""CCM Learned Info Filter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableccmLeanredInfo')

	@property
	def MdlevelLi(self):
		"""MD Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdlevelLi')

	@property
	def Mdmglevel(self):
		"""MD/MEG Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdmglevel')

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
	def SVlanIdLi(self):
		"""S-VLAN ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sVlanIdLi')

	@property
	def SVlanLi(self):
		"""S-VLAN

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sVlanLi')

	@property
	def SVlanPriorityLi(self):
		"""S-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sVlanPriorityLi')

	@property
	def SVlanPriorityLiccm(self):
		"""S-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sVlanPriorityLiccm')

	@property
	def SVlanTpidLi(self):
		"""S-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sVlanTpidLi')

	@property
	def SVlanTpidLiccm(self):
		"""S-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sVlanTpidLiccm')

	@property
	def ShortMaNameFormatLi(self):
		"""Short MA Name Format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('shortMaNameFormatLi')

	@property
	def ShortMaNameLi(self):
		"""Short MA Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('shortMaNameLi')

	@property
	def SourceMpMac(self):
		"""Source MP MAC

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceMpMac')

	@property
	def TimeoutLi(self):
		"""Timeout

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutLi')

	@property
	def TransactionIdLi(self):
		"""Transaction ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('transactionIdLi')

	@property
	def TtlLi(self):
		"""TTL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ttlLi')

	def ClearAllLearnedInfo(self, Arg2):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clears ALL Learned LSP Information By PCC Device.

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
		return self._execute('ClearAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, Arg2):
		"""Executes the getAllLearnedInfo operation on the server.

		Please provide a proper help text here.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): Please provide a proper description here

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetAllLearnedInfo', payload=locals(), response_object=None)

	def GetCfmCcmLearnedInformation(self, Arg2):
		"""Executes the getCfmCcmLearnedInformation operation on the server.

		Please provide a proper help text here.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): Please provide a proper description here.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetCfmCcmLearnedInformation', payload=locals(), response_object=None)
