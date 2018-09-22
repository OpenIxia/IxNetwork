from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchPorts(Base):
	"""The SwitchPorts class encapsulates a user managed switchPorts node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchPorts property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'switchPorts'

	def __init__(self, parent):
		super(SwitchPorts, self).__init__(parent)

	@property
	def AdvertisedFeatures(self):
		"""An instance of the AdvertisedFeatures class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.advertisedfeatures.AdvertisedFeatures)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.advertisedfeatures import AdvertisedFeatures
		return AdvertisedFeatures(self)._select()

	@property
	def Config(self):
		"""An instance of the Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.config.Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.config import Config
		return Config(self)._select()

	@property
	def CurrentFeatures(self):
		"""An instance of the CurrentFeatures class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.currentfeatures.CurrentFeatures)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.currentfeatures import CurrentFeatures
		return CurrentFeatures(self)._select()

	@property
	def PeerAdvertisedFeatures(self):
		"""An instance of the PeerAdvertisedFeatures class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.peeradvertisedfeatures.PeerAdvertisedFeatures)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.peeradvertisedfeatures import PeerAdvertisedFeatures
		return PeerAdvertisedFeatures(self)._select()

	@property
	def State(self):
		"""An instance of the State class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.state.State)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.state import State
		return State(self)._select()

	@property
	def SupportedFeatures(self):
		"""An instance of the SupportedFeatures class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.supportedfeatures.SupportedFeatures)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.supportedfeatures import SupportedFeatures
		return SupportedFeatures(self)._select()

	@property
	def SwitchPortQueues(self):
		"""An instance of the SwitchPortQueues class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchportqueues.SwitchPortQueues)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchportqueues import SwitchPortQueues
		return SwitchPortQueues(self)

	@property
	def Enabled(self):
		"""If true, the ports in the selected port range are added to the switch.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EthernetAddress(self):
		"""Indicates the hardware address of the ports in the port range.

		Returns:
			str
		"""
		return self._get_attribute('ethernetAddress')
	@EthernetAddress.setter
	def EthernetAddress(self, value):
		self._set_attribute('ethernetAddress', value)

	@property
	def NumberOfPorts(self):
		"""Specifies the number of ports in a port range.

		Returns:
			number
		"""
		return self._get_attribute('numberOfPorts')
	@NumberOfPorts.setter
	def NumberOfPorts(self, value):
		self._set_attribute('numberOfPorts', value)

	@property
	def PortName(self):
		"""Indicates the name for the switch port interface.

		Returns:
			str
		"""
		return self._get_attribute('portName')
	@PortName.setter
	def PortName(self, value):
		self._set_attribute('portName', value)

	@property
	def PortNumber(self):
		"""Indicates a value that the datapath associates with a physical port.

		Returns:
			str
		"""
		return self._get_attribute('portNumber')
	@PortNumber.setter
	def PortNumber(self, value):
		self._set_attribute('portNumber', value)

	def add(self, Enabled=None, EthernetAddress=None, NumberOfPorts=None, PortName=None, PortNumber=None):
		"""Adds a new switchPorts node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true, the ports in the selected port range are added to the switch.
			EthernetAddress (str): Indicates the hardware address of the ports in the port range.
			NumberOfPorts (number): Specifies the number of ports in a port range.
			PortName (str): Indicates the name for the switch port interface.
			PortNumber (str): Indicates a value that the datapath associates with a physical port.

		Returns:
			self: This instance with all currently retrieved switchPorts data using find and the newly added switchPorts data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the switchPorts data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, EthernetAddress=None, NumberOfPorts=None, PortName=None, PortNumber=None):
		"""Finds and retrieves switchPorts data from the server.

		All named parameters support regex and can be used to selectively retrieve switchPorts data from the server.
		By default the find method takes no parameters and will retrieve all switchPorts data from the server.

		Args:
			Enabled (bool): If true, the ports in the selected port range are added to the switch.
			EthernetAddress (str): Indicates the hardware address of the ports in the port range.
			NumberOfPorts (number): Specifies the number of ports in a port range.
			PortName (str): Indicates the name for the switch port interface.
			PortNumber (str): Indicates a value that the datapath associates with a physical port.

		Returns:
			self: This instance with matching switchPorts data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchPorts data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchPorts data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SimulatePortUpDown(self):
		"""Executes the simulatePortUpDown operation on the server.

		Exec to simulate port up and down.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchPorts)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SimulatePortUpDown', payload=locals(), response_object=None)
