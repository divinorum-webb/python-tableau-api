class CreateSiteRequest(BaseRequest):
    """
    Create site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param site_name:
    :type site_name:
    :param admin_mode:
    :type admin_mode:
    :param user_quota:
    :type user_quota:
    :param storage_quota:
    :type storage_quota:
    :param disable_subscriptions:
    :type disable_subscriptions:
    :param flows_enabled_flag:
    :type flows_enabled_flag:
    :param guest_access_enabled_flag:
    :type guest_access_enabled_flag:
    :param cache_warmup_enabled_flag:
    :type cache_warmup_enabled_flag:
    :param commenting_enabled_flag:
    :type commenting_enabled_flag:
    :param revision_history_enabled:
    :type revision_history_enabled:
    :param revision_limit:
    :type revision_limit:
    :param subscribe_others_enabled_flag:
    :type subscribe_others_enabled_flag:
    """
    def __init__(self,
                 ts_connection,
                 site_name,
                 admin_mode='ContentAndUsers',
                 user_quota=None,
                 storage_quota=None,
                 disable_subscriptions=False,
                 flows_enabled_flag=None,
                 guest_access_enabled_flag=False,
                 cache_warmup_enabled_flag=False,
                 commenting_enabled_flag=False,
                 revision_history_enabled=False,
                 revision_limit=None,
                 subscribe_others_enabled_flag=False):

        super().__init__(ts_connection)
        self._site_name = site_name
        self._admin_mode = admin_mode
        self._user_quota = user_quota
        self._storage_quota = storage_quota
        self._disable_subscriptions = disable_subscriptions
        self._flows_enabled_flag = flows_enabled_flag
        self._guest_access_enabled_flag = guest_access_enabled_flag
        self._cache_warmup_enabled_flag = cache_warmup_enabled_flag
        self._commenting_enabled_flag = commenting_enabled_flag
        self._revision_history_enabled = revision_history_enabled
        self._revision_limit = revision_limit
        self._subscribe_others_enabled_flag = subscribe_others_enabled_flag
        self.base_create_site_request

    @property
    def optional_param_keys(self):
        return [
            'storageQuota',
            'disableSubscriptions',
            'flowsEnabled',
            'guestAccessEnabled',
            'cacheWarmupEnabled',
            'commentingEnabled',
            'revisionHistoryEnabled',
            'revisionLimit',
            'subscribeOthersEnabled'
        ]

    @property
    def optional_param_values(self):
        return [
            self._storage_quota,
            'true' if self._disable_subscriptions else None,
            'true' if self._flows_enabled_flag else None,
            'true' if self._guest_access_enabled_flag else None,
            'true' if self._cache_warmup_enabled_flag else None,
            'true' if self._commenting_enabled_flag else None,
            'true' if self._revision_history_enabled else None,
            self._revision_limit,
            'true' if self._subscribe_others_enabled_flag else None
        ]

    @property
    def base_create_site_request(self):
        self._request_body.update({
            'site': {
                'name': self._site_name,
                'contentUrl': self._connection.site_url,
                'adminMode': self._admin_mode
            }
        })
        return self._request_body

    @property
    def modified_create_site_request(self):
        if self._user_quota and self._admin_mode != 'ContentOnly':
            self._request_body['site'].update({'userQuota': self._user_quota})
        elif self._user_quota:
            self._invalid_parameter_exception()

        self._request_body['site'].update(self._get_parameters_dict(self.optional_param_keys,
                                                                    self.optional_param_values))
        return self._request_body

    def get_request(self):
        return self.modified_create_site_request
