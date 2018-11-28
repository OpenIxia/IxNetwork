
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


class Parameter(Base):
	"""The Parameter class encapsulates a system managed parameter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Parameter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'parameter'

	def __init__(self, parent):
		super(Parameter, self).__init__(parent)

	@property
	def AvailableChoices(self):
		"""Available Choices

		Returns:
			list(str)
		"""
		return self._get_attribute('availableChoices')

	@property
	def CurrentValue(self):
		"""Parameter UI Display Value

		Returns:
			str
		"""
		return self._get_attribute('currentValue')
	@CurrentValue.setter
	def CurrentValue(self, value):
		self._set_attribute('currentValue', value)

	@property
	def CustomDefaultValue(self):
		"""Parameter Custom Default Value

		Returns:
			str
		"""
		return self._get_attribute('customDefaultValue')

	@property
	def DefaultValue(self):
		"""Parameter Default Value

		Returns:
			str
		"""
		return self._get_attribute('defaultValue')

	@property
	def IsReadOnly(self):
		"""Parameter value type

		Returns:
			bool
		"""
		return self._get_attribute('isReadOnly')

	@property
	def MaxValue(self):
		"""Parameter Maximum Value

		Returns:
			str
		"""
		return self._get_attribute('maxValue')

	@property
	def MinValue(self):
		"""Parameter Minimum Value

		Returns:
			str
		"""
		return self._get_attribute('minValue')

	@property
	def Name(self):
		"""Parameter Name.

		Returns:
			str
		"""
		return self._get_attribute('name')

	def find(self, AvailableChoices=None, CurrentValue=None, CustomDefaultValue=None, DefaultValue=None, IsReadOnly=None, MaxValue=None, MinValue=None, Name=None):
		"""Finds and retrieves parameter data from the server.

		All named parameters support regex and can be used to selectively retrieve parameter data from the server.
		By default the find method takes no parameters and will retrieve all parameter data from the server.

		Args:
			AvailableChoices (list(str)): Available Choices
			CurrentValue (str): Parameter UI Display Value
			CustomDefaultValue (str): Parameter Custom Default Value
			DefaultValue (str): Parameter Default Value
			IsReadOnly (bool): Parameter value type
			MaxValue (str): Parameter Maximum Value
			MinValue (str): Parameter Minimum Value
			Name (str): Parameter Name.

		Returns:
			self: This instance with matching parameter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of parameter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the parameter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
