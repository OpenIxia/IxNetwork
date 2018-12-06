
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


class PacketInList(Base):
	"""The PacketInList class encapsulates a system managed packetInList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PacketInList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'packetInList'

	def __init__(self, parent):
		super(PacketInList, self).__init__(parent)

	@property
	def AuxiliaryId(self):
		"""The identifier for auxiliary connections.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxiliaryId')

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
	def FlowTable(self):
		"""If selected, the Switch looks up for each PacketIn configured in the Flow Table.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowTable')

	@property
	def InPort(self):
		"""The Switch Port on which, this Packet has come.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('inPort')

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
	def PacketInName(self):
		"""The description of the packet-in.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInName')

	@property
	def PhysicalInPort(self):
		"""The physical In port value for this PacketIn range. It is the underlying physical port when packet is received on a logical port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('physicalInPort')

	@property
	def SendPacketIn(self):
		"""If selected, the Switch starts sending PacketIn messages when the session comes up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendPacketIn')

	@property
	def SwitchName(self):
		"""Parent Switch Name

		Returns:
			str
		"""
		return self._get_attribute('switchName')

	def find(self, Count=None, DescriptiveName=None, Name=None, SwitchName=None):
		"""Finds and retrieves packetInList data from the server.

		All named parameters support regex and can be used to selectively retrieve packetInList data from the server.
		By default the find method takes no parameters and will retrieve all packetInList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SwitchName (str): Parent Switch Name

		Returns:
			self: This instance with matching packetInList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of packetInList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the packetInList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, AuxiliaryId=None, FlowTable=None, InPort=None, PacketInName=None, PhysicalInPort=None, SendPacketIn=None):
		"""Base class infrastructure that gets a list of packetInList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AuxiliaryId (str): optional regex of auxiliaryId
			FlowTable (str): optional regex of flowTable
			InPort (str): optional regex of inPort
			PacketInName (str): optional regex of packetInName
			PhysicalInPort (str): optional regex of physicalInPort
			SendPacketIn (str): optional regex of sendPacketIn

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def SendPause(self, Arg2):
		"""Executes the sendPause operation on the server.

		Pause Sending PacketIn

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of PacketIn.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendPause', payload=locals(), response_object=None)

	def SendStart(self, Arg2):
		"""Executes the sendStart operation on the server.

		Start Sending PacketIn

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of PacketIn.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendStart', payload=locals(), response_object=None)

	def SendStop(self, Arg2):
		"""Executes the sendStop operation on the server.

		Stop Sending PacketIn

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of PacketIn.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendStop', payload=locals(), response_object=None)
