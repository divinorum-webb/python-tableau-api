class UpdateSiteRequest(BaseRequest):
    """
    Update site request for generating API request URLs to Tableau Server.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param site_name:
    :type site_name:
    :param content_url:
    :type content_url:
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
                 site_name=None,
                 content_url=None,
                 admin_mode=None,
                 user_quota=None,
                 state='Active',
                 storage_quota=None,
                 disable_subscriptions=None,
                 flows_enabled_flag=None,
                 guest_access_enabled_flag=False,
                 cache_warmup_enabled_flag=False,
                 commenting_enabled_flag=False,
                 revision_history_enabled=False,
                 revision_limit=None,
                 subscribe_others_enabled_flag=False
                 ):

        super().__init__(ts_connection)
        self._site_name = site_name
        self._content_url = content_url
        self._admin_mode = admin_mode
        self._user_quota = user_quota
        self._state = state
        self._storage_quota = storage_quota
        self._disable_subscriptions = disable_subscriptions
        self._flows_enabled_flag = flows_enabled_flag
        self._guest_access_enabled_flag = guest_access_enabled_flag
        self._cache_warmup_enabled_flag = cache_warmup_enabled_flag
        self._commenting_enabled_flag = commenting_enabled_flag
        self._revision_history_enabled = revision_history_enabled
        self._revision_limit = revision_limit
        self._subscribe_others_enabled_flag = subscribe_others_enabled_flag
        self._request_body = {'site': {}}

    @property
    def optional_param_keys(self):
        return [
            'name',
            'contentUrl',
            'adminMode',
            'state',
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
            self._site_name,
            self._content_url,
            self._admin_mode,
            self._state,
            self._storage_quota,
            'true' if self._disable_subscriptions == True else 'false' if self._disable_subscriptions == False else None,
            'true' if self._flows_enabled_flag == True else 'false' if self._flows_enabled_flag == False else None,
            'true' if self._guest_access_enabled_flag == True else 'false' if self._guest_access_enabled_flag == False else None,
            'true' if self._cache_warmup_enabled_flag == True else 'false' if self._cache_warmup_enabled_flag == False else None,
            'true' if self._commenting_enabled_flag == True else 'false' if self._commenting_enabled_flag == False else None,
            'true' if self._revision_history_enabled == True else 'false' if self._revision_history_enabled == False else None,
            self._revision_limit,
            'true' if self._subscribe_others_enabled_flag == True else 'false' if self._subscribe_others_enabled_flag == False else None
        ]

    @property
    def base_update_site_request(self):
        if self._user_quota and self._admin_mode != 'ContentOnly':
            self._request_body.update({'userQuota': self._user_quota})
        elif self._user_quota:
            self._invalid_parameter_exception()

        self._request_body['site'].update(self._get_parameters_dict(self.optional_param_keys,
                                                                    self.optional_param_values))
        return self._request_body

    def get_request(self):
        return self.base_update_site_request
