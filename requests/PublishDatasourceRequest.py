class PublishDatasourceRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:           The Tableau Server connection object.
    :type ts_connection:            class
    :param datasource_name:         The name for the datasource being published.
    :type datasource_name:          string
    :param project_id:              The project ID for the project the datasource belongs to.
    :type project_id:               string
    :param connection_username:     If the datasource requires credentials, this value specifies
                                    the connection username.
    :type connection_username:      string
    :param connection_password:     If the datasource requires credentials, this value specifies
                                    the connection password.
    :type connection_password:      string
    :param embed_credentials_flag:  Boolean flag; True if credentials are to be stored for when the connection is used,
                                    False otherwise.
    :type embed_credentials_flag:   boolean
    :param oauth_flag:              Boolean flag; True if the data connection username is an OAuth username,
                                    False otherwise.
    :type oauth_flag:               boolean
    """
    def __init__(self,
                 ts_connection,
                 datasource_name,
                 project_id,
                 connection_username=None,
                 connection_password=None,
                 embed_credentials_flag=False,
                 oauth_flag=False
                 ):
        super().__init__(ts_connection)
        self._datasource_name = datasource_name
        self._project_id = project_id
        self._connection_username = connection_username
        self._connection_password = connection_password
        self._embed_credentials_flag = embed_credentials_flag
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
            'true' if self._embed_credentials_flag is True else 'false' if self._embed_credentials_flag is False else None,
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

    # testing for chunk upload
    def publish_prep(self, file_path):
        filename = os.path.basename(file_path)
        file_extension = os.path.split('.')[1]

        file_size = os.path.getsize(file_path)
        self.file_is_chunked = True

        upload_session_id = self._connection.initiate_file_upload().json()['fileUpload']['uploadSessionId']
        chunks = self.read_chunks(file_path)
        for chunk in chunks:
            request, content_type = self.chunk_req(chunk)
            file_upload = self._connection.append_to_file_upload(upload_session_id=upload_session_id,
                                                                 payload=request,
                                                                 content_type=content_type)
        return filename, file_extension, upload_session_id


    @staticmethod
    def read_chunks(file_path):
        with open(file_path, 'rb') as f:
            while True:
                chunked_content = f.read(CHUNK_SIZE)
                if not chunked_content:
                    break
                yield chunked_content

    def chunk_req(self, chunk):
        parts = {'request_payload': (None, '', 'application/json'),
                 'tableau_file': ('file', chunk, 'application/octet-stream')}
        return self._add_multipart(parts)

    @staticmethod
    def _add_multipart(parts):
        mime_multipart_parts = list()
        for name, (filename, data, content_type) in parts.items():
            multipart_part = RequestField(name=name, data=data, filename=filename)
            multipart_part.make_multipart(content_type=content_type)
            mime_multipart_parts.append(multipart_part)
        request, content_type = encode_multipart_formdata(mime_multipart_parts)
        content_type = ''.join(('multipart/mixed',) + content_type.partition(';')[1:])
        return request, content_type

    def _publish_chunked_file_request(self):
        request = self.modified_publish_datasource_request
        parts = {'request_payload': (None, json.dumps(request), 'application/json')}
        return self._add_multipart(parts)

    def _publish_single_file_request(self):
        request = self.modified_publish_datasource_request
        parts = {'request_payload': (None, json.dumps(request), 'application/json'),
                 'tableau_datasource': (datasource_file, datasource_bytes, 'application/octet-stream')}
        return self._add_mutlipart(parts)

    def get_request(self):
        if self.file_is_chunked:
            print('publishing chunked file')
            return self._publish_chunked_file_request()
        else:
            print('publishing single file')
            return self._publish_single_file_request()
