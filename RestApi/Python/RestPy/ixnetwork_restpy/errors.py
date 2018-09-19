""" Transport error classes
"""
from requests import Response


class IxNetworkError(Exception):
    """The base error class for all IxNetwork REST API errors"""
    def __init__(self, response):
        if isinstance(response, Response):
            if response.status_code == 202:
                self._url = response.url
                async_status = response.json()
                self._status_code = async_status["state"]
                self._reason = async_status["message"]
                self._text = async_status["result"]
            else:
                self._url = response.url
                self._status_code = response.status_code
                self._reason = response.reason
                self._text = response.text
            self._message = '%s => %s %s %s' % (self._url, self._status_code, self._reason, self._text)
        else:
            self._message = response

    @property
    def message(self):
        return self._message

    @property
    def status_code(self):
        return self._status_code
        
    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message


class AsyncOperationError(IxNetworkError):
    """Operation has failed
    """
    def __init__(self, response):
        super(AsyncOperationError, self).__init__(response)


class UnauthorizedError(IxNetworkError):
    """Access is unauthorized

	Authorization has not been successfully completed.
	Use the IxNetwork.auth method or the IxNetwork.api_key property prior to using any other functionality.
	"""
    def __init__(self, response):
        super(UnauthorizedError, self).__init__(response)


class AlreadyExistsError(IxNetworkError):
    """The requested resource already exists on the server"""
    def __init__(self, response):
        super(AlreadyExistsError, self).__init__(response)


class BadRequestError(IxNetworkError):
    """The server has determined that the request is incorrect"""
    def __init__(self, response):
        super(BadRequestError, self).__init__(response)


class NotFoundError(IxNetworkError):
    """The requested resource does not exist on the server"""
    def __init__(self, response):
        super(NotFoundError, self).__init__(response)


class ResourceInUseError(IxNetworkError):
    """Resource in use
    
    The requested resource is in use by another request made to the server.
    The request will be retried 10 times with a wait of 6 seconds in between each retry. 
    After the retry period has elapsed this error will be raised.
    """
    def __init__(self, response):
        super(ResourceInUseError, self).__init__(response)


class ServerError(IxNetworkError):
    """The server has encountered an uncategorized error condition"""
    def __init__(self, response):
        super(ServerError, self).__init__(response)
