class FavoritesEndpoint(BaseEndpoint):
    """
    Favorites endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param add_to_favorites:
    :type add_to_favorites:
    :param delete_from_favorites:
    :type delete_from_favorites:
    :param object_type:
    :type object_type:
    :param object_id:
    :type object_id:
    :param get_user_favorites:
    :type get_user_favorites:
    :param user_id:
    :type user_id:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 add_to_favorites=False,
                 delete_from_favorites=False,
                 object_type=None,
                 object_id=None,
                 get_user_favorites=False,
                 user_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._add_to_favorites = add_to_favorites
        self._delete_from_favorites = delete_from_favorites
        self._object_type = object_type
        self._object_id = object_id
        self._get_user_favorites = get_user_favorites
        self._user_id = user_id
        self._parameter_dict = parameter_dict

    @property
    def base_favorites_url(self):
        return "{0}/api/{1}/sites/{2}/favorites".format(self._connection.server,
                                                        self._connection.api_version,
                                                        self._connection.site_id)

    @property
    def base_favorites_user_id_url(self):
        return "{0}/{1}".format(self.base_favorites_url,
                                self._user_id)

    @property
    def base_favorites_user_object_url(self):
        return "{0}/{1}s/{2}".format(self.base_favorites_user_id_url,
                                     self._object_type,
                                     self._object_id)

    def get_favorites_endpoint(self):
        if self._add_to_favorites and self._user_id:
            url = self.base_favorites_user_id_url
        elif self._delete_from_favorites and self._user_id:
            url = self.base_favorites_user_object_url
        elif self._get_user_favorites and self._user_id:
            url = self.base_favorites_user_id_url
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
