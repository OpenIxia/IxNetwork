
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


class Meter(Base):
	"""The Meter class encapsulates a user managed meter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Meter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'meter'

	def __init__(self, parent):
		super(Meter, self).__init__(parent)

	@property
	def Band(self):
		"""An instance of the Band class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.band.Band)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.band import Band
		return Band(self)

	@property
	def Flags(self):
		"""An instance of the Flags class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flags.Flags)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flags import Flags
		return Flags(self)._select()

	@property
	def __id__(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('__id__')
	@__id__.setter
	def __id__(self, value):
		self._set_attribute('__id__', value)

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
	def MeterAdvertise(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('meterAdvertise')
	@MeterAdvertise.setter
	def MeterAdvertise(self, value):
		self._set_attribute('meterAdvertise', value)

	@property
	def UpdateMeterModStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('updateMeterModStatus')

	def add(self, __id__=None, Description=None, Enabled=None, MeterAdvertise=None):
		"""Adds a new meter node on the server and retrieves it in this instance.

		Args:
			__id__ (number): 
			Description (str): 
			Enabled (bool): 
			MeterAdvertise (bool): 

		Returns:
			self: This instance with all currently retrieved meter data using find and the newly added meter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the meter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, __id__=None, Description=None, Enabled=None, MeterAdvertise=None, UpdateMeterModStatus=None):
		"""Finds and retrieves meter data from the server.

		All named parameters support regex and can be used to selectively retrieve meter data from the server.
		By default the find method takes no parameters and will retrieve all meter data from the server.

		Args:
			__id__ (number): 
			Description (str): 
			Enabled (bool): 
			MeterAdvertise (bool): 
			UpdateMeterModStatus (str): 

		Returns:
			self: This instance with matching meter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateMeterMod(self, Arg2):
		"""Executes the updateMeterMod operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=meter)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(sendMeterAdd|sendMeterModify|sendMeterRemove)): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateMeterMod', payload=locals(), response_object=None)
