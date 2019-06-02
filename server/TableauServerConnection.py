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
    def sign_out_headers(self):
        return sign_in_headers.copy().update({
            "X-Tableau-Auth": self.auth_token,
        })

    @property
    def auth_token(self):
        return self.__auth_token

    @auth_token.setter
    def auth_token(self, token_value):
        if not self.__auth_token or token_value is None:
            self.__auth_token = token_value
        else:
            raise Exception('You are already signed in with a valid auth token.')

    @property
    def site_id(self):
        return self.__site_id

    @site_id.setter
    def site_id(self, site_id_value):
        if not self.__site_id or site_id_value is None:
            self.__site_id = site_id_value
        else:
            raise Exception(
                'This Tableau Server connection is already connected to a specific site. Log out to reconnect.')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id_value):
        self.__user_id = user_id_value

    @verify_response(200)
    def sign_in(self):
        request = SignInRequest(ts_connection=self, username=self.username, password=self.password).get_request()
        endpoint = AuthEndpoint(ts_connection=self, sign_in=True).get_endpoint()
        response = requests.post(url=endpoint, json=request, headers=self.sign_in_headers)
        self.auth_token = response.json()['credentials']['token']
        self.site_id = response.json()['credentials']['site']['id']
        self.user_id = response.json()['credentials']['user']['id']

    @verify_signed_in
    @verify_response(200)
    def sign_out(self):
        endpoint = AuthEndpoint(ts_connection=self, sign_out=True).get_endpoint()
        response = requests.post(url=sign_out_endpoint, headers=default_headers)
        self.auth_token = None
        self.site_id = None
        self.user_id = None
