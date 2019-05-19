class PublishDatasourceRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param datasource_name:
    :type datasource_name:
    :param project_id:
    :type project_id:
    :param connection_username:
    :type connection_username:
    :param connection_password:
    :type connection_password:
    :param embed_flag:
    :type embed_flag:
    :param oauth_flag:
    :type oauth_flag:
    """
    def __init__(self,
                 ts_connection,
                 datasource_name,
                 #                  datasource_file_name,
                 #                  content_of_datasource_file,
                 project_id,
                 #                  boundary_string,
                 connection_username=None,
                 connection_password=None,
                 embed_flag=False,
                 oauth_flag=False
                 ):
        super().__init__(ts_connection)
        self._datasource_name = datasource_name
        #         self._datasource_file_name = datasource_file_name
        #         self._content_of_datasource_file = content_of_datasource_file
        self._project_id = project_id
        #         self._boundary_string = boundary_string
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
            'true' if self._embed_flag == True else 'false' if self._embed_flag == False else None,
            'true' if self._oauth_flag == True else 'false' if self._oauth_flag == False else None
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

    def get_request(self):
        return self.modified_publish_datasource_request
