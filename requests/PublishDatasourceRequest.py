class PublishDatasourceRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param datasource_name:     The name for the datasource being published.
    :type datasource_name:      string
    :param project_id:          The project ID for the project the datasource belongs to.
    :type project_id:           string
    :param connection_username: If the datasource requires credentials, this value specifies the connection username.
    :type connection_username:  string
    :param connection_password: If the datasource requires credentials, this value specifies the connection password.
    :type connection_password:  string
    :param embed_flag:          Boolean flag; True if credentials are to be stored for when the connection is used,
                                False otherwise.
    :type embed_flag:           boolean
    :param oauth_flag:          Boolean flag; True if the data connection username is an OAuth username,
                                False otherwise.
    :type oauth_flag:           boolean
    """
    def __init__(self,
                 ts_connection,
                 datasource_name,
                 project_id,
                 connection_username=None,
                 connection_password=None,
                 embed_flag=False,
                 oauth_flag=False
                 ):
        super().__init__(ts_connection)
        self._datasource_name = datasource_name
        self._project_id = project_id
        self._connection_username = connection_username
        self._connection_password = connection_password
        self._embed_flag = embed_flag
        self._oauth_flag = oauth_flag
        self.base_publish_datasource_request

    @property
    def optional_credentials_param_keys(self):
        return [
            'name',
            'password',
            'embed',
            'oAuth'
        ]

    @property
    def optional_credentials_param_values(self):
        return [
            self._connection_username,
            self._connection_password,
            'true' if self._embed_flag is True else 'false' if self._embed_flag is False else None,
            'true' if self._oauth_flag is True else 'false' if self._oauth_flag is False else None
        ]

    @property
    def base_publish_datasource_request(self):
        self._request_body.update({
            'datasource': {
                'name': self._datasource_name,
                'project': {'id': self._project_id}
            }
        })
        return self._request_body

    @property
    def modified_publish_datasource_request(self):
        if any(self.optional_credentials_param_values):
            self._request_body['datasource'].update({'connectionCredentials': {}})
            self._request_body['datasource']['connectionCredentials'].update(
                self._get_parameters_dict(self.optional_credentials_param_keys,
                                          self.optional_credentials_param_values))
        return self._request_body

    @staticmethod
    def get_datasource(datasource_file_path):
        datasource_file = os.path.basename(datasource_file_path)
        with open(datasource_file_path, 'rb') as f:
            datasource_bytes = f.read()
        if 'tdsx' in datasource_file_path.split('.'):
            datasource_type = 'tdsx'
        elif 'tds' in datasource_file_path.split('.'):
            datasource_type = 'tds'
        elif 'tde' in datasource_file_path.split('.'):
            datasource_type = 'tde'
        else:
            raise Exception('Invalid datasource type provided. Datasource must be a tdsx, tds, or tde file.')
        return datasource_file, datasource_bytes, datasource_type

    def _make_multipart(self, datasource_file_path):
        """
        Creates one "chunk" for a multi-part file upload to apply to a POST request.
        'parts' is a dictionary that provides key-value pairs of the
        format name: (filename, body, content_type).

        :param datasource_file_path:                            The file path for the datasource.
        :type datasource_file_path:                             string
        :returns payload, content_type, datasource_type:        Returns the post request body, the content-type header,
                                                                and the type of the datasource being published.
        """
        datasource_file, datasource_bytes, datasource_type = self.get_datasource(datasource_file_path)
        parts = {'request_payload': (None, json.dumps(self.get_request()), 'application/json'),
                 'tableau_datasource': (datasource_file, datasource_bytes, 'application/octet-stream')}

        mime_multipart_parts = []
        for name, (filename, blob, content_type) in parts.items():
            multipart_part = RequestField(name=name, data=blob, filename=filename)
            multipart_part.make_multipart(content_type=content_type)
            mime_multipart_parts.append(multipart_part)

        payload, content_type = encode_multipart_formdata(mime_multipart_parts)
        content_type = ''.join(('multipart/mixed',) + content_type.partition(';')[1:])
        return payload, content_type, datasource_type

    def get_headers(self, new_content_type):
        headers = self._connection.default_headers.copy()
        headers['Content-Type'] = new_content_type
        return headers

    def get_request(self):
        return self.modified_publish_datasource_request
