from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LabelBlock(Base):
	"""The LabelBlock class encapsulates a user managed labelBlock node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LabelBlock property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'labelBlock'

	def __init__(self, parent):
		super(LabelBlock, self).__init__(parent)

	@property
	def Enabled(self):
		"""Enables or disables use of the L2 VPN label block.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def LabelBlockOffsetIncrementAcrossL2Site(self):
		"""Signifies the increment of label block offset across L2 site

		Returns:
			number
		"""
		return self._get_attribute('labelBlockOffsetIncrementAcrossL2Site')
	@LabelBlockOffsetIncrementAcrossL2Site.setter
	def LabelBlockOffsetIncrementAcrossL2Site(self, value):
		self._set_attribute('labelBlockOffsetIncrementAcrossL2Site', value)

	@property
	def LabelStartIncrementAcrossL2Site(self):
		"""Starts the increment of label across L2 site

		Returns:
			number
		"""
		return self._get_attribute('labelStartIncrementAcrossL2Site')
	@LabelStartIncrementAcrossL2Site.setter
	def LabelStartIncrementAcrossL2Site(self, value):
		self._set_attribute('labelStartIncrementAcrossL2Site', value)

	@property
	def NumberOfLabels(self):
		"""The number of labels contained in the label block. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('numberOfLabels')
	@NumberOfLabels.setter
	def NumberOfLabels(self, value):
		self._set_attribute('numberOfLabels', value)

	@property
	def Offset(self):
		"""The VPLS block offset value used to create a unique subset of the label values. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def Start(self):
		"""The first label in the label block. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('start')
	@Start.setter
	def Start(self, value):
		self._set_attribute('start', value)

	@property
	def TotalLabelCount(self):
		"""Signifies the total label count

		Returns:
			number
		"""
		return self._get_attribute('totalLabelCount')

	def add(self, Enabled=None, LabelBlockOffsetIncrementAcrossL2Site=None, LabelStartIncrementAcrossL2Site=None, NumberOfLabels=None, Offset=None, Start=None):
		"""Adds a new labelBlock node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): Enables or disables use of the L2 VPN label block.
			LabelBlockOffsetIncrementAcrossL2Site (number): Signifies the increment of label block offset across L2 site
			LabelStartIncrementAcrossL2Site (number): Starts the increment of label across L2 site
			NumberOfLabels (number): The number of labels contained in the label block. (default = 0)
			Offset (number): The VPLS block offset value used to create a unique subset of the label values. (default = 0)
			Start (number): The first label in the label block. (default = 0)

		Returns:
			self: This instance with all currently retrieved labelBlock data using find and the newly added labelBlock data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the labelBlock data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, LabelBlockOffsetIncrementAcrossL2Site=None, LabelStartIncrementAcrossL2Site=None, NumberOfLabels=None, Offset=None, Start=None, TotalLabelCount=None):
		"""Finds and retrieves labelBlock data from the server.

		All named parameters support regex and can be used to selectively retrieve labelBlock data from the server.
		By default the find method takes no parameters and will retrieve all labelBlock data from the server.

		Args:
			Enabled (bool): Enables or disables use of the L2 VPN label block.
			LabelBlockOffsetIncrementAcrossL2Site (number): Signifies the increment of label block offset across L2 site
			LabelStartIncrementAcrossL2Site (number): Starts the increment of label across L2 site
			NumberOfLabels (number): The number of labels contained in the label block. (default = 0)
			Offset (number): The VPLS block offset value used to create a unique subset of the label values. (default = 0)
			Start (number): The first label in the label block. (default = 0)
			TotalLabelCount (number): Signifies the total label count

		Returns:
			self: This instance with matching labelBlock data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of labelBlock data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the labelBlock data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
