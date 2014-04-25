import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    
    name = "splparser",
    version = "0.2.0",
    url = "http://pypi.python.org/splparser",
    author = "Sara Alspaugh",
    author_email = "saraalspaugh@gmail.com",
    license = "BSD",
    description = ("A simple parser for the Splunk Processing Language which emits parse trees."),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Other",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: BSD License",
    ],
    keywords = "Splunk Processing Language SPL parser",
    
    packages=['splparser', 
        'splparser.lexers', 
        'splparser.parsetabs',
        'splparser.regexes',
        'splparser.rules',
        'splparser.rules.common', 
        'test'],
    requires=["ply", "nose"],
)
