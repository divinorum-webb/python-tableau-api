class TableauServerConnection:
    def __init__(self,
                 config_json,
                 env='tableau_prod'):
        """
        Used to create a Tableau Server connection.
        The config_json parameter requires a valid config file describing the Tableau Server configurations.
        The env parameter is a string that indicates which environment to reference from the config file.

        :param config_json:     The configuration object. This should be a dict / JSON object that defines the
                                Tableau Server configuration.
        :type config_json:      JSON or dict
        :param env:             The environment from the configuration file to use. Defaults to 'tableau_prod'.
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
                                                 query_data_alerts=True).get_endpoint()
        self.active_headers = self.default_headers
        response = requests.get(url=self.active_endpoint, headers=self.active_headers)
        return response
