This is an updated MultipartPostHandler that works with python 3, forked from
version 0.1.0.

Usage:
import MultipartPostHandler
opener = urllib.request.build_opener(MultipartPostHandler.MultipartPostHandler)

Enables the use of multipart/form-data for posting forms

Install: pip install git+https://github.com/anuvab/MultipartPostHandler-py3

Original at: http://pipe.scs.fsu.edu/PostHandler/MultipartPostHandler.py
Updated python2 version for utf-8 systems: https://github.com/sergiomb2/MultipartPostHandler2/

You can install the python 2 version using "pip install MultipartPostHandler".
