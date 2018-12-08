
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


class PceXroSubObjectsList(Base):
	"""The PceXroSubObjectsList class encapsulates a system managed pceXroSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PceXroSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pceXroSubObjectsList'

	def __init__(self, parent):
		super(PceXroSubObjectsList, self).__init__(parent)

	@property
	def Active(self):
		"""Controls whether the XRO sub-object will be sent in the PCRequest message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AsNumber(self):
		"""AS Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber')

	@property
	def Attribute(self):
		"""Indicates how the exclusion subobject is to be indicated

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('attribute')

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
	def Exclude_bit(self):
		"""Indicates whether the exclusion is mandatory or desired.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('exclude_bit')

	@property
	def InterfaceId(self):
		"""Interface ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interfaceId')

	@property
	def Ipv4Address(self):
		"""IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Address')

	@property
	def Ipv6Address(self):
		"""IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Address')

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
	def PceId128(self):
		"""128 bit PKS ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pceId128')

	@property
	def PceId32(self):
		"""32 bit PKS ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pceId32')

	@property
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def RouterId(self):
		"""Router ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routerId')

	@property
	def SrlgId(self):
		"""SRLG ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srlgId')

	@property
	def SubObjectType(self):
		"""Using the Sub Object Type control user can configure which sub object needs to be included from the following options: IPv4 Prefix IPv6 Prefix Unnumbered Interface ID AS Number. SRLG

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subObjectType')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves pceXroSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve pceXroSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all pceXroSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching pceXroSubObjectsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pceXroSubObjectsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pceXroSubObjectsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, Active=None, AsNumber=None, Attribute=None, Exclude_bit=None, InterfaceId=None, Ipv4Address=None, Ipv6Address=None, PceId128=None, PceId32=None, PrefixLength=None, RouterId=None, SrlgId=None, SubObjectType=None):
		"""Base class infrastructure that gets a list of pceXroSubObjectsList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AsNumber (str): optional regex of asNumber
			Attribute (str): optional regex of attribute
			Exclude_bit (str): optional regex of exclude_bit
			InterfaceId (str): optional regex of interfaceId
			Ipv4Address (str): optional regex of ipv4Address
			Ipv6Address (str): optional regex of ipv6Address
			PceId128 (str): optional regex of pceId128
			PceId32 (str): optional regex of pceId32
			PrefixLength (str): optional regex of prefixLength
			RouterId (str): optional regex of routerId
			SrlgId (str): optional regex of srlgId
			SubObjectType (str): optional regex of subObjectType

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
