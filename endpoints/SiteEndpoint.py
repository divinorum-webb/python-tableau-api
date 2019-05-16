class SiteEndpoint(BaseEndpoint):
    """
    Site endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param site_id:             
    :type site_id:              
    :param create_site:         
    :type create_site:          
    :param update_site:         
    :type update_site:          
    :param delete_site:         
    :type delete_site:          
    :param query_site:          
    :type query_site:           
    :param get_users:           
    :type get_users:            
    :param get_groups:          
    :type get_groups:           
    :param add_user:            
    :type add_user:             
    :param add_group:           
    :type add_group:            
    :param remove_user:         
    :type remove_user:          
    :param remove_group:        
    :type remove_group:         
    :param user_id:             
    :type user_id:              
    :param group_id:            
    :type group_id:             
    :param parameter_dict:      
    :type parameter_dict:       
    """
    def __init__(self, 
                 ts_connection, 
                 site_id=None,
                 create_site=False,
                 update_site=False,
                 delete_site=False,
                 query_site=False,
                 query_views=False,
                 get_users=False,
                 get_groups=False,
                 add_user=False,
                 add_group=False,
                 remove_user=False,
                 remove_group=False,
                 user_id=None,
                 group_id=None,
                 parameter_dict=None):
        
        super().__init__(ts_connection)
        self._site_id = site_id
        self._create_site = create_site
        self._update_site = update_site
        self._delete_site = delete_site
        self._query_site = query_site
        self._query_views = query_views
        self._get_users = get_users
        self._get_groups = get_groups
        self._add_user = add_user
        self._add_group = add_group
        self._remove_user = remove_user
        self._remove_group = remove_group
        self._user_id = user_id
        self._group_id = group_id
        self._parameter_dict = parameter_dict
        
    @property
    def base_site_url(self):
        return "{0}/api/{1}/sites".format(self._connection.server, 
                                          self._connection.api_version)
    
    @property
    def base_site_id_url(self):
        return "{0}/{1}".format(self.base_site_url, 
                                self._site_id)
    
    @property
    def base_site_views_url(self):
        return "{0}/views".format(self.base_site_id_url)
    
    @property
    def base_site_user_url(self):
        return "{0}/users".format(self.base_site_id_url)
    
    @property
    def base_site_user_id_url(self):
        return "{0}/{1}".format(self.base_site_user_url,
                                self._user_id)
    
    @property
    def base_site_group_url(self):
        return "{0}/groups".format(self.base_site_id_url)
    
    @property
    def base_site_group_id_url(self):
        return "{0}/{1}".format(self.base_site_group_url,
                                self._group_id)
    
    def get_endpoint(self):
        if self._site_id or self._user_id or self._group_id:
            if self._update_site and not self._delete_site:
                url = self.base_site_id_url
            elif self._delete_site and not self._update_site:
                url = self.base_site_id_url
            elif self._get_users and not self._add_user:
                url = self.base_site_user_url
            elif self._add_user and not self._get_users:
                url = self.base_site_user_url
            elif self._get_groups and not self._add_group:
                url = self.base_site_group_url
            elif self._add_group and not self._get_groups:
                url = self.base_site_group_url
            elif self._remove_user and self._user_id and self._site_id:
                url = self.base_site_user_id_url
            elif self._remove_group and self._group_id and self._site_id:
                url = self.base_site_group_id_url
            elif self._query_site:
                url = self.base_site_id_url
            elif self._query_views:
                url = self.base_site_views_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_site_url

        return self._append_url_parameters(url)
