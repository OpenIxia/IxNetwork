
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


class PccLearnedLspDb(Base):
	"""The PccLearnedLspDb class encapsulates a required pccLearnedLspDb node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PccLearnedLspDb property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pccLearnedLspDb'

	def __init__(self, parent):
		super(PccLearnedLspDb, self).__init__(parent)

	@property
	def DestIpv4Address(self):
		"""An instance of the DestIpv4Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv4address.DestIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv4address import DestIpv4Address
		return DestIpv4Address(self)._select()

	@property
	def DestIpv6Address(self):
		"""An instance of the DestIpv6Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv6address.DestIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.destipv6address import DestIpv6Address
		return DestIpv6Address(self)._select()

	@property
	def ErrorInfo(self):
		"""An instance of the ErrorInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.errorinfo.ErrorInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.errorinfo import ErrorInfo
		return ErrorInfo(self)._select()

	@property
	def IpVersion(self):
		"""An instance of the IpVersion class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipversion.IpVersion)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipversion import IpVersion
		return IpVersion(self)._select()

	@property
	def Ipv4NodeId(self):
		"""An instance of the Ipv4NodeId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4nodeid.Ipv4NodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv4nodeid import Ipv4NodeId
		return Ipv4NodeId(self)._select()

	@property
	def Ipv6NodeId(self):
		"""An instance of the Ipv6NodeId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6nodeid.Ipv6NodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ipv6nodeid import Ipv6NodeId
		return Ipv6NodeId(self)._select()

	@property
	def LearnedLspIndex(self):
		"""An instance of the LearnedLspIndex class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedlspindex.LearnedLspIndex)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedlspindex import LearnedLspIndex
		return LearnedLspIndex(self)._select()

	@property
	def LearnedMsgDbType(self):
		"""An instance of the LearnedMsgDbType class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedmsgdbtype.LearnedMsgDbType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedmsgdbtype import LearnedMsgDbType
		return LearnedMsgDbType(self)._select()

	@property
	def LocalIntefaceId(self):
		"""An instance of the LocalIntefaceId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localintefaceid.LocalIntefaceId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localintefaceid import LocalIntefaceId
		return LocalIntefaceId(self)._select()

	@property
	def LocalIpv4Address(self):
		"""An instance of the LocalIpv4Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv4address.LocalIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv4address import LocalIpv4Address
		return LocalIpv4Address(self)._select()

	@property
	def LocalIpv6Address(self):
		"""An instance of the LocalIpv6Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv6address.LocalIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localipv6address import LocalIpv6Address
		return LocalIpv6Address(self)._select()

	@property
	def LocalNodeId(self):
		"""An instance of the LocalNodeId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localnodeid.LocalNodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.localnodeid import LocalNodeId
		return LocalNodeId(self)._select()

	@property
	def MplsLabel(self):
		"""An instance of the MplsLabel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplslabel.MplsLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.mplslabel import MplsLabel
		return MplsLabel(self)._select()

	@property
	def PlspId(self):
		"""An instance of the PlspId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.plspid.PlspId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.plspid import PlspId
		return PlspId(self)._select()

	@property
	def RemoteInterfaceId(self):
		"""An instance of the RemoteInterfaceId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteinterfaceid.RemoteInterfaceId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteinterfaceid import RemoteInterfaceId
		return RemoteInterfaceId(self)._select()

	@property
	def RemoteIpv4Address(self):
		"""An instance of the RemoteIpv4Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv4address.RemoteIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv4address import RemoteIpv4Address
		return RemoteIpv4Address(self)._select()

	@property
	def RemoteIpv6Address(self):
		"""An instance of the RemoteIpv6Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv6address.RemoteIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remoteipv6address import RemoteIpv6Address
		return RemoteIpv6Address(self)._select()

	@property
	def RemoteNodeId(self):
		"""An instance of the RemoteNodeId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remotenodeid.RemoteNodeId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.remotenodeid import RemoteNodeId
		return RemoteNodeId(self)._select()

	@property
	def RequestId(self):
		"""An instance of the RequestId class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestid.RequestId)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.requestid import RequestId
		return RequestId(self)._select()

	@property
	def Sid(self):
		"""An instance of the Sid class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sid.Sid)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sid import Sid
		return Sid(self)._select()

	@property
	def SidType(self):
		"""An instance of the SidType class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype.SidType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype import SidType
		return SidType(self)._select()

	@property
	def SidType(self):
		"""An instance of the SidType class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype.SidType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sidtype import SidType
		return SidType(self)._select()

	@property
	def SourceIpv4Address(self):
		"""An instance of the SourceIpv4Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv4address.SourceIpv4Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv4address import SourceIpv4Address
		return SourceIpv4Address(self)._select()

	@property
	def SourceIpv6Address(self):
		"""An instance of the SourceIpv6Address class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv6address.SourceIpv6Address)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.sourceipv6address import SourceIpv6Address
		return SourceIpv6Address(self)._select()

	@property
	def SymbolicPathName(self):
		"""An instance of the SymbolicPathName class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.symbolicpathname.SymbolicPathName)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.symbolicpathname import SymbolicPathName
		return SymbolicPathName(self)._select()

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
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)
