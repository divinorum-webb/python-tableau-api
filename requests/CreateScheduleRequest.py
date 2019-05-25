class CreateScheduleRequest(BaseRequest):
    """
    Create schedule request for generating API request URLs to Tableau Server.

    :param ts_connection:               The Tableau Server connection object.
    :type ts_connection:                class
    :param schedule_name:               The name of the schedule being created.
    :type schedule_name:                string
    :param schedule_priority:           The priority value (1-100) for the schedule
    :type schedule_priority:            string
    :param schedule_type:               The schedule type (Flow, Extract, or Subscription)
    :type schedule_type:                string
    :param schedule_execution_order:    Set this value to 'Parallel' to allow jobs associated with this schedule to
                                        run in parallel; set the value to 'Serial' to require the jobs to run one at
                                        a time.
    :type schedule_execution_order:     string
    :param schedule_frequency:          The granularity of the schedule (Hourly, Daily, Weekly, or Monthly).
    :type schedule_frequency:           string
    :param start_time:                  The time of day when the schedule should run (HH:MM:SS). If the frequency is
                                        set to 'Hourly', this value indicates the hour the schedule starts running.
    :type start_time:                   string
    :param end_time:                    Only set this value if the schedule frequency has been set to 'Hourly'. This
                                        value indicates the hour the schedule will stop running (HH:MM:SS).
    :type end_time:                     string
    :param interval_expression:         This value specifies the time interval between jobs associated with the
                                        schedule. The value required here depends on the 'schedule_frequency' value.
                                        If 'schedule_frequency' = 'Hourly', the interval expression should be either
                                        hours="interval" (where "interval" is a number [1, 2, 4, 6, 8, 12] in quotes).
                                        If 'schedule_frequency' = 'Daily', no interval needs to be specified.
                                        If 'schedule_frequency' = 'Weekly, the interval is weekDay="weekday", where
                                        weekday is one of ['Sunday', 'Monday', 'Tuesday', etc.] wrapped in quotes.
                                        If 'schedule_frequency' = 'Monthly', the interval expression is monthDay="day",
                                        where day is either the day of the month (1-31), or 'LastDay'. In both cases
                                        the value is wrapped in quotes.
    :type interval_expression:          string
    """
    def __init__(self,
                 ts_connection,
                 schedule_name,
                 schedule_priority=50,
                 schedule_type='Extract',
                 schedule_execution_order='Parallel',
                 schedule_frequency='Daily',
                 start_time='12:00:00',
                 end_time='23:00:00',
                 interval_expression=None
                 ):

        super().__init__(ts_connection)
        self._schedule_name = schedule_name
        self._schedule_priority = schedule_priority
        self._schedule_type = schedule_type
        self._schedule_execution_order = schedule_execution_order
        self._schedule_frequency = schedule_frequency
        self._start_time = start_time
        self._end_time = end_time
        self._interval_expression = interval_expression
        self.base_create_schedule_request

    @property
    def required_schedule_param_keys(self):
        return [
            'name',
            'priority',
            'type',
            'frequency',
            'executionOrder'
        ]

    @property
    def required_frequency_param_keys(self):
        return [
            'start',
            'end'
        ]

    @property
    def required_schedule_param_values(self):
        return [
            self._schedule_name,
            self._schedule_priority,
            self._schedule_type,
            self._schedule_frequency,
            self._schedule_execution_order
        ]

    @property
    def required_frequency_param_values(self):
        return [
            self._start_time,
            self._end_time
        ]

    @property
    def base_create_schedule_request(self):
        self._request_body.update({'schedule': {'frequencyDetails': {}}})
        return self._request_body

    @property
    def modified_create_schedule_request(self):
        self._request_body['schedule'].update(
            self._get_parameters_dict(self.required_schedule_param_keys,
                                      self.required_schedule_param_values))
        self._request_body['schedule']['frequencyDetails'].update(
            self._get_parameters_dict(self.required_frequency_param_keys,
                                      self.required_frequency_param_values))
        if self._interval_expression:
            self._request_body['schedule']['frequencyDetails'].update({'intervals': {}})
            self._request_body['schedule']['frequencyDetails']['intervals'].update(
                {'interval': self._interval_expression})
        return self._request_body

    def get_request(self):
        return self.modified_create_schedule_request
