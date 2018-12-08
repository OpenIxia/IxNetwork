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
import os
import ssl
import datetime
import time
import json
import logging
from requests import Session
from io import BufferedReader
from ixnetwork_restpy.errors import *
from ixnetwork_restpy.files import Files


try:
    basestring
except NameError:
    basestring = str


class Connection(object):
    """Http/Https transport"""
    X_API_KEY = 'X-Api-Key'
    TRACE_NONE = 'none'
    TRACE_REQUEST = 'request'
    TRACE_REQUEST_RESPONSE = 'request_response'

    def __init__(self, hostname, rest_port=443, platform='windows', log_file_name=None, ignore_env_proxy=False):
        """ Set the connection parameters to a rest server

        Args:
            hostname (str): hostname or ip address
            rest_port (int, optional, default=443): the rest port of the server
            platform (str): 
            log_file_name (str):
            ignore_env_proxy (bool):
        """
        if sys.version < '2.7.9':
            import requests.packages.urllib3
            requests.packages.urllib3.disable_warnings()
        else:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._headers = {
            Connection.X_API_KEY: None
        }
        self._hostname = hostname
        self._rest_port = rest_port
        self._verify_cert = False
        self._scheme = 'https'
        if platform == 'windows':
            self._scheme = 'http'
        self._session = Session()

        if ignore_env_proxy is True:
            self._session.proxies.update({
                'http': None,
                'https': None
            })

        # setup logging to both console and file if requested
        self._trace = Connection.TRACE_NONE
        handlers = [logging.StreamHandler(sys.stdout)]
        if log_file_name is not None:
            handlers.append(logging.FileHandler(log_file_name, mode='w'))
        formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        formatter.converter = time.gmtime
        for handler in handlers:
            handler.setFormatter(formatter)
            logging.getLogger(__name__).addHandler(handler)

    @property
    def trace(self):
        """str: Trace all requests and responses."""
        return self._trace
    @trace.setter
    def trace(self, value):
        if value not in [Connection.TRACE_NONE, Connection.TRACE_REQUEST, Connection.TRACE_REQUEST_RESPONSE]:
            raise ValueError('the value %s is an incorrect Trace level' % value)
        self._trace = value
        if self._trace == Connection.TRACE_NONE:
            logging.getLogger(__name__).setLevel(logging.WARNING)
        if self._trace in [Connection.TRACE_REQUEST, Connection.TRACE_REQUEST_RESPONSE]:
            logging.getLogger(__name__).setLevel(logging.DEBUG)

    @property
    def x_api_key(self):
        """str: Get/Set the x-api-key header value."""
        return self._headers[Connection.X_API_KEY]
    @x_api_key.setter
    def x_api_key(self, value):
        self._headers[Connection.X_API_KEY] = value

    def _read(self, url):
        return self._send_recv('GET', url)

    def _create(self, url, payload):
        return self._send_recv('POST', url, payload)

    def _update(self, url, payload):
        return self._send_recv('PATCH', url, payload)

    def _delete(self, url, payload=None):
        return self._send_recv('DELETE', url, payload)

    def _execute(self, url, payload):
        return self._send_recv('POST', url, payload)

    def _options(self, url):
        return self._send_recv('OPTIONS', url)

    def _print_request(self, method, url, payload=None):
        if self._trace in [Connection.TRACE_REQUEST, Connection.TRACE_REQUEST_RESPONSE]:
            logging.getLogger(__name__).debug('%s %s %s' % (method, url, payload))
    
    def _print_response(self, response):
        if self._trace == Connection.TRACE_REQUEST_RESPONSE:
            logging.getLogger(__name__).debug('%s %s %s' % (response.status_code, response.reason, response.raw.data))
    
    def _send_recv(self, method, url, payload=None):
        connection = '%s://%s:%s' % (self._scheme, self._hostname, self._rest_port)
        headers = self._headers
        if url.startswith(self._scheme) == False:
            url = '%s/%s' % (connection, url.strip('/'))
        
        path_start = url.find('://') + 3
        url = '%s%s' % (url[0:path_start], url[path_start:].replace('//', '/'))

        data = payload
        if payload is not None:
            if isinstance(payload, dict) or isinstance(payload, list):
                headers['Content-Type'] = 'application/json'
                data = json.dumps(payload)
            elif isinstance(payload, Files):                          
                headers['Content-Type'] = 'application/octet-stream'
                if os.path.isfile(payload.file_path):
                    with open(payload.file_path, 'rb') as fid:
                        data = fid.read()
                else:
                    response = self._session.request('GET', url.replace('filename=', 'filter='), headers=headers, verify=self._verify_cert, allow_redirects=False)
                    if response.status_code == 200:
                        return
                    data = ''
            elif isinstance(payload, basestring):
                headers['Content-Type'] = 'application/json'
                data = payload

        self._print_request(method, url, None if isinstance(payload, Files) else data)
        response = self._session.request(method, url, data=data, headers=headers, verify=self._verify_cert, allow_redirects=False)
        self._print_response(response)
        
        if str(response.status_code).startswith('3'):
            url = response.headers['location']
            if url.find('://') != -1:
                self._scheme = url[:url.find('://')]
                self._hostname = url[url.find('://')+3:url.find('/', url.find('://')+3)]
                if self._scheme == 'https':
                    self._rest_port = 443
                host_pieces = self._hostname.split(':')
                if len(host_pieces) > 1:
                    self._hostname = host_pieces[0]
                    self._rest_port = host_pieces[1]
            else:
                url = '%s://%s:%s%s' % (self._scheme, self._hostname, self._rest_port, url)
            self._print_request(method, url, data)
            response = self._session.request(method, url, data=data, headers=headers, verify=self._verify_cert, allow_redirects=False)
            self._print_response(response)

        if response.status_code == 202:
            while True:
                async_status = response.json()
                if 'state' not in async_status.keys():
                    break
                state = async_status['state']
                if state == 'IN_PROGRESS':
                    time.sleep(1)
                    state_url = async_status['url']
                    if state_url.startswith(self._scheme) == False:
                        state_url = '%s/%s' % (connection, state_url.strip('/'))
                    self._print_request('GET', state_url)
                    response = self._session.request('GET', state_url, headers=headers, verify=self._verify_cert)
                    self._print_response(response)
                elif state == 'SUCCESS':
                    if 'result' in async_status.keys():
                        return async_status['result']
                    else:
                        return None
                elif async_status['message'] is not None and 'API CONTENTION' in async_status['message']:
                    raise ResourceInUseError(response)
                else:
                    raise ServerError(response) 
        
        while(response.status_code == 409):
            time.sleep(6)
            response = self._session.request(method, url, data=data, headers=headers, verify=self._verify_cert)

        if response.status_code == 204:
            return None
        elif str(response.status_code).startswith('2') is True:
            if response.status_code == 201 and 'links' in response.json().keys():
                href = response.json()['links'][0]['href']
                return self._send_recv('GET', href)
            if response.headers.get('Content-Type'):
                if 'application/json' in response.headers['Content-Type']:
                   return response.json()
            return None
        elif response.status_code == 400:
            raise BadRequestError(response)
        elif response.status_code == 401:
            raise UnauthorizedError(response)
        elif response.status_code == 404:
            raise NotFoundError(response)
        elif response.status_code == 409:
            raise ResourceInUseError(response)
        else:
            raise ServerError(response)

