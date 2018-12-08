
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


class Scriptgen(Base):
	"""The Scriptgen class encapsulates a required scriptgen node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Scriptgen property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'scriptgen'

	def __init__(self, parent):
		super(Scriptgen, self).__init__(parent)

	@property
	def Base64CodeOptions(self):
		"""An instance of the Base64CodeOptions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.base64codeoptions.base64codeoptions.Base64CodeOptions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.base64codeoptions.base64codeoptions import Base64CodeOptions
		return Base64CodeOptions(self)._select()

	@property
	def IxNetCodeOptions(self):
		"""An instance of the IxNetCodeOptions class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.ixnetcodeoptions.ixnetcodeoptions.IxNetCodeOptions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.ixnetcodeoptions.ixnetcodeoptions import IxNetCodeOptions
		return IxNetCodeOptions(self)._select()

	@property
	def ConnectHostname(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('connectHostname')
	@ConnectHostname.setter
	def ConnectHostname(self, value):
		self._set_attribute('connectHostname', value)

	@property
	def ConnectPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('connectPort')
	@ConnectPort.setter
	def ConnectPort(self, value):
		self._set_attribute('connectPort', value)

	@property
	def ConnectVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('connectVersion')
	@ConnectVersion.setter
	def ConnectVersion(self, value):
		self._set_attribute('connectVersion', value)

	@property
	def IncludeConnect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeConnect')
	@IncludeConnect.setter
	def IncludeConnect(self, value):
		self._set_attribute('includeConnect', value)

	@property
	def IncludeTestComposer(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTestComposer')
	@IncludeTestComposer.setter
	def IncludeTestComposer(self, value):
		self._set_attribute('includeTestComposer', value)

	@property
	def Language(self):
		"""

		Returns:
			str(perl|python|ruby|tcl)
		"""
		return self._get_attribute('language')
	@Language.setter
	def Language(self, value):
		self._set_attribute('language', value)

	@property
	def LinePerAttribute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('linePerAttribute')
	@LinePerAttribute.setter
	def LinePerAttribute(self, value):
		self._set_attribute('linePerAttribute', value)

	@property
	def OverwriteScriptFilename(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overwriteScriptFilename')
	@OverwriteScriptFilename.setter
	def OverwriteScriptFilename(self, value):
		self._set_attribute('overwriteScriptFilename', value)

	@property
	def ScriptFilename(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('scriptFilename')
	@ScriptFilename.setter
	def ScriptFilename(self, value):
		self._set_attribute('scriptFilename', value)

	@property
	def SerializationType(self):
		"""

		Returns:
			str(base64|ixNet)
		"""
		return self._get_attribute('serializationType')
	@SerializationType.setter
	def SerializationType(self, value):
		self._set_attribute('serializationType', value)

	def Generate(self):
		"""Executes the generate operation on the server.

		Generate a script of the currently loaded configuration using the options in the /globals/scriptgen hierarchy.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=scriptgen)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Generate', payload=locals(), response_object=None)

	def Generate(self, Arg2):
		"""Executes the generate operation on the server.

		Generate a script of the currently loaded configuration using the options in the /globals/scriptgen hierarchy.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=scriptgen)): The method internally sets Arg1 to the current href for this instance
			Arg2 (obj(ixnetwork_restpy.files.Files)): A valid writeTo file handle the script will be written to.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		return self._execute('Generate', payload=locals(), response_object=None)
