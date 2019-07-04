class TasksEndpoint(BaseEndpoint):
    """
    Tasks endpoint for Tableau Server API requests.

    :param ts_connection:                   The Tableau Server connection object.
    :type ts_connection:                    class
    :param get_refresh_tasks:               Boolean flag; True if getting all refresh tasks, False otherwise.
    :type get_refresh_tasks:                boolean
    :param get_refresh_task:                Boolean flag; True if getting a specific refresh task, False otherwise.
    :type get_refresh_task:                 boolean
    :param run_refresh_task:                Boolean flag; True if running a specific refresh task, False otherwise.
    :type run_refresh_task:                 boolean
    :param run_flow_task:                   Boolean flag; True if running a specific flow task, False otherwise.
    :type run_flow_task:                    boolean
    :param task_id:                         The task ID.
    :type task_id:                          string
    :param flow_id:                         The flow ID.
    :type flow_id:                          string
    :param query_schedule_refresh_tasks:    Boolean flag; True if querying all refresh tasks, False otherwise.
    :type query_schedule_refresh_tasks:     boolean
    :param schedule_id:                     The schedule ID.
    :type schedule_id:                      string
    :param parameter_dict:                  Dictionary of URL parameters to append. The value in each key-value pair
                                            is the literal text that will be appended to the URL endpoint.
    :type parameter_dict:                   dict
    """
    def __init__(self,
                 ts_connection,
                 get_refresh_tasks=False,
                 get_flow_run_tasks=False,
                 get_refresh_task=False,
                 get_flow_run_task=False,
                 run_refresh_task=False,
                 run_flow_task=False,
                 task_id=None,
                 flow_id=None,
                 query_schedule_refresh_tasks=False,
                 schedule_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._get_refresh_tasks = get_refresh_tasks
        self._get_flow_run_tasks = get_flow_run_tasks
        self._get_refresh_task = get_refresh_task
        self._get_flow_run_task = get_flow_run_task
        self._run_refresh_task = run_refresh_task
        self._run_flow_task = run_flow_task
        self._task_id = task_id
        self._flow_id = flow_id
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

    @property
    def base_flow_run_tasks_url(self):
        return "{0}/runFlow".format(self.base_task_url)

    @property
    def base_flow_run_task_id_url(self):
        if self._run_flow_task:
            return "{0}/{1}/runNow".format(self.base_flow_run_tasks_url,
                                           self._task_id)
        else:
            return "{0}/{1}".format(self.base_flow_run_tasks_url,
                                    self._task_id)

    def get_endpoint(self):
        if self._get_refresh_tasks:
            url = self.base_extract_refresh_url
        elif self._get_refresh_task or self._run_refresh_task:
            url = self.base_extract_refresh_id_url
        elif self._query_schedule_refresh_tasks:
            url = self.base_query_extract_refresh_url
        elif self._get_flow_run_tasks:
            url = self.base_flow_run_tasks_url
        elif self._get_flow_run_task:
            url = self.base_flow_run_task_id_url
        elif self._run_flow_task:
            url = self.base_flow_run_task_id_url
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
