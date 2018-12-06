
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


class OfTopologyLearnedInformation(Base):
	"""The OfTopologyLearnedInformation class encapsulates a required ofTopologyLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfTopologyLearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ofTopologyLearnedInformation'

	def __init__(self, parent):
		super(OfTopologyLearnedInformation, self).__init__(parent)

	@property
	def TopologyLearnedInfo(self):
		"""An instance of the TopologyLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.topologylearnedinfo.TopologyLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.topologylearnedinfo import TopologyLearnedInfo
		return TopologyLearnedInfo(self)

	@property
	def EnableInstallLldpFlow(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableInstallLldpFlow')
	@EnableInstallLldpFlow.setter
	def EnableInstallLldpFlow(self, value):
		self._set_attribute('enableInstallLldpFlow', value)

	@property
	def EnableRefreshLldpLearnedInformation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRefreshLldpLearnedInformation')
	@EnableRefreshLldpLearnedInformation.setter
	def EnableRefreshLldpLearnedInformation(self, value):
		self._set_attribute('enableRefreshLldpLearnedInformation', value)

	@property
	def IsOfTopologyLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isOfTopologyLearnedInformationRefreshed')

	@property
	def LldpDestinationMac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lldpDestinationMac')
	@LldpDestinationMac.setter
	def LldpDestinationMac(self, value):
		self._set_attribute('lldpDestinationMac', value)

	@property
	def LldpResponseTimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lldpResponseTimeOut')
	@LldpResponseTimeOut.setter
	def LldpResponseTimeOut(self, value):
		self._set_attribute('lldpResponseTimeOut', value)

	def RefreshOfTopology(self):
		"""Executes the refreshOfTopology operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofTopologyLearnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			number: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshOfTopology', payload=locals(), response_object=None)
