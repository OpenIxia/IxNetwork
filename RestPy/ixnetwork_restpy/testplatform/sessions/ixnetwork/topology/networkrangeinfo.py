
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


class NetworkRangeInfo(Base):
	"""The NetworkRangeInfo class encapsulates a user managed networkRangeInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NetworkRangeInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'networkRangeInfo'

	def __init__(self, parent):
		super(NetworkRangeInfo, self).__init__(parent)

	@property
	def CMacProperties(self):
		"""An instance of the CMacProperties class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return CMacProperties(self)

	@property
	def EvpnIPv4PrefixRange(self):
		"""An instance of the EvpnIPv4PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return EvpnIPv4PrefixRange(self)

	@property
	def EvpnIPv6PrefixRange(self):
		"""An instance of the EvpnIPv6PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return EvpnIPv6PrefixRange(self)

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
	def NetworkRangeIPByMask(self):
		"""Use mask to generate range of addresses

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeIPByMask')

	@property
	def NetworkRangeInterfaceIp(self):
		"""Interface IP address for a non-connected interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeInterfaceIp')

	@property
	def NetworkRangeInterfaceIpMask(self):
		"""Interface IP mask for a non-connected interface

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeInterfaceIpMask')

	@property
	def NetworkRangeIp(self):
		"""Network Range IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeIp')

	@property
	def NetworkRangeIpIncrementBy(self):
		"""Network Range IP Increment By

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeIpIncrementBy')

	@property
	def NetworkRangeIpMask(self):
		"""Network Range IP Mask

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeIpMask')

	@property
	def NetworkRangeLinkType(self):
		"""Link Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeLinkType')

	@property
	def NetworkRangeRID(self):
		"""Network Range RID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeRID')

	@property
	def NetworkRangeRIDIncrement(self):
		"""Network Range RID Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkRangeRIDIncrement')

	@property
	def NumColumns(self):
		"""4 Byte Integer.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numColumns')

	@property
	def NumRows(self):
		"""4 Byte Integer.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numRows')

	def add(self, Name=None):
		"""Adds a new networkRangeInfo node on the server and retrieves it in this instance.

		Args:
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with all currently retrieved networkRangeInfo data using find and the newly added networkRangeInfo data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the networkRangeInfo data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves networkRangeInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve networkRangeInfo data from the server.
		By default the find method takes no parameters and will retrieve all networkRangeInfo data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching networkRangeInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of networkRangeInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the networkRangeInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, NetworkRangeIPByMask=None, NetworkRangeInterfaceIp=None, NetworkRangeInterfaceIpMask=None, NetworkRangeIp=None, NetworkRangeIpIncrementBy=None, NetworkRangeIpMask=None, NetworkRangeLinkType=None, NetworkRangeRID=None, NetworkRangeRIDIncrement=None, NumColumns=None, NumRows=None):
		"""Base class infrastructure that gets a list of networkRangeInfo device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			NetworkRangeIPByMask (str): optional regex of networkRangeIPByMask
			NetworkRangeInterfaceIp (str): optional regex of networkRangeInterfaceIp
			NetworkRangeInterfaceIpMask (str): optional regex of networkRangeInterfaceIpMask
			NetworkRangeIp (str): optional regex of networkRangeIp
			NetworkRangeIpIncrementBy (str): optional regex of networkRangeIpIncrementBy
			NetworkRangeIpMask (str): optional regex of networkRangeIpMask
			NetworkRangeLinkType (str): optional regex of networkRangeLinkType
			NetworkRangeRID (str): optional regex of networkRangeRID
			NetworkRangeRIDIncrement (str): optional regex of networkRangeRIDIncrement
			NumColumns (str): optional regex of numColumns
			NumRows (str): optional regex of numRows

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
