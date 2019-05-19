class AddUserToSiteRequest(BaseRequest):
    """
    Add user to site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param user_name:
    :type user_name:
    :param site_role:
    :type site_role:
    :param auth_setting:
    :type auth_setting:
    """
    def __init__(self,
                 ts_connection,
                 user_name,
                 site_role,
                 auth_setting=None):
        super().__init__(ts_connection)
        self._user_name = user_name
        self._site_role = site_role
        self._auth_setting = auth_setting
        self.base_add_user_request

    @property
    def required_user_param_keys(self):
        return [
            'name',
            'siteRole'
        ]

    @property
    def optional_user_param_keys(self):
        return ['authSetting']

    @property
    def required_user_param_values(self):
        return [
            self._user_name,
            self._site_role
        ]

    @property
    def optional_user_param_values(self):
        return [self._auth_setting]

    @property
    def base_add_user_request(self):
        self._request_body.update({'user': {}})
        self._request_body['user'].update(
            self._get_parameters_dict(self.required_user_param_keys,
                                      self.required_user_param_values))
        return self._request_body

    @property
    def modified_add_user_request(self):
        if any(self.optional_user_param_values):
            self._request_body['user'].update(
                self._get_parameters_dict(self.optional_user_param_keys,
                                          self.optional_user_param_values))
        return self._request_body

    def get_request(self):
        return self.modified_add_user_request
