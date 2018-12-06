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
from ixnetwork_restpy.errors import IxNetworkError


class Sessions(Base):
    """Sessions class

    Manage IxNetwork sessions based on the connection information provided to the TestPlatform class.

    Child classes:  
        Sessions.Ixnetwork
    """
    _SDM_NAME = 'sessions'
    
    def __init__(self, parent):
        super(Sessions, self).__init__(parent)

    @property
    def Ixnetwork(self):
        """An instance of the Ixnetwork class
        
        Returns: 
            obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.ixnetwork.Ixnetwork):

        Raises: 
            ValueError: If the version of IxNetwork server is not suporrted. The minimum version supported is 8.42.
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.ixnetwork import Ixnetwork
        ixnetwork = Ixnetwork(self)
        build_number = ixnetwork._connection._read('%s/ixnetwork/globals' % self.href)['buildNumber']
        from distutils.version import LooseVersion
        if LooseVersion(build_number) < LooseVersion('8.42'):
            raise ValueError('IxNetwork server version %s is not supported. The minimum version supported is 8.42' % build_number)
        ixnetwork._set_properties(ixnetwork._connection._read('%s/%s' % (self.href, Ixnetwork._SDM_NAME)))
        return ixnetwork
    
    @property
    def State(self):
        """The state of the session

        Returns:
            str
        """
        return self._properties['state'].upper()
    
    @property
    def ApplicationType(self):
        """The application type of the session

        Returns:
            str
        """
        return self._properties['applicationType']
    
    @property
    def Id(self):
        """The id of the session

        Returns:
            number
        """
        return self._properties['id']
    
    @property
    def UserId(self):
        """The user id of the session

        Returns:
            str
        """
        return self._properties['userId']
    
    @property
    def UserName(self):
        """The user name of the session

        Returns:
            str
        """
        return self._properties['userName']

    def _start(self):
        """Starts the session

        Returns:
            None
        """
        import time
        if self.State.lower() == 'initial':
            self._execute('start', payload={'applicationType': self.ApplicationType})
    
    def find(self, Id=None):
        """Finds all child instances of Sessions on the server.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        responses = self._connection._read('%s/%s' % (self._parent.href, self._SDM_NAME))
        self._clear()
        for response in responses:
            if Id is not None:
                if response['id'] == Id:
                    self._set_properties(response)
            else:
                self._set_properties(response)
        return self

    def add(self):
        """Adds a new sessions node on the server and retrieves it in this instance.

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        applicationType = 'ixnrest'
        self._create(locals())
        self._start()
        return self

    def remove(self):
        """Deletes all the sessions data in this instance from server.

        Raises:
            NotFoundError: The requested resource does not exist on the server
            ServerError: The server has encountered an uncategorized error condition
        """
        try:
            self._execute('stop')
            self._delete()
        except IxNetworkError as e:
            if e._status_code not in [404, 405]:
                raise e