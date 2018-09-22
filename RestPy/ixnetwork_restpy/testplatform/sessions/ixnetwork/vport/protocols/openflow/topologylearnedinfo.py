from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TopologyLearnedInfo(Base):
	"""The TopologyLearnedInfo class encapsulates a system managed topologyLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TopologyLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'topologyLearnedInfo'

	def __init__(self, parent):
		super(TopologyLearnedInfo, self).__init__(parent)

	@property
	def InDataPathId(self):
		"""Indicates the Datapath Id of Datapath for LLDP Packet-In Port.

		Returns:
			str
		"""
		return self._get_attribute('inDataPathId')

	@property
	def InDataPathIdAshex(self):
		"""Indicates the Datapath Id, in hexadecimal format, of Datapath for LLDP Packet-In Port

		Returns:
			str
		"""
		return self._get_attribute('inDataPathIdAshex')

	@property
	def InIp(self):
		"""Indicates the IP Address of Datapath for LLDP Packet-In Port.

		Returns:
			str
		"""
		return self._get_attribute('inIp')

	@property
	def InPortEthernetAddress(self):
		"""Indicates the Ethernet Address for LLDP Packet-In Port

		Returns:
			str
		"""
		return self._get_attribute('inPortEthernetAddress')

	@property
	def InPortName(self):
		"""Indicates the Port Name for LLDP Packet-In Port

		Returns:
			str
		"""
		return self._get_attribute('inPortName')

	@property
	def InPortNumber(self):
		"""Indicates the Port Number for LLDP Packet-In Port.

		Returns:
			number
		"""
		return self._get_attribute('inPortNumber')

	@property
	def OutDataPathId(self):
		"""Indicates the Datapath Id of Datapath for LLDP Packet Out Port.

		Returns:
			str
		"""
		return self._get_attribute('outDataPathId')

	@property
	def OutDataPathIdAsHex(self):
		"""Indicates the Datapath Id, in hexadecimal format, of Datapath for LLDP Packet Out Port.

		Returns:
			str
		"""
		return self._get_attribute('outDataPathIdAsHex')

	@property
	def OutIp(self):
		"""Indicates the IP Address of Datapath for LLDP Packet Out Port.

		Returns:
			str
		"""
		return self._get_attribute('outIp')

	@property
	def OutPortEthernetAddress(self):
		"""Indicates the Ethernet Address for LLDP Packet Out Port.

		Returns:
			str
		"""
		return self._get_attribute('outPortEthernetAddress')

	@property
	def OutPortName(self):
		"""Indicates the Port Name for LLDP Packet Out Port.

		Returns:
			str
		"""
		return self._get_attribute('outPortName')

	@property
	def OutPortNumber(self):
		"""Indicates the Port Number for LLDP Packet Out Port.

		Returns:
			number
		"""
		return self._get_attribute('outPortNumber')

	def find(self, InDataPathId=None, InDataPathIdAshex=None, InIp=None, InPortEthernetAddress=None, InPortName=None, InPortNumber=None, OutDataPathId=None, OutDataPathIdAsHex=None, OutIp=None, OutPortEthernetAddress=None, OutPortName=None, OutPortNumber=None):
		"""Finds and retrieves topologyLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve topologyLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all topologyLearnedInfo data from the server.

		Args:
			InDataPathId (str): Indicates the Datapath Id of Datapath for LLDP Packet-In Port.
			InDataPathIdAshex (str): Indicates the Datapath Id, in hexadecimal format, of Datapath for LLDP Packet-In Port
			InIp (str): Indicates the IP Address of Datapath for LLDP Packet-In Port.
			InPortEthernetAddress (str): Indicates the Ethernet Address for LLDP Packet-In Port
			InPortName (str): Indicates the Port Name for LLDP Packet-In Port
			InPortNumber (number): Indicates the Port Number for LLDP Packet-In Port.
			OutDataPathId (str): Indicates the Datapath Id of Datapath for LLDP Packet Out Port.
			OutDataPathIdAsHex (str): Indicates the Datapath Id, in hexadecimal format, of Datapath for LLDP Packet Out Port.
			OutIp (str): Indicates the IP Address of Datapath for LLDP Packet Out Port.
			OutPortEthernetAddress (str): Indicates the Ethernet Address for LLDP Packet Out Port.
			OutPortName (str): Indicates the Port Name for LLDP Packet Out Port.
			OutPortNumber (number): Indicates the Port Number for LLDP Packet Out Port.

		Returns:
			self: This instance with matching topologyLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of topologyLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the topologyLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
