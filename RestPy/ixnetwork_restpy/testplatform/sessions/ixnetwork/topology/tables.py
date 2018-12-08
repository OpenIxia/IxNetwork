
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


class Tables(Base):
	"""The Tables class encapsulates a system managed tables node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Tables property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tables'

	def __init__(self, parent):
		super(Tables, self).__init__(parent)

	@property
	def FlowSet(self):
		"""An instance of the FlowSet class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.flowset.FlowSet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.flowset import FlowSet
		return FlowSet(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ChannelIndex(self):
		"""Parent Channel Index

		Returns:
			list(str)
		"""
		return self._get_attribute('channelIndex')

	@property
	def ChannelRemoteIp(self):
		"""The remote IP address of the OF Channel. This field is auto-populated and cannot be changed.

		Returns:
			list(str)
		"""
		return self._get_attribute('channelRemoteIp')

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
	def NumberOfFlowSet(self):
		"""Specify the number of Flow Set for this controller configuration.

		Returns:
			number
		"""
		return self._get_attribute('numberOfFlowSet')
	@NumberOfFlowSet.setter
	def NumberOfFlowSet(self, value):
		self._set_attribute('numberOfFlowSet', value)

	@property
	def TableId(self):
		"""Specify the controller table identifier. Lower numbered tables are consulted first.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableId')

	@property
	def TableName(self):
		"""Specify the name of the controller table.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tableName')

	def find(self, ChannelIndex=None, ChannelRemoteIp=None, Count=None, DescriptiveName=None, Name=None, NumberOfFlowSet=None):
		"""Finds and retrieves tables data from the server.

		All named parameters support regex and can be used to selectively retrieve tables data from the server.
		By default the find method takes no parameters and will retrieve all tables data from the server.

		Args:
			ChannelIndex (list(str)): Parent Channel Index
			ChannelRemoteIp (list(str)): The remote IP address of the OF Channel. This field is auto-populated and cannot be changed.
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfFlowSet (number): Specify the number of Flow Set for this controller configuration.

		Returns:
			self: This instance with matching tables data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tables data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tables data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, Active=None, TableId=None, TableName=None):
		"""Base class infrastructure that gets a list of tables device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			TableId (str): optional regex of tableId
			TableName (str): optional regex of tableName

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
