CHUNK_SIZE = 1024 * 1024 * 5  # 5MB


class PublishWorkbookRequest(BaseRequest):
    """
    Publish workbook request for API requests to Tableau Server.

    :param ts_connection:               The Tableau Server connection object.
    :type ts_connection:                class
    :param workbook_name:               The name the published workbook will have on Tableau Server.
    :type workbook_name:                string
    :param project_id:                  The project ID of the project the workbook is being published to.
    :type project_id:                   string
    :param show_tabs_flag:              Boolean flag; True if the workbook will show views as tabs, false otherwise.
    :type show_tabs_flag:               boolean
    :param user_id:                     If generating thumbnails as a specific user, specify the user ID here.
    :type user_id:                      string
    :param server_address:              Specify the server address for a data source connection if that data source
                                        does not use OAuth.
    :type server_address:               string
    :param port_number:                 Specify the port number for a data source connection if that data source does
                                        not use OAuth.
    :type port_number:                  string
    :param connection_username:         (Optional) If the workbook's data source connections require credentials, the
                                        <connectionCredentials> elements are included and this attribute specifies the
                                        connection username. If the element is included but is not required
                                        (for example, if the data source uses OAuth), the server ignores the
                                        element and its attributes.
    :type connection_username:          string
    :param connection_password:         (Optional) If the workbook's data source connections require credentials, the
                                        <connectionCredentials> elements are included and this attribute specifies the
                                        connection password. If the element is included but is not required (for
                                        example, if the data source uses OAuth), the server ignores the element
                                        and its attributes.
    :type connection_password:          string
    :param embed_credentials_flag:      Boolean flag; True if embedding credentials in the published workbook,
                                        False otherwise.
    :type embed_credentials_flag:       boolean
    :param oauth_flag:                  Boolean flag; True if OAuth is used for the credentials, False otherwise.
    :type oauth_flag:                   boolean
    :param workbook_views_to_hide:      A list of the views to hide for the workbook being published. The list should
                                        contain the view names, not view IDs.
    :type workbook_views_to_hide:       list
    :param hide_view_flag:              Boolean flag; True if the published workbook will hide any of its views,
                                        False otherwise.
    :type hide_view_flag:               boolean
    """
    def __init__(self,
                 ts_connection,
                 workbook_name,
                 project_id,
                 show_tabs_flag=False,
                 user_id=None,
                 server_address=None,
                 port_number=None,
                 connection_username=None,
                 connection_password=None,
                 embed_credentials_flag=False,
                 oauth_flag=False,
                 workbook_views_to_hide=None,
                 hide_view_flag=False):

        super().__init__(ts_connection)
        self._workbook_name = workbook_name
        self._project_id = project_id
        self._show_tabs_flag = show_tabs_flag
        self._user_id = user_id
        self._server_address = server_address
        self._port_number = port_number
        self._connection_username = connection_username
        self._connection_password = connection_password
        self._embed_credentials_flag = embed_credentials_flag
        self._oauth_flag = oauth_flag
        self._workbook_views_to_hide = workbook_views_to_hide
        self._hide_view_flag = hide_view_flag
        self.payload = None
        self.content_type = None
        self.file_is_chunked = False
        self.base_publish_workbook_request

    @property
    def optional_workbook_param_keys(self):
        return [
            'showTabs',
            'generateThumbnailsAsUser'
        ]

    @property
    def optional_connection_param_keys(self):
        return [
            'serverAddress',
            'serverPort'
        ]

    @property
    def optional_credentials_param_keys(self):
        return [
            'name',
            'password',
            'embed',
            'oAuth'
        ]

    @property
    def optional_view_param_keys(self):
        return [
            'name',
            'hidden'
        ]

    @property
    def optional_workbook_param_values(self):
        return [
            self._show_tabs_flag,
            self._user_id
        ]

    @property
    def optional_connection_param_values(self):
        return [
            self._server_address,
            self._port_number
        ]

    @property
    def optional_credentials_param_values(self):
        return [
            self._connection_username,
            self._connection_password,
            self._embed_credentials_flag,
            self._oauth_flag
        ]

    @property
    def optional_view_param_values(self):
        values_list = []
        if self._hide_view_flag:
            [values_list.append(view_name) for view_name in self._workbook_views_to_hide]
        else:
            [values_list.append(None) for key in self.optional_view_param_keys]
        return values_list

    @property
    def base_publish_workbook_request(self):
        self._request_body.update({
            'workbook': {
                'name': self._workbook_name,
                'project': {'id': self._project_id}
            }
        })
        return self._request_body

    @property
    def modified_publish_workbook_request(self):
        self._request_body['workbook'].update(self._get_parameters_dict(self.optional_workbook_param_keys,
                                                                        self.optional_workbook_param_values))
        if any(self.optional_connection_param_values):
            self._request_body['workbook'].update({'connections': {}})
            self._request_body['workbook']['connections'].update(
                self._get_parameters_dict(
                    self.optional_connection_param_keys,
                    self.optional_connection_param_values))

        if any(self.optional_connection_param_values) and any(self.optional_credentials_param_values):
            self._request_body['workbook']['connections'].update({'connectionCredentials': {}})
            self._request_body['workbook']['connections']['connectionCredentials'].update(
                self._get_parameters_dict(
                    self.optional_credentials_param_keys,
                    self.optional_credentials_param_values))

        if any(self.optional_view_param_values):
            self._request_body['workbook'].update({'views': {'view': []}})
            for i, view in enumerate(self.optional_view_param_values):
                self._request_body['workbook']['views']['view'].append({
                    'name': view,
                    'hidden': 'true'
                })
        return self._request_body

    @staticmethod
    def get_workbook(workbook_file_path):
        workbook_file = os.path.basename(workbook_file_path)
        with open(workbook_file_path, 'rb') as f:
            workbook_bytes = f.read()
        if 'twbx' in workbook_file_path.split('.'):
            workbook_type = 'twbx'
        elif 'twb' in workbook_file_path.split('.'):
            workbook_type = 'twb'
        else:
            raise Exception('Invalid workbook type provided. Workbook must be a twbx or twb file.')
        return workbook_file, workbook_bytes, workbook_type

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
        request = self.modified_publish_workbook_request
        parts = {'request_payload': (None, json.dumps(request), 'application/json')}
        return self._add_multipart(parts)

    def _publish_single_file_request(self):
        request = self.modified_publish_workbook_request
        parts = {'request_payload': (None, json.dumps(request), 'application/json'),
                 'tableau_workbook': (workbook_file, workbook_bytes, 'application/octet-stream')}
        return self._add_mutlipart(parts)

    def get_request(self):
        if self.file_is_chunked:
            print('publishing chunked file')
            return self._publish_chunked_file_request()
        else:
            print('publishing single file')
            return self._publish_single_file_request()
