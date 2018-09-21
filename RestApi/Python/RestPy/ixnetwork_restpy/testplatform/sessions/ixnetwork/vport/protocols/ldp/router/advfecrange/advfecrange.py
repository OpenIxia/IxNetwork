from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AdvFecRange(Base):
	"""The AdvFecRange class encapsulates a user managed advFecRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdvFecRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'advFecRange'

	def __init__(self, parent):
		super(AdvFecRange, self).__init__(parent)

	@property
	def EnablePacking(self):
		"""(For IPv4 FEC ranges and in Unsolicited Label Distribution Mode ONLY) If checked, FEC ranges will be aggregated within a single LDP PDU to conserve bandwidth and processing.

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def EnableReplyingLspPing(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableReplyingLspPing')
	@EnableReplyingLspPing.setter
	def EnableReplyingLspPing(self, value):
		self._set_attribute('enableReplyingLspPing', value)

	@property
	def Enabled(self):
		"""Enables this FEC range for use in label mapping messages. By default, the Ixia LDP emulation uses the prefix FEC type.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def FirstNetwork(self):
		"""The first network address in the range (in IP address format).

		Returns:
			str
		"""
		return self._get_attribute('firstNetwork')
	@FirstNetwork.setter
	def FirstNetwork(self, value):
		self._set_attribute('firstNetwork', value)

	@property
	def LabelMode(self):
		"""Indicates whether the same label or incrementing labels should be used in the VC ranges.

		Returns:
			str(none|increment)
		"""
		return self._get_attribute('labelMode')
	@LabelMode.setter
	def LabelMode(self, value):
		self._set_attribute('labelMode', value)

	@property
	def LabelValueStart(self):
		"""The first label in the range of labels.

		Returns:
			number
		"""
		return self._get_attribute('labelValueStart')
	@LabelValueStart.setter
	def LabelValueStart(self, value):
		self._set_attribute('labelValueStart', value)

	@property
	def MaskWidth(self):
		"""The number of bits in the mask applied to the network address. The masked bits in the First Network address form the address prefix.

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def NumberOfNetworks(self):
		"""The number of network addresses to be included in the range. The maximum number of valid possible addresses depends on the values for the first network and the network mask.

		Returns:
			number
		"""
		return self._get_attribute('numberOfNetworks')
	@NumberOfNetworks.setter
	def NumberOfNetworks(self, value):
		self._set_attribute('numberOfNetworks', value)

	def add(self, EnablePacking=None, EnableReplyingLspPing=None, Enabled=None, FirstNetwork=None, LabelMode=None, LabelValueStart=None, MaskWidth=None, NumberOfNetworks=None):
		"""Adds a new advFecRange node on the server and retrieves it in this instance.

		Args:
			EnablePacking (bool): (For IPv4 FEC ranges and in Unsolicited Label Distribution Mode ONLY) If checked, FEC ranges will be aggregated within a single LDP PDU to conserve bandwidth and processing.
			EnableReplyingLspPing (bool): NOT DEFINED
			Enabled (bool): Enables this FEC range for use in label mapping messages. By default, the Ixia LDP emulation uses the prefix FEC type.
			FirstNetwork (str): The first network address in the range (in IP address format).
			LabelMode (str(none|increment)): Indicates whether the same label or incrementing labels should be used in the VC ranges.
			LabelValueStart (number): The first label in the range of labels.
			MaskWidth (number): The number of bits in the mask applied to the network address. The masked bits in the First Network address form the address prefix.
			NumberOfNetworks (number): The number of network addresses to be included in the range. The maximum number of valid possible addresses depends on the values for the first network and the network mask.

		Returns:
			self: This instance with all currently retrieved advFecRange data using find and the newly added advFecRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the advFecRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnablePacking=None, EnableReplyingLspPing=None, Enabled=None, FirstNetwork=None, LabelMode=None, LabelValueStart=None, MaskWidth=None, NumberOfNetworks=None):
		"""Finds and retrieves advFecRange data from the server.

		All named parameters support regex and can be used to selectively retrieve advFecRange data from the server.
		By default the find method takes no parameters and will retrieve all advFecRange data from the server.

		Args:
			EnablePacking (bool): (For IPv4 FEC ranges and in Unsolicited Label Distribution Mode ONLY) If checked, FEC ranges will be aggregated within a single LDP PDU to conserve bandwidth and processing.
			EnableReplyingLspPing (bool): NOT DEFINED
			Enabled (bool): Enables this FEC range for use in label mapping messages. By default, the Ixia LDP emulation uses the prefix FEC type.
			FirstNetwork (str): The first network address in the range (in IP address format).
			LabelMode (str(none|increment)): Indicates whether the same label or incrementing labels should be used in the VC ranges.
			LabelValueStart (number): The first label in the range of labels.
			MaskWidth (number): The number of bits in the mask applied to the network address. The masked bits in the First Network address form the address prefix.
			NumberOfNetworks (number): The number of network addresses to be included in the range. The maximum number of valid possible addresses depends on the values for the first network and the network mask.

		Returns:
			self: This instance with matching advFecRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of advFecRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the advFecRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
