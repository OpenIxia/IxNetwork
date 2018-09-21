from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchActionLearnedInfo(Base):
	"""The SwitchActionLearnedInfo class encapsulates a system managed switchActionLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchActionLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchActionLearnedInfo'

	def __init__(self, parent):
		super(SwitchActionLearnedInfo, self).__init__(parent)

	@property
	def ActionType(self):
		"""This describes the action associated with the flow entry

		Returns:
			str
		"""
		return self._get_attribute('actionType')

	@property
	def EthernetDestination(self):
		"""This describes Ethernet destination address.

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetSource(self):
		"""This describes Ethernet source address.

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def IpDscp(self):
		"""This describes the IP DSCP value for advertising.

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def Ipv4Destination(self):
		"""This describes the IPv4 destination address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""This describes the IPv4 source address.

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')

	@property
	def MaxByteLength(self):
		"""This describes the maximum amount of data from a packet that should be sent when the port is OFPP_CONTROLLER.

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')

	@property
	def OutputPort(self):
		"""This describes the output port through which the packet should be sent.

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def QueueId(self):
		"""This describes the queue of the port in which the packet should be enqueued.

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def TransportDestination(self):
		"""This describes the transport destination address

		Returns:
			number
		"""
		return self._get_attribute('transportDestination')

	@property
	def TransportSource(self):
		"""This describes the transport source address

		Returns:
			number
		"""
		return self._get_attribute('transportSource')

	@property
	def VlanId(self):
		"""This describes the Value of the VLAN ID field.

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""This describes the VLAN priority

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ActionType=None, EthernetDestination=None, EthernetSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, MaxByteLength=None, OutputPort=None, QueueId=None, TransportDestination=None, TransportSource=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves switchActionLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchActionLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchActionLearnedInfo data from the server.

		Args:
			ActionType (str): This describes the action associated with the flow entry
			EthernetDestination (str): This describes Ethernet destination address.
			EthernetSource (str): This describes Ethernet source address.
			IpDscp (str): This describes the IP DSCP value for advertising.
			Ipv4Destination (str): This describes the IPv4 destination address.
			Ipv4Source (str): This describes the IPv4 source address.
			MaxByteLength (number): This describes the maximum amount of data from a packet that should be sent when the port is OFPP_CONTROLLER.
			OutputPort (number): This describes the output port through which the packet should be sent.
			QueueId (number): This describes the queue of the port in which the packet should be enqueued.
			TransportDestination (number): This describes the transport destination address
			TransportSource (number): This describes the transport source address
			VlanId (number): This describes the Value of the VLAN ID field.
			VlanPriority (number): This describes the VLAN priority

		Returns:
			self: This instance with matching switchActionLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchActionLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchActionLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
