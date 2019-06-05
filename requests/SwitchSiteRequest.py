class SwitchSiteRequest(BaseRequest):
    """
    Switch site request for generating API requests to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    """
    def __init__(self,
                 ts_connection,
                 site_name):

        super().__init__(ts_connection)
        self._site_name = site_name

    @property
    def base_switch_site_request(self):
        self._request_body.update({
            'site': {
                'contentUrl': self._site_name
            }
        })
        return self._request_body

    def get_request(self):
        return self.base_switch_site_request
