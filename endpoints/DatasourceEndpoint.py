class DatasourceEndpoint(BaseEndpoint):
    """
    Datasource endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param query_datasources:
    :type query_datasources:
    :param query_datasource:
    :type query_datasource:
    :param datasource_id:
    :type datasource_id:
    :param query_datasource_connections:
    :type query_datasource_connections:
    :param connection_id:
    :type connection_id:
    :param add_tags:
    :type add_tags:
    :param delete_tag:
    :type delete_tag:
    :param refresh_datasource:
    :type refresh_datasource:
    :param update_datasource_connection:
    :type update_datasource_connection:
    :type tag_name:
    :param tag_name:
    :type download_datasource:
    :param download_datasource:
    :type get_datasource_revisions:
    :param get_datasource_revisions:
    :type download_datasource_revision:
    :param download_datasource_revision:
    :type remove_datasource_revision:
    :param remove_datasource_revision:
    :type revision_number:
    :param revision_number:
    :type parameter_dict:
    :param parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 query_datasources=False,
                 query_datasource=False,
                 datasource_id=None,
                 query_datasource_connections=False,
                 connection_id=None,
                 add_tags=False,
                 delete_tag=False,
                 refresh_datasource=False,
                 update_datasource_connection=False,
                 tag_name=None,
                 download_datasource=False,
                 get_datasource_revisions=False,
                 download_datasource_revision=False,
                 remove_datasource_revision=False,
                 revision_number=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._datasource_id = datasource_id
        self._connection_id = connection_id
        self._add_tags = add_tags
        self._delete_tag = delete_tag
        self._refresh_datasource = refresh_datasource
        self._update_datasource_connection = update_datasource_connection
        self._tag_name = tag_name
        self._query_datasource = query_datasource
        self._query_datasources = query_datasources
        self._query_datasource_connections = query_datasource_connections
        self._download_datasource = download_datasource
        self._get_datasource_revisions = get_datasource_revisions
        self._download_datasource_revision = download_datasource_revision
        self._remove_datasource_revision = remove_datasource_revision
        self._revision_number = revision_number
        self._parameter_dict = parameter_dict

    @property
    def base_datasource_url(self):
        return "{0}/api/{1}/sites/{2}/datasources".format(self._connection.server,
                                                          self._connection.api_version,
                                                          self._connection.site_id)

    @property
    def base_datasource_id_url(self):
        return "{0}/{1}".format(self.base_datasource_url,
                                self._datasource_id)

    @property
    def base_datasource_tags_url(self):
        return "{0}/tags".format(self.base_datasource_id_url)

    @property
    def base_delete_datasource_tag_url(self):
        return "{0}/{1}".format(self.base_datasource_tags_url,
                                self._tag_name)

    @property
    def base_datasource_connections_url(self):
        return "{0}/connections".format(self.base_datasource_id_url)

    @property
    def base_datasource_revisions_url(self):
        return "{0}/revisions".format(self.base_datasource_id_url)

    @property
    def base_datasource_revision_number_url(self):
        return "{0}/{1}".format(self.base_datasource_revisions_url,
                                self._revision_number)

    @property
    def base_download_datasource_url(self):
        return "{0}/content".format(self.base_datasource_id_url)

    @property
    def base_download_datasource_revision_url(self):
        return "{0}/content".format(self.base_datasource_revision_number_url,
                                    self._revision_number)

    @property
    def base_datasource_connection_id_url(self):
        return "{0}/{1}".format(self.base_datasource_connections_url,
                                self._connection_id)

    @property
    def base_refresh_datasource_url(self):
        return "{0}/refresh".format(self.base_datasource_id_url)

    def get_datasource_endpoint(self):
        if self._datasource_id:
            if self._query_datasource:
                url = self.base_datasource_id_url
            elif self._add_tags:
                url = self.base_datasource_tags_url
            elif self._delete_tag and self._tag_name:
                url = self.base_delete_datasource_tag_url
            elif self._query_datasource_connections:
                url = self.base_datasource_connections_url
            elif self._get_datasource_revisions:
                url = self.base_datasource_revisions_url
            elif self._remove_datasource_revision and self._revision_number:
                url = self.base_datasource_revision_number_url
            elif self._download_datasource:
                url = self.base_download_datasource_url
            elif self._download_datasource_revision:
                url = self.base_download_datasource_revision_url
            elif self._refresh_datasource:
                url = self.base_refresh_datasource_url
            elif self._update_datasource_connection:
                url = self.base_datsource_connection_id_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_datasource_url

        return self._append_url_parameters(url)
