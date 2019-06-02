class BaseMethod:
    """
    Base method for building the methods listed on the Tableau Server API reference.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    """
    def __init__(self,
                 ts_connection,
                 request_endpoint,
                 success_code,
                 request_body=None,
                 request_type='get'
                 ):

        self._connection = ts_connection
        self._request_endpoint = request_endpoint
        self._request_body = request_body
        self._request_type = request_type
        self._success_code = success_code

    @verify_response(self._success_code)
    def send_request(self, headers=None):
        pass

    # def get_request_headers(self):
    #     #     request_headers = self._connection.default_headers.copy()
    #     #     if self._request_type in ['post', 'put']:
    #     #         request_content_length = len(str(self._request))
    #     #         request_headers.update({'Content-Length': str(request_content_length)})
    #     #     return request_headers
