class PublishWorkbookRequest(BaseRequest):
    """
    Create site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param workbook_name:
    :type workbook_name:
    :param project_id:
    :type project_id:
    :param boundary_string:
    :type boundary_string:
    :param show_tabs_flag:
    :type show_tabs_flag:
    :param user_id:
    :type user_id:
    :param server_address:
    :type server_address:
    :param port_number:
    :type port_number:
    :param connection_username:
    :type connection_username:
    :param connection_password:
    :type connection_password:
    :param embed_credentials_flag:
    :type embed_credentials_flag:
    :param oauth_flag:
    :type oauth_flag:
    :param workbook_views_to_hide:
    :type workbook_views_to_hide:
    :param hide_view_flag:
    :type hide_view_flag:
    """
    def __init__(self,
                 ts_connection,
                 workbook_name,
                 # workbook_file_name,
                 # content_of_workbook_file,
                 project_id,
                 boundary_string,
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
        # self._workbook_file_name = workbook_file_name
        # self._content_of_workbook_file = content_of_workbook_file
        self._project_id = project_id
        self._boundary_string = boundary_string
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

    def get_request(self):
        return self.modified_publish_workbook_request
