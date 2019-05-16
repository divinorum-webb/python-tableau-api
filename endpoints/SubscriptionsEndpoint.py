class SubscriptionsEndpoint(BaseEndpoint):
    """
    Subscriptions endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param create_subscription:
    :type create_subscription:
    :param query_subscriptions:
    :type query_subscriptions:
    :param query_subscription:
    :type query_subscription:
    :param update_subscription:
    :type update_subscription:
    :param delete_subscription:
    :type delete_subscription:
    :param subscription_id:
    :type subscription_id:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 create_subscription=False,
                 query_subscriptions=False,
                 query_subscription=False,
                 update_subscription=False,
                 delete_subscription=False,
                 subscription_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._create_subscription = create_subscription
        self._query_subscriptions = query_subscriptions
        self._query_subscription = query_subscription
        self._update_subscription = update_subscription
        self._delete_subscription = delete_subscription
        self._subscription_id = subscription_id
        self._parameter_dict = parameter_dict

    @property
    def base_subscription_url(self):
        return "{0}/api/{1}/sites/{2}/subscriptions".format(self._connection.server,
                                                            self._connection.api_version,
                                                            self._connection.site_id)

    @property
    def base_subscription_id_url(self):
        return "{0}/{1}".format(self.base_subscription_url,
                                self._subscription_id)

    def get_endpoint(self):
        if self._create_subscription:
            url = self.base_subscription_url
        elif self._query_subscriptions and not self._subscription_id:
            url = self.base_subscription_url
        elif self._subscription_id:
            if self._query_subscription or self._update_subscription or self._delete_subscription:
                url = self.base_subscription_id_url
            else:
                self._invalid_parameter_exception()
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
