from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceBasicSrSyncLspUpdateParams(Base):
	"""The PceBasicSrSyncLspUpdateParams class encapsulates a system managed pceBasicSrSyncLspUpdateParams node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceBasicSrSyncLspUpdateParams property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceBasicSrSyncLspUpdateParams'

	def __init__(self, parent):
		super(PceBasicSrSyncLspUpdateParams, self).__init__(parent)

	@property
	def PceUpdateSrEroSubObjectList(self):
		"""An instance of the PceUpdateSrEroSubObjectList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrerosubobjectlist.PceUpdateSrEroSubObjectList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrerosubobjectlist import PceUpdateSrEroSubObjectList
		return PceUpdateSrEroSubObjectList(self)

	@property
	def PceUpdateSrMetricSubObjectList(self):
		"""An instance of the PceUpdateSrMetricSubObjectList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrmetricsubobjectlist.PceUpdateSrMetricSubObjectList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pceupdatesrmetricsubobjectlist import PceUpdateSrMetricSubObjectList
		return PceUpdateSrMetricSubObjectList(self)

	@property
	def Bandwidth(self):
		"""Bandwidth (bps)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

	@property
	def BindingTypeTriggerParam(self):
		"""Indicates the type of binding included in the TLV. Types are as follows: 20bit MPLS Label 32bit MPLS Label. Default value is 20bit MPLS Label.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bindingTypeTriggerParam')

	@property
	def Bos_TriggerParam(self):
		"""This bit is set to true for the last entry in the label stack i.e., for the bottom of the stack, and false for all other label stack entries. This control will be editable only if Binding Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bos_TriggerParam')

	@property
	def ConfigureBandwidth(self):
		"""Configure Bandwidth

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureBandwidth')

	@property
	def ConfigureEro(self):
		"""Configure ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureEro')

	@property
	def ConfigureLsp(self):
		"""Configure LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureLsp')

	@property
	def ConfigureLspa(self):
		"""Configure LSPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureLspa')

	@property
	def ConfigureMetric(self):
		"""Configure Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureMetric')

	@property
	def ExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

	@property
	def HoldingPriority(self):
		"""Holding Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('holdingPriority')

	@property
	def IncludeAll(self):
		"""Include All

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAll')

	@property
	def IncludeAny(self):
		"""Include Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAny')

	@property
	def IncludeSrp(self):
		"""Indicates whether SRP object will be included in a PCInitiate message. All other attributes in sub-tab-SRP would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSrp')

	@property
	def IncludeSymbolicPathName(self):
		"""Indicates if Symbolic-Path-Name TLV is to be included in PCUpate trigger message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSymbolicPathName')

	@property
	def IncludeTEPathBindingTLVTriggerParam(self):
		"""Indicates if TE-PATH-BINDING TLV is to be included in PCUpate trigger message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeTEPathBindingTLVTriggerParam')

	@property
	def LocalProtection(self):
		"""Local Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

	@property
	def Mpls_label_20_TriggerParam(self):
		"""This control will be editable if the Binding Type is set to either 20bit or 32bit MPLS-Label. This field will take the 20bit value of the MPLS-Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mpls_label_20_TriggerParam')

	@property
	def NumberOfEroSubObjects(self):
		"""Value that indicates the number of ERO Sub Objects to be configured.

		Returns:
			number
		"""
		return self._get_attribute('numberOfEroSubObjects')
	@NumberOfEroSubObjects.setter
	def NumberOfEroSubObjects(self, value):
		self._set_attribute('numberOfEroSubObjects', value)

	@property
	def NumberOfMetricSubObjects(self):
		"""Value that indicates the number of Metric Objects to be configured.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMetricSubObjects')
	@NumberOfMetricSubObjects.setter
	def NumberOfMetricSubObjects(self, value):
		self._set_attribute('numberOfMetricSubObjects', value)

	@property
	def OverrideSrpId(self):
		"""Indicates whether SRP object will be included in a PCUpdate trigger parameters. All other attributes in sub-tab-SRP would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overrideSrpId')

	@property
	def PceTriggersChoiceList(self):
		"""Based on options selected, IxNetwork sends information to PCPU and refreshes the statistical data in the corresponding tab of Learned Information

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pceTriggersChoiceList')

	@property
	def SendEmptyTLVTriggerParam(self):
		"""If enabled all fields after Binding Type will be grayed out.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendEmptyTLVTriggerParam')

	@property
	def SetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SrpId(self):
		"""The SRP object is used to correlate between initiation requests sent by the PCE and the error reports and state reports sent by the PCC. This number is unique per PCEP session and is incremented per initiation.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srpId')

	@property
	def Tos_TriggerParam(self):
		"""This field is used to carry traffic class information. This control will be editable only if Binding Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tos_TriggerParam')

	@property
	def Ttl_TriggerParam(self):
		"""This field is used to encode a time-to-live value. This control will be editable only if Binding Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ttl_TriggerParam')

	def find(self, NumberOfEroSubObjects=None, NumberOfMetricSubObjects=None):
		"""Finds and retrieves pceBasicSrSyncLspUpdateParams data from the server.

		All named parameters support regex and can be used to selectively retrieve pceBasicSrSyncLspUpdateParams data from the server.
		By default the find method takes no parameters and will retrieve all pceBasicSrSyncLspUpdateParams data from the server.

		Args:
			NumberOfEroSubObjects (number): Value that indicates the number of ERO Sub Objects to be configured.
			NumberOfMetricSubObjects (number): Value that indicates the number of Metric Objects to be configured.

		Returns:
			self: This instance with matching pceBasicSrSyncLspUpdateParams data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceBasicSrSyncLspUpdateParams data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceBasicSrSyncLspUpdateParams data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SendPcUpdate(self, Arg2):
		"""Executes the sendPcUpdate operation on the server.

		Counts property changes created by the user.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the learned information corresponding to trigger data.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPcUpdate', payload=locals(), response_object=None)
