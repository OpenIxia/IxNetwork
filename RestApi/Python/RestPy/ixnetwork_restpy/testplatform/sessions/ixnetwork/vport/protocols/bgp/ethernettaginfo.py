from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EthernetTagInfo(Base):
	"""The EthernetTagInfo class encapsulates a system managed ethernetTagInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EthernetTagInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ethernetTagInfo'

	def __init__(self, parent):
		super(EthernetTagInfo, self).__init__(parent)

	@property
	def EsiLabel(self):
		"""(Read Only) ESI label learned.

		Returns:
			str
		"""
		return self._get_attribute('esiLabel')

	@property
	def EthernetTag(self):
		"""(Read Only) Ethernet Tag id in hex format.

		Returns:
			str
		"""
		return self._get_attribute('ethernetTag')

	@property
	def Labels(self):
		"""(Read Only) Per EVI/EthernetTag A-D label learned for an EVI or an Ethernet Tag.

		Returns:
			str
		"""
		return self._get_attribute('labels')

	def find(self, EsiLabel=None, EthernetTag=None, Labels=None):
		"""Finds and retrieves ethernetTagInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ethernetTagInfo data from the server.
		By default the find method takes no parameters and will retrieve all ethernetTagInfo data from the server.

		Args:
			EsiLabel (str): (Read Only) ESI label learned.
			EthernetTag (str): (Read Only) Ethernet Tag id in hex format.
			Labels (str): (Read Only) Per EVI/EthernetTag A-D label learned for an EVI or an Ethernet Tag.

		Returns:
			self: This instance with matching ethernetTagInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ethernetTagInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ethernetTagInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
