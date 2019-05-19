class AddTagsRequest(BaseRequest):
    """
    Create site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param tags:
    :type tags:
    """
    def __init__(self,
                 ts_connection,
                 tags=[]):
        super().__init__(ts_connection)
        self._tags = tags
        self.base_add_tags_request

    @property
    def base_add_tags_request(self):
        self._request_body.update({'tags': {'tag': []}})
        return self._request_body

    @property
    def modified_add_tags_request(self):
        for tag in self._tags:
            self._request_body['tags']['tag'].append({
                'label': tag
            })
        return self._request_body

    def get_request(self):
        return self.modified_add_tags_request
