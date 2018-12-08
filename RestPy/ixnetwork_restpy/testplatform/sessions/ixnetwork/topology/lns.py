
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


class Lns(Base):
	"""The Lns class encapsulates a user managed lns node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Lns property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'lns'

	def __init__(self, parent):
		super(Lns, self).__init__(parent)

	@property
	def LnsAuthCredentials(self):
		"""An instance of the LnsAuthCredentials class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lnsauthcredentials.LnsAuthCredentials)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.lnsauthcredentials import LnsAuthCredentials
		return LnsAuthCredentials(self)._select()

	@property
	def Pppoxserver(self):
		"""An instance of the Pppoxserver class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pppoxserver.Pppoxserver)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pppoxserver import Pppoxserver
		return Pppoxserver(self)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def BearerCapability(self):
		"""Indicates to the DUT the bearer device types from which incoming calls will be accepted.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bearerCapability')

	@property
	def BearerType(self):
		"""The bearer type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bearerType')

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
	def ControlMsgsRetryCounter(self):
		"""Number of L2TP retries

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('controlMsgsRetryCounter')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def CredentialsCount(self):
		"""Number of L2TP authentication credentials the LNS accepts for multiple tunnels establishment.

		Returns:
			number
		"""
		return self._get_attribute('credentialsCount')
	@CredentialsCount.setter
	def CredentialsCount(self, value):
		self._set_attribute('credentialsCount', value)

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnableControlChecksum(self):
		"""If checked, UDP checksum is enabled on control plane packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableControlChecksum')

	@property
	def EnableDataChecksum(self):
		"""If checked, UDP checksum is enabled on data plane packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDataChecksum')

	@property
	def EnableExcludeHdlc(self):
		"""If checked, HDLC header is not encoded in the L2TP packets.

		Returns:
			bool
		"""
		return self._get_attribute('enableExcludeHdlc')
	@EnableExcludeHdlc.setter
	def EnableExcludeHdlc(self, value):
		self._set_attribute('enableExcludeHdlc', value)

	@property
	def EnableHelloRequest(self):
		"""If checked, L2TP hello request is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHelloRequest')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def FramingCapability(self):
		"""Designates sync or async framing

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('framingCapability')

	@property
	def HelloRequestInterval(self):
		"""Timeout for L2TP hello request, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('helloRequestInterval')

	@property
	def InitRetransmitInterval(self):
		"""The initial amount of time that can elapse before an unacknowledged control message is retransmitted.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initRetransmitInterval')

	@property
	def LacHostName(self):
		"""This is the hostname used in authentication.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lacHostName')

	@property
	def LacSecret(self):
		"""L2TP secret to be used in authentication

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lacSecret')

	@property
	def LnsHostName(self):
		"""L2TP hostname sent by Ixia port when acting as LNS

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lnsHostName')

	@property
	def MaxRetransmitInterval(self):
		"""The maximum amount of time that can elapse for receiving a reply for a control message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxRetransmitInterval')

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
	def NoCallTimeout(self):
		"""Timeout for no call establishment, in seconds

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('noCallTimeout')

	@property
	def OffsetByte(self):
		"""L2TP offset byte. Applicable only if offset bit is set.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('offsetByte')

	@property
	def OffsetLength(self):
		"""L2TP offset length in bytes. Applicable only if offset bit set.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('offsetLength')

	@property
	def ReceiveWindowSize(self):
		"""L2TP Receive Window Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('receiveWindowSize')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

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

	@property
	def TunnelAuthentication(self):
		"""Enables or disables L2TP tunnel authentication

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tunnelAuthentication')

	@property
	def UdpDestinationPort(self):
		"""UDP port to employ for tunneling destinations

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('udpDestinationPort')

	@property
	def UdpSourcePort(self):
		"""UDP port to employ for tunneling sources

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('udpSourcePort')

	@property
	def UseHiddenAVPs(self):
		"""If checked, Attribute Value Pair hiding is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useHiddenAVPs')

	@property
	def UseLengthBitInPayload(self):
		"""If checked, length bit is set in L2TP data packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useLengthBitInPayload')

	@property
	def UseOffsetBitInPayload(self):
		"""If checked, offset bit is enabled in L2TP data packets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useOffsetBitInPayload')

	@property
	def UseSequenceNoInPayload(self):
		"""If checked, sequence bit is set in L2TP data packets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useSequenceNoInPayload')

	def add(self, ConnectedVia=None, CredentialsCount=None, EnableExcludeHdlc=None, Multiplier=None, Name=None, StackedLayers=None):
		"""Adds a new lns node on the server and retrieves it in this instance.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			CredentialsCount (number): Number of L2TP authentication credentials the LNS accepts for multiple tunnels establishment.
			EnableExcludeHdlc (bool): If checked, HDLC header is not encoded in the L2TP packets.
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved lns data using find and the newly added lns data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the lns data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ConnectedVia=None, Count=None, CredentialsCount=None, DescriptiveName=None, EnableExcludeHdlc=None, Errors=None, Multiplier=None, Name=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves lns data from the server.

		All named parameters support regex and can be used to selectively retrieve lns data from the server.
		By default the find method takes no parameters and will retrieve all lns data from the server.

		Args:
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			CredentialsCount (number): Number of L2TP authentication credentials the LNS accepts for multiple tunnels establishment.
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			EnableExcludeHdlc (bool): If checked, HDLC header is not encoded in the L2TP packets.
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching lns data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lns data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lns data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, BearerCapability=None, BearerType=None, ControlMsgsRetryCounter=None, EnableControlChecksum=None, EnableDataChecksum=None, EnableHelloRequest=None, FramingCapability=None, HelloRequestInterval=None, InitRetransmitInterval=None, LacHostName=None, LacSecret=None, LnsHostName=None, MaxRetransmitInterval=None, NoCallTimeout=None, OffsetByte=None, OffsetLength=None, ReceiveWindowSize=None, TunnelAuthentication=None, UdpDestinationPort=None, UdpSourcePort=None, UseHiddenAVPs=None, UseLengthBitInPayload=None, UseOffsetBitInPayload=None, UseSequenceNoInPayload=None):
		"""Base class infrastructure that gets a list of lns device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BearerCapability (str): optional regex of bearerCapability
			BearerType (str): optional regex of bearerType
			ControlMsgsRetryCounter (str): optional regex of controlMsgsRetryCounter
			EnableControlChecksum (str): optional regex of enableControlChecksum
			EnableDataChecksum (str): optional regex of enableDataChecksum
			EnableHelloRequest (str): optional regex of enableHelloRequest
			FramingCapability (str): optional regex of framingCapability
			HelloRequestInterval (str): optional regex of helloRequestInterval
			InitRetransmitInterval (str): optional regex of initRetransmitInterval
			LacHostName (str): optional regex of lacHostName
			LacSecret (str): optional regex of lacSecret
			LnsHostName (str): optional regex of lnsHostName
			MaxRetransmitInterval (str): optional regex of maxRetransmitInterval
			NoCallTimeout (str): optional regex of noCallTimeout
			OffsetByte (str): optional regex of offsetByte
			OffsetLength (str): optional regex of offsetLength
			ReceiveWindowSize (str): optional regex of receiveWindowSize
			TunnelAuthentication (str): optional regex of tunnelAuthentication
			UdpDestinationPort (str): optional regex of udpDestinationPort
			UdpSourcePort (str): optional regex of udpSourcePort
			UseHiddenAVPs (str): optional regex of useHiddenAVPs
			UseLengthBitInPayload (str): optional regex of useLengthBitInPayload
			UseOffsetBitInPayload (str): optional regex of useOffsetBitInPayload
			UseSequenceNoInPayload (str): optional regex of useSequenceNoInPayload

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

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
