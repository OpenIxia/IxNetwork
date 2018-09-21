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
		"""If true, Install Flow in Switch for LLDP Packets to explicitly send to Controller.

		Returns:
			bool
		"""
		return self._get_attribute('enableInstallLldpFlow')
	@EnableInstallLldpFlow.setter
	def EnableInstallLldpFlow(self, value):
		self._set_attribute('enableInstallLldpFlow', value)

	@property
	def EnableRefreshLldpLearnedInformation(self):
		"""If true, the LLDP trigger configuration parameters are available.

		Returns:
			bool
		"""
		return self._get_attribute('enableRefreshLldpLearnedInformation')
	@EnableRefreshLldpLearnedInformation.setter
	def EnableRefreshLldpLearnedInformation(self, value):
		self._set_attribute('enableRefreshLldpLearnedInformation', value)

	@property
	def IsOfTopologyLearnedInformationRefreshed(self):
		"""If true, it denotes that the Topology Learned Info is received.

		Returns:
			bool
		"""
		return self._get_attribute('isOfTopologyLearnedInformationRefreshed')

	@property
	def LldpDestinationMac(self):
		"""Indicates the Destination MAC Address for LLDP PacketOut.

		Returns:
			str
		"""
		return self._get_attribute('lldpDestinationMac')
	@LldpDestinationMac.setter
	def LldpDestinationMac(self, value):
		self._set_attribute('lldpDestinationMac', value)

	@property
	def LldpResponseTimeOut(self):
		"""Indicates the duration in milliseconds after which the trigger request times out if no Topology learned info response is received.

		Returns:
			number
		"""
		return self._get_attribute('lldpResponseTimeOut')
	@LldpResponseTimeOut.setter
	def LldpResponseTimeOut(self, value):
		self._set_attribute('lldpResponseTimeOut', value)

	def RefreshOfTopology(self):
		"""Executes the refreshOfTopology operation on the server.

		Exec to refresh ofChannel topology.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofTopologyLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			number: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshOfTopology', payload=locals(), response_object=None)
