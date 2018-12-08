
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


class SimRouter(Base):
	"""The SimRouter class encapsulates a system managed simRouter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SimRouter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'simRouter'

	def __init__(self, parent):
		super(SimRouter, self).__init__(parent)

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
	def IsisL3PseudoRouter(self):
		"""An instance of the IsisL3PseudoRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudorouter.IsisL3PseudoRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudorouter import IsisL3PseudoRouter
		return IsisL3PseudoRouter(self)

	@property
	def LdpPseudoRouter(self):
		"""An instance of the LdpPseudoRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldppseudorouter.LdpPseudoRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldppseudorouter import LdpPseudoRouter
		return LdpPseudoRouter(self)

	@property
	def OspfPseudoRouter(self):
		"""An instance of the OspfPseudoRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudorouter.OspfPseudoRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudorouter import OspfPseudoRouter
		return OspfPseudoRouter(self)

	@property
	def Ospfv3PseudoRouter(self):
		"""An instance of the Ospfv3PseudoRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3pseudorouter.Ospfv3PseudoRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3pseudorouter import Ospfv3PseudoRouter
		return Ospfv3PseudoRouter(self)

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
	def RouterId(self):
		"""4 Byte Router Id in dotted decimal format.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routerId')

	@property
	def SystemId(self):
		"""6 Byte System Id in hex format.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('systemId')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves simRouter data from the server.

		All named parameters support regex and can be used to selectively retrieve simRouter data from the server.
		By default the find method takes no parameters and will retrieve all simRouter data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching simRouter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of simRouter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the simRouter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, RouterId=None, SystemId=None):
		"""Base class infrastructure that gets a list of simRouter device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			RouterId (str): optional regex of routerId
			SystemId (str): optional regex of systemId

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

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
