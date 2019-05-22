class UserEndpoint(BaseEndpoint):
    """
    User endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param query_user:          Boolean flag; True if querying a specific user, False otherwise.
    :type query_user:           boolean
    :param user_id:             The user ID.
    :type user_id:              string
    :param update_user:         Boolean flag; True if updating a specific user, False otherwise.
    :type update_user:          boolean
    :param parameter_dict:      Dictionary of URL parameters to append. The value in each key-value pair
                                is the literal text that will be appended to the URL endpoint.
    :type parameter_dict:       dict
    """
    def __init__(self,
                 ts_connection,
                 query_user=False,
                 user_id=None,
                 update_user=False,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._query_user = query_user
        self._user_id = user_id
        self._update_user = update_user
        self._parameter_dict = parameter_dict

    @property
    def base_user_url(self):
        return "{0}/api/{1}/sites/{2}/users".format(self._connection.server,
                                                    self._connection.api_version,
                                                    self._connection.site_id)

    @property
    def base_user_id_url(self):
        return "{0}/{1}".format(self.base_user_url,
                                self._user_id)

    def get_endpoint(self):
        if self._user_id:
            if self._query_user and not self._update_user:
                url = self.base_user_id_url
            elif self._update_user and not self._query_user:
                url = self.base_user_id_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_user_url

        return self._append_url_parameters(url)
