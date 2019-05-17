class AddUserToAlertRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param user_id:
    :type user_id:
    """
    def __init__(self,
                 ts_connection,
                 user_id):
        super().__init__(ts_connection)
        self._user_id = user_id

    @property
    def base_add_user_request(self):
        self._request_body.update({'user': {'id': self._user_id}})
        return self._request_body

    def get_request(self):
        return self.base_add_user_request
