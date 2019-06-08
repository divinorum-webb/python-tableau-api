class WorkbookEndpoint(BaseEndpoint):
    """
    Workbook endpoint for Tableau Server API requests.

    :param ts_connection:                       The Tableau Server connection object.
    :type ts_connection:                        class
    :param query_workbooks:                     Boolean flag; True if querying all workbooks; False otherwise.
    :type query_workbooks:                      boolean
    :param query_workbook:                      Boolean flag; True if querying a specific workbook, False otherwise.
    :type query_workbook:                       boolean
    :param workbook_id:                         The workbook ID.
    :type workbook_id:                          string
    :param view_id:                             The view ID.
    :type view_id:                              string
    :param add_tags:                            Boolean flag; True if adding tags, False otherwise.
    :type add_tags:                             boolean
    :param delete_tag:                          Boolean flag; True if deleting a specific tag, False otherwise.
    :type delete_tag:                           boolean
    :param tag_name:                            The name of the tag.
    :type tag_name:                             string
    :param query_views:                         Boolean flag; True if querying all views, False otherwise.
    :type query_views:                          boolean
    :param query_connections:                   Boolean flag; True if querying all connections, False otherwise.
    :type query_connections:                    boolean
    :param query_workbook_preview_img:          Boolean flag; True if querying a specific preview image,
                                                False otherwise.
    :type query_workbook_preview_img:           boolean
    :param query_workbook_view_preview_img:     Boolean flag; True if querying a specific preview image,
                                                False otherwise.
    :type query_workbook_view_preview_img:      boolean
    :param get_workbook_revisions:              Boolean flag; True if getting all workbook revisions, False otherwise.
    :type get_workbook_revisions:               boolean
    :param trigger_refresh:                     Boolean flag; True if triggering a specific workbook refresh,
                                                False otherwise.
    :type trigger_refresh:                      boolean
    :param parameter_dict:                      Dictionary of URL parameters to append. The value in each key-value pair
                                                is the literal text that will be appended to the URL endpoint.
    :type parameter_dict:                       dict
    """
    def __init__(self,
                 ts_connection,
                 query_workbooks=False,
                 query_workbook=False,
                 workbook_id=None,
                 view_id=None,
                 add_tags=False,
                 delete_tag=False,
                 tag_name=None,
                 query_views=False,
                 query_connections=False,
                 query_workbook_preview_img=False,
                 query_workbook_view_preview_img=False,
                 get_workbook_revisions=False,
                 download_workbook=False,
                 trigger_refresh=False,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._query_workbooks = query_workbooks
        self._query_workbook = query_workbook
        self._workbook_id = workbook_id
        self._view_id = view_id
        self._add_tags = add_tags
        self._delete_tag = delete_tag
        self._tag_name = tag_name
        self._query_views = query_views
        self._query_connections = query_connections
        self._query_workbook_preview_img = query_workbook_preview_img
        self._query_workbook_view_preview_img = query_workbook_view_preview_img
        self._get_workbook_revisions = get_workbook_revisions
        self._download_workbook = download_workbook
        self._trigger_refresh = trigger_refresh
        self._parameter_dict = parameter_dict

    @property
    def base_workbook_url(self):
        return "{0}/api/{1}/sites/{2}/workbooks".format(self._connection.server,
                                                        self._connection.api_version,
                                                        self._connection.site_id)

    @property
    def base_workbook_id_url(self):
        return "{0}/{1}".format(self.base_workbook_url,
                                self._workbook_id)

    @property
    def base_workbook_tags_url(self):
        return "{0}/tags".format(self.base_workbook_id_url)

    @property
    def base_delete_workbook_tag_url(self):
        return "{0}/{1}".format(self.base_workbook_tags_url,
                                self._tag_name)

    @property
    def base_workbook_views_url(self):
        return "{0}/views".format(self.base_workbook_id_url)

    @property
    def base_workbook_connections_url(self):
        return "{0}/connections".format(self.base_workbook_id_url)

    @property
    def base_workbook_preview_url(self):
        return "{0}/previewImage".format(self.base_workbook_id_url)

    @property
    def base_workbook_view_preview_url(self):
        return "{0}/{1}/previewImage".format(self.base_workbook_views_url,
                                             self._view_id)

    @property
    def base_workbook_revisions_url(self):
        return "{0}/revisions".format(self.base_workbook_id_url)

    @property
    def base_workbook_content_url(self):
        return "{0}/content".format(self.base_workbook_id_url)

    @property
    def base_workbook_refresh_url(self):
        return "{0}/refresh".format(self.base_workbook_id_url)

    def get_endpoint(self):
        if self._workbook_id:
            if self._query_workbook:
                url = self.base_workbook_id_url
            elif self._add_tags:
                url = self.base_workbook_tags_url
            elif self._delete_tag:
                url = self.base_delete_workbook_tag_url
            elif self._query_views:
                url = self.base_workbook_views_url
            elif self._query_connections:
                url = self.base_workbook_connections_url
            elif self._query_workbook_preview_img:
                url = self.base_workbook_preview_url
            elif self._query_workbook_view_preview_img:
                url = self.base_workbook_view_preview_url
            elif self._get_workbook_revisions:
                url = self.base_workbook_revisions_url
            elif self._download_workbook:
                url = self.base_workbook_content_url
            elif self._trigger_refresh:
                url = self.base_workbook_refresh_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_workbook_url

        return self._append_url_parameters(url)
