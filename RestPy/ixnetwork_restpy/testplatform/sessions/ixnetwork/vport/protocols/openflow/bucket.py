
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


class Bucket(Base):
	"""The Bucket class encapsulates a user managed bucket node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bucket property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bucket'

	def __init__(self, parent):
		super(Bucket, self).__init__(parent)

	@property
	def BucketAction(self):
		"""An instance of the BucketAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.bucketaction.BucketAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.bucketaction import BucketAction
		return BucketAction(self)

	@property
	def Description(self):
		"""A description of the bucket.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def WatchGroup(self):
		"""A group whose state determines whether this bucket is live.

		Returns:
			number
		"""
		return self._get_attribute('watchGroup')
	@WatchGroup.setter
	def WatchGroup(self, value):
		self._set_attribute('watchGroup', value)

	@property
	def WatchPort(self):
		"""A Port whose state determines whether this bucket is live.

		Returns:
			number
		"""
		return self._get_attribute('watchPort')
	@WatchPort.setter
	def WatchPort(self, value):
		self._set_attribute('watchPort', value)

	@property
	def Weight(self):
		"""Specify the weight of buckets. The range allowed is 0-65535

		Returns:
			number
		"""
		return self._get_attribute('weight')
	@Weight.setter
	def Weight(self, value):
		self._set_attribute('weight', value)

	def add(self, Description=None, WatchGroup=None, WatchPort=None, Weight=None):
		"""Adds a new bucket node on the server and retrieves it in this instance.

		Args:
			Description (str): A description of the bucket.
			WatchGroup (number): A group whose state determines whether this bucket is live.
			WatchPort (number): A Port whose state determines whether this bucket is live.
			Weight (number): Specify the weight of buckets. The range allowed is 0-65535

		Returns:
			self: This instance with all currently retrieved bucket data using find and the newly added bucket data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bucket data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Description=None, WatchGroup=None, WatchPort=None, Weight=None):
		"""Finds and retrieves bucket data from the server.

		All named parameters support regex and can be used to selectively retrieve bucket data from the server.
		By default the find method takes no parameters and will retrieve all bucket data from the server.

		Args:
			Description (str): A description of the bucket.
			WatchGroup (number): A group whose state determines whether this bucket is live.
			WatchPort (number): A Port whose state determines whether this bucket is live.
			Weight (number): Specify the weight of buckets. The range allowed is 0-65535

		Returns:
			self: This instance with matching bucket data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bucket data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bucket data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
