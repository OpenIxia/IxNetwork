
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


class Instruction(Base):
	"""The Instruction class encapsulates a user managed instruction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Instruction property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'instruction'

	def __init__(self, parent):
		super(Instruction, self).__init__(parent)

	@property
	def Actions(self):
		"""An instance of the Actions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.actions.Actions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.actions import Actions
		return Actions(self)

	@property
	def Field(self):
		"""An instance of the Field class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.field.Field)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.field import Field
		return Field(self)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Description(self):
		"""Description of the field.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def DisplayName(self):
		"""Display name used by GUI.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def IsEditable(self):
		"""Information on the requirement of the field.

		Returns:
			bool
		"""
		return self._get_attribute('isEditable')
	@IsEditable.setter
	def IsEditable(self, value):
		self._set_attribute('isEditable', value)

	@property
	def IsEnabled(self):
		"""Enables disables the field.

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def IsRequired(self):
		"""Information on the requirement of the field.

		Returns:
			bool
		"""
		return self._get_attribute('isRequired')
	@IsRequired.setter
	def IsRequired(self, value):
		self._set_attribute('isRequired', value)

	@property
	def Name(self):
		"""Name of packet field

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def add(self, Description=None, IsEditable=None, IsEnabled=None, IsRequired=None, Name=None):
		"""Adds a new instruction node on the server and retrieves it in this instance.

		Args:
			Description (str): Description of the field.
			IsEditable (bool): Information on the requirement of the field.
			IsEnabled (bool): Enables disables the field.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of packet field

		Returns:
			self: This instance with all currently retrieved instruction data using find and the newly added instruction data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the instruction data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, Description=None, DisplayName=None, IsEditable=None, IsEnabled=None, IsRequired=None, Name=None):
		"""Finds and retrieves instruction data from the server.

		All named parameters support regex and can be used to selectively retrieve instruction data from the server.
		By default the find method takes no parameters and will retrieve all instruction data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			Description (str): Description of the field.
			DisplayName (str): Display name used by GUI.
			IsEditable (bool): Information on the requirement of the field.
			IsEnabled (bool): Enables disables the field.
			IsRequired (bool): Information on the requirement of the field.
			Name (str): Name of packet field

		Returns:
			self: This instance with matching instruction data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of instruction data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the instruction data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddAction(self, Arg2):
		"""Executes the addAction operation on the server.

		Adds an Action item.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddAction', payload=locals(), response_object=None)

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
