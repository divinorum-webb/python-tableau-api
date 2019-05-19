class UpdateDatasourceConnectionRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param server_address:
    :type server_address:
    :param port:
    :type port:
    :param connection_username:
    :type connection_username:
    :param connection_password:
    :type connection_password:
    :param embed_password:
    :type embed_password:
    """
    def __init__(self,
                 ts_connection,
                 server_address,
                 port,
                 connection_username,
                 connection_password,
                 embed_password=False):

        super().__init__(ts_connection)
        self._server_address = server_address
        self._port = port
        self._connection_username = connection_username
        self._connection_password = connection_password
        self._embed_password = embed_password

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
            'true' if self._embed_password == True else 'false' if self._embed_password == False else None
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
