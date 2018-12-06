
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


class RsvpIngressRROSubObjectsList(Base):
	"""The RsvpIngressRROSubObjectsList class encapsulates a system managed rsvpIngressRROSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpIngressRROSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rsvpIngressRROSubObjectsList'

	def __init__(self, parent):
		super(RsvpIngressRROSubObjectsList, self).__init__(parent)

	@property
	def BandwidthProtection(self):
		"""Bandwidth Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtection')

	@property
	def CType(self):
		"""C-Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cType')

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
	def GlobalLabel(self):
		"""Global Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('globalLabel')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NodeProtection(self):
		"""Node Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtection')

	@property
	def ProtectionAvailable(self):
		"""Protection Available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionAvailable')

	@property
	def ProtectionInUse(self):
		"""Protection In Use

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionInUse')

	@property
	def Type(self):
		"""Reservation Style

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

	def find(self, Count=None, DescriptiveName=None, LocalIp=None, Name=None):
		"""Finds and retrieves rsvpIngressRROSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve rsvpIngressRROSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all rsvpIngressRROSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			LocalIp (list(str)): Local IP
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching rsvpIngressRROSubObjectsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rsvpIngressRROSubObjectsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rsvpIngressRROSubObjectsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, BandwidthProtection=None, CType=None, GlobalLabel=None, Ip=None, Label=None, NodeProtection=None, ProtectionAvailable=None, ProtectionInUse=None, Type=None):
		"""Base class infrastructure that gets a list of rsvpIngressRROSubObjectsList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BandwidthProtection (str): optional regex of bandwidthProtection
			CType (str): optional regex of cType
			GlobalLabel (str): optional regex of globalLabel
			Ip (str): optional regex of ip
			Label (str): optional regex of label
			NodeProtection (str): optional regex of nodeProtection
			ProtectionAvailable (str): optional regex of protectionAvailable
			ProtectionInUse (str): optional regex of protectionInUse
			Type (str): optional regex of type

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())


class RsvpIngressRroSubObjectsList(Base):
	"""The RsvpIngressRroSubObjectsList class encapsulates a system managed rsvpIngressRroSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpIngressRroSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rsvpIngressRroSubObjectsList'

	def __init__(self, parent):
		super(RsvpIngressRroSubObjectsList, self).__init__(parent)

	@property
	def BandwidthProtection(self):
		"""Bandwidth Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtection')

	@property
	def CType(self):
		"""C-Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cType')

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
	def GlobalLabel(self):
		"""Global Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('globalLabel')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NodeProtection(self):
		"""Node Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtection')

	@property
	def P2mpIdAsIp(self):
		"""P2MP ID As IP

		Returns:
			list(str)
		"""
		return self._get_attribute('p2mpIdAsIp')

	@property
	def P2mpIdAsNum(self):
		"""P2MP ID displayed in Integer format

		Returns:
			list(str)
		"""
		return self._get_attribute('p2mpIdAsNum')

	@property
	def ProtectionAvailable(self):
		"""Protection Available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionAvailable')

	@property
	def ProtectionInUse(self):
		"""Protection In Use

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionInUse')

	@property
	def Type(self):
		"""Type: IP or Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

	def find(self, Count=None, DescriptiveName=None, LocalIp=None, Name=None, P2mpIdAsIp=None, P2mpIdAsNum=None):
		"""Finds and retrieves rsvpIngressRroSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve rsvpIngressRroSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all rsvpIngressRroSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			LocalIp (list(str)): Local IP
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			P2mpIdAsIp (list(str)): P2MP ID As IP
			P2mpIdAsNum (list(str)): P2MP ID displayed in Integer format

		Returns:
			self: This instance with matching rsvpIngressRroSubObjectsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rsvpIngressRroSubObjectsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rsvpIngressRroSubObjectsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, BandwidthProtection=None, CType=None, GlobalLabel=None, Ip=None, Label=None, NodeProtection=None, ProtectionAvailable=None, ProtectionInUse=None, Type=None):
		"""Base class infrastructure that gets a list of rsvpIngressRroSubObjectsList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BandwidthProtection (str): optional regex of bandwidthProtection
			CType (str): optional regex of cType
			GlobalLabel (str): optional regex of globalLabel
			Ip (str): optional regex of ip
			Label (str): optional regex of label
			NodeProtection (str): optional regex of nodeProtection
			ProtectionAvailable (str): optional regex of protectionAvailable
			ProtectionInUse (str): optional regex of protectionInUse
			Type (str): optional regex of type

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
