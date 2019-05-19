class CreateSubscriptionRequest(BaseRequest):
    """
    Create subscription request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param subscription_subject:
    :type subscription_subject:
    :param content_type:
    :type content_type:
    :param content_id:
    :type content_id:
    :param schedule_id:
    :type schedule_id:
    :param user_id:
    :type user_id:
    """
    def __init__(self,
                 ts_connection,
                 subscription_subject,
                 content_type,
                 content_id,
                 schedule_id,
                 user_id):

        super().__init__(ts_connection)
        self._subscription_subject = subscription_subject
        self._content_type = content_type
        self._content_id = content_id
        self._schedule_id = schedule_id
        self._user_id = user_id

    @property
    def base_create_subscription_request(self):
        self._request_body.update({
            'subscription': {
                'subject': self._subscription_subject,
                'content': {
                    'type': self._content_type,
                    'id': self._content_id
                },
                'schedule': {'id': self._schedule_id},
                'user': {'id': self._user_id}
            },
        })
        return self._request_body

    def get_request(self):
        return self.base_create_subscription_request
