from setuptools import setup, find_packages
setup(
    name = "MultipartPostHandler-py3",
    py_modules = ['MultipartPostHandler'],
    version = "0.1.1",
    description = "A handler for urllib to enable multipart form uploading",
    keywords = ["http", "multipart", "post", "urllib2"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
