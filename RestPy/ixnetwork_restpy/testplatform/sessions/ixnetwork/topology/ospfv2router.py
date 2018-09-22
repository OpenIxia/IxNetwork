from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ospfv2Router(Base):
	"""The Ospfv2Router class encapsulates a system managed ospfv2Router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ospfv2Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ospfv2Router'

	def __init__(self, parent):
		super(Ospfv2Router, self).__init__(parent)

	@property
	def OspfBierSubDomainList(self):
		"""An instance of the OspfBierSubDomainList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfbiersubdomainlist.OspfBierSubDomainList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfbiersubdomainlist import OspfBierSubDomainList
		return OspfBierSubDomainList(self)._select()

	@property
	def OspfSRAlgorithmList(self):
		"""An instance of the OspfSRAlgorithmList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsralgorithmlist.OspfSRAlgorithmList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsralgorithmlist import OspfSRAlgorithmList
		return OspfSRAlgorithmList(self)

	@property
	def OspfSRGBRangeSubObjectsList(self):
		"""An instance of the OspfSRGBRangeSubObjectsList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsrgbrangesubobjectslist.OspfSRGBRangeSubObjectsList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsrgbrangesubobjectslist import OspfSRGBRangeSubObjectsList
		return OspfSRGBRangeSubObjectsList(self)

	@property
	def BIERPrefix(self):
		"""Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BIERPrefix')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Algorithm(self):
		"""Algorithm for the Node SID/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('algorithm')

	@property
	def BBit(self):
		"""Router-LSA B-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bBit')

	@property
	def BierAFlag(self):
		"""Attach Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierAFlag')

	@property
	def BierNFlag(self):
		"""Node Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierNFlag')

	@property
	def ConfigureSIDIndexLabel(self):
		"""Configure SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureSIDIndexLabel')

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
	def DiscardLearnedLsa(self):
		"""Discard Learned LSAs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardLearnedLsa')

	@property
	def DoNotGenerateRouterLsa(self):
		"""Generate Router LSA.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('doNotGenerateRouterLsa')

	@property
	def EBit(self):
		"""Router-LSA E-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eBit')

	@property
	def EFlag(self):
		"""Explicit-Null Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlag')

	@property
	def EnableBIER(self):
		"""Enable BIER

		Returns:
			bool
		"""
		return self._get_attribute('enableBIER')
	@EnableBIER.setter
	def EnableBIER(self, value):
		self._set_attribute('enableBIER', value)

	@property
	def EnableMappingServer(self):
		"""Enable Mapping Server of Segment Routing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableMappingServer')

	@property
	def EnableSegmentRouting(self):
		"""Enable Segment Routing

		Returns:
			bool
		"""
		return self._get_attribute('enableSegmentRouting')
	@EnableSegmentRouting.setter
	def EnableSegmentRouting(self, value):
		self._set_attribute('enableSegmentRouting', value)

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def GracefulRestart(self):
		"""Enable Graceful Restart,if enabled Discard Learned LSAs should be disabled in order to learn the LSAs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('gracefulRestart')

	@property
	def InterFloodLsUpdateBurstGap(self):
		"""Inter Flood LSUpdate burst gap (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interFloodLsUpdateBurstGap')

	@property
	def LFlag(self):
		"""Local or Global Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def LocalRouterID(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterID')

	@property
	def LoopBackAddress(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('loopBackAddress')

	@property
	def LsaRefreshTime(self):
		"""LSA Refresh time (s)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lsaRefreshTime')

	@property
	def LsaRetransmitTime(self):
		"""LSA Retransmit time(s)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lsaRetransmitTime')

	@property
	def MFlag(self):
		"""Mapping Server Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mFlag')

	@property
	def MaxLsUpdatesPerBurst(self):
		"""Max Flood LSUpdates Per Burst

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLsUpdatesPerBurst')

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
	def NoOfAddressPrefix(self):
		"""Number Of Address Prefix Range

		Returns:
			number
		"""
		return self._get_attribute('noOfAddressPrefix')
	@NoOfAddressPrefix.setter
	def NoOfAddressPrefix(self, value):
		self._set_attribute('noOfAddressPrefix', value)

	@property
	def NoOfBIERSubDomains(self):
		"""Number of BIER Sub Domains

		Returns:
			number
		"""
		return self._get_attribute('noOfBIERSubDomains')
	@NoOfBIERSubDomains.setter
	def NoOfBIERSubDomains(self, value):
		self._set_attribute('noOfBIERSubDomains', value)

	@property
	def NpFlag(self):
		"""No-PHP Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('npFlag')

	@property
	def OobResyncBreakout(self):
		"""Enable out-of-band resynchronization breakout

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('oobResyncBreakout')

	@property
	def SRAlgorithmCount(self):
		"""SR Algorithm Count

		Returns:
			number
		"""
		return self._get_attribute('sRAlgorithmCount')
	@SRAlgorithmCount.setter
	def SRAlgorithmCount(self, value):
		self._set_attribute('sRAlgorithmCount', value)

	@property
	def SessionInfo(self):
		"""Logs additional information about the session Information

		Returns:
			list(str[noIfaceUp|sameNbrRouterId|up])
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
	def SidIndexLabel(self):
		"""SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidIndexLabel')

	@property
	def SrgbRangeCount(self):
		"""SRGB Range Count

		Returns:
			number
		"""
		return self._get_attribute('srgbRangeCount')
	@SrgbRangeCount.setter
	def SrgbRangeCount(self, value):
		self._set_attribute('srgbRangeCount', value)

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

	@property
	def StrictLsaChecking(self):
		"""Terminate graceful restart when an LSA has changed

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('strictLsaChecking')

	@property
	def SupportForRfc3623(self):
		"""Support RFC 3623 features,if enabled Discard Learned LSAs should be disabled in order to learn the LSAs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportForRfc3623')

	@property
	def SupportReasonSoftReloadUpgrade(self):
		"""Support graceful restart helper mode when restart reason is Software Reload or Upgrade.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportReasonSoftReloadUpgrade')

	@property
	def SupportReasonSoftRestart(self):
		"""Support graceful restart helper mode when restart reason is OSPFv2 software restart.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportReasonSoftRestart')

	@property
	def SupportReasonSwitchRedundantCntrlProcessor(self):
		"""Support graceful restart helper mode when restart reason is unplanned switchover.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportReasonSwitchRedundantCntrlProcessor')

	@property
	def SupportReasonUnknown(self):
		"""Support graceful restart helper mode when restart reason is unknown and unplanned.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportReasonUnknown')

	@property
	def VFlag(self):
		"""Value or Index Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

	def find(self, Count=None, DescriptiveName=None, EnableBIER=None, EnableSegmentRouting=None, Errors=None, LocalRouterID=None, LoopBackAddress=None, Name=None, NoOfAddressPrefix=None, NoOfBIERSubDomains=None, SRAlgorithmCount=None, SessionInfo=None, SessionStatus=None, SrgbRangeCount=None, StateCounts=None, Status=None):
		"""Finds and retrieves ospfv2Router data from the server.

		All named parameters support regex and can be used to selectively retrieve ospfv2Router data from the server.
		By default the find method takes no parameters and will retrieve all ospfv2Router data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableBIER (bool): Enable BIER
			EnableSegmentRouting (bool): Enable Segment Routing
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			LocalRouterID (list(str)): Router ID
			LoopBackAddress (list(str)): Router ID
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NoOfAddressPrefix (number): Number Of Address Prefix Range
			NoOfBIERSubDomains (number): Number of BIER Sub Domains
			SRAlgorithmCount (number): SR Algorithm Count
			SessionInfo (list(str[noIfaceUp|sameNbrRouterId|up])): Logs additional information about the session Information
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			SrgbRangeCount (number): SRGB Range Count
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching ospfv2Router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ospfv2Router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ospfv2Router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def OspfStartRouter(self):
		"""Executes the ospfStartRouter operation on the server.

		Start OSPF Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('OspfStartRouter', payload=locals(), response_object=None)

	def OspfStartRouter(self, SessionIndices):
		"""Executes the ospfStartRouter operation on the server.

		Start OSPF Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('OspfStartRouter', payload=locals(), response_object=None)

	def OspfStartRouter(self, SessionIndices):
		"""Executes the ospfStartRouter operation on the server.

		Start OSPF Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('OspfStartRouter', payload=locals(), response_object=None)

	def OspfStopRouter(self):
		"""Executes the ospfStopRouter operation on the server.

		Stop OSPF Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('OspfStopRouter', payload=locals(), response_object=None)

	def OspfStopRouter(self, SessionIndices):
		"""Executes the ospfStopRouter operation on the server.

		Stop OSPF Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('OspfStopRouter', payload=locals(), response_object=None)

	def OspfStopRouter(self, SessionIndices):
		"""Executes the ospfStopRouter operation on the server.

		Stop OSPF Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('OspfStopRouter', payload=locals(), response_object=None)

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
