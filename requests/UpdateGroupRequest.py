class UpdateGroupRequest(BaseRequest):
    """
    Update group request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param new_group_name:
    :type new_group_name:
    :param active_directory_group_name:
    :type active_directory_group_name:
    :param active_directory_domain:
    :type active_directory_domain:
    :param site_role:
    :type site_role:
    """
    def __init__(self,
                 ts_connection,
                 new_group_name,
                 active_directory_group_name=None,
                 active_directory_domain=None,
                 site_role=None):
        super().__init__(ts_connection)
        self._new_group_name = new_group_name
        self._active_directory_group_name = active_directory_group_name
        self._active_directory_domain = active_directory_domain
        self._site_role = site_role
        self.base_update_group_request

    @property
    def required_group_param_keys(self):
        return ['name']

    @property
    def optional_import_param_keys(self):
        return [
            'source',
            'domainName',
            'siteRole'
        ]

    @property
    def required_group_param_values(self):
        return [self._new_group_name]

    @property
    def optional_import_param_values(self):
        return [
            self._active_directory_group_name,
            self._active_directory_domain,
            self._site_role
        ]

    @property
    def base_update_group_request(self):
        self._request_body.update({'group': {}})
        self._request_body['group'].update(
            self._get_parameters_dict(self.required_group_param_keys,
                                      self.required_group_param_values))
        return self._request_body

    @property
    def modified_update_group_request(self):
        if any(self.optional_import_param_values):
            self._request_body['group'].update({'import': {}})
            self._request_body['group']['import'].update(
                self._get_parameters_dict(self.optional_import_param_keys,
                                          self.optional_import_param_values))
        return self._request_body

    def get_request(self):
        return self.modified_update_group_request
