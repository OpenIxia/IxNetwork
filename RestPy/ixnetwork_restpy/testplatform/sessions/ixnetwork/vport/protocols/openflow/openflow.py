from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpenFlow(Base):
	"""The OpenFlow class encapsulates a required openFlow node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpenFlow property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'openFlow'

	def __init__(self, parent):
		super(OpenFlow, self).__init__(parent)

	@property
	def Device(self):
		"""An instance of the Device class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.device.Device)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.device import Device
		return Device(self)

	@property
	def EthernetTrafficEndPoint(self):
		"""An instance of the EthernetTrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ethernettrafficendpoint.EthernetTrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ethernettrafficendpoint import EthernetTrafficEndPoint
		return EthernetTrafficEndPoint(self)

	@property
	def HostTopologyLearnedInformation(self):
		"""An instance of the HostTopologyLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.hosttopologylearnedinformation.HostTopologyLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.hosttopologylearnedinformation import HostTopologyLearnedInformation
		return HostTopologyLearnedInformation(self)._select()

	@property
	def Ipv4TrafficEndPoint(self):
		"""An instance of the Ipv4TrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ipv4trafficendpoint.Ipv4TrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ipv4trafficendpoint import Ipv4TrafficEndPoint
		return Ipv4TrafficEndPoint(self)

	@property
	def Ipv6TrafficEndPoint(self):
		"""An instance of the Ipv6TrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ipv6trafficendpoint.Ipv6TrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ipv6trafficendpoint import Ipv6TrafficEndPoint
		return Ipv6TrafficEndPoint(self)

	@property
	def LearnedInformation(self):
		"""An instance of the LearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.learnedinformation.LearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.learnedinformation import LearnedInformation
		return LearnedInformation(self)._select()

	@property
	def MplsTrafficEndPoint(self):
		"""An instance of the MplsTrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.mplstrafficendpoint.MplsTrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.mplstrafficendpoint import MplsTrafficEndPoint
		return MplsTrafficEndPoint(self)

	@property
	def OfTopologyLearnedInformation(self):
		"""An instance of the OfTopologyLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.oftopologylearnedinformation.OfTopologyLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.oftopologylearnedinformation import OfTopologyLearnedInformation
		return OfTopologyLearnedInformation(self)._select()

	@property
	def SwitchLearnedInformation(self):
		"""An instance of the SwitchLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchlearnedinformation.SwitchLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchlearnedinformation import SwitchLearnedInformation
		return SwitchLearnedInformation(self)._select()

	@property
	def TrafficEndPoint(self):
		"""An instance of the TrafficEndPoint class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.trafficendpoint.TrafficEndPoint)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.trafficendpoint import TrafficEndPoint
		return TrafficEndPoint(self)

	@property
	def Enabled(self):
		"""If true, the openFlow object is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def PortRole(self):
		"""Indicates the role of the port in the protocol configuration.

		Returns:
			str(control|traffic|controlAndTraffic)
		"""
		return self._get_attribute('portRole')
	@PortRole.setter
	def PortRole(self, value):
		self._set_attribute('portRole', value)

	@property
	def RunningState(self):
		"""Indicates the state of the OpenFlow protocol on the port.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def Start(self):
		"""Executes the start operation on the server.

		This describes the start value of the trigger settings.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=openFlow)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This describes the stop value of the trigger settings.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=openFlow)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
