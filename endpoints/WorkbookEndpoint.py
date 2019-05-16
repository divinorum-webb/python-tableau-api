class WorkbookEndpoint(BaseEndpoint):
    """
    Workbook endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param query_workbooks:
    :type query_workbooks:
    :param query_workbook:
    :type query_workbook:
    :param workbook_id:
    :type workbook_id:
    :param view_id:
    :type view_id:
    :param add_tags:
    :type add_tags:
    :param delete_tag:
    :type delete_tag:
    :param tag_name:
    :type tag_name:
    :param query_views:
    :type query_views:
    :param query_connections:
    :type query_connections:
    :param query_workbook_preview_img:
    :type query_workbook_preview_img:
    :param get_workbook_revisions:
    :type get_workbook_revisions:
    :param trigger_refresh:
    :type trigger_refresh:
    :param parameter_dict:
    :type parameter_dict:
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
    def base_workbook_refresh_url(self):
        return "{0}/refresh".format(self.base_workbook_id_url)

    def get_endpoint(self):
        if self._workbook_id:
            if self._query_workbook:
                url = self.base_workbook_id_url
            elif self._add_tags:
                url = self.base_workbook_tags_url
            elif self._delete_tags:
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
            elif self._trigger_refresh:
                url = self.base_workbook_refresh_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_workbook_url

        return self._append_url_parameters(url)
