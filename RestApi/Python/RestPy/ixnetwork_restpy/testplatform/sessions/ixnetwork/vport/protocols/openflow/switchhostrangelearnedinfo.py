from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchHostRangeLearnedInfo(Base):
	"""The SwitchHostRangeLearnedInfo class encapsulates a system managed switchHostRangeLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchHostRangeLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchHostRangeLearnedInfo'

	def __init__(self, parent):
		super(SwitchHostRangeLearnedInfo, self).__init__(parent)

	@property
	def SwitchHostRangeHopsLearnedInfo(self):
		"""An instance of the SwitchHostRangeHopsLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangehopslearnedinfo.SwitchHostRangeHopsLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchhostrangehopslearnedinfo import SwitchHostRangeHopsLearnedInfo
		return SwitchHostRangeHopsLearnedInfo(self)

	@property
	def DestinationHostIpv4Address(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationHostIpv4Address')

	@property
	def DestinationHostMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationHostMac')

	@property
	def PacketType(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('packetType')

	@property
	def Path(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('path')

	@property
	def SourceHostIpv4Address(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('sourceHostIpv4Address')

	@property
	def SourceHostMac(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('sourceHostMac')

	@property
	def Status(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('status')

	def find(self, DestinationHostIpv4Address=None, DestinationHostMac=None, PacketType=None, Path=None, SourceHostIpv4Address=None, SourceHostMac=None, Status=None):
		"""Finds and retrieves switchHostRangeLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchHostRangeLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchHostRangeLearnedInfo data from the server.

		Args:
			DestinationHostIpv4Address (str): NOT DEFINED
			DestinationHostMac (str): NOT DEFINED
			PacketType (str): NOT DEFINED
			Path (str): NOT DEFINED
			SourceHostIpv4Address (str): NOT DEFINED
			SourceHostMac (str): NOT DEFINED
			Status (str): NOT DEFINED

		Returns:
			self: This instance with matching switchHostRangeLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchHostRangeLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchHostRangeLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
