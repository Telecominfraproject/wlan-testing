#!/usr/bin/env python3

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Class holds default settings for json requests                -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import logging
import sys
import os
from pprint import pformat, PrettyPrinter
import urllib
from urllib import request
import json
import http.client
http.client._MAXHEADERS = 300


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../../")))

debug_printer = PrettyPrinter(indent=2)


class LFRequest:
    Default_Base_URL = "http://localhost:8080"
    No_Data = {'No Data': 0}
    requested_url = ""
    post_data = No_Data
    default_headers = {'Accept': 'application/json'}
    proxies = None
    logger = logging.getLogger(__name__)

    def __init__(self, url=None,
                 uri=None,
                 proxies_=None,
                 debug_=False,
                 die_on_error_=False):
        self.debug = debug_
        self.die_on_error = die_on_error_
        self.error_list = []

        # please see this discussion on ProxyHandlers:
        # https://docs.python.org/3/library/urllib.request.html#urllib.request.ProxyHandler
        # but this makes much more sense:
        # https://gist.github.com/aleiphoenix/4159510

        # if debug_:
        #     if proxies_ is None:
        #         print("LFRequest_init_: no proxies_")
        #     else:
        #         print("LFRequest: proxies_: ")
        #         pprint.pprint(proxies_)

        if (proxies_ is not None) and (len(proxies_) > 0):
            if ("http" not in proxies_) and ("https" not in proxies_):
                raise ValueError("Neither http or https set in proxy definitions. Expects proxy={'http':, 'https':, }")
            self.proxies = proxies_

        # if debug_:
        #     if self.proxies is None:
        #         print("LFRequest_init_: no proxies")
        #     else:
        #         print("LFRequest: proxies: ")
        #         pprint.pprint(self.proxies)

        if url and uri and (url.startswith("http:/") or url.startswith("https:/"))\
                and (uri.startswith("http:/") or uri.startswith("https:/")):
            raise ValueError("URL and PATH are both URLs: url[%s] uri[%s]" % (url, uri))
        if url and uri and uri.startswith("http:/"):
            raise ValueError("URL is present and PATH is an URL: url[%s] uri[%s]" % (url, uri))
        if not url.startswith("http://") and not url.startswith("https://"):
            self.logger.warning("No http:// or https:// found, prepending http:// to " + url)
            url = "http://" + url
        if uri is not None:
            if not url.endswith('/') and not uri.startswith('/'):
                url += '/'
            if (uri.find("http:")>=0) or (uri.find("https:")>=0):
                self.logger.warning("PATH contains an protocol that is not URL encoded: [%s]" % uri)
            self.requested_url = url + uri
        else:
            self.requested_url = url

        if self.requested_url is None:
            raise Exception("Bad LFRequest of url[%s] uri[%s] -> None" % (url, uri))

        if self.requested_url.find('//'):
            protopos = self.requested_url.find("://")
            self.requested_url = self.requested_url[:protopos + 2] + self.requested_url[protopos + 2:].replace("//",
                                                                                                               "/")

        # finding '#' prolly indicates a macvlan (eth1#0)
        # finding ' ' prolly indicates a field name that should imply %20
        if self.requested_url.find('#') >= 1:
            self.requested_url = self.requested_url.replace('#', '%23')
        if self.requested_url.find(' ') >= 1:
            self.requested_url = self.requested_url.replace(' ', '+')
        self.logger.debug("new LFRequest[%s]" % self.requested_url)

    # request first url on stack
    def formPost(self, show_error=True, debug=False, die_on_error_=False):
        return self.form_post(show_error=show_error, debug=debug, die_on_error_=die_on_error_)

    def form_post(self, show_error=True, debug=False, die_on_error_=False):
        if self.die_on_error:
            die_on_error_ = True
        if debug or self.debug:
            debug = True
        responses = []
        urlenc_data = ""
        # https://stackoverflow.com/a/59635684/11014343
        if (self.proxies is not None) and (len(self.proxies) > 0):
            # https://stackoverflow.com/a/59635684/11014343
            opener = request.build_opener(request.ProxyHandler(self.proxies))
            request.install_opener(opener)

        self.logger.debug("formPost: url: " + self.requested_url)
        if (self.post_data is not None) and (self.post_data is not self.No_Data):
            urlenc_data = urllib.parse.urlencode(self.post_data).encode("utf-8")
            self.logger.debug("formPost: data looks like:" + str(urlenc_data))
            self.logger.debug("formPost: url: " + self.requested_url)
            myrequest = request.Request(url=self.requested_url,
                                        data=urlenc_data,
                                        headers=self.default_headers)
        else:
            myrequest = request.Request(url=self.requested_url, headers=self.default_headers)
            self.logger.error("No data for this formPost?")

        myrequest.headers['Content-type'] = 'application/x-www-form-urlencoded'

        resp = ''
        try:
            resp = urllib.request.urlopen(myrequest)
            responses.append(resp)
            return responses[0]

        except urllib.error.HTTPError as error:
            print_diagnostics(url_=self.requested_url,
                              request_=myrequest,
                              responses_=responses,
                              error_=error,
                              error_list_=self.error_list,
                              debug_=debug)

        except urllib.error.URLError as uerror:
            print_diagnostics(url_=self.requested_url,
                              request_=myrequest,
                              responses_=responses,
                              error_=uerror,
                              error_list_=self.error_list,
                              debug_=debug)

        if die_on_error_ or self.die_on_error:
            exit(1)
        return None

    def jsonPost(self, show_error=True, debug=False, die_on_error_=False, response_json_list_=None):
        return self.json_post(show_error=show_error, debug=debug, die_on_error_=die_on_error_,
                              response_json_list_=response_json_list_)

    def json_post(self, show_error=True, debug=False, die_on_error_=False, response_json_list_=None, method_='POST'):
        if debug or self.debug:
            debug = True
        if self.die_on_error:
            die_on_error_ = True
        responses = []
        if (self.proxies is not None) and (len(self.proxies) > 0):
            opener = urllib.request.build_opener(request.ProxyHandler(self.proxies))
            urllib.request.install_opener(opener)

        if (self.post_data is not None) and (self.post_data is not self.No_Data):
            myrequest = request.Request(url=self.requested_url,
                                        method=method_,
                                        data=json.dumps(self.post_data).encode("utf-8"),
                                        headers=self.default_headers)
        else:
            myrequest = request.Request(url=self.requested_url, headers=self.default_headers)
            self.logger.error("No data for this jsonPost?")

        myrequest.headers['Content-type'] = 'application/json'

        # https://stackoverflow.com/a/59635684/11014343

        try:
            resp = urllib.request.urlopen(myrequest)
            resp_data = resp.read().decode('utf-8')
            if debug or die_on_error_:
                self.logger.debug("----- LFRequest::json_post:128 debug: --------------------------------------------")
                self.logger.debug("URL: <%s>  status: %d " % (self.requested_url, resp.status))
                if resp.status != 200:
                    self.logger.debug(pformat(resp.getheaders()))
                self.logger.debug("----- resp_data:128 -------------------------------------------------")
                self.logger.debug(resp_data)
                self.logger.debug("-------------------------------------------------")
            responses.append(resp)
            if response_json_list_ is not None:
                if type(response_json_list_) is not list:
                    raise ValueError("reponse_json_list_ needs to be type list")
                j = json.loads(resp_data)
                if debug:
                    self.logger.debug(
                        "----- LFRequest::json_post:140 debug: --------------------------------------------")
                    self.logger.debug(pformat(j))
                    self.logger.debug("-------------------------------------------------")
                response_json_list_.append(j)
            return responses[0]

        except urllib.error.HTTPError as error:
            print_diagnostics(url_=self.requested_url,
                              request_=myrequest,
                              responses_=responses,
                              error_=error,
                              debug_=debug)

        except urllib.error.URLError as uerror:
            print_diagnostics(url_=self.requested_url,
                              request_=myrequest,
                              responses_=responses,
                              error_=uerror,
                              debug_=debug)

        if die_on_error_:
            exit(1)
        return None

    def json_put(self, show_error=True, debug=False, die_on_error_=False, response_json_list_=None):
        return self.json_post(show_error=show_error,
                              debug=debug,
                              die_on_error_=die_on_error_,
                              response_json_list_=response_json_list_,
                              method_='PUT')

    def json_delete(self, show_error=True, debug=False, die_on_error_=False, response_json_list_=None):
        return self.get_as_json(method_='DELETE')

    def get(self, method_='GET'):
        if self.debug:
            self.logger.debug("LFUtils.get: url: " + self.requested_url)

        # https://stackoverflow.com/a/59635684/11014343
        if (self.proxies is not None) and (len(self.proxies) > 0):
            opener = request.build_opener(request.ProxyHandler(self.proxies))
            # opener = urllib.request.build_opener(myrequest.ProxyHandler(self.proxies))
            request.install_opener(opener)

        myrequest = request.Request(url=self.requested_url,
                                    headers=self.default_headers,
                                    method=method_)
        myresponses = []
        try:
            myresponses.append(request.urlopen(myrequest))
            return myresponses[0]

        except urllib.error.HTTPError as error:
            print_diagnostics(url_=self.requested_url,
                              request_=myrequest,
                              responses_=myresponses,
                              error_=error,
                              error_list_=self.error_list,
                              debug_=self.debug)

        except urllib.error.URLError as uerror:
            print_diagnostics(url_=self.requested_url,
                              request_=myrequest,
                              responses_=myresponses,
                              error_=uerror,
                              error_list_=self.error_list,
                              debug_=self.debug)

        if self.die_on_error:
            exit(1)
        return None

    def getAsJson(self):
        return self.get_as_json()

    def get_as_json(self, method_='GET'):
        responses = list()
        responses.append(self.get(method_=method_))
        if len(responses) < 1:
            if self.debug and self.has_errors():
                self.print_errors()
            return None
        if responses[0] is None:
            self.logger.debug("No response from " + self.requested_url)
            return None
        json_data = json.loads(responses[0].read().decode('utf-8'))
        return json_data

    def addPostData(self, data):
        self.add_post_data(data=data)

    def add_post_data(self, data):
        """
        TODO: this is a setter and should be named 'set_post_data'
        :param data: dictionary of parameters for post
        :return: nothing
        """
        self.post_data = data

    def has_errors(self):
        return (True, False)[len(self.error_list) > 0]

    def print_errors(self):
        if not self.has_errors:
            self.logger.debug("---------- no errors ----------")
            return
        for err in self.error_list:
            self.logger.error("error: %s" % err)


def plain_get(url_=None, debug_=False, die_on_error_=False, proxies_=None):
    """
    This static method does not respect LFRequest.proxy, it is not set in scope here
    :param url_:
    :param debug_:
    :param die_on_error_:
    :return:
    """
    myrequest = request.Request(url=url_)
    myresponses = []
    try:
        if (proxies_ is not None) and (len(proxies_) > 0):
            # https://stackoverflow.com/a/59635684/11014343
            opener = myrequest.build_opener(myrequest.ProxyHandler(proxies_))
            myrequest.install_opener(opener)

        myresponses.append(request.urlopen(myrequest))
        return myresponses[0]

    except urllib.error.HTTPError as error:
        print_diagnostics(url_=url_,
                          request_=request,
                          responses_=myresponses,
                          error_=error,
                          debug_=debug_)

    except urllib.error.URLError as uerror:
        print_diagnostics(url_=url_,
                          request_=request,
                          responses_=myresponses,
                          error_=uerror,
                          debug_=debug_)

    if die_on_error_:
        exit(1)
    return None


def print_diagnostics(url_=None, request_=None, responses_=None, error_=None, error_list_=None, debug_=False):
    logger = logging.getLogger(__name__)
    # logger.error("LFRequest::print_diagnostics: error_.__class__: %s"%error_.__class__)
    # logger.error(pformat(error_))
    warnings_list = []
    errors_list = []
    if url_ is None:
        warnings_list.append("WARNING LFRequest::print_diagnostics: url_ is None")
    if request_ is None:
        warnings_list.append("WARNING LFRequest::print_diagnostics: request_ is None")
    if error_ is None:
        warnings_list.append("WARNING LFRequest::print_diagnostics: error_ is None")

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
            errors_list.append("\n = = LANforge Error Messages = =")
            errors_list.append(" = = URL: %s" % err_full_url)
            for xerr in xerrors:
                errors_list.append("  "+xerr)
                if (error_list_ is not None) and isinstance(error_list_, list):
                    error_list_.append(xerr)
            errors_list.append(" = = = = = = = = = = = = = = = =")
            logger.error("\n".join(errors_list))

    if error_.__class__ is urllib.error.HTTPError:
        debug_list = []
        debug_list.append("\n----- LFRequest: HTTPError: --------------------------------------------")
        debug_list.append("%s <%s> HTTP %s: %s" % (method, err_full_url, err_code, err_reason))

        if err_code == 404:
            if (error_list_ is not None) and isinstance(error_list_, list):
                error_list_.append("[%s HTTP %s] <%s> : %s" % (method, err_code, err_full_url, err_reason))
        else:
            debug_list.append(
                "  Content-type:[%s] Accept[%s]" % (request_.get_header('Content-type'), request_.get_header('Accept')))

            if hasattr(request_, "data") and (request_.data is not None):
                debug_list.append("  Data:")
                debug_list.append(debug_printer.pformat(request_.data))
            elif debug_:
                debug_list.append("    <no request data>")

        if len(err_headers) > 0:
            # the HTTPError is of type HTTPMessage a subclass of email.message
            debug_list.append("  Response Headers: ")
            for headername in sorted(err_headers.keys()):
                debug_list.append("    %s: %s" % (headername, err_headers.get(headername)))

        if len(responses_) > 0:
            debug_list.append("----- Response: --------------------------------------------------------")
            debug_list.append(debug_printer.pformat(responses_[0].reason))

        debug_list.append("------------------------------------------------------------------------")
        logger.debug("\n".join(debug_list))
        return

    if error_.__class__ is urllib.error.URLError:
        errors_list.append("\n----- LFRequest: URLError: ---------------------------------------------")
        errors_list.append("%s <%s> HTTP %s: %s" % (method, err_full_url, err_code, err_reason))
        errors_list.append("------------------------------------------------------------------------")
        logger.error("\n".join(errors_list))
# ~LFRequest
