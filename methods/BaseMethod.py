class BaseMethod:
    """
    Base method for building the methods listed on the Tableau Server API reference.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    """
    def __init__(self,
                 ts_connection,
                 endpoint,
                 request=None,
                 request_type='get'
                 ):

        self._connection = ts_connection
        self._endpoint = endpoint
        self._request = request
        self._request_type = request_type

    def get_request_headers(self):
        request_headers = self._connection.default_headers.copy()
        if self._request_type in ['post', 'put']:
            request_content_length = len(str(self._request))
            request_headers.update({'Content-Length': str(request_content_length)})
        return request_headers