from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DelayLearnedInfo(Base):
	"""The DelayLearnedInfo class encapsulates a system managed delayLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DelayLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'delayLearnedInfo'

	def __init__(self, parent):
		super(DelayLearnedInfo, self).__init__(parent)

	@property
	def CVlan(self):
		"""(read only) The learned C-VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('cVlan')

	@property
	def DstMacAddress(self):
		"""(read only) The learned destination MAC address for the bridge.

		Returns:
			str
		"""
		return self._get_attribute('dstMacAddress')

	@property
	def MdLevel(self):
		"""(read only) The learned MD level for the bridge.

		Returns:
			number
		"""
		return self._get_attribute('mdLevel')

	@property
	def SVlan(self):
		"""(read only) The learned S-VLAN identifier.

		Returns:
			str
		"""
		return self._get_attribute('sVlan')

	@property
	def SrcMacAddress(self):
		"""(read only) The learned source MAC address for the bridge.

		Returns:
			str
		"""
		return self._get_attribute('srcMacAddress')

	@property
	def ValueInNanoSec(self):
		"""(read only) The delay measurement in nanoseconds.

		Returns:
			number
		"""
		return self._get_attribute('valueInNanoSec')

	@property
	def ValueInSec(self):
		"""(read only) The delay measurement in seconds.

		Returns:
			number
		"""
		return self._get_attribute('valueInSec')

	def find(self, CVlan=None, DstMacAddress=None, MdLevel=None, SVlan=None, SrcMacAddress=None, ValueInNanoSec=None, ValueInSec=None):
		"""Finds and retrieves delayLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve delayLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all delayLearnedInfo data from the server.

		Args:
			CVlan (str): (read only) The learned C-VLAN identifier.
			DstMacAddress (str): (read only) The learned destination MAC address for the bridge.
			MdLevel (number): (read only) The learned MD level for the bridge.
			SVlan (str): (read only) The learned S-VLAN identifier.
			SrcMacAddress (str): (read only) The learned source MAC address for the bridge.
			ValueInNanoSec (number): (read only) The delay measurement in nanoseconds.
			ValueInSec (number): (read only) The delay measurement in seconds.

		Returns:
			self: This instance with matching delayLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of delayLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the delayLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
