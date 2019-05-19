class UpdateProjectRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param project_name:
    :type project_name:
    :param project_description:
    :type project_description:
    :param content_permissions:
    :type content_permissions:
    :param parent_project_id:
    :type parent_project_id:
    """
    def __init__(self,
                 ts_connection,
                 project_name=None,
                 project_description=None,
                 content_permissions=None,
                 parent_project_id=None):
        super().__init__(ts_connection)
        self._project_name = project_name
        self._project_description = project_description
        self._content_permissions = content_permissions
        self._parent_project_id = parent_project_id
        self.base_create_project_request

    @property
    def optional_project_param_keys(self):
        return [
            'name',
            'parentProjectId',
            'description',
            'contentPermissions'
        ]

    @property
    def optional_project_param_values(self):
        return [
            self._project_name,
            self._parent_project_id,
            self._project_description,
            self._content_permissions
        ]

    @property
    def base_create_project_request(self):
        self._request_body.update({'project': {}})
        return self._request_body

    @property
    def modified_create_project_request(self):
        self._request_body['project'].update(
            self._get_parameters_dict(
                self.optional_project_param_keys,
                self.optional_project_param_values))
        return self._request_body

    def get_request(self):
        return self.modified_create_project_request
