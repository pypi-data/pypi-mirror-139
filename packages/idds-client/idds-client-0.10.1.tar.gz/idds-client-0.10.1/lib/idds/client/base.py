#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0OA
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2019


"""
Base rest client to access IDDS system.
"""


import logging
import os
import requests
try:
    # Python 2
    from urllib import urlencode, quote
except ImportError:
    # Python 3
    from urllib.parse import urlencode, quote

from idds.common import exceptions
from idds.common.constants import HTTP_STATUS_CODE
from idds.common.utils import json_dumps, json_loads
from idds.common.authentication import OIDCAuthenticationUtils


class BaseRestClient(object):

    """Base Rest client"""

    def __init__(self, host=None, auth=None, timeout=None, client_proxy=None):
        """
        Constructor of the BaseRestClient.

        :param host: the address of the IDDS server.
        :param client_proxy: the client certificate proxy.
        :param timeout: timeout in seconds.
        """

        self.host = host
        self.auth = auth
        self.client_proxy = client_proxy
        self.timeout = timeout
        self.session = requests.session()
        self.retries = 2

        self.auth_type = None
        self.oidc_token = None
        self.vo = None
        self.auth_setup = False
        if self.auth:
            if 'auth_type' in self.auth:
                self.auth_type = self.auth['auth_type']
            if 'client_proxy' in self.auth:
                self.client_proxy = self.auth['client_proxy']
            if 'oidc_token' in self.auth:
                self.oidc_token = self.auth['oidc_token']
            if 'vo' in self.auth:
                self.vo = self.auth['vo']
            if 'auth_setup' in self.auth:
                self.auth_setup = self.auth['auth_setup']

        self.check_auth()

    def check_auth(self):
        """
        To check whether the auth type is supported and the input for the auth is available.
        """
        if not self.auth_type:
            logging.warn("auth_type is not set, will use x509_proxy")
            self.auth_type = 'x509_proxy'

        if self.auth_type in ['x509_proxy']:
            if not self.client_proxy or not os.path.exists(self.client_proxy):
                raise exceptions.RestException("Cannot find a valid x509 proxy.")
        elif self.auth_type in ['oidc']:
            if not self.auth_setup:
                if not self.oidc_token or not os.path.exists(self.oidc_token):
                    raise exceptions.RestException("Cannot find oidc token.")
                if not self.vo:
                    raise exceptions.RestException("vo is not defined for oidc authentication.")
        else:
            logging.error("auth_type %s is not supported." % str(self.auth_type))

    def build_url(self, url, path=None, params=None, doseq=False):
        """
        Build url path.

        :param url: base url path.
        :param path: relative url path.
        :param params: parameters to be sent with url.

        :returns: full url path.
        """
        full_url = url
        if path is not None:
            full_url = '/'.join([full_url, path])
        if params:
            full_url += "?"
            if isinstance(params, str):
                full_url += quote(params)
            else:
                full_url += urlencode(params, doseq=doseq)
        return full_url

    def get_request_response(self, url, type='GET', data=None, headers=None, auth_setup_step=False):
        """
        Send request to the IDDS server and get the response.

        :param url: http url to connection.
        :param type: request type(GET, PUT, POST, DEL).
        :param data: data to be sent to the IDDS server.
        :param headers: http headers.

        :returns: response data as json.
        :raises:
        """

        result = None
        if not headers:
            headers = {}
        headers['X-IDDS-Auth-Type'] = self.auth_type
        headers['X-IDDS-Auth-VO'] = self.vo

        for retry in range(self.retries):
            try:
                if self.auth_type in ['x509_proxy']:
                    if type == 'GET':
                        result = self.session.get(url, cert=(self.client_proxy, self.client_proxy), timeout=self.timeout, headers=headers, verify=False)
                    elif type == 'PUT':
                        result = self.session.put(url, cert=(self.client_proxy, self.client_proxy), data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                    elif type == 'POST':
                        result = self.session.post(url, cert=(self.client_proxy, self.client_proxy), data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                    elif type == 'DEL':
                        result = self.session.delete(url, cert=(self.client_proxy, self.client_proxy), data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                    else:
                        return
                elif self.auth_type in ['oidc']:
                    if auth_setup_step:
                        if type == 'GET':
                            result = self.session.get(url, timeout=self.timeout, headers=headers, verify=False)
                        elif type == 'PUT':
                            result = self.session.put(url, data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                        elif type == 'POST':
                            result = self.session.post(url, data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                        elif type == 'DEL':
                            result = self.session.delete(url, data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                        else:
                            return
                    else:
                        oidc_utils = OIDCAuthenticationUtils()
                        status, token = oidc_utils.load_token(self.oidc_token)
                        if not status:
                            raise exceptions.IDDSException("Token %s cannot be loaded: %s" % (self.oidc_token, str(token)))
                        is_expired, errors = oidc_utils.is_token_expired(token)
                        if is_expired:
                            raise exceptions.IDDSException("Token is already expired: %s" % errors)
                        headers['X-IDDS-Auth-Token'] = token['id_token']

                        if type == 'GET':
                            result = self.session.get(url, timeout=self.timeout, headers=headers, verify=False)
                        elif type == 'PUT':
                            result = self.session.put(url, data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                        elif type == 'POST':
                            result = self.session.post(url, data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                        elif type == 'DEL':
                            result = self.session.delete(url, data=json_dumps(data), timeout=self.timeout, headers=headers, verify=False)
                        else:
                            return
            except requests.exceptions.ConnectionError as error:
                logging.warning('ConnectionError: ' + str(error))
                if retry >= self.retries - 1:
                    raise exceptions.ConnectionException('ConnectionError: ' + str(error))

            if result is not None:
                # print(result.text)
                # print(result.headers)
                # print(result.status_code)
                if result.status_code == HTTP_STATUS_CODE.OK:
                    # print(result.text)
                    if result.text:
                        return json_loads(result.text)
                    else:
                        return None
                elif result.headers and 'ExceptionClass' in result.headers:
                    try:
                        if result.headers and 'ExceptionClass' in result.headers:
                            cls = getattr(exceptions, result.headers['ExceptionClass'])
                            msg = result.headers['ExceptionMessage']
                            raise cls(msg)
                        else:
                            if result.text:
                                data = json_loads(result.text)
                                raise exceptions.IDDSException(**data)
                            else:
                                raise exceptions.IDDSException("Unknow exception: %s" % (result.text))
                    except AttributeError:
                        raise exceptions.IDDSException(result.text)
                elif result.status_code in [HTTP_STATUS_CODE.BadRequest,
                                            HTTP_STATUS_CODE.Unauthorized,
                                            HTTP_STATUS_CODE.Forbidden,
                                            HTTP_STATUS_CODE.NotFound,
                                            HTTP_STATUS_CODE.NoMethod,
                                            HTTP_STATUS_CODE.InternalError]:
                    raise exceptions.IDDSException(result.text)
                else:
                    try:
                        if result.headers and 'ExceptionClass' in result.headers:
                            cls = getattr(exceptions, result.headers['ExceptionClass'])
                            msg = result.headers['ExceptionMessage']
                            raise cls(msg)
                        else:
                            if result.text:
                                data = json_loads(result.text)
                                raise exceptions.IDDSException(**data)
                            else:
                                raise exceptions.IDDSException("Unknow exception: %s" % (result.text))
                    except AttributeError:
                        raise exceptions.IDDSException(result.text)
        if result is None:
            raise exceptions.IDDSException('Response is None')
