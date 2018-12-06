
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


class LdpRootRangeV6(Base):
	"""The LdpRootRangeV6 class encapsulates a required ldpRootRangeV6 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LdpRootRangeV6 property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ldpRootRangeV6'

	def __init__(self, parent):
		super(LdpRootRangeV6, self).__init__(parent)

	@property
	def LdpTLVList(self):
		"""An instance of the LdpTLVList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptlvlist.LdpTLVList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptlvlist import LdpTLVList
		return LdpTLVList(self)

	@property
	def ContinuousIncrementOVAcrossRoot(self):
		"""Continuous Increment Opaque Value Across Root

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('continuousIncrementOVAcrossRoot')

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
	def FilterOnGroupAddress(self):
		"""If selected, all the LSPs will belong to the same set of groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterOnGroupAddress')

	@property
	def GroupCountPerLSP(self):
		"""Group Count Per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCountPerLSP')

	@property
	def LspCountPerRoot(self):
		"""LSP Count Per Root

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspCountPerRoot')

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
	def NumberOfTLVs(self):
		"""Number Of TLVs

		Returns:
			number
		"""
		return self._get_attribute('numberOfTLVs')
	@NumberOfTLVs.setter
	def NumberOfTLVs(self, value):
		self._set_attribute('numberOfTLVs', value)

	@property
	def RootAddress(self):
		"""Root Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddress')

	@property
	def RootAddressCount(self):
		"""Root Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddressCount')

	@property
	def RootAddressStep(self):
		"""Root Address Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddressStep')

	@property
	def SourceAddressV4(self):
		"""IPv4 Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressV4')

	@property
	def SourceAddressV6(self):
		"""IPv6 Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressV6')

	@property
	def SourceCountPerLSP(self):
		"""Source Count Per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceCountPerLSP')

	@property
	def StartGroupAddressV4(self):
		"""Start Group Address(V4)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressV4')

	@property
	def StartGroupAddressV6(self):
		"""Start Group Address(V6)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressV6')

	def get_device_ids(self, PortNames=None, ContinuousIncrementOVAcrossRoot=None, FilterOnGroupAddress=None, GroupCountPerLSP=None, LspCountPerRoot=None, RootAddress=None, RootAddressCount=None, RootAddressStep=None, SourceAddressV4=None, SourceAddressV6=None, SourceCountPerLSP=None, StartGroupAddressV4=None, StartGroupAddressV6=None):
		"""Base class infrastructure that gets a list of ldpRootRangeV6 device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ContinuousIncrementOVAcrossRoot (str): optional regex of continuousIncrementOVAcrossRoot
			FilterOnGroupAddress (str): optional regex of filterOnGroupAddress
			GroupCountPerLSP (str): optional regex of groupCountPerLSP
			LspCountPerRoot (str): optional regex of lspCountPerRoot
			RootAddress (str): optional regex of rootAddress
			RootAddressCount (str): optional regex of rootAddressCount
			RootAddressStep (str): optional regex of rootAddressStep
			SourceAddressV4 (str): optional regex of sourceAddressV4
			SourceAddressV6 (str): optional regex of sourceAddressV6
			SourceCountPerLSP (str): optional regex of sourceCountPerLSP
			StartGroupAddressV4 (str): optional regex of startGroupAddressV4
			StartGroupAddressV6 (str): optional regex of startGroupAddressV6

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
