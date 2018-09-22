from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Multicast(Base):
	"""The Multicast class encapsulates a required multicast node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Multicast property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'multicast'

	def __init__(self, parent):
		super(Multicast, self).__init__(parent)

	@property
	def Cluster(self):
		"""An instance of the Cluster class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cluster.Cluster)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cluster import Cluster
		return Cluster(self)._select()

	@property
	def RouteDistinguisher(self):
		"""An instance of the RouteDistinguisher class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.routedistinguisher.RouteDistinguisher)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.routedistinguisher import RouteDistinguisher
		return RouteDistinguisher(self)._select()

	@property
	def EnableMulticast(self):
		"""Enables the use of Multicast VRFs (MVRFs). (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableMulticast')
	@EnableMulticast.setter
	def EnableMulticast(self, value):
		self._set_attribute('enableMulticast', value)

	@property
	def EnableMulticastCluster(self):
		"""If true, enables the use of BGP route reflection clusters for multicast VPN route distribution. (default = false)

		Returns:
			bool
		"""
		return self._get_attribute('enableMulticastCluster')
	@EnableMulticastCluster.setter
	def EnableMulticastCluster(self, value):
		self._set_attribute('enableMulticastCluster', value)

	@property
	def GroupAddress(self):
		"""The IP address for the Multicast Group. The default value is the default MDT group address, used as the Multicast Group address used as the destination for the MVPN tunnel. (default = 239.1.1.1

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')
	@GroupAddress.setter
	def GroupAddress(self, value):
		self._set_attribute('groupAddress', value)
