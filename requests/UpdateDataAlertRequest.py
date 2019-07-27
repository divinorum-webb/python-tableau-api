from .BaseRequest import BaseRequest


class UpdateDataAlertRequest(BaseRequest):
    """
    Update site request for generating API requests to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param subject:             (Optional) The string to set as the new subject of the alert.
    :type subject:              string
    :param frequency:           (Optional) The frequency of the data-driven alert: once, frequently, hourly,
                                daily, or weekly.
    :type frequency:            string
    :param alert_owner_id:      (Optional) The ID of the user to assign as owner of the data-driven alert.
    :type alert_owner_id:       string
    :param is_public_flag:      (Optional) Boolean flag.
                                Determines the visibility of the data-driven alert. If the flag is True,
                                users with access to the view containing the alert can see the alert and add
                                themselves as recipients. If the flag is False, then the alert is only visible
                                to the owner, site or server administrators, and specific users they add as recipients.
    :type is_public_flag:       boolean
    """
    def __init__(self,
                 ts_connection,
                 subject=None,
                 frequency=None,
                 alert_owner_id=None,
                 is_public_flag=None):
        super().__init__(ts_connection)
        self._subject = subject
        self._frequency = frequency
        self._alert_owner_id = alert_owner_id
        self._is_public_flag = is_public_flag
        self.base_update_alert_request

    @property
    def optional_alert_param_keys(self):
        return [
            'subject',
            'frequency',
            'public'
        ]

    @property
    def optional_owner_param_keys(self):
        return ['id']

    @property
    def optional_alert_param_values(self):
        return [
            self._subject,
            self._frequency,
            self._is_public_flag
        ]

    @property
    def optional_owner_param_values(self):
        return [self._alert_owner_id]

    @property
    def base_update_alert_request(self):
        self._request_body.update({'dataAlert': {}})
        return self._request_body

    @property
    def modified_update_alert_request(self):
        self._request_body['dataAlert'].update(
            self._get_parameters_dict(
                self.optional_alert_param_keys,
                self.optional_alert_param_values))
        if self._alert_owner_id:
            self._request_body['dataAlert'].update({'owner': {}})
            self._request_body['dataAlert']['owner'].update(
                self._get_parameters_dict(
                    self.optional_owner_param_keys,
                    self.optional_owner_param_values))
        return self._request_body

    def get_request(self):
        return self.modified_update_alert_request
