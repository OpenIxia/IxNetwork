
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


class Topology(Base):
	"""The Topology class encapsulates a user managed topology node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Topology property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'topology'

	def __init__(self, parent):
		super(Topology, self).__init__(parent)

	@property
	def DeviceGroup(self):
		"""An instance of the DeviceGroup class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup.DeviceGroup)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.devicegroup import DeviceGroup
		return DeviceGroup(self)

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
	def Note(self):
		"""Any Note about the Topology

		Returns:
			str
		"""
		return self._get_attribute('note')
	@Note.setter
	def Note(self, value):
		self._set_attribute('note', value)

	@property
	def PortCount(self):
		"""Number of /vports or /lags assigned (including unmapped ports)

		Returns:
			number
		"""
		return self._get_attribute('portCount')

	@property
	def Ports(self):
		"""Logical port information.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('ports')
	@Ports.setter
	def Ports(self, value):
		self._set_attribute('ports', value)

	@property
	def PortsStateCount(self):
		"""State of ports on this topology, arg1:total, arg2:up, arg3:down, arg4:other

		Returns:
			dict(arg1:number,arg2:number,arg3:number,arg4:number)
		"""
		return self._get_attribute('portsStateCount')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def Vports(self):
		"""Virtual port information.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('vports')
	@Vports.setter
	def Vports(self, value):
		self._set_attribute('vports', value)

	def add(self, Name=None, Note=None, Ports=None, Vports=None):
		"""Adds a new topology node on the server and retrieves it in this instance.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			Note (str): Any Note about the Topology
			Ports (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): Logical port information.
			Vports (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): Virtual port information.

		Returns:
			self: This instance with all currently retrieved topology data using find and the newly added topology data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the topology data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DescriptiveName=None, Errors=None, Name=None, Note=None, PortCount=None, Ports=None, PortsStateCount=None, Status=None, Vports=None):
		"""Finds and retrieves topology data from the server.

		All named parameters support regex and can be used to selectively retrieve topology data from the server.
		By default the find method takes no parameters and will retrieve all topology data from the server.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Errors (list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))): A list of errors that have occurred
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			Note (str): Any Note about the Topology
			PortCount (number): Number of /vports or /lags assigned (including unmapped ports)
			Ports (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): Logical port information.
			PortsStateCount (dict(arg1:number,arg2:number,arg3:number,arg4:number)): State of ports on this topology, arg1:total, arg2:up, arg3:down, arg4:other
			Status (str(configured|error|mixed|notStarted|started|starting|stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
			Vports (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): Virtual port information.

		Returns:
			self: This instance with matching topology data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of topology data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the topology data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AdjustPortCount(self, Arg2):
		"""Executes the adjustPortCount operation on the server.

		Adjusts the number of /vport objects in the -vports attribute by creating or deleting /vport objects and modifying the -vports attribute

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (number): The target number of /vport objects references in the /topology -vports attribute

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AdjustPortCount', payload=locals(), response_object=None)

	def FetchAndUpdateConfigFromCloud(self):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology|/api/v1/sessions/1/ixnetwork/topology|/api/v1/sessions/1/ixnetwork/topology|/api/v1/sessions/1/ixnetwork/topology?deepchild=deviceGroup|/api/v1/sessions/1/ixnetwork/topology?deepchild=deviceGroup|/api/v1/sessions/1/ixnetwork/topology?deepchild=deviceGroup)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)

	def RestartDown(self):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions in Topology that are in 'Down' state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RestartDown', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
