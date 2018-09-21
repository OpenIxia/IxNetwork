from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PccGroup(Base):
	"""The PccGroup class encapsulates a user managed pccGroup node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PccGroup property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'pccGroup'

	def __init__(self, parent):
		super(PccGroup, self).__init__(parent)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)

	@property
	def LearnedInfoUpdate(self):
		"""An instance of the LearnedInfoUpdate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfoupdate.LearnedInfoUpdate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfoupdate import LearnedInfoUpdate
		return LearnedInfoUpdate(self)

	@property
	def PcReplyLspParameters(self):
		"""An instance of the PcReplyLspParameters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcreplylspparameters.PcReplyLspParameters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcreplylspparameters import PcReplyLspParameters
		return PcReplyLspParameters(self)._select()

	@property
	def PcRequestMatchCriteria(self):
		"""An instance of the PcRequestMatchCriteria class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcrequestmatchcriteria.PcRequestMatchCriteria)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcrequestmatchcriteria import PcRequestMatchCriteria
		return PcRequestMatchCriteria(self)._select()

	@property
	def PceInitiateLSPParameters(self):
		"""An instance of the PceInitiateLSPParameters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceinitiatelspparameters.PceInitiateLSPParameters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceinitiatelspparameters import PceInitiateLSPParameters
		return PceInitiateLSPParameters(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Authentication(self):
		"""The type of cryptographic authentication to be used on this link interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authentication')

	@property
	def BurstInterval(self):
		"""Interval in milisecond in which desired rate of messages needs to be maintained.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('burstInterval')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DeadInterval(self):
		"""This is the time interval, after the expiration of which, a PCEP peer declares the session down if no PCEP message has been received.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('deadInterval')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def KeepaliveInterval(self):
		"""Frequency/Time Interval of sending PCEP messages to keep the session active.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keepaliveInterval')

	@property
	def MD5Key(self):
		"""A value to be used as the secret MD5 Key.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mD5Key')

	@property
	def MaxInitiatedLspPerInterval(self):
		"""Maximum number of messages can be sent per interval.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxInitiatedLspPerInterval')

	@property
	def MaxLspsPerPcInitiate(self):
		"""Controls the maximum number of LSPs that can be present in a PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLspsPerPcInitiate')

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

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
	def PcReplyLspsPerPcc(self):
		"""Controls the maximum number of PCE LSPs that can be send as PATH Response.

		Returns:
			number
		"""
		return self._get_attribute('pcReplyLspsPerPcc')
	@PcReplyLspsPerPcc.setter
	def PcReplyLspsPerPcc(self, value):
		self._set_attribute('pcReplyLspsPerPcc', value)

	@property
	def PccIpv4Address(self):
		"""IPv4 address of the PCC. This column is greyed out in case of PCEv6.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pccIpv4Address')

	@property
	def PceInitiatedLspsPerPcc(self):
		"""Controls the maximum number of PCE LSPs that can be Initiated per PCC.

		Returns:
			number
		"""
		return self._get_attribute('pceInitiatedLspsPerPcc')
	@PceInitiatedLspsPerPcc.setter
	def PceInitiatedLspsPerPcc(self, value):
		self._set_attribute('pceInitiatedLspsPerPcc', value)

	@property
	def PcePpagTLVType(self):
		"""PPAG TLV Type specifies PCE's capability of interpreting this type of PPAG TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pcePpagTLVType')

	@property
	def RateControl(self):
		"""The rate control is an optional feature associated with PCE initiated LSP.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rateControl')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SrPceCapability(self):
		"""The SR PCE Capability TLV is an optional TLV associated with the OPEN Object to exchange SR capability of PCEP speakers.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srPceCapability')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

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

	def add(self, ConnectedVia=None, Multiplier=None, Name=None, PcReplyLspsPerPcc=None, PceInitiatedLspsPerPcc=None, StackedLayers=None):
		"""Adds a new pccGroup node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			PcReplyLspsPerPcc (number): Controls the maximum number of PCE LSPs that can be send as PATH Response.
			PceInitiatedLspsPerPcc (number): Controls the maximum number of PCE LSPs that can be Initiated per PCC.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved pccGroup data using find and the newly added pccGroup data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the pccGroup data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, Multiplier=None, Name=None, PcReplyLspsPerPcc=None, PceInitiatedLspsPerPcc=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves pccGroup data from the server.

		All named parameters support regex and can be used to selectively retrieve pccGroup data from the server.
		By default the find method takes no parameters and will retrieve all pccGroup data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			PcReplyLspsPerPcc (number): Controls the maximum number of PCE LSPs that can be send as PATH Response.
			PceInitiatedLspsPerPcc (number): Controls the maximum number of PCE LSPs that can be Initiated per PCC.
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching pccGroup data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pccGroup data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pccGroup data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ClearPceAllLearnedInfo(self):
		"""Executes the clearPceAllLearnedInfo operation on the server.

		Clears ALL Learned LSP Information By PCC Device.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearPceAllLearnedInfo', payload=locals(), response_object=None)

	def ClearPceAllLearnedInfo(self, SessionIndices):
		"""Executes the clearPceAllLearnedInfo operation on the server.

		Clears ALL Learned LSP Information By PCC Device.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearPceAllLearnedInfo', payload=locals(), response_object=None)

	def ClearPceAllLearnedInfo(self, SessionIndices):
		"""Executes the clearPceAllLearnedInfo operation on the server.

		Clears ALL Learned LSP Information By PCC Device.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearPceAllLearnedInfo', payload=locals(), response_object=None)

	def ClearPceAllLearnedInfo(self, Arg2):
		"""Executes the clearPceAllLearnedInfo operation on the server.

		Clears ALL Learned LSP Information By PCC Device.

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
		return self._execute('ClearPceAllLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllRsvpLspLearnedInfo(self):
		"""Executes the getPceBasicAllRsvpLspLearnedInfo operation on the server.

		Gets Basic Information about All RSVP LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllRsvpLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicAllRsvpLspLearnedInfo operation on the server.

		Gets Basic Information about All RSVP LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllRsvpLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicAllRsvpLspLearnedInfo operation on the server.

		Gets Basic Information about All RSVP LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllRsvpLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicAllRsvpLspLearnedInfo operation on the server.

		Gets Basic Information about All RSVP LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllSrLspLearnedInfo(self):
		"""Executes the getPceBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllSrLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllSrLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicAllSrLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicAllSrLspLearnedInfo operation on the server.

		Gets Basic Information about All SR LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccRequestedLspLearnedInfo(self):
		"""Executes the getPceBasicRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccRequestedLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccSyncLspLearnedInfo(self):
		"""Executes the getPceBasicRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPccSyncLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPceInitiatedLspLearnedInfo(self):
		"""Executes the getPceBasicRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicRsvpPceInitiatedLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccRequestedLspLearnedInfo(self):
		"""Executes the getPceBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccRequestedLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicSrPccRequestedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Requested LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccSyncLspLearnedInfo(self):
		"""Executes the getPceBasicSrPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicSrPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicSrPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPccSyncLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicSrPccSyncLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPceInitiatedLspLearnedInfo(self):
		"""Executes the getPceBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceBasicSrPceInitiatedLspLearnedInfo(self, Arg2):
		"""Executes the getPceBasicSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Basic Information about SR-TE PCE Initiated LSPs learnt by this PCE.

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
		return self._execute('GetPceBasicSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllRsvpLspLearnedInfo(self):
		"""Executes the getPceDetailedAllRsvpLspLearnedInfo operation on the server.

		Gets Detailed Information about All RSVP LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllRsvpLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedAllRsvpLspLearnedInfo operation on the server.

		Gets Detailed Information about All RSVP LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllRsvpLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedAllRsvpLspLearnedInfo operation on the server.

		Gets Detailed Information about All RSVP LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllRsvpLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedAllRsvpLspLearnedInfo operation on the server.

		Gets Detailed Information about All RSVP LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedAllRsvpLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllSrLspLearnedInfo(self):
		"""Executes the getPceDetailedAllSrLspLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllSrLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedAllSrLspLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllSrLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedAllSrLspLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedAllSrLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedAllSrLspLearnedInfo operation on the server.

		Gets Detailed Information about All SR LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedAllSrLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccRequestedLspLearnedInfo(self):
		"""Executes the getPceDetailedRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccRequestedLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedRsvpPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Requested LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedRsvpPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccSyncLspLearnedInfo(self):
		"""Executes the getPceDetailedRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPccSyncLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedRsvpPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCC Sync/Report LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedRsvpPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPceInitiatedLspLearnedInfo(self):
		"""Executes the getPceDetailedRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedRsvpPceInitiatedLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedRsvpPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about RSVP-TE PCE Initiated LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedRsvpPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccRequestedLspLearnedInfo(self):
		"""Executes the getPceDetailedSrPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedSrPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccRequestedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedSrPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Requested LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccRequestedLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedSrPccRequestedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Requested LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedSrPccRequestedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccSyncLspLearnedInfo(self):
		"""Executes the getPceDetailedSrPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedSrPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccSyncLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedSrPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPccSyncLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedSrPccSyncLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCC Sync/Report LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedSrPccSyncLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPceInitiatedLspLearnedInfo(self):
		"""Executes the getPceDetailedSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPceInitiatedLspLearnedInfo(self, SessionIndices):
		"""Executes the getPceDetailedSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCE Initiated LSPs learnt by this PCE.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetPceDetailedSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

	def GetPceDetailedSrPceInitiatedLspLearnedInfo(self, Arg2):
		"""Executes the getPceDetailedSrPceInitiatedLspLearnedInfo operation on the server.

		Gets Detailed Information about SR-TE PCE Initiated LSPs learnt by this PCE.

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
		return self._execute('GetPceDetailedSrPceInitiatedLspLearnedInfo', payload=locals(), response_object=None)

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
