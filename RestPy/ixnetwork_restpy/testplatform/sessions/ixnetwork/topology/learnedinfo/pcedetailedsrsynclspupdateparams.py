
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceDetailedSrSyncLspUpdateParams(Base):
	"""The PceDetailedSrSyncLspUpdateParams class encapsulates a system managed pceDetailedSrSyncLspUpdateParams node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceDetailedSrSyncLspUpdateParams property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceDetailedSrSyncLspUpdateParams'

	def __init__(self, parent):
		super(PceDetailedSrSyncLspUpdateParams, self).__init__(parent)

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
	def LocalProtection(self):
		"""Local Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

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

	def find(self, NumberOfEroSubObjects=None, NumberOfMetricSubObjects=None):
		"""Finds and retrieves pceDetailedSrSyncLspUpdateParams data from the server.

		All named parameters support regex and can be used to selectively retrieve pceDetailedSrSyncLspUpdateParams data from the server.
		By default the find method takes no parameters and will retrieve all pceDetailedSrSyncLspUpdateParams data from the server.

		Args:
			NumberOfEroSubObjects (number): Value that indicates the number of ERO Sub Objects to be configured.
			NumberOfMetricSubObjects (number): Value that indicates the number of Metric Objects to be configured.

		Returns:
			self: This instance with matching pceDetailedSrSyncLspUpdateParams data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceDetailedSrSyncLspUpdateParams data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceDetailedSrSyncLspUpdateParams data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, Bandwidth=None, ConfigureBandwidth=None, ConfigureEro=None, ConfigureLsp=None, ConfigureLspa=None, ConfigureMetric=None, ExcludeAny=None, HoldingPriority=None, IncludeAll=None, IncludeAny=None, IncludeSrp=None, IncludeSymbolicPathName=None, LocalProtection=None, OverrideSrpId=None, PceTriggersChoiceList=None, SetupPriority=None, SrpId=None):
		"""Base class infrastructure that gets a list of pceDetailedSrSyncLspUpdateParams device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Bandwidth (str): optional regex of bandwidth
			ConfigureBandwidth (str): optional regex of configureBandwidth
			ConfigureEro (str): optional regex of configureEro
			ConfigureLsp (str): optional regex of configureLsp
			ConfigureLspa (str): optional regex of configureLspa
			ConfigureMetric (str): optional regex of configureMetric
			ExcludeAny (str): optional regex of excludeAny
			HoldingPriority (str): optional regex of holdingPriority
			IncludeAll (str): optional regex of includeAll
			IncludeAny (str): optional regex of includeAny
			IncludeSrp (str): optional regex of includeSrp
			IncludeSymbolicPathName (str): optional regex of includeSymbolicPathName
			LocalProtection (str): optional regex of localProtection
			OverrideSrpId (str): optional regex of overrideSrpId
			PceTriggersChoiceList (str): optional regex of pceTriggersChoiceList
			SetupPriority (str): optional regex of setupPriority
			SrpId (str): optional regex of srpId

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def SendPcUpdate(self, Arg2):
		"""Executes the sendPcUpdate operation on the server.

		Counts property changes created by the user.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the learned information corresponding to trigger data.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPcUpdate', payload=locals(), response_object=None)
