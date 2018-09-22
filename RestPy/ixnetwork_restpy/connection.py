"""Http/Https transport
"""
import sys
import os
import ssl
import datetime
import time
import json
import requests
import logging
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

    def __init__(self, hostname, rest_port=443, platform='windows'):
        """ Set the connection parameters to a rest server

        Args:
            hostname (str): hostname or ip address
            rest_port (int, optional, default=443): the rest port of the server
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
        self._trace = Connection.TRACE_NONE
        self._scheme = 'https'
        if platform == 'windows':
            self._scheme = 'http'

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
            logging.getLogger().setLevel(logging.WARNING)
        if self._trace in [Connection.TRACE_REQUEST, Connection.TRACE_REQUEST_RESPONSE]:
            logging.getLogger().setLevel(logging.DEBUG)

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
                data = open(payload.file_path, 'rb')
            elif isinstance(payload, basestring):
                headers['Content-Type'] = 'application/json'
                data = payload

        self._print_request(method, url, data)
        response = requests.request(method, url, data=data, headers=headers, verify=self._verify_cert, allow_redirects=False)
        self._print_response(response)
        
        if str(response.status_code).startswith('3'):
            self._scheme = 'https'
            url = response.headers['location']
            self._print_request(method, url, data)
            response = requests.request(method, url, data=data, headers=headers, verify=self._verify_cert, allow_redirects=False)
            self._print_response(response)

        if isinstance(payload, Files):
            data.close()

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
                    response = requests.request('GET', state_url, headers=headers, verify=self._verify_cert)
                elif state == 'SUCCESS':
                    if 'result' in async_status.keys():
                        return async_status['result']
                    else:
                        return None
                elif 'API CONTENTION' in async_status['message']:
                    raise ResourceInUseError(response)
                else:
                    raise ServerError(response) 
        
        while(response.status_code == 409):
            time.sleep(6)
            response = requests.request(method, url, data=data, headers=headers, verify=self._verify_cert)

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

