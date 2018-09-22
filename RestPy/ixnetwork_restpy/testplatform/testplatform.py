import sys
import time
import logging
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.connection import Connection
from ixnetwork_restpy.errors import NotFoundError


class TestPlatform(Base):
    _SDM_NAME = None

    def __init__(self, ip_address, rest_port=443, platform='windows', log_file_name=None):
        """Top level access to an IxNetwork test tool platform (Linux API Server, Windows GUI, ConnectionManager)

        Args:
            ip_address (str): the ip address of the test tool platform that requests will be made to
            rest_port (number): the ip port of the test tool platform that the server is listening on
            platform (str[windows|linux]): the platform type that is being connected to
            log_file_name (str): the name of the log file that trace logging will be written to, if omitted it will be written to the console
        """
        super(TestPlatform, self).__init__(None)
        self._connection = Connection(ip_address, rest_port, platform)
        self._set_default_href()

        # setup logging to both console and file if requested
        handlers = [logging.StreamHandler(sys.stdout)]
        if log_file_name is not None:
            handlers.append(logging.FileHandler(log_file_name, mode='w'))
        formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logging.Formatter.converter = time.gmtime
        for handler in handlers:
            handler.setFormatter(formatter)
            logging.getLogger('').addHandler(handler)
         
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
        """Get a list of test tool sessions on the connected TestPlatform

        Args:
            Id (number): The session Id of an existing session

        Returns:
            list(obj(ixnetwork_restpy.testplatform.sessions.sessions.Sessions)): A list of Sessions objects

        Raises:
            NotFoundError: No session matching Id was found
            UnauthorizedError: Access is unauthorized
            ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.sessions import Sessions
        return Sessions(self)

        # sessions = self._read(Sessions(self), None)
        # if Id is not None:
        #     for session in sessions:
        #         if session.Id == Id:
        #             return session
        #     raise NotFoundError('No session exists for id %s' % Id) 
        # else:
        #     return sessions
