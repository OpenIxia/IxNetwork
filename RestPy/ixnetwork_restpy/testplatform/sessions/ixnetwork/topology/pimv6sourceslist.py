
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


class PimV6SourcesList(Base):
	"""The PimV6SourcesList class encapsulates a required pimV6SourcesList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PimV6SourcesList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pimV6SourcesList'

	def __init__(self, parent):
		super(PimV6SourcesList, self).__init__(parent)

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
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def DiscardSgJoinStates(self):
		"""If selected, the Learned Join States sent by the RP (DUT) in response to this specific Register Message will be discarded-and will not be displayed in the table of the Register Range window.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('discardSgJoinStates')

	@property
	def GroupAddress(self):
		"""The first IPv6 multicast group address in the range of group addresses included in this Register message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddress')

	@property
	def GroupCount(self):
		"""The number of group addresses to be included in this register message

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCount')

	@property
	def LocalRouterId(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterId')

	@property
	def MulticastDataLength(self):
		"""(in bytes) This field indicates the length of the UDP packet (the payload) within the IPv4 packet that is encapsulated in the PIM-SM Register Message sent from the DR to the DUT. The default is 64 bytes.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('multicastDataLength')

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
	def RegisterProbeTime(self):
		"""(In seconds) Part of the Register-Stop Timer (RST (S,G). Used to control the time intervals for the transmission of Null-Register messages from the Source's DR to the RP. Prior to expiration of the Register Suppression Time of the RST, a Null-Register message is sent to probe the RP, as a reminder to the RP to send a new Register-Stop message and maintain the state. If the RP does not respond with a new Register-Stop message, the Source's DR will start sending Register-encapsulated data again. The default is 5 seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerProbeTime')

	@property
	def RpAddress(self):
		"""The IP address of the Rendezvous Point (RP) router-the root of the RPT (Rendezvous Point Tree).

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rpAddress')

	@property
	def SendNullRegAtBegin(self):
		"""If selected, a Null Register packet will be sent by the Ixia-emulated Designated Router (DR)/Source Range to the RP to start the message exchange. (A Null Register packet contains no data.) Regardless of whether or not the box is selected-in addition-a Null Register packet will be sent to the RP every time (just before) the Register Stop timer is about to expire on the RP. This will trigger the RP to restart the timer so it will continue sending Register Stop packets to the Ixia-emulated DR/Source Range.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendNullRegAtBegin')

	@property
	def SourceAddress(self):
		"""The first IPv6 source address to be included in this Register message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddress')

	@property
	def SourceCount(self):
		"""The number of source addresses to be included in this register message

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceCount')

	@property
	def Status(self):
		"""Status

		Returns:
			list(str[none|notStarted|started])
		"""
		return self._get_attribute('status')

	@property
	def SupressionTime(self):
		"""(In seconds) Part of the Register-Stop Timer (RST (S,G). The amount of time, following receipt of a Register-Stop message, that the DR will NOT send Register-encapsulated data to the Rendezvous Point (RP). The default is 60 seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supressionTime')

	@property
	def SwitchOverInterval(self):
		"""The time interval (in seconds) allowed for the switch from using the RP tree to using a Source-specific tree - from (*, G) to (S,G). The default value is 0.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('switchOverInterval')

	@property
	def TxIterationGap(self):
		"""(in milliseconds) The gap between each iteration of the Register Range. The default is 60,000 ms (= 60 seconds). (Does not apply to NULL Registers, which contain no data.)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('txIterationGap')

	@property
	def UdpDestinationPort(self):
		"""The number of UDP Destination Ports in the receiving Multicast Group. The default is 3000 UDP Destination Ports.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('udpDestinationPort')

	@property
	def UdpSourcePort(self):
		"""The number of UDP Source Ports sending encapsulated UDP packets to MultiCast Groups (through Register Messages to the RP). The default is 3000 UDP Source Ports.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('udpSourcePort')

	def get_device_ids(self, PortNames=None, Active=None, DiscardSgJoinStates=None, GroupAddress=None, GroupCount=None, MulticastDataLength=None, RegisterProbeTime=None, RpAddress=None, SendNullRegAtBegin=None, SourceAddress=None, SourceCount=None, SupressionTime=None, SwitchOverInterval=None, TxIterationGap=None, UdpDestinationPort=None, UdpSourcePort=None):
		"""Base class infrastructure that gets a list of pimV6SourcesList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			DiscardSgJoinStates (str): optional regex of discardSgJoinStates
			GroupAddress (str): optional regex of groupAddress
			GroupCount (str): optional regex of groupCount
			MulticastDataLength (str): optional regex of multicastDataLength
			RegisterProbeTime (str): optional regex of registerProbeTime
			RpAddress (str): optional regex of rpAddress
			SendNullRegAtBegin (str): optional regex of sendNullRegAtBegin
			SourceAddress (str): optional regex of sourceAddress
			SourceCount (str): optional regex of sourceCount
			SupressionTime (str): optional regex of supressionTime
			SwitchOverInterval (str): optional regex of switchOverInterval
			TxIterationGap (str): optional regex of txIterationGap
			UdpDestinationPort (str): optional regex of udpDestinationPort
			UdpSourcePort (str): optional regex of udpSourcePort

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def Start(self):
		"""Executes the start operation on the server.

		Activate Source

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

		Activate Source

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

		Activate Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		Start

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Deactivate Source

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

		Deactivate Source

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

		Deactivate Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		Stop

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
