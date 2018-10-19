
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


class Testworkflow(Base):
	"""The Testworkflow class encapsulates a required testworkflow node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Testworkflow property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'testworkflow'

	def __init__(self, parent):
		super(Testworkflow, self).__init__(parent)

	@property
	def CurrentDescripton(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('currentDescripton')

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		connect ports, start protocols and generate/apply/start traffic

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=testworkflow)): The method internally sets Arg1 to the current href for this instance
			Arg2 (bool): a boolean indicating if ownership should be taken forcefully

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		stop protocols and traffic

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=testworkflow)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
