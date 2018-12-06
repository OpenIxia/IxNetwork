
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


class GroupRange(Base):
	"""The GroupRange class encapsulates a user managed groupRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'groupRange'

	def __init__(self, parent):
		super(GroupRange, self).__init__(parent)

	@property
	def SourceRange(self):
		"""An instance of the SourceRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.sourcerange.sourcerange.SourceRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.sourcerange.sourcerange import SourceRange
		return SourceRange(self)

	@property
	def EnablePacking(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePacking')
	@EnablePacking.setter
	def EnablePacking(self, value):
		self._set_attribute('enablePacking', value)

	@property
	def EnableUpdateRequired(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableUpdateRequired')
	@EnableUpdateRequired.setter
	def EnableUpdateRequired(self, value):
		self._set_attribute('enableUpdateRequired', value)

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
	def GroupCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupIpFrom(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupIpFrom')
	@GroupIpFrom.setter
	def GroupIpFrom(self, value):
		self._set_attribute('groupIpFrom', value)

	@property
	def IncrementStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('incrementStep')
	@IncrementStep.setter
	def IncrementStep(self, value):
		self._set_attribute('incrementStep', value)

	@property
	def RecordsPerFrame(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recordsPerFrame')
	@RecordsPerFrame.setter
	def RecordsPerFrame(self, value):
		self._set_attribute('recordsPerFrame', value)

	@property
	def SourceMode(self):
		"""

		Returns:
			str(include|exclude)
		"""
		return self._get_attribute('sourceMode')
	@SourceMode.setter
	def SourceMode(self, value):
		self._set_attribute('sourceMode', value)

	@property
	def SourcesPerRecord(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourcesPerRecord')
	@SourcesPerRecord.setter
	def SourcesPerRecord(self, value):
		self._set_attribute('sourcesPerRecord', value)

	def add(self, EnablePacking=None, EnableUpdateRequired=None, Enabled=None, GroupCount=None, GroupIpFrom=None, IncrementStep=None, RecordsPerFrame=None, SourceMode=None, SourcesPerRecord=None):
		"""Adds a new groupRange node on the server and retrieves it in this instance.

		Args:
			EnablePacking (bool): 
			EnableUpdateRequired (bool): 
			Enabled (bool): 
			GroupCount (number): 
			GroupIpFrom (str): 
			IncrementStep (number): 
			RecordsPerFrame (number): 
			SourceMode (str(include|exclude)): 
			SourcesPerRecord (number): 

		Returns:
			self: This instance with all currently retrieved groupRange data using find and the newly added groupRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the groupRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnablePacking=None, EnableUpdateRequired=None, Enabled=None, GroupCount=None, GroupIpFrom=None, IncrementStep=None, RecordsPerFrame=None, SourceMode=None, SourcesPerRecord=None):
		"""Finds and retrieves groupRange data from the server.

		All named parameters support regex and can be used to selectively retrieve groupRange data from the server.
		By default the find method takes no parameters and will retrieve all groupRange data from the server.

		Args:
			EnablePacking (bool): 
			EnableUpdateRequired (bool): 
			Enabled (bool): 
			GroupCount (number): 
			GroupIpFrom (str): 
			IncrementStep (number): 
			RecordsPerFrame (number): 
			SourceMode (str(include|exclude)): 
			SourcesPerRecord (number): 

		Returns:
			self: This instance with matching groupRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateSource(self):
		"""Executes the updateSource operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=groupRange)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateSource', payload=locals(), response_object=None)
