class SwitchSiteRequest(BaseRequest):
    """
    Empty request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    """
    def __init__(self,
                 ts_connection):

        super().__init__(ts_connection)

    @property
    def base_switch_site_request(self):
        self._request_body.update({
            'site': {
                'contentUrl': self._connection.site_url
            }
        })
        return self._request_body

    def get_request(self):
        return self.base_switch_site_request
