class SchedulesEndpoint(BaseEndpoint):
    """
    Schedules endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param schedule_id:
    :type schedule_id:
    :param create_schedule:
    :type create_schedule:
    :param query_schedules:
    :type query_schedules:
    :param update_schedule:
    :type update_schedule:
    :param delete_schedule:
    :type delete_schedule:
    :param add_datasource:
    :type add_datasource:
    :param add_workbook:
    :type add_workbook:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 schedule_id=None,
                 create_schedule=False,
                 query_schedules=False,
                 update_schedule=False,
                 delete_schedule=False,
                 add_datasource=False,
                 add_workbook=False,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._schedule_id = schedule_id
        self._create_schedule = create_schedule
        self._query_schedules = query_schedules
        self._update_schedule = update_schedule
        self._delete_schedule = delete_schedule
        self._add_datasource = add_datasource
        self._add_workbook = add_workbook
        self._parameter_dict = parameter_dict

    @property
    def base_schedule_url(self):
        return "{0}/api/{1}/schedules".format(self._connection.server,
                                              self._connection.api_version)

    @property
    def base_schedule_id_url(self):
        return "{0}/{1}".format(self.base_schedule_url,
                                self._schedule_id)

    @property
    def base_schedule_datasource_url(self):
        return "{0}/datasources".format(self.base_schedule_id_url)

    @property
    def base_schedule_workbook_url(self):
        return "{0}/workbooks".format(self.base_schedule_id_url)

    def get_schedule_endpoint(self):
        if self._schedule_id:
            if self._add_datasource and not self._add_workbook:
                url = self.base_schedule_datasource_url
            elif self._add_workbook and not self._add_datasource:
                url = self.base_schedule_workbook_url
            elif self._update_schedule or self._delete_schedule:
                url = self.base_schedule_id_url
            else:
                self._invalid_parameter_exception()
        else:
            url = self.base_schedule_url

        return self._append_url_parameters(url)
