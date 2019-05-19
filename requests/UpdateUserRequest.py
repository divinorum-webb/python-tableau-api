class UpdateUserRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param new_full_name:
    :type new_full_name:
    :param new_email:
    :type new_email:
    :param new_password:
    :type new_password:
    :param new_site_role:
    :type new_site_role:
    :param new_auth_setting:
    :type new_auth_setting:
    """
    def __init__(self,
                 ts_connection,
                 new_full_name=None,
                 new_email=None,
                 new_password=None,
                 new_site_role=None,
                 new_auth_setting=None):

        super().__init__(ts_connection)
        self._new_full_name = new_full_name
        self._new_email = new_email
        self._new_password = new_password
        self._new_site_role = new_site_role
        self._new_auth_setting = new_auth_setting
        self.base_update_user_request

    @property
    def optional_user_param_keys(self):
        return [
            'fullName',
            'email',
            'password',
            'siteRole',
            'authSetting'
        ]

    @property
    def optional_user_param_values(self):
        return [
            self._new_full_name,
            self._new_email,
            self._new_password,
            self._new_site_role,
            self._new_auth_setting
        ]

    @property
    def base_update_user_request(self):
        self._request_body.update({'user': {}})
        return self._request_body

    @property
    def modified_update_user_request(self):
        if any(self.optional_user_param_values):
            self._request_body['user'].update(
                self._get_parameters_dict(self.optional_user_param_keys,
                                          self.optional_user_param_values))
        return self._request_body

    def get_request(self):
        return self.modified_update_user_request
