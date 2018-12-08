
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


class IsisMappingServerIPV4List(Base):
	"""The IsisMappingServerIPV4List class encapsulates a required isisMappingServerIPV4List node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IsisMappingServerIPV4List property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'isisMappingServerIPV4List'

	def __init__(self, parent):
		super(IsisMappingServerIPV4List, self).__init__(parent)

	@property
	def AFlag(self):
		"""Attached flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('aFlag')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Algorithm(self):
		"""Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('algorithm')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DFlag(self):
		"""When the SID/Label Binding TLV is leaked from level-2 to level-1, this flag MUST be set, else it should be clear

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dFlag')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EFlag(self):
		"""Explicit NULL flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlag')

	@property
	def FECPrefix(self):
		"""IPv4 FEC Prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fECPrefix')

	@property
	def LFlag(self):
		"""Local Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def LastFECAddress(self):
		"""Last IPv4 FEC Address

		Returns:
			list(str)
		"""
		return self._get_attribute('lastFECAddress')

	@property
	def MFlag(self):
		"""Mirror Context flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mFlag')

	@property
	def NFlag(self):
		"""N Flag: Indicates the nodal prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nFlag')

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
	def PFlag(self):
		"""P Flag: Indicates that to reach to a prefix, this router would be penultimate hop.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pFlag')

	@property
	def PrefixLength(self):
		"""Length of the IPv4 FEC prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def RFlag(self):
		"""Redistribution flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rFlag')

	@property
	def Range(self):
		"""This the count of continuous IPv4 address prefixes and their respective continuous SID/labels

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('range')

	@property
	def SFlag(self):
		"""Enabling this flag lets the SID/Label Binding TLV to get flooded across the entire routing domain, else this TLV should not be leaked between levels

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sFlag')

	@property
	def StartSIDLabel(self):
		"""Starting value of SID/ Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startSIDLabel')

	@property
	def VFlag(self):
		"""Value Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

	@property
	def Weight(self):
		"""Weight

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')

	def get_device_ids(self, PortNames=None, AFlag=None, Active=None, Algorithm=None, DFlag=None, EFlag=None, FECPrefix=None, LFlag=None, MFlag=None, NFlag=None, PFlag=None, PrefixLength=None, RFlag=None, Range=None, SFlag=None, StartSIDLabel=None, VFlag=None, Weight=None):
		"""Base class infrastructure that gets a list of isisMappingServerIPV4List device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AFlag (str): optional regex of aFlag
			Active (str): optional regex of active
			Algorithm (str): optional regex of algorithm
			DFlag (str): optional regex of dFlag
			EFlag (str): optional regex of eFlag
			FECPrefix (str): optional regex of fECPrefix
			LFlag (str): optional regex of lFlag
			MFlag (str): optional regex of mFlag
			NFlag (str): optional regex of nFlag
			PFlag (str): optional regex of pFlag
			PrefixLength (str): optional regex of prefixLength
			RFlag (str): optional regex of rFlag
			Range (str): optional regex of range
			SFlag (str): optional regex of sFlag
			StartSIDLabel (str): optional regex of startSIDLabel
			VFlag (str): optional regex of vFlag
			Weight (str): optional regex of weight

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def Advertise(self, Arg2):
		"""Executes the advertise operation on the server.

		Advertise the V4 Mapping Server Range TLVs

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Advertise', payload=locals(), response_object=None)

	def Withdraw(self, Arg2):
		"""Executes the withdraw operation on the server.

		Withdraw the V4 Mapping Server Range TLVs

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin.An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Withdraw', payload=locals(), response_object=None)
