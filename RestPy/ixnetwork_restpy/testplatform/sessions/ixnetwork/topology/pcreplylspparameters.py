
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


class PcReplyLspParameters(Base):
	"""The PcReplyLspParameters class encapsulates a required pcReplyLspParameters node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PcReplyLspParameters property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pcReplyLspParameters'

	def __init__(self, parent):
		super(PcReplyLspParameters, self).__init__(parent)

	@property
	def PceXroSubObjectsList(self):
		"""An instance of the PceXroSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcexrosubobjectslist.PceXroSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcexrosubobjectslist import PceXroSubObjectsList
		return PceXroSubObjectsList(self)

	@property
	def PcepEroSubObjectsList(self):
		"""An instance of the PcepEroSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceperosubobjectslist.PcepEroSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceperosubobjectslist import PcepEroSubObjectsList
		return PcepEroSubObjectsList(self)

	@property
	def PcepMetricSubObjectsList(self):
		"""An instance of the PcepMetricSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepmetricsubobjectslist.PcepMetricSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepmetricsubobjectslist import PcepMetricSubObjectsList
		return PcepMetricSubObjectsList(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Bandwidth(self):
		"""Bandwidth (bits/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

	@property
	def BiDirectional(self):
		"""Bi-directional

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('biDirectional')

	@property
	def BindingType(self):
		"""Indicates the type of binding included in the TLV. Types are as follows: 20bit MPLS Label 32bit MPLS Label. Default value is 20bit MPLS Label.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bindingType')

	@property
	def Bos(self):
		"""This bit is set to true for the last entry in the label stack i.e., for the bottom of the stack, and false for all other label stack entries. This control will be editable only if Binding Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bos')

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
	def EnableCFlag(self):
		"""C Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableCFlag')

	@property
	def EnableEro(self):
		"""Include ERO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableEro')

	@property
	def EnableLoose(self):
		"""Loose

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLoose')

	@property
	def EnableXro(self):
		"""Include XRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableXro')

	@property
	def ExcludeAny(self):
		"""Exclude Any

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

	@property
	def FailBit(self):
		"""Fail Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('failBit')

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
	def IncludeBandwidth(self):
		"""Include Bandwidth

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeBandwidth')

	@property
	def IncludeLsp(self):
		"""Include LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLsp')

	@property
	def IncludeLspa(self):
		"""Include LSPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLspa')

	@property
	def IncludeMetric(self):
		"""Include Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMetric')

	@property
	def IncludeRp(self):
		"""Include RP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeRp')

	@property
	def IncludeSymbolicPathNameTlv(self):
		"""Indicates if Symbolic-Path-Name TLV is to be included in PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSymbolicPathNameTlv')

	@property
	def IncludeTEPathBindingTLV(self):
		"""Indicates if TE-PATH-BINDING TLV is to be included in PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeTEPathBindingTLV')

	@property
	def LocalProtection(self):
		"""Local Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

	@property
	def MplsLabel(self):
		"""This control will be editable if the Binding Type is set to either 20bit or 32bit MPLS-Label. This field will take the 20bit value of the MPLS-Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mplsLabel')

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
	def NatureOfIssue(self):
		"""Nature Of Issue

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('natureOfIssue')

	@property
	def NumberOfEroSubObjects(self):
		"""Number of ERO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfEroSubObjects')
	@NumberOfEroSubObjects.setter
	def NumberOfEroSubObjects(self, value):
		self._set_attribute('numberOfEroSubObjects', value)

	@property
	def NumberOfMetricSubObject(self):
		"""Number of Metric

		Returns:
			number
		"""
		return self._get_attribute('numberOfMetricSubObject')
	@NumberOfMetricSubObject.setter
	def NumberOfMetricSubObject(self, value):
		self._set_attribute('numberOfMetricSubObject', value)

	@property
	def NumberOfXroSubObjects(self):
		"""Number of XRO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfXroSubObjects')
	@NumberOfXroSubObjects.setter
	def NumberOfXroSubObjects(self, value):
		self._set_attribute('numberOfXroSubObjects', value)

	@property
	def PlspId(self):
		"""An identifier for the LSP. A PCC creates a unique PLSP-ID for each LSP that is constant for the lifetime of a PCEP session. The PCC will advertise the same PLSP-ID on all PCEP sessions it maintains at a given time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('plspId')

	@property
	def PriorityValue(self):
		"""Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priorityValue')

	@property
	def ProcessType(self):
		"""Indicates how the XRO is responded in the Path Request Response.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('processType')

	@property
	def ReceivedPLSPID(self):
		"""Received PLSP-ID in PcRequest

		Returns:
			list(number)
		"""
		return self._get_attribute('receivedPLSPID')

	@property
	def ReceivedSymbolicPath(self):
		"""Received Symbolic Path Name in PcRequest

		Returns:
			list(str)
		"""
		return self._get_attribute('receivedSymbolicPath')

	@property
	def ReflectLSP(self):
		"""Reflect LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectLSP')

	@property
	def ReflectRP(self):
		"""Reflect RP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectRP')

	@property
	def ReflectedObjectNoPath(self):
		"""Reflected Object

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectedObjectNoPath')

	@property
	def RequestId(self):
		"""Request ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('requestId')

	@property
	def ResponseOptions(self):
		"""Reply Options

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('responseOptions')

	@property
	def ResponsePathType(self):
		"""Indicates which type of LSP will be responsed in the Path Request Response.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('responsePathType')

	@property
	def SendEmptyTLV(self):
		"""If enabled all fields after Binding Type will be grayed out.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendEmptyTLV')

	@property
	def SessionInfo(self):
		"""Logs additional information about the LSP state

		Returns:
			list(str[delegatedActive|delegatedDown|delegatedGoingUp|delegatedUp|noLSPObjectInPCRequest|none|notDelegatedActive|notDelegatedDown|notDelegatedGoingUp|notDelegatedUp|pcErrorReceived|removedByPCC|replySentReportNotReceived])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SetupPriority(self):
		"""Setup Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SymbolicPathName(self):
		"""Each LSP (path) must have a symbolic name that is unique in the PCC. It must remain constant throughout a path's lifetime, which may span across multiple consecutive PCEP sessions and/or PCC restarts.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('symbolicPathName')

	@property
	def Tc(self):
		"""This field is used to carry traffic class information. This control will be editable only if Binding Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tc')

	@property
	def Ttl(self):
		"""This field is used to encode a time-to-live value. This control will be editable only if Binding Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ttl')

	def ReturnDelegation(self):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Replied LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReturnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, SessionIndices):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Replied LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReturnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, SessionIndices):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Replied LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReturnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg2):
		"""Executes the returnDelegation operation on the server.

		Return Delegation helps PCE to return a delegation of LSP/LSPs.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): Return Delegation.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ReturnDelegation', payload=locals(), response_object=None)
