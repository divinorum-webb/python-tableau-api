class FileUploadEndpoint(BaseEndpoint):
    """
    FileUploadEndpoint endpoint for Tableau Server API requests.

    :param ts_connection:       The Tableau Server connection object.
    :type ts_connection:        class
    :param initiate_file_upload:
    :type initiate_file_upload:
    :param append_to_file_upload:
    :type append_to_file_upload:
    :param upload_session_id:
    :type upload_session_id:
    :param parameter_dict:
    :type parameter_dict:
    """
    def __init__(self,
                 ts_connection,
                 initiate_file_upload=False,
                 append_to_file_upload=False,
                 upload_session_id=None,
                 parameter_dict=None):

        super().__init__(ts_connection)
        self._initiate_file_upload = initiate_file_upload
        self._append_to_file_upload = append_to_file_upload
        self._upload_session_id = upload_session_id
        self._parameter_dict = parameter_dict

    @property
    def base_file_upload_url(self):
        return "{0}/api/{1}/sites/{2}/fileUploads".format(self._connection.server,
                                                          self._connection.api_version,
                                                          self._connection.site_id)

    @property
    def base_file_upload_id_url(self):
        return "{0}/{1}".format(self.base_file_upload_url,
                                self._upload_session_id)

    def get_file_upload_endpoint(self):
        if self._initiate_file_upload:
            url = self.base_file_upload_url
        elif self._append_to_file_upload and self._upload_session_id:
            url = self.base_file_upload_id_url
        else:
            self._invalid_parameter_exception()

        return self._append_url_parameters(url)
