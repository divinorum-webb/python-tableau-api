class PermissionsEndpoint(BaseEndpoint):
    """
    User endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param add_object_permissions:
    :type add_object_permissions:
    :param query_object_permissions:
    :type query_object_permissions:
    :param object_type:
    :type object_type:
    :param object_id:
    :type object_id:
    :param query_default_project_permissions:
    :type query_default_project_permissions:
    :param project_permissions_object:
    :type project_permissions_object:
    :param project_id:
    :type project_id:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 add_object_permissions=False,
                 query_object_permissions=False,
                 object_type=None,
                 object_id=None,
                 query_default_project_permissions=False,
                 project_permissions_object=None,
                 project_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._add_object_permissions = add_object_permissions
        self._query_object_permissions = query_object_permissions
        self._object_type = object_type
        self._object_id = object_id
        self._query_default_project_permissions = query_default_project_permissions
        self._project_permissions_object = project_permissions_object
        self._project_id = project_id
        self._parameter_dict = parameter_dict

    @property
    def base_permissions_url(self):
        return "{0}/api/{1}/sites/{2}".format(self._connection.server,
                                              self._connection.api_version,
                                              self._connection.site_id)

    @property
    def base_object_permissions_url(self):
        return "{0}/{1}s/{2}/permissions".format(self.base_permissions_url,
                                                 self._object_type,
                                                 self._object_id)

    @property
    def base_query_default_permissions_url(self):
        return "{0}/projects/{1}/default-permissions/{2}".format(self.base_permissions_url,
                                                                 self._project_id,
                                                                 self._project_permissions_object)

    def get_permissions_endpoint(self):
        if self._add_object_permissions and not self._query_object_permissions:
            url = self.base_object_permissions_url
        elif self._query_object_permissions and not self._add_object_permissions:
            url = self.base_object_permissions_url
        elif self._query_default_project_permissions:
            url = self.base_query_default_permissions_url
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
