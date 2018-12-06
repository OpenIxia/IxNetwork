
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


class OfSwitchPorts(Base):
	"""The OfSwitchPorts class encapsulates a required ofSwitchPorts node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfSwitchPorts property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ofSwitchPorts'

	def __init__(self, parent):
		super(OfSwitchPorts, self).__init__(parent)

	@property
	def OfSwitchQueues(self):
		"""An instance of the OfSwitchQueues class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchqueues.OfSwitchQueues)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ofswitchqueues import OfSwitchQueues
		return OfSwitchQueues(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvertisedFeatures(self):
		"""Select the features (link modes, link types, and link features) from the list that will be advertised by the port

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertisedFeatures')

	@property
	def Config(self):
		"""Select the port administrative settings to indicate the behavior of the physical port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('config')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def CurrentConnectionType(self):
		"""Port Type calculated based on host topology assigned and forced type.

		Returns:
			list(str[auto|externalSwitch|host|internalSwitch|noConnection])
		"""
		return self._get_attribute('currentConnectionType')

	@property
	def CurrentFeatures(self):
		"""Select the current features (link modes, link types, and link features) from the list that the port will support

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('currentFeatures')

	@property
	def CurrentSpeed(self):
		"""The current bit rate (raw transmission speed) of the link in kilobytes per second. This indicates the current capacity of the link.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('currentSpeed')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EtherAddr(self):
		"""The Ethernet address for the OpenFlow switch port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('etherAddr')

	@property
	def ForcedConnectionType(self):
		"""Users override for connection type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('forcedConnectionType')

	@property
	def MaxSpeed(self):
		"""The maximum bit rate (raw transmission speed) of the link in kilobytes per second. This indicates the maximum configured capacity of the link.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxSpeed')

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
	def NumQueueRange(self):
		"""Specify the number of Queue ranges to be configured for this switch port

		Returns:
			number
		"""
		return self._get_attribute('numQueueRange')
	@NumQueueRange.setter
	def NumQueueRange(self, value):
		self._set_attribute('numQueueRange', value)

	@property
	def ParentSwitch(self):
		"""Parent Switch Name

		Returns:
			str
		"""
		return self._get_attribute('parentSwitch')

	@property
	def PeerAdvertisedFeatures(self):
		"""Select the features (link modes, link types, and link features) from the list that will be advertised by the peer

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('peerAdvertisedFeatures')

	@property
	def PortIndex(self):
		"""Index of port in particular OF Switch.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portIndex')

	@property
	def PortLivenessSupport(self):
		"""If selected, port liveness is supported in its port state. A port is considered live when it is not down or when its link is not down.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portLivenessSupport')

	@property
	def PortName(self):
		"""Specify the name of the Port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portName')

	@property
	def PortNumber(self):
		"""The OpenFlow pipeline receives and sends packets on ports.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portNumber')

	@property
	def RemotePortIndex(self):
		"""Index of the Remote Port. Please refer Port Index to enter value in this field.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remotePortIndex')

	@property
	def RemoteSwitch(self):
		"""The name of the remote Switch at the other end of the Switch OF Channel

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteSwitch')

	@property
	def RemoteSwitchIndex(self):
		"""Index of the Remote Switch. Please refer Switch Index to enter value in this field.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteSwitchIndex')

	@property
	def RemoteSwitchPort(self):
		"""The remote Switch port number identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteSwitchPort')

	@property
	def State(self):
		"""Specify the port states

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('state')

	@property
	def SupportedFeatures(self):
		"""Select the features (link modes, link types, and link features) from the list that will be supported by the port

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('supportedFeatures')

	@property
	def SwitchIndex(self):
		"""Index of the OF Switch.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('switchIndex')

	@property
	def TransmissionDelay(self):
		"""The delay in milliseconds, between internal Switch ports

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('transmissionDelay')

	def get_device_ids(self, PortNames=None, Active=None, AdvertisedFeatures=None, Config=None, CurrentFeatures=None, CurrentSpeed=None, EtherAddr=None, ForcedConnectionType=None, MaxSpeed=None, PeerAdvertisedFeatures=None, PortIndex=None, PortLivenessSupport=None, PortName=None, PortNumber=None, RemotePortIndex=None, RemoteSwitch=None, RemoteSwitchIndex=None, RemoteSwitchPort=None, State=None, SupportedFeatures=None, SwitchIndex=None, TransmissionDelay=None):
		"""Base class infrastructure that gets a list of ofSwitchPorts device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AdvertisedFeatures (str): optional regex of advertisedFeatures
			Config (str): optional regex of config
			CurrentFeatures (str): optional regex of currentFeatures
			CurrentSpeed (str): optional regex of currentSpeed
			EtherAddr (str): optional regex of etherAddr
			ForcedConnectionType (str): optional regex of forcedConnectionType
			MaxSpeed (str): optional regex of maxSpeed
			PeerAdvertisedFeatures (str): optional regex of peerAdvertisedFeatures
			PortIndex (str): optional regex of portIndex
			PortLivenessSupport (str): optional regex of portLivenessSupport
			PortName (str): optional regex of portName
			PortNumber (str): optional regex of portNumber
			RemotePortIndex (str): optional regex of remotePortIndex
			RemoteSwitch (str): optional regex of remoteSwitch
			RemoteSwitchIndex (str): optional regex of remoteSwitchIndex
			RemoteSwitchPort (str): optional regex of remoteSwitchPort
			State (str): optional regex of state
			SupportedFeatures (str): optional regex of supportedFeatures
			SwitchIndex (str): optional regex of switchIndex
			TransmissionDelay (str): optional regex of transmissionDelay

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def SimulatePortUpDown(self, Arg2):
		"""Executes the simulatePortUpDown operation on the server.

		Method to Simulate Port Up Down.

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
		return self._execute('SimulatePortUpDown', payload=locals(), response_object=None)
