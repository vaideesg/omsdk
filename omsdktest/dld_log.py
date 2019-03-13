from omsdk.http.sdkhttpep import *
from omsdk.sdkcreds import UserCredentials
import requests
import zipfile, io
import gzip
import shutil
import re, os, glob

class T(HttpEndPoint):
    def __init__(self, ipaddr, creds, pOptions, headers = {}):
        super().__init__(ipaddr, creds, pOptions, headers)
        self.endpoint = self.endpoint[0:self.endpoint.rindex('/')]
        self.XSRF_TOKEN = None

    def _dologin_and_collect_cookies(self, uri, data, headers):
        self._logger.debug("Begin doing HTTP POST with SOAP message")

        if self.session:
            try:
                request = requests.Request('POST', self.endpoint + uri,
                    data=data, headers=headers)
                prepared_request = self.session.prepare_request(request)
            except requests.exceptions.RequestException:
                error_message = "Error preparing HTTP request"
                #self._logger.exception(error_message)
                raise HttpEndPointProtocolException(error_message)
            else:
                self._logger.debug("Finished preparing POST request")

            # Submit the http request
            self._logger.debug("Begin submitting POST request")
            try:
                reply = self.session.send(prepared_request,
                                verify=self.pOptions.verify_ssl,
                                timeout=(self.pOptions.connection_timeout,
                                        self.pOptions.read_timeout))
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout):
                error_message = "HTTP connection error"
                #self._logger.exception(error_message)
                raise HttpEndPointProtocolException(error_message)
            except requests.exceptions.RequestException:
                error_message = "Error preparing HTTP request"
                self._logger.exception(error_message)
                raise HttpEndPointTransportException(error_message)
            else:
                self._logger.debug("Finished submitting POST request")

            # now check reply for errors
            self._logger.debug("Begin checking POST reply")
            try:
                reply.raise_for_status()
            except requests.exceptions.HTTPError:
                error_message = (
                    "DRAC WSMAN endpoint returned HTTP code '{}' Reason '{}'"
                    ).format(reply.status_code, reply.reason)
                # reply.content
                #self._logger.exception(error_message)
                if reply.status_code == 401:
                    raise HttpEndPointProtocolAuthException(error_message)
                else:
                    raise HttpEndPointProtocolException(error_message)
            else:
                self._logger.debug("Received non-error HTTP reply")
            finally:
                self._logger.debug("Finished checking POST reply")

            # make sure its a string
            self.cookies = reply.cookies
            if 'XSRF-TOKEN' in reply.headers:
                self.XSRF_TOKEN = reply.headers['XSRF-TOKEN']
            self._logger.debug("Received reply:\n%s", reply)

        # return it
        return reply

    def _download_file(self, todir, uri, headers = {}):

        self._logger.debug("Begin doing HTTP POST with SOAP message")
        response = None
        tofile = None

        if self.session:
            try:
                request = requests.Request('GET', self.endpoint + uri,
                    cookies=self.cookies, headers=headers)

                prepared_request = self.session.prepare_request(request)
            except requests.exceptions.RequestException:
                error_message = "Error preparing HTTP request"
                #self._logger.exception(error_message)
                raise HttpEndPointProtocolException(error_message)
            else:
                self._logger.debug("Finished preparing POST request")

            # Submit the http request
            self._logger.debug("Begin submitting POST request")
            try:
                response = self.session.send(prepared_request,
                                verify=self.pOptions.verify_ssl,
                                timeout=(self.pOptions.connection_timeout,
                                        self.pOptions.read_timeout),
                                stream=True)
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout):
                error_message = "HTTP connection error"
                #self._logger.exception(error_message)
                raise HttpEndPointProtocolException(error_message)
            except requests.exceptions.RequestException:
                error_message = "Error preparing HTTP request"
                self._logger.exception(error_message)
                raise HttpEndPointTransportException(error_message)
            else:
                self._logger.debug("Finished submitting POST request")

            # now check response for errors
            self._logger.debug("Begin checking POST response")
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                error_message = (
                    "DRAC WSMAN endpoint returned HTTP code '{}' Reason '{}'"
                    ).format(response.status_code, response.reason)
                # response.content
                #self._logger.exception(error_message)
                if response.status_code == 401:
                    raise HttpEndPointProtocolAuthException(error_message)
                else:
                    raise HttpEndPointProtocolException(error_message)
            else:
                self._logger.debug("Received non-error HTTP response")
            finally:
                self._logger.debug("Finished checking POST response")

            tofile = "download_file"
            print(response.headers)
            if 'Content-Disposition' in response.headers:
                for pattern in ['filename="(.+)"', 'filename=(.+)']:
                    objs = re.findall(pattern,
                             response.headers['Content-Disposition'])
                    if len(objs):
                        tofile = objs[0]
                        break

            # make sure its a string
            with open(os.path.join(todir, tofile), 'wb') as handle:
                for chunk in response.iter_content():
                    if chunk:  # filter out keep-alive new chunks
                        handle.write(chunk)
                        handle.flush()
            self._logger.debug("Received SOAP reply:\n%s", response)

        # return it
        return response, tofile

    def download_logs(self, todir):
        self.connect()
        for (login_url, log_url, data_fmt, header_creds) in [
            ('/data/login', '/lcldata?set=lclExport()',
                    'user={0}&password={1}', False),
            ('/data/login', '/csvdata?get=eventLogEntriesCSV()',
                    'user={0}&password={1}', False),
            ('/data/login', '/csvdata?get=racLogEntriesCSV()',
                    'user={0}&password={1}', False),
            ('/sysmgmt/2015/bmc/session',
                 '/sysmgmt/2013/server/lclogs?format=gzip', '', True)
            ]:
            try :
                print('Trying ' + login_url)
                data=data_fmt.format(self.creds.username, self.creds.password)
                headers = {}
                if self.XSRF_TOKEN:
                    headers["XSRF-TOKEN"] = self.XSRF_TOKEN
                if header_creds:
                    headers["user"] = self.creds.username
                    headers["password"] = self.creds.password
                response = self._dologin_and_collect_cookies(login_url,
                                data,headers)
                print(response.text)
                print(response.headers)
                headers = {}
                if self.XSRF_TOKEN:
                    headers["XSRF-TOKEN"] = self.XSRF_TOKEN
                response, tofile = self._download_file(todir, log_url, headers)
                print(response.headers)
                print("Completed writing to " + tofile)
                return True
            except HttpEndPointProtocolAuthException:
                pass
            except HttpEndPointProtocolException:
                pass

        with open('_unable_to_download.txt', 'a') as f:
            f.write(todir)
            f.flush()
        print("Unable to write to " + todir)
        return False

hostlist = []
with open('../omdata/Store/list2.txt', 'r') as f:
    hostlist=[i.strip() for i in f.readlines()]

#with open('_unable_to_download.txt', 'r') as f:
#    hostlist=[i.strip() for i in f.readlines()]

for hostname in hostlist:
    todir = os.path.join('s', hostname)
    if not os.path.exists(todir):
        os.makedirs(todir)
    op = HttpEndPointOptions()
    skip = False
    for logname in ['*.xml.gz', 'log.csv', 'log.xml']:
        if len(glob.glob(os.path.join(todir, logname))):
            skip = True
            break
    if skip:
        print('skipping...' + todir)
        continue
    print("todir=" + todir)
    try:
        a = T(hostname,creds=UserCredentials('root','calvin'), pOptions=op)
        a.download_logs(todir)
    except:
        with open('_unable_to_download.txt', 'a') as f:
            f.write(todir)
            f.flush()
        print("Unable to write to " + todir)

#with gzip.open(filezip, 'rb') as f_in:
#    with open(filezip[0:filezip.rindex('.')], 'wb') as f_out:
#        shutil.copyfileobj(f_in, f_out)

