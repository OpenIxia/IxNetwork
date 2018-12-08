
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


class SwitchFlowInstructionLearnedInfo(Base):
	"""The SwitchFlowInstructionLearnedInfo class encapsulates a system managed switchFlowInstructionLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchFlowInstructionLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchFlowInstructionLearnedInfo'

	def __init__(self, parent):
		super(SwitchFlowInstructionLearnedInfo, self).__init__(parent)

	@property
	def SwitchActionV131LearnedInfo(self):
		"""An instance of the SwitchActionV131LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchactionv131learnedinfo.SwitchActionV131LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.switchactionv131learnedinfo import SwitchActionV131LearnedInfo
		return SwitchActionV131LearnedInfo(self)

	@property
	def Experimenter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenter')

	@property
	def ExperimenterData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def InstructionType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('instructionType')

	@property
	def Metadata(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadata')

	@property
	def MetadataMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('metadataMask')

	@property
	def MeterId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def TableId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tableId')

	def find(self, Experimenter=None, ExperimenterData=None, ExperimenterDataLength=None, InstructionType=None, Metadata=None, MetadataMask=None, MeterId=None, TableId=None):
		"""Finds and retrieves switchFlowInstructionLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchFlowInstructionLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchFlowInstructionLearnedInfo data from the server.

		Args:
			Experimenter (number): 
			ExperimenterData (str): 
			ExperimenterDataLength (number): 
			InstructionType (str): 
			Metadata (str): 
			MetadataMask (str): 
			MeterId (number): 
			TableId (number): 

		Returns:
			self: This instance with matching switchFlowInstructionLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchFlowInstructionLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchFlowInstructionLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
