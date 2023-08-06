from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2'
DESCRIPTION = 'Powerful security network package'
LONG_DESCRIPTION = 'Powerful security network package for hackers and all security experts'

# Setting up
setup(
    name="abdal-net-py",
    version=VERSION,
    author="Ebrahim Shafiei (EbraSha)",
    author_email="Prof.Shafiei@Gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url="https://github.com/abdal-security-group/abdal-net-py",
    project_urls={
        "Bug Tracker": "https://github.com/abdal-security-group/abdal-net-py/issues",
    },
    install_requires=['hurry.filesize', 'speedtest'],
    keywords=['python', 'security', 'hack', 'network', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
