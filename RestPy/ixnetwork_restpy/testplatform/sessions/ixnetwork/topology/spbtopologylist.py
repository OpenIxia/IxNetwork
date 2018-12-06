
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


class SpbTopologyList(Base):
	"""The SpbTopologyList class encapsulates a required spbTopologyList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbTopologyList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'spbTopologyList'

	def __init__(self, parent):
		super(SpbTopologyList, self).__init__(parent)

	@property
	def BaseVidList(self):
		"""An instance of the BaseVidList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.basevidlist.BaseVidList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.basevidlist import BaseVidList
		return BaseVidList(self)._select()

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AuxMcidConfName(self):
		"""Aux MCID Config Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxMcidConfName')

	@property
	def AuxMcidSignature(self):
		"""Aux MCID Signature

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxMcidSignature')

	@property
	def BaseVidCount(self):
		"""Base VID Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('baseVidCount')
	@BaseVidCount.setter
	def BaseVidCount(self, value):
		self._set_attribute('baseVidCount', value)

	@property
	def BridgePriority(self):
		"""Bridge Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bridgePriority')

	@property
	def CistExternalRootCost(self):
		"""CIST External Root Cost

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cistExternalRootCost')

	@property
	def CistRootId(self):
		"""CIST Root Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cistRootId')

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
	def LinkMetric(self):
		"""Link Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkMetric')

	@property
	def McidConfName(self):
		"""MCID Config Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mcidConfName')

	@property
	def McidSignature(self):
		"""MCID Signature

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mcidSignature')

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
	def NumberOfPorts(self):
		"""Number of Ports

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def PortIdentifier(self):
		"""Port Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portIdentifier')

	@property
	def SpSourceId(self):
		"""SP Source ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('spSourceId')

	@property
	def TopologyId(self):
		"""Topology Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('topologyId')

	@property
	def Vbit(self):
		"""Enable V Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vbit')

	def get_device_ids(self, PortNames=None, Active=None, AuxMcidConfName=None, AuxMcidSignature=None, BridgePriority=None, CistExternalRootCost=None, CistRootId=None, LinkMetric=None, McidConfName=None, McidSignature=None, NumberOfPorts=None, PortIdentifier=None, SpSourceId=None, TopologyId=None, Vbit=None):
		"""Base class infrastructure that gets a list of spbTopologyList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			AuxMcidConfName (str): optional regex of auxMcidConfName
			AuxMcidSignature (str): optional regex of auxMcidSignature
			BridgePriority (str): optional regex of bridgePriority
			CistExternalRootCost (str): optional regex of cistExternalRootCost
			CistRootId (str): optional regex of cistRootId
			LinkMetric (str): optional regex of linkMetric
			McidConfName (str): optional regex of mcidConfName
			McidSignature (str): optional regex of mcidSignature
			NumberOfPorts (str): optional regex of numberOfPorts
			PortIdentifier (str): optional regex of portIdentifier
			SpSourceId (str): optional regex of spSourceId
			TopologyId (str): optional regex of topologyId
			Vbit (str): optional regex of vbit

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
