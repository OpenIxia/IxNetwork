
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


class HostTopologyLearnedInformation(Base):
	"""The HostTopologyLearnedInformation class encapsulates a required hostTopologyLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the HostTopologyLearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'hostTopologyLearnedInformation'

	def __init__(self, parent):
		super(HostTopologyLearnedInformation, self).__init__(parent)

	@property
	def SwitchHostRangeLearnedInfo(self):
		"""An instance of the SwitchHostRangeLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfo.SwitchHostRangeLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfo import SwitchHostRangeLearnedInfo
		return SwitchHostRangeLearnedInfo(self)

	@property
	def SwitchHostRangeLearnedInfoTriggerAttributes(self):
		"""An instance of the SwitchHostRangeLearnedInfoTriggerAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfotriggerattributes.SwitchHostRangeLearnedInfoTriggerAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangelearnedinfotriggerattributes import SwitchHostRangeLearnedInfoTriggerAttributes
		return SwitchHostRangeLearnedInfoTriggerAttributes(self)._select()

	def RefreshHostRangeLearnedInformation(self):
		"""Executes the refreshHostRangeLearnedInformation operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=hostTopologyLearnedInformation)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshHostRangeLearnedInformation', payload=locals(), response_object=None)
