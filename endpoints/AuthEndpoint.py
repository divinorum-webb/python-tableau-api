class AuthEndpoint(BaseEndpoint):
    """
    Authorization endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param sign_in:             
    :type sign_in:              
    :param sign_out:            
    :type sign_out:             
    :param switch_site:         
    :type switch_site:          
    :param get_server_info:     
    :type get_server_info:      
    :param parameter_dict:      
    :type parameter_dict:       
    """
    def __init__(self,
                 ts_connection,
                 sign_in=False,
                 sign_out=False,
                 switch_site=False,
                 get_server_info=False,
                 parameter_dict=None):
        
        super().__init__(ts_connection)
        self._sign_in = sign_in
        self._sign_out = sign_out
        self._switch_site = switch_site
        self._get_server_info = get_server_info
        self._parameter_dict = parameter_dict
        
    @property
    def base_auth_url(self):
        return "{0}/api/{1}/auth".format(self._connection.server, 
                                         self._connection.api_version)
    
    @property
    def base_sign_in_url(self):
        return "{0}/signin".format(self.base_auth_url)
    
    @property
    def base_sign_out_url(self):
        return "{0}/signout".format(self.base_auth_url)
    
    @property
    def base_switch_site_url(self):
        return "{0}/switchSite".format(self.base_auth_url)
    
    @property
    def base_server_info_url(self):
        return "{0}/api/{1}/serverinfo".format(self._connection.server,
                                               self._connection.api_version)
    
    def get_endpoint(self):
        if self._sign_in and not (self._sign_out or self._switch_site):
            url = self.base_sign_in_url
        elif self._sign_out and not (self._sign_in or self._switch_site):
            url = self.base_sign_out_url
        elif self._switch_site and not (self._sign_in or self._sign_out):
            url = self.base_switch_site_url
        elif self._get_server_info:
            url = self.base_server_info_url
        
        if url:
            return self._append_url_parameters(url)
        else:
            self._invalid_parameter_exception()   
