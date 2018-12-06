
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


class AdvFecRange(Base):
	"""The AdvFecRange class encapsulates a user managed advFecRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AdvFecRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'advFecRange'

	def __init__(self, parent):
		super(AdvFecRange, self).__init__(parent)

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
	def EnableReplyingLspPing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableReplyingLspPing')
	@EnableReplyingLspPing.setter
	def EnableReplyingLspPing(self, value):
		self._set_attribute('enableReplyingLspPing', value)

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
	def FirstNetwork(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('firstNetwork')
	@FirstNetwork.setter
	def FirstNetwork(self, value):
		self._set_attribute('firstNetwork', value)

	@property
	def LabelMode(self):
		"""

		Returns:
			str(none|increment)
		"""
		return self._get_attribute('labelMode')
	@LabelMode.setter
	def LabelMode(self, value):
		self._set_attribute('labelMode', value)

	@property
	def LabelValueStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelValueStart')
	@LabelValueStart.setter
	def LabelValueStart(self, value):
		self._set_attribute('labelValueStart', value)

	@property
	def MaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maskWidth')
	@MaskWidth.setter
	def MaskWidth(self, value):
		self._set_attribute('maskWidth', value)

	@property
	def NumberOfNetworks(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfNetworks')
	@NumberOfNetworks.setter
	def NumberOfNetworks(self, value):
		self._set_attribute('numberOfNetworks', value)

	def add(self, EnablePacking=None, EnableReplyingLspPing=None, Enabled=None, FirstNetwork=None, LabelMode=None, LabelValueStart=None, MaskWidth=None, NumberOfNetworks=None):
		"""Adds a new advFecRange node on the server and retrieves it in this instance.

		Args:
			EnablePacking (bool): 
			EnableReplyingLspPing (bool): 
			Enabled (bool): 
			FirstNetwork (str): 
			LabelMode (str(none|increment)): 
			LabelValueStart (number): 
			MaskWidth (number): 
			NumberOfNetworks (number): 

		Returns:
			self: This instance with all currently retrieved advFecRange data using find and the newly added advFecRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the advFecRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnablePacking=None, EnableReplyingLspPing=None, Enabled=None, FirstNetwork=None, LabelMode=None, LabelValueStart=None, MaskWidth=None, NumberOfNetworks=None):
		"""Finds and retrieves advFecRange data from the server.

		All named parameters support regex and can be used to selectively retrieve advFecRange data from the server.
		By default the find method takes no parameters and will retrieve all advFecRange data from the server.

		Args:
			EnablePacking (bool): 
			EnableReplyingLspPing (bool): 
			Enabled (bool): 
			FirstNetwork (str): 
			LabelMode (str(none|increment)): 
			LabelValueStart (number): 
			MaskWidth (number): 
			NumberOfNetworks (number): 

		Returns:
			self: This instance with matching advFecRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of advFecRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the advFecRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
