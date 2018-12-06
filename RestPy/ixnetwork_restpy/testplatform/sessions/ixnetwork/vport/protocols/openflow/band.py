
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


class Band(Base):
	"""The Band class encapsulates a user managed band node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Band property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'band'

	def __init__(self, parent):
		super(Band, self).__init__(parent)

	@property
	def BurstSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('burstSize')
	@BurstSize.setter
	def BurstSize(self, value):
		self._set_attribute('burstSize', value)

	@property
	def Description(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def Experimenter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def PrecedenceLevel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('precedenceLevel')
	@PrecedenceLevel.setter
	def PrecedenceLevel(self, value):
		self._set_attribute('precedenceLevel', value)

	@property
	def Rate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rate')
	@Rate.setter
	def Rate(self, value):
		self._set_attribute('rate', value)

	@property
	def Type(self):
		"""

		Returns:
			str(drop|dscpRemark|experimenter)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	def add(self, BurstSize=None, Description=None, Experimenter=None, PrecedenceLevel=None, Rate=None, Type=None):
		"""Adds a new band node on the server and retrieves it in this instance.

		Args:
			BurstSize (number): 
			Description (str): 
			Experimenter (number): 
			PrecedenceLevel (number): 
			Rate (number): 
			Type (str(drop|dscpRemark|experimenter)): 

		Returns:
			self: This instance with all currently retrieved band data using find and the newly added band data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the band data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BurstSize=None, Description=None, Experimenter=None, PrecedenceLevel=None, Rate=None, Type=None):
		"""Finds and retrieves band data from the server.

		All named parameters support regex and can be used to selectively retrieve band data from the server.
		By default the find method takes no parameters and will retrieve all band data from the server.

		Args:
			BurstSize (number): 
			Description (str): 
			Experimenter (number): 
			PrecedenceLevel (number): 
			Rate (number): 
			Type (str(drop|dscpRemark|experimenter)): 

		Returns:
			self: This instance with matching band data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of band data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the band data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
