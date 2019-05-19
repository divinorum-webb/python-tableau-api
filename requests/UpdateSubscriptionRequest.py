class UpdateSubscriptionRequest(BaseRequest):
    """
    Update subscription request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param new_subscription_subject:
    :type new_subscription_subject:
    :param new_schedule_id:
    :type new_schedule_id:
    """
    def __init__(self,
                 ts_connection,
                 new_subscription_subject=None,
                 new_schedule_id=None):

        super().__init__(ts_connection)
        self._new_subscription_subject = new_subscription_subject
        self._new_schedule_id = new_schedule_id

    @property
    def base_update_subscription_request(self):
        if self._new_subscription_subject and self._new_schedule_id:
            self._request_body.update({
                'subscription': {
                    'subject': self._new_subscription_subject,
                    'schedule': {'id': self._new_schedule_id}
                }
            })
        elif self._new_subscription_subject and not self._new_schedule_id:
            self._request_body.update({
                'subscription': {
                    'subject': self._new_subscription_subject
                }
            })
        else:
            self._request_body.update({
                'subscription': {
                    'schedule': {'id': self._new_schedule_id}
                }
            })
        return self._request_body

    def get_request(self):
        return self.base_update_subscription_request
