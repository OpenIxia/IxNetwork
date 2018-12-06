
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


class Link(Base):
	"""The Link class encapsulates a user managed link node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Link property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'link'

	def __init__(self, parent):
		super(Link, self).__init__(parent)

	@property
	def DiscoveredLearnedInfo(self):
		"""An instance of the DiscoveredLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.discoveredlearnedinfo.discoveredlearnedinfo.DiscoveredLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.discoveredlearnedinfo.discoveredlearnedinfo import DiscoveredLearnedInfo
		return DiscoveredLearnedInfo(self)

	@property
	def ErroredFramePeriodTlv(self):
		"""An instance of the ErroredFramePeriodTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredframeperiodtlv.erroredframeperiodtlv.ErroredFramePeriodTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredframeperiodtlv.erroredframeperiodtlv import ErroredFramePeriodTlv
		return ErroredFramePeriodTlv(self)._select()

	@property
	def ErroredFrameSecondsSummaryTlv(self):
		"""An instance of the ErroredFrameSecondsSummaryTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredframesecondssummarytlv.erroredframesecondssummarytlv.ErroredFrameSecondsSummaryTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredframesecondssummarytlv.erroredframesecondssummarytlv import ErroredFrameSecondsSummaryTlv
		return ErroredFrameSecondsSummaryTlv(self)._select()

	@property
	def ErroredFrameTlv(self):
		"""An instance of the ErroredFrameTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredframetlv.erroredframetlv.ErroredFrameTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredframetlv.erroredframetlv import ErroredFrameTlv
		return ErroredFrameTlv(self)._select()

	@property
	def ErroredSymbolPeriodTlv(self):
		"""An instance of the ErroredSymbolPeriodTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredsymbolperiodtlv.erroredsymbolperiodtlv.ErroredSymbolPeriodTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.erroredsymbolperiodtlv.erroredsymbolperiodtlv import ErroredSymbolPeriodTlv
		return ErroredSymbolPeriodTlv(self)._select()

	@property
	def EventNotificationLearnedInfo(self):
		"""An instance of the EventNotificationLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.eventnotificationlearnedinfo.eventnotificationlearnedinfo.EventNotificationLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.eventnotificationlearnedinfo.eventnotificationlearnedinfo import EventNotificationLearnedInfo
		return EventNotificationLearnedInfo(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.interface.interface import Interface
		return Interface(self)

	@property
	def OrganizationSpecificEventTlv(self):
		"""An instance of the OrganizationSpecificEventTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.organizationspecificeventtlv.organizationspecificeventtlv.OrganizationSpecificEventTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.organizationspecificeventtlv.organizationspecificeventtlv import OrganizationSpecificEventTlv
		return OrganizationSpecificEventTlv(self)._select()

	@property
	def OrganizationSpecificInfoTlv(self):
		"""An instance of the OrganizationSpecificInfoTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.organizationspecificinfotlv.organizationspecificinfotlv.OrganizationSpecificInfoTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.organizationspecificinfotlv.organizationspecificinfotlv import OrganizationSpecificInfoTlv
		return OrganizationSpecificInfoTlv(self)

	@property
	def OrganizationSpecificOamPduData(self):
		"""An instance of the OrganizationSpecificOamPduData class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.organizationspecificoampdudata.organizationspecificoampdudata.OrganizationSpecificOamPduData)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.organizationspecificoampdudata.organizationspecificoampdudata import OrganizationSpecificOamPduData
		return OrganizationSpecificOamPduData(self)

	@property
	def VarDescriptor(self):
		"""An instance of the VarDescriptor class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.vardescriptor.vardescriptor.VarDescriptor)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.vardescriptor.vardescriptor import VarDescriptor
		return VarDescriptor(self)

	@property
	def VariableRequestLearnedInfo(self):
		"""An instance of the VariableRequestLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.variablerequestlearnedinfo.variablerequestlearnedinfo.VariableRequestLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.variablerequestlearnedinfo.variablerequestlearnedinfo import VariableRequestLearnedInfo
		return VariableRequestLearnedInfo(self)

	@property
	def VariableResponseDatabase(self):
		"""An instance of the VariableResponseDatabase class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.variableresponsedatabase.variableresponsedatabase.VariableResponseDatabase)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.variableresponsedatabase.variableresponsedatabase import VariableResponseDatabase
		return VariableResponseDatabase(self)

	@property
	def DisableInformationPduTx(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('disableInformationPduTx')
	@DisableInformationPduTx.setter
	def DisableInformationPduTx(self, value):
		self._set_attribute('disableInformationPduTx', value)

	@property
	def DisableNonInformationPduTx(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('disableNonInformationPduTx')
	@DisableNonInformationPduTx.setter
	def DisableNonInformationPduTx(self, value):
		self._set_attribute('disableNonInformationPduTx', value)

	@property
	def EnableCriticalEvent(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCriticalEvent')
	@EnableCriticalEvent.setter
	def EnableCriticalEvent(self, value):
		self._set_attribute('enableCriticalEvent', value)

	@property
	def EnableDyingGasp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDyingGasp')
	@EnableDyingGasp.setter
	def EnableDyingGasp(self, value):
		self._set_attribute('enableDyingGasp', value)

	@property
	def EnableLinkFault(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLinkFault')
	@EnableLinkFault.setter
	def EnableLinkFault(self, value):
		self._set_attribute('enableLinkFault', value)

	@property
	def EnableLoopbackResponse(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLoopbackResponse')
	@EnableLoopbackResponse.setter
	def EnableLoopbackResponse(self, value):
		self._set_attribute('enableLoopbackResponse', value)

	@property
	def EnableVariableResponse(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVariableResponse')
	@EnableVariableResponse.setter
	def EnableVariableResponse(self, value):
		self._set_attribute('enableVariableResponse', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EthernetTypeUsedForDataTraffic(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ethernetTypeUsedForDataTraffic')
	@EthernetTypeUsedForDataTraffic.setter
	def EthernetTypeUsedForDataTraffic(self, value):
		self._set_attribute('ethernetTypeUsedForDataTraffic', value)

	@property
	def EventInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('eventInterval')
	@EventInterval.setter
	def EventInterval(self, value):
		self._set_attribute('eventInterval', value)

	@property
	def InformationPduCountPerSecond(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('informationPduCountPerSecond')
	@InformationPduCountPerSecond.setter
	def InformationPduCountPerSecond(self, value):
		self._set_attribute('informationPduCountPerSecond', value)

	@property
	def IsDiscLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDiscLearnedInfoRefreshed')

	@property
	def IsEventNotificationLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isEventNotificationLearnedInfoRefreshed')

	@property
	def IsLoopbackLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLoopbackLearnedInfoRefreshed')

	@property
	def IsVariableRequestLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isVariableRequestLearnedInfoRefreshed')

	@property
	def LinkEventTxMode(self):
		"""

		Returns:
			str(single|periodic)
		"""
		return self._get_attribute('linkEventTxMode')
	@LinkEventTxMode.setter
	def LinkEventTxMode(self, value):
		self._set_attribute('linkEventTxMode', value)

	@property
	def LocalLostLinkTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localLostLinkTimer')
	@LocalLostLinkTimer.setter
	def LocalLostLinkTimer(self, value):
		self._set_attribute('localLostLinkTimer', value)

	@property
	def LoopbackCmd(self):
		"""

		Returns:
			str(disableLoopback|enableLoopback)
		"""
		return self._get_attribute('loopbackCmd')
	@LoopbackCmd.setter
	def LoopbackCmd(self, value):
		self._set_attribute('loopbackCmd', value)

	@property
	def LoopbackTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('loopbackTimeout')
	@LoopbackTimeout.setter
	def LoopbackTimeout(self, value):
		self._set_attribute('loopbackTimeout', value)

	@property
	def MacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MaxOamPduSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxOamPduSize')
	@MaxOamPduSize.setter
	def MaxOamPduSize(self, value):
		self._set_attribute('maxOamPduSize', value)

	@property
	def OperationMode(self):
		"""

		Returns:
			str(active|passive)
		"""
		return self._get_attribute('operationMode')
	@OperationMode.setter
	def OperationMode(self, value):
		self._set_attribute('operationMode', value)

	@property
	def Oui(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('oui')
	@Oui.setter
	def Oui(self, value):
		self._set_attribute('oui', value)

	@property
	def OverrideLocalEvaluating(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideLocalEvaluating')
	@OverrideLocalEvaluating.setter
	def OverrideLocalEvaluating(self, value):
		self._set_attribute('overrideLocalEvaluating', value)

	@property
	def OverrideLocalSatisfied(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideLocalSatisfied')
	@OverrideLocalSatisfied.setter
	def OverrideLocalSatisfied(self, value):
		self._set_attribute('overrideLocalSatisfied', value)

	@property
	def OverrideLocalStable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideLocalStable')
	@OverrideLocalStable.setter
	def OverrideLocalStable(self, value):
		self._set_attribute('overrideLocalStable', value)

	@property
	def OverrideRemoteEvaluating(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideRemoteEvaluating')
	@OverrideRemoteEvaluating.setter
	def OverrideRemoteEvaluating(self, value):
		self._set_attribute('overrideRemoteEvaluating', value)

	@property
	def OverrideRemoteStable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideRemoteStable')
	@OverrideRemoteStable.setter
	def OverrideRemoteStable(self, value):
		self._set_attribute('overrideRemoteStable', value)

	@property
	def OverrideRevision(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideRevision')
	@OverrideRevision.setter
	def OverrideRevision(self, value):
		self._set_attribute('overrideRevision', value)

	@property
	def OverrideSequenceNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideSequenceNumber')
	@OverrideSequenceNumber.setter
	def OverrideSequenceNumber(self, value):
		self._set_attribute('overrideSequenceNumber', value)

	@property
	def Revision(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('revision')
	@Revision.setter
	def Revision(self, value):
		self._set_attribute('revision', value)

	@property
	def SequenceNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sequenceNumber')
	@SequenceNumber.setter
	def SequenceNumber(self, value):
		self._set_attribute('sequenceNumber', value)

	@property
	def SupportsInterpretingLinkEvents(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsInterpretingLinkEvents')
	@SupportsInterpretingLinkEvents.setter
	def SupportsInterpretingLinkEvents(self, value):
		self._set_attribute('supportsInterpretingLinkEvents', value)

	@property
	def SupportsRemoteLoopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsRemoteLoopback')
	@SupportsRemoteLoopback.setter
	def SupportsRemoteLoopback(self, value):
		self._set_attribute('supportsRemoteLoopback', value)

	@property
	def SupportsUnidirectionalMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsUnidirectionalMode')
	@SupportsUnidirectionalMode.setter
	def SupportsUnidirectionalMode(self, value):
		self._set_attribute('supportsUnidirectionalMode', value)

	@property
	def SupportsVariableRetrieval(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportsVariableRetrieval')
	@SupportsVariableRetrieval.setter
	def SupportsVariableRetrieval(self, value):
		self._set_attribute('supportsVariableRetrieval', value)

	@property
	def UpdateRequired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('updateRequired')

	@property
	def VariableResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('variableResponseTimeout')
	@VariableResponseTimeout.setter
	def VariableResponseTimeout(self, value):
		self._set_attribute('variableResponseTimeout', value)

	@property
	def VendorSpecificInformation(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vendorSpecificInformation')
	@VendorSpecificInformation.setter
	def VendorSpecificInformation(self, value):
		self._set_attribute('vendorSpecificInformation', value)

	@property
	def Version(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, DisableInformationPduTx=None, DisableNonInformationPduTx=None, EnableCriticalEvent=None, EnableDyingGasp=None, EnableLinkFault=None, EnableLoopbackResponse=None, EnableVariableResponse=None, Enabled=None, EthernetTypeUsedForDataTraffic=None, EventInterval=None, InformationPduCountPerSecond=None, LinkEventTxMode=None, LocalLostLinkTimer=None, LoopbackCmd=None, LoopbackTimeout=None, MacAddress=None, MaxOamPduSize=None, OperationMode=None, Oui=None, OverrideLocalEvaluating=None, OverrideLocalSatisfied=None, OverrideLocalStable=None, OverrideRemoteEvaluating=None, OverrideRemoteStable=None, OverrideRevision=None, OverrideSequenceNumber=None, Revision=None, SequenceNumber=None, SupportsInterpretingLinkEvents=None, SupportsRemoteLoopback=None, SupportsUnidirectionalMode=None, SupportsVariableRetrieval=None, VariableResponseTimeout=None, VendorSpecificInformation=None, Version=None):
		"""Adds a new link node on the server and retrieves it in this instance.

		Args:
			DisableInformationPduTx (bool): 
			DisableNonInformationPduTx (bool): 
			EnableCriticalEvent (bool): 
			EnableDyingGasp (bool): 
			EnableLinkFault (bool): 
			EnableLoopbackResponse (bool): 
			EnableVariableResponse (bool): 
			Enabled (bool): 
			EthernetTypeUsedForDataTraffic (number): 
			EventInterval (number): 
			InformationPduCountPerSecond (number): 
			LinkEventTxMode (str(single|periodic)): 
			LocalLostLinkTimer (number): 
			LoopbackCmd (str(disableLoopback|enableLoopback)): 
			LoopbackTimeout (number): 
			MacAddress (str): 
			MaxOamPduSize (number): 
			OperationMode (str(active|passive)): 
			Oui (str): 
			OverrideLocalEvaluating (bool): 
			OverrideLocalSatisfied (bool): 
			OverrideLocalStable (bool): 
			OverrideRemoteEvaluating (bool): 
			OverrideRemoteStable (bool): 
			OverrideRevision (bool): 
			OverrideSequenceNumber (bool): 
			Revision (number): 
			SequenceNumber (number): 
			SupportsInterpretingLinkEvents (bool): 
			SupportsRemoteLoopback (bool): 
			SupportsUnidirectionalMode (bool): 
			SupportsVariableRetrieval (bool): 
			VariableResponseTimeout (number): 
			VendorSpecificInformation (str): 
			Version (number): 

		Returns:
			self: This instance with all currently retrieved link data using find and the newly added link data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the link data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DisableInformationPduTx=None, DisableNonInformationPduTx=None, EnableCriticalEvent=None, EnableDyingGasp=None, EnableLinkFault=None, EnableLoopbackResponse=None, EnableVariableResponse=None, Enabled=None, EthernetTypeUsedForDataTraffic=None, EventInterval=None, InformationPduCountPerSecond=None, IsDiscLearnedInfoRefreshed=None, IsEventNotificationLearnedInfoRefreshed=None, IsLoopbackLearnedInfoRefreshed=None, IsVariableRequestLearnedInfoRefreshed=None, LinkEventTxMode=None, LocalLostLinkTimer=None, LoopbackCmd=None, LoopbackTimeout=None, MacAddress=None, MaxOamPduSize=None, OperationMode=None, Oui=None, OverrideLocalEvaluating=None, OverrideLocalSatisfied=None, OverrideLocalStable=None, OverrideRemoteEvaluating=None, OverrideRemoteStable=None, OverrideRevision=None, OverrideSequenceNumber=None, Revision=None, SequenceNumber=None, SupportsInterpretingLinkEvents=None, SupportsRemoteLoopback=None, SupportsUnidirectionalMode=None, SupportsVariableRetrieval=None, UpdateRequired=None, VariableResponseTimeout=None, VendorSpecificInformation=None, Version=None):
		"""Finds and retrieves link data from the server.

		All named parameters support regex and can be used to selectively retrieve link data from the server.
		By default the find method takes no parameters and will retrieve all link data from the server.

		Args:
			DisableInformationPduTx (bool): 
			DisableNonInformationPduTx (bool): 
			EnableCriticalEvent (bool): 
			EnableDyingGasp (bool): 
			EnableLinkFault (bool): 
			EnableLoopbackResponse (bool): 
			EnableVariableResponse (bool): 
			Enabled (bool): 
			EthernetTypeUsedForDataTraffic (number): 
			EventInterval (number): 
			InformationPduCountPerSecond (number): 
			IsDiscLearnedInfoRefreshed (bool): 
			IsEventNotificationLearnedInfoRefreshed (bool): 
			IsLoopbackLearnedInfoRefreshed (bool): 
			IsVariableRequestLearnedInfoRefreshed (bool): 
			LinkEventTxMode (str(single|periodic)): 
			LocalLostLinkTimer (number): 
			LoopbackCmd (str(disableLoopback|enableLoopback)): 
			LoopbackTimeout (number): 
			MacAddress (str): 
			MaxOamPduSize (number): 
			OperationMode (str(active|passive)): 
			Oui (str): 
			OverrideLocalEvaluating (bool): 
			OverrideLocalSatisfied (bool): 
			OverrideLocalStable (bool): 
			OverrideRemoteEvaluating (bool): 
			OverrideRemoteStable (bool): 
			OverrideRevision (bool): 
			OverrideSequenceNumber (bool): 
			Revision (number): 
			SequenceNumber (number): 
			SupportsInterpretingLinkEvents (bool): 
			SupportsRemoteLoopback (bool): 
			SupportsUnidirectionalMode (bool): 
			SupportsVariableRetrieval (bool): 
			UpdateRequired (bool): 
			VariableResponseTimeout (number): 
			VendorSpecificInformation (str): 
			Version (number): 

		Returns:
			self: This instance with matching link data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of link data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the link data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshDiscLearnedInfo(self):
		"""Executes the refreshDiscLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshDiscLearnedInfo', payload=locals(), response_object=None)

	def RefreshEventNotificationLearnedInfo(self):
		"""Executes the refreshEventNotificationLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshEventNotificationLearnedInfo', payload=locals(), response_object=None)

	def RestartDiscovery(self):
		"""Executes the restartDiscovery operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RestartDiscovery', payload=locals(), response_object=None)

	def SendLoopback(self):
		"""Executes the sendLoopback operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendLoopback', payload=locals(), response_object=None)

	def SendOrgSpecificPdu(self):
		"""Executes the sendOrgSpecificPdu operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendOrgSpecificPdu', payload=locals(), response_object=None)

	def SendUpdatedParameters(self):
		"""Executes the sendUpdatedParameters operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendUpdatedParameters', payload=locals(), response_object=None)

	def SendVariableRequest(self):
		"""Executes the sendVariableRequest operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendVariableRequest', payload=locals(), response_object=None)

	def StartEventPduTransmission(self):
		"""Executes the startEventPduTransmission operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartEventPduTransmission', payload=locals(), response_object=None)

	def StopEventPduTransmission(self):
		"""Executes the stopEventPduTransmission operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=link)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StopEventPduTransmission', payload=locals(), response_object=None)
