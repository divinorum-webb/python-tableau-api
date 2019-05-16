class GroupEndpoint(BaseEndpoint):
    """
    Group endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param query_groups:
    :type query_groups:
    :param group_id:
    :type group_id:
    :param update_group:
    :type update_group:
    :param get_users:
    :type get_users:
    :param add_user:
    :type add_user:
    :param remove_user:
    :type remove_user:
    :param user_id:
    :type user_id:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 query_groups=False,
                 group_id=None,
                 update_group=False,
                 get_users=False,
                 add_user=False,
                 remove_user=False,
                 user_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._query_groups = query_groups
        self._group_id = group_id
        self._update_group = update_group
        self._get_users = get_users
        self._add_user = add_user
        self._remove_user = remove_user
        self._user_id = user_id
        self._parameter_dict = parameter_dict

    @property
    def base_group_url(self):
        return "{0}/api/{1}/sites/{2}/groups".format(self._connection.server,
                                                     self._connection.api_version,
                                                     self._connection.site_id)

    @property
    def base_group_id_url(self):
        return "{0}/{1}".format(self.base_group_url, self._group_id)

    @property
    def base_group_user_url(self):
        return "{0}/users".format(self.base_group_id_url)

    @property
    def base_group_user_id_url(self):
        return "{0}/{1}".format(self.base_group_user_url,
                                self._user_id)

    def get_endpoint(self):
        if self._group_id:
            if self._update_group:
                url = self.base_group_id_url
            elif self._get_users or self._add_user:
                url = self.base_group_user_url
            elif self._remove_user and self._user_id:
                url = self.base_group_user_id_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_group_url

        return self._append_url_parameters(url)
