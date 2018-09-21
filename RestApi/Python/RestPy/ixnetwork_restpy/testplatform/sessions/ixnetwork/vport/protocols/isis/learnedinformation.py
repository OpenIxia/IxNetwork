from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInformation(Base):
	"""The LearnedInformation class encapsulates a required learnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInformation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedInformation'

	def __init__(self, parent):
		super(LearnedInformation, self).__init__(parent)

	@property
	def Ipv4Multicast(self):
		"""An instance of the Ipv4Multicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv4multicast.Ipv4Multicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv4multicast import Ipv4Multicast
		return Ipv4Multicast(self)

	@property
	def Ipv4Prefixes(self):
		"""An instance of the Ipv4Prefixes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv4prefixes.Ipv4Prefixes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv4prefixes import Ipv4Prefixes
		return Ipv4Prefixes(self)

	@property
	def Ipv6Multicast(self):
		"""An instance of the Ipv6Multicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv6multicast.Ipv6Multicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv6multicast import Ipv6Multicast
		return Ipv6Multicast(self)

	@property
	def Ipv6Prefixes(self):
		"""An instance of the Ipv6Prefixes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv6prefixes.Ipv6Prefixes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.ipv6prefixes import Ipv6Prefixes
		return Ipv6Prefixes(self)

	@property
	def MacMulticast(self):
		"""An instance of the MacMulticast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.macmulticast.MacMulticast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.macmulticast import MacMulticast
		return MacMulticast(self)

	@property
	def RBridges(self):
		"""An instance of the RBridges class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.rbridges.RBridges)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.rbridges import RBridges
		return RBridges(self)

	@property
	def SpbRbridges(self):
		"""An instance of the SpbRbridges class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbrbridges.SpbRbridges)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbrbridges import SpbRbridges
		return SpbRbridges(self)

	@property
	def TrillMacUnicast(self):
		"""An instance of the TrillMacUnicast class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillmacunicast.TrillMacUnicast)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trillmacunicast import TrillMacUnicast
		return TrillMacUnicast(self)

	@property
	def TrillOamPing(self):
		"""An instance of the TrillOamPing class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trilloamping.TrillOamPing)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.trilloamping import TrillOamPing
		return TrillOamPing(self)
