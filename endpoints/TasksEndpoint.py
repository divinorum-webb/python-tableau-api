class TasksEndpoint(BaseEndpoint):
    """
    Tasks endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param get_refresh_tasks:
    :type get_refresh_tasks:
    :param get_refresh_task:
    :type get_refresh_task:
    :param run_refresh_task:
    :type run_refresh_task:
    :param task_id:
    :type task_id:
    :param query_schedule_refresh_tasks:
    :type query_schedule_refresh_tasks:
    :param schedule_id:
    :type schedule_id:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 get_refresh_tasks=False,
                 get_refresh_task=False,
                 run_refresh_task=False,
                 task_id=None,
                 query_schedule_refresh_tasks=False,
                 schedule_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._get_refresh_tasks = get_refresh_tasks
        self._get_refresh_task = get_refresh_task
        self._run_refresh_task = run_refresh_task
        self._task_id = task_id
        self._query_schedule_refresh_tasks = query_schedule_refresh_tasks
        self._schedule_id = schedule_id
        self._parameter_dict = parameter_dict

    @property
    def base_task_url(self):
        return "{0}/api/{1}/sites/{2}/tasks".format(self._connection.server,
                                                    self._connection.api_version,
                                                    self._connection.site_id)

    @property
    def base_schedules_url(self):
        return "{0}/api/{1}/sites/{2}/schedules".format(self._connection.server,
                                                        self._connection.api_version,
                                                        self._connection.site_id)

    @property
    def base_extract_refresh_url(self):
        return "{0}/extractRefreshes".format(self.base_task_url)

    @property
    def base_extract_refresh_id_url(self):
        if self._run_refresh_task:
            return "{0}/{1}/runNow".format(self.base_extract_refresh_url,
                                           self._task_id)
        else:
            return "{0}/{1}".format(self.base_extract_refresh_url,
                                    self._task_id)

    @property
    def base_query_extract_refresh_url(self):
        return "{0}/{1}/extracts".format(self.base_schedules_url,
                                         self._schedule_id)

    def get_task_endpoint(self):
        if self._get_refresh_tasks:
            url = self.base_extract_refresh_url
        elif self._get_refresh_task or self._run_refresh_task:
            url = self.base_extract_refresh_id_url
        elif self._query_schedule_refresh_tasks:
            url = self.base_query_extract_refresh_url
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
