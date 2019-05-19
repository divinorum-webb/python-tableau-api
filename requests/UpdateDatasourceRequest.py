class UpdateDatasourceRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param new_project_id:
    :type new_project_id:
    :param new_owner_id:
    :type new_owner_id:
    :param is_certified:
    :type is_certified:
    :param certification_note:
    :type certification_note:
    """
    def __init__(self,
                 ts_connection,
                 new_project_id=None,
                 new_owner_id=None,
                 is_certified=None,
                 certification_note=None):

        super().__init__(ts_connection)
        self._new_project_id = new_project_id
        self._new_owner_id = new_owner_id
        self._is_certified = is_certified
        self._certification_note = certification_note
        self.base_update_datasource_request

    @property
    def optional_datasource_param_keys(self):
        return [
            'isCertified',
            'certificationNote'
        ]

    @property
    def optional_project_param_keys(self):
        return ['id']

    @property
    def optional_owner_param_keys(self):
        return ['id']

    @property
    def optional_datasource_param_values(self):
        return [
            'true' if self._is_certified == True else 'false' if self._is_certified == False else None,
            self._certification_note
        ]

    @property
    def optional_project_param_values(self):
        return [self._new_project_id]

    @property
    def optional_owner_param_values(self):
        return [self._new_owner_id]

    @property
    def base_update_datasource_request(self):
        self._request_body.update({'datasource': {}})
        return self._request_body

    @property
    def modified_update_datasource_request(self):
        if any(self.optional_datasource_param_keys):
            self._request_body['datasource'].update(
                self._get_parameters_dict(self.optional_datasource_param_keys,
                                          self.optional_datasource_param_values))

        if any(self.optional_project_param_keys):
            self._request_body['datasource'].update({'project': {}})
            self._request_body['datasource']['project'].update(
                self._get_parameters_dict(self.optional_project_param_keys,
                                          self.optional_project_param_values))

        if any(self.optional_owner_param_keys):
            self._request_body['datasource'].update({'owner': {}})
            self._request_body['datasource']['owner'].update(
                self._get_parameters_dict(self.optional_owner_param_keys,
                                          self.optional_owner_param_values))

        return self._request_body

    def get_request(self):
        return self.modified_update_datasource_request
