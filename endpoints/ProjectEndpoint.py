class ProjectEndpoint(BaseEndpoint):
    """
    Projects endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param create_project:             
    :type create_project:              
    :param query_projects:            
    :type query_projects:             
    :param update_project:         
    :type update_project:          
    :param delete_project:     
    :type delete_project:      
    :param project_id:     
    :type project_id:      
    :param parameter_dict:      
    :type parameter_dict:       
    """
    def __init__(self, 
                 ts_connection, 
                 query_projects=False,
                 update_project=False,
                 delete_project=False,
                 project_id=None, 
                 parameter_dict=None):
        
        super().__init__(ts_connection)
        self._query_projects = query_projects
        self._update_project = update_project
        self._delete_project = delete_project
        self._project_id = project_id
        self._parameter_dict = parameter_dict
        
    @property
    def base_project_url(self):
        return "{0}/api/{1}/sites/{2}/projects".format(self._connection.server, 
                                                       self._connection.api_version, 
                                                       self._connection.site_id)
    
    @property
    def base_project_id_url(self):
        return "{0}/{1}".format(self.base_project_url, 
                                self._project_id)
        
    def get_endpoint(self):
        if self._project_id:
            url = self.base_project_id_url
        else:
            url = self.base_project_url
        if url:
            return self._append_url_parameters(url)
        else:
            self._invalid_parameter_exception()
