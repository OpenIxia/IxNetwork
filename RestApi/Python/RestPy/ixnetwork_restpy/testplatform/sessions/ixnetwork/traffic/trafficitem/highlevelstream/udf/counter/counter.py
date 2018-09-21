from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Counter(Base):
	"""The Counter class encapsulates a system managed counter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Counter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'counter'

	def __init__(self, parent):
		super(Counter, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Contains all the possible widths available for a UDF in particular Type.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def BitOffset(self):
		"""Specifies additional Offset of the UDF in terms of bits. This Offset will start from where the Offset provided in Byte Offset field ends.

		Returns:
			number
		"""
		return self._get_attribute('bitOffset')
	@BitOffset.setter
	def BitOffset(self, value):
		self._set_attribute('bitOffset', value)

	@property
	def Count(self):
		"""Specifies the repeat count for the UDF. After the elapse of this count, UDF will again start from the Start Value.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Direction(self):
		"""Specifies if the UDF value will be incremented or decremented.

		Returns:
			str(decrement|increment)
		"""
		return self._get_attribute('direction')
	@Direction.setter
	def Direction(self, value):
		self._set_attribute('direction', value)

	@property
	def StartValue(self):
		"""Specifies the Start Value of the UDF.

		Returns:
			number
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def StepValue(self):
		"""Specifies the Step Value by which the UDF value will be incremented or decremented.

		Returns:
			number
		"""
		return self._get_attribute('stepValue')
	@StepValue.setter
	def StepValue(self, value):
		self._set_attribute('stepValue', value)

	@property
	def Width(self):
		"""Specifies the width of the UDF.

		Returns:
			str(1|10|11|12|13|14|15|16|17|18|19|2|20|21|22|23|24|25|26|27|28|29|3|30|31|32|4|5|6|7|8|9)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)

	def find(self, AvailableWidths=None, BitOffset=None, Count=None, Direction=None, StartValue=None, StepValue=None, Width=None):
		"""Finds and retrieves counter data from the server.

		All named parameters support regex and can be used to selectively retrieve counter data from the server.
		By default the find method takes no parameters and will retrieve all counter data from the server.

		Args:
			AvailableWidths (list(str)): Contains all the possible widths available for a UDF in particular Type.
			BitOffset (number): Specifies additional Offset of the UDF in terms of bits. This Offset will start from where the Offset provided in Byte Offset field ends.
			Count (number): Specifies the repeat count for the UDF. After the elapse of this count, UDF will again start from the Start Value.
			Direction (str(decrement|increment)): Specifies if the UDF value will be incremented or decremented.
			StartValue (number): Specifies the Start Value of the UDF.
			StepValue (number): Specifies the Step Value by which the UDF value will be incremented or decremented.
			Width (str(1|10|11|12|13|14|15|16|17|18|19|2|20|21|22|23|24|25|26|27|28|29|3|30|31|32|4|5|6|7|8|9)): Specifies the width of the UDF.

		Returns:
			self: This instance with matching counter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of counter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the counter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
