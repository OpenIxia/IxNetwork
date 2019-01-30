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

import sys
import time
import logging
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.connection import Connection
from ixnetwork_restpy.errors import NotFoundError


class TestPlatform(Base):
    """TestPlatform class

    Top level access to an IxNetwork test tool platform (Linux API Server, Windows GUI, ConnectionManager)

    Args:  
        ip_address (str): the ip address of the test tool platform that requests will be made to
        rest_port (number): the ip port of the test tool platform that the server is listening on
        platform (str[windows|linux]): connecting to a windows platform will start with an http scheme, a linux platform will start with an https scheme
        log_file_name (str): the name of the log file that trace logging will be written to, if omitted it will be written to the console
        ignore_env_proxy (bool): if requests is returning a 504 error use this to bypass local environment proxy settings
    
	Raises:
		ConnectionError: this error will be raised if attempting to connect to a linux host with platform=`windows`
    """
    _SDM_NAME = None

    def __init__(self, ip_address, rest_port=443, platform='windows', log_file_name=None, ignore_env_proxy=False):
        super(TestPlatform, self).__init__(None)
        self._connection = Connection(ip_address, rest_port, platform, log_file_name, ignore_env_proxy)
        self._set_default_href()
         
    def _set_default_href(self, href='/api/v1'):
        self._set_properties({'href': href}, clear=True)

    def Authenticate(self, uid, pwd):
        """Set the X-Api-Key by authenticating against the connected TestPlatform
        
        Args:
            uid (str): The userid to be authenticated
            pwd (str): The password to be authenticated

        Raises:
            UnauthorizedError: Access is unauthorized
            ServerError: The server has encountered an uncategorized error condition

        Example:
            test_platform = TestPlatform('127.0.0.1')
            test_platform.Authenticate('admin', 'admin')
         """
        self._set_default_href('/api/v1/auth/session')
        response = self._execute(None, payload={'username': uid, 'password': pwd})
        self.ApiKey = response['apiKey']
        self._set_default_href()

    @property
    def Trace(self):
        """Trace http transactions to console
        
        Returns:
            str(none|request|request_response): Enables tracing of the connection transport request and responses
        """
        return self._connection.trace
    @Trace.setter
    def Trace(self, trace):
        self._connection.trace = trace

    @property
    def ApiKey(self):
        """Set the X-Api-Key for authorizing transactions instead of using the authenticate method
        
        Returns:
            bool
        """
        return self._connection.x_api_key
    @ApiKey.setter
    def ApiKey(self, value):
        self._connection.x_api_key = value

    @property
    def Sessions(self):
        """An instance of the Sessions class

        Returns:
            obj(ixnetwork_restpy.testplatform.sessions.sessions.Sessions): A Sessions object
        """
        from ixnetwork_restpy.testplatform.sessions.sessions import Sessions
        return Sessions(self)
