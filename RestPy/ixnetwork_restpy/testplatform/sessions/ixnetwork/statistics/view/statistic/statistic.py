
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistic(Base):
	"""The Statistic class encapsulates a system managed statistic node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Statistic property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'statistic'

	def __init__(self, parent):
		super(Statistic, self).__init__(parent)

	@property
	def AggregationType(self):
		"""

		Returns:
			str(average|averageRate|ax|axRate|intervalAverage|min|minRate|none|rate|runStateAgg|runStateAggIgnoreRamp|sum|vectorMax|vectorMin|weightedAverage)
		"""
		return self._get_attribute('aggregationType')
	@AggregationType.setter
	def AggregationType(self, value):
		self._set_attribute('aggregationType', value)

	@property
	def Caption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def DefaultCaption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('defaultCaption')

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ScaleFactor(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('scaleFactor')
	@ScaleFactor.setter
	def ScaleFactor(self, value):
		self._set_attribute('scaleFactor', value)

	@property
	def SourceTypes(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceTypes')

	def find(self, AggregationType=None, Caption=None, DefaultCaption=None, Enabled=None, ScaleFactor=None, SourceTypes=None):
		"""Finds and retrieves statistic data from the server.

		All named parameters support regex and can be used to selectively retrieve statistic data from the server.
		By default the find method takes no parameters and will retrieve all statistic data from the server.

		Args:
			AggregationType (str(average|averageRate|ax|axRate|intervalAverage|min|minRate|none|rate|runStateAgg|runStateAggIgnoreRamp|sum|vectorMax|vectorMin|weightedAverage)): 
			Caption (str): 
			DefaultCaption (str): 
			Enabled (bool): 
			ScaleFactor (number): 
			SourceTypes (list(str)): 

		Returns:
			self: This instance with matching statistic data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of statistic data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the statistic data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
