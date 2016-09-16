#!/usr/bin/python

#Included the original creators name, but removed the License
#Will put in the license later
####
# 02/2006 Will Holcomb <wholcomb@gmail.com>
#
"""
Usage:
  Enables the use of multipart/form-data for posting forms

Inspirations:
  Upload files in python:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
  urllib2_file:
    Fabien Seisen: <fabien@seisen.org>

Example:
  import MultipartPostHandler, urllib.request, cookielib

  cookies = cookielib.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies),
                                MultipartPostHandler.MultipartPostHandler)
  params = { "username" : "bob", "password" : "riviera",
             "file" : open("filename", "rb") }
  opener.open("http://wwww.bobsite.com/upload/", params)

Further Example:
  The main function of this file is a sample which downloads a page and
  then uploads it to the W3C validator.
"""

import urllib
import urllib.request
import mimetypes
import os, stat

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

class MultipartPostHandler(urllib.request.BaseHandler):
    handler_order = urllib.request.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                print (TypeError, "not a valid non-string sequence or mapping object", file = traceback)
                raise TypeError("not a valid non-string sequence or mapping object")

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print ("Replacing {} with {}".format(request.get_header('content-type'), 'multipart/form-data'))
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request


    def choose_boundary(self):
        """Return a string usable as a multipart boundary.
        The string chosen is unique within a single program run, and
        incorporates the user id (if available), process id (if available),
        and current time.  So it's very unlikely the returned string appears
        in message text, but there's no guarantee.
        The boundary contains dots so you have to quote it in the header."""
        _prefix = None
        import time
        if _prefix is None:
            import socket
            try:
                hostid = socket.gethostbyname(socket.gethostname())
            except socket.gaierror:
                hostid = '127.0.0.1'
            try:
                uid = repr(os.getuid())
            except AttributeError:
                uid = '1'
            try:
                pid = repr(os.getpid())
            except AttributeError:
                pid = '1'
            _prefix = hostid + '.' + uid + '.' + pid
        return "%s.%.3f.%d" % (_prefix, time.time(), _get_next_counter())


    def multipart_encode(vars, files, boundary = None, buffer = None):
        if boundary is None:
            boundary = self.choose_boundary()
        if buffer is None:
            buffer = ''
        for(key, value) in vars:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + value + '\r\n'
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buffer += '\r\n' + fd.read() + '\r\n'
        buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer
    multipart_encode = Callable(multipart_encode)

    https_request = http_request

def main():
    import tempfile, sys

    validatorURL = "http://validator.w3.org/check"
    opener = urllib.request.build_opener(MultipartPostHandler)

    def validateFile(url):
        temp = tempfile.mkstemp(suffix=".html")
        os.write(temp[0], opener.open(url).read())
        params = { "ss" : "0",            # show source
                   "doctype" : "Inline",
                   "uploaded_file" : open(temp[1], "rb") }
        print (opener.open(validatorURL, params).read())
        os.remove(temp[1])

    if len(sys.argv[1:]) > 0:
        for arg in sys.argv[1:]:
            validateFile(arg)
    else:
        validateFile("http://www.google.com")

if __name__=="__main__":
    main()
