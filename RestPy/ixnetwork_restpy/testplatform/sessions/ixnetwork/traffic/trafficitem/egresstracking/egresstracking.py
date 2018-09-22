from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EgressTracking(Base):
	"""The EgressTracking class encapsulates a user managed egressTracking node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EgressTracking property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'egressTracking'

	def __init__(self, parent):
		super(EgressTracking, self).__init__(parent)

	@property
	def FieldOffset(self):
		"""An instance of the FieldOffset class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.fieldoffset.FieldOffset)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.fieldoffset import FieldOffset
		return FieldOffset(self)._select()

	@property
	def AvailableEncapsulations(self):
		"""(Read only) Specifies the available Encapsulations for Egress Tracking.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableEncapsulations')

	@property
	def AvailableOffsets(self):
		"""(Read only) Specifies the available Offsets for Egress Tracking.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableOffsets')

	@property
	def CustomOffsetBits(self):
		"""Specifies the Custom Offset in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .

		Returns:
			number
		"""
		return self._get_attribute('customOffsetBits')
	@CustomOffsetBits.setter
	def CustomOffsetBits(self, value):
		self._set_attribute('customOffsetBits', value)

	@property
	def CustomWidthBits(self):
		"""Specifies the Custom Width in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .

		Returns:
			number
		"""
		return self._get_attribute('customWidthBits')
	@CustomWidthBits.setter
	def CustomWidthBits(self, value):
		self._set_attribute('customWidthBits', value)

	@property
	def Encapsulation(self):
		"""Specifies the Encapsulation for Egress Tracking.

		Returns:
			str
		"""
		return self._get_attribute('encapsulation')
	@Encapsulation.setter
	def Encapsulation(self, value):
		self._set_attribute('encapsulation', value)

	@property
	def Offset(self):
		"""Specifies the Offset for Egress Tracking.

		Returns:
			str
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	def add(self, CustomOffsetBits=None, CustomWidthBits=None, Encapsulation=None, Offset=None):
		"""Adds a new egressTracking node on the server and retrieves it in this instance.

		Args:
			CustomOffsetBits (number): Specifies the Custom Offset in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .
			CustomWidthBits (number): Specifies the Custom Width in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .
			Encapsulation (str): Specifies the Encapsulation for Egress Tracking.
			Offset (str): Specifies the Offset for Egress Tracking.

		Returns:
			self: This instance with all currently retrieved egressTracking data using find and the newly added egressTracking data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the egressTracking data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AvailableEncapsulations=None, AvailableOffsets=None, CustomOffsetBits=None, CustomWidthBits=None, Encapsulation=None, Offset=None):
		"""Finds and retrieves egressTracking data from the server.

		All named parameters support regex and can be used to selectively retrieve egressTracking data from the server.
		By default the find method takes no parameters and will retrieve all egressTracking data from the server.

		Args:
			AvailableEncapsulations (list(str)): (Read only) Specifies the available Encapsulations for Egress Tracking.
			AvailableOffsets (list(str)): (Read only) Specifies the available Offsets for Egress Tracking.
			CustomOffsetBits (number): Specifies the Custom Offset in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .
			CustomWidthBits (number): Specifies the Custom Width in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .
			Encapsulation (str): Specifies the Encapsulation for Egress Tracking.
			Offset (str): Specifies the Offset for Egress Tracking.

		Returns:
			self: This instance with matching egressTracking data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of egressTracking data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the egressTracking data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
