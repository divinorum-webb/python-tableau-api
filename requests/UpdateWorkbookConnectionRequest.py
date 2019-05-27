class UpdateWorkbookConnectionRequest(BaseRequest):
    """
    Update workbook connection request for sending API requests to Tableau Server.

    :param ts_connection:           The Tableau Server connection object.
    :type ts_connection:            class
    :param server_address:          The new server for the connection.
    :type server_address:           string
    :param port:                    The new port for the connection.
    :type port:                     string
    :param connection_username:     The new username for the connection.
    :type connection_username:      string
    :param connection_password:     The new password for the connection.
    :type connection_password:      string
    :param embed_password_flag:     Boolean; True to embed the password in the connection, False otherwise.
    :type embed_password_flag:      boolean
    """
    def __init__(self,
                 ts_connection,
                 server_address,
                 port,
                 connection_username,
                 connection_password,
                 embed_password_flag):
        super().__init__(ts_connection)
        self._server_address = server_address
        self._port = port
        self._connection_username = connection_username
        self._connection_password = connection_password
        self._embed_password_flag = embed_password_flag
        self.base_update_workbook_connection_request

    @property
    def required_parameter_keys(self):
        return [
            'serverAddress',
            'serverPort',
            'userName',
            'password',
            'embedPassword'
        ]

    @property
    def required_parameter_values(self):
        return [
            self._server_address,
            self._port,
            self._connection_username,
            self._connection_password,
            'true' if self._embed_password_flag is True else 'false' if self._embed_password_flag is False else None
        ]

    @property
    def base_update_workbook_connection_request(self):
        self._request_body.update({'connection': {}})
        return self._request_body

    @property
    def modified_update_workbook_connection_request(self):
        if any(self.required_parameter_values):
            self._request_body['connection'].update(
                self._get_parameters_dict(self.required_parameter_keys,
                                          self.required_parameter_values))
        return self._request_body

    def get_request(self):
        return self.modified_update_workbook_connection_request
