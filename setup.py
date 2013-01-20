import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "splparser",
    version = "0.1.0",
    author = "Sara Alspaugh",
    author_email = "saraalspaugh@gmail.com",
    description = ("A simple parser for the Splunk Processing Language which emits parse trees."),
    license = "BSD",
    keywords = "Splunk Processing Language SPL parser",
    url = "http://pypi.python.org/splparser",
    packages=['splparser', 
        'splparser.cmdparsers', 
        'splparser.cmdparsers.common', 
        'test'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Other",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: BSD License",
    ],
    requires=["ply"]

)
