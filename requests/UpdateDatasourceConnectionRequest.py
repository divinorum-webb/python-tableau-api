class UpdateDatasourceConnectionRequest(BaseRequest):
    """
    Update datasource connection request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param server_address:      The new server address for the connection.
    :type server_address:       string
    :param port:                The new port for the connection.
    :type port:                 string
    :param connection_username: The new username for the connection.
    :type connection_username:  string
    :param connection_password: The new password for the connection.
    :type connection_password:  string
    :param embed_password_flag: Boolean flag; True if embedding password in the datasource connection, False otherwise.
    :type embed_password_flag:  boolean
    """
    def __init__(self,
                 ts_connection,
                 server_address,
                 port,
                 connection_username,
                 connection_password,
                 embed_password_flag=False):

        super().__init__(ts_connection)
        self._server_address = server_address
        self._port = port
        self._connection_username = connection_username
        self._connection_password = connection_password
        self._embed_password_flag = embed_password_flag

    @property
    def required_connection_param_keys(self):
        return [
            'serverAddress',
            'serverPort',
            'userName',
            'password',
            'embedPassword'
        ]

    @property
    def required_connection_param_values(self):
        return [
            self._server_address,
            self._port,
            self._connection_username,
            self._connection_password,
            'true' if self._embed_password_flag is True else 'false' if self._embed_password_flag is False else None
        ]

    @property
    def base_update_datasource_connection_request(self):
        self._request_body.update({'connection': {}})
        return self._request_body

    @property
    def modified_update_datasource_connection_request(self):
        if all(self.required_connection_param_values):
            self._request_body.update(
                self._get_parameters_dict(self.required_connection_param_keys,
                                          self.required_connection_param_values))
        else:
            self._invalid_parameter_exception()
        return self._request_body

    def get_request(self):
        return self.modified_update_datasource_connection_request
