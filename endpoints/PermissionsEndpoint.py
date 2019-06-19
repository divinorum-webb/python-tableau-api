class PermissionsEndpoint(BaseEndpoint):
    """
    User endpoint for Tableau Server API requests.

    :param ts_connection:                       The Tableau Server connection object.
    :type ts_connection:                        class
    :param add_object_permissions:              Boolean flag; True if adding object permissions, False otherwise.
    :type add_object_permissions:               boolean
    :param query_object_permissions:            Boolean flag; True if querying object permissions, False otherwise.
    :type query_object_permissions:             boolean
    :param delete_object_permissions:           Boolean flag; True if deleting object permissions, False otherwise.
    :type delete_object_permissions:            boolean
    :param object_type:                         The Tableau object type (workbook, etc.).
    :type object_type:                          string
    :param object_id:                           The Tableau object ID.
    :type object_id:                            string
    :param query_default_project_permissions:   Boolean flag; True if querying default project permissions,
                                                False otherwise.
    :type query_default_project_permissions:    boolean
    :param project_permissions_object:          The project permissions object (workbook, etc.).
    :type project_permissions_object:           string
    :param project_id:                          The project ID.
    :type project_id:                           string
    :param parameter_dict:                      Dictionary of URL parameters to append. The value in each key-value pair
                                                is the literal text that will be appended to the URL endpoint.
    :type parameter_dict:                       dict
    """
    def __init__(self,
                 ts_connection,
                 add_object_permissions=False,
                 query_object_permissions=False,
                 delete_object_permissions=False,
                 object_type=None,
                 object_id=None,
                 query_default_project_permissions=False,
                 project_permissions_object=None,
                 project_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._add_object_permissions = add_object_permissions
        self._query_object_permissions = query_object_permissions
        self._delete_object_permissions = delete_object_permissions
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

    def get_endpoint(self):
        if self._add_object_permissions and not (self._query_object_permissions or self._delete_object_permissions):
            url = self.base_object_permissions_url
        elif self._query_object_permissions and not (self._add_object_permissions or self._delete_object_permissions):
            url = self.base_object_permissions_url
        elif self._delete_object_permissions and not (self._add_object_permissions or self._query_object_permissions):
            url = self.base_object_permissions_url
        elif self._query_default_project_permissions:
            url = self.base_query_default_permissions_url
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
