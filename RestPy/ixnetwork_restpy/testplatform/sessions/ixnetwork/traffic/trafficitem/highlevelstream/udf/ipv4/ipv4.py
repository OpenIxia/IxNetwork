from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv4(Base):
	"""The Ipv4 class encapsulates a system managed ipv4 node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ipv4 property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ipv4'

	def __init__(self, parent):
		super(Ipv4, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Species all the possible widths available for a UDF in particular Type.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def BitmaskCount(self):
		"""Specifies the number of bits to be masked to any integer value between 2 to 32.

		Returns:
			number
		"""
		return self._get_attribute('bitmaskCount')
	@BitmaskCount.setter
	def BitmaskCount(self, value):
		self._set_attribute('bitmaskCount', value)

	@property
	def InnerLoopIncrementBy(self):
		"""Specifies the Step Value by which the Inner Loop will be incremented.

		Returns:
			number
		"""
		return self._get_attribute('innerLoopIncrementBy')
	@InnerLoopIncrementBy.setter
	def InnerLoopIncrementBy(self, value):
		self._set_attribute('innerLoopIncrementBy', value)

	@property
	def InnerLoopLoopCount(self):
		"""Specifies the no. of times the inner loop will occur.

		Returns:
			number
		"""
		return self._get_attribute('innerLoopLoopCount')
	@InnerLoopLoopCount.setter
	def InnerLoopLoopCount(self, value):
		self._set_attribute('innerLoopLoopCount', value)

	@property
	def OuterLoopLoopCount(self):
		"""Specifies the no. of times the outer loop will occur.

		Returns:
			number
		"""
		return self._get_attribute('outerLoopLoopCount')
	@OuterLoopLoopCount.setter
	def OuterLoopLoopCount(self, value):
		self._set_attribute('outerLoopLoopCount', value)

	@property
	def SkipValues(self):
		"""If true, Skip Values option is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('skipValues')
	@SkipValues.setter
	def SkipValues(self, value):
		self._set_attribute('skipValues', value)

	@property
	def StartValue(self):
		"""Specifies the start value of the UDF.

		Returns:
			number
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def Width(self):
		"""Specifies the width of the UDF.

		Returns:
			str(32)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)

	def find(self, AvailableWidths=None, BitmaskCount=None, InnerLoopIncrementBy=None, InnerLoopLoopCount=None, OuterLoopLoopCount=None, SkipValues=None, StartValue=None, Width=None):
		"""Finds and retrieves ipv4 data from the server.

		All named parameters support regex and can be used to selectively retrieve ipv4 data from the server.
		By default the find method takes no parameters and will retrieve all ipv4 data from the server.

		Args:
			AvailableWidths (list(str)): Species all the possible widths available for a UDF in particular Type.
			BitmaskCount (number): Specifies the number of bits to be masked to any integer value between 2 to 32.
			InnerLoopIncrementBy (number): Specifies the Step Value by which the Inner Loop will be incremented.
			InnerLoopLoopCount (number): Specifies the no. of times the inner loop will occur.
			OuterLoopLoopCount (number): Specifies the no. of times the outer loop will occur.
			SkipValues (bool): If true, Skip Values option is enabled.
			StartValue (number): Specifies the start value of the UDF.
			Width (str(32)): Specifies the width of the UDF.

		Returns:
			self: This instance with matching ipv4 data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ipv4 data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ipv4 data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
