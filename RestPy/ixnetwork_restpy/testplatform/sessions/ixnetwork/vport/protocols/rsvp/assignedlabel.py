
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


class AssignedLabel(Base):
	"""The AssignedLabel class encapsulates a system managed assignedLabel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AssignedLabel property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'assignedLabel'

	def __init__(self, parent):
		super(AssignedLabel, self).__init__(parent)

	@property
	def CurrentLspOrSubLspUpTime(self):
		"""Indicates the re-optimization time per LSP/Sub LSP in port level.

		Returns:
			number
		"""
		return self._get_attribute('currentLspOrSubLspUpTime')

	@property
	def DestinationIp(self):
		"""The destination router's IP address.

		Returns:
			str
		"""
		return self._get_attribute('destinationIp')

	@property
	def Label(self):
		"""Label value assigned to the LSP/tunnel (by the Ixia-emulated router) in response to a label request from the DUT.

		Returns:
			number
		"""
		return self._get_attribute('label')

	@property
	def LeafIp(self):
		"""The IP of the leaf range.

		Returns:
			str
		"""
		return self._get_attribute('leafIp')

	@property
	def LspId(self):
		"""A unique LSP tunnel ID.

		Returns:
			number
		"""
		return self._get_attribute('lspId')

	@property
	def LspOrSubLspSetupTime(self):
		"""Indicates the set up time per LSP/Sub LSP in port level.

		Returns:
			number
		"""
		return self._get_attribute('lspOrSubLspSetupTime')

	@property
	def ReservationState(self):
		"""The reservation state, once there is a graceful restart. The values are None, Stale, Recovered, Restarting.

		Returns:
			str
		"""
		return self._get_attribute('reservationState')

	@property
	def SourceIp(self):
		"""The source router's IP address.

		Returns:
			str
		"""
		return self._get_attribute('sourceIp')

	@property
	def TunnelId(self):
		"""A unique tunnel ID.

		Returns:
			number
		"""
		return self._get_attribute('tunnelId')

	@property
	def Type(self):
		"""Tunnel type, one of P2P or P2MP.

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, CurrentLspOrSubLspUpTime=None, DestinationIp=None, Label=None, LeafIp=None, LspId=None, LspOrSubLspSetupTime=None, ReservationState=None, SourceIp=None, TunnelId=None, Type=None):
		"""Finds and retrieves assignedLabel data from the server.

		All named parameters support regex and can be used to selectively retrieve assignedLabel data from the server.
		By default the find method takes no parameters and will retrieve all assignedLabel data from the server.

		Args:
			CurrentLspOrSubLspUpTime (number): Indicates the re-optimization time per LSP/Sub LSP in port level.
			DestinationIp (str): The destination router's IP address.
			Label (number): Label value assigned to the LSP/tunnel (by the Ixia-emulated router) in response to a label request from the DUT.
			LeafIp (str): The IP of the leaf range.
			LspId (number): A unique LSP tunnel ID.
			LspOrSubLspSetupTime (number): Indicates the set up time per LSP/Sub LSP in port level.
			ReservationState (str): The reservation state, once there is a graceful restart. The values are None, Stale, Recovered, Restarting.
			SourceIp (str): The source router's IP address.
			TunnelId (number): A unique tunnel ID.
			Type (str): Tunnel type, one of P2P or P2MP.

		Returns:
			self: This instance with matching assignedLabel data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of assignedLabel data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the assignedLabel data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
