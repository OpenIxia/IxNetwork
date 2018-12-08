
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


class DefaultStacks(Base):
	"""The DefaultStacks class encapsulates a required defaultStacks node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DefaultStacks property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'defaultStacks'

	def __init__(self, parent):
		super(DefaultStacks, self).__init__(parent)

	def Create(self, Arg2):
		"""Executes the create operation on the server.

		Creates an NGPF default stack

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=defaultStacks)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/topology|/api/v1/sessions/1/ixnetwork/topology)): host for the stack to be created: a) ref to a /topology, b) ref to /topology/deviceGroup, c) null to create a new Topology

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Create', payload=locals(), response_object=None)
