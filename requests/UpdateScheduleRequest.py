class UpdateScheduleRequest(BaseRequest):
    """
    Update schedule request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param schedule_name:
    :type schedule_name:
    :param schedule_priority:
    :type schedule_priority:
    :param schedule_type:
    :type schedule_type:
    :param schedule_execution_order:
    :type schedule_execution_order:
    :param schedule_frequency:
    :type schedule_frequency:
    :param start_time:
    :type start_time:
    :param end_time:
    :type end_time:
    :param interval_expression:
    :type interval_expression:
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
