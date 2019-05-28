class BaseMethod:
    """
    Base method for building the methods listed on the Tableau Server API reference.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    """
    def __init__(self,
                 ts_connection):
        self._connection = ts_connection
