
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


class IsisSpbRouter(Base):
	"""The IsisSpbRouter class encapsulates a user managed isisSpbRouter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IsisSpbRouter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'isisSpbRouter'

	def __init__(self, parent):
		super(IsisSpbRouter, self).__init__(parent)

	@property
	def SpbTopologyList(self):
		"""An instance of the SpbTopologyList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbtopologylist.SpbTopologyList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbtopologylist import SpbTopologyList
		return SpbTopologyList(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AreaAddresses(self):
		"""Area Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaAddresses')

	@property
	def AreaAuthenticationType(self):
		"""Area Authentication Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaAuthenticationType')

	@property
	def AreaTransmitPasswordOrMD5Key(self):
		"""Area Transmit Password / MD5-Key

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('areaTransmitPasswordOrMD5Key')

	@property
	def Attached(self):
		"""Attached

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('attached')

	@property
	def CSNPInterval(self):
		"""CSNP Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cSNPInterval')

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
	def DiscardLSPs(self):
		"""Discard LSPs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardLSPs')

	@property
	def EnableHelloPadding(self):
		"""Enable Hello Padding

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHelloPadding')

	@property
	def EnableHitlessRestart(self):
		"""Enable Hitless Restart

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHitlessRestart')

	@property
	def EnableHostName(self):
		"""Enable Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHostName')

	@property
	def EnableWideMetric(self):
		"""Enable Wide Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableWideMetric')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def HitlessRestartMode(self):
		"""Restart Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hitlessRestartMode')

	@property
	def HitlessRestartTime(self):
		"""Restart Time

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hitlessRestartTime')

	@property
	def HitlessRestartVersion(self):
		"""Restart Version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hitlessRestartVersion')

	@property
	def HostName(self):
		"""Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostName')

	@property
	def IgnoreMTPortCapability(self):
		"""Ignore MT Port Capability

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignoreMTPortCapability')

	@property
	def IgnoreReceiveMD5(self):
		"""Ignore Receive MD5

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignoreReceiveMD5')

	@property
	def InterLSPsOrMGroupPDUBurstGap(self):
		"""Inter LSPs/MGROUP-PDUs Burst Gap (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interLSPsOrMGroupPDUBurstGap')

	@property
	def LSPLifetime(self):
		"""LSP Rifetime (sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPLifetime')

	@property
	def LSPRefreshRate(self):
		"""LSP Refresh Rate (sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPRefreshRate')

	@property
	def LSPorMGroupPDUMinTransmissionInterval(self):
		"""LSP/MGROUP-PDU Min Transmission Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPorMGroupPDUMinTransmissionInterval')

	@property
	def LocalSystemID(self):
		"""System ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localSystemID')

	@property
	def MaxAreaAddresses(self):
		"""Maximum Area Addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxAreaAddresses')

	@property
	def MaxLSPSize(self):
		"""Max LSP Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLSPSize')

	@property
	def MaxLSPsOrMGroupPDUsPerBurst(self):
		"""Max LSPs/MGROUP-PDUs Per Burst

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLSPsOrMGroupPDUsPerBurst')

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
	def Overloaded(self):
		"""Overloaded

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('overloaded')

	@property
	def PSNPInterval(self):
		"""PSNP Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pSNPInterval')

	@property
	def PartitionRepair(self):
		"""Partition Repair

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('partitionRepair')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session Information

		Returns:
			list(str[noIfaceUp|up])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SpbTopologyCount(self):
		"""Topology Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('spbTopologyCount')
	@SpbTopologyCount.setter
	def SpbTopologyCount(self, value):
		self._set_attribute('spbTopologyCount', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	def add(self, Name=None, SpbTopologyCount=None):
		"""Adds a new isisSpbRouter node on the server and retrieves it in this instance.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SpbTopologyCount (number): Topology Count(multiplier)

		Returns:
			self: This instance with all currently retrieved isisSpbRouter data using find and the newly added isisSpbRouter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the isisSpbRouter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, DescriptiveName=None, Errors=None, LocalSystemID=None, Name=None, SessionInfo=None, SessionStatus=None, SpbTopologyCount=None, StateCounts=None, Status=None):
		"""Finds and retrieves isisSpbRouter data from the server.

		All named parameters support regex and can be used to selectively retrieve isisSpbRouter data from the server.
		By default the find method takes no parameters and will retrieve all isisSpbRouter data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			LocalSystemID (list(str)): System ID
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SessionInfo (list(str[noIfaceUp|up])): Logs additional information about the session Information
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			SpbTopologyCount (number): Topology Count(multiplier)
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching isisSpbRouter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of isisSpbRouter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the isisSpbRouter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, Active=None, AreaAddresses=None, AreaAuthenticationType=None, AreaTransmitPasswordOrMD5Key=None, Attached=None, CSNPInterval=None, DiscardLSPs=None, EnableHelloPadding=None, EnableHitlessRestart=None, EnableHostName=None, EnableWideMetric=None, HitlessRestartMode=None, HitlessRestartTime=None, HitlessRestartVersion=None, HostName=None, IgnoreMTPortCapability=None, IgnoreReceiveMD5=None, InterLSPsOrMGroupPDUBurstGap=None, LSPLifetime=None, LSPRefreshRate=None, LSPorMGroupPDUMinTransmissionInterval=None, MaxAreaAddresses=None, MaxLSPSize=None, MaxLSPsOrMGroupPDUsPerBurst=None, Overloaded=None, PSNPInterval=None, PartitionRepair=None):
		"""Base class infrastructure that gets a list of isisSpbRouter device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AreaAddresses (str): optional regex of areaAddresses
			AreaAuthenticationType (str): optional regex of areaAuthenticationType
			AreaTransmitPasswordOrMD5Key (str): optional regex of areaTransmitPasswordOrMD5Key
			Attached (str): optional regex of attached
			CSNPInterval (str): optional regex of cSNPInterval
			DiscardLSPs (str): optional regex of discardLSPs
			EnableHelloPadding (str): optional regex of enableHelloPadding
			EnableHitlessRestart (str): optional regex of enableHitlessRestart
			EnableHostName (str): optional regex of enableHostName
			EnableWideMetric (str): optional regex of enableWideMetric
			HitlessRestartMode (str): optional regex of hitlessRestartMode
			HitlessRestartTime (str): optional regex of hitlessRestartTime
			HitlessRestartVersion (str): optional regex of hitlessRestartVersion
			HostName (str): optional regex of hostName
			IgnoreMTPortCapability (str): optional regex of ignoreMTPortCapability
			IgnoreReceiveMD5 (str): optional regex of ignoreReceiveMD5
			InterLSPsOrMGroupPDUBurstGap (str): optional regex of interLSPsOrMGroupPDUBurstGap
			LSPLifetime (str): optional regex of lSPLifetime
			LSPRefreshRate (str): optional regex of lSPRefreshRate
			LSPorMGroupPDUMinTransmissionInterval (str): optional regex of lSPorMGroupPDUMinTransmissionInterval
			MaxAreaAddresses (str): optional regex of maxAreaAddresses
			MaxLSPSize (str): optional regex of maxLSPSize
			MaxLSPsOrMGroupPDUsPerBurst (str): optional regex of maxLSPsOrMGroupPDUsPerBurst
			Overloaded (str): optional regex of overloaded
			PSNPInterval (str): optional regex of pSNPInterval
			PartitionRepair (str): optional regex of partitionRepair

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def IsisStartRouter(self):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStartRouter', payload=locals(), response_object=None)

	def IsisStartRouter(self, SessionIndices):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStartRouter', payload=locals(), response_object=None)

	def IsisStartRouter(self, SessionIndices):
		"""Executes the isisStartRouter operation on the server.

		Start ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStartRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStopRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, SessionIndices):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStopRouter', payload=locals(), response_object=None)

	def IsisStopRouter(self, SessionIndices):
		"""Executes the isisStopRouter operation on the server.

		Stop ISIS Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IsisStopRouter', payload=locals(), response_object=None)

	def RestartDown(self):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def RestartDown(self, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
