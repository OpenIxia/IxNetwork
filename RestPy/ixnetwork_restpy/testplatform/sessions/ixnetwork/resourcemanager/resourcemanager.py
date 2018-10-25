
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


class ResourceManager(Base):
	"""The ResourceManager class encapsulates a required resourceManager node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ResourceManager property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'resourceManager'

	def __init__(self, parent):
		super(ResourceManager, self).__init__(parent)

	def ExportConfig(self, Arg2, Arg3, Arg4):
		"""Executes the exportConfig operation on the server.

		Export the entire configuration or fragments of it in a text based format

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/resourceManager)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(str)): A list of xpaths each of which is a starting point in the configuration. The only supported xpath notation is by index or descendant-or-self:*. To export the entire configuration specify /descendant-or-self:*
			Arg3 (bool): True to include attributes that are equal to the default in the export, false to exclude them
			Arg4 (str(json)): The format of the exported configuration

		Returns:
			str: JSON configuration as a string

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ExportConfig', payload=locals(), response_object=None)

	def ExportConfigFile(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the exportConfigFile operation on the server.

		Export the entire configuration or fragments of it in a text based format

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/resourceManager)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(str)): A list of xpaths each of which is a starting point in the configuration. The only supported xpath notation is by index or descendant-or-self:*. To export the entire configuration specify /descendant-or-self:*
			Arg3 (bool): True to include attributes that are equal to the default in the export, false to exclude them
			Arg4 (str(json)): The format of the exported configuration
			Arg5 (obj(ixnetwork_restpy.files.Files)): The file object to write the configuration to

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg5, Files)
		return self._execute('ExportConfigFile', payload=locals(), response_object=None)

	def ImportConfig(self, Arg2, Arg3):
		"""Executes the importConfig operation on the server.

		Create or update the test tool configuration

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/resourceManager)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): The configuration as a string
			Arg3 (bool): True to create a new configuration, false to update the current configuration

		Returns:
			list(str): A list of errors that occurred during import

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ImportConfig', payload=locals(), response_object=None)

	def ImportConfigFile(self, Arg2, Arg3):
		"""Executes the importConfigFile operation on the server.

		Create or update the test tool configuration

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/resourceManager)): The method internally sets Arg1 to the current href for this instance
			Arg2 (obj(ixnetwork_restpy.files.Files)): The file object to read the configuration from
			Arg3 (bool): True to create a new configuration, false to update the current configuration

		Returns:
			list(str): A list of errors that occurred during import

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		return self._execute('ImportConfigFile', payload=locals(), response_object=None)
