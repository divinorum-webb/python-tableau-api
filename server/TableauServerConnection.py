class TableauServerConnection:
    def __init__(self,
                 config_json,
                 env='tableau_prod'):
        """
        Initialize the TableauServer object.
        The config_json parameter requires a valid config file.
        The env parameter is a string that indicates which environment to reference from the config file.
        :param config_json:     The configuration object. This should be a dict / JSON object that defines the
                                Tableau Server configuration.
        :type config_json:      JSON or dict
        :param env:             The environment from the configuration file to use.
        :type env:              string
        """
        self._config = config_json
        self._env = env
        self.__auth_token = None
        self.__site_id = None
        self.__user_id = None
        self.active_endpoint = None
        self.active_request = None
        self.active_headers = None

    @property
    def server(self):
        return self._config[self._env]['server']

    @property
    def api_version(self):
        return self._config[self._env]['api_version']

    @property
    def username(self):
        return self._config[self._env]['username']

    @property
    def password(self):
        return self._config[self._env]['password']

    @property
    def site_name(self):
        return self._config[self._env]['site_name']

    @property
    def site_url(self):
        return self._config[self._env]['site_url']

    @property
    def sign_in_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @property
    def x_auth_header(self):
        return {
            "X-Tableau-Auth": self.auth_token
        }

    @property
    def default_headers(self):
        headers = self.sign_in_headers.copy()
        headers.update({"X-Tableau-Auth": self.auth_token})
        return headers

    @property
    def auth_token(self):
        return self.__auth_token

    @auth_token.setter
    def auth_token(self, token_value):
        if token_value != self.__auth_token or token_value is None:
            self.__auth_token = token_value
        else:
            raise Exception('You are already signed in with a valid auth token.')

    @property
    def site_id(self):
        return self.__site_id

    @site_id.setter
    def site_id(self, site_id_value):
        if self.site_id != site_id_value:
            self.__site_id = site_id_value
        else:
            raise Exception('This Tableau Server connection is already connected the specified site.')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id_value):
        self.__user_id = user_id_value

    #     @verify_response(200)
    def sign_in(self):
        request = SignInRequest(ts_connection=self, username=self.username, password=self.password).get_request()
        endpoint = AuthEndpoint(ts_connection=self, sign_in=True).get_endpoint()
        response = requests.post(url=endpoint, json=request, headers=self.sign_in_headers)
        if response.status_code == 200:
            self.auth_token = response.json()['credentials']['token']
            self.site_id = response.json()['credentials']['site']['id']
            self.user_id = response.json()['credentials']['user']['id']

    @verify_signed_in
    #     @verify_response(200)
    def sign_out(self):
        endpoint = AuthEndpoint(ts_connection=self, sign_out=True).get_endpoint()
        response = requests.post(url=endpoint, headers=self.x_auth_header)
        if response.status_code == 204:
            self.auth_token = None
            self.site_id = None
            self.user_id = None
        return response

    @verify_signed_in
    #     @verify_response(200)
    def switch_site(self, site_name):
        self.active_request = SwitchSiteRequest(ts_connection=self, site_name=site_name).get_request()
        self.active_endpoint = AuthEndpoint(ts_connection=self, switch_site=True).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.post(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        if response.status_code == 200:
            self.auth_token = response.json()['credentials']['token']
            self.site_id = response.json()['credentials']['site']['id']
            self.user_id = response.json()['credentials']['user']['id']
        return response

    def create_site(self):
        # This method can only be called by server administrators.
        print("This method can only be called by server administrators.")
        pass

    def query_site(self, parameter_dict=None):
        self.active_endpoint = SiteEndpoint(ts_connection=self,
                                            query_site=True,
                                            site_id=self.site_id,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_sites(self, parameter_dict=None):
        self.active_endpoint = SiteEndpoint(ts_connection=self,
                                            query_sites=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_views_for_site(self, parameter_dict=None):
        self.active_endpoint = SiteEndpoint(ts_connection=self,
                                            query_views=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def update_site(self):
        # This method can only be called by server administrators.
        print("This method can only be called by server administrators.")
        pass

    def delete_site(self):
        # This method can only be called by server administrators.
        print("This method can only be called by server administrators.")
        pass

    def delete_data_driven_alert(self, data_alert_id):
        self.active_endpoint = DataAlertEndpoint(ts_connection=self,
                                                 data_alert_id=data_alert_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.delete(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_data_driven_alert_details(self, data_alert_id):
        self.active_endpoint = DataAlertEndpoint(ts_connection=self,
                                                 query_data_alert=True,
                                                 data_alert_id=data_alert_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_data_driven_alerts(self, parameter_dict=None):
        self.active_endpoint = DataAlertEndpoint(ts_connection=self,
                                                 query_data_alerts=True,
                                                 parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def add_user_to_data_driven_alert(self, user_id, data_alert_id):
        # this appears to be broken on Tableau's side, always returning an internal server error
        self.active_request = AddUserToAlertRequest(ts_connection=self, user_id=user_id).get_request()
        self.active_endpoint = DataAlertEndpoint(ts_connection=self, add_user=True, user_id=user_id,
                                                 data_alert_id=data_alert_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.post(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        return response

    def delete_user_from_data_driven_alert(self, user_id, data_alert_id):
        self.active_endpoint = DataAlertEndpoint(ts_connection=self, remove_user=True, user_id=user_id,
                                                 data_alert_id=data_alert_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.delete(url=self.active_endpoint, headers=self.active_headers)
        return response

    def update_data_driven_alert(self, data_alert_id, subject=None, frequency=None, alert_owner_id=None,
                                 is_public_flag=None):
        self.active_request = UpdateDataAlertRequest(ts_connection=self, subject=subject, frequency=frequency,
                                                     alert_owner_id=alert_owner_id,
                                                     is_public_flag=is_public_flag).get_request()
        self.active_endpoint = DataAlertEndpoint(ts_connection=self, data_alert_id=data_alert_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.put(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        return response

    # Add flow functions here eventually

    def create_project(self, project_name, project_description=None, content_permissions='ManagedByOwner',
                       parent_project_id=None, parameter_dict=None):
        self.active_request = CreateProjectRequest(ts_connection=self, project_name=project_name,
                                                   project_description=project_description,
                                                   content_permissions=content_permissions,
                                                   parent_project_id=parent_project_id).get_request()
        self.active_endpoint = ProjectEndpoint(ts_connection=self, create_project=True,
                                               parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.post(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        return response

    def query_projects(self, parameter_dict=None):
        self.active_endpoint = ProjectEndpoint(ts_connection=self, query_projects=True,
                                               parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def update_project(self, project_id, project_name=None, project_description=None, content_permissions=None,
                       parent_project_id=None):
        self.active_request = UpdateProjectRequest(ts_connection=self, project_name=project_name,
                                                   project_description=project_description,
                                                   content_permissions=content_permissions,
                                                   parent_project_id=parent_project_id).get_request()
        self.active_endpoint = ProjectEndpoint(ts_connection=self, update_project=True,
                                               project_id=project_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.put(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        return response

    def delete_project(self, project_id):
        self.active_endpoint = ProjectEndpoint(ts_connection=self, project_id=project_id).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.delete(url=self.active_endpoint, headers=self.active_headers)
        return response

    def publish_workbook(self, workbook_file_path, workbook_name, project_id, show_tabs_flag=False,
                         user_id=None, server_address=None, port_number=None, connection_username=None,
                         connection_password=None,
                         embed_credentials_flag=False, oauth_flag=False, workbook_views_to_hide=None,
                         hide_view_flag=False, parameter_dict={}):
        self.active_request = PublishWorkbookRequest(ts_connection=self, workbook_name=workbook_name,
                                                     project_id=project_id,
                                                     show_tabs_flag=show_tabs_flag, user_id=user_id,
                                                     server_address=server_address,
                                                     port_number=port_number, connection_username=connection_username,
                                                     connection_password=connection_password,
                                                     embed_credentials_flag=embed_credentials_flag,
                                                     oauth_flag=oauth_flag,
                                                     workbook_views_to_hide=workbook_views_to_hide,
                                                     hide_view_flag=hide_view_flag)
        payload, content_type, workbook_type = self.active_request._make_multipart(workbook_file_path)
        parameter_dict.update({'workbookType': 'workbookType={}'.format(workbook_type)})
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, publish_workbook=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.active_request.get_headers(content_type)
        response = requests.post(url=self.active_endpoint, data=payload, headers=self.active_headers)
        return response

    def add_tags_to_view(self):
        pass

    def add_tags_to_workbook(self):
        pass

    def query_views_for_site(self, parameter_dict=None):
        self.active_endpoint = ViewEndpoint(ts_connection=self, query_views=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_views_for_workbook(self, workbook_id, parameter_dict=None):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, query_views=True, workbook_id=workbook_id,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_view_data(self, view_id, parameter_dict=None):
        # the CSV returned is in the response body as response.content
        self.active_endpoint = ViewEndpoint(ts_connection=self, view_id=view_id, query_view_data=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_view_image(self, view_id, parameter_dict=None):
        # the image returned is in the response body as response.content
        self.active_endpoint = ViewEndpoint(ts_connection=self, view_id=view_id, query_view_image=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_view_pdf(self, view_id, parameter_dict=None):
        # the PDF returned is in the response body as response.content
        self.active_endpoint = ViewEndpoint(ts_connection=self, view_id=view_id, query_view_pdf=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_view_preview_image(self, workbook_id, view_id, parameter_dict=None):
        # the preview thumbnail image returned is in the response body as response.content
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id, view_id=view_id,
                                                query_workbook_view_preview_img=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_workbook(self, workbook_id, parameter_dict=None):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id, query_workbook=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_workbook_connections(self, workbook_id, parameter_dict=None):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id, query_connections=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def get_workbook_revisions(self, workbook_id, parameter_dict=None):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id,
                                                get_workbook_revisions=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_workbook_preview_image(self, workbook_id, parameter_dict=None):
        # the preview image returned is in the response body as response.content
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id,
                                                query_workbook_preview_img=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_workbooks_for_site(self, parameter_dict=None):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, query_workbooks=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def query_workbooks_for_user(self, user_id, parameter_dict=None):
        self.active_endpoint = UserEndpoint(ts_connection=self, user_id=user_id, query_workbooks_for_user=True,
                                            parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def download_workbook(self, workbook_id, parameter_dict=None):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id, download_workbook=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def download_workbook_revision(self, workbook_id, revision_number, parameter_dict=None):
        # this method only works for workbook versions that are NOT the current version
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id,
                                                revision_number=revision_number,
                                                download_workbook_revision=True,
                                                parameter_dict=parameter_dict).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response

    def update_workbook(self, workbook_id, show_tabs_flag=None, project_id=None, owner_id=None):
        self.active_request = UpdateWorkbookRequest(ts_connection=self, show_tabs_flag=show_tabs_flag,
                                                    project_id=project_id, owner_id=owner_id).get_request()
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id,
                                                update_workbook=True).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.put(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        return response

    def update_workbook_connection(self):
        pass

    def update_workbook_now(self, workbook_id):
        self.active_request = EmptyRequest(ts_connection=self).get_request()
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id,
                                                refresh_workbook=True).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.post(url=self.active_endpoint, json=self.active_request, headers=self.active_headers)
        return response

    def delete_workbook(self, workbook_id):
        self.active_endpoint = WorkbookEndpoint(ts_connection=self, workbook_id=workbook_id,
                                                delete_workbook=True).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.delete(url=self.active_endpoint, headers=self.active_headers)
        return response

    def delete_tag_from_view(self):
        pass

    def delete_tag_from_workbook(self):
        pass
