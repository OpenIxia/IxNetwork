
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


class Ldpotherpws(Base):
	"""The Ldpotherpws class encapsulates a user managed ldpotherpws node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ldpotherpws property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ldpotherpws'

	def __init__(self, parent):
		super(Ldpotherpws, self).__init__(parent)

	@property
	def CfmMp(self):
		"""An instance of the CfmMp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cfmmp.CfmMp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cfmmp import CfmMp
		return CfmMp(self)

	@property
	def Connector(self):
		"""An instance of the Connector class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return Connector(self)

	@property
	def Ethernet(self):
		"""An instance of the Ethernet class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ethernet.Ethernet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ethernet import Ethernet
		return Ethernet(self)

	@property
	def Ipv4Loopback(self):
		"""An instance of the Ipv4Loopback class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4loopback.Ipv4Loopback)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4loopback import Ipv4Loopback
		return Ipv4Loopback(self)

	@property
	def Ipv6Loopback(self):
		"""An instance of the Ipv6Loopback class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6loopback.Ipv6Loopback)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6loopback import Ipv6Loopback
		return Ipv6Loopback(self)

	@property
	def LdpBasicRouter(self):
		"""An instance of the LdpBasicRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpbasicrouter.LdpBasicRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpbasicrouter import LdpBasicRouter
		return LdpBasicRouter(self)

	@property
	def LdpBasicRouterV6(self):
		"""An instance of the LdpBasicRouterV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpbasicrouterv6.LdpBasicRouterV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpbasicrouterv6 import LdpBasicRouterV6
		return LdpBasicRouterV6(self)

	@property
	def LdpTargetedRouter(self):
		"""An instance of the LdpTargetedRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouter.LdpTargetedRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouter import LdpTargetedRouter
		return LdpTargetedRouter(self)

	@property
	def LdpTargetedRouterV6(self):
		"""An instance of the LdpTargetedRouterV6 class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouterv6.LdpTargetedRouterV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptargetedrouterv6 import LdpTargetedRouterV6
		return LdpTargetedRouterV6(self)

	@property
	def ATMPresent(self):
		"""If selected, indicates that ATM Transparent Cell Transport mode is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('aTMPresent')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AutoPeerID(self):
		"""If selected, LDP Peer IP would be taken from LDP router's peer configuration.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoPeerID')

	@property
	def AutoPeerId(self):
		"""If selected, LDP Peer IP would be taken from LDP router's peer configuration.

		Returns:
			bool
		"""
		return self._get_attribute('autoPeerId')
	@AutoPeerId.setter
	def AutoPeerId(self, value):
		self._set_attribute('autoPeerId', value)

	@property
	def BfdPwCV(self):
		"""BFD PW-ACH CV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bfdPwCV')

	@property
	def BfdUdpCV(self):
		"""BFD IP/UDP CV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bfdUdpCV')

	@property
	def CAS(self):
		"""CAS Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cAS')

	@property
	def CBitEnabled(self):
		"""If selected, sets the C-Bit (flag). It is the highest order bit in the VC Type field. If the bit is set, it indicates the presence of a control word on this VC.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cBitEnabled')

	@property
	def CEMOption(self):
		"""The value of the CEM option

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cEMOption')

	@property
	def CEMOptionPresent(self):
		"""If selected, indicates that a CEM option is present

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cEMOptionPresent')

	@property
	def CEMPayLoadEnable(self):
		"""If selected, indicates that there is a Circuit Emulation Service over MPLS (CEM) payload

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cEMPayLoadEnable')

	@property
	def CEMPayload(self):
		"""The length of the CEM payload (in bytes)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cEMPayload')

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
	def DescEnabled(self):
		"""If selected, indicates that an optional Interface Description is present

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('descEnabled')

	@property
	def Description(self):
		"""An optional user-defined Interface Description. It may be used with ALL VC types. Valid length is 0 to 80 octets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('description')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DownInterval(self):
		"""Time interval for which the PW status will remain down

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('downInterval')

	@property
	def DownStart(self):
		"""The duration in time after session becomes up and a notification message being sent to make the session down

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('downStart')

	@property
	def EnableCCCVNegotiation(self):
		"""If selected, indicates that CCCV Negotiation is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableCCCVNegotiation')

	@property
	def EnablePWStatus(self):
		"""If selected, this enables the use of PW Status TLV in notification messages to notify the PW status

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePWStatus')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def Frequency(self):
		"""Configures the frequency of the payload type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('frequency')

	@property
	def GroupId(self):
		"""A user-defined 32-bit value used to identify a group of VCs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupId')

	@property
	def IfaceType(self):
		"""The 15-bit VC Type used in the VC FEC element.It depends on the Layer 2 protocol used on the interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ifaceType')

	@property
	def IncludeRTPHeader(self):
		"""If selected, indicates that RTP Header is present

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeRTPHeader')

	@property
	def IncludeSSRC(self):
		"""Click to enable SSRC

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSSRC')

	@property
	def IncludeTDMBitrate(self):
		"""If selected, indicates that TDM Bitrate is present

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeTDMBitrate')

	@property
	def IncludeTDMOption(self):
		"""Include TDM Option

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeTDMOption')

	@property
	def IncludeTDMPayload(self):
		"""If selected, indicates that TDM Payload is present

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeTDMPayload')

	@property
	def Ipv6PeerId(self):
		"""The 128-bit IPv6 address of the LDP Peer.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6PeerId')

	@property
	def LSPPingCV(self):
		"""LSP Ping CV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lSPPingCV')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalRouterID(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterID')

	@property
	def MaxATMCells(self):
		"""The Maximum number of ATM Cells which may be concatenated and sent in a single MPLS frame

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxATMCells')

	@property
	def Mtu(self):
		"""The 2-octet value for the maximum Transmission Unit (MTU).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mtu')

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
	def PWACHCC(self):
		"""PW-ACH CC

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pWACHCC')

	@property
	def PWStatusCode(self):
		"""PW Status Code to be sent when to transition to down state if PW Status Send Notification is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pWStatusCode')

	@property
	def PayloadType(self):
		"""Configures the pay load type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('payloadType')

	@property
	def PeerId(self):
		"""The 32-bit IPv4 address of the LDP Peer.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerId')

	@property
	def PwStatusSendNotification(self):
		"""If selected, it signifies whether to send a notification message with a PW status for the corresponding PW

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pwStatusSendNotification')

	@property
	def RepeatCount(self):
		"""The number of times to repeat the Up/Down status of the PW. '0' means keep toggling the Up/Down state indefinitely.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('repeatCount')

	@property
	def RouterAlertCC(self):
		"""Router Alert CC

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routerAlertCC')

	@property
	def SP(self):
		"""SP Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sP')

	@property
	def SSRC(self):
		"""SSRC Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sSRC')

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
	def TDMBitrate(self):
		"""The value of the TDM bitrate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tDMBitrate')

	@property
	def TDMDataSize(self):
		"""The total size of the TDM data

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tDMDataSize')

	@property
	def TimestampMode(self):
		"""Timestamp Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timestampMode')

	@property
	def UpInterval(self):
		"""Time Interval for which the PW status will remain in Up state before transitioning again to Down state.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('upInterval')

	@property
	def VCIDStart(self):
		"""The value of the VC ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vCIDStart')

	def add(self, AutoPeerId=None, ConnectedVia=None, Multiplier=None, Name=None, StackedLayers=None):
		"""Adds a new ldpotherpws node on the server and retrieves it in this instance.

		Args:
			AutoPeerId (bool): If selected, LDP Peer IP would be taken from LDP router's peer configuration.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			self: This instance with all currently retrieved ldpotherpws data using find and the newly added ldpotherpws data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ldpotherpws data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoPeerId=None, ConnectedVia=None, Count=None, DescriptiveName=None, Errors=None, LocalRouterID=None, Multiplier=None, Name=None, SessionStatus=None, StackedLayers=None, StateCounts=None, Status=None):
		"""Finds and retrieves ldpotherpws data from the server.

		All named parameters support regex and can be used to selectively retrieve ldpotherpws data from the server.
		By default the find method takes no parameters and will retrieve all ldpotherpws data from the server.

		Args:
			AutoPeerId (bool): If selected, LDP Peer IP would be taken from LDP router's peer configuration.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			LocalRouterID (list(str)): Router ID
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SessionStatus (list(str[down|notStarted|up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols
			StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			self: This instance with matching ldpotherpws data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ldpotherpws data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ldpotherpws data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, ATMPresent=None, Active=None, AutoPeerID=None, BfdPwCV=None, BfdUdpCV=None, CAS=None, CBitEnabled=None, CEMOption=None, CEMOptionPresent=None, CEMPayLoadEnable=None, CEMPayload=None, DescEnabled=None, Description=None, DownInterval=None, DownStart=None, EnableCCCVNegotiation=None, EnablePWStatus=None, Frequency=None, GroupId=None, IfaceType=None, IncludeRTPHeader=None, IncludeSSRC=None, IncludeTDMBitrate=None, IncludeTDMOption=None, IncludeTDMPayload=None, Ipv6PeerId=None, LSPPingCV=None, Label=None, MaxATMCells=None, Mtu=None, PWACHCC=None, PWStatusCode=None, PayloadType=None, PeerId=None, PwStatusSendNotification=None, RepeatCount=None, RouterAlertCC=None, SP=None, SSRC=None, TDMBitrate=None, TDMDataSize=None, TimestampMode=None, UpInterval=None, VCIDStart=None):
		"""Base class infrastructure that gets a list of ldpotherpws device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ATMPresent (str): optional regex of aTMPresent
			Active (str): optional regex of active
			AutoPeerID (str): optional regex of autoPeerID
			BfdPwCV (str): optional regex of bfdPwCV
			BfdUdpCV (str): optional regex of bfdUdpCV
			CAS (str): optional regex of cAS
			CBitEnabled (str): optional regex of cBitEnabled
			CEMOption (str): optional regex of cEMOption
			CEMOptionPresent (str): optional regex of cEMOptionPresent
			CEMPayLoadEnable (str): optional regex of cEMPayLoadEnable
			CEMPayload (str): optional regex of cEMPayload
			DescEnabled (str): optional regex of descEnabled
			Description (str): optional regex of description
			DownInterval (str): optional regex of downInterval
			DownStart (str): optional regex of downStart
			EnableCCCVNegotiation (str): optional regex of enableCCCVNegotiation
			EnablePWStatus (str): optional regex of enablePWStatus
			Frequency (str): optional regex of frequency
			GroupId (str): optional regex of groupId
			IfaceType (str): optional regex of ifaceType
			IncludeRTPHeader (str): optional regex of includeRTPHeader
			IncludeSSRC (str): optional regex of includeSSRC
			IncludeTDMBitrate (str): optional regex of includeTDMBitrate
			IncludeTDMOption (str): optional regex of includeTDMOption
			IncludeTDMPayload (str): optional regex of includeTDMPayload
			Ipv6PeerId (str): optional regex of ipv6PeerId
			LSPPingCV (str): optional regex of lSPPingCV
			Label (str): optional regex of label
			MaxATMCells (str): optional regex of maxATMCells
			Mtu (str): optional regex of mtu
			PWACHCC (str): optional regex of pWACHCC
			PWStatusCode (str): optional regex of pWStatusCode
			PayloadType (str): optional regex of payloadType
			PeerId (str): optional regex of peerId
			PwStatusSendNotification (str): optional regex of pwStatusSendNotification
			RepeatCount (str): optional regex of repeatCount
			RouterAlertCC (str): optional regex of routerAlertCC
			SP (str): optional regex of sP
			SSRC (str): optional regex of sSRC
			TDMBitrate (str): optional regex of tDMBitrate
			TDMDataSize (str): optional regex of tDMDataSize
			TimestampMode (str): optional regex of timestampMode
			UpInterval (str): optional regex of upInterval
			VCIDStart (str): optional regex of vCIDStart

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def PurgeVCRanges(self):
		"""Executes the purgeVCRanges operation on the server.

		Purge VC Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PurgeVCRanges', payload=locals(), response_object=None)

	def PurgeVCRanges(self, SessionIndices):
		"""Executes the purgeVCRanges operation on the server.

		Purge VC Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PurgeVCRanges', payload=locals(), response_object=None)

	def PurgeVCRanges(self, SessionIndices):
		"""Executes the purgeVCRanges operation on the server.

		Purge VC Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PurgeVCRanges', payload=locals(), response_object=None)

	def Purgevcranges(self, Arg2):
		"""Executes the purgevcranges operation on the server.

		Purge Ethernet VC. Sends Address Withdraw message to purge all MACs learnt for this VC. Applicable for Ethernet Type VC only ( not VLAN).

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): Purge VC Ranges.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Purgevcranges', payload=locals(), response_object=None)

	def PurgeVPLSMac(self, Mac_count, Mac):
		"""Executes the purgeVPLSMac operation on the server.

		Purge VPLS MAC

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Mac_count (number): This parameter requires a mac_count of type kInteger
			Mac (str): This parameter requires a mac of type kString

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PurgeVPLSMac', payload=locals(), response_object=None)

	def PurgeVPLSMac(self, Mac_count, Mac, SessionIndices):
		"""Executes the purgeVPLSMac operation on the server.

		Purge VPLS MAC

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Mac_count (number): This parameter requires a mac_count of type kInteger
			Mac (str): This parameter requires a mac of type kString
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PurgeVPLSMac', payload=locals(), response_object=None)

	def PurgeVPLSMac(self, SessionIndices, Mac_count, Mac):
		"""Executes the purgeVPLSMac operation on the server.

		Purge VPLS MAC

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a mac_count of type kInteger
			Mac_count (number): This parameter requires a mac of type kString
			Mac (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('PurgeVPLSMac', payload=locals(), response_object=None)

	def PurgeVPLSMac(self, Arg2, Arg3, Arg4):
		"""Executes the purgeVPLSMac operation on the server.

		Purge Ethernet MAC. Sends Address Withdraw message with specified MACs. Applicable for Ethernet Type VC only ( not VLAN).

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): Purge Ethernet MAC.
			Arg3 (number): Number of Mac addresses to purge
			Arg4 (str): Mac addresses start

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('PurgeVPLSMac', payload=locals(), response_object=None)

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

		Activate VC

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

		Activate VC

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

		Activate VC

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

		Deactivate VC

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

		Deactivate VC

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

		Deactivate VC

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
