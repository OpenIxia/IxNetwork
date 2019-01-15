
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


class QueueConfigLearnedInformation(Base):
	"""The QueueConfigLearnedInformation class encapsulates a system managed queueConfigLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the QueueConfigLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'queueConfigLearnedInformation'

	def __init__(self, parent):
		super(QueueConfigLearnedInformation, self).__init__(parent)

	@property
	def DataPathId(self):
		"""Indicates the Datapath ID of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Indicates the Datapath ID, in hexadecimal format, of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def ErrorCode(self):
		"""Signifies the error code of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""Signifies the type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def ExperimenterData(self):
		"""The experimenter data field value.

		Returns:
			str
		"""
		return self._get_attribute('experimenterData')

	@property
	def ExperimenterDataLength(self):
		"""Value of the Experimenter data length field.

		Returns:
			number
		"""
		return self._get_attribute('experimenterDataLength')

	@property
	def ExperimenterId(self):
		"""Value of the experimenter ID field.

		Returns:
			number
		"""
		return self._get_attribute('experimenterId')

	@property
	def Latency(self):
		"""Indicates the duration elapsed (in microsecond) between the learned info request and response.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""Indicates the local IP of the Controller.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def PortNumber(self):
		"""Indicates the Port number to which the queue belongs.

		Returns:
			number
		"""
		return self._get_attribute('portNumber')

	@property
	def PropertyRate(self):
		"""Indicates the minimum transmission rate of the queue if the queue supports the minimum rate property

		Returns:
			number
		"""
		return self._get_attribute('propertyRate')

	@property
	def QueueId(self):
		"""Indicates the identifier of the queue

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def QueuePortNumber(self):
		"""The Switch port number on which Queue has been configured.

		Returns:
			number
		"""
		return self._get_attribute('queuePortNumber')

	@property
	def QueueProperty(self):
		"""Indicates the supported properties of the queue.

		Returns:
			str
		"""
		return self._get_attribute('queueProperty')

	@property
	def RemoteIp(self):
		"""Indicates the IP of the remote end of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""Indicates the reply state of the switch.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	def find(self, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, ExperimenterData=None, ExperimenterDataLength=None, ExperimenterId=None, Latency=None, LocalIp=None, NegotiatedVersion=None, PortNumber=None, PropertyRate=None, QueueId=None, QueuePortNumber=None, QueueProperty=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves queueConfigLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve queueConfigLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all queueConfigLearnedInformation data from the server.

		Args:
			DataPathId (str): Indicates the Datapath ID of the switch.
			DataPathIdAsHex (str): Indicates the Datapath ID, in hexadecimal format, of the switch.
			ErrorCode (str): Signifies the error code of the error received.
			ErrorType (str): Signifies the type of the error received.
			ExperimenterData (str): The experimenter data field value.
			ExperimenterDataLength (number): Value of the Experimenter data length field.
			ExperimenterId (number): Value of the experimenter ID field.
			Latency (number): Indicates the duration elapsed (in microsecond) between the learned info request and response.
			LocalIp (str): Indicates the local IP of the Controller.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			PortNumber (number): Indicates the Port number to which the queue belongs.
			PropertyRate (number): Indicates the minimum transmission rate of the queue if the queue supports the minimum rate property
			QueueId (number): Indicates the identifier of the queue
			QueuePortNumber (number): The Switch port number on which Queue has been configured.
			QueueProperty (str): Indicates the supported properties of the queue.
			RemoteIp (str): Indicates the IP of the remote end of the OF Channel.
			ReplyState (str): Indicates the reply state of the switch.

		Returns:
			self: This instance with matching queueConfigLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of queueConfigLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the queueConfigLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
