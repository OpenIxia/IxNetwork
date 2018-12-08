
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


class Aggregation(Base):
	"""The Aggregation class encapsulates a system managed aggregation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Aggregation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'aggregation'

	def __init__(self, parent):
		super(Aggregation, self).__init__(parent)

	@property
	def ActivePort(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)
		"""
		return self._get_attribute('activePort')

	@property
	def ActivePorts(self):
		"""

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])
		"""
		return self._get_attribute('activePorts')

	@property
	def AvailableModes(self):
		"""

		Returns:
			list(str[atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGig|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|normal|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGig|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut])
		"""
		return self._get_attribute('availableModes')

	@property
	def Mode(self):
		"""

		Returns:
			str(atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGig|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|normal|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGig|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def ResourcePorts(self):
		"""

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])
		"""
		return self._get_attribute('resourcePorts')

	def find(self, ActivePort=None, ActivePorts=None, AvailableModes=None, Mode=None, ResourcePorts=None):
		"""Finds and retrieves aggregation data from the server.

		All named parameters support regex and can be used to selectively retrieve aggregation data from the server.
		By default the find method takes no parameters and will retrieve all aggregation data from the server.

		Args:
			ActivePort (str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)): 
			ActivePorts (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 
			AvailableModes (list(str[atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGig|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|normal|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGig|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut])): 
			Mode (str(atlasEightByFiftyGigFanOut|atlasFourByOneHundredGigFanOut|atlasOneByFourHundredGigNonFanOut|atlasTwoByTwoHundredGigNonFanOut|dualMode|eightByTenGigFanOut|fortyGig|fortyGigCapturePlayback|fortyGigFanOut|fortyGigNonFanOut|fourByTenGigFanOut|fourByTwentyFiveGigNonFanOut|hundredGigCapturePlayback|hundredGigNonFanOut|incompatibleMode|krakenFourByFiftyGigFanOut|krakenOneByFourHundredGigNonFanOut|krakenOneByTwoHundredGigNonFanOut|krakenTwoByOneHundredGigFanOut|normal|novusFourByTenGigNonFanOut|novusFourByTwentyFiveGigNonFanOut|novusHundredGigNonFanOut|novusOneByFortyGigNonFanOut|novusTwoByFiftyGigNonFanOut|oneByFiftyGigNonFanOut|oneByTenGigFanOut|singleMode|tenGig|threeByTenGigFanOut|twoByTwentyFiveGigNonFanOut)): 
			ResourcePorts (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port])): 

		Returns:
			self: This instance with matching aggregation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of aggregation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the aggregation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
