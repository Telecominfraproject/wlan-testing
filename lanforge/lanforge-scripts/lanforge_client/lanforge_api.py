#!/usr/bin/env python3
"""----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    LANforge-GUI Source Code
    Copyright (C) 1999-2021  Candela Technologies Inc
    http:www.candelatech.com

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

    Contact:  Candela Technologies <support@candelatech.com> if you have any
    questions.

                                LANforge JSON API

    A distinct difference from previous LF scripts is the notion of a session.
    Please create a session instance before connecting to your LANforge client.
    The session is informative for a GUI user how many scripts are actively
    using the GUI. It also provides logging to diagnose how many scripts are
    potentially accessing the GUI at the same time.

    EXAMPLE PYTHON USAGE:
    ----- ----- ----- 8< ----- ----- ----- 8< ----- ----- -----
    session = LFSession(lfclient_url="http://localhost:8080",
                        connect_timeout_sec=20,
                        proxy_map={
                                'http':'http://192.168.1.250:3128'
                            },
                        debug=True,
                        die_on_error=False);
    lf_command = session.get_command()
    full_response = []
    first_response = lf_command.json_post(  url="/nc_show_ports",
                                            post_data={
                                                "shelf": 1,
                                                "resource": 1,
                                                "ports": "all"
                                            },
                                            full_response)
    pprint(first_response)

    lf_query = session.get_query()
    response = lf_query.get_as_json(url="/port/1/1/list",
                                    debug=True)
    pprint(response)
    ----- ----- ----- 8< ----- ----- ----- 8< ----- ----- -----

    The API that this library provides is ACTIVELY BEING CHANGED.

    MAINTENANCE:
    To maintain this library, please refer to these files:
    * client/candela/lanforge/json_api.py
        -   the basis for many of the auto-generated python classes
            that follow after these class definitions.
    * client/candela/lanforge/JsonApiPythonGenerator.java
        -   the builder class that produces lf_json_autogen
    The file json_api.py is intended to be bundled in lfclient.jar and
    not to be extracted. It is sourced during build by the JsonApiPythonGenerator
    class which appends subclasses to it.

----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

from datetime import datetime
from enum import Enum
from enum import IntFlag
import http.client
from http.client import HTTPResponse
import json
import logging
from logging import Logger
from .logg import Logg
from .strutil import nott, iss
from pprint import pprint, pformat
import time
import traceback
from typing import Optional
import urllib
from urllib import request, error, parse

SESSION_HEADER = 'X-LFJson-Session'
LOGGER = Logger('json_api')


def _now_ms() -> int:
    return round(time.time() * 1000)


def _now_sec() -> int:
    return round(time.time() * 1000 * 1000)


def default_proxies() -> dict:
    return {
        # 'http': 'http://example.com',
        # 'https': 'https://example.com'
    }


def print_diagnostics(url_: str = None,
                      request_: urllib.request.Request = None,
                      responses_: list = None,
                      error_=None,
                      error_list_: list = None,
                      debug_: bool = False,
                      die_on_error_: bool = False):
    if debug_:
        print("::print_diagnostics: error_.__class__: %s" % error_.__class__)
        pprint(error_)

    if url_ is None:
        print("WARNING:print_diagnostics: url_ is None")
    if request_ is None:
        print("WARNING:print_diagnostics: request_ is None")
    if error_ is None:
        print("WARNING:print_diagnostics: error_ is None")

    method = 'NA'
    if hasattr(request_, 'method'):
        method = request_.method
    err_code = 0
    err_reason = 'NA'
    err_headers = []
    err_full_url = url_
    if hasattr(error_, 'code'):
        err_code = error_.code
    if hasattr(error_, 'reason'):
        err_reason = error_.reason
    if hasattr(error_, 'headers'):
        err_headers = error_.headers
    if hasattr(error_, 'get_full_url'):
        err_full_url = error_.get_full_url()
    xerrors = []
    if err_code == 404:
        xerrors.append("[%s HTTP %s] <%s> : %s" % (method, err_code, err_full_url, err_reason))
    else:
        if len(err_headers) > 0:
            for headername in sorted(err_headers.keys()):
                if headername.startswith("X-Error-"):
                    xerrors.append("%s: %s" % (headername, err_headers.get(headername)))
        if len(xerrors) > 0:
            print(" = = LANforge Error Messages = =")
            print(" = = URL: %s" % err_full_url)
            for xerr in xerrors:
                print(xerr)
                if (error_list_ is not None) and isinstance(error_list_, list):
                    error_list_.append(xerr)
            print(" = = = = = = = = = = = = = = = =")

    if error_.__class__ is urllib.error.HTTPError:
        if debug_:
            print("----- HTTPError: ------------------------------------ print_diagnostics:")
            print("%s <%s> HTTP %s: %s" % (method, err_full_url, err_code, err_reason))

        if err_code == 404:
            if (error_list_ is not None) and isinstance(error_list_, list):
                error_list_.append("[%s HTTP %s] <%s> : %s" % (method, err_code, err_full_url, err_reason))
        else:
            if debug_:
                print("  Content-type:[%s] Accept[%s]" % (
                    request_.get_header('Content-type'), request_.get_header('Accept')))

            if hasattr(request_, "data") and (request_.data is not None):
                print("  Data:")
                pprint(request_.data)
            elif debug_:
                print("    <no request data>")

        if debug_ and (len(err_headers) > 0):
            # the HTTPError is of type HTTPMessage a subclass of email.message
            print("  Response Headers: ")
            for headername in sorted(err_headers.keys()):
                print("    %s: %s" % (headername, err_headers.get(headername)))

        if len(responses_) > 0:
            print("----- Response: --------------------------------------------------------")
            pprint(responses_[0].reason)
        if debug_:
            print("------------------------------------------------------------------------")
        if die_on_error_:
            exit(1)
        return

    if error_.__class__ is urllib.error.URLError:
        print("----- URLError: ---------------------------------------------")
        print("%s <%s> HTTP %s: %s" % (method, err_full_url, err_code, err_reason))
        print("------------------------------------------------------------------------")
    if die_on_error_:
        exit(1)


class BaseLFJsonRequest:
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        Perform HTTP get/post/put/delete with extensions specific to LANforge JSON
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    No_Data: dict = {'No Data': 0}
    OK_STATUSES = (100, 200, 201, 204, 205, 206, 301, 302, 303, 304, 307, 308, 404)
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def __init__(self,
                 session_obj: 'BaseSession' = None,
                 debug: bool = False,
                 stream_errors: bool = True,
                 stream_warnings: bool = False,
                 exit_on_error: bool = False):
        self.default_headers: dict = {'Accept': 'application/json'}
        self.debug_on: bool = False
        self.error_list: list = []
        # post_data: dict = No_Data
        self.proxies_installed: bool = False
        self.session_instance: 'BaseSession'
        self.session_instance = None
        self.stream_errors: bool = True
        self.stream_warnings: bool = False

        if not session_obj:
            logging.getLogger(__name__).warning("BaseLFJsonRequest: no session instance")
        else:
            self.session_instance = session_obj
            self.session_id = session_obj.get_session_id()
            self.proxies_installed = session_obj.proxies_installed

        self.die_on_error: bool
        self.die_on_error = exit_on_error
        if session_obj:
            self.die_on_error |= session_obj.is_exit_on_error()

        self.lfclient_url = session_obj.get_lfclient_url()

        self.stream_errors = stream_errors
        self.warnings = []
        self.stream_warnings = stream_warnings
        self.logger = Logg(name="LFJsonRequest-@", debug=debug)
        self.debug_on = debug

    def get_corrected_url(self,
                          url: str = None,
                          debug: bool = False):
        """

        :param url: If you have a session you can provide the abbreviated URL optionally starting with a slash
        :param debug: turn on debugging
        :return: full url prepended with
        """

        if nott(url):
            raise Exception("%s: Bad url[%s]" % (__name__, url))

        corrected_url: str = url

        if not url.startswith(self.session_instance.get_lfclient_url()):
            if url.startswith('/'):
                corrected_url = self.session_instance.get_lfclient_url() + url
            else:
                corrected_url = self.session_instance.get_lfclient_url() + '/' + url

        if nott(corrected_url):
            raise Exception("%s: Bad url[%s]" % (__name__, url))

        if corrected_url.find('//'):
            protopos = corrected_url.find("://")
            corrected_url = corrected_url[:protopos + 2] + corrected_url[protopos + 2:].replace("//", "/")

        # finding '#' prolly indicates a macvlan (eth1#0)
        # finding ' ' prolly indicates a field name that should imply %20
        if corrected_url.find('#') >= 1:
            corrected_url = corrected_url.replace('#', '%23')
        if corrected_url.find(' ') >= 1:
            corrected_url = corrected_url.replace(' ', '%20')
        if debug:
            self.logger.by_method("%s: url [%s] now [%s]" % (str(__class__), url, corrected_url))
        return corrected_url

    def add_error(self, message: str = None):
        if not message:
            return
        if self.stream_errors:
            self.logger.error(message=message)
        self.error_list.append(message)

    def add_warning(self, message: str = None):
        self.logger.warning(message)
        if self.stream_errors:
            self.logger.warning(message=message)
        self.warnings.append(message)

    def get_errors(self) -> list:
        return self.error_list

    def get_warnings(self) -> list:
        return self.warnings

    def clear_warnings_errors(self, flush_to_session=False):
        """ erase errors and warnings """
        if flush_to_session:
            if not self.session_instance:
                self.logger.error(message="cannot flush messages to session when there is no session instance")
            else:
                self.session_instance.session_error_list.extend(self.error_list)
                self.session_instance.session_warnings_list.extend(self.warnings)
        self.error_list = []
        self.warnings = []
        self.logger.info(message='BaseLFJsonRequest.clear()')

    def extract_values(self,
                       response: dict = None,
                       singular_key: str = None,
                       plural_key: str = None) -> list:
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Extract fields from this response using the expected keys:
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        if not singular_key:
            raise ValueError("extract_values wants non-empty singular_key")
        if not plural_key:
            raise ValueError("extract_values wants non-empty plural_key")

        if singular_key not in response:
            if plural_key not in response:
                self.add_warning("response did not contain <{}> or <{}>".format(singular_key, plural_key))
                return []
            if not response[plural_key]:
                self.add_warning("response[{}] is empty".format(plural_key))
            return response[plural_key]
        if not response[singular_key]:
            self.add_warning("response[{}] is empty".format(singular_key))
        return response[singular_key]

    def form_post(self,
                  url: str = None,
                  post_data: dict = None,
                  debug: bool = False,
                  die_on_error_: bool = False):
        die_on_error_ |= self.die_on_error
        debug |= self.debug_on
        responses = []
        # https://stackoverflow.com/a/59635684/11014343
        if (self.session_instance.proxy_map is not None) and (len(self.session_instance.proxy_map) > 0):
            # https://stackoverflow.com/a/59635684/11014343
            opener = request.build_opener(request.ProxyHandler(self.session_instance.proxy_map))
            request.install_opener(opener)

        # if debug:
            self.logger.by_method("form_post: url: " + url)
        if (post_data is not None) and (post_data is not self.No_Data):
            urlenc_data = urllib.parse.urlencode(post_data).encode("utf-8")
            self.logger.by_method("formPost: data looks like:" + str(urlenc_data))
            if debug:
                print("formPost: url: " + url)
            myrequest = request.Request(url=url,
                                        data=urlenc_data,
                                        headers=self.default_headers)
        else:
            myrequest = request.Request(url=url, headers=self.default_headers)
            self.logger.by_method("json_post: No data sent to [%s]" % url)

        myrequest.headers['Content-type'] = 'application/x-www-form-urlencoded'

        try:
            resp = urllib.request.urlopen(myrequest)
            responses.append(resp)
            return responses[0]

        except urllib.error.HTTPError as herror:
            print_diagnostics(url_=url,
                              request_=myrequest,
                              responses_=responses,
                              error_=herror,
                              error_list_=self.error_list,
                              debug_=debug,
                              die_on_error_=die_on_error_)
            if die_on_error_ and (herror.code != 404):
                exit(1)
        except urllib.error.URLError as uerror:
            print_diagnostics(url_=url,
                              request_=myrequest,
                              responses_=responses,
                              error_=uerror,
                              error_list_=self.error_list,
                              debug_=debug,
                              die_on_error_=die_on_error_)
            if die_on_error_:
                exit(1)
        if die_on_error_:
            exit(1)
        return None

    def json_post(self,
                  url: str = "",
                  post_data: dict = None,
                  debug: bool = False,
                  wait_sec: float = None,
                  connection_timeout_sec: float = None,
                  max_timeout_sec: float = None,
                  die_on_error: bool = False,
                  errors_warnings: list = None,    # p3.9 list[str]
                  response_json_list: list = None,
                  method_: str = 'POST',
                  session_id_: str = "") -> Optional:  # p3.9 Optional[HTTPResponse]
        """

        :param url: URL to post to
        :param post_data: data to send in post
        :param debug: turn on diagnostics
        :param wait_sec: pause before making request
        :param connection_timeout_sec: immediate connection timeout
        :param max_timeout_sec: retry for this many seconds before returning
        :param errors_warnings: list to collect errors and warnings with
        :param die_on_error: exit() if the return status is not 200
        :param response_json_list: pass in a list to store json data in the response
        :param method_: override HTTP method, please do not override
        :param session_id_: insert a session to the header; this is useful in the case where we are
        operating outside a session context, like during the __del__ constructor
        :return: returns first set of http.client.HTTPResponse data
        """
        debug |= self.debug_on
        die_on_error |= self.die_on_error

        if self.session_id != self.session_instance.get_session_id():
            self.logger.error("BaseLFJsonRequest.session_id[%s] != session.get_session_id: [%s]"
                              % (self.session_id, self.session_instance.get_session_id()))
            if die_on_error:
                exit(1)
        responses: list = []  # p3.9 list[HTTPResponse]
        url = self.get_corrected_url(url)
        self.logger.by_method("url: "+url)
        if (post_data is not None) and (post_data is not self.No_Data):
            myrequest = request.Request(url=url,
                                        method=method_,
                                        data=json.dumps(post_data).encode("utf-8"),
                                        headers=self.default_headers)
        else:
            myrequest = request.Request(url=url,
                                        headers=self.default_headers,
                                        method=method_,
                                        data=post_data)
            self.logger.by_method("empty post sent to [%s]" % url)

        if not connection_timeout_sec:
            if self.session_instance.get_timeout_sec():
                connection_timeout_sec = self.session_instance.get_timeout_sec()
            else:
                connection_timeout_sec = 120
        if connection_timeout_sec:
            myrequest.timeout = connection_timeout_sec

        myrequest.headers['Content-type'] = 'application/json'
        sess_id = self.session_instance.get_session_id()
        if iss(sess_id):
            myrequest.headers[SESSION_HEADER] = str(sess_id)
        elif iss(session_id_):
            myrequest.headers[SESSION_HEADER] = str(session_id_)
        else:
            self.logger.warning("Request sent without X-LFJson-ID header: " + url)
        if debug:
            self.logger.by_method("headers sent to: " + url)
            self.logger.by_method(pformat(myrequest.headers))

        # https://stackoverflow.com/a/59635684/11014343

        response: http.client.HTTPResponse

        if wait_sec:
            time.sleep(wait_sec)
        begin_time_ms = time.time() * 1000
        if not max_timeout_sec:
            max_timeout_sec = self.session_instance.max_timeout_sec
        finish_time_ms = (max_timeout_sec * 1000) + begin_time_ms
        attempt = 1
        while (time.time() * 1000) < finish_time_ms:
            try:
                response = urllib.request.urlopen(myrequest)
                resp_data = response.read().decode('utf-8')
                jzon_data = None
                if debug and die_on_error:
                    self.logger.warning(__name__ +
                                        " ----- json_post: %d debug: --------------------------------------------" %
                                        attempt)
                    self.logger.warning("URL: %s :%d " % (url, response.status))
                    self.logger.warning(__name__ + " ----- headers -------------------------------------------------")
                    if response.status != 200:
                        self.logger.error(pformat(response.getheaders()))
                    self.logger.error(__name__ + " ----- response -------------------------------------------------")
                    self.logger.error(pformat(resp_data))
                    self.logger.error(" ----- -------------------------------------------------")
                responses.append(response)
                header_items = response.getheaders()
                if debug:
                    self.logger.by_method("BaseJsonRequest::json_post: response headers:")
                    self.logger.by_method(pformat(header_items))
                if SESSION_HEADER in header_items:
                    if self.session_id != response.getheader(SESSION_HEADER):
                        self.logger.warning("established session header [%s] different from response session header[%s]"
                                            % (self.session_id, response.getheader(SESSION_HEADER)))
                if errors_warnings:
                    for header in header_items:
                        if header[0].startswith("X-Error") == 0:
                            errors_warnings.append(header)
                        if header[0].startswith("X-Warning") == 0:
                            errors_warnings.append(header)

                if response_json_list is not None:
                    if type(response_json_list) is not list:
                        raise ValueError("reponse_json_list needs to be type list")
                    jzon_data = json.loads(resp_data)
                    if debug:
                        self.logger.debug(
                            __name__ + ":----- json_post debug: ------------------------------------------")
                        self.logger.debug("URL: %s :%d " % (url, response.status))
                        self.logger.debug(
                            __name__ + " ----- headers   -------------------------------------------------")
                        self.logger.debug(pformat(response.getheaders()))
                        self.logger.debug(
                            __name__ + " ----- response  -------------------------------------------------")
                        self.logger.debug(pformat(jzon_data))
                        self.logger.debug("-------------------------------------------------")
                    response_json_list.append(jzon_data)

                if response.status not in self.OK_STATUSES:
                    if errors_warnings:
                        if "errors" in jzon_data:
                            errors_warnings.extend(jzon_data["errors"])
                        if "warnings" in jzon_data:
                            errors_warnings.extend(jzon_data["warnings"])
                    self.logger.debug("----------------- BAD STATUS --------------------------------")
                    if die_on_error:
                        exit(1)
                return responses[0]

            except urllib.error.HTTPError as herror:
                print_diagnostics(url_=url,
                                  request_=myrequest,
                                  responses_=responses,
                                  error_=herror,
                                  debug_=debug,
                                  die_on_error_=die_on_error)
                if die_on_error:
                    exit(1)

            except urllib.error.URLError as uerror:
                print_diagnostics(url_=url,
                                  request_=myrequest,
                                  responses_=responses,
                                  error_=uerror,
                                  debug_=debug,
                                  die_on_error_=die_on_error)
                if die_on_error:
                    exit(1)

        if die_on_error:
            exit(1)
        return None

    def json_put(self,
                 url: str = None,
                 debug: bool = False,
                 wait_sec: float = None,
                 request_timeout_sec: float = None,
                 max_timeout_sec: float = None,
                 errors_warnings: list = None,
                 die_on_error: bool = False,
                 response_json_list: list = None) -> Optional:  # Optional[HTTPResponse]
        if not url:
            raise ValueError("json_put requires url")
        return self.json_post(url=url,
                              debug=debug | self.debug_on,
                              wait_sec=wait_sec,
                              connection_timeout_sec=request_timeout_sec,
                              max_timeout_sec=max_timeout_sec,
                              die_on_error=die_on_error | self.die_on_error,
                              response_json_list=response_json_list,
                              errors_warnings=errors_warnings,
                              method_='PUT')

    def json_delete(self,
                    url: str = None,
                    debug: bool = False,
                    die_on_error: bool = False,
                    wait_sec: float = None,
                    request_timeout_sec: float = None,
                    max_timeout_sec: float = None,
                    errors_warnings: list = None):
        """
        Perform a HTTP DELETE call
        :param url: fully qualified URL to request
        :param debug: turn on diagnostic info
        :param die_on_error: call exit if response is nither 100, 200, or 404
        :param wait_sec: time to pause before making call
        :param request_timeout_sec: time to override default request timeout
        :param max_timeout_sec: time after which to stop making more requests
        :param errors_warnings: provide a list into which API errors and warnings are placed
        :return: as get_as_json() returns (a native decoding of JSON document: dict, list, str, float or int)
        """
        if wait_sec and (wait_sec > 0):
            time.sleep(wait_sec)
        return self.get_as_json(url=url,
                                debug=debug | self.debug_on,
                                die_on_error=die_on_error,
                                request_timeout_sec=request_timeout_sec,
                                max_timeout_sec=max_timeout_sec,
                                method_='DELETE',
                                errors_warnings=errors_warnings)

    def get(self,
            url: str = None,
            debug: bool = False,
            die_on_error: bool = False,
            method_: str = 'GET',
            connection_timeout_sec: int = None) -> Optional:  # Optional[HTTPResponse]
        """
        Makes a HTTP GET request with specified timeout.
        :param url: Fully qualified URL to request
        :param debug: if true, print out diagnostic information
        :param die_on_error: call exit() if query fails to connect, is a 400 or 500 response status.
        Responses with 404 status are expected to be normal and will not cause an exit.
        :param method_: Override the HTTP METHOD. Please do not override.
        :param connection_timeout_sec: number of seconds to have an outstanding request
        :return: returns an urllib.response or None
        """
        debug |= self.debug_on
        die_on_error |= self.die_on_error

        if debug:
            self.logger.debug(message="%s url:[%s]" % (__name__, url))

        if not connection_timeout_sec:
            if self.session_instance.get_timeout_sec():
                connection_timeout_sec = self.session_instance.get_timeout_sec()
            else:
                connection_timeout_sec = 120

        requested_url = self.get_corrected_url(url,
                                               debug=debug | self.debug_on)
        myrequest = request.Request(url=requested_url,
                                    headers=self.default_headers,
                                    method=method_)
        if connection_timeout_sec:
            myrequest.timeout = connection_timeout_sec

        myresponses: list = []  # list[HTTPResponse]
        try:
            myresponses.append(request.urlopen(myrequest))
            return myresponses[0]

        except urllib.error.HTTPError as herror:
            print_diagnostics(url_=requested_url,
                              request_=myrequest,
                              responses_=myresponses,
                              error_=herror,
                              error_list_=self.error_list,
                              debug_=debug,
                              die_on_error_=die_on_error)
            if die_on_error:
                exit(1)
        except urllib.error.URLError as uerror:
            print_diagnostics(url_=requested_url,
                              request_=myrequest,
                              responses_=myresponses,
                              error_=uerror,
                              error_list_=self.error_list,
                              debug_=debug,
                              die_on_error_=die_on_error)
            if die_on_error:
                exit(1)
        if die_on_error:
            exit(1)
        return None

    def get_as_json(self,
                    url: str = None,
                    die_on_error: bool = False,
                    debug: bool = False,
                    wait_sec: float = None,
                    request_timeout_sec: float = None,
                    max_timeout_sec: float = None,  # TODO: use if we do retries
                    method_='GET',
                    errors_warnings: list = None):
        """
        :param url: url to do GET request on
        :param die_on_error:  exit immediate if result status is BAD RESPONSE
        :param debug: print diagnostic information about query
        :param wait_sec: wait before requesting
        :param request_timeout_sec: number of seconds to wait for a response
        :param method_: Overrides the HTTP method used. Please do not override.
        :param errors_warnings: if present, this list gets populated with errors and warnings from the result
        :param max_timeout_sec: if there is no response, this request can retry every request_timeout_sec
        :return: get response as a python object decoded from Json data
        This often is a dict, but it could be any primitive Python type such as str, int, float or list.
        """
        begin_sec = time.time() * 1000
        responses = []
        while (time.time() * 1000) < (begin_sec + max_timeout_sec):
            if wait_sec and (wait_sec > 0):
                time.sleep(wait_sec)
            responses = [self.get(url=url,
                                  debug=debug,
                                  die_on_error=die_on_error,
                                  connection_timeout_sec=request_timeout_sec,
                                  method_=method_)]
            if (len(responses) > 0) and responses[0]:
                break

        if responses[0] is None:
            if debug:
                self.logger.debug(message="No response from " + url)
            return None

        json_data = json.loads(responses[0].read().decode('utf-8'))
        if errors_warnings is not None:
            if "errors" in json_data:
                errors_warnings.extend(json_data["errors"])
            if "warnings" in responses[0]:
                errors_warnings.extend(json_data["warnings"])

        return json_data

    def json_get(self,
                 url: str = None,
                 debug: bool = False,
                 wait_sec: float = None,
                 request_timeout_sec: float = None,
                 max_timeout_sec: float = None,
                 errors_warnings: list = None):
        """
        Returns json record from GET request. This will retry until timeout_sec
        :param url: URL to make GET request to
        :param debug: print diagnostic information if true
        :param wait_sec: time to wait before making request, or waiting until you get a non-404 response
        :param request_timeout_sec: maximum time each request can take
        :param max_timeout_sec: maximum time to spend making requests
        :param errors_warnings: if present, fill this with error and warning messages from the response JSON
        :return: dictionary of json response from server
        """
        debug |= self.debug_on
        json_response = None
        if not max_timeout_sec:
            max_timeout_sec = self.session_instance.max_timeout_sec

        if nott(url):
            raise ValueError("json_get called withou url")

        url = self.get_corrected_url(url=url)

        deadline_sec: float = (_now_ms() * 1000) + max_timeout_sec
        self.error_list.clear()
        attempt_counter = 1
        while _now_sec() < deadline_sec:
            if wait_sec:
                time.sleep(wait_sec)
            try:
                json_response = self.get_as_json(url=url,
                                                 debug=debug,
                                                 die_on_error=False,
                                                 request_timeout_sec=request_timeout_sec,
                                                 max_timeout_sec=max_timeout_sec,
                                                 errors_warnings=errors_warnings)
                if debug:
                    self.logger.debug("[%s] json_get: URL[%s]" % (attempt_counter, url))
                    self.logger.debug(pformat(json_response))
                if json_response is None:
                    if errors_warnings:
                        errors_warnings.append("No json_response")
                        errors_warnings.extend(self.error_list)
                    if debug:
                        if hasattr(self, 'print_errors'):
                            self.print_errors()
                        else:
                            self.logger.error("json_get: [%s] no response, check other errors" % url)
                            time.sleep(wait_sec)
                    return None
                else:
                    return json_response
            except ValueError as ve:
                if debug or self.die_on_error:
                    self.logger.error("json_get: [%s] " % url)
                    self.logger.error("Exception %s:" % ve)
                    self.logger.error(traceback.format_exception(ValueError, ve, ve.__traceback__, chain=True))
                    # traceback.print_exception(ValueError, ve, ve.__traceback__, chain=True)
                if self.die_on_error:
                    sys.exit(1)
        return json_response

    # def set_post_data(self, data):
    #     """
    #     :param data: dictionary of parameters for post
    #     :return: nothing
    #     """
    #     self.post_data = data

    def has_errors(self):
        return (True, False)[len(self.error_list) > 0]

    def print_errors(self):
        if not self.has_errors:
            self.logger.debug("---------- no errors ----------")
            return
        for err in self.error_list:
            Logg.error("error: %s" % err)

    @staticmethod
    def create_port_eid_url(eid_list: list = None) -> str:
        """ ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        Convert a list of EIDs into a URL:
        :param eid_list
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- """
        if not len(eid_list):
            return "/list"
        url = "/"
        if isinstance(eid_list, str):
            return url + eid_list.replace('.', '/')

        # The first in a series has to define the resource number,
        # but the remainder of a series has to match that resource number
        for i in range(0, len(eid_list)):
            eid = eid_list[i]
            if i == 0:
                url += eid.replace('.', '/')
            elif eid.find('.') > 0:
                url += str(',' + eid.split('.')[-1])
            else:
                url += str(',' + eid)
        return url


class JsonQuery(BaseLFJsonRequest):
    """ ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        request LANforge JSON data with knowledge of the LANforge JSON headers
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- """

    def __init__(self,
                 session_obj: 'BaseSession' = None,
                 debug=False,
                 exit_on_error=False):
        super().__init__(session_obj=session_obj,
                         debug=debug | session_obj.is_debug(),
                         exit_on_error=exit_on_error)


class JsonCommand(BaseLFJsonRequest):
    def __init__(self,
                 session_obj: object = None,
                 debug: bool = False,
                 exit_on_error: bool = False):
        super().__init__(session_obj=session_obj,
                         debug=debug,
                         exit_on_error=exit_on_error)
        self.logger.debug("%s new instance " % str(__class__))

    @staticmethod
    def set_flags(flag_class: IntFlag, starting_value: int, flag_names=None):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        :param flag_class:     flag class, a subclass of IntFlag
        :param starting_value: integer flag value to OR values into
        :param flag_names:     list of flag names to convert to integers to OR onto starting_value

        Example Usage:
            value = LFJsonPost.add_flags(SetPortMumble, 0, flag_names=['bridge', 'dhcp'])
            print('value now: '+value)
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        if starting_value is None:
            raise ValueError("starting_value should be an integer greater or equal than zero, not None")
        if not flag_names:
            raise ValueError("flag_names should be a name or a list of names, not None")
        if type(flag_names) is list:
            selected_flags = []
            for flag in flag_names:
                if isinstance(flag, str):
                    if flag not in flag_class.__members__:
                        raise ValueError("%s lacks member:[%s]" %
                                         (flag_class.__class__.__name__, flag))
                    selected_flags.extend([flag_class[member].value
                                           for member in flag_class.__members__ if member == flag])
                if isinstance(flag, IntFlag):
                    if flag not in flag_class:
                        raise ValueError("%s lacks member:[%s]" %
                                         (flag_class.__class__.__name__, flag))
                    selected_flags.extend([member.value
                                           for member in flag_class.__members___ if member == flag])
            selected_flags.append(starting_value)
            result_flags = 0
            for i in selected_flags:
                result_flags |= i
            return result_flags
        f_name = None
        if type(flag_names) is str:
            f_name = flag_names
            print('f_name is str %s' % f_name)
        else:
            print('f_name is %s' % type(flag_names))
        if f_name not in flag_class.__members__:
            raise ValueError("%s lacks member:[%s]" %
                             (flag_class.__class__.__name__, f_name))
        return flag_class.valueof(f_name)

    @staticmethod
    def clear_flags(flag_class: IntFlag, starting_value: int, flag_names=None):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        :param flag_class:     flag class, a subclass of IntFlag
        :param starting_value: integer flag value to OR values into
        :param flag_names:     list of flag names to convert to integers to OR onto starting_value

        Example Usage:
            value = LFJsonPost.clear_flags(SetPortMumble, 0, flag_names=['bridge', 'dhcp'])
            print('value now: '+value)
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        if starting_value is None:
            raise ValueError("starting_value should be an integer greater than zero and not None")
        if not flag_names:
            raise ValueError("flag_names should be a name or a list of names, not None")
        unselected_val = None
        if type(flag_names) is list:
            unselected_val = starting_value
            for flag in flag_names:
                if isinstance(flag, str):
                    if flag not in flag_class.__members__:
                        raise ValueError("%s has no member:[%s]" % (flag_class.__class__.__name__, flag))
                if isinstance(flag, IntFlag):
                    if flag not in flag_class:
                        raise ValueError("%s has no member:[%s]" % (flag_class.__class__.__name__, flag))
                unselected_val &= ~flag.value
            # print("unselected b[%s]" % (hex(unselected_val)))
            return unselected_val
        if isinstance(flag_names, str):
            if flag_names not in flag_class.__members__:
                raise ValueError("%s lacks member:[%s]" %
                                 (flag_class.__class__.__name__, flag_names))
            unselected_val = starting_value
            unselected_val &= ~flag_class.valueof(flag_names)
        if isinstance(flag_names, IntFlag):
            if flag_names not in flag_class:
                raise ValueError("%s lacks member:[%s]" %
                                 (flag_class.__class__.__name__, flag_names))
            unselected_val = starting_value
            unselected_val &= ~flag_names.value
        return unselected_val

    def start_session(self,
                      debug: bool = False,
                      die_without_session_id_: bool = False) -> bool:
        responses = []
        debug |= self.debug_on
        if not self.session_instance:
            raise ValueError("JsonCommand::start_session lacks self.session_instance")

        first_response: HTTPResponse
        errors_warnings: list = []
        first_response = self.json_post(url="/newsession",
                                        debug=False,
                                        errors_warnings=errors_warnings,
                                        response_json_list=responses)
        if not first_response:
            self.logger.warning("No session established.")
            self.logger.debug(pformat(first_response))
            self.logger.debug(pformat(responses))
            self.logger.warning(pformat(errors_warnings))
            if die_without_session_id_:
                exit(1)
            return False
        # first_response.msg is HttpMessage not a string
        elif first_response.status != 200:
            self.logger.error("Error starting session msg: %s" % pformat(first_response.headers))
            self.logger.warning(pformat(errors_warnings))
            if die_without_session_id_:
                exit(1)
            return False

        if debug:
            self.logger.debug("%s: newsession: %s" % (__name__, pformat(first_response)))
        # self.session_instance.session_id = first_response["session_id"]
        self.logger.debug(pformat(("start_session headers:",
                                   first_response.getheaders())))
        if SESSION_HEADER not in first_response.headers:
            self.logger.error("start_session: no %s in response headers:" % SESSION_HEADER)
            self.logger.error(pformat(first_response.headers))
            self.logger.warning(pformat(errors_warnings))
            if die_without_session_id_:
                exit(1)
            return False

        self.session_id = first_response.getheader(SESSION_HEADER)
        self.session_instance.session_id = first_response.getheader(SESSION_HEADER)
        return True


class BaseSession:
    """
    Use this class to make your initial connection to a LANforge GUI. This class can
    will create a session id and hold errors and warnings as needed.
    """

    Default_Base_URL: str = "http://localhost:8080"
    Default_Retry_Sec: float = 1.0
    Default_Request_Timeout_Sec: float = 120.0
    Default_Max_Timeout_Sec: float = 240.0
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def __init__(self, lfclient_url: str = 'http://localhost:8080',
                 debug: bool = False,
                 proxy_map: dict = None,
                 connection_timeout_sec: float = Default_Request_Timeout_Sec,
                 max_timeout_sec: float = Default_Max_Timeout_Sec,
                 retry_sec: float = Default_Retry_Sec,
                 stream_errors: bool = True,
                 stream_warnings: bool = False,
                 exit_on_error: bool = False):
        self.debug_on = debug
        self.logger = Logg(name='json_api_session')
        if debug:
            self.logger.level = logging.DEBUG
        self.exit_on_error = exit_on_error
        self.command_instance: JsonCommand
        self.connection_timeout_sec: int = 10
        self.debug_on: bool
        self.debug_on = False
        self.exit_on_error: bool
        self.exit_on_error = False
        self.lfclient_url: str
        self.max_timeout_sec: float
        self.max_timeout_sec = max_timeout_sec
        self.proxies_installed: bool
        self.proxies_installed = False
        self.proxy_map: dict
        self.query_instance: JsonQuery
        self.query_instance = None
        self.retry_sec: float
        self.retry_sec = retry_sec
        self.session_error_list: list = []
        self.session_id: str
        self.session_id = None
        self.session_warnings_list: list = []
        self.stream_errors: bool
        self.stream_errors = True
        self.stream_warnings: bool
        self.stream_warnings = False
        self.session_connection_check: bool
        self.session_connection_check = False
        self.session_started_at: int = 0

        # please see this discussion on ProxyHandlers:
        # https://docs.python.org/3/library/urllib.request.html#urllib.request.ProxyHandler
        # but this makes much more sense:
        # https://gist.github.com/aleiphoenix/4159510

        if debug:
            if proxy_map is None:
                self.logger.debug("%s: no proxy_str" % __class__)
            else:
                self.logger.debug("BaseSession.__init__: proxies_: %s" % pformat(proxy_map))

        if (proxy_map is not None) and (len(proxy_map) > 0):
            if ("http" not in proxy_map) and ("https" not in proxy_map):
                raise ValueError("Neither http or https set in proxy definitions. Expects proxy={'http':, 'https':, }")
            self.proxy_map = proxy_map
        if (proxy_map is not None) and (len(proxy_map) > 0):
            opener = urllib.request.build_opener(request.ProxyHandler(proxy_map))
            urllib.request.install_opener(opener)
            self.proxies_installed = True

        if connection_timeout_sec:
            self.connection_timeout_sec = connection_timeout_sec
            self.logger.debug("%s connection timeout sec now [%f]" % (__name__, connection_timeout_sec))

        self.stream_errors = stream_errors
        self.stream_warnings = stream_warnings

        # if debug:
        #     if self.proxies is None:
        #         print("BaseSession _init_: no proxies")
        #     else:
        #         print("BaseSession _init_: proxies: ")
        #         pprint.pprint(self.proxies)

        if not lfclient_url.startswith("http://") and not lfclient_url.startswith("https://"):
            self.logger.warning("No http:// or https:// found, prepending http:// to " + lfclient_url)
            lfclient_url = "http://" + lfclient_url

        # we do not want the lfclient_url to end with a slash
        if lfclient_url.endswith('/'):
            self.lfclient_url = lfclient_url[0: len(lfclient_url) - 1]
        else:
            self.lfclient_url = lfclient_url

        # test connection with GUI to get a session id, then set our session ids in those instances
        # self.session_connection_check = self.command_instance.start_session(debug=debug)
        self.command_instance = None
        self.query_instance = None

    # indicate session destroyed if possible
    def __del__(self):
        if not self.session_connection_check:
            self.logger.warning("%s no connection established, exiting" % self.session_connection_check)
            return
        self.logger.debug("%s: asking for session %s to end" % (__name__, self.session_id))
        BaseSession.end_session(command_obj=self.command_instance,
                                session_id_=self.session_id,
                                debug=False)

    def get_command(self) -> 'JsonCommand':
        """
        Remember to override this method with your session subclass, it should return LFJsonCommand
        :return: registered instance of JsonCommand
        """
        if self.command_instance:
            return self.command_instance
        self.command_instance = JsonCommand(session_obj=self)
        return self.command_instance

    def get_query(self) -> 'JsonQuery':
        """
        Remember to override this method with your session subclass, it should return LFJsonQuery
        :return: registered instance of JsonQuery
        """
        if self.query_instance:
            return self.query_instance
        self.query_instance = JsonQuery(session_obj=self, debug=self.debug_on)
        return self.query_instance

    def is_exit_on_error(self) -> bool:
        return self.exit_on_error

    def get_lfclient_url(self) -> str:
        return self.lfclient_url

    def get_lf_client_error(self) -> str:
        return self.lfclient_url

    def is_debug(self) -> bool:
        return self.debug_on

    def get_session_id(self) -> str:
        return self.session_id

    def get_proxies(self):
        return self.proxy_map

    def get_timeout_sec(self) -> float:
        return self.connection_timeout_sec

    @classmethod
    def end_session(cls,
                    command_obj: JsonCommand = None,
                    session_id_: str = "",
                    debug: bool = False):
        responses = []
        command_obj.debug_on = False
        command_obj.json_post(url="endsession",
                              debug=debug,
                              response_json_list=responses,
                              session_id_=session_id_)

# End of json_api.py; subclasses defined below


class LFJsonCommand(JsonCommand):
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        LFJsonCommand inherits from JsonCommand
        Commands are used for POST requests.
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def __init__(self,
                 session_obj: object = None,
                 debug: bool = False,
                 exit_on_error: bool = False):
        super().__init__(session_obj=session_obj,
                         debug=debug,
                         exit_on_error=exit_on_error)

    # Auto generated methods follow: 

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_ARM_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_arm_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_arm_endp(self, 
                          alias: str = None,      # Name of endpoint. [R]
                          cpu_id: str = None,     # Preferred CPU ID on which this endpoint should run.
                          mx_pkt_sz: str = None,  # Maximum packet size, including all Ethernet headers.
                          pkt_sz: str = None,     # Minimum packet size, including all Ethernet headers.
                          port: str = None,       # Port number. [W]
                          pps: str = None,        # Packets per second to generate.
                          resource: int = None,   # Resource number. [W]
                          shelf: int = 1,         # Shelf name/id. Required. [R][D:1]
                          tos: str = None,        # The Type of Service, can be HEX. See set_endp_tos for details.
                          p_type: str = None,     # Endpoint Type : arm_udp. [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_arm_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if cpu_id is not None:
            data["cpu_id"] = cpu_id
        if mx_pkt_sz is not None:
            data["mx_pkt_sz"] = mx_pkt_sz
        if pkt_sz is not None:
            data["pkt_sz"] = pkt_sz
        if port is not None:
            data["port"] = port
        if pps is not None:
            data["pps"] = pps
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if tos is not None:
            data["tos"] = tos
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_arm_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_BGP_PEER> type requests

        https://www.candelatech.com/lfcli_ug.php#add_bgp_peer
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddBgpPeerFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddBgpPeerFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        ENABLE_PEER = 0x1             # Set this to zero if you don't want this peer enabled.
        PEER_CLIENT = 0x2             # Sets corresponding Xorp flag in BGP Peer section.
        PEER_CONFED_MEMBER = 0x4      # Sets corresponding Xorp flag in BGP Peer section.
        PEER_UNICAST_V4 = 0x8         # Sets corresponding Xorp flag in BGP Peer section.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddBgpPeerFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_bgp_peer(self, 
                          p_as: str = None,             # BGP Peer Autonomous System number, 0-65535
                          delay_open_time: str = None,  # BGP Peer delay open time.
                          flags: str = None,            # Virtual router BGP Peer flags, see above for definitions.
                          holdtime: str = None,         # BGP Peer hold-time.
                          local_dev: str = None,        # BGP Peer Local interface.
                          nexthop: str = None,          # BGP Peer Nexthop, IPv4 Address.
                          nexthop6: str = None,         # BGP Peer IPv6 Nexthop address.
                          peer_id: str = None,          # BGP Peer Identifier: IPv4 Address
                          peer_index: str = None,       # Peer index in this virtual router (0-7).
                          resource: int = None,         # Resource number. [W]
                          shelf: int = 1,               # Shelf name/id. [R][D:1]
                          vr_id: str = None,            # Name of virtual router. [R]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_bgp_peer(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if p_as is not None:
            data["as"] = p_as
        if delay_open_time is not None:
            data["delay_open_time"] = delay_open_time
        if flags is not None:
            data["flags"] = flags
        if holdtime is not None:
            data["holdtime"] = holdtime
        if local_dev is not None:
            data["local_dev"] = local_dev
        if nexthop is not None:
            data["nexthop"] = nexthop
        if nexthop6 is not None:
            data["nexthop6"] = nexthop6
        if peer_id is not None:
            data["peer_id"] = peer_id
        if peer_index is not None:
            data["peer_index"] = peer_index
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if vr_id is not None:
            data["vr_id"] = vr_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_bgp_peer",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_BOND> type requests

        https://www.candelatech.com/lfcli_ug.php#add_bond
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_bond(self, 
                      network_devs: str = None,  # Comma-separated list of network devices: eth1,eth2,eth3... [W]
                      port: str = None,          # Name of the bond device. [W]
                      resource: int = None,      # Resource number. [W]
                      shelf: int = 1,            # Shelf number. [R][D:1]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_bond(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if network_devs is not None:
            data["network_devs"] = network_devs
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_bond",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_BR> type requests

        https://www.candelatech.com/lfcli_ug.php#add_br
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddBrBrFlags(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        none = 0             # no features
        stp_enabled = 1      # Enable Spanning Tree Protocol (STP)

    def post_add_br(self, 
                    br_aging_time: str = None,        # MAC aging time, in seconds, 32-bit number.
                    br_flags: str = None,             # Bridge flags, see above.
                    br_forwarding_delay: str = None,  # How long to wait until the bridge will start forwarding packets.
                    br_hello_time: str = None,        # How often does the bridge send out STP hello packets.
                    br_max_age: str = None,           # How long until STP considers a non-responsive bridge dead.
                    br_priority: str = None,          # Bridge priority, 16-bit number.
                    network_devs: str = None,         # Comma-separated list of network devices: eth1,eth2,eth3...
                    port: str = None,                 # Name of the bridge device. [W]
                    resource: int = None,             # Resource number. [W]
                    shelf: int = 1,                   # Shelf number. [R][D:1]
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_br(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if br_aging_time is not None:
            data["br_aging_time"] = br_aging_time
        if br_flags is not None:
            data["br_flags"] = br_flags
        if br_forwarding_delay is not None:
            data["br_forwarding_delay"] = br_forwarding_delay
        if br_hello_time is not None:
            data["br_hello_time"] = br_hello_time
        if br_max_age is not None:
            data["br_max_age"] = br_max_age
        if br_priority is not None:
            data["br_priority"] = br_priority
        if network_devs is not None:
            data["network_devs"] = network_devs
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_br",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CD> type requests

        https://www.candelatech.com/lfcli_ug.php#add_cd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddCdFlags(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        ERR = 2          # Set to kernel mode.
        RUNNING = 1      # Set to running state.

    def post_add_cd(self, 
                    alias: str = None,         # Name of Collision Domain. [W]
                    bps: str = None,           # Maximum speed at which this collision domain can run.
                    flags: str = None,         # See above. Leave blank or use 'NA' for no default values.
                    report_timer: int = None,  # How often to report stats.
                    resource: int = None,      # Resource number. [W]
                    shelf: int = 1,            # Shelf name/id. [R][D:1]
                    state: str = None,         # RUNNING or STOPPED (default is RUNNING). Use this to start/stop.
                    p_type: str = None,        # CD Type: WIFI, WISER_SURFACE, WISER_SURFACE_AIR, WISER_AIR_AIR,
                    # WISER_NCW
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_cd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if bps is not None:
            data["bps"] = bps
        if flags is not None:
            data["flags"] = flags
        if report_timer is not None:
            data["report_timer"] = report_timer
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if state is not None:
            data["state"] = state
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_cd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CD_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_cd_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_cd_endp(self, 
                         cd: str = None,    # Name of Collision Domain. [R]
                         endp: str = None,  # Endpoint name/id. [R]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_cd_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cd is not None:
            data["cd"] = cd
        if endp is not None:
            data["endp"] = endp
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_cd_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CD_VR> type requests

        https://www.candelatech.com/lfcli_ug.php#add_cd_vr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_cd_vr(self, 
                       cd: str = None,  # Name of Collision Domain. [R]
                       vr: str = None,  # Virtual-Router name/ID. [R]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_cd_vr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cd is not None:
            data["cd"] = cd
        if vr is not None:
            data["vr"] = vr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_cd_vr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CHAMBER> type requests

        https://www.candelatech.com/lfcli_ug.php#add_chamber
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddChamberChamberFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddChamberChamberFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        OPEN = 0x4         # (3) Door is open, no real isolation right now.
        PHANTOM = 0x1      # (1) Chamber is not actually here right now.
        VIRTUAL = 0x2      # (2) No real chamber, open-air grouping of equipment.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddChamberChamberFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddChamberTurntableType(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddChamberTurntableType0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        COMXIM = 0x1      # ComXim stand-alone USB connected turn-table.
        CT840A = 0x2      # Modbus API turntable in CT840A 2D chamber.
        CT850A = 0x0      # TCP-IP Connected turntable in CT850A 2D chamber.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddChamberTurntableType has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_chamber(self, 
                         chamber_type: str = None,    # Chamber type, see above. Use 1 for Medium if uncertain. [W]
                         dut_name1: str = None,       # Name of first DUT in this chamber or NA
                         dut_name2: str = None,       # Name of second DUT in this chamber or NA
                         dut_name3: str = None,       # Name of third DUT in this chamber or NA
                         dut_name4: str = None,       # Name of fourth DUT in this chamber or NA
                         flags: str = None,           # Flag field for Chamber, see above. [W]
                         flags_mask: str = None,      # Mask of what flags to pay attention to, or NA for all.
                         height: str = None,          # Height to be used when drawn in the LANforge-GUI.
                         isolation: str = None,       # Estimated isolation in db for this chamber.
                         lanforge1: str = None,       # EID of first LANforge Resource in this chamber or NA
                         lanforge2: str = None,       # EID of second LANforge Resource in this chamber or NA
                         lanforge3: str = None,       # EID of third LANforge Resource in this chamber or NA
                         lanforge4: str = None,       # EID of fourth LANforge Resource in this chamber or NA
                         name: str = None,            # Name of Chamber, unique identifier. [R]
                         resource: int = None,        # LANforge Resource ID for controlling turn-table via serial
                         # protocol.
                         sma_count: str = None,       # Number of SMA connectors on this chamber, default is 16.
                         turntable_type: str = None,  # Turn-Table type: see above.
                         width: str = None,           # Width to be used when drawn in the LANforge-GUI.
                         x: str = None,               # X coordinate to be used when drawn in the LANforge-GUI.
                         y: str = None,               # Y coordinate to be used when drawn in the LANforge-GUI.
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_chamber(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if chamber_type is not None:
            data["chamber_type"] = chamber_type
        if dut_name1 is not None:
            data["dut_name1"] = dut_name1
        if dut_name2 is not None:
            data["dut_name2"] = dut_name2
        if dut_name3 is not None:
            data["dut_name3"] = dut_name3
        if dut_name4 is not None:
            data["dut_name4"] = dut_name4
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if height is not None:
            data["height"] = height
        if isolation is not None:
            data["isolation"] = isolation
        if lanforge1 is not None:
            data["lanforge1"] = lanforge1
        if lanforge2 is not None:
            data["lanforge2"] = lanforge2
        if lanforge3 is not None:
            data["lanforge3"] = lanforge3
        if lanforge4 is not None:
            data["lanforge4"] = lanforge4
        if name is not None:
            data["name"] = name
        if resource is not None:
            data["resource"] = resource
        if sma_count is not None:
            data["sma_count"] = sma_count
        if turntable_type is not None:
            data["turntable_type"] = turntable_type
        if width is not None:
            data["width"] = width
        if x is not None:
            data["x"] = x
        if y is not None:
            data["y"] = y
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_chamber",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CHAMBER_CX> type requests

        https://www.candelatech.com/lfcli_ug.php#add_chamber_cx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddChamberCxChamberCxFlags(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        CONNECTED = 1       # (1) Connected to something. If flag is not set, connection is open to the air
        # +(maybe with antenna)
        TERMINATED = 2      # (2) Connection is terminated, signal shall not pass!

    def post_add_chamber_cx(self, 
                            a_id: str = None,            # EidAntenna in string format for A side connection.
                            atten_id: str = None,        # EID for the Attenuator module if one is inline on this
                            # connection.
                            b_id: str = None,            # EidAntenna in string format for B side connection.
                            connection_idx: str = None,  # Connection index, currently up to 32 connections supported
                            # (0-31) [R]
                            flags: str = None,           # Flag field for Chamber Connection, see above.
                            flags_mask: str = None,      # Mask of what flags to pay attention to, or NA for all.
                            internal: str = None,        # Internal (1) or not (0): Internal connections are no longer
                            # supported.
                            min_atten: str = None,       # Specify minimum attenuation in 10ths of a db. Distance
                            # logic will not set atten below this.
                            name: str = None,            # Name of Chamber, unique identifier. [R]
                            zrssi2: str = None,          # Specify 2.4Ghz zero-attenuation RSSI in 10ths of a db.
                            # Distance logic will consider this in its calculations.
                            zrssi5: str = None,          # Specify 5Ghz zero-attenuation RSSI in 10ths of a db.
                            # Distance logic will consider this in its calculations.
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_chamber_cx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if a_id is not None:
            data["a_id"] = a_id
        if atten_id is not None:
            data["atten_id"] = atten_id
        if b_id is not None:
            data["b_id"] = b_id
        if connection_idx is not None:
            data["connection_idx"] = connection_idx
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if internal is not None:
            data["internal"] = internal
        if min_atten is not None:
            data["min_atten"] = min_atten
        if name is not None:
            data["name"] = name
        if zrssi2 is not None:
            data["zrssi2"] = zrssi2
        if zrssi5 is not None:
            data["zrssi5"] = zrssi5
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_chamber_cx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CHAMBER_PATH> type requests

        https://www.candelatech.com/lfcli_ug.php#add_chamber_path
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_chamber_path(self, 
                              chamber: str = None,  # Chamber Name. [R]
                              content: str = None,  # <tt>[BLANK]</tt> will erase all content, any other text will
                              # be appended to existing text.
                              path: str = None,     # Path Name [R]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_chamber_path(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if chamber is not None:
            data["chamber"] = chamber
        if content is not None:
            data["content"] = content
        if path is not None:
            data["path"] = path
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_chamber_path",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CHANNEL_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_channel_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddChannelGroupTypes(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        clear = "clear"          # Channel(s) are bundled into a single span. No conversion or
        e_m = "e&amp;m"          # Channel(s) are signalled using E&amp;M signalling (specific
        fcshdlc = "fcshdlc"      # The zapdel driver performs HDLC encoding and decoding on the
        fxogs = "fxogs"          # Channel(s) are signalled using FXO Groundstart protocol.
        fxoks = "fxoks"          # Channel(s) are signalled using FXO Koolstart protocol.
        fxols = "fxols"          # Channel(s) are signalled using FXO Loopstart protocol.
        fxsgs = "fxsgs"          # Channel(s) are signalled using FXS Groundstart protocol.
        fxsks = "fxsks"          # Channel(s) are signalled using FXS Koolstart protocol.
        fxsls = "fxsls"          # Channel(s) are signalled using FXS Loopstart protocol.
        indclear = "indclear"    # Like 'clear' except all channels are treated individually and
        nethdlc = "nethdlc"      # The zaptel driver bundles the channels together into an
        rawhdlc = "rawhdlc"      # The zaptel driver performs HDLC encoding and decoding on the
        unused = "unused"        # No signalling is performed, each channel in the list remains idle

    def post_add_channel_group(self, 
                               alias: str = None,      # Name for this Channel Group. [R]
                               channels: str = None,   # List of channels to add to this group.
                               idle_flag: str = None,  # Idle flag (byte) for this channel group, for instance:
                               # 0x7e
                               mtu: str = None,        # MTU (and MRU) for this channel group. Must be a multiple
                               # of the number of channels if configuring a T1 WanLink.
                               resource: int = None,   # Resource number. [W]
                               shelf: int = 1,         # Shelf name/id. [R][D:1]
                               span_num: str = None,   # The span number. First span is 1, second is 2... [W]
                               p_type: str = None,     # The channel-type. Use 'clear' for PPP links.
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_channel_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if channels is not None:
            data["channels"] = channels
        if idle_flag is not None:
            data["idle_flag"] = idle_flag
        if mtu is not None:
            data["mtu"] = mtu
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if span_num is not None:
            data["span_num"] = span_num
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_channel_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_CX> type requests

        https://www.candelatech.com/lfcli_ug.php#add_cx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_cx(self, 
                    alias: str = None,     # Name of the Cross Connect to create. [R]
                    rx_endp: str = None,   # Name of Receiving endpoint. [W]
                    test_mgr: str = None,  # Name of test-manager to create the CX on. [W][D:default_tm]
                    tx_endp: str = None,   # Name of Transmitting endpoint. [R]
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_cx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if rx_endp is not None:
            data["rx_endp"] = rx_endp
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if tx_endp is not None:
            data["tx_endp"] = tx_endp
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_cx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_DUT> type requests

        https://www.candelatech.com/lfcli_ug.php#add_dut
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddDutDutFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddDutDutFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_11r = 0x200            # Use .11r connection logic on all ssids, deprecated, see add_dut_ssid.
        AP_MODE = 0x2            # (2) DUT acts as AP.
        DHCPD_LAN = 0x40         # Provides DHCP server on LAN port
        DHCPD_WAN = 0x80         # Provides DHCP server on WAN port
        EAP_PEAP = 0x800         # Use EAP-PEAP connection logic on all ssids, deprecated, see add_dut_ssid.
        EAP_TTLS = 0x400         # Use EAP-TTLS connection logic on all ssids, deprecated, see add_dut_ssid.
        INACTIVE = 0x4           # (3) Ignore this in ChamberView, etc
        NOT_DHCPCD = 0x1000      # Station/edge device that is NOT using DHCP.
        STA_MODE = 0x1           # (1) DUT acts as Station.
        WEP = 0x8                # Use WEP encryption on all ssids, deprecated, see add_dut_ssid.
        WPA = 0x10               # Use WPA encryption on all ssids, deprecated, see add_dut_ssid.
        WPA2 = 0x20              # Use WPA2 encryption on all ssids, deprecated, see add_dut_ssid.
        WPA3 = 0x100             # Use WPA3 encryption on all ssids, deprecated, see add_dut_extras.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddDutDutFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_dut(self, 
                     antenna_count1: str = None,  # Antenna count for first radio.
                     antenna_count2: str = None,  # Antenna count for second radio.
                     antenna_count3: str = None,  # Antenna count for third radio.
                     api_id: str = None,          # DUT API Identifier (none specified yet)
                     bssid1: str = None,          # BSSID for first radio.
                     bssid2: str = None,          # BSSID for second radio.
                     bssid3: str = None,          # BSSID for third radio.
                     eap_id: str = None,          # EAP Identifier, for EAP-PEAP.
                     flags: str = None,           # Flag field for DUT, see above. [W]
                     flags_mask: str = None,      # Optional mask to specify what DUT flags are being set.
                     hw_version: str = None,      # DUT Hardware Version information
                     img_file: str = None,        # File-Name for image to represent DUT.
                     lan_port: str = None,        # IP/Mask for LAN port
                     mgt_ip: str = None,          # Management IP Address to access DUT
                     model_num: str = None,       # DUT Model information
                     name: str = None,            # Name of DUT, cannot contain '.' [R]
                     passwd1: str = None,         # WiFi Password that can be used to connect to DUT
                     passwd2: str = None,         # WiFi Password that can be used to connect to DUT
                     passwd3: str = None,         # WiFi Password that can be used to connect to DUT
                     serial_num: str = None,      # DUT Identifier (serial-number, etc)
                     serial_port: str = None,     # Resource and Serial port name on LANforge that connects to DUT
                     # (1.2.ttyS0).
                     ssid1: str = None,           # WiFi SSID that can be used to connect to DUT
                     ssid2: str = None,           # WiFi SSID that can be used to connect to DUT
                     ssid3: str = None,           # WiFi SSID that can be used to connect to DUT
                     sw_version: str = None,      # DUT Software Version information
                     top_left_x: str = None,      # X Location for Chamber View.
                     top_left_y: str = None,      # X Location for Chamber View.
                     wan_port: str = None,        # IP/Mask for WAN port
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_dut(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if antenna_count1 is not None:
            data["antenna_count1"] = antenna_count1
        if antenna_count2 is not None:
            data["antenna_count2"] = antenna_count2
        if antenna_count3 is not None:
            data["antenna_count3"] = antenna_count3
        if api_id is not None:
            data["api_id"] = api_id
        if bssid1 is not None:
            data["bssid1"] = bssid1
        if bssid2 is not None:
            data["bssid2"] = bssid2
        if bssid3 is not None:
            data["bssid3"] = bssid3
        if eap_id is not None:
            data["eap_id"] = eap_id
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if hw_version is not None:
            data["hw_version"] = hw_version
        if img_file is not None:
            data["img_file"] = img_file
        if lan_port is not None:
            data["lan_port"] = lan_port
        if mgt_ip is not None:
            data["mgt_ip"] = mgt_ip
        if model_num is not None:
            data["model_num"] = model_num
        if name is not None:
            data["name"] = name
        if passwd1 is not None:
            data["passwd1"] = passwd1
        if passwd2 is not None:
            data["passwd2"] = passwd2
        if passwd3 is not None:
            data["passwd3"] = passwd3
        if serial_num is not None:
            data["serial_num"] = serial_num
        if serial_port is not None:
            data["serial_port"] = serial_port
        if ssid1 is not None:
            data["ssid1"] = ssid1
        if ssid2 is not None:
            data["ssid2"] = ssid2
        if ssid3 is not None:
            data["ssid3"] = ssid3
        if sw_version is not None:
            data["sw_version"] = sw_version
        if top_left_x is not None:
            data["top_left_x"] = top_left_x
        if top_left_y is not None:
            data["top_left_y"] = top_left_y
        if wan_port is not None:
            data["wan_port"] = wan_port
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_dut",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_DUT_NOTES> type requests

        https://www.candelatech.com/lfcli_ug.php#add_dut_notes
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_dut_notes(self, 
                           dut: str = None,   # DUT Name. [R]
                           text: str = None,  # [BLANK] will erase all, any other text will be appended to
                           # existing text.
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_dut_notes(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if dut is not None:
            data["dut"] = dut
        if text is not None:
            data["text"] = text
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_dut_notes",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_DUT_SSID> type requests

        https://www.candelatech.com/lfcli_ug.php#add_dut_ssid
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddDutSsidDutFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddDutSsidDutFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_11r = 0x200          # Use .11r connection logic
        EAP_PEAP = 0x800       # Use EAP-PEAP connection logic
        EAP_TTLS = 0x400       # Use EAP-TTLS connection logic
        WEP = 0x8              # Use WEP encryption
        WPA = 0x10             # Use WPA encryption
        WPA2 = 0x20            # Use WPA2 encryption
        WPA3 = 0x100           # Use WPA3 encryption

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddDutSsidDutFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_dut_ssid(self, 
                          bssid: str = None,            # BSSID for cooresponding SSID.
                          name: str = None,             # Name of DUT, cannot contain '.' [R]
                          passwd: str = None,           # WiFi Password that can be used to connect to DUT
                          ssid: str = None,             # WiFi SSID that can be used to connect to DUT
                          ssid_flags: str = None,       # SSID flags, see above.
                          ssid_flags_mask: str = None,  # SSID flags mask
                          ssid_idx: str = None,         # Index of the SSID. Zero-based indexing: (0 - 7) [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_dut_ssid(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if bssid is not None:
            data["bssid"] = bssid
        if name is not None:
            data["name"] = name
        if passwd is not None:
            data["passwd"] = passwd
        if ssid is not None:
            data["ssid"] = ssid
        if ssid_flags is not None:
            data["ssid_flags"] = ssid_flags
        if ssid_flags_mask is not None:
            data["ssid_flags_mask"] = ssid_flags_mask
        if ssid_idx is not None:
            data["ssid_idx"] = ssid_idx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_dut_ssid",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddEndpPayloadPattern(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        PRBS_11_8_10 = "PRBS_11_8_10"    # PRBS (see above)
        PRBS_15_0_14 = "PRBS_15_0_14"    # PRBS (see above)
        PRBS_4_0_3 = "PRBS_4_0_3"        # Use linear feedback shift register to generate pseudo random sequence.
        PRBS_7_0_6 = "PRBS_7_0_6"        # PRBS (see above)
        custom = "custom"                # Enter your own payload with the set_endp_payload cmd.
        decreasing = "decreasing"        # bytes start at FF and decrease, wrapping if needed
        increasing = "increasing"        # bytes start at 00 and increase, wrapping if needed
        ones = "ones"                    # payload is all ones (FF)
        random = "random"                # generate a new random payload each time sent
        random_fixed = "random_fixed"    # means generate one random payload, and send it over and over again.
        zeros = "zeros"                  # payload is all zeros (00)

    class AddEndpType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        custom_ether = "custom_ether"      # LF frames with custom options, use with playback
        custom_mc_udp = "custom_mc_udp"    # LF Multicast UDP IPv4
        custom_tcp = "custom_tcp"          # LF TCP IPv4 frame with custom options
        custom_udp = "custom_udp"          # LF UDP IPv4 frame with custom options
        lf = "lf"                          # LF protocol
        lf_sctp = "lf_sctp"                # SCTP IPv4 protocol
        lf_sctp6 = "lf_sctp6"              # SCTP IPv6 protocol
        lf_tcp = "lf_tcp"                  # TCP IPv4 connection
        lf_tcp6 = "lf_tcp6"                # TCP IPv6 connection
        lf_udp = "lf_udp"                  # UDP IPv4 connection
        lf_udp6 = "lf_udp6"                # UDP IPv6 connection
        mc_udp = "mc_udp"                  # LF Multicast IPv4

    def post_add_endp(self, 
                      alias: str = None,                     # Name of endpoint. [R]
                      ip_port: str = None,                   # IP Port: IP port for layer three endpoints. Use -1 to let
                      # the LANforge server automatically configure the ip_port.
                      # Layer 2 endpoints will ignore
                      is_pkt_sz_random: str = None,          # Yes means use random sized packets, anything else means NO.
                      is_rate_bursty: str = None,            # Yes means bursty, anything else means NO.
                      max_pkt: str = None,                   # Maximum packet size, including all headers. 0 means 'same',
                      # -1 means AUTO (5.3.2+) [D:0]
                      max_rate: str = None,                  # Maximum transmit rate (bps), used if in bursty mode.
                      min_pkt: str = None,                   # Minimum packet size, including all headers. -1 means AUTO
                      # (5.3.2+) [W][D:-1]
                      min_rate: str = None,                  # Minimum transmit rate (bps), or only rate if not bursty. [W]
                      multi_conn: str = None,                # If > 0, will create separate process with this many
                      # connections per endpoint. See AUTO_HELPER flag
                      payload_pattern: str = None,           # Payload pattern, see above.
                      port: str = None,                      # Port/Interface name or number. [R]
                      resource: int = None,                  # Resource number. [W]
                      send_bad_crc_per_million: str = None,  # If NIC supports it, will randomly send X per million packets
                      # with bad ethernet Frame Check Sum.
                      shelf: int = 1,                        # Shelf name/id. [R][D:1]
                      ttl: str = None,                       # Time-to-live, used by UDP Multicast Endpoints only.
                      p_type: str = None,                    # Endpoint Type: See above. [W]
                      use_checksum: str = None,              # Yes means checksum the payload, anything else means NO.
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if ip_port is not None:
            data["ip_port"] = ip_port
        if is_pkt_sz_random is not None:
            data["is_pkt_sz_random"] = is_pkt_sz_random
        if is_rate_bursty is not None:
            data["is_rate_bursty"] = is_rate_bursty
        if max_pkt is not None:
            data["max_pkt"] = max_pkt
        if max_rate is not None:
            data["max_rate"] = max_rate
        if min_pkt is not None:
            data["min_pkt"] = min_pkt
        if min_rate is not None:
            data["min_rate"] = min_rate
        if multi_conn is not None:
            data["multi_conn"] = multi_conn
        if payload_pattern is not None:
            data["payload_pattern"] = payload_pattern
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if send_bad_crc_per_million is not None:
            data["send_bad_crc_per_million"] = send_bad_crc_per_million
        if shelf is not None:
            data["shelf"] = shelf
        if ttl is not None:
            data["ttl"] = ttl
        if p_type is not None:
            data["type"] = p_type
        if use_checksum is not None:
            data["use_checksum"] = use_checksum
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_EVENT> type requests

        https://www.candelatech.com/lfcli_ug.php#add_event
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_event(self, 
                       details: str = None,   # Event text description. Cannot include double-quote characters. [R]
                       event_id: str = None,  # Numeric ID for the event to modify, or 'new' if creating a new one.
                       # [W][D:new]
                       name: str = None,      # Event entity name.
                       priority: str = None,  # See set_event_priority for available priorities.
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_event(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if details is not None:
            data["details"] = details
        if event_id is not None:
            data["event_id"] = event_id
        if name is not None:
            data["name"] = name
        if priority is not None:
            data["priority"] = priority
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_event",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_FILE_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_file_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddFileEndpFioFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddFileEndpFioFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        AUTO_MOUNT = 0x2          # (2) Attempt to mount with the provided information if not already mounted.
        AUTO_UNMOUNT = 0x4        # (4) Attempt to un-mount when stopping test.
        CHECK_MOUNT = 0x1         # (1) Attempt to verify NFS and SMB mounts match the configured values.
        O_APPEND = 0x200          # (512) Open files for writing with O_APPEND instead
        O_DIRECT = 0x8            # (8) Open file with O_DIRECT flag, disables caching. Must use block-size
        # +read/write calls.
        O_LARGEFILE = 0x20        # (32) Open files with O_LARGEFILE. This allows greater than 2GB files on
        # +32-bit systems.
        UNLINK_BW = 0x10          # (16) Unlink file before writing. This works around issues with CIFS for some
        # +file-servers.
        UNMOUNT_FORCE = 0x40      # (64) Use -f flag when calling umount
        UNMOUNT_LAZY = 0x80       # (128) Use -l flag when calling umount
        USE_FSTATFS = 0x100       # (256) Use fstatfs system call to verify file-system type when opening files.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddFileEndpFioFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddFileEndpPayloadPattern(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        PRBS_11_8_10 = "PRBS_11_8_10"    # PRBS (see above)
        PRBS_15_0_14 = "PRBS_15_0_14"    # PRBS (see above)
        PRBS_4_0_3 = "PRBS_4_0_3"        # Use linear feedback shift register to generate pseudo random sequence.
        PRBS_7_0_6 = "PRBS_7_0_6"        # PRBS (see above)
        custom = "custom"                # Enter your own payload with the set_endp_payload cmd.
        decreasing = "decreasing"        # bytes start at FF and decrease, wrapping if needed.
        increasing = "increasing"        # bytes start at 00 and increase, wrapping if needed.
        ones = "ones"                    # Payload is all ones (FF).
        random = "random"                # generate a new random payload each time sent.
        random_fixed = "random_fixed"    # Means generate one random payload, and send it over
        zeros = "zeros"                  # Payload is all zeros (00).

    class AddFileEndpType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        fe_cifs = "fe_cifs"              # Does a CIFS (Samba) mount
        fe_cifs_ip6 = "fe_cifs/ip6"      # Does an IPv6 CIFS mount
        fe_generic = "fe_generic"        # Uses unspecified file protocol
        fe_iscsi = "fe_iscsi"            # Does a ISCSI mount
        fe_nfs = "fe_nfs"                # Does an NFSv3 mount
        fe_nfs_ip6 = "fe_nfs/ip6"        # Does a NFSv3 IPv6 mount
        fe_nfs4 = "fe_nfs4"              # Does an NFSv4 mount
        fe_nfs4_ip6 = "fe_nfs4/ip6"      # Does a NFSv4 IPv6 mount
        fe_smb2 = "fe_smb2"              # Does a SMB v2.0 mount
        fe_smb2_ip6 = "fe_smb2/ip6"      # Does a SMB v2.0 IPv6 mount
        fe_smb21 = "fe_smb21"            # Does a SMB v2.1 mount
        fe_smb21_ip6 = "fe_smb21/ip6"    # Does a SMB v2.1 IPv6 mount
        fe_smb30 = "fe_smb30"            # Does a SMB v3.0 mount
        fe_smb30_ip6 = "fe_smb30/ip6"    # Does a SMB v3.0 IPv6 mount

    def post_add_file_endp(self, 
                           alias: str = None,            # Name of endpoint. [R]
                           directory: str = None,        # The directory to read/write in. Absolute path suggested.
                           # [W]
                           fio_flags: str = None,        # File-IO flags, see above for details.
                           max_read_rate: str = None,    # Maximum read rate, bits-per-second.
                           max_write_rate: str = None,   # Maximum write rate, bits-per-second.
                           min_read_rate: str = None,    # Minimum read rate, bits-per-second.
                           min_write_rate: str = None,   # Minimum write rate, bits-per-second.
                           mount_dir: str = None,        # Directory to mount/unmount (if blank, will use
                           # 'directory').
                           mount_options: str = None,    # Optional mount options, passed to the mount command. 'NONE'
                           # clears.
                           payload_pattern: str = None,  # Payload pattern, see above.
                           port: str = None,             # Port number. [W]
                           prefix: str = None,           # The prefix of the file(s) to read/write.
                           resource: int = None,         # Resource number. [W]
                           retry_timer: str = None,      # Number of miliseconds to retry errored IO calls before
                           # giving up.
                           server_mount: str = None,     # The server to mount, ex:
                           # <tt>192.168.100.5/exports/test1</tt> [W]
                           shelf: int = 1,               # Shelf name/id. [R][D:1]
                           p_type: str = None,           # Endpoint Type (like <tt>fe_nfs</tt>) [W]
                           volume: str = None,           # iSCSI volume to mount
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_file_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if directory is not None:
            data["directory"] = directory
        if fio_flags is not None:
            data["fio_flags"] = fio_flags
        if max_read_rate is not None:
            data["max_read_rate"] = max_read_rate
        if max_write_rate is not None:
            data["max_write_rate"] = max_write_rate
        if min_read_rate is not None:
            data["min_read_rate"] = min_read_rate
        if min_write_rate is not None:
            data["min_write_rate"] = min_write_rate
        if mount_dir is not None:
            data["mount_dir"] = mount_dir
        if mount_options is not None:
            data["mount_options"] = mount_options
        if payload_pattern is not None:
            data["payload_pattern"] = payload_pattern
        if port is not None:
            data["port"] = port
        if prefix is not None:
            data["prefix"] = prefix
        if resource is not None:
            data["resource"] = resource
        if retry_timer is not None:
            data["retry_timer"] = retry_timer
        if server_mount is not None:
            data["server_mount"] = server_mount
        if shelf is not None:
            data["shelf"] = shelf
        if p_type is not None:
            data["type"] = p_type
        if volume is not None:
            data["volume"] = volume
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_file_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_GEN_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_gen_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_gen_endp(self, 
                          alias: str = None,     # Name of endpoint. [R]
                          port: str = None,      # Port number. [W]
                          resource: int = None,  # Resource number. [W]
                          shelf: int = 1,        # Shelf name/id. [R][D:1]
                          p_type: str = None,    # Endpoint Type : gen_generic [W][D:gen_generic]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_gen_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_gen_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_GRE> type requests

        https://www.candelatech.com/lfcli_ug.php#add_gre
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_gre(self, 
                     local_lower_ip: str = None,   # The local lower-level IP to use.
                     port: str = None,             # Name of the GRE to create, suggested to start with 'gre' [W]
                     remote_lower_ip: str = None,  # The remote lower-level IP to use.
                     report_timer: int = None,     # Report timer for this port, leave blank or use NA for defaults.
                     resource: int = None,         # Resource number. [W]
                     shelf: int = 1,               # Shelf number. [R][D:1]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_gre(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if local_lower_ip is not None:
            data["local_lower_ip"] = local_lower_ip
        if port is not None:
            data["port"] = port
        if remote_lower_ip is not None:
            data["remote_lower_ip"] = remote_lower_ip
        if report_timer is not None:
            data["report_timer"] = report_timer
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_gre",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddGroupFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddGroupFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        group_total_rates = 0x4      # Set rates as total for group.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddGroupFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_group(self, 
                       flags: str = None,       # Flags for this group, see above.
                       flags_mask: str = None,  # Mask for flags that we care about, use 0xFFFFFFFF or leave blank
                       # for all.
                       name: str = None,        # The name of the test group. Must be unique across all groups. [R]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_L4_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_l4_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddL4EndpHttpAuthType(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddL4EndpHttpAuthType0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BASIC = 0x1             # Basic authentication
        DIGEST = 0x2            # Digest (MD5) authentication
        GSSNEGOTIATE = 0x4      # GSS authentication
        NTLM = 0x8              # NTLM authentication

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddL4EndpHttpAuthType has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddL4EndpProxyAuthType(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddL4EndpProxyAuthType0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BASIC = 0x1                          # 1 Basic authentication
        BIND_DNS = 0x200                     # 512 Make DNS requests go out endpoints Port.
        DIGEST = 0x2                         # 2 Digest (MD5) authentication
        DISABLE_EPSV = 0x1000                # 4096 Disable FTP EPSV option
        DISABLE_PASV = 0x800                 # 2048 Disable FTP PASV option (will use PORT command)
        GSSNEGOTIATE = 0x4                   # 4 GSS authentication
        INCLUDE_HEADERS = 0x100              # 256 especially for IMAP
        NTLM = 0x8                           # 8 NTLM authentication
        USE_DEFLATE_COMPRESSION = 0x80       # 128 Use deflate compression
        USE_GZIP_COMPRESSION = 0x40          # 64 Use gzip compression
        USE_IPV6 = 0x400                     # 1024 Resolve URL is IPv6. Will use IPv4 if not selected.
        USE_PROXY_CACHE = 0x20               # 32 Use proxy cache

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddL4EndpProxyAuthType has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddL4EndpType(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddL4EndpType0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        l4_generic = 0x0      # Layer 4 type

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddL4EndpType has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_l4_endp(self, 
                         alias: str = None,              # Name of endpoint. [R]
                         block_size: str = None,         # TFTP Block size, in bytes.
                         dns_cache_timeout: str = None,  # In seconds, how long to cache DNS lookups. 0 means no
                         # caching at all.
                         http_auth_type: str = None,     # Bit-field for allowable http-authenticate methods.
                         ip_addr: str = None,            # Local IP address, for binding to specific secondary IP.
                         max_speed: str = None,          # In bits-per-second, can rate limit upload or download speed
                         # of the URL contents. 0 means infinite.
                         port: str = None,               # Port number. [W]
                         proxy_auth_type: str = None,    # Bit-field for allowable proxy-authenticate methods.
                         proxy_port: str = None,         # HTTP Proxy port if you are using a proxy.
                         proxy_server: str = None,       # The name of our proxy server if using one.
                         proxy_userpwd: str = None,      # The user-name and password for proxy authentication, format:
                         # <tt>user:passwd</tt>.
                         quiesce_after: str = None,      # Quiesce test after this many URLs have been processed.
                         resource: int = None,           # Resource number. [W]
                         shelf: int = 1,                 # Shelf name/id. [R][D:1]
                         smtp_from: str = None,          # SMTP From address.
                         ssl_cert_fname: str = None,     # Name of SSL Certs file.
                         timeout: str = None,            # How long to wait for a connection, in milliseconds
                         p_type: str = None,             # Endpoint Type : <tt>l4_generic</tt> [W]
                         url: str = None,                # The URL, see syntax above. Can also be a local file.
                         url_rate: str = None,           # How often should we process the URL(s), per 10
                         # minutes.<ul><li>600: 1/s<li>1200: 2/s<li>1800: 3/s<li>2400:
                         # 4/s</ul> [R][D:600]
                         user_agent: str = None,         # User-Agent string. Leave blank for default. Also SMTP-TO:
                         # &lt;a@b.com&gt;&lt;c@d.com&gt;...&lt;q@x.com&gt;
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_l4_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if block_size is not None:
            data["block_size"] = block_size
        if dns_cache_timeout is not None:
            data["dns_cache_timeout"] = dns_cache_timeout
        if http_auth_type is not None:
            data["http_auth_type"] = http_auth_type
        if ip_addr is not None:
            data["ip_addr"] = ip_addr
        if max_speed is not None:
            data["max_speed"] = max_speed
        if port is not None:
            data["port"] = port
        if proxy_auth_type is not None:
            data["proxy_auth_type"] = proxy_auth_type
        if proxy_port is not None:
            data["proxy_port"] = proxy_port
        if proxy_server is not None:
            data["proxy_server"] = proxy_server
        if proxy_userpwd is not None:
            data["proxy_userpwd"] = proxy_userpwd
        if quiesce_after is not None:
            data["quiesce_after"] = quiesce_after
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if smtp_from is not None:
            data["smtp_from"] = smtp_from
        if ssl_cert_fname is not None:
            data["ssl_cert_fname"] = ssl_cert_fname
        if timeout is not None:
            data["timeout"] = timeout
        if p_type is not None:
            data["type"] = p_type
        if url is not None:
            data["url"] = url
        if url_rate is not None:
            data["url_rate"] = url_rate
        if user_agent is not None:
            data["user_agent"] = user_agent
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_l4_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_MONITOR> type requests

        https://www.candelatech.com/lfcli_ug.php#add_monitor
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddMonitorFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddMonitorFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        disable_ht40 = 0x800             # Disable HT-40 even if hardware and AP support it.
        disable_ht80 = 0x8000000         # Disable HT80 (for AC chipset NICs only)
        ht160_enable = 0x100000000       # Enable HT160 mode.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddMonitorFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_monitor(self, 
                         aid: str = None,         # AID, may be used when sniffing on /AX radios.
                         ap_name: str = None,     # Name for this Monitor interface, for example: moni0 [W]
                         bssid: str = None,       # BSSID to use when sniffing on /AX radios, optional.
                         flags: str = None,       # Flags for this monitor interface.
                         flags_mask: str = None,  # Flags mask for this monitor interface.
                         radio: str = None,       # Name of the physical radio interface, for example: wiphy0 [W]
                         resource: int = None,    # Resource number. [W]
                         shelf: int = 1,          # Shelf number. [R][D:1]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_monitor(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aid is not None:
            data["aid"] = aid
        if ap_name is not None:
            data["ap_name"] = ap_name
        if bssid is not None:
            data["bssid"] = bssid
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if radio is not None:
            data["radio"] = radio
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_monitor",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_MVLAN> type requests

        https://www.candelatech.com/lfcli_ug.php#add_mvlan
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_mvlan(self, 
                       flags: str = None,         # 0x1: Create admin-down.
                       index: str = None,         # Optional: The index of the VLAN, (the <b>4</b> in
                       # <tt>eth0#4</tt>)
                       mac: str = None,           # The MAC address, can also use parent-pattern in 5.3.8 and higher:
                       # <tt>xx:xx:xx:*:*:xx</tt> [W]
                       old_name: str = None,      # The temporary name, used for configuring un-discovered hardware.
                       port: str = None,          # Port number of an existing Ethernet interface. [W]
                       report_timer: int = None,  # Report timer for this port, leave blank or use NA for defaults.
                       resource: int = None,      # Resource number. [W]
                       shelf: int = 1,            # Shelf number. [R][D:1]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_mvlan(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if flags is not None:
            data["flags"] = flags
        if index is not None:
            data["index"] = index
        if mac is not None:
            data["mac"] = mac
        if old_name is not None:
            data["old_name"] = old_name
        if port is not None:
            data["port"] = port
        if report_timer is not None:
            data["report_timer"] = report_timer
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_mvlan",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_PPP_LINK> type requests

        https://www.candelatech.com/lfcli_ug.php#add_ppp_link
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_ppp_link(self, 
                          auth: str = None,                  # YES if you want to authenticate. Default is NO.
                          channel_groups: str = None,        # List of channel groups, see above.
                          p_debug: bool = False,             # YES for debug, otherwise debugging for the ppp connection
                          # is off.
                          down_time_max_ms: str = None,      # Maximum length of downtime (ms) for PPP link between runs,
                          # or 0 for the link to be always up.
                          down_time_min_ms: str = None,      # Minimum length of downtime (ms) for PPP link between runs,
                          # or 0 for the link to be always up.
                          dst_ip: str = None,                # Destination IP address for this PPP connection.
                          extra_args: str = None,            # Extra arguments to be passed directly to the pppd server.
                          holdoff: str = None,               # Seconds between attempt to bring link back up if it dies,
                          # suggest 1.
                          lcp_echo_failure: str = None,      # LCP echo failures before we determine links is dead,
                          # suggest 5.
                          lcp_echo_interval: str = None,     # Seconds between LCP echos, suggest 1.
                          mlppp_descriptor: str = None,      # A unique key for use with multi-link PPP connections.
                          persist: str = None,               # YES if you want to persist the connection. This is
                          # suggested.
                          pppoe_transport_port: str = None,  # Port number (or name) for underlying PPPoE transport.
                          resource: int = None,              # Resource (machine) number. [W]
                          run_time_max_ms: str = None,       # Maximum uptime (ms) for PPP link during an experiment, or
                          # 0 for the link to be always up.
                          run_time_min_ms: str = None,       # Minimum uptime (ms) for PPP link during an experiment, or
                          # 0 for the link to be always up.
                          shelf: int = 1,                    # Shelf name/id. [R]
                          src_ip: str = None,                # Source IP address for this PPP connection.
                          transport_type: str = None,        # What sort of transport this ppp link uses.
                          tty_transport_device: str = None,  # TTY device for PPP links associated with TTYs.
                          unit: str = None,                  # Unit number for the PPP link. ie, the 7 in ppp7. [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_ppp_link(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if auth is not None:
            data["auth"] = auth
        if channel_groups is not None:
            data["channel_groups"] = channel_groups
        if p_debug is not None:
            data["debug"] = p_debug
        if down_time_max_ms is not None:
            data["down_time_max_ms"] = down_time_max_ms
        if down_time_min_ms is not None:
            data["down_time_min_ms"] = down_time_min_ms
        if dst_ip is not None:
            data["dst_ip"] = dst_ip
        if extra_args is not None:
            data["extra_args"] = extra_args
        if holdoff is not None:
            data["holdoff"] = holdoff
        if lcp_echo_failure is not None:
            data["lcp_echo_failure"] = lcp_echo_failure
        if lcp_echo_interval is not None:
            data["lcp_echo_interval"] = lcp_echo_interval
        if mlppp_descriptor is not None:
            data["mlppp_descriptor"] = mlppp_descriptor
        if persist is not None:
            data["persist"] = persist
        if pppoe_transport_port is not None:
            data["pppoe_transport_port"] = pppoe_transport_port
        if resource is not None:
            data["resource"] = resource
        if run_time_max_ms is not None:
            data["run_time_max_ms"] = run_time_max_ms
        if run_time_min_ms is not None:
            data["run_time_min_ms"] = run_time_min_ms
        if shelf is not None:
            data["shelf"] = shelf
        if src_ip is not None:
            data["src_ip"] = src_ip
        if transport_type is not None:
            data["transport_type"] = transport_type
        if tty_transport_device is not None:
            data["tty_transport_device"] = tty_transport_device
        if unit is not None:
            data["unit"] = unit
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_ppp_link",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_PROFILE> type requests

        https://www.candelatech.com/lfcli_ug.php#add_profile
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddProfileProfileFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddProfileProfileFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_11r = 0x40               # Use 802.11r roaming setup.
        ALLOW_11W = 0x800          # Set 11w (MFP/PMF) to optional.
        BSS_TRANS = 0x400          # Enable BSS Transition logic
        DHCP_SERVER = 0x1          # This should provide DHCP server.
        EAP_PEAP = 0x200           # Enable EAP-PEAP
        EAP_TTLS = 0x80            # Use 802.1x EAP-TTLS
        NAT = 0x100                # Enable NAT if this object is in a virtual router
        SKIP_DHCP_ROAM = 0x10      # Ask station to not re-do DHCP on roam.
        WEP = 0x2                  # Use WEP encryption
        WPA = 0x4                  # Use WPA encryption
        WPA2 = 0x8                 # Use WPA2 encryption
        WPA3 = 0x20                # Use WPA3 encryption

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddProfileProfileFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddProfileWifiMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_802_11a = "802.11a"        # 802.11a
        AUTO = "AUTO"                # 802.11g
        aAX = "aAX"                  # 802.11a-AX (6E disables /n and /ac)
        abg = "abg"                  # 802.11abg
        abgn = "abgn"                # 802.11abgn
        abgnAC = "abgnAC"            # 802.11abgn-AC
        abgnAX = "abgnAX"            # 802.11abgn-AX
        an = "an"                    # 802.11an
        anAC = "anAC"                # 802.11an-AC
        anAX = "anAX"                # 802.11an-AX
        as_is = "as_is"              # Make no changes to current configuration
        b = "b"                      # 802.11b
        bg = "bg"                    # 802.11bg
        bgn = "bgn"                  # 802.11bgn
        bgnAC = "bgnAC"              # 802.11bgn-AC
        bgnAX = "bgnAX"              # 802.11bgn-AX
        bond = "bond"                # Bonded pair of Ethernet ports.
        bridged_ap = "bridged_ap"    # AP device in bridged mode. The EIDs may specify radio and bridged port.
        client = "client"            # Client-side non-WiFi device (Ethernet port, for instance).
        g = "g"                      # 802.11g
        mobile_sta = "mobile_sta"    # Mobile station device. Expects to connect to DUT AP(s) and upstream
        # +LANforge.
        monitor = "monitor"          # Monitor device/sniffer. The EIDs may specify which radios to use.
        peer = "peer"                # Edge device, client or server (Ethernet port, for instance).
        rdd = "rdd"                  # Pair of redirect devices, typically associated with VR to act as traffic
        # +endpoint
        routed_ap = "routed_ap"      # AP in routed mode. The EIDs may specify radio and upstream port.
        sta = "sta"                  # Station device, most likely non mobile. The EIDs may specify radio(s) to
        # +use.
        uplink = "uplink"            # Uplink towards rest of network (can go in virtual router and do NAT)
        upstream = "upstream"        # Upstream server device. The EIDs may specify which ports to use.
        vlan = "vlan"                # 802.1q VLAN. Specify VID with the 'freq' option.

    def post_add_profile(self, 
                         alias_prefix: str = None,    # Port alias prefix, aka hostname prefix.
                         antenna: str = None,         # Antenna count for this profile.
                         bandwidth: str = None,       # 0 (auto), 20, 40, 80 or 160
                         eap_id: str = None,          # EAP Identifier
                         flags_mask: str = None,      # Specify what flags to set.
                         freq: str = None,            # WiFi frequency to be used, 0 means default.
                         instance_count: str = None,  # Number of devices (stations, vdevs, etc)
                         mac_pattern: str = None,     # Optional MAC-Address pattern, for instance: xx:xx:xx:*:*:xx
                         name: str = None,            # Profile Name. [R]
                         passwd: str = None,          # WiFi Password to be used (AP Mode), [BLANK] means no password.
                         profile_flags: str = None,   # Flags for this profile, see above.
                         profile_type: str = None,    # Profile type: See above. [W]
                         ssid: str = None,            # WiFi SSID to be used, [BLANK] means any.
                         vid: str = None,             # Vlan-ID (only valid for vlan profiles).
                         wifi_mode: str = None,       # WiFi Mode for this profile.
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_profile(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias_prefix is not None:
            data["alias_prefix"] = alias_prefix
        if antenna is not None:
            data["antenna"] = antenna
        if bandwidth is not None:
            data["bandwidth"] = bandwidth
        if eap_id is not None:
            data["eap_id"] = eap_id
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if freq is not None:
            data["freq"] = freq
        if instance_count is not None:
            data["instance_count"] = instance_count
        if mac_pattern is not None:
            data["mac_pattern"] = mac_pattern
        if name is not None:
            data["name"] = name
        if passwd is not None:
            data["passwd"] = passwd
        if profile_flags is not None:
            data["profile_flags"] = profile_flags
        if profile_type is not None:
            data["profile_type"] = profile_type
        if ssid is not None:
            data["ssid"] = ssid
        if vid is not None:
            data["vid"] = vid
        if wifi_mode is not None:
            data["wifi_mode"] = wifi_mode
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_profile",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_PROFILE_NOTES> type requests

        https://www.candelatech.com/lfcli_ug.php#add_profile_notes
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_profile_notes(self, 
                               dut: str = None,   # Profile Name. [R]
                               text: str = None,  # [BLANK] will erase all, any other text will be appended to
                               # existing text. <tt escapearg='false'>Unescaped Value</tt>
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_profile_notes(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if dut is not None:
            data["dut"] = dut
        if text is not None:
            data["text"] = text
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_profile_notes",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_RDD> type requests

        https://www.candelatech.com/lfcli_ug.php#add_rdd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_rdd(self, 
                     peer_ifname: str = None,   # The peer (other) RedirectDevice in this pair.
                     port: str = None,          # Name of the Redirect Device to create. [W]
                     report_timer: int = None,  # Report timer for this port, leave blank or use NA for defaults.
                     resource: int = None,      # Resource number. [W]
                     shelf: int = 1,            # Shelf number. [R][D:1]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_rdd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if peer_ifname is not None:
            data["peer_ifname"] = peer_ifname
        if port is not None:
            data["port"] = port
        if report_timer is not None:
            data["report_timer"] = report_timer
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_rdd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_SEC_IP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_sec_ip
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_sec_ip(self, 
                        ip_list: str = None,   # IP1/prefix,IP2/prefix,...IPZ/prefix. [W]
                        port: str = None,      # Name of network device (Port) to which these IPs will be added.
                        # [W]
                        resource: int = None,  # Resource number. [W]
                        shelf: int = 1,        # Shelf number. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_sec_ip(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ip_list is not None:
            data["ip_list"] = ip_list
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_sec_ip",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_STA> type requests

        https://www.candelatech.com/lfcli_ug.php#add_sta
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddStaFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddStaFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_80211r_pmska_cache = 0x4000000          # Enable oportunistic PMSKA caching for WPA2 (Related to
        # +802.11r).
        p_80211u_additional = 0x100000            # AP requires additional step for access (802.11u Interworking)
        p_80211u_auto = 0x40000                   # Enable 802.11u (Interworking) Auto-internetworking feature.
        # +Always enabled currently.
        p_80211u_e911 = 0x200000                  # AP claims emergency services reachable (802.11u Interworking)
        p_80211u_e911_unauth = 0x400000           # AP provides Unauthenticated emergency services (802.11u
        # +Interworking)
        p_80211u_enable = 0x20000                 # Enable 802.11u (Interworking) feature.
        p_80211u_gw = 0x80000                     # AP Provides access to internet (802.11u Interworking)
        p_8021x_radius = 0x2000000                # Use 802.1x (RADIUS for AP).
        create_admin_down = 0x1000000000          # Station should be created admin-down.
        custom_conf = 0x20                        # Use Custom wpa_supplicant config file.
        disable_obss_scan = 0x400000000000        # Disable OBSS SCAN feature in supplicant.
        disable_ofdma = 0x200000000000            # Disable OFDMA mode
        disable_twt = 0x100000000000              # Disable TWT mode
        disable_fast_reauth = 0x200000000         # Disable fast_reauth option for virtual stations.
        disable_gdaf = 0x1000000                  # AP: Disable DGAF (used by HotSpot 2.0).
        disable_ht80 = 0x8000000                  # Disable HT80 (for AC chipset NICs only)
        disable_roam = 0x80000000                 # Disable automatic station roaming based on scan results.
        disable_sgi = 0x4000                      # Disable SGI (Short Guard Interval).
        hs20_enable = 0x800000                    # Enable Hotspot 2.0 (HS20) feature. Requires WPA-2.
        ht160_enable = 0x100000000                # Enable HT160 mode.
        ht40_disable = 0x800                      # Disable HT-40 even if hardware and AP support it.
        ibss_mode = 0x20000000                    # Station should be in IBSS mode.
        lf_sta_migrate = 0x8000                   # OK-To-Migrate (Allow station migration between LANforge
        # +radios)
        mesh_mode = 0x400000000                   # Station should be in MESH mode.
        no_supp_op_class_ie = 0x4000000000        # Do not include supported-oper-class-IE in assoc requests. May
        # +work around AP bugs.
        osen_enable = 0x40000000                  # Enable OSEN protocol (OSU Server-only Authentication)
        passive_scan = 0x2000                     # Use passive scanning (don't send probe requests).
        power_save_enable = 0x800000000           # Station should enable power-save. May not work in all
        # +drivers/configurations.
        scan_ssid = 0x1000                        # Enable SCAN-SSID flag in wpa_supplicant.
        txo_enable = 0x8000000000                 # Enable/disable tx-offloads, typically managed by set_wifi_txo
        # +command
        use_bss_transition = 0x80000000000        # Enable BSS transition.
        use_wpa3 = 0x10000000000                  # Enable WPA-3 (SAE Personal) mode.
        verbose = 0x10000                         # Verbose-Debug: Increase debug info in wpa-supplicant and
        # +hostapd logs.
        wds_mode = 0x2000000000                   # WDS station (sort of like a lame mesh), not supported on
        # +ath10k
        wep_enable = 0x200                        # Use wpa_supplicant configured for WEP encryption.
        wpa2_enable = 0x400                       # Use wpa_supplicant configured for WPA2 encryption.
        wpa_enable = 0x10                         # Enable WPA

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddStaFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddStaMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_802_11a = 1      # 802.11a
        AUTO = 0           # 802.11g
        aAX = 15           # 802.11a-AX (6E disables /n and /ac)
        abg = 4            # 802.11abg
        abgn = 5           # 802.11abgn
        abgnAC = 8         # 802.11abgn-AC
        abgnAX = 12        # 802.11abgn-AX
        an = 10            # 802.11an
        anAC = 9           # 802.11an-AC
        anAX = 14          # 802.11an-AX
        b = 2              # 802.11b
        bg = 7             # 802.11bg
        bgn = 6            # 802.11bgn
        bgnAC = 11         # 802.11bgn-AC
        bgnAX = 13         # 802.11bgn-AX
        g = 3              # 802.11g

    class AddStaRate(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_a_g = "/a/g"            # 6 Mbps, 9 Mbps, 12 Mbps, 18 Mbps, 24 Mbps, 36 Mbps, 48 Mbps, 54 Mbps
        p_b = "/b"                # 1Mbps, 2Mbps, 5.5 Mbps, 11 Mbps
        DEFAULT = "DEFAULT"       # Use maximum available speed
        MCS0_76 = "MCS0-76"       # /n rates
        p_bitmap_ = "[bitmap]"    # <b>'0xff 00 ...'</b> to directly specify the MCS bitmap.

    def post_add_sta(self, 
                     ampdu_density: str = None,  # 0-7, or 0xFF to not set.
                     ampdu_factor: str = None,   # 0-3, or 0xFF to not set.
                     ap: str = None,             # The Access Point BSSID this Virtual STA should be associated with
                     flags: str = None,          # Flags for this interface (see above.) [W]
                     flags_mask: str = None,     # If set, only these flags will be considered.
                     ieee80211w: str = None,     # Management Frame Protection: 0: disabled, 1: optional, 2:
                     # Required.
                     key: str = None,            # Encryption key (WEP, WPA, WPA2, WPA3, etc) for this Virtual STA.
                     # Prepend with 0x for ascii-hex input.
                     mac: str = None,            # The MAC address, can also use parent-pattern in 5.3.8 and higher:
                     # <tt>xx:xx:xx:*:*:xx</tt> [W]
                     max_amsdu: str = None,      # 1 == enabled, 0 == disabled, 0xFF == do not set.
                     mode: str = None,           # WiFi mode: <ul><li>0: AUTO, <li>1: 802.11a</li> <li>2: b</li>
                     # <li>3: g</li> <li>4: abg</li> <li>5: abgn</li> <li>6: bgn</li>
                     # <li>7: bg</li> <li>8: abgnAC</li> <li>9 anAC</li> <li>10
                     # an</li><li>11 bgnAC</li><li>12 abgnAX</li><li>13 bgnAX</li><li>14
                     # anAX</li><li>15 aAX</li></ul> [D:0]
                     nickname: str = None,       # Nickname for this Virtual STA. (No longer used)
                     radio: str = None,          # Name of the physical radio interface, for example: wiphy0 [W]
                     rate: str = None,           # Max rate, see help above.
                     resource: int = None,       # Resource number. [W]
                     shelf: int = 1,             # Shelf number. [R][D:1]
                     ssid: str = None,           # SSID for this Virtual STA. Use [BLANK] for empty SSID. Start with
                     # <tt>0x</tt> for HEX interpretation. [W]
                     sta_br_ip: str = None,      # IP Address for station bridging. Set to 0.0.0.0 to use MAC
                     # bridging.
                     sta_name: str = None,       # Name for this Virtual STA, for example: sta0 [W]
                     wpa_cfg_file: str = None,   # WPA Supplicant config file.
                     x_coord: str = None,        # Floating point number.
                     y_coord: str = None,        # Floating point number.
                     z_coord: str = None,        # Floating point number.
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_sta(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ampdu_density is not None:
            data["ampdu_density"] = ampdu_density
        if ampdu_factor is not None:
            data["ampdu_factor"] = ampdu_factor
        if ap is not None:
            data["ap"] = ap
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if ieee80211w is not None:
            data["ieee80211w"] = ieee80211w
        if key is not None:
            data["key"] = key
        if mac is not None:
            data["mac"] = mac
        if max_amsdu is not None:
            data["max_amsdu"] = max_amsdu
        if mode is not None:
            data["mode"] = mode
        if nickname is not None:
            data["nickname"] = nickname
        if radio is not None:
            data["radio"] = radio
        if rate is not None:
            data["rate"] = rate
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if ssid is not None:
            data["ssid"] = ssid
        if sta_br_ip is not None:
            data["sta_br_ip"] = sta_br_ip
        if sta_name is not None:
            data["sta_name"] = sta_name
        if wpa_cfg_file is not None:
            data["wpa_cfg_file"] = wpa_cfg_file
        if x_coord is not None:
            data["x_coord"] = x_coord
        if y_coord is not None:
            data["y_coord"] = y_coord
        if z_coord is not None:
            data["z_coord"] = z_coord
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_sta",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_T1_SPAN> type requests

        https://www.candelatech.com/lfcli_ug.php#add_t1_span
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddT1SpanBuildout(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_15db = 6        # -15db (CSU)
        p_22_5db = 7      # -22.5db (CSU)
        p_7_5db = 5       # -7.5db (CSU)
        p_0db = 8         # 0db (CSU)
        p_133_ft = 0      # 1-133 feet
        p_266_ft = 1      # 122-266 feet
        p_399_ft = 2      # 266-399 feet
        p_533_ft = 3      # 399-533 feet
        p_655_ft = 4      # 533-655 feet

    class AddT1SpanType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        Digium_T1 = "Digium_T1"      #
        Sangoma_E1 = "Sangoma_E1"    #
        Sangoma_T1 = "Sangoma_T1"    #

    def post_add_t1_span(self, 
                         buildout: str = None,       # Buildout, Integer, see above.
                         coding: str = None,         # Coding: T1: ami or b8zs. E1: ami or hdb3
                         cpu_id: str = None,         # CPU identifier (A, B, etc) for multiport Sangoma resources.
                         first_channel: str = None,  # The first DS0 channel for this span.
                         framing: str = None,        # Framing: T1: esf or d4. E1: cas or ccs.
                         mtu: str = None,            # MTU for this span (used by in-band management, if at all).
                         pci_bus: str = None,        # PCI Bus number, needed for Sangoma resources.
                         pci_slot: str = None,       # PCI slot number, needed for Sangoma resources.
                         resource: int = None,       # Resource number. [W]
                         shelf: int = 1,             # Shelf name/id. [R][D:1]
                         span_num: str = None,       # The span number. First span is 1, second is 2... [W]
                         timing: str = None,         # Timing: 0 == do not use, 1 == primary, 2 == secondary..
                         p_type: str = None,         # Currently supported types listed above. [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_t1_span(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if buildout is not None:
            data["buildout"] = buildout
        if coding is not None:
            data["coding"] = coding
        if cpu_id is not None:
            data["cpu_id"] = cpu_id
        if first_channel is not None:
            data["first_channel"] = first_channel
        if framing is not None:
            data["framing"] = framing
        if mtu is not None:
            data["mtu"] = mtu
        if pci_bus is not None:
            data["pci_bus"] = pci_bus
        if pci_slot is not None:
            data["pci_slot"] = pci_slot
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if span_num is not None:
            data["span_num"] = span_num
        if timing is not None:
            data["timing"] = timing
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_t1_span",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_TEXT_BLOB> type requests

        https://www.candelatech.com/lfcli_ug.php#add_text_blob
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_text_blob(self, 
                           name: str = None,  # Text name, for instance '2-AP-test-case' [R]
                           text: str = None,  # [BLANK] will erase all, any other text will be appended to
                           # existing text. <tt escapearg='false'>Unescaped Value</tt>
                           p_type: str = None,  # Text type identifier stream, for instance 'cv-connectivity' [R]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_text_blob(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if text is not None:
            data["text"] = text
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_text_blob",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_TGCX> type requests

        https://www.candelatech.com/lfcli_ug.php#add_tgcx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_tgcx(self, 
                      cxname: str = None,  # The name of the CX. [R]
                      tgname: str = None,  # The name of the test group. [R]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_tgcx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cxname is not None:
            data["cxname"] = cxname
        if tgname is not None:
            data["tgname"] = tgname
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_tgcx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_THRESHOLD> type requests

        https://www.candelatech.com/lfcli_ug.php#add_threshold
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddThresholdThreshId(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        Delete_Marked = -3      # Delete any marked.
        Mark_All = -2           # Mark all

    class AddThresholdThreshType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NO_RX_SINCE = 6              # Have not received any bytes/packets in specified time.
        RX_BPS_RATE_OOR_1m = 5       # rx-bps over last 1 minute is out of range.
        RX_BPS_RATE_OOR_30S = 3      # rx-bps over last 30 seconds is out of range.
        RX_BPS_RATE_OOR_3S = 1       # rx-bps over last 3 seconds is out of range.
        TT_RX_DROP_OOR = 8           # RX Drop percentage is out of range (per-million).
        TT_RX_LAT_OOR = 7            # Latency running-average out of range.
        TX_BPS_RATE_OOR_1m = 4       # tx-bps over last 1 minute is out of range.
        TX_BPS_RATE_OOR_30S = 2      # tx-bps over last 30 seconds is out of range.
        TX_BPS_RATE_OOR_3S = 0       # tx-bps over last 3 seconds is out of range.

    def post_add_threshold(self, 
                           endp: str = None,         # Endpoint name or ID. [R]
                           thresh_id: str = None,    # Threshold ID. If adding new threshold, use -1, otherwise use
                           # correct ID. [W]
                           thresh_max: str = None,   # Maximum acceptable value for this threshold.
                           thresh_min: str = None,   # Minimum acceptable value for this threshold.
                           thresh_type: str = None,  # Threshold type, integer, (see above).
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_threshold(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp is not None:
            data["endp"] = endp
        if thresh_id is not None:
            data["thresh_id"] = thresh_id
        if thresh_max is not None:
            data["thresh_max"] = thresh_max
        if thresh_min is not None:
            data["thresh_min"] = thresh_min
        if thresh_type is not None:
            data["thresh_type"] = thresh_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_threshold",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_TM> type requests

        https://www.candelatech.com/lfcli_ug.php#add_tm
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_tm(self, 
                    name: str = None,  # The name of the test manager. Must be unique across test managers. [R]
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_tm(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_tm",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_TRAFFIC_PROFILE> type requests

        https://www.candelatech.com/lfcli_ug.php#add_traffic_profile
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddTrafficProfileTrafficProfileFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddTrafficProfileTrafficProfileFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BI_DIRECTIONAL = 0x2      # Should we do bi-directional traffic?
        IPERF_UDP = 0x4           # If Iperf, should use UDP. If not set, then will use TCP.
        UP = 0x1                  # Upload direction (this not set means download)

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddTrafficProfileTrafficProfileFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddTrafficProfileWifiMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        Iperf3_Client = "Iperf3-Client"    # iperf3 client
        Iperf3_Server = "Iperf3-Server"    # iperf3 server
        as_is = "as_is"                    # Make no changes to current configuration
        http = "http"                      # Not yet implemented
        https = "https"                    # Not yet implemented
        tcp = "tcp"                        #
        udp = "udp"                        #

    def post_add_traffic_profile(self, 
                                 instance_count: str = None,              # Number of connections per device
                                 max_pdu: str = None,                     # Minimum PDU size
                                 max_speed: str = None,                   # Opposite-Direction Speed in bps.
                                 min_pdu: str = None,                     # Minimum PDU size
                                 min_speed: str = None,                   # Opposite-Direction Speed in bps.
                                 name: str = None,                        # Profile Name. [R]
                                 tos: str = None,                         # IP Type-of-Service
                                 traffic_profile_flags: str = None,       # Flags for this profile, none defined at this
                                 # point.
                                 traffic_profile_flags_mask: str = None,  # Specify what flags to set.
                                 p_type: str = None,                      # Profile type: See above. [W]
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_traffic_profile(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if instance_count is not None:
            data["instance_count"] = instance_count
        if max_pdu is not None:
            data["max_pdu"] = max_pdu
        if max_speed is not None:
            data["max_speed"] = max_speed
        if min_pdu is not None:
            data["min_pdu"] = min_pdu
        if min_speed is not None:
            data["min_speed"] = min_speed
        if name is not None:
            data["name"] = name
        if tos is not None:
            data["tos"] = tos
        if traffic_profile_flags is not None:
            data["traffic_profile_flags"] = traffic_profile_flags
        if traffic_profile_flags_mask is not None:
            data["traffic_profile_flags_mask"] = traffic_profile_flags_mask
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_traffic_profile",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_TRAFFIC_PROFILE_NOTES> type requests

        https://www.candelatech.com/lfcli_ug.php#add_traffic_profile_notes
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_traffic_profile_notes(self, 
                                       dut: str = None,   # Profile Name. [R]
                                       text: str = None,  # [BLANK] will erase all, any other text will be
                                       # appended to existing text. <tt
                                       # escapearg='false'>Unescaped Value</tt>
                                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_traffic_profile_notes(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if dut is not None:
            data["dut"] = dut
        if text is not None:
            data["text"] = text
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_traffic_profile_notes",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VAP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_vap
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddVapFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddVapFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_80211h_enable = 0x10000000              # Enable 802.11h (needed for running on DFS channels) Requires
        # +802.11d.
        p_80211r_pmska_cache = 0x4000000          # Enable oportunistic PMSKA caching for WPA2 (Related to
        # +802.11r).
        p_80211u_additional = 0x100000            # AP requires additional step for access (802.11u Interworking)
        p_80211u_auto = 0x40000                   # Enable 802.11u (Interworking) Auto-internetworking feature.
        # +Always enabled currently.
        p_80211u_e911 = 0x200000                  # AP claims emergency services reachable (802.11u Interworking)
        p_80211u_e911_unauth = 0x400000           # AP provides Unauthenticated emergency services (802.11u
        # +Interworking)
        p_80211u_enable = 0x20000                 # Enable 802.11u (Interworking) feature.
        p_80211u_gw = 0x80000                     # AP Provides access to internet (802.11u Interworking)
        p_8021x_radius = 0x2000000                # Use 802.1x (RADIUS for AP).
        create_admin_down = 0x1000000000          # Station should be created admin-down.
        disable_dgaf = 0x1000000                  # AP Disable DGAF (used by HotSpot 2.0).
        disable_ht40 = 0x800                      # Disable HT-40 (will use HT-20 if available).
        disable_ht80 = 0x8000000                  # Disable HT80 (for AC chipset NICs only)
        enable_80211d = 0x40                      # Enable 802.11D to broadcast country-code &amp; channels in
        # +VAPs
        enable_wpa = 0x10                         # Enable WPA
        hostapd_config = 0x20                     # Use Custom hostapd config file.
        hs20_enable = 0x800000                    # Enable Hotspot 2.0 (HS20) feature. Requires WPA-2.
        ht160_enable = 0x100000000                # Enable HT160 mode.
        osen_enable = 0x40000000                  # Enable OSEN protocol (OSU Server-only Authentication)
        pri_sec_ch_enable = 0x100                 # Enable Primary/Secondary channel switch.
        short_preamble = 0x80                     # Allow short-preamble
        use_bss_load = 0x20000000000              # Enable BSS Load IE in Beacons and Probe Responses (.11e).
        use_bss_transition = 0x80000000000        # Enable BSS transition.
        use_rrm_report = 0x40000000000            # Enable Radio measurements IE in beacon and probe responses.
        use_wpa3 = 0x10000000000                  # Enable WPA-3 (SAE Personal) mode.
        verbose = 0x10000                         # Verbose-Debug: Increase debug info in wpa-supplicant and
        # +hostapd logs.
        wep_enable = 0x200                        # Enable WEP Encryption
        wpa2_enable = 0x400                       # Enable WPA2 Encryption

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddVapFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddVapMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_802_11a = 1      # 802.11a
        AUTO = 0           # 802.11g
        aAX = 15           # 802.11a-AX (6E disables /n and /ac)
        abg = 4            # 802.11abg
        abgn = 5           # 802.11abgn
        abgnAC = 8         # 802.11abgn-AC
        abgnAX = 12        # 802.11abgn-AX
        an = 10            # 802.11an
        anAC = 9           # 802.11an-AC
        anAX = 14          # 802.11an-AX
        b = 2              # 802.11b
        bg = 7             # 802.11bg
        bgn = 6            # 802.11bgn
        bgnAC = 11         # 802.11bgn-AC
        bgnAX = 13         # 802.11bgn-AX
        g = 3              # 802.11g

    def post_add_vap(self, 
                     ap_name: str = None,      # Name for this Virtual AP, for example: vap0 [W]
                     beacon: str = None,       # The beacon interval, in 1kus (1.024 ms), default 100, range:
                     # 15..65535
                     custom_cfg: str = None,   # Custom hostapd config file, if you want to craft your own config.
                     dtim_period: str = None,  # DTIM period, range 1..255. Default 2.
                     flags: str = None,        # Flags for this interface (see above.) [W]
                     flags_mask: str = None,   # If set, only these flags will be considered.
                     frag_thresh: str = None,  # UN-USED, Was Fragmentation threshold, which is now set with
                     # set_wifi_radio, use NA [W]
                     ieee80211w: str = None,   # Management Frame Protection: 0: disabled, 1: optional, 2: Required.
                     key: str = None,          # Encryption key for this Virtual AP. Prepend with 0x for ascii-hex
                     # representation.
                     mac: str = None,          # The MAC address, can also use parent-pattern in 5.3.8 and higher:
                     # <tt>xx:xx:xx:*:*:xx</tt>
                     max_sta: str = None,      # Maximum number of Stations allowed to join this AP (1..2007)
                     mode: str = None,         # WiFi mode: see table [W]
                     radio: str = None,        # Name of the physical radio interface, for example: wiphy0 [W]
                     rate: str = None,         # Max rate, see help for add_vsta
                     resource: int = None,     # Resource number. [W]
                     shelf: int = 1,           # Shelf number. [R][D:1]
                     ssid: str = None,         # SSID for this Virtual AP. [W]
                     x_coord: str = None,      # Floating point number.
                     y_coord: str = None,      # Floating point number.
                     z_coord: str = None,      # Floating point number.
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_vap(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ap_name is not None:
            data["ap_name"] = ap_name
        if beacon is not None:
            data["beacon"] = beacon
        if custom_cfg is not None:
            data["custom_cfg"] = custom_cfg
        if dtim_period is not None:
            data["dtim_period"] = dtim_period
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if frag_thresh is not None:
            data["frag_thresh"] = frag_thresh
        if ieee80211w is not None:
            data["ieee80211w"] = ieee80211w
        if key is not None:
            data["key"] = key
        if mac is not None:
            data["mac"] = mac
        if max_sta is not None:
            data["max_sta"] = max_sta
        if mode is not None:
            data["mode"] = mode
        if radio is not None:
            data["radio"] = radio
        if rate is not None:
            data["rate"] = rate
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if ssid is not None:
            data["ssid"] = ssid
        if x_coord is not None:
            data["x_coord"] = x_coord
        if y_coord is not None:
            data["y_coord"] = y_coord
        if z_coord is not None:
            data["z_coord"] = z_coord
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_vap",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VENUE> type requests

        https://www.candelatech.com/lfcli_ug.php#add_venue
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddVenueFreq24(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddVenueFreq240, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        ALL = 0xffff       # ALL
        Ch_1 = 0x1         # Channel 1
        Ch_2 = 0x2         # Channel 2
        Ch_3 = 0x4         # Channel 3

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddVenueFreq24 has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class AddVenueFreq5(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddVenueFreq50, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        Ch_100 = 0x800           # Channel 100 5500
        Ch_104 = 0x1000          # Channel 104 5520
        Ch_108 = 0x2000          # Channel 108 5540
        Ch_112 = 0x4000          # Channel 112 5560
        Ch_116 = 0x8000          # Channel 116 5580
        Ch_120 = 0x10000         # Channel 120 5600
        Ch_124 = 0x20000         # Channel 124 5620
        Ch_128 = 0x40000         # Channel 128 5640
        Ch_132 = 0x80000         # Channel 132 5660
        Ch_136 = 0x100000        # Channel 136 5680
        Ch_140 = 0x200000        # Channel 140 5700
        Ch_149 = 0x400000        # Channel 149 5745
        Ch_153 = 0x800000        # Channel 153 5765
        Ch_157 = 0x1000000       # Channel 157 5785
        Ch_161 = 0x2000000       # Channel 161 5805
        Ch_165 = 0x4000000       # Channel 165 5825
        Ch_36 = 0x1              # Channel 36 5180
        Ch_38 = 0x2              # Channel 38 5190
        Ch_40 = 0x4              # Channel 40 5200
        Ch_42 = 0x8              # Channel 42 5210
        Ch_44 = 0x10             # Channel 44 5220
        Ch_46 = 0x20             # Channel 46 5230
        Ch_48 = 0x40             # Channel 48 5240
        Ch_52 = 0x80             # Channel 52 5260
        Ch_56 = 0x100            # Channel 56 5280
        Ch_60 = 0x200            # Channel 60 5300
        Ch_64 = 0x400            # Channel 64 5320

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddVenueFreq5 has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_venue(self, 
                       description: str = None,  # User-supplied description, ie: <tt>Big City Ball Park</tt>;
                       # 47-characters max.
                       freq_24: str = None,      # Frequency list for 2.4Ghz band, see above.
                       freq_5: str = None,       # Frequency list for 5Ghz band, see above.
                       resource: int = None,     # Resource number. [W]
                       shelf: int = 1,           # Shelf number. [R][D:1]
                       venu_id: str = None,      # Number to uniquely identify this venue on this resource. [W]
                       x1: str = None,           # Floating point coordinate for lower-left corner.
                       x2: str = None,           # Floating point coordinate for upper-right corner.
                       y1: str = None,           # Floating point coordinate for lower-left corner.
                       y2: str = None,           # Floating point coordinate for upper-right corner.
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_venue(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if description is not None:
            data["description"] = description
        if freq_24 is not None:
            data["freq_24"] = freq_24
        if freq_5 is not None:
            data["freq_5"] = freq_5
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if venu_id is not None:
            data["venu_id"] = venu_id
        if x1 is not None:
            data["x1"] = x1
        if x2 is not None:
            data["x2"] = x2
        if y1 is not None:
            data["y1"] = y1
        if y2 is not None:
            data["y2"] = y2
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_venue",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VLAN> type requests

        https://www.candelatech.com/lfcli_ug.php#add_vlan
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_vlan(self, 
                      old_name: str = None,      # The temporary name, used for configuring un-discovered hardware.
                      port: str = None,          # Port number of an existing Ethernet interface. [W]
                      report_timer: int = None,  # Report timer for this port, leave blank or use NA for defaults.
                      resource: int = None,      # Resource number. [W]
                      shelf: int = 1,            # Shelf number. [R][D:1]
                      vid: str = None,           # The VLAN-ID for this 802.1Q VLAN interface. [W]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_vlan(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if old_name is not None:
            data["old_name"] = old_name
        if port is not None:
            data["port"] = port
        if report_timer is not None:
            data["report_timer"] = report_timer
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if vid is not None:
            data["vid"] = vid
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_vlan",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VOIP_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_voip_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_voip_endp(self, 
                           alias: str = None,           # Name of endpoint. [R]
                           auth_user_name: str = None,  # Use this field for authentication user name. AUTO or blank
                           # mean use phone number.
                           display_name: str = None,    # User-Name to be displayed. Use AUTO to display phone number.
                           gateway_port: str = None,    # IP Port for SIP gateway (defaults to 5060).
                           ip_addr: str = None,         # Use this IP for local IP address. Useful when there are
                           # multiple IPs on a port.
                           peer_phone_num: str = None,  # Use AUTO to use phone number of peer endpoint, otherwise
                           # specify a number: user[@host[:port]]
                           phone_num: str = None,       # Phone number for Endpoint [W]
                           port: str = None,            # Port number or name. [W]
                           proxy_passwd: str = None,    # Password to be used when registering with proxy/gateway.
                           resource: int = None,        # Resource number. [W]
                           rtp_port: str = None,        # RTP port to use for send and receive.
                           rx_sound_file: str = None,   # File name to save received PCM data to. Will be in WAV
                           # format, or AUTO
                           shelf: int = 1,              # Shelf name/id. [R][D:1]
                           sip_gateway: str = None,     # SIP Gateway/Proxy Name, this is who to register with, or
                           # AUTO
                           tx_sound_file: str = None,   # File name containing the sound sample we will be playing.
                           vad_max_timer: str = None,   # How often should we force a packet, even if VAD is on.
                           vad_timer: str = None,       # How much silence (milliseconds) before VAD is enabled.
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_voip_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if auth_user_name is not None:
            data["auth_user_name"] = auth_user_name
        if display_name is not None:
            data["display_name"] = display_name
        if gateway_port is not None:
            data["gateway_port"] = gateway_port
        if ip_addr is not None:
            data["ip_addr"] = ip_addr
        if peer_phone_num is not None:
            data["peer_phone_num"] = peer_phone_num
        if phone_num is not None:
            data["phone_num"] = phone_num
        if port is not None:
            data["port"] = port
        if proxy_passwd is not None:
            data["proxy_passwd"] = proxy_passwd
        if resource is not None:
            data["resource"] = resource
        if rtp_port is not None:
            data["rtp_port"] = rtp_port
        if rx_sound_file is not None:
            data["rx_sound_file"] = rx_sound_file
        if shelf is not None:
            data["shelf"] = shelf
        if sip_gateway is not None:
            data["sip_gateway"] = sip_gateway
        if tx_sound_file is not None:
            data["tx_sound_file"] = tx_sound_file
        if vad_max_timer is not None:
            data["vad_max_timer"] = vad_max_timer
        if vad_timer is not None:
            data["vad_timer"] = vad_timer
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_voip_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VR> type requests

        https://www.candelatech.com/lfcli_ug.php#add_vr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddVrFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddVrFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_4BYTE_AS_NUMBER = 0x40      # Sets corresponding Xorp flag.
        BGP_CONFED = 0x100            # Configure BGP in a confederation.
        BGP_DAMPING = 0x200           # Enable BGP damping section in Xorp configuration file.
        ENABLE_BGP = 0x20             # Set this to zero if you don't want BGP on this VR.
        RIP_ACCEPT_DR = 0x800         # Tell RIP to accept default-routes.
        ROUTE_REFLECTOR = 0x80        # Act as BGP Route Reflector.
        USE_IPV6 = 0x10               # Enable IPv6 OSPF routing for this virtual router.
        USE_IPV6_RADVD = 0x8          # Enable IPv6 RADV Daemon for interfaces in this virtual router.
        USE_RIP = 0x400               # Enable RIP routing protocol in Xorp.
        USE_XORP_MCAST = 0x2          # Enable Xorp Multicast routing (requires OSPF to be enabled currently)
        USE_XORP_OLSR = 0x1000        # Enable OLSR routing protocol in Xorp.
        USE_XORP_OSPF = 0x1           # Enable Xorp router daemon with OSPF (IPv4) protocol
        USE_XORP_SHA = 0x4            # Enable Telcordia's Xorp SHA option (requires OSPF to be enabled)

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddVrFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_vr(self, 
                    alias: str = None,     # Name of virtual router. [R]
                    flags: str = None,     # Virtual router flags, see above for definitions.
                    height: str = None,    # Height to be used when drawn in the LANforge-GUI.
                    notes: str = None,     # Notes for this Virtual Router. Put in quotes if the notes include
                    # white-space.
                    resource: int = None,  # Resource number. [W]
                    shelf: int = 1,        # Shelf name/id. [R][D:1]
                    vr_id: str = None,     # Leave blank, use NA or 0xFFFF unless you are certain of the value you
                    # want to enter.
                    width: str = None,     # Width to be used when drawn in the LANforge-GUI.
                    x: str = None,         # X coordinate to be used when drawn in the LANforge-GUI.
                    y: str = None,         # Y coordinate to be used when drawn in the LANforge-GUI.
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_vr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if flags is not None:
            data["flags"] = flags
        if height is not None:
            data["height"] = height
        if notes is not None:
            data["notes"] = notes
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if vr_id is not None:
            data["vr_id"] = vr_id
        if width is not None:
            data["width"] = width
        if x is not None:
            data["x"] = x
        if y is not None:
            data["y"] = y
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_vr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VR_BGP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_vr_bgp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddVrBgpFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddVrBgpFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        p_4BYTE_AS_NUMBER = 0x40      # Sets corresponding Xorp flag.
        BGP_CONFED = 0x100            # Configure BGP in a confederation.
        BGP_DAMPING = 0x200           # Enable BGP damping section in Xorp configuration file.
        ENABLE_BGP = 0x20             # Set this to zero if you don't want BGP on this VR.
        ROUTE_REFLECTOR = 0x80        # Act as BGP Route Reflector.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddVrBgpFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_vr_bgp(self, 
                        bgp_id: str = None,        # BGP Identifier: IPv4 Address [W]
                        cluster_id: str = None,    # Cluster ID, IPv4 Address. Use NA if not clustering.
                        confed_id: str = None,     # Confederation ID 1-65535. Use NA if not in a confederation.
                        flags: str = None,         # Virtual router BGP flags, see above for definitions.
                        half_life: str = None,     # Halflife in minutes for damping configuration.
                        local_as: str = None,      # BGP Autonomous System number, 1-65535
                        max_suppress: str = None,  # Maximum hold down time in minutes for damping configuration.
                        resource: int = None,      # Resource number. [W]
                        reuse: str = None,         # Route flag damping reuse threshold, in minutes.
                        shelf: int = 1,            # Shelf name/id. [R][D:1]
                        suppress: str = None,      # Route flag damping cutoff threshold, in minutes.
                        vr_id: str = None,         # Name of virtual router. [R]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_vr_bgp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if bgp_id is not None:
            data["bgp_id"] = bgp_id
        if cluster_id is not None:
            data["cluster_id"] = cluster_id
        if confed_id is not None:
            data["confed_id"] = confed_id
        if flags is not None:
            data["flags"] = flags
        if half_life is not None:
            data["half_life"] = half_life
        if local_as is not None:
            data["local_as"] = local_as
        if max_suppress is not None:
            data["max_suppress"] = max_suppress
        if resource is not None:
            data["resource"] = resource
        if reuse is not None:
            data["reuse"] = reuse
        if shelf is not None:
            data["shelf"] = shelf
        if suppress is not None:
            data["suppress"] = suppress
        if vr_id is not None:
            data["vr_id"] = vr_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_vr_bgp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VRCX> type requests

        https://www.candelatech.com/lfcli_ug.php#add_vrcx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddVrcxFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(AddVrcxFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        custom_dhcpd = 0x400        # Use custom DHCP config file
        dhcpd_enabled = 0x200       # Serve IPv4 DHCP on this interface
        ipv6_enabled = 0x2000       # Serve IPv6 DHCP on this interface
        nat_enabled = 0x100         # This connection will NAT outgoing packets
        subnet_0 = 0x1              # Specify subnet 0
        subnet_1 = 0x2              # Specify subnet 1
        subnet_2 = 0x4              # Specify subnet 2
        subnet_3 = 0x8              # Specify subnet 3
        subnet_4 = 0x10             # Specify subnet 4
        subnet_5 = 0x20             # Specify subnet 5
        subnet_6 = 0x40             # Specify subnet 6
        subnet_7 = 0x80             # Specify subnet 7
        use_multicast = 0x800       # Use this interface for multicast and-rp
        use_vrrp = 0x1000           # Use this interface for VRRP

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("AddVrcxFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_add_vrcx(self, 
                      dhcp_dns: str = None,         # IP Address of DNS server.
                      dhcp_dns6: str = None,        # IPv6 Address of DNS server.
                      dhcp_domain: str = None,      # DHCP Domain name to serve.
                      dhcp_lease_time: str = None,  # DHCP Lease time (in seconds)
                      dhcp_max: str = None,         # Minimum IP address range to serve.
                      dhcp_max6: str = None,        # Minimum IPv6 address to serve.
                      dhcp_min: str = None,         # Minimum IP address range to serve.
                      dhcp_min6: str = None,        # Minimum IPv6 address to serve.
                      flags: str = None,            # Flags, specify if subnets 0-7 are in use, see above for others.
                      height: str = None,           # Height to be used when drawn in the LANforge-GUI.
                      interface_cost: str = None,   # If using OSPF, this sets the cost for this link (1-65535).
                      local_dev: str = None,        # Name of port A, the local network device pair. [W]
                      local_dev_b: str = None,      # Name of port B for the local redirect device pair. [W]
                      nexthop: str = None,          # The next-hop to use when routing packets out this interface.
                      ospf_area: str = None,        # If using OSPF, this sets the OSPF area for this interface.
                      # Default is 0.0.0.0.
                      remote_dev: str = None,       # Name the remote network device. [W]
                      remote_dev_b: str = None,     # Name of port B for the remote network device. [W]
                      resource: int = None,         # Resource number. [W]
                      rip_metric: str = None,       # If using RIP, this determines the RIP metric (cost), (1-15, 15
                      # is infinite).
                      shelf: int = 1,               # Shelf name/id. [R][D:1]
                      subnets: str = None,          # Subnets associated with this link, format:
                      # 1.1.1.1/24,1.1.2.1/16...
                      vr_name: str = None,          # Virtual Router this endpoint belongs to. Use 'FREE_LIST' to add
                      # a stand-alone endpoint. [R][D:FREE_LIST]
                      vrrp_id: str = None,          # VRRP id, must be unique in this virtual router (1-255)
                      vrrp_interval: str = None,    # VRRP broadcast message interval, in seconds (1-255)
                      vrrp_ip: str = None,          # VRRP IPv4 address..ignored if not flagged for VRRP.
                      vrrp_ip_prefix: str = None,   # Number of bits in subnet mask, ie 24 for 255.255.255.0
                      vrrp_priority: str = None,    # VRRP Priority (1-255, higher is more priority.)
                      wanlink: str = None,          # The name of the WanLink that connects the two B ports. [W]
                      width: str = None,            # Width to be used when drawn in the LANforge-GUI.
                      x: str = None,                # X coordinate to be used when drawn in the LANforge-GUI.
                      y: str = None,                # Y coordinate to be used when drawn in the LANforge-GUI.
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_vrcx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if dhcp_dns is not None:
            data["dhcp_dns"] = dhcp_dns
        if dhcp_dns6 is not None:
            data["dhcp_dns6"] = dhcp_dns6
        if dhcp_domain is not None:
            data["dhcp_domain"] = dhcp_domain
        if dhcp_lease_time is not None:
            data["dhcp_lease_time"] = dhcp_lease_time
        if dhcp_max is not None:
            data["dhcp_max"] = dhcp_max
        if dhcp_max6 is not None:
            data["dhcp_max6"] = dhcp_max6
        if dhcp_min is not None:
            data["dhcp_min"] = dhcp_min
        if dhcp_min6 is not None:
            data["dhcp_min6"] = dhcp_min6
        if flags is not None:
            data["flags"] = flags
        if height is not None:
            data["height"] = height
        if interface_cost is not None:
            data["interface_cost"] = interface_cost
        if local_dev is not None:
            data["local_dev"] = local_dev
        if local_dev_b is not None:
            data["local_dev_b"] = local_dev_b
        if nexthop is not None:
            data["nexthop"] = nexthop
        if ospf_area is not None:
            data["ospf_area"] = ospf_area
        if remote_dev is not None:
            data["remote_dev"] = remote_dev
        if remote_dev_b is not None:
            data["remote_dev_b"] = remote_dev_b
        if resource is not None:
            data["resource"] = resource
        if rip_metric is not None:
            data["rip_metric"] = rip_metric
        if shelf is not None:
            data["shelf"] = shelf
        if subnets is not None:
            data["subnets"] = subnets
        if vr_name is not None:
            data["vr_name"] = vr_name
        if vrrp_id is not None:
            data["vrrp_id"] = vrrp_id
        if vrrp_interval is not None:
            data["vrrp_interval"] = vrrp_interval
        if vrrp_ip is not None:
            data["vrrp_ip"] = vrrp_ip
        if vrrp_ip_prefix is not None:
            data["vrrp_ip_prefix"] = vrrp_ip_prefix
        if vrrp_priority is not None:
            data["vrrp_priority"] = vrrp_priority
        if wanlink is not None:
            data["wanlink"] = wanlink
        if width is not None:
            data["width"] = width
        if x is not None:
            data["x"] = x
        if y is not None:
            data["y"] = y
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_vrcx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_VRCX2> type requests

        https://www.candelatech.com/lfcli_ug.php#add_vrcx2
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_add_vrcx2(self, 
                       local_dev: str = None,  # Name of port A for the connection. [W]
                       nexthop6: str = None,   # The IPv6 next-hop to use when routing packets out this interface.
                       resource: int = None,   # Resource number. [W]
                       shelf: int = 1,         # Shelf name/id. [R][D:1]
                       subnets6: str = None,   # IPv6 Subnets associated with this link, format:
                       # aaaa:bbbb::0/64,cccc:dddd:eeee::0/64...
                       vr_name: str = None,    # Virtual Router this endpoint belongs to. Use 'FREE_LIST' to add a
                       # stand-alone endpoint. [W][D:FREE_LIST]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_vrcx2(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if local_dev is not None:
            data["local_dev"] = local_dev
        if nexthop6 is not None:
            data["nexthop6"] = nexthop6
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if subnets6 is not None:
            data["subnets6"] = subnets6
        if vr_name is not None:
            data["vr_name"] = vr_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_vrcx2",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADD_WL_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#add_wl_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class AddWlEndpWleFlags(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        SHOW_WP = 1      # Show WanPaths in wanlink endpoint table in GUI

    def post_add_wl_endp(self, 
                         alias: str = None,                  # Name of WanPath. [R]
                         cpu_id: str = None,                 # The CPU/thread that this process should run on
                         # (kernel-mode only).
                         description: str = None,            # Description for this endpoint, put in single quotes if it
                         # contains spaces.
                         dest_ip: str = None,                # Selection filter: Destination IP.
                         dest_ip_mask: str = None,           # Selection filter: Destination IP MASK.
                         drop_every_xth_pkt: str = None,     # YES to periodically drop every Xth pkt, NO to drop packets
                         # randomly.
                         drop_freq: str = None,              # How often, out of 1,000,000 packets, should we
                         # purposefully drop a packet. [W]
                         dup_every_xth_pkt: str = None,      # YES to periodically duplicate every Xth pkt, NO to
                         # duplicate packets randomly.
                         dup_freq: str = None,               # How often, out of 1,000,000 packets, should we
                         # purposefully duplicate a packet. [W]
                         extra_buffer: str = None,           # The extra amount of bytes to buffer before dropping pkts,
                         # in units of 1024, use -1 for AUTO. [D:-1]
                         ignore_bandwidth: str = None,       # Should we ignore the bandwidth settings from the playback
                         # file? YES, NO, or NA.
                         ignore_dup: str = None,             # Should we ignore the Duplicate Packet settings from the
                         # playback file? YES, NO, or NA.
                         ignore_latency: str = None,         # Should we ignore the latency settings from the playback
                         # file? YES, NO, or NA.
                         ignore_loss: str = None,            # Should we ignore the packet-loss settings from the
                         # playback file? YES, NO, or NA.
                         jitter_freq: str = None,            # How often, out of 1,000,000 packets, should we apply
                         # random jitter.
                         latency: str = None,                # The base latency added to all packets, in milliseconds (or
                         # add 'us' suffix for microseconds) [W]
                         max_drop_amt: str = None,           # Maximum amount of packets to drop in a row. Default is 1.
                         # [D:1]
                         max_jitter: str = None,             # The maximum jitter, in milliseconds (or add 'us' suffix
                         # for microseconds) [W]
                         max_lateness: str = None,           # Maximum amount of un-intentional delay before pkt is
                         # dropped. Default is AUTO
                         max_rate: str = None,               # Maximum transmit rate (bps) for this WanLink.
                         max_reorder_amt: str = None,        # Maximum amount of packets by which to reorder, Default is
                         # 10. [D:10]
                         min_drop_amt: str = None,           # Minimum amount of packets to drop in a row. Default is 1.
                         # [D:1]
                         min_reorder_amt: str = None,        # Minimum amount of packets by which to reorder, Default is
                         # 1. [D:1]
                         playback_capture: str = None,       # ON or OFF, should we play back a WAN capture file?
                         playback_capture_file: str = None,  # Name of the WAN capture file to play back.
                         playback_loop: str = None,          # Should we loop the playback file, YES or NO or NA.
                         port: str = None,                   # Port number. [W]
                         reorder_every_xth_pkt: str = None,  # YES to periodically reorder every Xth pkt, NO to reorder
                         # packets randomly.
                         reorder_freq: str = None,           # How often, out of 1,000,000 packets, should we make a
                         # packet out of order. [W]
                         resource: int = None,               # Resource number. [W]
                         shelf: int = 1,                     # Shelf name/id. [R][D:1]
                         source_ip: str = None,              # Selection filter: Source IP.
                         source_ip_mask: str = None,         # Selection filter: Source IP MASK.
                         speed: str = None,                  # The maximum speed this WanLink will accept (bps). [W]
                         test_mgr: str = None,               # The name of the Test-Manager this WanPath is to use. Leave
                         # blank for no restrictions.
                         wanlink: str = None,                # Name of WanLink to which we are adding this WanPath. [R]
                         wle_flags: str = None,              # WanLink Endpoint specific flags, see above.
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_add_wl_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if cpu_id is not None:
            data["cpu_id"] = cpu_id
        if description is not None:
            data["description"] = description
        if dest_ip is not None:
            data["dest_ip"] = dest_ip
        if dest_ip_mask is not None:
            data["dest_ip_mask"] = dest_ip_mask
        if drop_every_xth_pkt is not None:
            data["drop_every_xth_pkt"] = drop_every_xth_pkt
        if drop_freq is not None:
            data["drop_freq"] = drop_freq
        if dup_every_xth_pkt is not None:
            data["dup_every_xth_pkt"] = dup_every_xth_pkt
        if dup_freq is not None:
            data["dup_freq"] = dup_freq
        if extra_buffer is not None:
            data["extra_buffer"] = extra_buffer
        if ignore_bandwidth is not None:
            data["ignore_bandwidth"] = ignore_bandwidth
        if ignore_dup is not None:
            data["ignore_dup"] = ignore_dup
        if ignore_latency is not None:
            data["ignore_latency"] = ignore_latency
        if ignore_loss is not None:
            data["ignore_loss"] = ignore_loss
        if jitter_freq is not None:
            data["jitter_freq"] = jitter_freq
        if latency is not None:
            data["latency"] = latency
        if max_drop_amt is not None:
            data["max_drop_amt"] = max_drop_amt
        if max_jitter is not None:
            data["max_jitter"] = max_jitter
        if max_lateness is not None:
            data["max_lateness"] = max_lateness
        if max_rate is not None:
            data["max_rate"] = max_rate
        if max_reorder_amt is not None:
            data["max_reorder_amt"] = max_reorder_amt
        if min_drop_amt is not None:
            data["min_drop_amt"] = min_drop_amt
        if min_reorder_amt is not None:
            data["min_reorder_amt"] = min_reorder_amt
        if playback_capture is not None:
            data["playback_capture"] = playback_capture
        if playback_capture_file is not None:
            data["playback_capture_file"] = playback_capture_file
        if playback_loop is not None:
            data["playback_loop"] = playback_loop
        if port is not None:
            data["port"] = port
        if reorder_every_xth_pkt is not None:
            data["reorder_every_xth_pkt"] = reorder_every_xth_pkt
        if reorder_freq is not None:
            data["reorder_freq"] = reorder_freq
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if source_ip is not None:
            data["source_ip"] = source_ip
        if source_ip_mask is not None:
            data["source_ip_mask"] = source_ip_mask
        if speed is not None:
            data["speed"] = speed
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if wanlink is not None:
            data["wanlink"] = wanlink
        if wle_flags is not None:
            data["wle_flags"] = wle_flags
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/add_wl_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/ADMIN> type requests

        https://www.candelatech.com/lfcli_ug.php#admin
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_admin(self, 
                   arg1: str = None,  # Argument 1: xorp-port | scan-rslts-file | iface-name | iface-eid |
                   # rfgen-message | id
                   arg2: str = None,  # Argument 2: scan key | message | angle | dest-radio
                   arg3: str = None,  # Argument 3: noprobe | migrate-sta-mac-pattern
                   arg5: str = None,  # Argument 4: table-speed
                   cmd: str = None,   # Admin command:
                   # resync_clock|write_xorp_cfg|scan_complete|ifup_post_complete|flush_complete|req_migrate|rfgen|chamber|clean_logs
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_admin(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if arg1 is not None:
            data["arg1"] = arg1
        if arg2 is not None:
            data["arg2"] = arg2
        if arg3 is not None:
            data["arg3"] = arg3
        if arg5 is not None:
            data["arg5"] = arg5
        if cmd is not None:
            data["cmd"] = cmd
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/admin",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/APPLY_VR_CFG> type requests

        https://www.candelatech.com/lfcli_ug.php#apply_vr_cfg
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_apply_vr_cfg(self, 
                          resource: int = None,  # The number of the resource in question, or 'ALL'. [W]
                          shelf: int = 1,        # The number of the shelf in question, or 'ALL'. [R][D:ALL]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_apply_vr_cfg(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/apply_vr_cfg",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/BLINK_ATTENUATOR> type requests

        https://www.candelatech.com/lfcli_ug.php#blink_attenuator
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_blink_attenuator(self, 
                              resource: int = None,  # Resource number. [W]
                              serno: str = None,     # Serial number for requested Attenuator, or 'all'. [W]
                              shelf: int = 1,        # Shelf number, usually 1. [R][D:1]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_blink_attenuator(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if serno is not None:
            data["serno"] = serno
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/blink_attenuator",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/C_SHOW_PORTS> type requests

        https://www.candelatech.com/lfcli_ug.php#c_show_ports
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class CShowPortsProbeFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(CShowPortsProbeFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BRIDGE = 0x8                 # 8 include bridges
        EASY_IP_INFO = 0x10          # 16 Everything but gateway information, which is expensive to probe.
        ETHTOOL = 0x4                # 4 include ethtool results
        GW = 0x20                    # 32 include gateway information
        GW_FORCE_REFRESH = 0x40      # 64 Force GW (re)probe. Otherwise, cached values *might* be used.
        MII = 0x2                    # 2 include MII
        WIFI = 0x1                   # 1 include wifi stations

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("CShowPortsProbeFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_c_show_ports(self, 
                          port: str = None,         # Port number, or 'all'. [W]
                          probe_flags: str = None,  # See above, add them together for multiple probings. Leave
                          # blank if you want stats only.
                          resource: int = None,     # Resource number, or 'all'. [W]
                          shelf: int = 1,           # Name/id of the shelf, or 'all'. [R][D:1]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_c_show_ports(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if probe_flags is not None:
            data["probe_flags"] = probe_flags
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/c_show_ports",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CANCEL_VR_CFG> type requests

        https://www.candelatech.com/lfcli_ug.php#cancel_vr_cfg
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_cancel_vr_cfg(self, 
                           resource: int = None,  # The number of the resource in question, or 'ALL'. [W]
                           shelf: int = 1,        # The number of the shelf in question, or 'ALL'. [R][D:ALL]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_cancel_vr_cfg(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/cancel_vr_cfg",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_CD_COUNTERS> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_cd_counters
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_clear_cd_counters(self, 
                               cd_name: str = None,  # Name of Collision Domain, or 'all'. Null argument is same
                               # as 'all'. [W][D:all]
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_cd_counters(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cd_name is not None:
            data["cd_name"] = cd_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_cd_counters",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_CX_COUNTERS> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_cx_counters
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_clear_cx_counters(self, 
                               cx_name: str = None,  # Name of Cross Connect, or 'all'. Null argument is same as
                               # 'all'. [W][D:all]
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_cx_counters(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cx_name is not None:
            data["cx_name"] = cx_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_cx_counters",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_ENDP_COUNTERS> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_endp_counters
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_clear_endp_counters(self, 
                                 endp_name: str = None,     # Name of Endpoint, or 'all'. Null argument is same as
                                 # 'all'. [W][D:all]
                                 incr_seqno: str = None,    # Enter 'YES' if you want the target to increment the
                                 # cfg-seq-no.
                                 just_latency: str = None,  # Enter 'YES' if you only want to clear latency counters,
                                 # and see above for RXGAP.
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_endp_counters(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if incr_seqno is not None:
            data["incr_seqno"] = incr_seqno
        if just_latency is not None:
            data["just_latency"] = just_latency
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_endp_counters",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_clear_group(self, 
                         name: str = None,  # The name of the test group. [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_PORT_COUNTERS> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_port_counters
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class ClearPortCountersExtra(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        dhcp4_lease = "dhcp4_lease"    # Remove dhcp lease files for IPv4 DHCP
        dhcp6_lease = "dhcp6_lease"    # Remove dhcp lease files for IPv6 DHCP
        dhcp_leases = "dhcp_leases"    # Remove dhcp lease files for IPv4 and IPv6 DHCP

    def post_clear_port_counters(self, 
                                 extra: str = None,     # Clear something else instead: dhcp4_lease | dhcp6_lease |
                                 # dhcp_leases
                                 port: str = None,      # The number of the port in question, or 'ALL'. [W]
                                 resource: int = None,  # The number of the resource in question, or 'ALL'. [W]
                                 shelf: int = 1,        # The number of the shelf in question, or 'ALL'. [R][D:1]
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_port_counters(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if extra is not None:
            data["extra"] = extra
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_port_counters",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_RESOURCE_COUNTERS> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_resource_counters
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_clear_resource_counters(self, 
                                     resource: int = None,  # The number of the resource in question, or 'ALL'. [W]
                                     shelf: int = 1,        # The number of the shelf in question, or 'ALL'.
                                     # [R][D:1]
                                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_resource_counters(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_resource_counters",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CLEAR_WP_COUNTERS> type requests

        https://www.candelatech.com/lfcli_ug.php#clear_wp_counters
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_clear_wp_counters(self, 
                               endp_name: str = None,  # Name of WanLink Endpoint. [W]
                               wp_name: str = None,    # Name of WanPath to clear.
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_clear_wp_counters(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if wp_name is not None:
            data["wp_name"] = wp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/clear_wp_counters",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/CREATE_CLIENT> type requests

        https://www.candelatech.com/lfcli_ug.php#create_client
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_create_client(self, 
                           name: str = None,        # A single name with no white-spaces (15 characters or less) [W]
                           password: str = None,    # Can be blank or 'NA' if no password is set, otherwise must be
                           # the password. Use IGNORE for no change.
                           super_user: str = None,  # 1 If you want this user to have Administrative powers, 0 or
                           # blank otherwise.
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_create_client(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if password is not None:
            data["password"] = password
        if super_user is not None:
            data["super_user"] = super_user
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/create_client",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/DIAG> type requests

        https://www.candelatech.com/lfcli_ug.php#diag
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class DiagType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NA = "NA"                  # everything (default)
        alerts = "alerts"          # alert messages
        clients = "clients"        # connected clients
        counters = "counters"      # endpoint counters
        endpoints = "endpoints"    # list of endpoints
        fds = "fds"                # file descriptors
        iobuffer = "iobuffer"      #
        license = "license"        # license contents
        shelf = "shelf"            #

    def post_diag(self, 
                  arg1: str = None,  # Optional: Endpoint name to diag.
                  p_type: str = None,  # Default (blank) is everything, options: alerts, license, counters, fds,
                  # clients, endpoints, shelf, iobuffer.
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_diag(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if arg1 is not None:
            data["arg1"] = arg1
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/diag",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/DISCOVER> type requests

        https://www.candelatech.com/lfcli_ug.php#discover
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_discover(self, 
                      disconnect: str = None,  # Set to 'disconnect' to force disconnect to remote resource process.
                      resource: int = None,    # Resource ID. Use if discovering Attenuators. [W]
                      shelf: int = 1,          # Shelf-ID, only used if discovering Attenuators. [R][D:1]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_discover(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if disconnect is not None:
            data["disconnect"] = disconnect
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/discover",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/DO_PESQ> type requests

        https://www.candelatech.com/lfcli_ug.php#do_pesq
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_do_pesq(self, 
                     endp_name: str = None,         # Name of Endpoint. [W]
                     result_file_name: str = None,  # The name of the file received by the endpoint. [W]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_do_pesq(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if result_file_name is not None:
            data["result_file_name"] = result_file_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/do_pesq",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/FILE> type requests

        https://www.candelatech.com/lfcli_ug.php#file
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_file(self, 
                  card: int = None,      # Resource ID [W]
                  cmd: str = None,       # Only 'Download' supported for now, 'Upload' reserved for future use.
                  # [W][D:Download]
                  filename: str = None,  # File to transfer. [W]
                  shelf: int = 1,        # Shelf ID [R][D:1]
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_file(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if card is not None:
            data["card"] = card
        if cmd is not None:
            data["cmd"] = cmd
        if filename is not None:
            data["filename"] = filename
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/file",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/FLASH_ATTENUATOR> type requests

        https://www.candelatech.com/lfcli_ug.php#flash_attenuator
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_flash_attenuator(self, 
                              filename: str = None,  # File to use when uploading to attenuator.
                              resource: int = None,  # Resource number. [W]
                              serno: str = None,     # Serial number for requested Attenuator, or 'all'. [W]
                              shelf: int = 1,        # Shelf number, usually 1. [R][D:1]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_flash_attenuator(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if filename is not None:
            data["filename"] = filename
        if resource is not None:
            data["resource"] = resource
        if serno is not None:
            data["serno"] = serno
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/flash_attenuator",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETAVGLATENCY> type requests

        https://www.candelatech.com/lfcli_ug.php#getavglatency
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getavglatency(self, 
                           aorb: str = None,  # For AtoB, enter 'B', for BtoA, enter 'A'.
                           cx: str = None,    # Cross-connect or Test-Group name [W]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getavglatency(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getavglatency",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETINRXBPS> type requests

        https://www.candelatech.com/lfcli_ug.php#getinrxbps
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getinrxbps(self, 
                        aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                        cx: str = None,    # Cross-connect or Test-Group name [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getinrxbps(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getinrxbps",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETINRXRATE> type requests

        https://www.candelatech.com/lfcli_ug.php#getinrxrate
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getinrxrate(self, 
                         aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                         cx: str = None,    # Cross-connect or Test-Group name [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getinrxrate(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getinrxrate",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETINTXRATE> type requests

        https://www.candelatech.com/lfcli_ug.php#getintxrate
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getintxrate(self, 
                         aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                         cx: str = None,    # Cross-connect or Test-Group name [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getintxrate(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getintxrate",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETIPADD> type requests

        https://www.candelatech.com/lfcli_ug.php#getipadd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getipadd(self, 
                      aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                      cx: str = None,    # Cross-connect name [W]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getipadd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getipadd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETMAC> type requests

        https://www.candelatech.com/lfcli_ug.php#getmac
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getmac(self, 
                    aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                    cx: str = None,    # Cross-connect name [W]
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getmac(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getmac",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETMASK> type requests

        https://www.candelatech.com/lfcli_ug.php#getmask
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getmask(self, 
                     aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                     cx: str = None,    # Cross-connect name
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getmask(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getmask",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETPKTDROPS> type requests

        https://www.candelatech.com/lfcli_ug.php#getpktdrops
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getpktdrops(self, 
                         aorb: str = None,  # For AtoB, enter 'B', for BtoA, enter 'A'.
                         cx: str = None,    # Cross-connect or Test-Group name [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getpktdrops(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getpktdrops",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETRXENDPERRPKTS> type requests

        https://www.candelatech.com/lfcli_ug.php#getrxendperrpkts
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getrxendperrpkts(self, 
                              aorb: str = None,  # For AtoB, enter 'B', for BtoA, enter 'A'.
                              cx: str = None,    # Cross-connect or Test-Group name [W]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getrxendperrpkts(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getrxendperrpkts",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETRXPKTS> type requests

        https://www.candelatech.com/lfcli_ug.php#getrxpkts
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getrxpkts(self, 
                       aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                       cx: str = None,    # Cross-connect or Test-Group name [W]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getrxpkts(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getrxpkts",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETRXPORTERRPKTS> type requests

        https://www.candelatech.com/lfcli_ug.php#getrxporterrpkts
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_getrxporterrpkts(self, 
                              aorb: str = None,  # For AtoB, enter 'B', for BtoA, enter 'A'.
                              cx: str = None,    # Cross-connect name [W]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_getrxporterrpkts(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/getrxporterrpkts",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GETTXPKTS> type requests

        https://www.candelatech.com/lfcli_ug.php#gettxpkts
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_gettxpkts(self, 
                       aorb: str = None,  # For endpoint a, enter 'A', for endpoint b, enter 'B'.
                       cx: str = None,    # Cross-connect or Test-Group name [W]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_gettxpkts(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if aorb is not None:
            data["aorb"] = aorb
        if cx is not None:
            data["cx"] = cx
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/gettxpkts",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/GOSSIP> type requests

        https://www.candelatech.com/lfcli_ug.php#gossip
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_gossip(self, 
                    message: str = None,  # Message to show to others currently logged on. <tt
                    # escapearg='false'>Unescaped Value</tt> [W]
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_gossip(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if message is not None:
            data["message"] = message
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/gossip",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/HELP> type requests

        https://www.candelatech.com/lfcli_ug.php#help
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_help(self, 
                  command: str = None,  # The command to get help for. Can be 'all', or blank.
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_help(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if command is not None:
            data["command"] = command
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/help",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/INIT_WISER> type requests

        https://www.candelatech.com/lfcli_ug.php#init_wiser
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_init_wiser(self, 
                        file_name: str = None,   # The WISER file name for the desired emulation, or 'NA' for empty
                        # string.
                        node_count: str = None,  # The number of WISER nodes for the desired emulation, or 'NA' for
                        # empty string.
                        resource: int = None,    # The number of the resource in question. [W]
                        shelf: int = 1,          # The number of the shelf in question. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_init_wiser(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if file_name is not None:
            data["file_name"] = file_name
        if node_count is not None:
            data["node_count"] = node_count
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/init_wiser",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/LICENSES> type requests

        https://www.candelatech.com/lfcli_ug.php#licenses
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_licenses(self, 
                      popup: str = None,      # If 'popup', then cause a GUI popup msg, otherwise, just show text.
                      show_file: str = None,  # If 'yes', then show the license file, not the parsed license
                      # information.
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_licenses(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if popup is not None:
            data["popup"] = popup
        if show_file is not None:
            data["show_file"] = show_file
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/licenses",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/LOAD> type requests

        https://www.candelatech.com/lfcli_ug.php#load
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_load(self, 
                  action: str = None,          # Should be 'append' or 'overwrite'. [W]
                  clean_chambers: str = None,  # If yes, then Chambers will be cleaned up when overwrite is selected,
                  # otherwise they will be kept.
                  clean_dut: str = None,       # If yes, then DUT will be cleaned up when overwrite is selected,
                  # otherwise they will be kept.
                  clean_profiles: str = None,  # If yes, then clean all profiles when overwrite is selected, otherwise
                  # they will be kept.
                  name: str = None,            # The name of the database to load. (DFLT is the default) [W]
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_load(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if action is not None:
            data["action"] = action
        if clean_chambers is not None:
            data["clean_chambers"] = clean_chambers
        if clean_dut is not None:
            data["clean_dut"] = clean_dut
        if clean_profiles is not None:
            data["clean_profiles"] = clean_profiles
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/load",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/LOG_LEVEL> type requests

        https://www.candelatech.com/lfcli_ug.php#log_level
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class LogLevelLevel(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(LogLevelLevel0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        ALL = 0xffffffff        # Log everything
        CUST1 = 0x10000         # Cust-1, latency info (65536)
        DB = 0x80               # Database related logging (128)
        DBG = 0x20              # debug (32)
        DBG2 = 0x1000           # very verbose logging (4096)
        DIS = 0x1               # disasters (1)
        ERR = 0x2               # errors (2)
        INF = 0x8               # info (8)
        LIO = 0x2000            # IO logging (8192)
        LL_PROF = 0x8000        # Profiling information (32768)
        OUT1 = 0x4000           # Some std-out logging (16384)
        PARSE = 0x800           # PARSE specific (2048)
        SCRIPT = 0x400          # Scripting specific stuff (1024)
        SEC = 0x40              # log security violations (64)
        TRC = 0x10              # function trace (16)
        WRN = 0x4               # warnings (4)
        XMT = 0x100             # Output going to clients (256)

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("LogLevelLevel has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_log_level(self, 
                       level: str = None,   # Integer corresponding to the logging flags. [W]
                       target: str = None,  # Options: 'gnu' | [file-endp-name].
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_log_level(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if level is not None:
            data["level"] = level
        if target is not None:
            data["target"] = target
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/log_level",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/LOG_MSG> type requests

        https://www.candelatech.com/lfcli_ug.php#log_msg
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_log_msg(self, 
                     message: str = None,  # Message to log. <tt escapearg='false'>Unescaped Value</tt> [W]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_log_msg(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if message is not None:
            data["message"] = message
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/log_msg",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/LOGIN> type requests

        https://www.candelatech.com/lfcli_ug.php#login
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_login(self, 
                   name: str = None,      # A single name with no white-spaces (15 characters or less) [W]
                   password: str = None,  # Can be blank or 'NA' if no password is set, otherwise must be the
                   # password.
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_login(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if password is not None:
            data["password"] = password
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/login",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/MOTD> type requests

        https://www.candelatech.com/lfcli_ug.php#motd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_motd(self, 
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_motd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/motd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_CD> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_cd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_cd(self, 
                        collision_domain: str = None,  # Name of the Collision Domain, or 'all'. [W]
                        resource: int = None,          # Resource number, or 'all'. [W]
                        shelf: int = 1,                # Name/id of the shelf, or 'all'. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_cd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if collision_domain is not None:
            data["collision_domain"] = collision_domain
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_cd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_CHANNEL_GROUPS> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_channel_groups
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_channel_groups(self, 
                                    channel_name: str = None,  # Name of the channel, or 'all'. [W]
                                    resource: int = None,      # Resource number, or 'all'. [W]
                                    shelf: int = 1,            # Name/id of the shelf, or 'all'. [R][D:1]
                                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_channel_groups(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if channel_name is not None:
            data["channel_name"] = channel_name
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_channel_groups",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_ENDPOINTS> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_endpoints
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_endpoints(self, 
                               endpoint: str = None,  # Name of endpoint, or 'all'. [W]
                               extra: str = None,     # See above.
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_endpoints(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endpoint is not None:
            data["endpoint"] = endpoint
        if extra is not None:
            data["extra"] = extra
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_endpoints",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_PESQ> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_pesq
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_pesq(self, 
                          endpoint: str = None,  # Name of endpoint, or 'all'. [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_pesq(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endpoint is not None:
            data["endpoint"] = endpoint
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_pesq",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_PORTS> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_ports
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class NcShowPortsProbeFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(NcShowPortsProbeFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BRIDGE = 0x8                 # 8 include bridges
        EASY_IP_INFO = 0x10          # 16 Everything but gateway information, which is expensive to probe.
        ETHTOOL = 0x4                # 4 include ethtool results
        GW = 0x20                    # 32 include gateway information
        GW_FORCE_REFRESH = 0x40      # 64 Force GW (re)probe. Otherwise, cached values *might* be used.
        MII = 0x2                    # 2 include MII
        WIFI = 0x1                   # 1 include wifi stations

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("NcShowPortsProbeFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_nc_show_ports(self, 
                           port: str = None,         # Port number, or 'all'. [W]
                           probe_flags: str = None,  # See above, add them together for multiple probings. Leave
                           # blank if you want stats only.
                           resource: int = None,     # Resource number, or 'all'. [W]
                           shelf: int = 1,           # Name/id of the shelf, or 'all'. [R][D:1]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_ports(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if probe_flags is not None:
            data["probe_flags"] = probe_flags
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_ports",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_PPP_LINKS> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_ppp_links
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_ppp_links(self, 
                               link_num: str = None,  # Ppp-Link number of the span, or 'all'. [W]
                               resource: int = None,  # Resource number, or 'all'. [W]
                               shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_ppp_links(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if link_num is not None:
            data["link_num"] = link_num
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_ppp_links",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_SPANS> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_spans
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_spans(self, 
                           resource: int = None,     # Resource number, or 'all'. [W]
                           shelf: int = 1,           # Name/id of the shelf, or 'all'. [R][D:1]
                           span_number: str = None,  # Span-Number of the span, or 'all'. [W]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_spans(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if span_number is not None:
            data["span_number"] = span_number
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_spans",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_VR> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_vr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_vr(self, 
                        resource: int = None,  # Resource number, or 'all'. [W]
                        router: str = None,    # Name of the Virtual Router, or 'all'. [W]
                        shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_vr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if router is not None:
            data["router"] = router
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_vr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NC_SHOW_VRCX> type requests

        https://www.candelatech.com/lfcli_ug.php#nc_show_vrcx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_nc_show_vrcx(self, 
                          cx_name: str = None,   # Name of the Virtual Router Connection, or 'all'. [W]
                          resource: int = None,  # Resource number, or 'all'. [W]
                          shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_nc_show_vrcx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cx_name is not None:
            data["cx_name"] = cx_name
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/nc_show_vrcx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/NOTIFY_DHCP> type requests

        https://www.candelatech.com/lfcli_ug.php#notify_dhcp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_notify_dhcp(self, 
                         cmd: str = None,         # set/down/timeout/info: What does DHCP want us to do? [W]
                         netmask: str = None,     # New subnet mask.
                         new_dns: str = None,     # New DNS server(s) for use by this interface.
                         new_ip: str = None,      # New IP address.
                         new_ip6: str = None,     # New Global IPv6 address: ipv6/prefix
                         new_mtu: str = None,     # New MTU.
                         new_router: str = None,  # One or more default routers. LANforge will only use the first
                         # one.
                         port: str = None,        # Interface name. [W]
                         reason: str = None,      # DHCP reason, informational mostly.
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_notify_dhcp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cmd is not None:
            data["cmd"] = cmd
        if netmask is not None:
            data["netmask"] = netmask
        if new_dns is not None:
            data["new_dns"] = new_dns
        if new_ip is not None:
            data["new_ip"] = new_ip
        if new_ip6 is not None:
            data["new_ip6"] = new_ip6
        if new_mtu is not None:
            data["new_mtu"] = new_mtu
        if new_router is not None:
            data["new_router"] = new_router
        if port is not None:
            data["port"] = port
        if reason is not None:
            data["reason"] = reason
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/notify_dhcp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/PORT_RESET_COMPLETED> type requests

        https://www.candelatech.com/lfcli_ug.php#port_reset_completed
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_port_reset_completed(self, 
                                  extra: str = None,  # IP for SECIP, blank for others.
                                  port: str = None,   # The port in question. [W]
                                  p_type: str = None,  # SUNOS, NORMAL, or SECIP..let us know what kind of reset
                                  # completed.
                                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_port_reset_completed(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if extra is not None:
            data["extra"] = extra
        if port is not None:
            data["port"] = port
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/port_reset_completed",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/PROBE_PORT> type requests

        https://www.candelatech.com/lfcli_ug.php#probe_port
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_probe_port(self, 
                        key: str = None,       # Unique identifier for this request. Usually left blank.<br/>
                        port: str = None,      # Port number or name [W]
                        resource: int = None,  # Resource number. [W]
                        shelf: int = 1,        # Shelf number. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_probe_port(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if key is not None:
            data["key"] = key
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/probe_port",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/PROBE_PORTS> type requests

        https://www.candelatech.com/lfcli_ug.php#probe_ports
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_probe_ports(self, 
                         resource: int = None,  # Resource number, or 'all'. [W]
                         shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_probe_ports(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/probe_ports",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/QUIESCE_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#quiesce_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_quiesce_endp(self, 
                          endp_name: str = None,  # Name of the endpoint, or 'all'. [R]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_quiesce_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/quiesce_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/QUIESCE_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#quiesce_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_quiesce_group(self, 
                           name: str = None,  # The name of the test group, or 'all' [R]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_quiesce_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/quiesce_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/QUIT> type requests

        https://www.candelatech.com/lfcli_ug.php#quit
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_quit(self, 
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_quit(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/quit",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/REBOOT_OS> type requests

        https://www.candelatech.com/lfcli_ug.php#reboot_os
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_reboot_os(self, 
                       resource: int = None,  # Resource number, or ALL. [W]
                       shelf: int = 1,        # Shelf number, or ALL. [R][D:1]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_reboot_os(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/reboot_os",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/REPORT> type requests

        https://www.candelatech.com/lfcli_ug.php#report
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_report(self, 
                    reporting_on: str = None,   # Should we globally enable/disable reporting. (YES, NO or NA)
                    rpt_dir: str = None,        # Directory in which reports should be saved. [W]
                    save_endps: str = None,     # Should we save endpoint reports or not. (YES, NO or NA)
                    save_ports: str = None,     # Should we save Port reports or not. (YES, NO or NA)
                    save_resource: str = None,  # Should we save Resource reports or not. (YES, NO or NA)
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_report(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if reporting_on is not None:
            data["reporting_on"] = reporting_on
        if rpt_dir is not None:
            data["rpt_dir"] = rpt_dir
        if save_endps is not None:
            data["save_endps"] = save_endps
        if save_ports is not None:
            data["save_ports"] = save_ports
        if save_resource is not None:
            data["save_resource"] = save_resource
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/report",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RESET_PORT> type requests

        https://www.candelatech.com/lfcli_ug.php#reset_port
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class ResetPortPreIfdown(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        P_IN = "P-IN"      # Only call the portal login (do not reset drivers/supplicant/dhcp)
        P_OUT = "P-OUT"    # Only call the portal logout (do not reset drivers/supplicant/dhcp)
        YES = "YES"        # (include logout) Call portal-bot.pl ... <b>--logout</b> before going down.

    def post_reset_port(self, 
                        port: str = None,        # Port number to reset, or ALL. [W]
                        pre_ifdown: str = None,  # See above. Leave blank or use NA if unsure.
                        reset_ospf: str = None,  # If set to 'NO' or 'NA', then OSPF will not be updated. Otherwise,
                        # it will be updated.
                        resource: int = None,    # Resource number, or ALL. [W]
                        shelf: int = 1,          # Shelf number, or ALL. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_reset_port(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if pre_ifdown is not None:
            data["pre_ifdown"] = pre_ifdown
        if reset_ospf is not None:
            data["reset_ospf"] = reset_ospf
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/reset_port",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RESET_SERIAL_SPAN> type requests

        https://www.candelatech.com/lfcli_ug.php#reset_serial_span
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_reset_serial_span(self, 
                               resource: int = None,  # Resource (machine) number. [W]
                               shelf: int = 1,        # Shelf number [R][D:1]
                               span: str = None,      # Serial-Span number to reset. [W]
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_reset_serial_span(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if span is not None:
            data["span"] = span
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/reset_serial_span",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_ATTENUATOR> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_attenuator
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_attenuator(self, 
                           resource: int = None,  # Resource number [W]
                           serno: str = None,     # Serial number for requested Attenuator. [W]
                           shelf: int = 1,        # Shelf number, usually 1 [R][D:1]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_attenuator(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if serno is not None:
            data["serno"] = serno
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_attenuator",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CD> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_cd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_cd(self, 
                   cd: str = None,  # Name of Collision Domain. [W]
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_cd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cd is not None:
            data["cd"] = cd
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_cd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CD_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_cd_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_cd_endp(self, 
                        cd: str = None,    # Name of Collision Domain. [W]
                        endp: str = None,  # Endpoint name/id. [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_cd_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cd is not None:
            data["cd"] = cd
        if endp is not None:
            data["endp"] = endp
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_cd_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CD_VR> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_cd_vr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_cd_vr(self, 
                      cd: str = None,    # Name of Collision Domain. [W]
                      endp: str = None,  # Virtual-Router name/id. [W]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_cd_vr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cd is not None:
            data["cd"] = cd
        if endp is not None:
            data["endp"] = endp
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_cd_vr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CHAMBER> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_chamber
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_chamber(self, 
                        chamber: str = None,  # Chamber name, or 'ALL' [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_chamber(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if chamber is not None:
            data["chamber"] = chamber
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_chamber",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CHAMBER_PATH> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_chamber_path
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_chamber_path(self, 
                             chamber: str = None,  # Chamber Name. [W]
                             path: str = None,     # Path Name, use 'ALL' to delete all paths. [W]
                             debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_chamber_path(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if chamber is not None:
            data["chamber"] = chamber
        if path is not None:
            data["path"] = path
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_chamber_path",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CHANNEL_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_channel_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_channel_group(self, 
                              channel_name: str = None,  # Name of the channel, or 'all'. [W]
                              resource: int = None,      # Resource number, or 'all'. [W]
                              shelf: int = 1,            # Name/id of the shelf, or 'all'. [R][D:1]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_channel_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if channel_name is not None:
            data["channel_name"] = channel_name
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_channel_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CLIENT> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_client
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_client(self, 
                       client_name: str = None,      # Name of the client profile you wish to remove. [W]
                       client_password: str = None,  # Client password. Not required if we are super-user.
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_client(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if client_name is not None:
            data["client_name"] = client_name
        if client_password is not None:
            data["client_password"] = client_password
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_client",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_CX> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_cx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_cx(self, 
                   cx_name: str = None,   # Name of the cross-connect, or 'all'. [W]
                   test_mgr: str = None,  # Name of test-mgr, or 'all'. [W]
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_cx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cx_name is not None:
            data["cx_name"] = cx_name
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_cx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_DB> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_db
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_db(self, 
                   db_name: str = None,  # Name of the database to delete. [W]
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_db(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if db_name is not None:
            data["db_name"] = db_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_db",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_DUT> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_dut
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_dut(self, 
                    shelf: int = 1,  # DUT name, or 'ALL' [W]
                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_dut(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_dut",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_endp(self, 
                     endp_name: str = None,  # Name of the endpoint, or 'YES_ALL'. [W]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_EVENT> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_event
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_event(self, 
                      event_id: str = None,  # Numeric event-id, or 'all' [W]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_event(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if event_id is not None:
            data["event_id"] = event_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_event",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_group(self, 
                      name: str = None,  # The name of the test group. [W]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_PPP_LINK> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_ppp_link
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_ppp_link(self, 
                         resource: int = None,  # Resource number that holds this PppLink. [W]
                         shelf: int = 1,        # Name/id of the shelf. [R][D:1]
                         unit_num: str = None,  # Unit-Number for the PppLink to be deleted. [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_ppp_link(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if unit_num is not None:
            data["unit_num"] = unit_num
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_ppp_link",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_PROFILE> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_profile
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_profile(self, 
                        name: str = None,  # Profile name, or 'ALL' [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_profile(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_profile",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_RESOURCE> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_resource
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_resource(self, 
                         resource: int = None,  # Resource number. [W]
                         shelf: int = 1,        # Shelf number. [R][D:1]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_resource(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_resource",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_RFGEN> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_rfgen
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_rfgen(self, 
                      resource: int = None,  # Resource number [W]
                      shelf: int = 1,        # Shelf number, usually 1 [R][D:1]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_rfgen(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_rfgen",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_SEC_IP> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_sec_ip
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_sec_ip(self, 
                       ip_list: str = None,   # IP1/prefix,IP2/prefix,...IPZ/prefix, or ALL [W]
                       port: str = None,      # Name of network device (Port) from which these IPs will be removed.
                       # [W]
                       resource: int = None,  # Resource number. [W]
                       shelf: int = 1,        # Shelf number. [R][D:1]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_sec_ip(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ip_list is not None:
            data["ip_list"] = ip_list
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_sec_ip",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_SPAN> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_span
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_span(self, 
                     resource: int = None,  # Resource number, or 'all'. [W]
                     shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                     span_num: str = None,  # Span-Number of the channel, or 'all'. [W]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_span(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if span_num is not None:
            data["span_num"] = span_num
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_span",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_TEST_MGR> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_test_mgr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_test_mgr(self, 
                         test_mgr: str = None,  # Name of the test manager to be removed. [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_test_mgr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_test_mgr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_TEXT_BLOB> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_text_blob
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_text_blob(self, 
                          name: str = None,  # Text Blob Name, or 'ALL' [W]
                          p_type: str = None,  # Text Blob type, or 'ALL' [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_text_blob(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_text_blob",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_TGCX> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_tgcx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_tgcx(self, 
                     cxname: str = None,  # The name of the CX. [W]
                     tgname: str = None,  # The name of the test group. [W]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_tgcx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cxname is not None:
            data["cxname"] = cxname
        if tgname is not None:
            data["tgname"] = tgname
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_tgcx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_THRESHOLD> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_threshold
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_threshold(self, 
                          endp: str = None,       # Endpoint name or ID. [W]
                          thresh_id: str = None,  # Threshold ID to remove. Use 'all' to remove all. [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_threshold(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp is not None:
            data["endp"] = endp
        if thresh_id is not None:
            data["thresh_id"] = thresh_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_threshold",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_TRAFFIC_PROFILE> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_traffic_profile
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_traffic_profile(self, 
                                name: str = None,  # Profile name, or 'ALL' [W]
                                debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_traffic_profile(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_traffic_profile",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_VENUE> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_venue
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_venue(self, 
                      resource: int = None,  # Resource number, or 'ALL' [W]
                      shelf: int = 1,        # Shelf number. [R][D:1]
                      venu_id: str = None,   # Number to uniquely identify this venue on this resource, or 'ALL'
                      # [W]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_venue(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if venu_id is not None:
            data["venu_id"] = venu_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_venue",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_VLAN> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_vlan
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_vlan(self, 
                     port: str = None,      # Port number or name of the virtual interface. [W]
                     resource: int = None,  # Resource number. [W]
                     shelf: int = 1,        # Shelf number. [R][D:1]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_vlan(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_vlan",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_VR> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_vr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_vr(self, 
                   resource: int = None,     # Resource number, or 'all'. [W]
                   router_name: str = None,  # Virtual Router name, or 'all'. [W]
                   shelf: int = 1,           # Name/id of the shelf, or 'all'. [R][D:1]
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_vr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if router_name is not None:
            data["router_name"] = router_name
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_vr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_VRCX> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_vrcx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_vrcx(self, 
                     connection_name: str = None,  # Virtual Router Connection name, or 'all'. [W]
                     resource: int = None,         # Resource number, or 'all'. [W]
                     shelf: int = 1,               # Name/id of the shelf, or 'all'. [R][D:1]
                     vr_id: str = None,            # If not removing from the free-list, then supply the
                     # virtual-router name/ID here. Leave blank or use NA for free-list.
                     vrcx_only: str = None,        # If we should NOT delete underlying auto-created objects, enter
                     # 'vrcx_only' here, otherwise leave blank or use NA.
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_vrcx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if connection_name is not None:
            data["connection_name"] = connection_name
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if vr_id is not None:
            data["vr_id"] = vr_id
        if vrcx_only is not None:
            data["vrcx_only"] = vrcx_only
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_vrcx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RM_WANPATH> type requests

        https://www.candelatech.com/lfcli_ug.php#rm_wanpath
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rm_wanpath(self, 
                        endp_name: str = None,  # Name of the endpoint. [W]
                        wp_name: str = None,    # Name of the wanpath. [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rm_wanpath(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if wp_name is not None:
            data["wp_name"] = wp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rm_wanpath",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/RPT_SCRIPT> type requests

        https://www.candelatech.com/lfcli_ug.php#rpt_script
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_rpt_script(self, 
                        endp: str = None,          # Endpoint name or ID. [W]
                        flags: str = None,         # See above for description of the defined flags.
                        group_action: str = None,  # All or Sequential.
                        loop_count: str = None,    # How many times to loop before stopping (0 is infinite).
                        name: str = None,          # Script name. [W]
                        private: str = None,       # Private encoding for the particular script.
                        p_type: str = None,        # One of: NONE, Script2544, ScriptHunt, ScriptWL
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_rpt_script(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp is not None:
            data["endp"] = endp
        if flags is not None:
            data["flags"] = flags
        if group_action is not None:
            data["group_action"] = group_action
        if loop_count is not None:
            data["loop_count"] = loop_count
        if name is not None:
            data["name"] = name
        if private is not None:
            data["private"] = private
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/rpt_script",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SCAN_WIFI> type requests

        https://www.candelatech.com/lfcli_ug.php#scan_wifi
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class ScanWifiExtra(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NA = "NA"                                      # (or left blank) the system does a full scan
        dump = "dump"                                  # then only cached values are returned
        trigger_freq__freq_ = "trigger freq [freq]"    # scan exactly those frequencies

    def post_scan_wifi(self, 
                       extra: str = None,     # Extra arguments to the scan script, see above.
                       key: str = None,       # Unique identifier for this request. Usually left blank.
                       port: str = None,      # Port number or name of the virtual interface. [W]
                       resource: int = None,  # Resource number. [W]
                       shelf: int = 1,        # Shelf number. [R][D:1]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_scan_wifi(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if extra is not None:
            data["extra"] = extra
        if key is not None:
            data["key"] = key
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/scan_wifi",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ARM_INFO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_arm_info
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetArmInfoArmFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetArmInfoArmFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        random_payload = 0x10000      # Use random payload sizes instead of linear increase
        rel_tstamp = 0x400            # Use Relative Timestamps. This will increase performance
        slow_start = 0x2000           # Use slow-start logic. This ramps up
        udp_checksum = 0x4000         # Use UDP Checksums.
        use_gw_mac = 0x1000           # Use default gateway's MAC for destination MAC.
        use_tcp = 0x8000              # Use TCP instead of UDP protocol. (Note this is NOT stateful TCP!)

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetArmInfoArmFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_arm_info(self, 
                          arm_flags: str = None,      # Armageddon-related flags, see above for details.
                          burst: str = None,          # Burst amount, can significantly improve throughput with some
                          # modern drivers, similar to 'multi_pkts', and uses the
                          # 'xmit_more' linux skb option.
                          dst_mac: str = None,        # The destination MAC address.
                          dst_mac_count: str = None,  # How many destination MACs to iterate through.
                          ip_dst_max: str = None,     # Maximum destination IP address to use.
                          ip_dst_min: str = None,     # Minimum destination IP address to use.
                          ip_src_max: str = None,     # Maximum source IP address to use.
                          ip_src_min: str = None,     # Minimum source IP address to use.
                          max_pkt_size: str = None,   # Maximum packet size, including all Ethernet headers (but not
                          # CRC).
                          min_pkt_size: str = None,   # Minimum packet size, including all Ethernet headers (but not
                          # CRC).
                          multi_pkts: str = None,     # The number of identical packets to send before creating a new
                          # one.
                          name: str = None,           # Name of the Endpoint we are setting. [R]
                          pkts_to_send: str = None,   # The number of packets to send. Set to zero for infinite.
                          src_mac: str = None,        # The source MAC address.
                          src_mac_count: str = None,  # How many source MACs to iterate through.
                          udp_dst_max: str = None,    # Minimum destination UDP port.
                          udp_dst_min: str = None,    # Minimum destination UDP port.
                          udp_src_max: str = None,    # Maximum source UDP port.
                          udp_src_min: str = None,    # Minimum source UDP port.
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_arm_info(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if arm_flags is not None:
            data["arm_flags"] = arm_flags
        if burst is not None:
            data["burst"] = burst
        if dst_mac is not None:
            data["dst_mac"] = dst_mac
        if dst_mac_count is not None:
            data["dst_mac_count"] = dst_mac_count
        if ip_dst_max is not None:
            data["ip_dst_max"] = ip_dst_max
        if ip_dst_min is not None:
            data["ip_dst_min"] = ip_dst_min
        if ip_src_max is not None:
            data["ip_src_max"] = ip_src_max
        if ip_src_min is not None:
            data["ip_src_min"] = ip_src_min
        if max_pkt_size is not None:
            data["max_pkt_size"] = max_pkt_size
        if min_pkt_size is not None:
            data["min_pkt_size"] = min_pkt_size
        if multi_pkts is not None:
            data["multi_pkts"] = multi_pkts
        if name is not None:
            data["name"] = name
        if pkts_to_send is not None:
            data["pkts_to_send"] = pkts_to_send
        if src_mac is not None:
            data["src_mac"] = src_mac
        if src_mac_count is not None:
            data["src_mac_count"] = src_mac_count
        if udp_dst_max is not None:
            data["udp_dst_max"] = udp_dst_max
        if udp_dst_min is not None:
            data["udp_dst_min"] = udp_dst_min
        if udp_src_max is not None:
            data["udp_src_max"] = udp_src_max
        if udp_src_min is not None:
            data["udp_src_min"] = udp_src_min
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_arm_info",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ATTENUATOR> type requests

        https://www.candelatech.com/lfcli_ug.php#set_attenuator
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetAttenuatorMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_0 = "0"    # Normal
        p_1 = "1"    # Pulse mode (API Tech 4205A modules directly connected via USB only)

    def post_set_attenuator(self, 
                            atten_idx: str = None,          # Attenuator index, or 'all'. [W]
                            mode: str = None,               # 0 == normal attenuator, 1 == pulse mode (API Tech 4205A
                            # modules directly connected via USB only)
                            pulse_count: str = None,        # Number of pulses (0-255)
                            pulse_interval_ms: str = None,  # Time between pulses, in mili-seconds (0-60000).
                            pulse_time_ms: str = None,      # Time interval between pulse groups in miliseconds
                            # (1-60000)
                            pulse_width_us5: str = None,    # Pulse width in units of 1/2 micro second. So, if you want
                            # 1.5us, use value 3 (0-60000)
                            resource: int = None,           # Resource number. [W]
                            serno: str = None,              # Serial number for requested Attenuator, or 'all'. [W]
                            shelf: int = 1,                 # Shelf number, usually 1. [R][D:1]
                            val: str = None,                # Requested attenution in 1/10ths of dB (ddB). [W]
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_attenuator(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if atten_idx is not None:
            data["atten_idx"] = atten_idx
        if mode is not None:
            data["mode"] = mode
        if pulse_count is not None:
            data["pulse_count"] = pulse_count
        if pulse_interval_ms is not None:
            data["pulse_interval_ms"] = pulse_interval_ms
        if pulse_time_ms is not None:
            data["pulse_time_ms"] = pulse_time_ms
        if pulse_width_us5 is not None:
            data["pulse_width_us5"] = pulse_width_us5
        if resource is not None:
            data["resource"] = resource
        if serno is not None:
            data["serno"] = serno
        if shelf is not None:
            data["shelf"] = shelf
        if val is not None:
            data["val"] = val
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_attenuator",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_CHAMBER> type requests

        https://www.candelatech.com/lfcli_ug.php#set_chamber
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_chamber(self, 
                         chamber: str = None,       # Chamber name [W]
                         cur_rotation: str = None,  # Primarily used to store the last known rotation for turntables
                         # that do not report absolute position.
                         position: str = None,      # Absolute position in degrees.
                         speed_rpm: str = None,     # Speed in rpm (floating point number is accepted
                         tilt: str = None,          # Absolute tilt in degrees.
                         turntable: str = None,     # Turn-table address, for instance: 192.168.1.22:3001
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_chamber(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if chamber is not None:
            data["chamber"] = chamber
        if cur_rotation is not None:
            data["cur_rotation"] = cur_rotation
        if position is not None:
            data["position"] = position
        if speed_rpm is not None:
            data["speed_rpm"] = speed_rpm
        if tilt is not None:
            data["tilt"] = tilt
        if turntable is not None:
            data["turntable"] = turntable
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_chamber",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_CX_REPORT_TIMER> type requests

        https://www.candelatech.com/lfcli_ug.php#set_cx_report_timer
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_cx_report_timer(self, 
                                 cx_name: str = None,       # Name of cross-connect, or 'all'. [W]
                                 cxonly: str = None,        # If you want to set the timer for ONLY the CX, and not
                                 milliseconds: str = None,  # Report timer length in milliseconds.
                                 # [W,250-60000][D:5000]
                                 test_mgr: str = None,      # Name of the test manager, or 'all'. [W]
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_cx_report_timer(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cx_name is not None:
            data["cx_name"] = cx_name
        if cxonly is not None:
            data["cxonly"] = cxonly
        if milliseconds is not None:
            data["milliseconds"] = milliseconds
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_cx_report_timer",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_CX_STATE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_cx_state
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetCxStateCxState(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        DELETED = "DELETED"    # Deletes the CX(s).
        QUIESCE = "QUIESCE"    # Stop transmitting and gracefully stop cross-connect.
        RUNNING = "RUNNING"    # Sets the CX(s) in the running state.
        STOPPED = "STOPPED"    # Sets the CX(s) in the stopped state.
        SWITCH = "SWITCH"      # Sets the CX(s) in the running state, stopping any conflicting tests.

    def post_set_cx_state(self, 
                          cx_name: str = None,   # Name of the cross-connect, or 'all'. [W]
                          cx_state: str = None,  # One of: RUNNING, SWITCH, QUIESCE, STOPPED, or DELETED. [W]
                          test_mgr: str = None,  # Name of the test-manager, or 'all'. [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_cx_state(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cx_name is not None:
            data["cx_name"] = cx_name
        if cx_state is not None:
            data["cx_state"] = cx_state
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_cx_state",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_ADDR> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_addr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_addr(self, 
                           ip: str = None,        # The IP Address. Used for TCP/IP and UDP/IP protocols.
                           mac: str = None,       # The MAC address. Only needed for LANforge protocol Endpoints.
                           max_port: str = None,  # The Maximum IP Port. Used for TCP/IP and UDP/IP protocols.
                           min_port: str = None,  # The Minimum IP Port. Used for TCP/IP and UDP/IP protocols.
                           name: str = None,      # The name of the endpoint we are configuring. [R]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_addr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ip is not None:
            data["ip"] = ip
        if mac is not None:
            data["mac"] = mac
        if max_port is not None:
            data["max_port"] = max_port
        if min_port is not None:
            data["min_port"] = min_port
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_addr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_DETAILS> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_details
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_details(self, 
                              conn_timeout: str = None,      # For TCP, the max time in miliseconds to wait for
                              # connection to establish.
                              dst_mac: str = None,           # Destination MAC address, used for custom Ethernet
                              # replays.
                              max_conn_timer: str = None,    # The maximum duration (in ms) this connection should run
                              # before re-establishing.
                              max_ip_port: str = None,       # The maximum IP Port value. (The value for min ip port is
                              # set through the add_endp/ip_port parameter.) If greater
                              # than min, each connection will use a random value
                              # between min and max.
                              max_reconn_pause: str = None,  # The maximum time between re-connects, in ms.
                              mcast_src_ip: str = None,      # Multicast source address (used in SSM mode, multicast
                              # endpoints only)
                              mcast_src_port: str = None,    # Multicast source address (used in SSM mode, multicast
                              # endpoints only)
                              min_conn_timer: str = None,    # The minimum duration (in ms) this connection should run
                              # before re-establishing.
                              min_reconn_pause: str = None,  # The minimum time between re-connects, in ms.
                              name: str = None,              # The name of the endpoint we are configuring. [R]
                              pkts_to_send: str = None,      # Number of packets to send before stopping. 0 means
                              # infinite.
                              rcvbuf_size: str = None,       # The receive buffer (window) size. Zero for AUTO
                              sndbuf_size: str = None,       # The sending buffer (window) size. Zero for AUTO
                              tcp_delack_segs: str = None,   # NA: No longer supported.
                              tcp_max_delack: str = None,    # NA: No longer supported.
                              tcp_min_delack: str = None,    # NA: No longer supported.
                              tcp_mss: str = None,           # TCP Maximum Segment Size, affects packet size on the
                              # wire (88 - 32767).
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_details(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if conn_timeout is not None:
            data["conn_timeout"] = conn_timeout
        if dst_mac is not None:
            data["dst_mac"] = dst_mac
        if max_conn_timer is not None:
            data["max_conn_timer"] = max_conn_timer
        if max_ip_port is not None:
            data["max_ip_port"] = max_ip_port
        if max_reconn_pause is not None:
            data["max_reconn_pause"] = max_reconn_pause
        if mcast_src_ip is not None:
            data["mcast_src_ip"] = mcast_src_ip
        if mcast_src_port is not None:
            data["mcast_src_port"] = mcast_src_port
        if min_conn_timer is not None:
            data["min_conn_timer"] = min_conn_timer
        if min_reconn_pause is not None:
            data["min_reconn_pause"] = min_reconn_pause
        if name is not None:
            data["name"] = name
        if pkts_to_send is not None:
            data["pkts_to_send"] = pkts_to_send
        if rcvbuf_size is not None:
            data["rcvbuf_size"] = rcvbuf_size
        if sndbuf_size is not None:
            data["sndbuf_size"] = sndbuf_size
        if tcp_delack_segs is not None:
            data["tcp_delack_segs"] = tcp_delack_segs
        if tcp_max_delack is not None:
            data["tcp_max_delack"] = tcp_max_delack
        if tcp_min_delack is not None:
            data["tcp_min_delack"] = tcp_min_delack
        if tcp_mss is not None:
            data["tcp_mss"] = tcp_mss
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_details",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_FILE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_file
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetEndpFilePlayback(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        OFF = "OFF"    # off
        ON = "ON"      # on

    def post_set_endp_file(self, 
                           file: str = None,      # The file name to read the playback packets from.
                           name: str = None,      # The name of the endpoint we are configuring. [R]
                           playback: str = None,  # Should we playback the capture or not? ON or OFF. [R]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_file(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if file is not None:
            data["file"] = file
        if name is not None:
            data["name"] = name
        if playback is not None:
            data["playback"] = playback
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_file",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_FLAG> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_flag
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetEndpFlagFlag(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        AutoHelper = "AutoHelper"                          # Automatically run on helper process
        ClearPortOnStart = "ClearPortOnStart"              # clear stats on start
        DoChecksum = "DoChecksum"                          # Enable checksumming
        EnableConcurrentSrcIP = "EnableConcurrentSrcIP"    # Concurrent source IPs?
        EnableLinearSrcIP = "EnableLinearSrcIP"            # linearized source IPs
        EnableLinearSrcIPPort = "EnableLinearSrcIPPort"    # linearized IP ports
        EnableRndSrcIP = "EnableRndSrcIP"                  # randomize source IP
        KernelMode = "KernelMode"                          # Enable kernel mode
        QuiesceAfterDuration = "QuiesceAfterDuration"      # quiesce after time period
        QuiesceAfterRange = "QuiesceAfterRange"            # quiesce after range of bytes
        Unmanaged = "Unmanaged"                            # Set endpoint unmanaged
        UseAutoNAT = "UseAutoNAT"                          # NAT friendly behavior

    def post_set_endp_flag(self, 
                           flag: str = None,  # The name of the flag. [R]
                           name: str = None,  # The name of the endpoint we are configuring. [R]
                           val: str = None,   # Either 1 (for on), or 0 (for off). [R,0-1]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_flag(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if flag is not None:
            data["flag"] = flag
        if name is not None:
            data["name"] = name
        if val is not None:
            data["val"] = val
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_flag",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_PAYLOAD> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_payload
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetEndpPayloadPayloadType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        PRBS_11_8_10 = "PRBS_11_8_10"    # PRBS (see above)
        PRBS_15_0_14 = "PRBS_15_0_14"    # PRBS (see above)
        PRBS_4_0_3 = "PRBS_4_0_3"        # Use linear feedback shift register to generate pseudo random sequence.
        PRBS_7_0_6 = "PRBS_7_0_6"        # PRBS (see above)
        custom = "custom"                # Enter your own payload with the set_endp_payload
        decreasing = "decreasing"        # bytes start at FF and decrease, wrapping if needed.
        increasing = "increasing"        # bytes start at 00 and increase, wrapping if needed.
        ones = "ones"                    # Payload is all ones (FF).
        random = "random"                # generate a new random payload each time sent.
        random_fixed = "random_fixed"    # means generate one random payload, and send it over and over again.
        zeros = "zeros"                  # Payload is all zeros (00).

    def post_set_endp_payload(self, 
                              name: str = None,          # The name of the endpoint we are configuring. [R]
                              payload: str = None,       # For custom payloads, enter the payload in hex, up to 2048
                              # bytes. <tt escapearg='false'>Unescaped Value</tt>
                              payload_type: str = None,  # The payload type. See help for add_endp. [W][D:increasing]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_payload(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if payload is not None:
            data["payload"] = payload
        if payload_type is not None:
            data["payload_type"] = payload_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_payload",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_PLD_BOUNDS> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_pld_bounds
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_pld_bounds(self, 
                                 is_random: str = None,     # YES if random, anything else for NO.
                                 max_pld_size: str = None,  # The maximum payload size, in bytes.
                                 min_pld_size: str = None,  # The minimum payload size, in bytes.
                                 name: str = None,          # The name of the endpoint we are configuring. [R]
                                 use_checksum: str = None,  # YES if use checksum on payload, anything else for NO.
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_pld_bounds(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if is_random is not None:
            data["is_random"] = is_random
        if max_pld_size is not None:
            data["max_pld_size"] = max_pld_size
        if min_pld_size is not None:
            data["min_pld_size"] = min_pld_size
        if name is not None:
            data["name"] = name
        if use_checksum is not None:
            data["use_checksum"] = use_checksum
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_pld_bounds",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_PROXY> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_proxy
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_proxy(self, 
                            enabled: str = None,        # YES or NO to enable or disable proxying.
                            endp_name: str = None,      # Name of endpoint. [W]
                            proxy_ip: str = None,       # Proxy IP Address.
                            proxy_ip_port: str = None,  # Proxy IP Port.
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_proxy(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if enabled is not None:
            data["enabled"] = enabled
        if endp_name is not None:
            data["endp_name"] = endp_name
        if proxy_ip is not None:
            data["proxy_ip"] = proxy_ip
        if proxy_ip_port is not None:
            data["proxy_ip_port"] = proxy_ip_port
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_proxy",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_QUIESCE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_quiesce
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_quiesce(self, 
                              name: str = None,     # The name of the endpoint we are configuring. [R]
                              quiesce: str = None,  # The number of seconds to quiesce this endpoint when told to
                              # quiesce. [R]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_quiesce(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if quiesce is not None:
            data["quiesce"] = quiesce
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_quiesce",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_REPORT_TIMER> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_report_timer
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_report_timer(self, 
                                   endp_name: str = None,     # Name of endpoint. [R]
                                   milliseconds: str = None,  # Report timer length in milliseconds.
                                   # [W,250-60000][D:5000]
                                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_report_timer(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if milliseconds is not None:
            data["milliseconds"] = milliseconds
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_report_timer",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_TOS> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_tos
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetEndpTosTos(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        LOWCOST = "LOWCOST"            #
        LOWDELAY = "LOWDELAY"          #
        RELIABILITY = "RELIABILITY"    #
        THROUGHPUT = "THROUGHPUT"      #

    def post_set_endp_tos(self, 
                          name: str = None,      # The name of the endpoint we are configuring. [R]
                          priority: str = None,  # The socket priority, can be any positive number.
                          tos: str = None,       # The Type of Service, can be HEX, see above.
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_tos(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if priority is not None:
            data["priority"] = priority
        if tos is not None:
            data["tos"] = tos
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_tos",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_ENDP_TX_BOUNDS> type requests

        https://www.candelatech.com/lfcli_ug.php#set_endp_tx_bounds
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_endp_tx_bounds(self, 
                                is_bursty: str = None,    # YES if bursty, anything else for NO.
                                max_tx_rate: str = None,  # The maximum transmit rate, in bits per second (bps).
                                min_tx_rate: str = None,  # The minimum transmit rate, in bits per second (bps).
                                name: str = None,         # The name of the endpoint we are configuring. [R]
                                debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_endp_tx_bounds(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if is_bursty is not None:
            data["is_bursty"] = is_bursty
        if max_tx_rate is not None:
            data["max_tx_rate"] = max_tx_rate
        if min_tx_rate is not None:
            data["min_tx_rate"] = min_tx_rate
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_endp_tx_bounds",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_EVENT_INTEREST> type requests

        https://www.candelatech.com/lfcli_ug.php#set_event_interest
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetEventInterestEiFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetEventInterestEiFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        CLEAR = 0x0      # will clear interest
        SET = 0x1        # set interest flag

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetEventInterestEiFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetEventInterestEvents1(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetEventInterestEvents10, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BAD_TOS = 0x400000                        # Endpoint has bad ToS values configured.
        Bad_MAC = 0x100000                        # Invalid MAC address configured.
        Cleared = 0x2000                          # Counters were cleared for some entity.
        Connect = 0x100                           # WiFi interface connected to AP.
        Custom = 0x4                              # Custom event (generated by USER in GUI or CLI).
        DHCP_Fail = 0x8000                        # DHCP Failed, maybe out of leases?
        DHCP_Timeout = 0x10000                    # Timed out talking to DHCP server.
        DHCP4_Error = 0x20000                     # DHCP gave out duplicated IP address.
        DHCP6_Error = 0x40000                     # DHCPv6 gave out duplicated IPv6 address.
        Disconnect = 0x80                         # WiFi interface disconnected from AP.
        Endp_Started = 0x40                       # Endpoint was started.
        Endp_Stopped = 0x20                       # Endpoint stopped for some reason.
        Link_Down = 0x1                           # Notify when Interface Link goes DOWN.
        Link_Errors = 0x4000                      # Port shows low-level link errors.
        Link_Up = 0x2                             # Notify when Interface Link goes UP.
        Login = 0x400                             # CLI/GUI user connected to LANforge.
        Logout = 0x200                            # CLI/GUI user disconnected from LANforge.
        Migrated = 0x200000                       # Port (station network interface) migrated.
        NO_RX_SINCE = 0x800000                    # Endpoint threshold alert.
        NO_RX_SINCE_CLEARED = 0x1000000           # Endpoint threshold alert cleared.
        RX_BPS_OOR_1M = 0x20000000                # Endpoint threshold alert.
        RX_BPS_OOR_1M_CLEARED = 0x40000000        # Endpoint threshold alert cleared.
        RX_BPS_OOR_30S = 0x8000000                # Endpoint threshold alert.
        RX_BPS_OOR_30S_CLEARED = 0x10000000       # Endpoint threshold alert cleared.
        RX_BPS_OOR_3S = 0x2000000                 # Endpoint threshold alert.
        RX_BPS_OOR_3S_CLEARED = 0x4000000         # Endpoint threshold alert cleared.
        Resource_Down = 0x8                       # Resource has crashed, rebooted, etc.
        Resource_Up = 0x10                        # Resource has connected to manager.
        Start_Reports = 0x1000                    # Start saving report data files (CSV).
        Stop_Reports = 0x800                      # Stop saving report data files (CSV).
        TX_BPS_OOR_3S = 0x80000000                # Endpoint threshold alert.
        WiFi_Config = 0x80000                     # WiFi Configuration Error.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetEventInterestEvents1 has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetEventInterestEvents2(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetEventInterestEvents20, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        FW_CRASH = 0x800                     # Firmware for entity has crashed.
        FW_FAIL = 0x1000                     # Firmware failed powerup, may require reboot.
        IFDOWN_FAIL = 0x8000                 # IFDOWN-PRE Script (ifup --logout) returned error code.
        IFDOWN_OK = 0x10000                  # IFDOWN-PRE Script (ifup --logout) completed successfully.
        IFUP_FAIL = 0x2000                   # IFUP-POST Script returned error code.
        IFUP_OK = 0x4000                     # IFUP-POST Script completed successfully.
        RX_DROP_OOR_1M = 0x200               # Endpoint threshold alert.
        RX_DROP_OOR_1M_CLEARED = 0x400       # Endpoint threshold alert cleared.
        RX_DROP_OOR_3S = 0x80                # Endpoint threshold alert.
        RX_DROP_OOR_3S_CLEARED = 0x100       # Endpoint threshold alert cleared.
        RX_LAT_OOR = 0x20                    # Endpoint threshold alert.
        RX_LAT_OOR_CLEARED = 0x40            # Endpoint threshold alert cleared.
        TX_BPS_OOR_1M = 0x8                  # Endpoint threshold alert.
        TX_BPS_OOR_1M_CLEARED = 0x10         # Endpoint threshold alert cleared.
        TX_BPS_OOR_30S = 0x2                 # Endpoint threshold alert.
        TX_BPS_OOR_30S_CLEARED = 0x4         # Endpoint threshold alert cleared.
        TX_BPS_OOR_3S_CLEARED = 0x1          # Endpoint threshold alert cleared.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetEventInterestEvents2 has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_event_interest(self, 
                                ei_flags: str = None,   # Event Interest flags, see above. [W]
                                event_cnt: str = None,  # Maximum number of events to store.
                                events1: str = None,    # See description for possible values.
                                events2: str = None,    # See description for possible values.
                                events3: str = None,    # See description for possible values.
                                events4: str = None,    # See description for possible values.
                                var1: str = None,       # Currently un-used.
                                debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_event_interest(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ei_flags is not None:
            data["ei_flags"] = ei_flags
        if event_cnt is not None:
            data["event_cnt"] = event_cnt
        if events1 is not None:
            data["events1"] = events1
        if events2 is not None:
            data["events2"] = events2
        if events3 is not None:
            data["events3"] = events3
        if events4 is not None:
            data["events4"] = events4
        if var1 is not None:
            data["var1"] = var1
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_event_interest",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_EVENT_PRIORITY> type requests

        https://www.candelatech.com/lfcli_ug.php#set_event_priority
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetEventPriorityEvent(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        Bad_MAC = 20            # Invalid MAC address configured.
        Cleared = 13            # Counters were cleared for some entity.
        Connect = 8             # WiFi interface connected to AP.
        Custom = 2              # Custom event (generated by USER in GUI or CLI).
        DHCP_Fail = 15          # DHCP Failed, maybe out of leases?
        DHCP_Timeout = 16       # Timed out talking to DHCP server.
        DHCP4_Error = 17        # DHCP gave out duplicated IP address.
        DHCP6_Error = 18        # DHCPv6 gave out duplicated IPv6 address.
        Disconnect = 7          # WiFi interface disconnected from AP.
        Endp_Started = 6        # Endpoint was started.
        Endp_Stopped = 5        # Endpoint stopped for some reason.
        Link_Down = 0           # Notify when Interface Link goes UP.
        Link_Errors = 14        # Port shows low-level link errors.
        Link_Up = 1             # Notify when Interface Link goes DOWN.
        Login = 10              # CLI/GUI user connected to LANforge.
        Logout = 9              # CLI/GUI user disconnected from LANforge.
        Migrated = 21           # Port (station network interface) migrated.
        Resource_Down = 3       # Resource has crashed, rebooted, etc.
        Resource_Up = 4         # Resource has connected to manager.
        Start_Reports = 12      # Start saving report data files (CSV).
        Stop_Reports = 11       # Stop saving report data files (CSV).
        WiFi_Config = 19        # WiFi Configuration Error.

    class SetEventPriorityPriority(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        AUTO = "AUTO"            # Let event creator decide the priority.
        CRITICAL = "CRITICAL"    #
        DEBUG = "DEBUG"          #
        FATAL = "FATAL"          #
        INFO = "INFO"            #
        WARNING = "WARNING"      #

    def post_set_event_priority(self, 
                                event: str = None,     # Number or name for the event, see above. [R,0-21]
                                priority: str = None,  # Number or name for the priority. [R,0-5]
                                debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_event_priority(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if event is not None:
            data["event"] = event
        if priority is not None:
            data["priority"] = priority
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_event_priority",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_FE_INFO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_fe_info
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_fe_info(self, 
                         directory: str = None,            # The directory to read/write in. Absolute path suggested.
                         io_direction: str = None,         # Should we be reading or writing: options: read, write
                         max_file_size: str = None,        # The maximum file size, in bytes.
                         max_rw_sz: str = None,            # Maximum read/write size, in bytes.
                         min_file_size: str = None,        # The minimum file size, in bytes.
                         min_rw_sz: str = None,            # Minimum read/write size, in bytes.
                         name: str = None,                 # The name of the file endpoint we are configuring. [R]
                         num_files: str = None,            # Number of files to create when writing.
                         prefix: str = None,               # The prefix of the file(s) to read/write.
                         quiesce_after_files: str = None,  # If non-zero, quiesce test after this many files have been
                         # read/written.
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_fe_info(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if directory is not None:
            data["directory"] = directory
        if io_direction is not None:
            data["io_direction"] = io_direction
        if max_file_size is not None:
            data["max_file_size"] = max_file_size
        if max_rw_sz is not None:
            data["max_rw_sz"] = max_rw_sz
        if min_file_size is not None:
            data["min_file_size"] = min_file_size
        if min_rw_sz is not None:
            data["min_rw_sz"] = min_rw_sz
        if name is not None:
            data["name"] = name
        if num_files is not None:
            data["num_files"] = num_files
        if prefix is not None:
            data["prefix"] = prefix
        if quiesce_after_files is not None:
            data["quiesce_after_files"] = quiesce_after_files
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_fe_info",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_FLAG> type requests

        https://www.candelatech.com/lfcli_ug.php#set_flag
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetFlagFlag(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        brief = "brief"                              # Request more abbreviated output to various commands.
        prompt_newlines = "prompt_newlines"          # Add a newline after every prompt. Can help with scripts
        push_all_rpts = "push_all_rpts"              # If enabled, server will send port, endpoint, and other
        push_endp_rpts = "push_endp_rpts"            # If enabled, server will send endpoint reports without
        request_keyed_text = "request_keyed_text"    # Normally most keyed-text events are only sent to the GUI
        stream_events = "stream_events"              # Normally the CLI will not show Events (as seen in the
        # +Event

    def post_set_flag(self, 
                      client: str = None,  # Specify the user, if it is not the current user. Requires admin
                      # privileges.
                      flag: str = None,    # The name of the flag. [R]
                      val: str = None,     # Either 1 (for on), or 0 (for off). [R,0-1]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_flag(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if client is not None:
            data["client"] = client
        if flag is not None:
            data["flag"] = flag
        if val is not None:
            data["val"] = val
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_flag",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_GEN_CMD> type requests

        https://www.candelatech.com/lfcli_ug.php#set_gen_cmd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_gen_cmd(self, 
                         command: str = None,  # The rest of the command line arguments. <tt
                         # escapearg='false'>Unescaped Value</tt> [R]
                         name: str = None,     # The name of the file endpoint we are configuring. [R]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_gen_cmd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if command is not None:
            data["command"] = command
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_gen_cmd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_GPS_INFO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_gps_info
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_gps_info(self, 
                          altitude: str = None,   # Altitude, assumes units are Meters.
                          ew: str = None,         # East or west (Longitude).
                          lattitude: str = None,  # The lattitude, as read from a GPS device.
                          longitude: str = None,  # The longitude, as ready from a GPS device.
                          ns: str = None,         # North or South (Latitude).
                          resource: int = None,   # Resource number for the port to be modified. [W]
                          shelf: int = 1,         # Shelf number for the port to be modified, or SELF. [R][D:1]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_gps_info(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if altitude is not None:
            data["altitude"] = altitude
        if ew is not None:
            data["ew"] = ew
        if lattitude is not None:
            data["lattitude"] = lattitude
        if longitude is not None:
            data["longitude"] = longitude
        if ns is not None:
            data["ns"] = ns
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_gps_info",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_IFUP_SCRIPT> type requests

        https://www.candelatech.com/lfcli_ug.php#set_ifup_script
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_ifup_script(self, 
                             flags: str = None,             # Currently un-defined, use NA
                             port: str = None,              # WiFi interface name or number. [W]
                             post_ifup_script: str = None,  # Script name with optional args, will run after interface
                             # comes up and gets IP.
                             resource: int = None,          # Resource number. [W]
                             shelf: int = 1,                # Shelf number. [R][D:1]
                             debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_ifup_script(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if flags is not None:
            data["flags"] = flags
        if port is not None:
            data["port"] = port
        if post_ifup_script is not None:
            data["post_ifup_script"] = post_ifup_script
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_ifup_script",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_LICENSE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_license
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_license(self, 
                         licenses: str = None,  # License keys all appended into a single line. <tt
                         # escapearg='false'>Unescaped Value</tt> [W]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_license(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if licenses is not None:
            data["licenses"] = licenses
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_license",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_MC_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#set_mc_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_mc_endp(self, 
                         mcast_dest_port: str = None,  # Multicast destination IP Port, for example: 55000
                         mcast_group: str = None,      # Multicast group IP, ie: 224.1.1.2 IPv6 supported as well.
                         name: str = None,             # The name of the endpoint we are configuring. [R]
                         rcv_mcast: str = None,        # Should we attempt to receive? Values: Yes or No
                         ttl: str = None,              # Time to live for the multicast packets generated.
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_mc_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if mcast_dest_port is not None:
            data["mcast_dest_port"] = mcast_dest_port
        if mcast_group is not None:
            data["mcast_group"] = mcast_group
        if name is not None:
            data["name"] = name
        if rcv_mcast is not None:
            data["rcv_mcast"] = rcv_mcast
        if ttl is not None:
            data["ttl"] = ttl
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_mc_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_PASSWORD> type requests

        https://www.candelatech.com/lfcli_ug.php#set_password
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_password(self, 
                          client: str = None,        # Specify the client. If left blank, will use current client.
                          new_password: str = None,  # New password, or 'NA' for blank password. [W]
                          old_password: str = None,  # Old password, or 'NA' for blank password. [W]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_password(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if client is not None:
            data["client"] = client
        if new_password is not None:
            data["new_password"] = new_password
        if old_password is not None:
            data["old_password"] = old_password
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_password",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_POLL_MODE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_poll_mode
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetPollModeMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        polling = "polling"    #
        push = "push"          #

    def post_set_poll_mode(self, 
                           mode: str = None,  # 'polling' or 'push'. [R]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_poll_mode(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if mode is not None:
            data["mode"] = mode
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_poll_mode",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_PORT> type requests

        https://www.candelatech.com/lfcli_ug.php#set_port
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetPortCmdFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetPortCmdFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        abort_if_scripts = 0x400       # Forceably abort all ifup/down scripts on this Port.
        force_MII_probe = 0x4          # Force MII probe
        from_dhcp = 0x200              # Settings come from DHCP client.
        from_user = 0x80               # from_user (Required to change Mgt Port config
        new_gw_probe = 0x20            # Force new GW probe
        new_gw_probe_dev = 0x40        # Force new GW probe for ONLY this interface
        no_hw_probe = 0x8              # Don&apos;t probe hardware
        probe_wifi = 0x10              # Probe WIFI
        reset_transceiver = 0x1        # Reset transciever
        restart_link_neg = 0x2         # Restart link negotiation
        skip_port_bounce = 0x100       # skip-port-bounce (Don&apos;t ifdown/up
        use_pre_ifdown = 0x800         # Call pre-ifdown script before bringing interface down.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetPortCmdFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetPortCurrentFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetPortCurrentFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        adv_100bt_fd = 0x800000                       # advert-100bt-FD
        adv_100bt_hd = 0x400000                       # advert-100bt-HD
        adv_10bt_fd = 0x200000                        # advert-10bt-FD
        adv_10bt_hd = 0x100000                        # advert-10bt-HD
        adv_10g_fd = 0x800000000                      # advert-10G-FD
        adv_2_5g_fd = 0x400000000                     # advert-2.5G-FD
        adv_5g_fd = 0x400000000000000                 # Advertise 5Gbps link speed.
        adv_flow_ctl = 0x8000000                      # advert-flow-control
        auto_neg = 0x100                              # auto-negotiate
        aux_mgt = 0x800000000000                      # Enable Auxillary-Management flag for this port.
        fixed_100bt_fd = 0x10                         # Fixed-100bt-FD
        fixed_100bt_hd = 0x8                          # Fixed-100bt-HD
        fixed_10bt_fd = 0x4                           # Fixed-10bt-FD
        fixed_10bt_hd = 0x2                           # Fixed-10bt-HD (half duplex)
        ftp_enabled = 0x400000000000                  # Enable FTP (vsftpd) service for this port.
        gro_enabled = 0x4000000000                    # GRO-Enabled
        gso_enabled = 0x10000000000                   # GSO-Enabled
        http_enabled = 0x200000000000                 # Enable HTTP (nginx) service for this port.
        if_down = 0x1                                 # Interface Down
        ignore_dhcp = 0x2000000000000                 # Don&apos;t set DHCP acquired IP on interface,
        ipsec_client = 0x40000000000000               # Enable client IPSEC xfrm on this port.
        ipsec_concentrator = 0x80000000000000         # Enable concentrator (upstream) IPSEC xfrm on this port.
        lro_enabled = 0x2000000000                    # LRO-Enabled
        no_dhcp_rel = 0x80000000000                   # No-DHCP-Release
        no_dhcp_restart = 0x1000000000000             # Disable restart of DHCP on link connect (ie, wifi).
        no_ifup_post = 0x4000000000000                # Skip ifup-post script if we can detect that we
        promisc = 0x10000000                          # PROMISC
        radius_enabled = 0x20000000000000             # Enable RADIUS service (using hostapd as radius server)
        rxfcs = 0x40000000000                         # RXFCS
        service_dns = 0x100000000000000               # Enable DNS (dnsmasq) service on this port.
        staged_ifup = 0x100000000000                  # Staged-IFUP
        tso_enabled = 0x1000000000                    # TSO-Enabled
        ufo_enabled = 0x8000000000                    # UFO-Enabled
        use_dhcp = 0x80000000                         # USE-DHCP
        use_dhcpv6 = 0x20000000000                    # USE-DHCPv6

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetPortCurrentFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetPortDhcpClientId(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NA = "NA"                   # Do not change from current value.
        NONE = "NONE"               # Do not use dhcp client ID.
        p_string_ = "[string]"      # Use the string for the client ID.
        p__DEVNAME = "__DEVNAME"    # Use the interface&apos;s name as the client ID.
        p__MAC = "__MAC"            # Use interface&apos;s MAC address for the client ID.

    class SetPortDhcpHostname(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NA = "NA"                   # Do not change from current value.
        NONE = "NONE"               # Do not use dhcp Hostname
        p_string_ = "[string]"      # Use the string for the Hostname.
        p__ALIAS__ = "__ALIAS__"    # Use alias if set, or EID behaviour if alias is not set..
        p__EID__ = "__EID__"        # Use hostname 'CT-[resource-id].[port-name]'

    class SetPortDhcpVendorId(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NA = "NA"                 # Do not change from current value.
        NONE = "NONE"             # Do not use dhcp vendor ID
        p_string_ = "[string]"    # Use the string for the vendor ID.

    class SetPortFlags2(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetPortFlags20, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        bypass_disconnect = 0x200      # Logically disconnect the cable (link-down)
        bypass_enabled = 0x10          # Enable Bypass Device
        bypass_power_down = 0x80       # Should bypass be on when we shutdown or loose power?
        bypass_power_on = 0x100        # Should bypass be on when we first power up?
        supports_bypass = 0x2          # Support Bypass Devices
        use_stp = 0x1                  # Use Spanning Tree Protocol

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetPortFlags2 has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetPortInterest(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetPortInterest0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        alias = 0x1000                     # Port alias
        aux_mgt = 0x20000000               # Enable/disable Auxillary-Management for a port
        bridge = 0x10000                   # BRIDGE
        bypass = 0x40000                   # Bypass
        command_flags = 0x1                # apply command flags
        cpu_mask = 0x100000                # CPU Mask, useful for pinning process to CPU core
        current_flags = 0x2                # apply current flags
        dhcp = 0x4000                      # including client-id.
        dhcp_rls = 0x4000000               # DHCP release
        dhcpv6 = 0x1000000                 # Use DHCPv6
        gen_offload = 0x80000              # Generic offload flags, everything but LRO
        ifdown = 0x800000                  # Down interface
        interal_use_1 = 0x800              # (INTERNAL USE)
        ip_Mask = 0x8                      # IP mask
        ip_address = 0x4                   # IP address
        ip_gateway = 0x10                  # IP gateway
        ipv6_addrs = 0x20000               # IPv6 Address
        link_speed = 0x80                  # Link speed
        lro_offload = 0x200000             # LRO (Must be disabled when used in Wanlink,
        mac_address = 0x20                 # MAC address
        mtu = 0x100                        # MTU
        no_apply_dhcp = 0x80000000         # Enable/disable NO-APPLY-DHCP flag for a port
        no_dhcp_conn = 0x40000000          # Enable/disable NO-DHCP-ON-CONNECT flag for a port
        promisc_mode = 0x400               # PROMISC mode
        rpt_timer = 0x8000                 # Report Timer
        rx_all = 0x2000                    # Rx-ALL
        rxfcs = 0x2000000                  # RXFCS
        skip_ifup_roam = 0x100000000       # Enable/disable SKIP-IFUP-ON-ROAM flag for a port
        sta_br_id = 0x400000               # WiFi Bridge identifier. 0 means no bridging.
        supported_flags = 0x40             # apply supported flags
        svc_ftpd = 0x10000000              # Enable/disable FTP Service for a port
        svc_httpd = 0x8000000              # Enable/disable HTTP Service for a port
        tx_queue_length = 0x200            # TX Queue Length

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetPortInterest has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_port(self, 
                      alias: str = None,                # A user-defined name for this interface. Can be BLANK or NA.
                      br_aging_time: str = None,        # MAC aging time, in seconds, 32-bit number (or peer IP for
                      # GRE).
                      br_forwarding_delay: str = None,  # How long to wait until the bridge will start forwarding
                      # packets.
                      br_hello_time: str = None,        # How often does the bridge send out STP hello packets.
                      br_max_age: str = None,           # How long until STP considers a non-responsive bridge dead.
                      br_port_cost: str = None,         # STP Port cost for a port (this applies only to NON-BRIDGE
                      # interfaces).
                      br_port_priority: str = None,     # STP Port priority for a port (this applies only to NON-BRIDGE
                      # interfaces).
                      br_priority: str = None,          # Bridge priority, 16-bit number.
                      bypass_wdt: str = None,           # Watch Dog Timer (in seconds) for this port. Zero (0) to
                      # disable.
                      cmd_flags: str = None,            # Command Flags: See above, or NA.
                      cpu_mask: str = None,             # CPU Mask for CPUs that should service this interface. Zero is
                      # don't set (let OS make the decision). This value will be
                      # applied to the proper /proc/irq/[irq-num]/smp_affinity file by
                      # the pin_irq.pl script.
                      current_flags: str = None,        # See above, or NA.
                      current_flags_msk: str = None,    # This sets 'interest' for flags 'Enable RADIUS service' and
                      # higher. See above, or NA.
                      dhcp_client_id: str = None,       # Optional string of up to 63 bytes in length to be passed to
                      # the dhclient process. See above.
                      dhcp_hostname: str = None,        # Optional string of up to 63 bytes in length to be passed to
                      # the dhclient process. Option 12, see above.
                      dhcp_vendor_id: str = None,       # Optional string of up to 63 bytes in length to be passed to
                      # the dhclient process. See above.
                      dns_servers: str = None,          # DNS servers for use by traffic on this port, comma-separated
                      # list, BLANK means zero-length string.
                      flags2: str = None,               # Bridge &amp; other flags, see above.
                      gateway: str = None,              # IP address of the gateway device - used for IP routing, or NA.
                      interest: str = None,             # Which things are we really interested in setting. Can
                      # over-ride defaults based on the other arguments.
                      ip_addr: str = None,              # IP address for the port, or NA.
                      ipsec_concentrator: str = None,   # IP Address of IPSec concentrator.
                      ipsec_local_id: str = None,       # Local Identifier for this IPSec tunnel.
                      ipsec_passwd: str = None,         # Password for IPSec, for pubkey, use: pubkey:[pem-file-name],
                      # for instance: pubkey:station.pem
                      ipsec_remote_id: str = None,      # Remote Identifier for this IPSec tunnel.
                      ipv6_addr_global: str = None,     # Global scoped IPv6 address.
                      ipv6_addr_link: str = None,       # Link scoped IPv6 address.
                      ipv6_dflt_gw: str = None,         # IPv6 default gateway.
                      mac: str = None,                  # MAC address to set this port to, or leave blank to not set it,
                      # or NA.
                      mtu: str = None,                  # Maximum Transmit Unit (MTU) for this interface. Can be blank
                      # or NA.
                      netmask: str = None,              # Netmask which this port should use, or NA.
                      port: str = None,                 # Port number for the port to be modified. [W]
                      report_timer: int = None,         # How often, in milliseconds, should we poll stats on this
                      # interface?
                      resource: int = None,             # Resource number for the port to be modified. [W]
                      shelf: int = 1,                   # Shelf number for the port to be modified. [R][D:1]
                      sta_br_id: str = None,            # WiFi STAtion bridge ID. Zero means none.
                      tx_queue_len: str = None,         # Transmit Queue Length for this interface. Can be blank or NA.
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_port(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if br_aging_time is not None:
            data["br_aging_time"] = br_aging_time
        if br_forwarding_delay is not None:
            data["br_forwarding_delay"] = br_forwarding_delay
        if br_hello_time is not None:
            data["br_hello_time"] = br_hello_time
        if br_max_age is not None:
            data["br_max_age"] = br_max_age
        if br_port_cost is not None:
            data["br_port_cost"] = br_port_cost
        if br_port_priority is not None:
            data["br_port_priority"] = br_port_priority
        if br_priority is not None:
            data["br_priority"] = br_priority
        if bypass_wdt is not None:
            data["bypass_wdt"] = bypass_wdt
        if cmd_flags is not None:
            data["cmd_flags"] = cmd_flags
        if cpu_mask is not None:
            data["cpu_mask"] = cpu_mask
        if current_flags is not None:
            data["current_flags"] = current_flags
        if current_flags_msk is not None:
            data["current_flags_msk"] = current_flags_msk
        if dhcp_client_id is not None:
            data["dhcp_client_id"] = dhcp_client_id
        if dhcp_hostname is not None:
            data["dhcp_hostname"] = dhcp_hostname
        if dhcp_vendor_id is not None:
            data["dhcp_vendor_id"] = dhcp_vendor_id
        if dns_servers is not None:
            data["dns_servers"] = dns_servers
        if flags2 is not None:
            data["flags2"] = flags2
        if gateway is not None:
            data["gateway"] = gateway
        if interest is not None:
            data["interest"] = interest
        if ip_addr is not None:
            data["ip_addr"] = ip_addr
        if ipsec_concentrator is not None:
            data["ipsec_concentrator"] = ipsec_concentrator
        if ipsec_local_id is not None:
            data["ipsec_local_id"] = ipsec_local_id
        if ipsec_passwd is not None:
            data["ipsec_passwd"] = ipsec_passwd
        if ipsec_remote_id is not None:
            data["ipsec_remote_id"] = ipsec_remote_id
        if ipv6_addr_global is not None:
            data["ipv6_addr_global"] = ipv6_addr_global
        if ipv6_addr_link is not None:
            data["ipv6_addr_link"] = ipv6_addr_link
        if ipv6_dflt_gw is not None:
            data["ipv6_dflt_gw"] = ipv6_dflt_gw
        if mac is not None:
            data["mac"] = mac
        if mtu is not None:
            data["mtu"] = mtu
        if netmask is not None:
            data["netmask"] = netmask
        if port is not None:
            data["port"] = port
        if report_timer is not None:
            data["report_timer"] = report_timer
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if sta_br_id is not None:
            data["sta_br_id"] = sta_br_id
        if tx_queue_len is not None:
            data["tx_queue_len"] = tx_queue_len
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_port",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_PORT_ALIAS> type requests

        https://www.candelatech.com/lfcli_ug.php#set_port_alias
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_port_alias(self, 
                            alias: str = None,     # New alias to assign to this virtual interface. [W]
                            port: str = None,      # Physical Port identifier that owns the virtual interface. [R]
                            resource: int = None,  # Resource number for the port to be modified. [W]
                            shelf: int = 1,        # Shelf number for the port to be modified. [R][D:1]
                            vport: str = None,     # Virtual port identifier. MAC for MAC-VLANs, VLAN-ID for 802.1Q
                            # vlans.
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_port_alias(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if alias is not None:
            data["alias"] = alias
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if vport is not None:
            data["vport"] = vport
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_port_alias",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_PPP_LINK_STATE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_ppp_link_state
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_ppp_link_state(self, 
                                link: str = None,       # Unit Number of the PPP Link, or 'all'. [W]
                                ppp_state: str = None,  # One of: RUNNING, STOPPED, or DELETED. [R]
                                resource: int = None,   # Number of the Resource, or 'all'. [W]
                                shelf: int = 1,         # Name of the Shelf, or 'all'. [R][D:1]
                                debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_ppp_link_state(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if link is not None:
            data["link"] = link
        if ppp_state is not None:
            data["ppp_state"] = ppp_state
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_ppp_link_state",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_RESOURCE> type requests

        https://www.candelatech.com/lfcli_ug.php#set_resource
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetResourceResourceFlags(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        skip_load_db_on_start = 1      # Should we skip loading the DB on start?

    def post_set_resource(self, 
                          device_profiles: str = None,      # List of profiles, see above
                          max_helper_count: str = None,     # Maximum number of helper traffic generation processes. 0
                          # means CPU-core-count (AUTO).
                          max_staged_bringup: str = None,   # Maximum amount of interfaces attempting to come up at
                          # once. Default is 50
                          max_station_bringup: str = None,  # Maximum amount of stations to bring up per radio per tick.
                          # Default is 12.
                          max_trying_ifup: str = None,      # Maximum amount of interfaces running the network config
                          # 'ifup' logic. Default is 15
                          resource: int = None,             # Number of the Resource, or <tt>all</tt>. [W]
                          resource_flags: str = None,       # System wide flags, often requires a reboot for changes to
                          # take effect.
                          resource_flags_mask: str = None,  # What flags to change. If unset, default is all.
                          shelf: int = 1,                   # Name of the Shelf, or <tt>all</tt>. [R][D:1]
                          top_left_x: str = None,           # X Location for Chamber View.
                          top_left_y: str = None,           # X Location for Chamber View.
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_resource(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if device_profiles is not None:
            data["device_profiles"] = device_profiles
        if max_helper_count is not None:
            data["max_helper_count"] = max_helper_count
        if max_staged_bringup is not None:
            data["max_staged_bringup"] = max_staged_bringup
        if max_station_bringup is not None:
            data["max_station_bringup"] = max_station_bringup
        if max_trying_ifup is not None:
            data["max_trying_ifup"] = max_trying_ifup
        if resource is not None:
            data["resource"] = resource
        if resource_flags is not None:
            data["resource_flags"] = resource_flags
        if resource_flags_mask is not None:
            data["resource_flags_mask"] = resource_flags_mask
        if shelf is not None:
            data["shelf"] = shelf
        if top_left_x is not None:
            data["top_left_x"] = top_left_x
        if top_left_y is not None:
            data["top_left_y"] = top_left_y
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_resource",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_RFGEN> type requests

        https://www.candelatech.com/lfcli_ug.php#set_rfgen
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetRfgenRfgenFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetRfgenRfgenFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        one_burst = 0x8      # Run for about 1 second and stop. Uses 5-sec sweep time for single pulse train.
        running = 0x2        # Should we start the RF Generator or not?

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetRfgenRfgenFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_rfgen(self, 
                       bb_gain: str = None,            # RX Gain, 0 - 62 in 2dB steps
                       freq_khz: str = None,           # Center frequency in Khz
                       gain: str = None,               # Main TX/RX Amp, 0 or 14 (dB), default is 14
                       p_id: str = None,               # RF Generator ID, not used at this time, enter 'NA' or 0.
                       # [D:NA]
                       if_gain: str = None,            # Fine-tune TX/RX Gain, 0 - 40 dB
                       pulse_count: str = None,        # Number of pulses (0-255)
                       pulse_interval_us: str = None,  # Time between pulses, in micro-seconds.
                       pulse_width_us: str = None,     # Requested pulse width, units are in micro-seconds.
                       resource: int = None,           # Resource number. [W]
                       rfgen_flags: str = None,        # RF Generator flags, see above.
                       rfgen_flags_mask: str = None,   # Mask of what flags to set, see above.
                       shelf: int = 1,                 # Shelf number, usually 1. [R][D:1]
                       sweep_time_ms: str = None,      # Time interval between pulse groups in miliseconds
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_rfgen(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if bb_gain is not None:
            data["bb_gain"] = bb_gain
        if freq_khz is not None:
            data["freq_khz"] = freq_khz
        if gain is not None:
            data["gain"] = gain
        if p_id is not None:
            data["id"] = p_id
        if if_gain is not None:
            data["if_gain"] = if_gain
        if pulse_count is not None:
            data["pulse_count"] = pulse_count
        if pulse_interval_us is not None:
            data["pulse_interval_us"] = pulse_interval_us
        if pulse_width_us is not None:
            data["pulse_width_us"] = pulse_width_us
        if resource is not None:
            data["resource"] = resource
        if rfgen_flags is not None:
            data["rfgen_flags"] = rfgen_flags
        if rfgen_flags_mask is not None:
            data["rfgen_flags_mask"] = rfgen_flags_mask
        if shelf is not None:
            data["shelf"] = shelf
        if sweep_time_ms is not None:
            data["sweep_time_ms"] = sweep_time_ms
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_rfgen",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_SCRIPT> type requests

        https://www.candelatech.com/lfcli_ug.php#set_script
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetScriptFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetScriptFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        SCR_COMPLETED = 0x80                # Set automatically by LANforge.
        SCR_HIDE_CONSTRAINTS = 0x2000       # Hide constraints messages.
        SCR_HIDE_CSV = 0x20                 # Don't print the CSV data in the report.
        SCR_HIDE_HUNT = 0x800               # Hide the individual hunt steps..just show results.
        SCR_HIDE_ITER_DETAILS = 0x8         # Hide iteration detail reports.
        SCR_HIDE_LAT = 0x1000               # Hide latency distribution reports.
        SCR_HIDE_LEGEND = 0x10              # Don't print the legend in the report.
        SCR_LOOP = 0x100                    # Loop script until manually stopped.
        SCR_NO_KEYED_RPT = 0x2              # Script should NOT send reports to the CLI/GUI.
        SCR_RUN_ON_MGR = 0x40               # Set automatically by LANforge.
        SCR_SHOW_ATTENUATION = 0x4000       # Show attenuation packet stats.
        SCR_SHOW_DUPS = 0x200               # Report duplicate packets.
        SCR_SHOW_GOLDEN_3P = 0x20000        # Add 'golden' third-party AP graph for comparison (where available).
        SCR_SHOW_GOLDEN_LF = 0x10000        # Add 'golden' LANforge graph for comparison (where available).
        SCR_SHOW_OOO = 0x400                # Report out-of-order packets.
        SCR_STOPPED = 0x1                   # Script should NOT have any affect on the endpoint.
        SCR_SYMMETRIC = 0x4                 # This script should apply settings to the peer endpoing as well.
        SCR_USE_MSS = 0x8000                # When setting packet size, set TCP MSS instead if endpoint supports
        # +that.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetScriptFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetScriptType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        NONE = "NONE"                  # Delete any existing script.
        Script2544 = "Script2544"      # For RFC 2544 type testing.
        ScriptAtten = "ScriptAtten"    # For Attenuators only.
        ScriptHunt = "ScriptHunt"      # Hunt for maximum speed with constraints.
        ScriptWL = "ScriptWL"          # For iterating through WanLink settings

    def post_set_script(self, 
                        endp: str = None,          # Endpoint, Test Group or Attenuator name or ID. [R]
                        flags: str = None,         # See above for description of the defined flags.
                        group_action: str = None,  # How to handle group script operations: ALL, Sequential
                        loop_count: str = None,    # How many times to loop before stopping (0 is infinite).
                        name: str = None,          # Script name. [W]
                        private: str = None,       # Private encoding for the particular script.
                        p_type: str = None,        # One of: NONE, Script2544, ScriptHunt, ScriptWL, ScriptAtten
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_script(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp is not None:
            data["endp"] = endp
        if flags is not None:
            data["flags"] = flags
        if group_action is not None:
            data["group_action"] = group_action
        if loop_count is not None:
            data["loop_count"] = loop_count
        if name is not None:
            data["name"] = name
        if private is not None:
            data["private"] = private
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_script",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_SEC_IP> type requests

        https://www.candelatech.com/lfcli_ug.php#set_sec_ip
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_sec_ip(self, 
                        ip_list: str = None,   # IP1/prefix,IP2/prefix,...IPZ/prefix. [W]
                        port: str = None,      # Name of network device (Port) to which these IPs will be added.
                        # [R]
                        resource: int = None,  # Resource number. [W]
                        shelf: int = 1,        # Shelf number. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_sec_ip(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if ip_list is not None:
            data["ip_list"] = ip_list
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_sec_ip",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_VOIP_INFO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_voip_info
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_voip_info(self, 
                           codec: str = None,                # Codec to use for the voice stream, supported values:
                           # G711U, G711A, SPEEX, g726-16, g726-24, g726-32, g726-40,
                           # g729a.
                           first_call_delay: str = None,     # How long to wait before making first call, in seconds.
                           jitter_buffer_sz: str = None,     # The size of the jitter buffer in packets. Default value
                           # is 8.
                           local_sip_port: str = None,       # Local SIP UDP port. Default is min-rtp-port + 2.
                           loop_call_count: str = None,      # How many calls to make, zero means infinite.
                           loop_wavefile_count: str = None,  # How many times to play the wave file, zero means
                           # infinite.
                           max_call_duration: str = None,    # How long should the call be, in seconds.
                           max_inter_call_gap: str = None,   # Maximum time to wait between calls, in seconds.
                           messaging_protocol: str = None,   # Messaging protocol, supported values: SIP.
                           min_call_duration: str = None,    # How long should the call be, in seconds.
                           min_inter_call_gap: str = None,   # Minimum time to wait between calls, in seconds.
                           name: str = None,                 # The name of the endpoint we are configuring. [R]
                           pesq_server_ip: str = None,       # LANforge PESQ server IP address.
                           pesq_server_passwd: str = None,   # LANforge PESQ server password. Default is to use no
                           # authentication (blank entry).
                           pesq_server_port: str = None,     # LANforge PESQ server port, default is 3998.
                           reg_expire_timer: str = None,     # SIP Registration expire timer, in seconds.
                           ringing_timer: str = None,        # How long (milliseconds) to wait in the ringing state
                           # before flagging call as no-answer.
                           sound_dev: str = None,            # Which sound device should we play sound to. (see
                           # set_endp_flags).
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_voip_info(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if codec is not None:
            data["codec"] = codec
        if first_call_delay is not None:
            data["first_call_delay"] = first_call_delay
        if jitter_buffer_sz is not None:
            data["jitter_buffer_sz"] = jitter_buffer_sz
        if local_sip_port is not None:
            data["local_sip_port"] = local_sip_port
        if loop_call_count is not None:
            data["loop_call_count"] = loop_call_count
        if loop_wavefile_count is not None:
            data["loop_wavefile_count"] = loop_wavefile_count
        if max_call_duration is not None:
            data["max_call_duration"] = max_call_duration
        if max_inter_call_gap is not None:
            data["max_inter_call_gap"] = max_inter_call_gap
        if messaging_protocol is not None:
            data["messaging_protocol"] = messaging_protocol
        if min_call_duration is not None:
            data["min_call_duration"] = min_call_duration
        if min_inter_call_gap is not None:
            data["min_inter_call_gap"] = min_inter_call_gap
        if name is not None:
            data["name"] = name
        if pesq_server_ip is not None:
            data["pesq_server_ip"] = pesq_server_ip
        if pesq_server_passwd is not None:
            data["pesq_server_passwd"] = pesq_server_passwd
        if pesq_server_port is not None:
            data["pesq_server_port"] = pesq_server_port
        if reg_expire_timer is not None:
            data["reg_expire_timer"] = reg_expire_timer
        if ringing_timer is not None:
            data["ringing_timer"] = ringing_timer
        if sound_dev is not None:
            data["sound_dev"] = sound_dev
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_voip_info",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_VRCX_COST> type requests

        https://www.candelatech.com/lfcli_ug.php#set_vrcx_cost
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_vrcx_cost(self, 
                           interface_cost: str = None,  # If using OSPF, this sets the cost for this link (1-65535).
                           local_dev: str = None,       # Name of port A for the local redirect device pair.
                           local_dev_b: str = None,     # Name of port B for the local redirect device pair.
                           remote_dev: str = None,      # Name of port B for the remote redirect device pair.
                           remote_dev_b: str = None,    # Name of port B for the remote redirect device pair.
                           resource: int = None,        # Resource number. [W]
                           shelf: int = 1,              # Shelf name/id. [R][D:1]
                           vr_name: str = None,         # Virtual Router this endpoint belongs to. Use 'FREE_LIST' to
                           # add a stand-alone endpoint. [W][D:FREE_LIST]
                           wanlink: str = None,         # The name of the WanLink that connects the two B ports.
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_vrcx_cost(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if interface_cost is not None:
            data["interface_cost"] = interface_cost
        if local_dev is not None:
            data["local_dev"] = local_dev
        if local_dev_b is not None:
            data["local_dev_b"] = local_dev_b
        if remote_dev is not None:
            data["remote_dev"] = remote_dev
        if remote_dev_b is not None:
            data["remote_dev_b"] = remote_dev_b
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if vr_name is not None:
            data["vr_name"] = vr_name
        if wanlink is not None:
            data["wanlink"] = wanlink
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_vrcx_cost",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WANLINK_INFO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wanlink_info
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_wanlink_info(self, 
                              drop_freq: str = None,              # How often, out of 1,000,000 packets, should we
                              # purposefully drop a packet.
                              dup_freq: str = None,               # How often, out of 1,000,000 packets, should we
                              # purposefully duplicate a packet.
                              extra_buffer: str = None,           # The extra amount of bytes to buffer before dropping
                              # pkts, in units of 1024. Use -1 for AUTO.
                              jitter_freq: str = None,            # How often, out of 1,000,000 packets, should we apply
                              # jitter.
                              latency: str = None,                # The base latency added to all packets, in
                              # milliseconds (or add 'us' suffix for microseconds
                              max_drop_amt: str = None,           # Maximum amount of packets to drop in a row. Default
                              # is 1.
                              max_jitter: str = None,             # The maximum jitter, in milliseconds (or ad 'us'
                              # suffix for microseconds)
                              max_lateness: str = None,           # Maximum amount of un-intentional delay before pkt is
                              # dropped. Default is AUTO
                              max_reorder_amt: str = None,        # Maximum amount of packets by which to reorder,
                              # Default is 10.
                              min_drop_amt: str = None,           # Minimum amount of packets to drop in a row. Default
                              # is 1.
                              min_reorder_amt: str = None,        # Minimum amount of packets by which to reorder,
                              # Default is 1.
                              name: str = None,                   # The name of the endpoint we are configuring. [R]
                              playback_capture_file: str = None,  # Name of the WAN capture file to play back.
                              reorder_freq: str = None,           # How often, out of 1,000,000 packets, should we make a
                              # packet out of order.
                              speed: str = None,                  # The maximum speed of traffic this endpoint will
                              # accept (bps).
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wanlink_info(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if drop_freq is not None:
            data["drop_freq"] = drop_freq
        if dup_freq is not None:
            data["dup_freq"] = dup_freq
        if extra_buffer is not None:
            data["extra_buffer"] = extra_buffer
        if jitter_freq is not None:
            data["jitter_freq"] = jitter_freq
        if latency is not None:
            data["latency"] = latency
        if max_drop_amt is not None:
            data["max_drop_amt"] = max_drop_amt
        if max_jitter is not None:
            data["max_jitter"] = max_jitter
        if max_lateness is not None:
            data["max_lateness"] = max_lateness
        if max_reorder_amt is not None:
            data["max_reorder_amt"] = max_reorder_amt
        if min_drop_amt is not None:
            data["min_drop_amt"] = min_drop_amt
        if min_reorder_amt is not None:
            data["min_reorder_amt"] = min_reorder_amt
        if name is not None:
            data["name"] = name
        if playback_capture_file is not None:
            data["playback_capture_file"] = playback_capture_file
        if reorder_freq is not None:
            data["reorder_freq"] = reorder_freq
        if speed is not None:
            data["speed"] = speed
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wanlink_info",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WANLINK_PCAP> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wanlink_pcap
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWanlinkPcapCapture(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        OFF = "OFF"    # stop capturing
        ON = "ON"      # start capturing

    def post_set_wanlink_pcap(self, 
                              capture: str = None,    # Should we capture or not? ON or OFF. [R]
                              directory: str = None,  # The directory name in which packet capture files will be
                              # written.
                              name: str = None,       # The name of the endpoint we are configuring. [R]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wanlink_pcap(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if capture is not None:
            data["capture"] = capture
        if directory is not None:
            data["directory"] = directory
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wanlink_pcap",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WANPATH_CORRUPTION> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wanpath_corruption
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWanpathCorruptionFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetWanpathCorruptionFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BIT_FLIP = 0x4              # Flip a random bit in a byte.
        BIT_TRANSPOSE = 0x8         # Transpose two side-by-side bits in a byte.
        DO_CHAIN_ON_HIT = 0x10      # Do next corruption if this corruption is applied.
        OVERWRITE_FIXED = 0x2       # Write a fixed value to a byte.
        OVERWRITE_RANDOM = 0x1      # Write a random value to a byte.
        RECALC_CSUMS = 0x20         # Attempt to re-calculate UDP and TCP checksums.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetWanpathCorruptionFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_wanpath_corruption(self, 
                                    byte: str = None,        # The byte to use for OVERWRITE_FIXED (or NA).
                                    flags: str = None,       # The flags for this corruption.
                                    index: str = None,       # The corruption to modify (0-5). [R,0-5]
                                    max_offset: str = None,  # The maximum offset from start of Ethernet packet for
                                    # the byte to be modified.
                                    min_offset: str = None,  # The minimum offset from start of Ethernet packet for
                                    # the byte to be modified.
                                    name: str = None,        # WanLink name [R]
                                    path: str = None,        # WanPath name [R]
                                    rate: str = None,        # Specifies how often, per million, this corruption
                                    # should be applied.
                                    debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wanpath_corruption(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if byte is not None:
            data["byte"] = byte
        if flags is not None:
            data["flags"] = flags
        if index is not None:
            data["index"] = index
        if max_offset is not None:
            data["max_offset"] = max_offset
        if min_offset is not None:
            data["min_offset"] = min_offset
        if name is not None:
            data["name"] = name
        if path is not None:
            data["path"] = path
        if rate is not None:
            data["rate"] = rate
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wanpath_corruption",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WANPATH_FILTER> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wanpath_filter
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_wanpath_filter(self, 
                                defer_flush: str = None,  # Enter 'YES' if you do NOT want this flushed to the
                                # remote.
                                dst_filter: str = None,   # The destination MAC or IP/Mask, 'NA' for PCAP.
                                filter_type: str = None,  # The filter type, one of: MAC, IP, PCAP.
                                passive: str = None,      # Enter 'YES' if you do NOT want to use this filter
                                # currently.
                                reverse: str = None,      # If you want the logic reversed, use 'ON', otherwise set
                                # to 'OFF'
                                src_filter: str = None,   # The source MAC or IP/Mask. For PCAP, this is the only
                                # filter.
                                wl_name: str = None,      # The name of the WanLink endpoint we are configuring. [R]
                                wp_name: str = None,      # The name of the WanPath we are configuring. [R]
                                debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wanpath_filter(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if defer_flush is not None:
            data["defer_flush"] = defer_flush
        if dst_filter is not None:
            data["dst_filter"] = dst_filter
        if filter_type is not None:
            data["filter_type"] = filter_type
        if passive is not None:
            data["passive"] = passive
        if reverse is not None:
            data["reverse"] = reverse
        if src_filter is not None:
            data["src_filter"] = src_filter
        if wl_name is not None:
            data["wl_name"] = wl_name
        if wp_name is not None:
            data["wp_name"] = wp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wanpath_filter",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WANPATH_RUNNING> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wanpath_running
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWanpathRunningRunning(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        AS_PARENT = "AS_PARENT"    # then it will be started and stopped as the parent WanLink is.
        RUNNING = "RUNNING"        # then it will be running at all times
        STOPPED = "STOPPED"        # then it will not be running at any time.

    def post_set_wanpath_running(self, 
                                 running: str = None,  # The state, one of: AS_PARENT, RUNNING, STOPPED. [R]
                                 wl_name: str = None,  # The name of the WanLink endpoint we are configuring. [R]
                                 wp_name: str = None,  # The name of the WanPath we are configuring. [R]
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wanpath_running(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if running is not None:
            data["running"] = running
        if wl_name is not None:
            data["wl_name"] = wl_name
        if wp_name is not None:
            data["wp_name"] = wp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wanpath_running",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WIFI_CORRUPTIONS> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wifi_corruptions
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWifiCorruptionsCorruptFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetWifiCorruptionsCorruptFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        MSG_TYPE_DEAUTH = 0x2                   # de-authentication message
        MSG_TYPE_EAPOL = 0x1                    # Any EAPOL message
        MSG_TYPE_EAPOL_1_OF_2 = 0x40            # EAPOL message 1/2
        MSG_TYPE_EAPOL_1_OF_4 = 0x4             # EAPOL message 1/4
        MSG_TYPE_EAPOL_2_OF_2 = 0x80            # EAPOL message 2/2
        MSG_TYPE_EAPOL_2_OF_4 = 0x8             # EAPOL message 2/4
        MSG_TYPE_EAPOL_3_OF_4 = 0x10            # EAPOL message 3/4
        MSG_TYPE_EAPOL_4_OF_4 = 0x20            # EAPOL message 4/4
        MSG_TYPE_EAPOL_ASSOC = 0x200            # EAP Association
        MSG_TYPE_EAPOL_KEY_REQ = 0x100          # EAP Key Request (not sure if this works properly)
        MST_TYPE_EAPOL_ID_REQ = 0x400           # EAP Identity request
        MST_TYPE_EAPOL_ID_RESP = 0x800          # EAP Identity response
        MST_TYPE_EAPOL_OTHER_REQ = 0x1000       # EAP Requests that do not match other things.
        MST_TYPE_EAPOL_OTHER_RESP = 0x2000      # EAP Responses that do not match other things.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetWifiCorruptionsCorruptFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_wifi_corruptions(self, 
                                  corrupt_flags: str = None,    # Specify packet types to corrupt (see flags above).
                                  corrupt_per_mil: str = None,  # Per-million: Station to randomly corrupt selected
                                  # message types by this amount.
                                  delay_flags: str = None,      # Specify packet types to delay (see flags above).
                                  delay_max: str = None,        # miliseconds: Station to randomly delay processing
                                  # received messages, max time
                                  delay_min: str = None,        # miliseconds: Station to randomly delay processing
                                  # received messages, min time
                                  dup_flags: str = None,        # Specify packet types to duplicate (see flags above).
                                  dup_per_65535: str = None,    # Percentage, represented as x per 65535 of packets we
                                  # should duplicate.
                                  ignore_flags: str = None,     # Specify packet types to ignore (see flags above).
                                  ignore_per_mil: str = None,   # Per-million: Station to randomly ignore selected
                                  # message types by this amount.
                                  port: str = None,             # WiFi interface name or number. [W]
                                  req_flush: str = None,        # Set to 1 if you wish to flush changes to kernel now.
                                  resource: int = None,         # Resource number. [W]
                                  shelf: int = 1,               # Shelf number. [R][D:1]
                                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wifi_corruptions(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if corrupt_flags is not None:
            data["corrupt_flags"] = corrupt_flags
        if corrupt_per_mil is not None:
            data["corrupt_per_mil"] = corrupt_per_mil
        if delay_flags is not None:
            data["delay_flags"] = delay_flags
        if delay_max is not None:
            data["delay_max"] = delay_max
        if delay_min is not None:
            data["delay_min"] = delay_min
        if dup_flags is not None:
            data["dup_flags"] = dup_flags
        if dup_per_65535 is not None:
            data["dup_per_65535"] = dup_per_65535
        if ignore_flags is not None:
            data["ignore_flags"] = ignore_flags
        if ignore_per_mil is not None:
            data["ignore_per_mil"] = ignore_per_mil
        if port is not None:
            data["port"] = port
        if req_flush is not None:
            data["req_flush"] = req_flush
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wifi_corruptions",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WIFI_CUSTOM> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wifi_custom
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_wifi_custom(self, 
                             port: str = None,      # WiFi interface name or number. [W]
                             resource: int = None,  # Resource number. [W]
                             shelf: int = 1,        # Shelf number. [R][D:1]
                             text: str = None,      # [BLANK] will erase all, any other text will be appended to
                             # existing text.
                             p_type: str = None,    # NA for now, may specify specific locations later. [D:NA]
                             debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wifi_custom(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if text is not None:
            data["text"] = text
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wifi_custom",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WIFI_EXTRA> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wifi_extra
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_wifi_extra(self, 
                            anonymous_identity: str = None,  # Anonymous identity string for EAP.
                            anqp_3gpp_cell_net: str = None,  # 802.11u 3GCPP Cellular Network Info, VAP only.
                            ca_cert: str = None,             # CA-CERT file name.
                            client_cert: str = None,         # 802.11u Client cert file: /etc/wpa_supplicant/ca.pem
                            domain: str = None,              # 802.11u domain: mytelco.com
                            eap: str = None,                 # EAP method: MD5, MSCHAPV2, OTP, GTC, TLS, PEAP, TTLS.
                            group: str = None,               # Group cyphers: CCMP, TKIP, WEP104, WEP40, or combination.
                            hessid: str = None,              # 802.11u HESSID (MAC address format) (or peer for WDS
                            # stations).
                            identity: str = None,            # EAP Identity string.
                            imsi: str = None,                # 802.11u IMSI: 310026-000000000
                            ipaddr_type_avail: str = None,   # 802.11u network type available, integer, VAP only.
                            key: str = None,                 # WEP key0. This should be entered in ascii-hex. Use this
                            # only for WEP.
                            key_mgmt: str = None,            # Key management: WPA-PSK, WPA-EAP, IEEE8021X, NONE,
                            # WPA-PSK-SHA256, WPA-EAP-SHA256 or combo.
                            milenage: str = None,            # 802.11u milenage:
                            # 90dca4eda45b53cf0f12d7c9c3bc6a89:cb9cccc4b9258e6dca4760379fb82
                            network_auth_type: str = None,   # 802.11u network authentication type, VAP only.
                            network_type: str = None,        # 802.11u network type, integer, VAP only.
                            pac_file: str = None,            # EAP-FAST PAC-File name. (For AP, this field is the RADIUS
                            # secret password)
                            pairwise: str = None,            # Pairwise ciphers: CCMP, TKIP, NONE, or combination.
                            password: str = None,            # EAP Password string.
                            phase1: str = None,              # Outer-authentication, ie TLS tunnel parameters.
                            phase2: str = None,              # Inner authentication with TLS tunnel.
                            pin: str = None,                 # EAP-SIM pin string. (For AP, this field is HS20 Operating
                            # Class)
                            pk_passwd: str = None,           # EAP private key password. (For AP, this field is HS20
                            # connection capability)
                            port: str = None,                # WiFi interface name or number. [W]
                            private_key: str = None,         # EAP private key certificate file name. (For AP, this
                            # field is HS20 WAN Metrics)
                            psk: str = None,                 # WPA(2) pre-shared key. If unsure, use this field for any
                            # password entry. Prepend with 0x for ascii-hex
                            # representation.
                            realm: str = None,               # 802.11u realm: mytelco.com
                            resource: int = None,            # Resource number. [W]
                            roaming_consortium: str = None,  # 802.11u roaming consortium: 223344 (15 characters max)
                            shelf: int = 1,                  # Shelf number. [R][D:1]
                            venue_group: str = None,         # 802.11u Venue Group, integer. VAP only.
                            venue_type: str = None,          # 802.11u Venue Type, integer. VAP only.
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wifi_extra(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if anonymous_identity is not None:
            data["anonymous_identity"] = anonymous_identity
        if anqp_3gpp_cell_net is not None:
            data["anqp_3gpp_cell_net"] = anqp_3gpp_cell_net
        if ca_cert is not None:
            data["ca_cert"] = ca_cert
        if client_cert is not None:
            data["client_cert"] = client_cert
        if domain is not None:
            data["domain"] = domain
        if eap is not None:
            data["eap"] = eap
        if group is not None:
            data["group"] = group
        if hessid is not None:
            data["hessid"] = hessid
        if identity is not None:
            data["identity"] = identity
        if imsi is not None:
            data["imsi"] = imsi
        if ipaddr_type_avail is not None:
            data["ipaddr_type_avail"] = ipaddr_type_avail
        if key is not None:
            data["key"] = key
        if key_mgmt is not None:
            data["key_mgmt"] = key_mgmt
        if milenage is not None:
            data["milenage"] = milenage
        if network_auth_type is not None:
            data["network_auth_type"] = network_auth_type
        if network_type is not None:
            data["network_type"] = network_type
        if pac_file is not None:
            data["pac_file"] = pac_file
        if pairwise is not None:
            data["pairwise"] = pairwise
        if password is not None:
            data["password"] = password
        if phase1 is not None:
            data["phase1"] = phase1
        if phase2 is not None:
            data["phase2"] = phase2
        if pin is not None:
            data["pin"] = pin
        if pk_passwd is not None:
            data["pk_passwd"] = pk_passwd
        if port is not None:
            data["port"] = port
        if private_key is not None:
            data["private_key"] = private_key
        if psk is not None:
            data["psk"] = psk
        if realm is not None:
            data["realm"] = realm
        if resource is not None:
            data["resource"] = resource
        if roaming_consortium is not None:
            data["roaming_consortium"] = roaming_consortium
        if shelf is not None:
            data["shelf"] = shelf
        if venue_group is not None:
            data["venue_group"] = venue_group
        if venue_type is not None:
            data["venue_type"] = venue_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wifi_extra",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WIFI_EXTRA2> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wifi_extra2
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_wifi_extra2(self, 
                             corrupt_gtk_rekey_mic: str = None,  # Per-million: AP corrupts GTK Rekey MIC.
                             freq_24: str = None,                # Frequency list for 2.4Ghz band, see above.
                             freq_5: str = None,                 # Frequency list for 5Ghz band, see above.
                             ignore_assoc: str = None,           # Per-million: AP ignore assoc request percentage.
                             ignore_auth: str = None,            # Per-million: AP ignore auth request percentage.
                             ignore_probe: str = None,           # Per-million: AP ignore probe percentage.
                             ignore_reassoc: str = None,         # Per-million: AP ignore re-assoc request percentage.
                             ocsp: str = None,                   # OCSP settings: 0=disabled, 1=try, but to not require
                             # response, 2=require valid OCSP stapling response.
                             port: str = None,                   # WiFi interface name or number. [W]
                             post_ifup_script: str = None,       # Script name with optional args, will run after
                             # interface comes up and gets IP.
                             radius_ip: str = None,              # RADIUS server IP Address (AP Only)
                             radius_port: str = None,            # RADIUS server IP Port (AP Only)
                             req_flush: str = None,              # Set to 1 if you wish to flush changes to kernel now.
                             resource: int = None,               # Resource number. [W]
                             sae_pwe: str = None,                # Set SAE-PWE, 0 == hunting-and-pecking, 1 ==
                             # hash-to-element, 2 allow both.
                             shelf: int = 1,                     # Shelf number. [R][D:1]
                             venue_id: str = None,               # Venue-ID for this wifi device. VAP in same venue will
                             # share neigh reports as appropriate.
                             debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wifi_extra2(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if corrupt_gtk_rekey_mic is not None:
            data["corrupt_gtk_rekey_mic"] = corrupt_gtk_rekey_mic
        if freq_24 is not None:
            data["freq_24"] = freq_24
        if freq_5 is not None:
            data["freq_5"] = freq_5
        if ignore_assoc is not None:
            data["ignore_assoc"] = ignore_assoc
        if ignore_auth is not None:
            data["ignore_auth"] = ignore_auth
        if ignore_probe is not None:
            data["ignore_probe"] = ignore_probe
        if ignore_reassoc is not None:
            data["ignore_reassoc"] = ignore_reassoc
        if ocsp is not None:
            data["ocsp"] = ocsp
        if port is not None:
            data["port"] = port
        if post_ifup_script is not None:
            data["post_ifup_script"] = post_ifup_script
        if radius_ip is not None:
            data["radius_ip"] = radius_ip
        if radius_port is not None:
            data["radius_port"] = radius_port
        if req_flush is not None:
            data["req_flush"] = req_flush
        if resource is not None:
            data["resource"] = resource
        if sae_pwe is not None:
            data["sae_pwe"] = sae_pwe
        if shelf is not None:
            data["shelf"] = shelf
        if venue_id is not None:
            data["venue_id"] = venue_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wifi_extra2",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WIFI_RADIO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wifi_radio
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWifiRadioFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetWifiRadioFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        ct_sta_mode = 0x40000         # Enable CT-STA mode if radio supports it. Efficiently replaces sw-crypt in
        # +some firmware.
        firmware_cfg = 0x80000        # Apply firmware config.
        hw_sim = 0x1                  # Create hw-sim virtual radio if radio does not already exist.
        ignore_radar = 0x100000       # Ignore RADAR events reported by firmware.
        no_scan_share = 0x40          # Disable sharing scan results.
        no_sw_crypt = 0x20000         # Disable software-crypt for this radio. Disables some virtual-station
        # +features.
        use_syslog = 0x20000000       # Put supplicant logs in syslog instead of a file.
        verbose = 0x10000             # Verbose-Debug: Increase debug info in wpa-supplicant and hostapd logs.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetWifiRadioFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    class SetWifiRadioMode(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        p_802_11a = 1      # 802.11a
        AUTO = 0           # 802.11g
        aAX = 15           # 802.11a-AX (6E disables /n and /ac)
        abg = 4            # 802.11abg
        abgn = 5           # 802.11abgn
        abgnAC = 8         # 802.11abgn-AC
        abgnAX = 12        # 802.11abgn-AX
        an = 10            # 802.11an
        anAC = 9           # 802.11an-AC
        anAX = 14          # 802.11an-AX
        b = 2              # 802.11b
        bg = 7             # 802.11bg
        bgn = 6            # 802.11bgn
        bgnAC = 11         # 802.11bgn-AC
        bgnAX = 13         # 802.11bgn-AX
        g = 3              # 802.11g

    def post_set_wifi_radio(self, 
                            active_peer_count: str = None,   # Number of locally-cached peer objects for this radio.
                            ampdu_factor: str = None,        # ax200/ax210 only, currently. Requires module reload. OS
                            # Default: 0xFF
                            antenna: str = None,             # Antenna configuration: 0 Diversity/All, 1 Fixed-A (1x1),
                            # 4 AB (2x2), 7 ABC (3x3), 8 ABCD (4x4), 9 8x8
                            channel: str = None,             # Channel number for this radio device. Frequency takes
                            # precedence if both are set to non-default values.
                            const_tx: str = None,            # RF Pattern Generator , encoded as a single 32-bit
                            # integer. See above.
                            country: str = None,             # Country number for this radio device.
                            flags: str = None,               # Flags for this interface (see above.)
                            flags_mask: str = None,          # If set, only these flags will be considered.
                            frag_thresh: str = None,         # Fragmentation Threshold (256 - 2346, 2346 == disabled).
                            frequency: str = None,           # Frequency for this radio. <tt>0xFFFF, AUTO or
                            # DEFAULT</tt> means ANY.
                            fwname: str = None,              # Firmware name (for example: firmware-5.bin)
                            fwver: str = None,               # Firmware API version (for example, 5 if firmware is based
                            # on firmware-5.bin
                            mac: str = None,                 # Used to identify when name cannot be trusted (2.6.34+
                            # kernels).
                            max_amsdu: str = None,           # Maximum number of frames per AMSDU that may be
                            # transmitted. See above.
                            mode: str = None,                # WiFi mode, see table
                            peer_count: str = None,          # Number of peer objects for this radio.
                            pref_ap: str = None,             # Preferred AP BSSID for all station vdevs on this radio.
                            pulse2_interval_us: str = None,  # Pause between pattern burst for RF noise generator.
                            pulse_interval: str = None,      # RF Pattern generator: interval between pulses in usecs.
                            pulse_width: str = None,         # RF Pattern generator: pulse width in usecs.
                            radio: str = None,               # Name of the physical radio interface, for example: wiphy0
                            # [W]
                            rate: str = None,                # No longer used, specify the rate on the virtual
                            # station(s) instead.
                            rate_ctrl_count: str = None,     # Number of rate-ctrl objects for this radio.
                            resource: int = None,            # Resource number. [W]
                            rts: str = None,                 # The RTS Threshold for this radio (off, or 1-2347).
                            shelf: int = 1,                  # Shelf number. [R][D:1]
                            skid_limit: str = None,          # Firmware hash-table Skid Limit for this radio.
                            stations_count: str = None,      # Number of stations supported by this radio.
                            tids_count: str = None,          # TIDs count for this radio.
                            tx_pulses: str = None,           # Number of pattern pulses per burst for RF noise
                            # generator.
                            txdesc_count: str = None,        # Transmit descriptor count for this radio.
                            txpower: str = None,             # The transmit power setting for this radio. (AUTO for
                            # system defaults)
                            vdev_count: str = None,          # Configure radio vdev count.
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wifi_radio(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if active_peer_count is not None:
            data["active_peer_count"] = active_peer_count
        if ampdu_factor is not None:
            data["ampdu_factor"] = ampdu_factor
        if antenna is not None:
            data["antenna"] = antenna
        if channel is not None:
            data["channel"] = channel
        if const_tx is not None:
            data["const_tx"] = const_tx
        if country is not None:
            data["country"] = country
        if flags is not None:
            data["flags"] = flags
        if flags_mask is not None:
            data["flags_mask"] = flags_mask
        if frag_thresh is not None:
            data["frag_thresh"] = frag_thresh
        if frequency is not None:
            data["frequency"] = frequency
        if fwname is not None:
            data["fwname"] = fwname
        if fwver is not None:
            data["fwver"] = fwver
        if mac is not None:
            data["mac"] = mac
        if max_amsdu is not None:
            data["max_amsdu"] = max_amsdu
        if mode is not None:
            data["mode"] = mode
        if peer_count is not None:
            data["peer_count"] = peer_count
        if pref_ap is not None:
            data["pref_ap"] = pref_ap
        if pulse2_interval_us is not None:
            data["pulse2_interval_us"] = pulse2_interval_us
        if pulse_interval is not None:
            data["pulse_interval"] = pulse_interval
        if pulse_width is not None:
            data["pulse_width"] = pulse_width
        if radio is not None:
            data["radio"] = radio
        if rate is not None:
            data["rate"] = rate
        if rate_ctrl_count is not None:
            data["rate_ctrl_count"] = rate_ctrl_count
        if resource is not None:
            data["resource"] = resource
        if rts is not None:
            data["rts"] = rts
        if shelf is not None:
            data["shelf"] = shelf
        if skid_limit is not None:
            data["skid_limit"] = skid_limit
        if stations_count is not None:
            data["stations_count"] = stations_count
        if tids_count is not None:
            data["tids_count"] = tids_count
        if tx_pulses is not None:
            data["tx_pulses"] = tx_pulses
        if txdesc_count is not None:
            data["txdesc_count"] = txdesc_count
        if txpower is not None:
            data["txpower"] = txpower
        if vdev_count is not None:
            data["vdev_count"] = vdev_count
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wifi_radio",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WIFI_TXO> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wifi_txo
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_set_wifi_txo(self, 
                          port: str = None,         # WiFi interface name or number. [W]
                          resource: int = None,     # Resource number. [W]
                          shelf: int = 1,           # Shelf number. [R][D:1]
                          txo_bw: str = None,       # Configure bandwidth: 0 == 20, 1 == 40, 2 == 80, 3 == 160, 4 ==
                          # 80+80.
                          txo_enable: str = None,   # Set to 1 if you wish to enable transmit override, 0 to
                          # disable.
                          txo_mcs: str = None,      # Configure the MCS (0-3 for CCK, 0-7 for OFDM, 0-7 for HT, 0-9
                          # for VHT, 0-11 for HE
                          txo_nss: str = None,      # Configure number of spatial streams (0 == nss1, 1 == nss2,
                          # ...).
                          txo_pream: str = None,    # Select rate preamble: 0 == OFDM, 1 == CCK, 2 == HT, 3 == VHT,
                          # 4 == HE_SU.
                          txo_retries: str = None,  # Configure number of retries. 0 or 1 means no retries).
                          txo_sgi: str = None,      # Should rates be sent with short-guard-interval or not?
                          txo_txpower: str = None,  # Configure TX power in db. Use 255 for system defaults. See
                          # notes above.
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wifi_txo(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if txo_bw is not None:
            data["txo_bw"] = txo_bw
        if txo_enable is not None:
            data["txo_enable"] = txo_enable
        if txo_mcs is not None:
            data["txo_mcs"] = txo_mcs
        if txo_nss is not None:
            data["txo_nss"] = txo_nss
        if txo_pream is not None:
            data["txo_pream"] = txo_pream
        if txo_retries is not None:
            data["txo_retries"] = txo_retries
        if txo_sgi is not None:
            data["txo_sgi"] = txo_sgi
        if txo_txpower is not None:
            data["txo_txpower"] = txo_txpower
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wifi_txo",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WL_CORRUPTION> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wl_corruption
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWlCorruptionFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SetWlCorruptionFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        BIT_FLIP = 0x4              # Flip a random bit in a byte.
        BIT_TRANSPOSE = 0x8         # Transpose two side-by-side bits in a byte.
        DO_CHAIN_ON_HIT = 0x10      # Do next corruption if this corruption is applied.
        OVERWRITE_FIXED = 0x2       # Write a fixed value to a byte.
        OVERWRITE_RANDOM = 0x1      # Write a random value to a byte.
        RECALC_CSUMS = 0x20         # Attempt to re-calculate UDP and TCP checksums.

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SetWlCorruptionFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_set_wl_corruption(self, 
                               byte: str = None,        # The byte to use for OVERWRITE_FIXED (or NA).
                               flags: str = None,       # The flags for this corruption.
                               index: str = None,       # The corruption to modify (0-5). [R,0-5]
                               max_offset: str = None,  # The maximum offset from start of Ethernet packet for the
                               # byte to be modified.
                               min_offset: str = None,  # The minimum offset from start of Ethernet packet for the
                               # byte to be modified.
                               name: str = None,        # WanLink name [R]
                               rate: str = None,        # Specifies how often, per million, this corruption should
                               # be applied.
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wl_corruption(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if byte is not None:
            data["byte"] = byte
        if flags is not None:
            data["flags"] = flags
        if index is not None:
            data["index"] = index
        if max_offset is not None:
            data["max_offset"] = max_offset
        if min_offset is not None:
            data["min_offset"] = min_offset
        if name is not None:
            data["name"] = name
        if rate is not None:
            data["rate"] = rate
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wl_corruption",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SET_WL_QDISC> type requests

        https://www.candelatech.com/lfcli_ug.php#set_wl_qdisc
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SetWlQdiscQdisc(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        FIFO = "FIFO"                                      # is the default queuing discipline, no arguments
        WRR__queue_queue_____ = "WRR,[queue,queue,...]"    # Weighted Round Robbin is also available

    def post_set_wl_qdisc(self, 
                          name: str = None,   # WanLink name [R]
                          qdisc: str = None,  # FIFO, WRR,a,b,c,d,e,f,g etc [R]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_set_wl_qdisc(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if qdisc is not None:
            data["qdisc"] = qdisc
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/set_wl_qdisc",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_ALERTS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_alerts
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class ShowAlertsType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        All = "All"                            #
        CX = "CX"                              #
        Card = "Card"                          #
        Channel_Group = "Channel_Group"        #
        CollisionDomain = "CollisionDomain"    #
        Endp = "Endp"                          #
        PESQ = "PESQ"                          #
        PPP_Link = "PPP_Link"                  #
        Port = "Port"                          #
        Shelf = "Shelf"                        #
        Span = "Span"                          #
        Test_Mgr = "Test_Mgr"                  #

    def post_show_alerts(self, 
                         card: int = None,   # Alert resource filter.
                         endp: str = None,   # Alert endpoint filter.
                         extra: str = None,  # Extra filter, currently ignored.
                         port: str = None,   # Alert port filter (can be port name or number).
                         shelf: int = 1,     # Alert shelf filter.
                         p_type: str = None,  # Alert type filter. [R]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_alerts(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if card is not None:
            data["card"] = card
        if endp is not None:
            data["endp"] = endp
        if extra is not None:
            data["extra"] = extra
        if port is not None:
            data["port"] = port
        if shelf is not None:
            data["shelf"] = shelf
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_alerts",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_ATTENUATORS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_attenuators
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_attenuators(self, 
                              resource: int = None,  # Resource number, or 'all'. [W]
                              serno: str = None,     # Serial number for requested Attenuator, or 'all'. [W]
                              shelf: int = 1,        # Shelf number or alias, can be 'all'. [R][D:1]
                              debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_attenuators(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if serno is not None:
            data["serno"] = serno
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_attenuators",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_CD> type requests

        https://www.candelatech.com/lfcli_ug.php#show_cd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_cd(self, 
                     collision_domain: str = None,  # Name of the Collision Domain, or 'all'. [W]
                     resource: int = None,          # Resource number, or 'all'. [W]
                     shelf: int = 1,                # Name/id of the shelf, or 'all'. [R][D:1]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_cd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if collision_domain is not None:
            data["collision_domain"] = collision_domain
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_cd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_CHAMBER> type requests

        https://www.candelatech.com/lfcli_ug.php#show_chamber
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_chamber(self, 
                          name: str = None,  # Chamber Name or 'ALL'. [W][D:ALL]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_chamber(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_chamber",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_CHANNEL_GROUPS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_channel_groups
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_channel_groups(self, 
                                 channel_name: str = None,  # Name of the channel, or 'all'. [W]
                                 resource: int = None,      # Resource number, or 'all'. [W]
                                 shelf: int = 1,            # Name/id of the shelf, or 'all'. [R][D:1]
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_channel_groups(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if channel_name is not None:
            data["channel_name"] = channel_name
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_channel_groups",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_CLIENTS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_clients
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_clients(self, 
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_clients(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/show_clients",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_CX> type requests

        https://www.candelatech.com/lfcli_ug.php#show_cx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_cx(self, 
                     cross_connect: str = None,  # Specify cross-connect to act on, or 'all'. [W]
                     test_mgr: str = None,       # Specify test-mgr to act on, or 'all'. [R]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_cx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cross_connect is not None:
            data["cross_connect"] = cross_connect
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_cx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_CXE> type requests

        https://www.candelatech.com/lfcli_ug.php#show_cxe
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_cxe(self, 
                      cross_connect: str = None,  # Specify cross-connect to show, or 'all'. [W]
                      test_mgr: str = None,       # Specify test-mgr to use, or 'all'. [R]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_cxe(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cross_connect is not None:
            data["cross_connect"] = cross_connect
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_cxe",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_DBS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_dbs
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_dbs(self, 
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_dbs(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/show_dbs",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_DUT> type requests

        https://www.candelatech.com/lfcli_ug.php#show_dut
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_dut(self, 
                      name: str = None,  # DUT Name or 'ALL'. [W][D:ALL]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_dut(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_dut",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_ENDP_PAYLOAD> type requests

        https://www.candelatech.com/lfcli_ug.php#show_endp_payload
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_endp_payload(self, 
                               max_bytes: str = None,  # The max number of payload bytes to print out, default is
                               # 128. [R][D:128]
                               name: str = None,       # The name of the endpoint we are configuring. [R]
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_endp_payload(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if max_bytes is not None:
            data["max_bytes"] = max_bytes
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_endp_payload",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_ENDPOINTS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_endpoints
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_endpoints(self, 
                            endpoint: str = None,  # Name of endpoint, or 'all'. [R]
                            extra: str = None,     # See above.
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_endpoints(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endpoint is not None:
            data["endpoint"] = endpoint
        if extra is not None:
            data["extra"] = extra
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_endpoints",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_ERR> type requests

        https://www.candelatech.com/lfcli_ug.php#show_err
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_err(self, 
                      message: str = None,  # Message to show to others currently logged on. <tt
                      # escapearg='false'>Unescaped Value</tt> [R]
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_err(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if message is not None:
            data["message"] = message
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_err",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_EVENT_INTEREST> type requests

        https://www.candelatech.com/lfcli_ug.php#show_event_interest
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_event_interest(self, 
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_event_interest(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/show_event_interest",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_EVENTS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_events
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class ShowEventsType(Enum):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        All = "All"                            #
        CX = "CX"                              #
        Card = "Card"                          #
        Channel_Group = "Channel_Group"        #
        CollisionDomain = "CollisionDomain"    #
        Endp = "Endp"                          #
        PESQ = "PESQ"                          #
        PPP_Link = "PPP_Link"                  #
        Port = "Port"                          #
        Shelf = "Shelf"                        #
        Span = "Span"                          #
        Test_Mgr = "Test_Mgr"                  #

    def post_show_events(self, 
                         card: int = None,   # Event resource filter.
                         endp: str = None,   # Event endpoint filter.
                         extra: str = None,  # Extra filter, currently ignored.
                         port: str = None,   # Event port filter (can be port name or number).
                         shelf: int = 1,     # Event shelf filter.
                         p_type: str = None,  # Event type filter. [R]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_events(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if card is not None:
            data["card"] = card
        if endp is not None:
            data["endp"] = endp
        if extra is not None:
            data["extra"] = extra
        if port is not None:
            data["port"] = port
        if shelf is not None:
            data["shelf"] = shelf
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_events",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_FILES> type requests

        https://www.candelatech.com/lfcli_ug.php#show_files
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_files(self, 
                        dir_flags: str = None,  # Determines format of listing, see above.
                        directory: str = None,  # The sub-directory in which to list.
                        p_filter: str = None,   # An optional filter, as used by the 'ls' command.
                        key: str = None,        # A special key, can be used for scripting.
                        resource: int = None,   # The machine to search in. [W]
                        shelf: int = 1,         # The virtual shelf to search in. Use 0 for manager machine.
                        # [R,0-1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_files(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if dir_flags is not None:
            data["dir_flags"] = dir_flags
        if directory is not None:
            data["directory"] = directory
        if p_filter is not None:
            data["filter"] = p_filter
        if key is not None:
            data["key"] = key
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_files",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#show_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_group(self, 
                        group: str = None,  # Can be name of test group. Use 'all' or leave blank for all groups.
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if group is not None:
            data["group"] = group
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_PESQ> type requests

        https://www.candelatech.com/lfcli_ug.php#show_pesq
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_pesq(self, 
                       endpoint: str = None,  # Name of endpoint, or 'all'. [R]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_pesq(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endpoint is not None:
            data["endpoint"] = endpoint
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_pesq",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_PORTS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_ports
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_ports(self, 
                        port: str = None,         # Port number, or 'all'. [W]
                        probe_flags: str = None,  # See above, add them together for multiple probings. Leave blank
                        # if you want stats only.
                        resource: int = None,     # Resource number, or 'all'. [W]
                        shelf: int = 1,           # Name/id of the shelf, or 'all'. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_ports(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if probe_flags is not None:
            data["probe_flags"] = probe_flags
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_ports",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_PPP_LINKS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_ppp_links
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_ppp_links(self, 
                            link_num: str = None,  # Ppp-Link number of the span, or 'all'. [W]
                            resource: int = None,  # Resource number, or 'all'. [W]
                            shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_ppp_links(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if link_num is not None:
            data["link_num"] = link_num
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_ppp_links",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_PROFILE> type requests

        https://www.candelatech.com/lfcli_ug.php#show_profile
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_profile(self, 
                          name: str = None,  # Profile Name or 'ALL'. [R]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_profile(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_profile",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_RESOURCES> type requests

        https://www.candelatech.com/lfcli_ug.php#show_resources
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_resources(self, 
                            resource: int = None,  # Resource number, or 'all'. [W]
                            shelf: int = 1,        # Shelf number or alias, can be 'all'. [R][D:1]
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_resources(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_resources",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_RFGEN> type requests

        https://www.candelatech.com/lfcli_ug.php#show_rfgen
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_rfgen(self, 
                        resource: int = None,  # Resource number, or 'all'. [W]
                        shelf: int = 1,        # Shelf number or alias, can be 'all'. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_rfgen(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_rfgen",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_RT> type requests

        https://www.candelatech.com/lfcli_ug.php#show_rt
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_rt(self, 
                     key: str = None,             # Unique identifier for this request. Usually left blank.
                     resource: int = None,        # Resource number. [W]
                     shelf: int = 1,              # Shelf number. [R][D:1]
                     virtual_router: str = None,  # Name of the virtual router. [W]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_rt(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if key is not None:
            data["key"] = key
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if virtual_router is not None:
            data["virtual_router"] = virtual_router
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_rt",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_SCRIPT_RESULTS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_script_results
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_script_results(self, 
                                 endpoint: str = None,  # Name of endpoint, test-group, or 'all'. [R]
                                 key: str = None,       # Optional 'key' to be used in keyed-text message result.
                                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_script_results(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endpoint is not None:
            data["endpoint"] = endpoint
        if key is not None:
            data["key"] = key
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_script_results",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_SPANS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_spans
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_spans(self, 
                        resource: int = None,     # Resource number, or 'all'. [W]
                        shelf: int = 1,           # Name/id of the shelf, or 'all'. [R][D:1]
                        span_number: str = None,  # Span-Number of the span, or 'all'. [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_spans(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if span_number is not None:
            data["span_number"] = span_number
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_spans",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_TEXT_BLOB> type requests

        https://www.candelatech.com/lfcli_ug.php#show_text_blob
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_text_blob(self, 
                            brief: str = None,  # Set to 'brief' for a brief listing of all text blobs.
                            name: str = None,   # Text Blob Name or 'ALL'. [R]
                            p_type: str = None,  # Text Blob type or 'ALL'. [R]
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_text_blob(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if brief is not None:
            data["brief"] = brief
        if name is not None:
            data["name"] = name
        if p_type is not None:
            data["type"] = p_type
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_text_blob",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_TM> type requests

        https://www.candelatech.com/lfcli_ug.php#show_tm
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_tm(self, 
                     test_mgr: str = None,  # Can be name of test manager, or 'all'. [R]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_tm(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_tm",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_TRAFFIC_PROFILE> type requests

        https://www.candelatech.com/lfcli_ug.php#show_traffic_profile
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_traffic_profile(self, 
                                  name: str = None,  # Profile Name or 'ALL'. [R]
                                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_traffic_profile(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_traffic_profile",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_VENUE> type requests

        https://www.candelatech.com/lfcli_ug.php#show_venue
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_venue(self, 
                        resource: int = None,  # Resource number, or 'ALL' [W]
                        shelf: int = 1,        # Shelf number. [R][D:1]
                        venu_id: str = None,   # Number to uniquely identify this venue on this resource, or 'ALL'
                        # [W]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_venue(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if venu_id is not None:
            data["venu_id"] = venu_id
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_venue",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_VR> type requests

        https://www.candelatech.com/lfcli_ug.php#show_vr
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_vr(self, 
                     resource: int = None,  # Resource number, or 'all'. [W]
                     router: str = None,    # Name of the Virtual Router, or 'all'. [W]
                     shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_vr(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if router is not None:
            data["router"] = router
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_vr",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_VRCX> type requests

        https://www.candelatech.com/lfcli_ug.php#show_vrcx
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_vrcx(self, 
                       cx_name: str = None,   # Name of the Virtual Router Connection, or 'all'. [W]
                       resource: int = None,  # Resource number, or 'all'. [W]
                       shelf: int = 1,        # Name/id of the shelf, or 'all'. [R][D:1]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_vrcx(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cx_name is not None:
            data["cx_name"] = cx_name
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_vrcx",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHOW_WANPATHS> type requests

        https://www.candelatech.com/lfcli_ug.php#show_wanpaths
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_show_wanpaths(self, 
                           endpoint: str = None,  # Name of endpoint, or 'all'. [W]
                           wanpath: str = None,   # Name of wanpath, or 'all'. [W]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_show_wanpaths(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endpoint is not None:
            data["endpoint"] = endpoint
        if wanpath is not None:
            data["wanpath"] = wanpath
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/show_wanpaths",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHUTDOWN> type requests

        https://www.candelatech.com/lfcli_ug.php#shutdown
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_shutdown(self, 
                      chdir: str = None,      # Directory to cd to before dying. Only useful when using gprof to
                      # debug, or 'NA' to ignore.
                      really: str = None,     # Must be 'YES' for command to really work.
                      serverctl: str = None,  # Enter 'YES' to do a ./serverctl.bash restart to restart all
                      # LANforge processes.
                      debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_shutdown(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if chdir is not None:
            data["chdir"] = chdir
        if really is not None:
            data["really"] = really
        if serverctl is not None:
            data["serverctl"] = serverctl
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/shutdown",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHUTDOWN_OS> type requests

        https://www.candelatech.com/lfcli_ug.php#shutdown_os
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_shutdown_os(self, 
                         resource: int = None,  # Resource number, or ALL. [W]
                         shelf: int = 1,        # Shelf number, or ALL. [R][D:1]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_shutdown_os(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/shutdown_os",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SHUTDOWN_RESOURCE> type requests

        https://www.candelatech.com/lfcli_ug.php#shutdown_resource
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_shutdown_resource(self, 
                               resource: int = None,  # Resource number, or ALL. [W]
                               shelf: int = 1,        # Shelf number, or ALL. [R][D:1]
                               debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_shutdown_resource(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/shutdown_resource",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/SNIFF_PORT> type requests

        https://www.candelatech.com/lfcli_ug.php#sniff_port
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    class SniffPortFlags(IntFlag):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            This class is stateless. It can do binary flag math, returning the integer value.
            Example Usage: 
                int:flag_val = 0
                flag_val = LFPost.set_flags(SniffPortFlags0, flag_names=['bridge', 'dhcp'])
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

        DUMPCAP = 0x2            # Use command-line dumpcap, more efficient than tshark
        MATE_TERMINAL = 0x4      # Launch tshark/dumpcap in mate-terminal
        MATE_XTERM = 0x8         # Launch tshark/dumpcap in xterm
        TSHARK = 0x1             # Use command-line tshark instead of wireshark

        # use to get in value of flag
        @classmethod
        def valueof(cls, name=None):
            if name is None:
                return name
            if name not in cls.__members__:
                raise ValueError("SniffPortFlags has no member:[%s]" % name)
            return (cls[member].value for member in cls.__members__ if member == name)

    def post_sniff_port(self, 
                        display: str = None,   # The DISPLAY option, for example: 192.168.1.5:0.0. Will guess if
                        # left blank.
                        duration: str = None,  # Duration for doing a capture (in seconds). Default is 5 minutes
                        # for dumpcap/tshark, and forever for wireshark
                        flags: str = None,     # Flags that control how the sniffing is done.
                        outfile: str = None,   # Optional file location for saving a capture.
                        port: str = None,      # The port we are trying to run the packet sniffer on. [R]
                        resource: int = None,  # Resource number. [W]
                        shelf: int = 1,        # Shelf number. [R][D:1]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_sniff_port(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if display is not None:
            data["display"] = display
        if duration is not None:
            data["duration"] = duration
        if flags is not None:
            data["flags"] = flags
        if outfile is not None:
            data["outfile"] = outfile
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/sniff_port",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/START_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#start_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_start_endp(self, 
                        endp_name: str = None,  # Name of the cross-connect, or 'all'. [R]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_start_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/start_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/START_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#start_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_start_group(self, 
                         name: str = None,  # The name of the test group. [R]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_start_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/start_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/START_PPP_LINK> type requests

        https://www.candelatech.com/lfcli_ug.php#start_ppp_link
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_start_ppp_link(self, 
                            resource: int = None,  # Resource number that holds this PppLink. [W]
                            shelf: int = 1,        # Name/id of the shelf. [R][D:1]
                            unit_num: str = None,  # Unit-Number for the PppLink to be started. [R]
                            debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_start_ppp_link(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if unit_num is not None:
            data["unit_num"] = unit_num
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/start_ppp_link",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/STOP_ENDP> type requests

        https://www.candelatech.com/lfcli_ug.php#stop_endp
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_stop_endp(self, 
                       endp_name: str = None,  # Name of the endpoint, or 'all'. [R]
                       debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_stop_endp(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if endp_name is not None:
            data["endp_name"] = endp_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/stop_endp",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/STOP_GROUP> type requests

        https://www.candelatech.com/lfcli_ug.php#stop_group
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_stop_group(self, 
                        name: str = None,  # The name of the test group, or 'all' [R]
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_stop_group(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if name is not None:
            data["name"] = name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/stop_group",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/STOP_PPP_LINK> type requests

        https://www.candelatech.com/lfcli_ug.php#stop_ppp_link
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_stop_ppp_link(self, 
                           resource: int = None,  # Resource number that holds this PppLink. [W]
                           shelf: int = 1,        # Name/id of the shelf. [R][D:1]
                           unit_num: str = None,  # Unit-Number for the PppLink to be stopped. [W]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_stop_ppp_link(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if unit_num is not None:
            data["unit_num"] = unit_num
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/stop_ppp_link",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/TAIL> type requests

        https://www.candelatech.com/lfcli_ug.php#tail
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_tail(self, 
                  cmd: str = None,       # Command: start, stop, results
                  key: str = None,       # File-name that we should be tailing.
                  message: str = None,   # The contents to display (for results only) <tt
                  # escapearg='false'>Unescaped Value</tt>
                  resource: int = None,  # Resource that holds the file. [W]
                  shelf: int = 1,        # Shelf that holds the resource that holds the file. [R][D:1]
                  debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_tail(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if cmd is not None:
            data["cmd"] = cmd
        if key is not None:
            data["key"] = key
        if message is not None:
            data["message"] = message
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/tail",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/TM_REGISTER> type requests

        https://www.candelatech.com/lfcli_ug.php#tm_register
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_tm_register(self, 
                         client_name: str = None,  # Name of client to be registered. (dflt is current client) [W]
                         test_mgr: str = None,     # Name of test manager (can be all.) [R]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_tm_register(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if client_name is not None:
            data["client_name"] = client_name
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/tm_register",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/TM_UNREGISTER> type requests

        https://www.candelatech.com/lfcli_ug.php#tm_unregister
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_tm_unregister(self, 
                           client_name: str = None,  # Name of client to be un-registered. (dflt is current client)
                           # [W]
                           test_mgr: str = None,     # Name of test manager (can be all.) [R]
                           debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_tm_unregister(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if client_name is not None:
            data["client_name"] = client_name
        if test_mgr is not None:
            data["test_mgr"] = test_mgr
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/tm_unregister",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/VERSION> type requests

        https://www.candelatech.com/lfcli_ug.php#version
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_version(self, 
                     debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_version(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/version",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/WHO> type requests

        https://www.candelatech.com/lfcli_ug.php#who
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_who(self, 
                 debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_who(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        response = self.json_post(url="/cli-json/who",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/WIFI_CLI_CMD> type requests

        https://www.candelatech.com/lfcli_ug.php#wifi_cli_cmd
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_wifi_cli_cmd(self, 
                          port: str = None,         # Name of the WiFi station or AP interface to which this command
                          # will be directed. [R]
                          resource: int = None,     # Resource number. [W]
                          shelf: int = 1,           # Shelf number. [R][D:1]
                          wpa_cli_cmd: str = None,  # Command to pass to wpa_cli or hostap_cli. This must be
                          # single-quoted. [R]
                          debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_wifi_cli_cmd(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if port is not None:
            data["port"] = port
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if wpa_cli_cmd is not None:
            data["wpa_cli_cmd"] = wpa_cli_cmd
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/wifi_cli_cmd",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/WIFI_EVENT> type requests

        https://www.candelatech.com/lfcli_ug.php#wifi_event
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_wifi_event(self, 
                        device: str = None,  # Interface or PHY in most cases. [R]
                        event: str = None,   # What happened. [R]
                        msg: str = None,     # Entire event in human readable form.
                        status: str = None,  # Status on what happened.
                        debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_wifi_event(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if device is not None:
            data["device"] = device
        if event is not None:
            data["event"] = event
        if msg is not None:
            data["msg"] = msg
        if status is not None:
            data["status"] = status
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/wifi_event",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/WISER_RESET> type requests

        https://www.candelatech.com/lfcli_ug.php#wiser_reset
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_wiser_reset(self, 
                         resource: int = None,  # Resource number, or ALL. [W]
                         shelf: int = 1,        # Shelf number, or ALL. [R][D:1]
                         debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_wiser_reset(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if resource is not None:
            data["resource"] = resource
        if shelf is not None:
            data["shelf"] = shelf
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/wiser_reset",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CLI-JSON/WRITE> type requests

        https://www.candelatech.com/lfcli_ug.php#write
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def post_write(self, 
                   db_name: str = None,  # The name the backup shall be saved as (blank means dflt)
                   debug=False):
        """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Example Usage: 
                result = post_write(param=value ...)
                pprint.pprint( result )
        ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
        debug |= self.debug_on
        data = {}
        if db_name is not None:
            data["db_name"] = db_name
        if len(data) < 1:
            raise ValueError(__name__+": no parameters to submit")
        response = self.json_post(url="/cli-json/write",
                                  post_data=data,
                                  die_on_error=self.die_on_error,
                                  debug=debug)
        return response
    #


class LFJsonQuery(JsonQuery):
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        LFJsonQuery inherits from JsonQuery.
        Queries are used for GET requests.
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def __init__(self,
                 session_obj: object = None,
                 debug: bool = False,
                 exit_on_error: bool = False):
        super().__init__(session_obj=session_obj,
                         debug=debug,
                         exit_on_error=exit_on_error)

    # Auto generated methods follow: 

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <ALERTS> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /alerts/
        /alerts/$event_id
        /alerts/before/$event_id
        /alerts/between/$start_event_id/$end_event_id
        /alerts/last/$event_count
        /alerts/since/$event_id

    When requesting specific column names, they need to be URL encoded:
        eid, entity+id, event, event+description, id, name, priority, time-stamp, 
        type
    Example URL: /alerts?fields=eid,entity+id

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_alerts(eid_list=['1.234', '1.344'],
                                      requested_col_names=['entity id'], 
                                      debug=True)

    The record returned will have these members: 
    {
        'eid':               # Time at which this event was created.This uses the clock on the source
                             # machine.
        'entity id':         # Entity IdentifierExact format depends on the
                             # type.(shelf.resource.port.endpoint.extra)
        'event':             # Event Type
        'event description': # Text description for this event.
        'id':                # Unique ID for this event.
        'name':              # Name of the entity associated with this event.
        'priority':          # Event priority.
        'time-stamp':        # Time at which this event was created.This uses the clock on the source
                             # machine.
        'type':              # Entity type.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_alerts(self, 
                   eid_list: list = None,
                   requested_col_names: list = None,
                   wait_sec: float = 0.01,
                   timeout_sec: float = 5.0,
                   errors_warnings: list = None,
                   debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/alerts"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="alert",
                                   plural_key="alerts")
    #
    """
        Below are 7 methods defined by LFClient URL Responders
    """

    def alerts_since(self,
                     event_id: int = None,
                     debug : bool = False,
                     wait_sec : float = None,
                     request_timeout_sec : float = None,
                     max_timeout_sec : float = None,
                     errors_warnings : list = None):
        """
        Select alerts since an alert ID
        :param event_id: earliest to start at
        """
        response = self.json_get(url="/alerts/alerts_since/{event_id}".format(event_id=event_id),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    def alerts_last_events(self,
                           event_count: int = None,
                           debug : bool = False,
                           wait_sec : float = None,
                           request_timeout_sec : float = None,
                           max_timeout_sec : float = None,
                           errors_warnings : list = None):
        """
        Select last event_count alerts
        :param event_count: number since end to select
        """
        response = self.json_get(url="/alerts/last/{event_count}".format(event_count=event_count),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    def alerts_before(self,
                      event_id: int = None,
                      debug : bool = False,
                      wait_sec : float = None,
                      request_timeout_sec : float = None,
                      max_timeout_sec : float = None,
                      errors_warnings : list = None):
        """
        Select first alerts before alert_id
        :param event_id: id to stop selecting at
        """
        response = self.json_get(url="/alerts/before/{event_id}".format(event_id=event_id),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    def events_between(self,
                       start_event_id: int = None,
                       end_event_id: int = None,
                       debug : bool = False,
                       wait_sec : float = None,
                       request_timeout_sec : float = None,
                       max_timeout_sec : float = None,
                       errors_warnings : list = None):
        """
        Select events between start and end IDs, inclusive
        :param start_event_id: start selection at this id
        :param end_event_id: end selection at this id
        """
        response = self.json_get(url="/events/between/{start_event_id}/{end_event_id}".format(start_event_id=start_event_id, end_event_id=end_event_id),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    def events_get_event(self,
                         event_id: int = None,
                         debug : bool = False,
                         wait_sec : float = None,
                         request_timeout_sec : float = None,
                         max_timeout_sec : float = None,
                         errors_warnings : list = None):
        """
        Query an event by id
        :param event_id: id to select
        """
        response = self.json_get(url="/events/{event_id}".format(event_id=event_id),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    def events_last_events(self,
                           event_count: int = None,
                           debug : bool = False,
                           wait_sec : float = None,
                           request_timeout_sec : float = None,
                           max_timeout_sec : float = None,
                           errors_warnings : list = None):
        """
        Select last event_count events
        :param event_count: number since end to select
        """
        response = self.json_get(url="/events/last/{event_count}".format(event_count=event_count),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    def events_since(self,
                     event_id: int = None,
                     debug : bool = False,
                     wait_sec : float = None,
                     request_timeout_sec : float = None,
                     max_timeout_sec : float = None,
                     errors_warnings : list = None):
        """
        Select events since an id
        :param event_id: event id to start at
        """
        response = self.json_get(url="/events/since/{event_id}".format(event_id=event_id),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return self.extract_values(response=response,
                                   singular_key="event",
                                   plural_key="events")
        #

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <ATTENUATOR> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /attenuator/
        /attenuator/$shelf_id
        /attenuator/$shelf_id/$resource_id
        /attenuator/$shelf_id/$resource_id/$port_id
        /attenuators/
        /attenuators/$shelf_id
        /attenuators/$shelf_id/$resource_id
        /attenuators/$shelf_id/$resource_id/$port_id

    When requesting specific column names, they need to be URL encoded:
        entity+id, module+1, module+2, module+3, module+4, module+5, module+6, module+7, 
        module+8, name, script, state, temperature
    Example URL: /attenuator?fields=entity+id,module+1

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_attenuator(eid_list=['1.234', '1.344'],
                                          requested_col_names=['entity id'], 
                                          debug=True)

    The record returned will have these members: 
    {
        'entity id':   # Entity ID
        'module 1':    # Reported attenuator dB settings.
        'module 2':    # Reported attenuator dB settings.
        'module 3':    # Reported attenuator dB settings.
        'module 4':    # Reported attenuator dB settings.
        'module 5':    # Reported attenuator dB settings.
        'module 6':    # Reported attenuator dB settings.
        'module 7':    # Reported attenuator dB settings.
        'module 8':    # Reported attenuator dB settings.
        'name':        # Attenuator module identifier (shelf . resource . serial-num).
        'script':      # Attenuator script state.
        'state':       # Attenuator state.
        'temperature': # Temperature in degres Farenheight reported in Attenuator unit.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_attenuator(self, 
                       eid_list: list = None,
                       requested_col_names: list = None,
                       wait_sec: float = 0.01,
                       timeout_sec: float = 5.0,
                       errors_warnings: list = None,
                       debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/attenuator"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="attenuator",
                                   plural_key="attenuators")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CHAMBER> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /chamber/
        /chamber/$chamber_name

    When requesting specific column names, they need to be URL encoded:
        chamber, chamber+connections, chamber+resources, chamber+type, duts, entity+id, 
        flags, hide, isolation, marked, open, reported+rotation+%28deg%29, reported+rpm, 
        reported+tilt+%28deg%29, resource, rotation+%28deg%29, rpm, smas, tilt+%28deg%29, turntable, 
        turntable+type, virtual
    Example URL: /chamber?fields=chamber,chamber+connections

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_chamber(eid_list=['1.234', '1.344'],
                                       requested_col_names=['entity id'], 
                                       debug=True)

    The record returned will have these members: 
    {
        'chamber':                 # -
        'chamber connections':     # -
        'chamber resources':       # -
        'chamber type':            # -
        'duts':                    # -
        'entity id':               # -
        'flags':                   # -
        'hide':                    # -
        'isolation':               # -
        'marked':                  # -
        'open':                    # -
        'reported rotation (deg)': # -
        'reported rpm ':           # -
        'reported tilt (deg)':     # -
        'resource':                # -
        'rotation (deg)':          # -
        'rpm':                     # -
        'smas':                    # -
        'tilt (deg)':              # -
        'turntable':               # -
        'turntable type':          # -
        'virtual':                 # -
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_chamber(self, 
                    eid_list: list = None,
                    requested_col_names: list = None,
                    wait_sec: float = 0.01,
                    timeout_sec: float = 5.0,
                    errors_warnings: list = None,
                    debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/chamber"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="chamber",
                                   plural_key="chambers")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CONTROL> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /control/$command

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_control(eid_list=['1.234', '1.344'],
                                       debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_control(self, 
                    eid_list: list = None,
                    requested_col_names: list = None,
                    wait_sec: float = 0.01,
                    timeout_sec: float = 5.0,
                    errors_warnings: list = None,
                    debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/control"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <CX> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /cx/
        /cx/$cx_id

    When requesting specific column names, they need to be URL encoded:
        avg+rtt, bps+rx+a, bps+rx+b, drop+pkts+a, drop+pkts+b, eid, endpoints+%28a%C2%A0%E2%86%94%C2%A0b%29, 
        entity+id, name, pkt+rx+a, pkt+rx+b, rpt+timer, rx+drop+%25+a, rx+drop+%25+b, 
        state, type
    Example URL: /cx?fields=avg+rtt,bps+rx+a

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_cx(eid_list=['1.234', '1.344'],
                                  requested_col_names=['entity id'], 
                                  debug=True)

    The record returned will have these members: 
    {
        'avg rtt':                            # Average Round-Trip-Time (latency) for this connection (ms).
        'bps rx a':                           # Endpoint A's real receive rate (bps).
        'bps rx b':                           # Endpoint B's real receive rate (bps).
        'drop pkts a':                        # The number of packets Endpoint B sent minus the number Endpoint A
                                              # received.This number is not 100% correct as long as packets are in
                                              # flight.After a Quiesce of the test, the number should be perfectly
                                              # accurate.
        'drop pkts b':                        # The number of packets Endpoint A sent minus the number Endpoint B
                                              # received.This number is not 100% correct as long as packets are in
                                              # flight.After a Quiesce of the test, the number should be perfectly
                                              # accurate.
        'eid':                                # Cross Connect's Name.
        'endpoints (a&nbsp;&#x2194;&nbsp;b)': # Endpoints that make up this Cross Connect.
        'entity id':                          # Cross Connect's Name.
        'name':                               # Cross Connect's Name.
        'pkt rx a':                           # Endpoint A's Packets Recieved.
        'pkt rx b':                           # Endpoint B's Packets Recieved.
        'rpt timer':                          # Cross Connect's Report Timer (milliseconds).This is how often the GUI
                                              # will ask for updates from the LANforge processes.If the GUI is sluggish,
                                              # increasing the report timers may help.
        'rx drop % a':                        # Endpoint A percentage packet loss.Calculated using the number of PDUs
                                              # Endpoint B sent minus the number Endpoint A received.This number is not
                                              # 100% correct as long as packets are in flight.After a Quiesce of the
                                              # test, the number should be perfectly accurate.
        'rx drop % b':                        # Endpoint B percentage packet loss.Calculated using the number of PDUs
                                              # Endpoint A sent minus the number Endpoint B received.This number is not
                                              # 100% correct as long as packets are in flight.After a Quiesce of the
                                              # test, the number should be perfectly accurate.
        'state':                              # Current State of the connection.UninitializedHas not yet been
                                              # started/stopped.InitializingBeing set up.StartingStarting the
                                              # test.RunningTest is actively running.StoppedTest has been
                                              # stopped.QuiesceTest will gracefully stop soon.HW-BYPASSTest is in
                                              # hardware-bypass mode (WanLinks only)FTM_WAITTest wants to run, but is
                                              # phantom, probably due to non-existent interface or resource.WAITINGWill
                                              # restart as soon as resources are available.PHANTOMTest is stopped, and
                                              # is phantom, probably due to non-existent interface or resource.
        'type':                               # Cross-Connect type.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_cx(self, 
               eid_list: list = None,
               requested_col_names: list = None,
               wait_sec: float = 0.01,
               timeout_sec: float = 5.0,
               errors_warnings: list = None,
               debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/cx"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <DUT> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /dut/
        /dut/$name

    When requesting specific column names, they need to be URL encoded:
        api+version, bssid-1, bssid-2, bssid-3, bssid-4, bssid-5, bssid-6, bssid-7, 
        bssid-8, dut, eap-id, entity+id, hw+info, image+file, lan, mgt+ip, model+number, 
        notes, num+ant+radio+1, num+ant+radio+2, num+ant+radio+3, password-1, password-2, 
        password-3, password-4, password-5, password-6, password-7, password-8, serial+number, 
        serial+port, ssid-1, ssid-2, ssid-3, ssid-4, ssid-5, ssid-6, ssid-7, ssid-8, 
        sw+info, wan
    Example URL: /dut?fields=api+version,bssid-1

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_dut(eid_list=['1.234', '1.344'],
                                   requested_col_names=['entity id'], 
                                   debug=True)

    The record returned will have these members: 
    {
        'api version':     # API Version
        'bssid-1':         # WiFi BSSID for DUT.
        'bssid-2':         # WiFi BSSID for DUT.
        'bssid-3':         # WiFi BSSID for DUT.
        'bssid-4':         # WiFi BSSID for DUT.
        'bssid-5':         # WiFi BSSID for DUT.
        'bssid-6':         # WiFi BSSID for DUT.
        'bssid-7':         # WiFi BSSID for DUT.
        'bssid-8':         # WiFi BSSID for DUT.
        'dut':             # Devices Under Test
        'eap-id':          # EAP Identifier, only used when one of the EAP options are selected.
        'entity id':       # Entity ID
        'hw info':         # DUT Hardware Info
        'image file':      # Image file name. Relative paths assume directory /home/lanforge. Fully
                           # qualified pathnames begin with a slash (eg
                           # /usr/lib/share/icons/icon.png).File format should be PNG, JPG or BMP.
        'lan':             # IP/Mask for LAN port (192.168.2.1/24).
        'mgt ip':          # DUT Management IP address.
        'model number':    # DUT model number or product name
        'notes':           # Notes
        'num ant radio 1': # Antenna count for DUT radio(s).
        'num ant radio 2': # Antenna count for DUT radio(s).
        'num ant radio 3': # Antenna count for DUT radio(s).
        'password-1':      # WiFi Password needed to connect to DUT.
        'password-2':      # WiFi Password needed to connect to DUT.
        'password-3':      # WiFi Password needed to connect to DUT.
        'password-4':      # WiFi Password needed to connect to DUT.
        'password-5':      # WiFi Password needed to connect to DUT.
        'password-6':      # WiFi Password needed to connect to DUT.
        'password-7':      # WiFi Password needed to connect to DUT.
        'password-8':      # WiFi Password needed to connect to DUT.
        'serial number':   # DUT Identifier (serial-number, or similar)
        'serial port':     # Resource and name of LANforge serial port that connects to this DUT.
                           # (1.1.ttyS0). Does not need to belong to lan_port or wan_port resource.
        'ssid-1':          # WiFi SSID advertised by DUT.
        'ssid-2':          # WiFi SSID advertised by DUT.
        'ssid-3':          # WiFi SSID advertised by DUT.
        'ssid-4':          # WiFi SSID advertised by DUT.
        'ssid-5':          # WiFi SSID advertised by DUT.
        'ssid-6':          # WiFi SSID advertised by DUT.
        'ssid-7':          # WiFi SSID advertised by DUT.
        'ssid-8':          # WiFi SSID advertised by DUT.
        'sw info':         # DUT Software Info
        'wan':             # IP/Mask for WAN port (192.168.3.2/24).
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_dut(self, 
                eid_list: list = None,
                requested_col_names: list = None,
                wait_sec: float = 0.01,
                timeout_sec: float = 5.0,
                errors_warnings: list = None,
                debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/dut"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="dut",
                                   plural_key="duts")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <ENDP> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /endp/
        /endp/$endp_id

    When requesting specific column names, they need to be URL encoded:
        1st+rx, a%2Fb, bursty, crc+fail, cwnd, cx+active, cx+estab, cx+estab%2Fs, cx+to, 
        delay, destination+addr, dropped, dup+pkts, eid, elapsed, entity+id, jitter, 
        max+pdu, max+rate, min+pdu, min+rate, mng, name, ooo+pkts, pattern, pdu%2Fs+rx, 
        pdu%2Fs+tx, pps+rx+ll, pps+tx+ll, rcv+buf, replays, run, rx+ber, rx+bytes, 
        rx+drop+%25, rx+dup+%25, rx+ooo+%25, rx+pdus, rx+pkts+ll, rx+rate, rx+rate+%281%C2%A0min%29, 
        rx+rate+%28last%29, rx+rate+ll, rx+wrong+dev, script, send+buf, source+addr, 
        tcp+mss, tcp+rtx, tx+bytes, tx+pdus, tx+pkts+ll, tx+rate, tx+rate+%281%C2%A0min%29, 
        tx+rate+%28last%29, tx+rate+ll        # hidden columns:
        drop-count-5m, latency-5m, rt-latency-5m, rx-silence-5m
    Example URL: /endp?fields=1st+rx,a%2Fb

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_endp(eid_list=['1.234', '1.344'],
                                    requested_col_names=['entity id'], 
                                    debug=True)

    The record returned will have these members: 
    {
        '1st rx':               # Miliseconds between starting the endpoint and receiving the first
                                # packet.Note that LANforge UDP connections (not including multicast) will
                                # wait 20msbefore sending first frame to make sure receiver has adequate
                                # time to start.
        'a/b':                  # Display side (A or B) for the endpoint.
        'bursty':               # Is the transmit rate bursty or not?
        'crc fail':             # Total packets received with a bad payload CRC.
        'cwnd':                 # Sender's TCP Current Window Size.  In units of Maximum Segment Size.
        'cx active':            # Total number of active connections for this endpoint.
        'cx estab':             # Total times the connection between the endpoints has been established.
        'cx estab/s':           # Connections established per second, averaged over the last 30 seconds.
        'cx to':                # Number of TCP connection attemtps timed out by LANforge.
        'delay':                # Average latency in milliseconds for packets received by this endpoint.
        'destination addr':     # Destination Address (MAC, ip/port, VoIP destination).
        'dropped':              # Total dropped packets, as identified by gaps in packet sequence numbers.
        'dup pkts':             # Total duplicate packets received.  Only an estimate, but never less than
                                # this value.
        'eid':                  # Entity ID
        'elapsed':              # Amount of time (seconds) this endpoint has been running (or ran.)
        'entity id':            # Entity ID
        'jitter':               # Exponential decaying average jitter calculated per RFC3393(old_jitter *
                                # 15/16 + new_jitter * 1/16)
        'max pdu':              # The maximum write size.For Ethernet protocols, this is the entire
                                # Ethernet frame. For UDP, it is the UDP payload size, and for TCP, it
                                # just means the maximum amount of data that is written per socket
                                # write.In all cases, the packets on the wire will not exceed theport's
                                # MTU + Ethernet-Header-Size (typically 1514 for Ethernet)
        'max rate':             # Maximum desired transmit rate, in bits per second (bps).
        'min pdu':              # The minimum write size.For Ethernet protocols, this is the entire
                                # Ethernet frame. For UDP, it is the UDP payload size, and for TCP, it
                                # just means the maximum amount of data that is written per socket
                                # write.In all cases, the packets on the wire will not exceed theport's
                                # MTU + Ethernet-Header-Size (typically 1514 for Ethernet)
        'min rate':             # Minimum desired transmit rate, in bits per second (bps).
        'mng':                  # Is the Endpoint managed or not?
        'name':                 # Endpoint's Name.
        'ooo pkts':             # Total out of order packets received.  Only an estimate, but never less
                                # than this value.
        'pattern':              # Pattern of bytes this endpoint transmits.
        'pdu/s rx':             # Received PDU per second.This counts the protocol reads, such as UDP
                                # PDUs.
        'pdu/s tx':             # Transmitted PDU per second.This counts the protocol writes, such as UDP
                                # PDUs.
        'pps rx ll':            # Estimated total received packets per second (on the wire).For TCP, this
                                # is an estimate.UDP and Ethernet protocols should be quite accurate on
                                # normal networks.
        'pps tx ll':            # Estimated total transmitted packets per second (on the wire).For TCP,
                                # this is an estimate.UDP and Ethernet protocols should be quite accurate
                                # on normal networks.
        'rcv buf':              # Configured/Actual values for receiving buffer size (bytes).
        'replays':              # Total number of files replayed.
        'run':                  # Is the Endpoint is Running or not.
        'rx ber':               # Received bit-errors.  These are only calculated in the LANforge payload
                                # portion starting 28 bytes into the UDP or TCP payload.  In addition, the
                                # bit-errors are only checked when LANforge CRCis enabled and detected to
                                # be invalid.  If the 28-byte header is corrupted, LANforge will not
                                # detectit, and may also give false positives for other packet errors.
                                # Bit-Errors are only calculated forcertain payload patterns:  Increasing,
                                # Decreasing, Zeros, Ones, and the PRBS patterns. 
        'rx bytes':             # Total received bytes count.
        'rx drop %':            # Percentage of packets that should have been received by Endpoint, but
                                # were not, as calculated by the Cross-Connect.
        'rx dup %':             # Percentage of duplicate packets, as detected by sequence numbers.
        'rx ooo %':             # Percentage of packets received out of order, as detected by sequence
                                # numbers.
        'rx pdus':              # Total received PDU count.This counts the protocol reads, such as UDP
                                # PDUs (aka goodput).
        'rx pkts ll':           # Estimated total received packet count (on the wire).For TCP, this is an
                                # estimate.UDP and Ethernet protocols should be quite accurate on normal
                                # networks.
        'rx rate':              # Real receive rate (bps) for this run.This includes only the protocol
                                # payload (goodput).
        'rx rate (1&nbsp;min)': # Real receive rate (bps) over the last minute.This includes only the
                                # protocol payload (goodput).
        'rx rate (last)':       # Real receive rate (bps) over the last report interval.This includes only
                                # the protocol payload (goodput).
        'rx rate ll':           # Estimated low-level receive rate (bps) over the last minute.This
                                # includes any Ethernet, IP, TCP, UDP or similar headers.
        'rx wrong dev':         # Total packets received on the wrong device (port).
        'script':               # Endpoint script state.
        'send buf':             # Configured/Actual values for sending buffer size (bytes).
        'source addr':          # 
        'tcp mss':              # Sender's TCP-MSS (max segment size) setting.This cooresponds to the
                                # TCP_MAXSEGS socket option,and TCP-MSS plus 54 is the maximum packet size
                                # on the wirefor Ethernet frames.This is a good option to efficiently
                                # limit TCP packet size.
        'tcp rtx':              # Total packets retransmitted by the TCP stack for this connection.These
                                # were likely dropped or corrupted in transit.
        'tx bytes':             # Total transmitted bytes count.
        'tx pdus':              # Total transmitted PDU count.This counts the protocol writes, such as UDP
                                # PDUs (aka goodput).
        'tx pkts ll':           # Estimated total transmitted packet count (on the wire).For TCP, this is
                                # an estimate.UDP and Ethernet protocols should be quite accurate on
                                # normal networks.
        'tx rate':              # Real transmit rate (bps) for this run.This includes only the protocol
                                # payload (goodput).
        'tx rate (1&nbsp;min)': # Real transmit rate (bps) over the last minute.This includes only the
                                # protocol payload (goodput).
        'tx rate (last)':       # Real transmit rate (bps) over the last report interval.This includes
                                # only the protocol payload (goodput).
        'tx rate ll':           # Estimated low-level transmit rate (bps) over the last minute.This
                                # includes any Ethernet, IP, TCP, UDP or similar headers.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_endp(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/endp"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="endpoint",
                                   plural_key="endpoint")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <ENDSESSION> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /endsession

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_endsession(eid_list=['1.234', '1.344'],
                                          debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_endsession(self, 
                       eid_list: list = None,
                       requested_col_names: list = None,
                       wait_sec: float = 0.01,
                       timeout_sec: float = 5.0,
                       errors_warnings: list = None,
                       debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/endsession"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <EVENTS> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /events/
        /events/$event_id
        /events/before/$event_id
        /events/between/$start_event_id/$end_event_id
        /events/last/$event_count
        /events/since/$event_id

    When requesting specific column names, they need to be URL encoded:
        eid, entity+id, event, event+description, id, name, priority, time-stamp, 
        type
    Example URL: /events?fields=eid,entity+id

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_events(eid_list=['1.234', '1.344'],
                                      requested_col_names=['entity id'], 
                                      debug=True)

    The record returned will have these members: 
    {
        'eid':               # Time at which this event was created.This uses the clock on the source
                             # machine.
        'entity id':         # Entity IdentifierExact format depends on the
                             # type.(shelf.resource.port.endpoint.extra)
        'event':             # Event Type
        'event description': # Text description for this event.
        'id':                # Unique ID for this event.
        'name':              # Name of the entity associated with this event.
        'priority':          # Event priority.
        'time-stamp':        # Time at which this event was created.This uses the clock on the source
                             # machine.
        'type':              # Entity type.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_events(self, 
                   eid_list: list = None,
                   requested_col_names: list = None,
                   wait_sec: float = 0.01,
                   timeout_sec: float = 5.0,
                   errors_warnings: list = None,
                   debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/events"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="alert",
                                   plural_key="alerts")
    #
    """
        Below are 7 methods defined by LFClient URL Responders
    """

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <FILEIO> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /fileio/
        /fileio/$endp_id

    When requesting specific column names, they need to be URL encoded:
        buf-rd, buf-wr, bytes-rd, bytes-wr, crc+fail, eid, entity+id, files+%23, files-read, 
        files-wr, io+fail, max-file-sz, max-rd-bps, max-rw-sz, max-wr-bps, min-file-sz, 
        min-rd-bps, min-rw-sz, min-wr-bps, name, read-bps, rpt+timer, rx-bps-20s, 
        status, tx-bps-20s, type, write-bps
    Example URL: /fileio?fields=buf-rd,buf-wr

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_fileio(eid_list=['1.234', '1.344'],
                                      requested_col_names=['entity id'], 
                                      debug=True)

    The record returned will have these members: 
    {
        'buf-rd':      # Buffer reads.  When doing CRC, it takes two reads per 'packet', because
                       # we first read the header, then the payload.  Non-CRC reads ignore the
                       # header.
        'buf-wr':      # Buffer writes.
        'bytes-rd':    # Bytes read.
        'bytes-wr':    # Bytes written.
        'crc fail':    # 32-bit CRC Errors detected upon READ.
        'eid':         # Entity ID
        'entity id':   # Entity ID
        'files #':     # Number of files to write.
        'files-read':  # Files read.
        'files-wr':    # Files written.
        'io fail':     # Amount of time in miliseconds this test has been experiencing IO
                       # failures.
        'max-file-sz': # Maximum configured file size (bytes).
        'max-rd-bps':  # Maximum configured read rate (bps).
        'max-rw-sz':   # Maximum configured size for each call to read(2) or write(2) (bytes).
        'max-wr-bps':  # Maximum configured write rate (bps).
        'min-file-sz': # Minimum configured file size (bytes).
        'min-rd-bps':  # Minimum configured read rate (bps).
        'min-rw-sz':   # Minimum configured size for each call to read(2) or write(2) (bytes).
        'min-wr-bps':  # Minimum configured write rate (bps).
        'name':        # File Endpoint's Name.
        'read-bps':    # File read rate for this endpoint over the duration of the test.
        'rpt timer':   # Report Timer (milliseconds).This is how often the GUI will ask for
                       # updates from the LANforge processes.If the GUI is sluggish, increasing
                       # the report timers may help.
        'rx-bps-20s':  # File read rate for this endpoint over the last 20 seconds.
        'status':      # Current State of the connection.UninitializedHas not yet been
                       # started/stopped.InitializingBeing set up.StartingStarting the
                       # test.RunningTest is actively running.StoppedTest has been
                       # stopped.QuiesceTest will gracefully stop soon.HW-BYPASSTest is in
                       # hardware-bypass mode (WanLinks only)FTM_WAITTest wants to run, but is
                       # phantom, probably due to non-existent interface or resource.WAITINGWill
                       # restart as soon as resources are available.PHANTOMTest is stopped, and
                       # is phantom, probably due to non-existent interface or resource.
        'tx-bps-20s':  # File write rate for this endpoint over the last 20 seconds.
        'type':        # The specific type of this File Endpoint.
        'write-bps':   # File write rate for this endpoint over the duration of the test.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_fileio(self, 
                   eid_list: list = None,
                   requested_col_names: list = None,
                   wait_sec: float = 0.01,
                   timeout_sec: float = 5.0,
                   errors_warnings: list = None,
                   debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/fileio"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="endpoint",
                                   plural_key="endpoint")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <GENERIC> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /generic/
        /generic/$endp_id

    When requesting specific column names, they need to be URL encoded:
        bps+rx, bps+tx, command, dropped, eid, elapsed, entity+id, last+results, 
        name, pdu%2Fs+rx, pdu%2Fs+tx, rpt+timer, rpt%23, rx+bytes, rx+pkts, status, tx+bytes, 
        tx+pkts, type
    Example URL: /generic?fields=bps+rx,bps+tx

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_generic(eid_list=['1.234', '1.344'],
                                       requested_col_names=['entity id'], 
                                       debug=True)

    The record returned will have these members: 
    {
        'bps rx':       # Receive rate reported by this endpoint.
        'bps tx':       # Transmit rate reported by this endpoint.
        'command':      # The command that this endpoint executes.
        'dropped':      # Dropped PDUs reported by this endpoint.
        'eid':          # Entity ID
        'elapsed':      # Amount of time (seconds) this endpoint has been running (or ran.)
        'entity id':    # Entity ID
        'last results': # Latest output from the Generic Endpoint.
        'name':         # Endpoint's Name.
        'pdu/s rx':     # Received packets-per-second reported by this endpoint.
        'pdu/s tx':     # Transmitted packets-per-second reported by this endpoint.
        'rpt timer':    # Report Timer (milliseconds).This is how often the GUI will ask for
                        # updates from the LANforge processes.If the GUI is sluggish, increasing
                        # the report timers may help.
        'rpt#':         # The N_th report that we have received. (Some cmds will produce only one
                        # report, others will produce continuous reports.)
        'rx bytes':     # Received bytes reported by this endpoint.
        'rx pkts':      # Received PDUs reported by this endpoint.
        'status':       # Current State of the connection.UninitializedHas not yet been
                        # started/stopped.InitializingBeing set up.StartingStarting the
                        # test.RunningTest is actively running.StoppedTest has been
                        # stopped.QuiesceTest will gracefully stop soon.HW-BYPASSTest is in
                        # hardware-bypass mode (WanLinks only)FTM_WAITTest wants to run, but is
                        # phantom, probably due to non-existent interface or resource.WAITINGWill
                        # restart as soon as resources are available.PHANTOMTest is stopped, and
                        # is phantom, probably due to non-existent interface or resource.
        'tx bytes':     # Transmitted bytes reported by this endpoint.
        'tx pkts':      # Transmitted PDUs reported by this endpoint.
        'type':         # The specific type of this Generic Endpoint.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_generic(self, 
                    eid_list: list = None,
                    requested_col_names: list = None,
                    wait_sec: float = 0.01,
                    timeout_sec: float = 5.0,
                    errors_warnings: list = None,
                    debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/generic"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="endpoint",
                                   plural_key="endpoints")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <GUI-CLI> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /gui-cli/

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_gui_cli(eid_list=['1.234', '1.344'],
                                       debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_gui_cli(self, 
                    eid_list: list = None,
                    requested_col_names: list = None,
                    wait_sec: float = 0.01,
                    timeout_sec: float = 5.0,
                    errors_warnings: list = None,
                    debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/gui-cli"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <LAYER4> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /layer4/
        /layer4/$endp_id

    When requesting specific column names, they need to be URL encoded:
        %21conn, acc.+denied, bad-proto, bad-url, bytes-rd, bytes-wr, dns-avg, dns-max, 
        dns-min, eid, elapsed, entity+id, fb-avg, fb-max, fb-min, ftp-host, ftp-port, 
        ftp-stor, http-p, http-r, http-t, login-denied, name, nf+%284xx%29, other-err, 
        read, redir, rpt+timer, rslv-h, rslv-p, rx+rate, rx+rate+%281%C2%A0min%29, status, 
        timeout, total-err, total-urls, tx+rate, tx+rate+%281%C2%A0min%29, type, uc-avg, 
        uc-max, uc-min, urls%2Fs, write        # hidden columns:
        rpt-time
    Example URL: /layer4?fields=%21conn,acc.+denied

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_layer4(eid_list=['1.234', '1.344'],
                                      requested_col_names=['entity id'], 
                                      debug=True)

    The record returned will have these members: 
    {
        '!conn':                # Could not establish connection.
        'acc. denied':          # Access Access Denied Error.This could be password, user-name,
                                # file-permissions or other error.
        'bad-proto':            # Bad protocol.
        'bad-url':              # Bad URL format.
        'bytes-rd':             # Bytes read.
        'bytes-wr':             # Bytes written.
        'dns-avg':              # Average time in milliseconds to complete resolving the DNS lookupfor the
                                # last 100 requests.
        'dns-max':              # Maximum time in milliseconds to complete resolving the DNS lookupfor
                                # requests made in the last 30 seconds.
        'dns-min':              # Minimum time in milliseconds to complete resolving the DNS lookupfor
                                # requests made in the last 30 seconds.
        'eid':                  # EID
        'elapsed':              # Amount of time (seconds) this endpoint has been running (or ran.)
        'entity id':            # Entity ID
        'fb-avg':               # Average time in milliseconds for receiving the first byte of the URLfor
                                # the last 100 requests.
        'fb-max':               # Maximum time in milliseconds for receiving the first byte of the URLfor
                                # requests made in the last 30 seconds.
        'fb-min':               # Minimum time in milliseconds for receiving the first byte of the URLfor
                                # requests made in the last 30 seconds.
        'ftp-host':             # FTP HOST Error
        'ftp-port':             # FTP PORT Error.
        'ftp-stor':             # FTP STOR Error.
        'http-p':               # HTTP Post error.
        'http-r':               # HTTP RANGE error.
        'http-t':               # HTTP PORT Error.
        'login-denied':         # Login attempt was denied.Probable cause is user-name or password errors.
        'name':                 # Endpoint's Name.
        'nf (4xx)':             # File not found.For HTTP, an HTTP 4XX error was returned.  This is only
                                # counted when the endpoint has 'Enable 4XX' selected.Includes 403
                                # permission denied and 404 not found errors.For other protocols, it
                                # should be returned any time a file is not found.
        'other-err':            # Error not otherwise specified.  The actual error code may be found
                                # inl4helper logs.  Contact support if you see these errors:we would like
                                # to account for all possible errors.
        'read':                 # Error attempting to read file or URL.
        'redir':                # Noticed redirect loop!
        'rpt timer':            # Cross Connect's Report Timer (milliseconds).This is how often the GUI
                                # will ask for updates from the LANforge processes.If the GUI is sluggish,
                                # increasing the report timers may help.
        'rslv-h':               # Couldn't resolve host.
        'rslv-p':               # Couldn't resolve Proxy.
        'rx rate':              # Payload receive rate (bps).
        'rx rate (1&nbsp;min)': # Payload receive rate over the last minute (bps).
        'status':               # Current State of the connection.UninitializedHas not yet been
                                # started/stopped.InitializingBeing set up.StartingStarting the
                                # test.RunningTest is actively running.StoppedTest has been
                                # stopped.QuiesceTest will gracefully stop soon.HW-BYPASSTest is in
                                # hardware-bypass mode (WanLinks only)FTM_WAITTest wants to run, but is
                                # phantom, probably due to non-existent interface or resource.WAITINGWill
                                # restart as soon as resources are available.PHANTOMTest is stopped, and
                                # is phantom, probably due to non-existent interface or resource.
        'timeout':              # Operation timed out.
        'total-err':            # Total Errors.
        'total-urls':           # URLs processed.
        'tx rate':              # Payload transmit rate (bps).
        'tx rate (1&nbsp;min)': # Payload transmit rate over the last minute (bps).
        'type':                 # The specific type of this Layer 4-7 Endpoint.
        'uc-avg':               # Average time in milliseconds to complete processing of the URLfor the
                                # last 100 requests.
        'uc-max':               # Maximum time in milliseconds to complete processing of the URLfor
                                # requests made in the last 30 seconds.
        'uc-min':               # Minimum time in milliseconds to complete processing of the URLfor
                                # requests made in the last 30 seconds.
        'urls/s':               # URLs processed per second over the last minute.
        'write':                # Error attempting to write file or URL.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_layer4(self, 
                   eid_list: list = None,
                   requested_col_names: list = None,
                   wait_sec: float = 0.01,
                   timeout_sec: float = 5.0,
                   errors_warnings: list = None,
                   debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/layer4"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="endpoint",
                                   plural_key="endpoint")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <NEWSESSION> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /newsession

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_newsession(eid_list=['1.234', '1.344'],
                                          debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_newsession(self, 
                       eid_list: list = None,
                       requested_col_names: list = None,
                       wait_sec: float = 0.01,
                       timeout_sec: float = 5.0,
                       errors_warnings: list = None,
                       debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/newsession"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <PORT> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /port/
        /port/$shelf_id
        /port/$shelf_id/$resource_id
        /port/$shelf_id/$resource_id/$port_id
        /portprobe/
        /portprobe/$shelf_id/$resource_id/$port_id
        /ports/
        /ports/$shelf_id
        /ports/$shelf_id/$resource_id
        /ports/$shelf_id/$resource_id/$port_id

    When requesting specific column names, they need to be URL encoded:
        4way+time+%28us%29, activity, alias, anqp+time+%28us%29, ap, beacon, bps+rx, bps+rx+ll, 
        bps+tx, bps+tx+ll, bytes+rx+ll, bytes+tx+ll, channel, collisions, connections, 
        crypt, cx+ago, cx+time+%28us%29, device, dhcp+%28ms%29, down, entity+id, gateway+ip, 
        ip, ipv6+address, ipv6+gateway, key%2Fphrase, login-fail, login-ok, logout-fail, 
        logout-ok, mac, mask, misc, mode, mtu, no+cx+%28us%29, noise, parent+dev, phantom, 
        port, port+type, pps+rx, pps+tx, qlen, reset, retry+failed, rx+bytes, rx+crc, 
        rx+drop, rx+errors, rx+fifo, rx+frame, rx+length, rx+miss, rx+over, rx+pkts, 
        rx-rate, sec, signal, ssid, status, time-stamp, tx+abort, tx+bytes, tx+crr, 
        tx+errors, tx+fifo, tx+hb, tx+pkts, tx+wind, tx-failed+%25, tx-rate, wifi+retries, 
              # hidden columns:
        beacon_rx_signal, port_cur_flags_h, port_cur_flags_l, port_supported_flags_h, 
        port_supported_flags_l, resource, rx_multicast, tx_dropped
    Example URL: /port?fields=4way+time+%28us%29,activity

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_port(eid_list=['1.234', '1.344'],
                                    requested_col_names=['entity id'], 
                                    debug=True)

    The record returned will have these members: 
    {
        '4way time (us)': # TIme (in micro-seconds) it took to complete the last WiFi 4-way
                          # authentication.
        'activity':       # Percent of the channel that is utilized over the last minute.This
                          # includes locally generated traffic as well as anyother systems active on
                          # this channel.This is a per-radio value.
        'alias':          # User-specified alias for this Port.
        'anqp time (us)': # Time (in micro-seconds) it took to complete the last WiFi ANQP
                          # request/response session.
        'ap':             # BSSID of AP for connected stations.
        'beacon':         # Number of Wireless beacons from Cell or AP that have been missed.
        'bps rx':         # Average bits per second received for the last 30 seconds.
        'bps rx ll':      # Bits per second received, including low-level framing (Ethernet Only).
        'bps tx':         # Average bits per second transmitted for the last 30 seconds.
        'bps tx ll':      # Bits per second transmitted, including low-level framing (Ethernet
                          # Only).
        'bytes rx ll':    # Bytes received, including low-level framing (Ethernet Only).
        'bytes tx ll':    # Bytes transmitted, including low-level framing (Ethernet Only).
        'channel':        # Channel at the device is currently on, if known.
        'collisions':     # Total number of collisions reported by this Interface.For WiFi devices,
                          # this is number of re-transmit attempts.
        'connections':    # Number of wireless connections completed.
        'crypt':          # Number of Wireless packets dropped due to inability to decrypt.
        'cx ago':         # How long ago was the last WiFi connection attempt started?This relates
                          # only to the network interface, not any higher level protocol traffic
                          # upon it.
        'cx time (us)':   # Time (in micro-seconds) it took to complete the last WiFi connection to
                          # the AP.
        'device':         # Ethernet device name, as seen by the kernel.
        'dhcp (ms)':      # Time (in miliseconds) it took to acquire DHCP lease,or to time out while
                          # trying to acquire lease.
        'down':           # The interface is configured DOWN.  It must be configured UP to be in
                          # active use.
        'entity id':      # Entity ID
        'gateway ip':     # Default Router/Gateway IP for the Interface.
        'ip':             # IP Address of the Interface.
        'ipv6 address':   # IPv6 Address for this interface.  If global-scope address exists, it
                          # will be displayed,otherwise link-local will be displayed.
        'ipv6 gateway':   # IPv6 default gateway.
        'key/phrase':     # WEP Key or WPA Phrase (if enabled).
        'login-fail':     # The 'ifup-post' script reported failure.  This is usually used for WiFi
                          # portallogins, but may be customized by the user for other needs.
        'login-ok':       # The 'ifup-post' script reported OK.  This is usually used for WiFi
                          # portallogins, but may be customized by the user for other needs.
        'logout-fail':    # The 'ifup-post --logout' script reported failure.  This is usually used
                          # for WiFi portallogouts, but may be customized by the user for other
                          # needs.
        'logout-ok':      # The 'ifup-post --logout' script reported OK.  This is usually used for
                          # WiFi portallogouts, but may be customized by the user for other needs.
        'mac':            # Ethernet MAC address of the Interface.
        'mask':           # IP Mask of the Interface.
        'misc':           # Number of Wireless packets dropped on receive due to unspecified
                          # reasons.
        'mode':           # Wireless radio mode (802.11a/b/g).
        'mtu':            # MTU (Maximum Transmit Unit) size, in bytes.
        'no cx (us)':     # How long was the WiFi disconnect duration for the last disconnection?
        'noise':          # Wireless noise level.
        'parent dev':     # Parent device or port of this port. Blank if this device is not a child
                          # of another device or port.
        'phantom':        # Is the port PHANTOM (no hardware found) or not.
        'port':           # Entity ID
        'port type':      # Ports can be Ethernet, Radio, vAP, vSTA, Redirect, or Bridges
        'pps rx':         # Average packets per second received for the last 30 seconds.
        'pps tx':         # Average packets per second transmitted for the last 30 seconds.
        'qlen':           # "Transmit Queue Length for this Interface.
        'reset':          # Current Reset-State.
        'retry failed':   # Number of Wireless packets that the interface failed to send due to
                          # excessive retries.
        'rx bytes':       # Total number of bytes received by this Interface.
        'rx crc':         # Total number of packets dropped because of a bad CRC/FCS.
        'rx drop':        # Total number of dropped packets on recieve.  Usually means driver/kernel
                          # is being over-worked.
        'rx errors':      # Total number of all types of Receive Errors.
        'rx fifo':        # Total number of packets dropped because driver/kernel queues are full.
        'rx frame':       # Total number of packets dropped because of framing errors at the
                          # physical layer.
        'rx length':      # Total number of packets dropped because their length was invalid.
        'rx miss':        # Total number of packets dropped because of a missed interrupt.
        'rx over':        # Total number of packets dropped because of framing errors at the
                          # physical layer.
        'rx pkts':        # Total number of packets received by this Interface.
        'rx-rate':        # Reported network device RX link speed.
        'sec':            # Number of secondary IP addresses configured or detected.
        'signal':         # Wireless signal strength (RSSI).
        'ssid':           # WiFi SSID identifier.Use [BLANK] for empty SSID, which means use any
                          # available SSID when associating.
        'status':         # Wireless link status.
        'time-stamp':     # Time-Stamp
        'tx abort':       # Total packets dropped on transmit because of driver abort.
        'tx bytes':       # Total number of bytes sent by this Interface.
        'tx crr':         # Total packets dropped on transmit because of carrier error.
        'tx errors':      # Total number of all types of Transmit Errors.
        'tx fifo':        # Total packets dropped on transmit because outgoing queue was full.
        'tx hb':          # Total packets dropped on transmit because of transceiver heartbeat
                          # errors.
        'tx pkts':        # Total number of packets sent by this Interface.
        'tx wind':        # Total number dropped on transmit because of Out-of-Window collision.
        'tx-failed %':    # Percentage of transmitted Wireless packets that were not ACKed.They
                          # might have succeeded on retry.
        'tx-rate':        # Reported network device TX link speed.
        'wifi retries':   # Number of Wireless packets that the wifi radio retried.One packet may be
                          # tried multiple times and each try would be counted in this stat.Not all
                          # radios can properly report this statistic.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_port(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/port"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="interface",
                                   plural_key="interfaces")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <PROBE> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /probe/
        /probe/$shelf_id/$resource_id/$port_id

    When requesting specific column names, they need to be URL encoded:
        entity+id, probe+results
    Example URL: /probe?fields=entity+id,probe+results

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_probe(eid_list=['1.234', '1.344'],
                                     requested_col_names=['probe results'], 
                                     debug=True)

    The record returned will have these members: 
    {
        'entity id':     # Entity ID
        'probe results': # Probe the low level information about the port.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_probe(self, 
                  eid_list: list = None,
                  requested_col_names: list = None,
                  wait_sec: float = 0.01,
                  timeout_sec: float = 5.0,
                  errors_warnings: list = None,
                  debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/probe"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="probe-results",
                                   plural_key="probe-results")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <QUIT> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /quit

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_quit(eid_list=['1.234', '1.344'],
                                    debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_quit(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/quit"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <RADIOSTATUS> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /radiostatus/
        /radiostatus/$eid
        /radiostatus/$shelf_id/$resource_id/$port_id

    When requesting specific column names, they need to be URL encoded:
        _links, antenna, ap, capabilities, channel, country, driver, entity+id, firmware+version, 
        frag, frequency, max_sta, max_vap, max_vifs, monitors_down, monitors_up, 
        phantom, port, resource, rts, stations_down, stations_up, tx-power, vaps_down, 
        vaps_up, verbose+debug
    Example URL: /radiostatus?fields=_links,antenna

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_radiostatus(eid_list=['1.234', '1.344'],
                                           requested_col_names=['firmware version'], 
                                           debug=True)

    The record returned will have these members: 
    {
        '_links':           # -
        'antenna':          # -
        'ap':               # -
        'capabilities':     # -
        'channel':          # -
        'country':          # -
        'driver':           # -
        'entity id':        # -
        'firmware version': # -
        'frag':             # -
        'frequency':        # -
        'max_sta':          # -
        'max_vap':          # -
        'max_vifs':         # -
        'monitors_down':    # -
        'monitors_up':      # -
        'phantom':          # -
        'port':             # -
        'resource':         # -
        'rts':              # -
        'stations_down':    # -
        'stations_up':      # -
        'tx-power':         # -
        'vaps_down':        # -
        'vaps_up':          # -
        'verbose debug':    # -
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_radiostatus(self, 
                        eid_list: list = None,
                        requested_col_names: list = None,
                        wait_sec: float = 0.01,
                        timeout_sec: float = 5.0,
                        errors_warnings: list = None,
                        debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/radiostatus"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="radio",
                                   plural_key="radios")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <RESOURCE> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /resource/
        /resource/$shelf_id
        /resource/$shelf_id/$resource_id

    When requesting specific column names, they need to be URL encoded:
        bps-rx-3s, bps-tx-3s, cli-port, cpu, ctrl-ip, ctrl-port, eid, entity+id, 
        free+mem, free+swap, gps, hostname, hw+version, load, max+if-up, max+staged, 
        mem, phantom, ports, rx+bytes, shelf, sta+up, sw+version, swap, tx+bytes, 
              # hidden columns:
        timestamp
    Example URL: /resource?fields=bps-rx-3s,bps-tx-3s

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_resource(eid_list=['1.234', '1.344'],
                                        requested_col_names=['entity id'], 
                                        debug=True)

    The record returned will have these members: 
    {
        'bps-rx-3s':  # Rate in bits-per-second that the manager issending management data to
                      # the resource, averaged over the last 3 seconds.This is TCP payload data,
                      # and does not count the IP and Ethernet overhead.
        'bps-tx-3s':  # Rate in bits-per-second that the manager isreceiving management data
                      # from the resource, averaged over the last 3 seconds.This is TCP payload
                      # data, and does not count the IP and Ethernet overhead.
        'cli-port':   # Text (telnet) interface IP Port.
        'cpu':        # CPU information for the machine.
        'ctrl-ip':    # IP Address of the Control Interface.
        'ctrl-port':  # Binary interface IP Port.
        'eid':        # Resource EID (Shelf.Resource).
        'entity id':  # Entity ID
        'free mem':   # Free Memory (Kbytes) in the machine.  If this is too low, performance
                      # will be degraded.
        'free swap':  # Free Swap (Kbytes) in the machine.  If this is too low, performance will
                      # be degraded.
        'gps':        # GPS Info for this machine, if GPS is attached.
        'hostname':   # The name for this resource, as reported by the resource.
        'hw version': # Hardware version on the machine.
        'load':       # Unix process load..
        'max if-up':  # Max number of interface-config scripts try to run at once.
        'max staged': # Max number of interfaces the system will try to bringup at once.
        'mem':        # Total memory (Kbytes) on the machine.
        'phantom':    # Is the resource PHANTOM (undiscovered) or not.
        'ports':      # All real and phantom ports on this machine.
        'rx bytes':   # Total management TCP payload bytes received from the manager process by
                      # this resource.
        'shelf':      # Number of shelf that this resource belongs to.
        'sta up':     # Max number of stations to bring up per radio per 0.25s tick.
        'sw version': # LANforge Software version running on the machine.
        'swap':       # Total swap space (Kbytes) on the machine.
        'tx bytes':   # Total management TCP payload bytes sent from this resource to the
                      # manager process.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_resource(self, 
                     eid_list: list = None,
                     requested_col_names: list = None,
                     wait_sec: float = 0.01,
                     timeout_sec: float = 5.0,
                     errors_warnings: list = None,
                     debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/resource"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="resource",
                                   plural_key="resources")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <SCAN> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /scan-results/
        /scan-results/$shelf_id/$resource_id/$port_id
        /scan-results/$shelf_id/$resource_id/$port_id/$bssid
        /scan/
        /scan/$shelf_id/$resource_id/$port_id
        /scan/$shelf_id/$resource_id/$port_id/$bssid
        /scanresults/
        /scanresults/$shelf_id/$resource_id/$port_id
        /scanresults/$shelf_id/$resource_id/$port_id/$bssid

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_scan(eid_list=['1.234', '1.344'],
                                    debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_scan(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/scan"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="scan-results",
                                   plural_key="scan-results")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <STATIONS> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /stations/
        /stations/$mac

    When requesting specific column names, they need to be URL encoded:
        ap, auth-for, capabilities, entity+id, idle, roam-duration, rx+bytes, rx+pkts, 
        rx+rate, signal, station+bssid, tx+bytes, tx+pkts, tx+rate, tx+retries, tx-failed, 
      
    Example URL: /stations?fields=ap,auth-for

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_stations(eid_list=['1.234', '1.344'],
                                        requested_col_names=['entity id'], 
                                        debug=True)

    The record returned will have these members: 
    {
        'ap':            # The Port that owns this station.
        'auth-for':      # Duration in seconds this station has been authenticated.
        'capabilities':  # Station's negotiated capabilities.
        'entity id':     # Entity ID
        'idle':          # Miliseconds since this station last received a frame from the peer.
        'roam-duration': # The difference between the authenticate-time on the new APand the last
                         # frame received on old AP, in milliseconds.It is not always possible to
                         # compute this accurately,especially if traffic is not flowing during the
                         # roam.
        'rx bytes':      # RX Byte counter for this station.
        'rx pkts':       # RX Packets counter for this station.
        'rx rate':       # Station last received encoding rate.
        'signal':        # Station signal quality.
        'station bssid': # Station's MAC address (BSSID).
        'tx bytes':      # TX Byte counter for this station.
        'tx pkts':       # TX Packets counter for this station.
        'tx rate':       # Station transmit encoding rate.
        'tx retries':    # TX Retries counter for this station.This counts retries at the driver
                         # level.Retries made by the WiFi hardware and/or firmware is not counted.
        'tx-failed':     # TX Failed counter for this station.This counts TX failures at the driver
                         # level.The hardware and/or firmware may have made several failed attempts
                         # that are not included in this counter.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_stations(self, 
                     eid_list: list = None,
                     requested_col_names: list = None,
                     wait_sec: float = 0.01,
                     timeout_sec: float = 5.0,
                     errors_warnings: list = None,
                     debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/stations"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="station",
                                   plural_key="stations")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <STATUS-MSG> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /status-msg/
        /status-msg/$session
        /status-msg/$session/$id
        /status-msg/$session/$id/ws-msg,...
        /status-msg/$session/all
        /status-msg/$session/this
        /status-msg/sessions

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_status_msg(eid_list=['1.234', '1.344'],
                                          debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_status_msg(self, 
                       eid_list: list = None,
                       requested_col_names: list = None,
                       wait_sec: float = 0.01,
                       timeout_sec: float = 5.0,
                       errors_warnings: list = None,
                       debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/status-msg"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="sessions/messages",
                                   plural_key="sessions/messages")
    #
    """
        Below are 3 methods defined by LFClient URL Responders
    """

    def status_msg_new_session(self,
                               session : str = None,
                               debug : bool = False,
                               wait_sec : float = None,
                               request_timeout_sec : float = None,
                               max_timeout_sec : float = None,
                               errors_warnings : list = None):
        """
        Add a status message
        :param [R]session: session ID [R]
        """
        response = self.json_put(url="/status-msg/{session}".format(session=session),
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=request_timeout_sec,
                                 max_timeout_sec=max_timeout_sec,
                                 errors_warnings=errors_warnings)
        if not response:
            return None
        return response

    def status_msg_delete_session(self,
                                  session : str = None,
                                  debug : bool = False,
                                  wait_sec : float = None,
                                  request_timeout_sec : float = None,
                                  max_timeout_sec : float = None,
                                  errors_warnings : list = None):
        """
        Delete a status-msg session
        :param session: id to delete
        """
        response = self.json_delete(url="/status-msg/{session}".format(session=session),
                                    debug=debug,
                                    wait_sec=wait_sec,
                                    request_timeout_sec=request_timeout_sec,
                                    max_timeout_sec=max_timeout_sec,
                                    errors_warnings=errors_warnings)
        if not response:
            return None
        return response

    def status_msg_delete_message(self,
                                  session : str = None,
                                  key : str = None,
                                  debug : bool = False,
                                  wait_sec : float = None,
                                  request_timeout_sec : float = None,
                                  max_timeout_sec : float = None,
                                  errors_warnings : list = None):
        """
        Delete a status message
        :param session: session ID
        :param key: item ID
        """
        response = self.json_delete(url="/status-msg/{session}/{key}".format(session=session, key=key),
                                    debug=debug,
                                    wait_sec=wait_sec,
                                    request_timeout_sec=request_timeout_sec,
                                    max_timeout_sec=max_timeout_sec,
                                    errors_warnings=errors_warnings)
        if not response:
            return None
        return response

    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <TEST-GROUP> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /test-group/
        /test-group/$id
        /test-groups/
        /test-groups/$id

    When requesting specific column names, they need to be URL encoded:
        cross+connects, entity+id, name, run, script
    Example URL: /test-group?fields=cross+connects,entity+id

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_test_group(eid_list=['1.234', '1.344'],
                                          requested_col_names=['entity id'], 
                                          debug=True)

    The record returned will have these members: 
    {
        'cross connects': # List of Test Manager's Cross-Connects.
        'entity id':      # Entity ID
        'name':           # Test Group's Name.
        'run':            # Is Test Group running or not.
        'script':         # Endpoint script state.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_test_group(self, 
                       eid_list: list = None,
                       requested_col_names: list = None,
                       wait_sec: float = 0.01,
                       timeout_sec: float = 5.0,
                       errors_warnings: list = None,
                       debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/test-group"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="groups",
                                   plural_key="groups")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <TEXT> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /text/
        /text/$group
        /text/$group/$class
        /text/$group/$class/$key

    When requesting specific column names, they need to be URL encoded:
        eid, name, text, type
    Example URL: /text?fields=eid,name

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_text(eid_list=['1.234', '1.344'],
                                    requested_col_names=['text'], 
                                    debug=True)

    The record returned will have these members: 
    {
        'eid':  # -
        'name': # -
        'text': # -
        'type': # -
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_text(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/text"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="record",
                                   plural_key="records")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <VOIP> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /voip-endp/
        /voip-endp/$endp_id
        /voip-ep/
        /voip-ep/$endp_id
        /voip/
        /voip/$cx_id
        /voip_endp/
        /voip_endp/$endp_id
        /voip_ep/
        /voip_ep/$endp_id

    When requesting specific column names, they need to be URL encoded:
        bps+rx+a, bps+rx+b, delay+a+%E2%86%90+b, delay+a+%E2%86%92+b, eid, endpoints+%28a%C2%A0%E2%86%94%C2%A0b%29, 
        entity+id, jitter+a+%E2%86%90+b, jitter+a+%E2%86%92+b, name, pkt+tx+a%C2%A0%E2%86%90%C2%A0b, 
        pkt+tx+a%C2%A0%E2%86%92%C2%A0b, rpt+timer, rx+drop+%25+a, rx+drop+%25+b, state, 
        type
    Example URL: /voip?fields=bps+rx+a,bps+rx+b

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_voip(eid_list=['1.234', '1.344'],
                                    requested_col_names=['entity id'], 
                                    debug=True)

    The record returned will have these members: 
    {
        'bps rx a':                           # Endpoint B's real transmit rate (bps).Measured at the CX Type layer.
        'bps rx b':                           # Endpoint A's real transmit rate (bps).Measured at the CX Type layer.
        'delay a &#x2190; b':                 # Average Latency in milliseconds for traffic from Endpoint B to Endpoint
                                              # A
        'delay a &#x2192; b':                 # Average Latency in milliseconds for traffic from Endpoint A to Endpoint
                                              # B
        'eid':                                # Entity ID
        'endpoints (a&nbsp;&#x2194;&nbsp;b)': # Endpoints that make up this Cross Connect.
        'entity id':                          # Entity ID
        'jitter a &#x2190; b':                # Average Jitter in milliseconds for traffic from Endpoint B to Endpoint A
        'jitter a &#x2192; b':                # Average Jitter in milliseconds for traffic from Endpoint A to Endpoint B
        'name':                               # Cross Connect's Name.
        'pkt tx a&nbsp;&#x2190;&nbsp;b':      # Endpoint B's Packets Transmitted.
        'pkt tx a&nbsp;&#x2192;&nbsp;b':      # Endpoint A's Packets Transmitted.
        'rpt timer':                          # Cross Connect's Report Timer (milliseconds).This is how often the GUI
                                              # will ask for updates from the LANforge processes.If the GUI is sluggish,
                                              # increasing the report timers may help.
        'rx drop % a':                        # Endpoint A percentage packet loss.Calculated using the number of PDUs
                                              # Endpoint B sent minus the number Endpoint A received.This number is not
                                              # 100% correct as long as packets are in flight.After a Quiesce of the
                                              # test, the number should be perfectly accurate.
        'rx drop % b':                        # Endpoint B percentage packet loss.Calculated using the number of PDUs
                                              # Endpoint A sent minus the number Endpoint B received.This number is not
                                              # 100% correct as long as packets are in flight.After a Quiesce of the
                                              # test, the number should be perfectly accurate.
        'state':                              # Current State of the connection.UninitializedHas not yet been
                                              # started/stopped.InitializingBeing set up.StartingStarting the
                                              # test.RunningTest is actively running.StoppedTest has been
                                              # stopped.QuiesceTest will gracefully stop soon.HW-BYPASSTest is in
                                              # hardware-bypass mode (WanLinks only)FTM_WAITTest wants to run, but is
                                              # phantom, probably due to non-existent interface or resource.WAITINGWill
                                              # restart as soon as resources are available.PHANTOMTest is stopped, and
                                              # is phantom, probably due to non-existent interface or resource.
        'type':                               # Cross-Connect type.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_voip(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/voip"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="connection",
                                   plural_key="connections")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <VOIP-ENDP> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /voip-endp/
        /voip-endp/$endp_id

    When requesting specific column names, they need to be URL encoded:
        calls+answered, calls+attempted, calls+completed, calls+failed, cf+404, cf+408, 
        cf+busy, cf+canceled, delay, destination+addr, dropped, dup+pkts, eid, elapsed, 
        entity+id, jb+cur, jb+over, jb+silence, jb+under, jitter, mng, name, ooo+pkts, 
        pesq, pesq+bklg, pesq%23, reg+state, rst, rtp+rtt, run, rx+bytes, rx+pkts, 
        source+addr, state, tx+bytes, tx+pkts, vad+pkts
    Example URL: /voip-endp?fields=calls+answered,calls+attempted

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_voip_endp(eid_list=['1.234', '1.344'],
                                         requested_col_names=['entity id'], 
                                         debug=True)

    The record returned will have these members: 
    {
        'calls answered':   # Number of calls that where the remote answered
        'calls attempted':  # Number of calls that have been attempted
        'calls completed':  # Number of calls that have been successfully completed
        'calls failed':     # Number of calls that did not succeed for any reason.
        'cf 404':           # Number of calls failed for '404': callee not found.
        'cf 408':           # Number of calls failed for '408': callee did not answer.
        'cf busy':          # Number of calls failed because callee is busy.
        'cf canceled':      # Number of calls failed because they were canceled.
        'delay':            # Average latency in milliseconds for packets received by this endpoint.
        'destination addr': # Destination Address (MAC, ip/port, VoIP destination).
        'dropped':          # Total dropped packets, as identified by gaps in RTP sequence numbers
                            # (pre jitter buffer).
        'dup pkts':         # Total duplicate packets, as identified by RTP sequence numbers (pre
                            # jitter buffer).
        'eid':              # Entity ID
        'elapsed':          # Amount of time (seconds) this endpoint has been running (or ran.)
        'entity id':        # Entity ID
        'jb cur':           # Current number of packets in the jitter buffer waiting to be played /
                            # Jitter Buffer Size.
        'jb over':          # Total times the jitter buffer was given more packets than it could hold.
        'jb silence':       # Silence is played when there is no valid voice packet, due to drop, or
                            # reorder/jitter/latency out of range of the jitter buffer.
        'jb under':         # Total times the reader asked for a packet to play but the jitter buffer
                            # was empty.
        'jitter':           # Average interpacket variation, calculated per RFC 1889 A.8.
        'mng':              # Is the Endpoint managed or not?
        'name':             # Endpoint's Name.
        'ooo pkts':         # Total out-of-order packets, as identified by RTP sequence numbers (pre
                            # jitter buffer).
        'pesq':             # PESQ Report score for the PESQ report number (PESQ#).
        'pesq bklg':        # PESQ server call processing backlog.
        'pesq#':            # The pesq-report-number to which the PESQ value cooresponds.
        'reg state':        # Current State of the Endpoint.
        'rst':              # How many times has the endpoint been restarted due to abnormal
                            # termination.
        'rtp rtt':          # Round trip latency as reported by RTCP
        'run':              # Is the Endpoint is Running or not.
        'rx bytes':         # Total received bytes count.
        'rx pkts':          # Total received packet count.
        'source addr':      # Source Address (MAC, ip/port, VoIP source).
        'state':            # Phone registration state
        'tx bytes':         # Total transmitted bytes count.
        'tx pkts':          # Total transmitted packet count.
        'vad pkts':         # Total VAD (Silence Suppression) packets suppressed before transmit.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_voip_endp(self, 
                      eid_list: list = None,
                      requested_col_names: list = None,
                      wait_sec: float = 0.01,
                      timeout_sec: float = 5.0,
                      errors_warnings: list = None,
                      debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/voip-endp"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="endpoint",
                                   plural_key="endpoints")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <VR> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /vr-cx/
        /vr-cx/$shelf_id/$resource_id/$port_id
        /vr/
        /vr/$shelf_id/$resource_id
        /vrcx/
        /vrcx/$shelf_id/$resource_id/$port_id

    When requesting specific column names, they need to be URL encoded:
        active+ipv6+router, bgp+4byte+as, bgp+damping, bgp+peers, cluster+id, collision+domain+id, 
        confederation+id, damping+half+life, damping+max+suppress, damping+reuse, 
        damping+suppress, entity+id, height, ipv6+radv, is+bgp+reflector, local+as, 
        multicast+routing, name, netsmith-state, notes, pad, ripv2, router+connections, 
        router+id, router+id, use+confederation, use+existing+cfg, use+ospf, use+rip+dft+route, 
        using+bgp, using+olsr, width, x, xorp+sha, y
    Example URL: /vr?fields=active+ipv6+router,bgp+4byte+as

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_vr(eid_list=['1.234', '1.344'],
                                  requested_col_names=['netsmith-state'], 
                                  debug=True)

    The record returned will have these members: 
    {
        'active ipv6 router':   # -
        'bgp 4byte as':         # -
        'bgp damping':          # lc_key > lc_col_name-
        'bgp peers':            # -
        'cluster id':           # -
        'collision domain id':  # -
        'confederation id':     # -
        'damping half life':    # -
        'damping max suppress': # -
        'damping reuse':        # -
        'damping suppress':     # -
        'entity id':            # Entity ID
        'height':               # -
        'ipv6 radv':            # -
        'is bgp reflector':     # -
        'local as':             # -
        'multicast routing':    # -
        'name':                 # Name
        'netsmith-state':       # -
        'notes':                # -
        'pad':                  # -
        'ripv2':                # -
        'router connections':   # -
        'router id':            # -
        'router id':            # -
        'use confederation ':   # -
        'use existing cfg':     # -
        'use ospf':             # -
        'use rip dft route':    # -
        'using bgp':            # -
        'using olsr':           # -
        'width':                # -
        'x':                    # -
        'xorp sha':             # -
        'y':                    # -
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_vr(self, 
               eid_list: list = None,
               requested_col_names: list = None,
               wait_sec: float = 0.01,
               timeout_sec: float = 5.0,
               errors_warnings: list = None,
               debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/vr"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="virtual-routers",
                                   plural_key="virtual-routers")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <VRCX> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /vrcx/
        /vrcx/$shelf_id/$resource_id/$port_id

    When requesting specific column names, they need to be URL encoded:
        entity+id, height, interface+cost, local-a, local-b, netsmith-state, remote-a, 
        remote-b, resource, rip+metric, vrrp+id, vrrp+interval, vrrp+ip, vrrp+ip-prefix, 
        vrrp+priority, wan+link, width, x, y
    Example URL: /vrcx?fields=entity+id,height

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_vrcx(eid_list=['1.234', '1.344'],
                                    requested_col_names=['netsmith-state'], 
                                    debug=True)

    The record returned will have these members: 
    {
        'entity id':      # -
        'height':         # -
        'interface cost': # -
        'local-a':        # -
        'local-b':        # -
        'netsmith-state': # -
        'remote-a':       # -
        'remote-b':       # -
        'resource':       # -
        'rip metric':     # -
        'vrrp id':        # -
        'vrrp interval':  # -
        'vrrp ip':        # -
        'vrrp ip-prefix': # -
        'vrrp priority':  # -
        'wan link':       # -
        'width':          # -
        'x':              # -
        'y':              # -
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_vrcx(self, 
                 eid_list: list = None,
                 requested_col_names: list = None,
                 wait_sec: float = 0.01,
                 timeout_sec: float = 5.0,
                 errors_warnings: list = None,
                 debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/vrcx"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="router-connections",
                                   plural_key="router-connections")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <WL> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /wl-endp/
        /wl-endp/$wl_ep_id
        /wl-ep/
        /wl-ep/$wl_ep_id
        /wl/
        /wl/$wl_id
        /wl_endp/
        /wl_endp/$wl_ep_id
        /wl_ep/
        /wl_ep/$wl_ep_id
        /wlendp/$wl_ep_id

    When requesting specific column names, they need to be URL encoded:
        bps+rx+a, bps+rx+b, eid, endpoints+%28a%C2%A0%E2%86%94%C2%A0b%29, entity+id, k-m, 
        name, pkt+tx+a%C2%A0%E2%86%90%C2%A0b, pkt+tx+a%C2%A0%E2%86%92%C2%A0b, rpt+timer, 
        state
    Example URL: /wl?fields=bps+rx+a,bps+rx+b

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_wl(eid_list=['1.234', '1.344'],
                                  requested_col_names=['entity id'], 
                                  debug=True)

    The record returned will have these members: 
    {
        'bps rx a':                           # Endpoint B's Max transmit rate (bps).
        'bps rx b':                           # Endpoint A's Max transmit rate (bps).
        'eid':                                # Entity ID
        'endpoints (a&nbsp;&#x2194;&nbsp;b)': # Endpoints that make up this WanLink.
        'entity id':                          # Entity ID
        'k-m':                                # Whether the WanLink is Kernel-Mode or not.
        'name':                               # WanLink's Name.
        'pkt tx a&nbsp;&#x2190;&nbsp;b':      # Packets received on endpoint B and transmitted out endpoint A.
        'pkt tx a&nbsp;&#x2192;&nbsp;b':      # Packets received on endpoint A and transmitted out endpoint B.
        'rpt timer':                          # Cross Connect's Report Timer (milliseconds).This is how often the GUI
                                              # will ask for updates from the LANforge processes.If the GUI is sluggish,
                                              # increasing the report timers may help.
        'state':                              # Current State of the connection.UninitializedHas not yet been
                                              # started/stopped.InitializingBeing set up.StartingStarting the
                                              # test.RunningTest is actively running.StoppedTest has been
                                              # stopped.QuiesceTest will gracefully stop soon.HW-BYPASSTest is in
                                              # hardware-bypass mode (WanLinks only)FTM_WAITTest wants to run, but is
                                              # phantom, probably due to non-existent interface or resource.WAITINGWill
                                              # restart as soon as resources are available.PHANTOMTest is stopped, and
                                              # is phantom, probably due to non-existent interface or resource.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_wl(self, 
               eid_list: list = None,
               requested_col_names: list = None,
               wait_sec: float = 0.01,
               timeout_sec: float = 5.0,
               errors_warnings: list = None,
               debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/wl"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <WL-ENDP> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /wl-endp/
        /wl-endp/$wl_ep_id

    When requesting specific column names, they need to be URL encoded:
        buffer, corrupt+1, corrupt+2, corrupt+3, corrupt+4, corrupt+5, corrupt+6, 
        delay, dropfreq+%25, dropped, dup+pkts, dupfreq+%25, eid, elapsed, extrabuf, 
        failed-late, jitfreq+%25, max+rate, maxjitter, maxlate, name, ooo+pkts, qdisc, 
        reordfrq+%25, run, rx+bytes, rx+pkts, script, serdelay, tx+bytes, tx+drop+%25, 
        tx+pkts, tx+rate, tx-failed, wps
    Example URL: /wl-endp?fields=buffer,corrupt+1

    Example py-json call (it knows the URL):
        record = LFJsonGet.get_wl_endp(eid_list=['1.234', '1.344'],
                                       requested_col_names=['eid'], 
                                       debug=True)

    The record returned will have these members: 
    {
        'buffer':      # Maximum size of receive buffer, in bytes.This is the sum of the amount
                       # needed for the transit buffers (delay * bandwidth)plus the WanLink
                       # "Backlog Buffer:" queue size which handles bursts.
        'corrupt 1':   # Counters for how many times this corruption has been applied.
        'corrupt 2':   # Counters for how many times this corruption has been applied.
        'corrupt 3':   # Counters for how many times this corruption has been applied.
        'corrupt 4':   # Counters for how many times this corruption has been applied.
        'corrupt 5':   # Counters for how many times this corruption has been applied.
        'corrupt 6':   # Counters for how many times this corruption has been applied.
        'delay':       # Base induced latency on received packets, in microseconds.
        'dropfreq %':  # Frequency out of 1,000,000 to drop a received packet.Select a preset
                       # value or enter your own.
        'dropped':     # Total dropped packets on receive.This does not include the tx-failed
                       # counters.
        'dup pkts':    # Total duplicate packets generated.
        'dupfreq %':   # Frequency out of 1,000,000 to duplicate a received packet.Select a
                       # preset value or enter your own.
        'eid':         # Entity ID
        'elapsed':     # Amount of time (seconds) this endpoint has been running (or ran.)
        'extrabuf':    # Size of "Backlog Buffer:" setting in WanLink configuration in bytes.
        'failed-late': # Total amount of received packets that could not be transmitted out the
                       # peer becausethe emulator was overloaded and could not transmit within
                       # the specified 'lateness'
        'jitfreq %':   # Frequency out of 1,000,000 that packets should have jitter applied to
                       # them.Select a preset value or enter your own.
        'max rate':    # Max transmit rate (bps) for this Endpoint.
        'maxjitter':   # Maximum additional delay, in microseconds.  See Jitter-Frequency as
                       # well.
        'maxlate':     # The maximum lateness in milliseconds allowed before packets will be
                       # dropped on transmit.If lateness is configured to be automatic, this
                       # variable will change based onconfigured bandwidth and backlog buffer,
                       # but will not go below 10ms.
        'name':        # Endpoint's Name.
        'ooo pkts':    # Total out of order packets generated.
        'qdisc':       # Queueing discipline (FIFO, WRR, etc).
        'reordfrq %':  # Frequency out of 1,000,000 to re-order a received packet.Select a preset
                       # value or enter your own.
        'run':         # Is the Endpoint is Running or not.
        'rx bytes':    # Total received bytes count.
        'rx pkts':     # Total received packet count.
        'script':      # Endpoint script state.
        'serdelay':    # Additional serialization delay for a 1514 byte packet at the configured
                       # speed (microseconds).
        'tx bytes':    # Total transmitted bytes count.
        'tx drop %':   # Packet drop percentage over the last 1 minute.
        'tx pkts':     # Packets received on the peer interface and transmitted out this
                       # endpoint's interface.
        'tx rate':     # The average speed over the last 30 seconds at which we are
                       # transmittingout the peer interface.This can be thought of as the actual
                       # transfer rate for packets entering the interfaceassociated with this
                       # Endpoint.
        'tx-failed':   # Total amount of received packets that could not be transmitted out the
                       # peer.This includes any tx-failed-late packets.
        'wps':         # Enable/Disable showing of WanPaths for individual endpoints.
    }
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_wl_endp(self, 
                    eid_list: list = None,
                    requested_col_names: list = None,
                    wait_sec: float = 0.01,
                    timeout_sec: float = 5.0,
                    errors_warnings: list = None,
                    debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/wl-endp"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="endpoint",
                                   plural_key="endpoint")
    #
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
            Notes for <WS-MSG> type requests

    If you need to call the URL directly,
    request one of these URLs:
        /ws-msg/
        /ws-msg/$sessionid

    
    Example py-json call (it knows the URL):
        record = LFJsonGet.get_ws_msg(eid_list=['1.234', '1.344'],
                                      debug=True)
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""

    def get_ws_msg(self, 
                   eid_list: list = None,
                   requested_col_names: list = None,
                   wait_sec: float = 0.01,
                   timeout_sec: float = 5.0,
                   errors_warnings: list = None,
                   debug: bool = False):
        """
        :param eid_list: list of entity IDs to query for
        :param requested_col_names: list of column names to return
        :param wait_sec: duration to wait between retries if no response or response is HTTP 404
        :param timeout_sec: duration in which to keep querying before returning
        :param errors_warnings: optional list to extend with errors and warnings from response
        :param debug: print diagnostic info if true
        :return: dictionary of results
        """
        debug |= self.debug_on
        url = "/ws-msg"
        if (eid_list is None) or (len(eid_list) < 1):
            raise ValueError("no entity id in request")
        trimmed_fields = []
        if isinstance(requested_col_names, str):
            if not requested_col_names.strip():
                raise ValueError("column name cannot be blank")
            trimmed_fields.append(requested_col_names.strip())
        if isinstance(requested_col_names, list):
            for field in requested_col_names:
                if not field.strip():
                    raise ValueError("column names cannot be blank")
                field = field.strip()
                if field.find(" ") > -1:
                    raise ValueError("field should be URL encoded: [%s]" % field)
                trimmed_fields.append(field)
        url += self.create_port_eid_url(eid_list=eid_list)

        if len(trimmed_fields) > 0:
            url += "?fields=%s" % (",".join(trimmed_fields))

        response = self.json_get(url=url,
                                 debug=debug,
                                 wait_sec=wait_sec,
                                 request_timeout_sec=timeout_sec,
                                 max_timeout_sec=timeout_sec,
                                 errors_warnings=errors_warnings)
        if response is None:
            return None
        return self.extract_values(response=response,
                                   singular_key="",
                                   plural_key="")
    #


class LFSession(BaseSession):
    """----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        This subclass of BaseSession knows about LFJsonQuery and LFJsonCommand
    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"""
    def __init__(self, lfclient_url: str = 'http://localhost:8080',
                 debug: bool = False,
                 proxy_map: dict = None,
                 connection_timeout_sec: float = None,
                 stream_errors: bool = True,
                 stream_warnings: bool = False,
                 require_session: bool = False,
                 exit_on_error: bool = False):
        """
        :param debug: turn on diagnostic information
        :param proxy_map: a dict with addresses of proxies to route requests through.
        E.G.: { 'http':'http://192.168.1.253:3128', 'https':'https://192.168.1.253:443' }
        :param connection_timeout_sec: timeout in second to wait for a connect to the LANforge client (GUI)
        This timeout does should not apply to long running client requests, there are individual
        timeouts for those conditions, such as max_timeout_sec.
        :param stream_errors: print HTTP JSON API errors to system out and logging stream
        :param stream_warnings: print HTTP JSON API warnings to system out and logging stream
        :param require_session: exit(1) if unable to establish a session_id
        :param exit_on_error: on requests failing HTTP requests on besides error 404,
        exit(1). This does not include failing to establish a session_id
        """
        super().__init__(lfclient_url=lfclient_url,
                         debug=debug,
                         proxy_map=proxy_map,
                         connection_timeout_sec=connection_timeout_sec,
                         stream_errors=stream_errors,
                         stream_warnings=stream_warnings,
                         exit_on_error=exit_on_error)
        self.command_instance = LFJsonCommand(session_obj=self, debug=debug, exit_on_error=exit_on_error)
        self.query_instance = LFJsonQuery(session_obj=self, debug=debug, exit_on_error=exit_on_error)
        self.session_connection_check = \
            self.command_instance.start_session(debug=debug,
                                                die_without_session_id_=require_session)
        if self.session_connection_check:
            self.session_id = self.command_instance.session_id
            self.query_instance.session_id = self.session_id
        else:
            self.logger.error('LFSession failed to establish session_id') 
        if require_session and ((not self.command_instance.session_id) or (not self.session_id)):
            self.logger.error('LFSession failed to setup session_id correctly') 

    def get_command(self) -> LFJsonCommand:
        """
            Remember to override this method with your session subclass, it should return LFJsonCommand
            :return: registered instance of JsonCommand
        """
        if self.command_instance:
            return self.command_instance
        self.command_instance = LFJsonCommand(session_obj=self)
        return self.command_instance

    def get_query(self) -> LFJsonQuery:
        """
            Remember to override this method with your session subclass, it should return LFJsonQuery
            :return: registered instance of JsonQuery
        """
        if self.query_instance:
            return self.query_instance
        self.query_instance = LFJsonQuery(session_obj=self, debug=self.debug_on)
        return self.query_instance
