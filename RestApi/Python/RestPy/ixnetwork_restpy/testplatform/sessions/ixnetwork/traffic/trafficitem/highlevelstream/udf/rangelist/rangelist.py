from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RangeList(Base):
	"""The RangeList class encapsulates a system managed rangeList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RangeList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rangeList'

	def __init__(self, parent):
		super(RangeList, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Species all the possible widths available for a UDF in particular Type.

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
	def StartValueCountStepList(self):
		"""Specifies the Start Value, Count and Step Value of the UDF.

		Returns:
			list(number)
		"""
		return self._get_attribute('startValueCountStepList')
	@StartValueCountStepList.setter
	def StartValueCountStepList(self, value):
		self._set_attribute('startValueCountStepList', value)

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

	def find(self, AvailableWidths=None, BitOffset=None, StartValueCountStepList=None, Width=None):
		"""Finds and retrieves rangeList data from the server.

		All named parameters support regex and can be used to selectively retrieve rangeList data from the server.
		By default the find method takes no parameters and will retrieve all rangeList data from the server.

		Args:
			AvailableWidths (list(str)): Species all the possible widths available for a UDF in particular Type.
			BitOffset (number): Specifies additional Offset of the UDF in terms of bits. This Offset will start from where the Offset provided in Byte Offset field ends.
			StartValueCountStepList (list(number)): Specifies the Start Value, Count and Step Value of the UDF.
			Width (str(1|10|11|12|13|14|15|16|17|18|19|2|20|21|22|23|24|25|26|27|28|29|3|30|31|32|4|5|6|7|8|9)): Specifies the width of the UDF.

		Returns:
			self: This instance with matching rangeList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rangeList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rangeList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
