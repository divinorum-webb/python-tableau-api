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
