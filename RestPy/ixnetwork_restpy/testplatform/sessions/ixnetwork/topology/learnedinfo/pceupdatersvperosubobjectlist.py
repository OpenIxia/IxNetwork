
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


class PceUpdateRsvpEroSubObjectList(Base):
	"""The PceUpdateRsvpEroSubObjectList class encapsulates a system managed pceUpdateRsvpEroSubObjectList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceUpdateRsvpEroSubObjectList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceUpdateRsvpEroSubObjectList'

	def __init__(self, parent):
		super(PceUpdateRsvpEroSubObjectList, self).__init__(parent)

	@property
	def ActiveThisEro(self):
		"""Controls whether the ERO sub-object will be sent in the PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('activeThisEro')

	@property
	def AsNumber(self):
		"""AS Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber')

	@property
	def Ipv4Prefix(self):
		"""IPv4 Prefix is specified as an IPv4 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Prefix')

	@property
	def Ipv6Prefix(self):
		"""IPv6 Prefix is specified as an IPv6 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Prefix')

	@property
	def LooseHop(self):
		"""Indicates if user wants to represent a loose-hop sub object in the LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('looseHop')

	@property
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def SubObjectType(self):
		"""Using the Sub Object Type control user can configure which sub object needs to be included from the following options: Not Applicable IPv4 Prefix IPv6 Prefix AS Number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subObjectType')

	def find(self):
		"""Finds and retrieves pceUpdateRsvpEroSubObjectList data from the server.

		All named parameters support regex and can be used to selectively retrieve pceUpdateRsvpEroSubObjectList data from the server.
		By default the find method takes no parameters and will retrieve all pceUpdateRsvpEroSubObjectList data from the server.

		Returns:
			self: This instance with matching pceUpdateRsvpEroSubObjectList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceUpdateRsvpEroSubObjectList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceUpdateRsvpEroSubObjectList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, ActiveThisEro=None, AsNumber=None, Ipv4Prefix=None, Ipv6Prefix=None, LooseHop=None, PrefixLength=None, SubObjectType=None):
		"""Base class infrastructure that gets a list of pceUpdateRsvpEroSubObjectList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ActiveThisEro (str): optional regex of activeThisEro
			AsNumber (str): optional regex of asNumber
			Ipv4Prefix (str): optional regex of ipv4Prefix
			Ipv6Prefix (str): optional regex of ipv6Prefix
			LooseHop (str): optional regex of looseHop
			PrefixLength (str): optional regex of prefixLength
			SubObjectType (str): optional regex of subObjectType

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
