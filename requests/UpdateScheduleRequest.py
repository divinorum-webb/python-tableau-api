class UpdateScheduleRequest(BaseRequest):
    """
    Update schedule request for API requests to Tableau Server.

    :param ts_connection:               The Tableau Server connection object.
    :type ts_connection:                class
    :param schedule_name:               The new name to give to the schedule.
    :type schedule_name:                string
    :param schedule_priority:           An integer value (entered here as a string) between 1 and 100 that determines
                                        the default priority of the schedule if multiple tasks are pending in the queue.
                                        Higher numbers have higher priority.
    :type schedule_priority:            string
    :param schedule_type:               This value (Extract or Subscription) indicates whether the schedule type is
                                        an extract or a subscription schedule.
    :type schedule_type:                string
    :param schedule_execution_order:    Parallel to allow jobs associated with this schedule to run at the same time,
                                        or Serial to require the jobs to run one after the other.
    :type schedule_execution_order:     string
    :param schedule_frequency:          The granularity of the schedule. Valid values are:
                                        Hourly, Daily, Weekly, Monthly.
    :type schedule_frequency:           string
    :param start_time:                  The time of day on which scheduled jobs should run (or if the frequency is
                                        hourly, on which they should start being run), in the format HH:MM:SS
                                        (for example, 18:30:00). This value is required for all schedule frequencies.
    :type start_time:                   string
    :param end_time:                    If the schedule frequency is Hourly, the time of day on which scheduled jobs
                                        should stop being run, in the format HH:MM:SS (for example, 23:30:00).
                                        Hourly jobs will occur at the specified intervals between the start time and
                                        the end time. For other schedule frequencies, this value is not required and
                                        if the attribute is included, it is ignored.
    :type end_time:                     string
    :param interval_expression:         See the Tableau Server REST API documentation for details of this parameter.
    :type interval_expression:          string
    """
    def __init__(self,
                 ts_connection,
                 schedule_name=None,
                 schedule_priority=50,
                 schedule_type='Extract',
                 schedule_execution_order='Parallel',
                 schedule_frequency='Daily',
                 start_time='12:00:00',
                 end_time='23:00:00',
                 interval_expression=None):

        super().__init__(ts_connection)
        self._schedule_name = schedule_name
        self._schedule_priority = schedule_priority
        self._schedule_type = schedule_type
        self._schedule_execution_order = schedule_execution_order
        self._schedule_frequency = schedule_frequency
        self._start_time = start_time
        self._end_time = end_time
        self._interval_expression = interval_expression
        self.base_update_schedule_request

    @property
    def optional_schedule_param_keys(self):
        return [
            'name',
            'priority',
            'type',
            'frequency',
            'executionOrder'
        ]

    @property
    def optional_frequency_param_keys(self):
        return [
            'start',
            'end'
        ]

    @property
    def optional_schedule_param_values(self):
        return [
            self._schedule_name,
            self._schedule_priority,
            self._schedule_type,
            self._schedule_frequency,
            self._schedule_execution_order
        ]

    @property
    def optional_frequency_param_values(self):
        return [
            self._start_time,
            self._end_time
        ]

    @property
    def base_update_schedule_request(self):
        self._request_body.update({'schedule': {'frequencyDetails': {}}})
        return self._request_body

    @property
    def modified_update_schedule_request(self):
        if any(self.optional_schedule_param_values):
            self._request_body['schedule'].update(
                self._get_parameters_dict(self.required_schedule_param_keys,
                                          self.required_schedule_param_values))

        if any(self.optional_frequency_param_values):
            self._request_body['schedule']['frequencyDetails'].update(
                self._get_parameters_dict(self.required_frequency_param_keys,
                                          self.required_frequency_param_values))

        if self._interval_expression:
            self._request_body['schedule']['frequencyDetails'].update({'intervals': {}})
            self._request_body['schedule']['frequencyDetails']['intervals'].update(
                {'interval': self._interval_expression})

        return self._request_body

    def get_request(self):
        return self.modified_update_schedule_request
