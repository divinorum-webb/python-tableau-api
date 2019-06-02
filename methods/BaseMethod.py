from requests.packages.urllib3.fields import RequestField
from requests.packages.urllib3.filepost import encode_multipart_formdata


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

    @staticmethod
    def _make_multipart(parts):
        """
        Creates one "chunk" for a multi-part file upload to apply to a POST request.

        :param parts:                       'parts' is a dictionary that provides key-value pairs of the
                                            format name: (filename, body, content_type).
        :returns post_body, content_type:   Returns the post body and the content type string.
        """
        mime_multipart_parts = []
        for name, (filename, blob, content_type) in parts.items():
            multipart_part = RequestField(name=name, data=blob, filename=filename)
            multipart_part.make_multipart(content_type=content_type)
            mime_multipart_parts.append(multipart_part)

        post_body, content_type = encode_multipart_formdata(mime_multipart_parts)
        content_type = ''.join(('multipart/mixed',) + content_type.partition(';')[1:])
        return post_body, content_type

    @verify_response(self._success_code)
    def send_request(self, headers=None):
        pass

    # def get_request_headers(self):
    #     #     request_headers = self._connection.default_headers.copy()
    #     #     if self._request_type in ['post', 'put']:
    #     #         request_content_length = len(str(self._request))
    #     #         request_headers.update({'Content-Length': str(request_content_length)})
    #     #     return request_headers
