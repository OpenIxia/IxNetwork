
"""
A script that shows how to use REST APIs to connect to a Linux 
based chassis including IxVM chassis to retrieve chassis, card/port info.
"""

import json
import time
import requests

# hide warnings related to unsigned ssl certificates to keep logs cleaner
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except: pass

# most frequently used variables
CHASSIS = '192.168.70.11'
USER = 'admin'
PASSWORD = 'admin'

# examples below target following card/port
CARD = 1
PORT = 1

# If True, will print every HTTP request/response header and body
VERBOSE = True
class IxRestException(Exception): pass

class IxRestSession(object):
    """
    class for handling HTTP requests/response for IxOS REST APIs
    """

    def __init__(self):
        try:
            self.chassis_ip = CHASSIS
            self.username = USER
            self.password = PASSWORD
            self.api_key = ''
            self.timeout = 500
            self.poll_interval = 2
            self.verbose = VERBOSE
            self.authenticate()
        except:
            raise

    def get_ixos_uri(self):
        return 'https://%s/chassis/api/v2/ixos' % self.chassis_ip

    def get_headers(self):
        # headers should at least contain these two
        return {
            "Content-Type": "application/json",
            'x-api-key': self.api_key
        }

    def authenticate(self):
        """
        we need to obtain API key to be able to perform any REST
        calls on IxOS
        """

        try:
            print('getting api key ...')
            payload = {
                'username': self.username,
                'password': self.password,
                'rememberMe': False
            }
            response = self.http_request(
                'POST',
                'https://%s/platform/api/v1/auth/session' % self.chassis_ip,
                payload=payload
                )
            self.api_key = response.data['apiKey']
            print('api key is %s' % self.api_key)
        except:
            raise

    def http_request(self, method, uri, payload=None, params=None):
        """
        wrapper over requests.requests to pretty-print debug info
        and invoke async operation polling depending on HTTP status code (e.g. 202)
        """
        try:
            # lines with 'debug_string' can be removed without affecting the code
            if not uri.startswith('http'):
                uri = self.get_ixos_uri() + uri

            debug_string = 'Request => %s %s\n' % (method, uri)

            if payload is not None:
                payload = json.dumps(payload, indent=2, sort_keys=True)

            headers = self.get_headers()

            if self.verbose:
                debug_string += 'Params:\n' + json.dumps(params, indent=2, sort_keys=True) + '\n'
                debug_string += 'Headers:\n' + json.dumps(headers, indent=2, sort_keys=True) + '\n'
                debug_string += 'Payload:\n' + str(payload) + '\n'

            print(debug_string)
            response = requests.request(
                method, uri, data=payload, params=params,
                headers=headers, verify=False
            )

            debug_string = 'Response => Status %d\n' % response.status_code
            data = response.content.decode()

            try:
                data = json.loads(data) if data else None
            except:
                print('Invalid/Non-JSON payload received: %s' % data)
                data = None

            if self.verbose:
                debug_string += 'Headers:\n' + json.dumps(dict(response.headers), indent=2, sort_keys=True) + '\n'
                if data:
                    debug_string += 'Payload:\n' + json.dumps(data, indent=2, sort_keys=True) + '\n'

            print(debug_string)

            if response.status_code == 202:
                return self.wait_for_async_operation(data)
            else:
                response.data = data
                return response
        except:
            raise

    def wait_for_async_operation(self, response_body):
        """
        method for handeling intermediate async operation results
        """
        try:
            print('Polling for async operation ...')
            operation_status = response_body['state']
            start_time = int(time.time())
            while operation_status == 'IN_PROGRESS':
                response = self.http_request('GET', response_body['url'])
                response_body = response.data
                operation_status = response_body['state']
                if int(time.time() - start_time) > self.timeout:
                    raise IxRestException('timeout occured while polling for async operation')

                time.sleep(self.poll_interval)

            if operation_status == 'COMPLETED':
                return response
            else:
                raise IxRestException('async operation failed')
        except:
            raise
        finally:
            print('Completed async operation')

    def get_chassis(self, params=None):
        return self.http_request('GET', self.get_ixos_uri() + '/chassis', params=params)

    def get_cards(self, params=None):
        return self.http_request('GET', self.get_ixos_uri() + '/cards', params=params)

    def get_ports(self, params=None):
        return self.http_request('GET', self.get_ixos_uri() + '/ports', params=params)

    def get_services(self, params=None):
        return self.http_request('GET', self.get_ixos_uri() + '/services', params=params)

    def take_ownership(self, resource_id):
        return self.http_request(
            'POST',
            self.get_ixos_uri() + '/ports/%d/operations/takeownership' % resource_id
        )

    def release_ownership(self, resource_id):
        return self.http_request(
            'POST',
            self.get_ixos_uri() + '/ports/%d/operations/releaseownership' % resource_id
        )

    def reboot_port(self, resource_id):
        return self.http_request(
            'POST',
            self.get_ixos_uri() + '/ports/%d/operations/reboot' % resource_id
        )

    def reset_port(self, resource_id):
        return self.http_request(
            'POST',
            self.get_ixos_uri() + '/ports/%d/operations/resetfactorydefaults' % resource_id
        )

    def hotswap_card(self, resource_id):
        return self.http_request(
            'POST',
            self.get_ixos_uri() + '/cards/%d/operations/hotswap' % resource_id
        )

def main():
    """
    execution starts here
    """
    try:
        session = IxRestSession()
        # Get all chassis/cards/ports
        session.get_chassis()
        session.get_cards()
        session.get_ports()

        # Get card/port using card/port number
        card = session.get_cards(params={'cardNumber': CARD}).data[0]
        port = session.get_ports(params={'cardNumber': CARD, 'portNumber': PORT}).data[0]

        # Port specific operations
        session.take_ownership(port['id'])
        session.reboot_port(port['id'])
        session.reset_port(port['id'])
        session.release_ownership(port['id'])

        # Card specific operations
        session.hotswap_card(card['id'])

        # Chassis specific operations
        session.get_services()
    except:
        raise

if __name__ == '__main__':
    main()

