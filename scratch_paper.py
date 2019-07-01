def publish(self, workbook_item, file_path, mode, connection_credentials=None, connections=None, as_job=False):

    filename = os.path.basename(file_path)
    file_extension = os.path.splitext(filename)[1][1:]

    # Construct the url with the defined mode
    url = "{0}?workbookType={1}".format(self.baseurl, file_extension)
    if mode == self.parent_srv.PublishMode.Overwrite:
        url += '&{0}=true'.format(mode.lower())
    elif mode == self.parent_srv.PublishMode.Append:
        error = 'Workbooks cannot be appended.'
        raise ValueError(error)

    if as_job:
        url += '&{0}=true'.format('asJob')

    # Determine if chunking is required (64MB is the limit for single upload method)
    if os.path.getsize(file_path) >= FILESIZE_LIMIT:
        upload_session_id = Fileuploads.upload_chunks(self.parent_srv, file_path)
        url = "{0}&uploadSessionId={1}".format(url, upload_session_id)
        conn_creds = connection_credentials
        xml_request, content_type = RequestFactory.Workbook.publish_req_chunked(workbook_item,
                                                                                connection_credentials=conn_creds,
                                                                                connections=connections)
    else:
        with open(file_path, 'rb') as f:
            file_contents = f.read()
        conn_creds = connection_credentials
        xml_request, content_type = RequestFactory.Workbook.publish_req(workbook_item,
                                                                        filename,
                                                                        file_contents,
                                                                        connection_credentials=conn_creds,
                                                                        connections=connections)
    logger.debug('Request xml: {0} '.format(xml_request[:1000]))

    # Send the publishing request to server
    try:
        server_response = self.post_request(url, xml_request, content_type)
    except InternalServerError as err:
        if err.code == 504 and not as_job:
            err.content = "Timeout error while publishing. Please use asynchronous publishing to avoid timeouts."
        raise err

    if as_job:
        new_job = JobItem.from_response(server_response.content, self.parent_srv.namespace)[0]
        logger.info('Published {0} (JOB_ID: {1}'.format(filename, new_job.id))
        return new_job
    else:
        new_workbook = WorkbookItem.from_response(server_response.content, self.parent_srv.namespace)[0]
        logger.info('Published {0} (ID: {1})'.format(filename, new_workbook.id))
        return new_workbook

@classmethod
def upload_chunks(cls, parent_srv, file_path):
    file_uploader = cls(parent_srv)
    upload_id = file_uploader.initiate()
    chunks = file_uploader.read_chunks(file_path)
    for chunk in chunks:
        xml_request, content_type = RequestFactory.Fileupload.chunk_req(chunk)
        fileupload_item = file_uploader.append(xml_request, content_type)
        logger.info("\tPublished {0}MB of {1}".format(fileupload_item.file_size,
                                                      os.path.basename(file_path)))
    logger.info("\tCommitting file upload...")
    return upload_id


class FileuploadRequest(object):
    def chunk_req(self, chunk):
        parts = {'request_payload': ('', '', 'text/xml'),
                 'tableau_file': ('file', chunk, 'application/octet-stream')}
        return _add_multipart(parts)

def read_chunks(self, file_path):
    with open(file_path, 'rb') as f:
        while True:
            chunked_content = f.read(CHUNK_SIZE)
            if not chunked_content:
                break
            yield chunked_content


"""
Dissect code for publishing
"""


def publish(self, workbook_item, file_path, mode, connection_credentials=None, connections=None, as_job=False):

    filename = os.path.basename(file_path)
    file_extension = os.path.splitext(filename)[1][1:]

    # Construct the url with the defined mode
    url = "{0}?workbookType={1}".format(self.baseurl, file_extension)
    if mode == self.parent_srv.PublishMode.Overwrite:
        url += '&{0}=true'.format(mode.lower())

    if as_job:
        url += '&{0}=true'.format('asJob')

    # Determine if chunking is required (64MB is the limit for single upload method)
    if os.path.getsize(file_path) >= FILESIZE_LIMIT:
        upload_session_id = Fileuploads.upload_chunks(self.parent_srv, file_path)
        url = "{0}&uploadSessionId={1}".format(url, upload_session_id)
        conn_creds = connection_credentials
        xml_request, content_type = RequestFactory.Workbook.publish_req_chunked(workbook_item,
                                                                                connection_credentials=conn_creds,
                                                                                connections=connections)
    else:
        with open(file_path, 'rb') as f:
            file_contents = f.read()
        conn_creds = connection_credentials
        xml_request, content_type = RequestFactory.Workbook.publish_req(workbook_item,
                                                                        filename,
                                                                        file_contents,
                                                                        connection_credentials=conn_creds,
                                                                        connections=connections)

    # Send the publishing request to server
    server_response = self.post_request(url, xml_request, content_type)

    if as_job:
        new_job = JobItem.from_response(server_response.content, self.parent_srv.namespace)[0]
        return new_job
    else:
        new_workbook = WorkbookItem.from_response(server_response.content, self.parent_srv.namespace)[0]
        return new_workbook


"""
From above, expand these lines:
-> upload_session_id = Fileuploads.upload_chunks(self.parent_srv, file_path)
-> xml_request, content_type = RequestFactory.Workbook.publish_req_chunked(workbook_item,
                                                                            connection_credentials=conn_creds,
                                                                            connections=connections)
"""

# expanding on upload_session_id


@classmethod
def upload_chunks(cls, parent_srv, file_path):
    file_uploader = cls(parent_srv)
    # generate the session ID to use during uploads
    upload_id = file_uploader.initiate()
    # store all of the file chunks into variable 'chunks'
    # uses yield to ... yield each chunk of the whole object
    chunks = file_uploader.read_chunks(file_path)
    for chunk in chunks:
        # for each chunk, generate the xml request and content type
        # the RequestFactory.Fileupload.chun_req(chunk) ends up calling _add_multipart(parts)
        # xml_request, content_type are returned from the _add_multipart(parts) call
        xml_request, content_type = RequestFactory.Fileupload.chunk_req(chunk)
        # file_uploader.append(xml_request, content_type) uses a put request to append the chunk to the file
        fileupload_item = file_uploader.append(xml_request, content_type)
    return upload_id


def initiate(self):
    url = self.baseurl
    server_response = self.post_request(url, '')
    fileupload_item = FileuploadItem.from_response(server_response.content, self.parent_srv.namespace)
    self.upload_id = fileupload_item.upload_session_id
    return self.upload_id


def read_chunks(self, file_path):
    with open(file_path, 'rb') as f:
        while True:
            chunked_content = f.read(CHUNK_SIZE)
            if not chunked_content:
                break
            yield chunked_content


# RequestFactory.Fileupload.chunk_req(chunk)
def chunk_req(self, chunk):
    parts = {'request_payload': ('', '', 'text/xml'),
             'tableau_file': ('file', chunk, 'application/octet-stream')}
    return _add_multipart(parts)


def _add_multipart(parts):
    mime_multipart_parts = list()
    for name, (filename, data, content_type) in parts.items():
        multipart_part = RequestField(name=name, data=data, filename=filename)
        multipart_part.make_multipart(content_type=content_type)
        mime_multipart_parts.append(multipart_part)
    xml_request, content_type = encode_multipart_formdata(mime_multipart_parts)
    content_type = ''.join(('multipart/mixed',) + content_type.partition(';')[1:])
    return xml_request, content_type


def append(self, xml_request, content_type):
    url = "{0}/{1}".format(self.baseurl, self.upload_id)
    server_response = self.put_request(url, xml_request, content_type)
    return FileuploadItem.from_response(server_response.content, self.parent_srv.namespace)


def publish_req_chunked(self, workbook_item, connection_credentials=None, connections=None):
    xml_request = self._generate_xml(workbook_item,
                                     connection_credentials=connection_credentials,
                                     connections=connections)

    parts = {'request_payload': ('', xml_request, 'text/xml')}
    return _add_multipart(parts)
