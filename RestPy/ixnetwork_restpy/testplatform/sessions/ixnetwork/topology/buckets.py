
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


class Buckets(Base):
	"""The Buckets class encapsulates a system managed buckets node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Buckets property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'buckets'

	def __init__(self, parent):
		super(Buckets, self).__init__(parent)

	@property
	def ActionsProfile(self):
		"""An instance of the ActionsProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.actionsprofile.ActionsProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.actionsprofile import ActionsProfile
		return ActionsProfile(self)._select()

	@property
	def BucketDescription(self):
		"""A description for the bucket.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bucketDescription')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def GroupIndex(self):
		"""Group Index

		Returns:
			list(str)
		"""
		return self._get_attribute('groupIndex')

	@property
	def GroupName(self):
		"""Parent Group Name

		Returns:
			str
		"""
		return self._get_attribute('groupName')

	@property
	def Multiplier(self):
		"""Number of instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def WatchGroup(self):
		"""A group whose state determines whether this bucket is live or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('watchGroup')

	@property
	def WatchPort(self):
		"""A Port whose state determines whether this bucket is live or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('watchPort')

	@property
	def Weight(self):
		"""Specify the weight of buckets. The permissible range is 0-65535.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')

	def find(self, Count=None, DescriptiveName=None, GroupIndex=None, GroupName=None, Multiplier=None, Name=None):
		"""Finds and retrieves buckets data from the server.

		All named parameters support regex and can be used to selectively retrieve buckets data from the server.
		By default the find method takes no parameters and will retrieve all buckets data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			GroupIndex (list(str)): Group Index
			GroupName (str): Parent Group Name
			Multiplier (number): Number of instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching buckets data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of buckets data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the buckets data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, BucketDescription=None, WatchGroup=None, WatchPort=None, Weight=None):
		"""Base class infrastructure that gets a list of buckets device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BucketDescription (str): optional regex of bucketDescription
			WatchGroup (str): optional regex of watchGroup
			WatchPort (str): optional regex of watchPort
			Weight (str): optional regex of weight

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
