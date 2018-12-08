
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


class InterestedVlanList(Base):
	"""The InterestedVlanList class encapsulates a required interestedVlanList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InterestedVlanList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interestedVlanList'

	def __init__(self, parent):
		super(InterestedVlanList, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def IncludeInLSP(self):
		"""Include in LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeInLSP')

	@property
	def IncludeInMGroupPDU(self):
		"""Include in MGROUP-PDU

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeInMGroupPDU')

	@property
	def M4BitEnabled(self):
		"""M4 Bit Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('m4BitEnabled')

	@property
	def M6BitEnabled(self):
		"""M6 Bit Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('m6BitEnabled')

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
	def Nickname(self):
		"""Nickname

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nickname')

	@property
	def NoOfSpanningTreeRoots(self):
		"""No. of Spanning Tree Roots

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('noOfSpanningTreeRoots')

	@property
	def StartSpanningTreeRootBridgeId(self):
		"""Start Spanning Tree Root Bridge ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startSpanningTreeRootBridgeId')

	@property
	def StartVlanId(self):
		"""Start Vlan Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startVlanId')

	@property
	def VlanCount(self):
		"""Vlan Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanCount')

	@property
	def VlanIdIncr(self):
		"""Vlan Id Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanIdIncr')

	def get_device_ids(self, PortNames=None, Active=None, IncludeInLSP=None, IncludeInMGroupPDU=None, M4BitEnabled=None, M6BitEnabled=None, Nickname=None, NoOfSpanningTreeRoots=None, StartSpanningTreeRootBridgeId=None, StartVlanId=None, VlanCount=None, VlanIdIncr=None):
		"""Base class infrastructure that gets a list of interestedVlanList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			IncludeInLSP (str): optional regex of includeInLSP
			IncludeInMGroupPDU (str): optional regex of includeInMGroupPDU
			M4BitEnabled (str): optional regex of m4BitEnabled
			M6BitEnabled (str): optional regex of m6BitEnabled
			Nickname (str): optional regex of nickname
			NoOfSpanningTreeRoots (str): optional regex of noOfSpanningTreeRoots
			StartSpanningTreeRootBridgeId (str): optional regex of startSpanningTreeRootBridgeId
			StartVlanId (str): optional regex of startVlanId
			VlanCount (str): optional regex of vlanCount
			VlanIdIncr (str): optional regex of vlanIdIncr

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
