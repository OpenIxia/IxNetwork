
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


class InterfaceGroup(Base):
	"""The InterfaceGroup class encapsulates a user managed interfaceGroup node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InterfaceGroup property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interfaceGroup'

	def __init__(self, parent):
		super(InterfaceGroup, self).__init__(parent)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.interfacegroup.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.interfacegroup.interface.interface import Interface
		return Interface(self)

	@property
	def AtmEncapsulation(self):
		"""

		Returns:
			str(vcMuxIpv4Routed|vcMuxIpv6Routed|vcMuxBridgedEth802p3WithFcs|vcMuxBridgedEth802p3WithOutFcs|llcRoutedAal5Snap|llcBridgedEthernetWithFcs|llcBridgedEthernetWithoutFcs)
		"""
		return self._get_attribute('atmEncapsulation')
	@AtmEncapsulation.setter
	def AtmEncapsulation(self, value):
		self._set_attribute('atmEncapsulation', value)

	@property
	def Description(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def EnableVlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Ip(self):
		"""

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('ip')
	@Ip.setter
	def Ip(self, value):
		self._set_attribute('ip', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, AtmEncapsulation=None, Description=None, EnableVlan=None, Enabled=None, Ip=None, TrafficGroupId=None):
		"""Adds a new interfaceGroup node on the server and retrieves it in this instance.

		Args:
			AtmEncapsulation (str(vcMuxIpv4Routed|vcMuxIpv6Routed|vcMuxBridgedEth802p3WithFcs|vcMuxBridgedEth802p3WithOutFcs|llcRoutedAal5Snap|llcBridgedEthernetWithFcs|llcBridgedEthernetWithoutFcs)): 
			Description (str): 
			EnableVlan (bool): 
			Enabled (bool): 
			Ip (str(ipv4|ipv6)): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with all currently retrieved interfaceGroup data using find and the newly added interfaceGroup data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interfaceGroup data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AtmEncapsulation=None, Description=None, EnableVlan=None, Enabled=None, Ip=None, TrafficGroupId=None):
		"""Finds and retrieves interfaceGroup data from the server.

		All named parameters support regex and can be used to selectively retrieve interfaceGroup data from the server.
		By default the find method takes no parameters and will retrieve all interfaceGroup data from the server.

		Args:
			AtmEncapsulation (str(vcMuxIpv4Routed|vcMuxIpv6Routed|vcMuxBridgedEth802p3WithFcs|vcMuxBridgedEth802p3WithOutFcs|llcRoutedAal5Snap|llcBridgedEthernetWithFcs|llcBridgedEthernetWithoutFcs)): 
			Description (str): 
			EnableVlan (bool): 
			Enabled (bool): 
			Ip (str(ipv4|ipv6)): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with matching interfaceGroup data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interfaceGroup data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interfaceGroup data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
