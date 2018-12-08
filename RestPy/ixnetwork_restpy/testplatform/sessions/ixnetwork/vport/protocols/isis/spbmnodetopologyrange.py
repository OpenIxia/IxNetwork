
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


class SpbmNodeTopologyRange(Base):
	"""The SpbmNodeTopologyRange class encapsulates a user managed spbmNodeTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbmNodeTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbmNodeTopologyRange'

	def __init__(self, parent):
		super(SpbmNodeTopologyRange, self).__init__(parent)

	@property
	def SpbmNodeBaseVidRange(self):
		"""An instance of the SpbmNodeBaseVidRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodebasevidrange.SpbmNodeBaseVidRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbmnodebasevidrange import SpbmNodeBaseVidRange
		return SpbmNodeBaseVidRange(self)

	@property
	def BridgePriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bridgePriority')
	@BridgePriority.setter
	def BridgePriority(self, value):
		self._set_attribute('bridgePriority', value)

	@property
	def CistExternalRootCost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cistExternalRootCost')
	@CistExternalRootCost.setter
	def CistExternalRootCost(self, value):
		self._set_attribute('cistExternalRootCost', value)

	@property
	def CistRootIdentifier(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cistRootIdentifier')
	@CistRootIdentifier.setter
	def CistRootIdentifier(self, value):
		self._set_attribute('cistRootIdentifier', value)

	@property
	def EnableVbit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVbit')
	@EnableVbit.setter
	def EnableVbit(self, value):
		self._set_attribute('enableVbit', value)

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
	def InterNodeLinkMetricIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interNodeLinkMetricIncrement')
	@InterNodeLinkMetricIncrement.setter
	def InterNodeLinkMetricIncrement(self, value):
		self._set_attribute('interNodeLinkMetricIncrement', value)

	@property
	def InterNodeSpSourceIdIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interNodeSpSourceIdIncrement')
	@InterNodeSpSourceIdIncrement.setter
	def InterNodeSpSourceIdIncrement(self, value):
		self._set_attribute('interNodeSpSourceIdIncrement', value)

	@property
	def LinkMetric(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('linkMetric')
	@LinkMetric.setter
	def LinkMetric(self, value):
		self._set_attribute('linkMetric', value)

	@property
	def NoOfPorts(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfPorts')
	@NoOfPorts.setter
	def NoOfPorts(self, value):
		self._set_attribute('noOfPorts', value)

	@property
	def PortIdentifier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portIdentifier')
	@PortIdentifier.setter
	def PortIdentifier(self, value):
		self._set_attribute('portIdentifier', value)

	@property
	def SpSourceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('spSourceId')
	@SpSourceId.setter
	def SpSourceId(self, value):
		self._set_attribute('spSourceId', value)

	def add(self, BridgePriority=None, CistExternalRootCost=None, CistRootIdentifier=None, EnableVbit=None, Enabled=None, InterNodeLinkMetricIncrement=None, InterNodeSpSourceIdIncrement=None, LinkMetric=None, NoOfPorts=None, PortIdentifier=None, SpSourceId=None):
		"""Adds a new spbmNodeTopologyRange node on the server and retrieves it in this instance.

		Args:
			BridgePriority (number): 
			CistExternalRootCost (number): 
			CistRootIdentifier (str): 
			EnableVbit (bool): 
			Enabled (bool): 
			InterNodeLinkMetricIncrement (number): 
			InterNodeSpSourceIdIncrement (number): 
			LinkMetric (number): 
			NoOfPorts (number): 
			PortIdentifier (number): 
			SpSourceId (number): 

		Returns:
			self: This instance with all currently retrieved spbmNodeTopologyRange data using find and the newly added spbmNodeTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbmNodeTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BridgePriority=None, CistExternalRootCost=None, CistRootIdentifier=None, EnableVbit=None, Enabled=None, InterNodeLinkMetricIncrement=None, InterNodeSpSourceIdIncrement=None, LinkMetric=None, NoOfPorts=None, PortIdentifier=None, SpSourceId=None):
		"""Finds and retrieves spbmNodeTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbmNodeTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all spbmNodeTopologyRange data from the server.

		Args:
			BridgePriority (number): 
			CistExternalRootCost (number): 
			CistRootIdentifier (str): 
			EnableVbit (bool): 
			Enabled (bool): 
			InterNodeLinkMetricIncrement (number): 
			InterNodeSpSourceIdIncrement (number): 
			LinkMetric (number): 
			NoOfPorts (number): 
			PortIdentifier (number): 
			SpSourceId (number): 

		Returns:
			self: This instance with matching spbmNodeTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbmNodeTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbmNodeTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
