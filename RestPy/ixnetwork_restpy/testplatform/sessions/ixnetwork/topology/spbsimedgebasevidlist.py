
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


class SpbSimEdgeBaseVidList(Base):
	"""The SpbSimEdgeBaseVidList class encapsulates a required spbSimEdgeBaseVidList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbSimEdgeBaseVidList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'spbSimEdgeBaseVidList'

	def __init__(self, parent):
		super(SpbSimEdgeBaseVidList, self).__init__(parent)

	@property
	def SpbSimEdgeIsidList(self):
		"""An instance of the SpbSimEdgeIsidList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgeisidlist.SpbSimEdgeIsidList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgeisidlist import SpbSimEdgeIsidList
		return SpbSimEdgeIsidList(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BaseVid(self):
		"""Base VID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('baseVid')

	@property
	def BaseVlanPriority(self):
		"""B-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('baseVlanPriority')

	@property
	def BvlanTpid(self):
		"""B-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bvlanTpid')

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
	def EctAlgorithm(self):
		"""ECT AlgorithmType

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ectAlgorithm')

	@property
	def IsidCount(self):
		"""ISID Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('isidCount')
	@IsidCount.setter
	def IsidCount(self, value):
		self._set_attribute('isidCount', value)

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
	def UseFlagBit(self):
		"""Use Flag Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useFlagBit')

	def get_device_ids(self, PortNames=None, Active=None, BaseVid=None, BaseVlanPriority=None, BvlanTpid=None, EctAlgorithm=None, UseFlagBit=None):
		"""Base class infrastructure that gets a list of spbSimEdgeBaseVidList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			BaseVid (str): optional regex of baseVid
			BaseVlanPriority (str): optional regex of baseVlanPriority
			BvlanTpid (str): optional regex of bvlanTpid
			EctAlgorithm (str): optional regex of ectAlgorithm
			UseFlagBit (str): optional regex of useFlagBit

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
