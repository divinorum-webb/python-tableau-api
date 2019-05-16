class DataAlertEndpoint(BaseEndpoint):
    """
    Data Alert endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param data_alert_id:             
    :type data_alert_id:              
    :param user_id:            
    :type user_id:             
    :param add_user:         
    :type add_user:          
    :param remove_user:     
    :type remove_user:      
    :param parameter_dict:      
    :type parameter_dict:       
    """
    def __init__(self, 
                 ts_connection, 
                 data_alert_id=None, 
                 user_id=None, 
                 add_user=False, 
                 remove_user=False,
                 parameter_dict=None):
        
        super().__init__(ts_connection)
        self._data_alert_id = data_alert_id
        self._user_id = user_id
        self._add_user = add_user
        self._remove_user = remove_user
        self._parameter_dict = parameter_dict
        
    @property
    def base_data_alert_url(self):
        return "{0}/api/{1}/sites/{2}/dataAlerts".format(self._connection.server,
                                                         self._connection.api_version,
                                                         self._connection.site_id)
    
    @property
    def base_data_alert_id_url(self):
        return "{0}/{1}".format(self.base_data_alert_url, 
                                self._data_alert_id)
    
    @property
    def base_data_alert_user_url(self):
        return "{0}/users".format(self.base_data_alert_id_url)
    
    @property
    def base_data_alert_user_id_url(self):
        return "{0}/{1}".format(self.base_data_alert_user_url, 
                                self._user_id)
    
    def get_endpoint(self):
        if not (self._data_alert_id or self._user_id or self._add_user or self._remove_user):
            url = self.base_data_alert_url
        elif self._data_alert_id and not (self._user_id or self._add_user or self._remove_user):
            url = self.base_data_alert_id_url
        elif self._data_alert_id and self._add_user and not (self._user_id or self._remove_user):
            url = self.base_data_alert_user_url
        elif self._data_alert_id and self._remove_user and self._user_id and not self._add_user:
            url = self.base_data_alert_user_id_url
        else:
            self._invalid_parameter_exception()
            
        return self._append_url_parameters(url)
