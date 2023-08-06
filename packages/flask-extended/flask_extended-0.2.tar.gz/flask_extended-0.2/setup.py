from setuptools import setup, find_packages
import codecs
import os

current_directory = os.path.abspath(os.path.dirname(__file__))

'''with codecs.open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()
    f.close()
'''

_VERSION = '0.2'
_DESCRIPTION = 'flask_extended is a tool for help you developing flask applications'
_LONG_DESCRIPTION = 'flask_extended is a tool for help you developing flask application using some api'
_PACKAGES_REQUIRED = ["flask"]
_AUTHOR="giusekk"

setup(
    name="flask_extended",
    version=_VERSION,
    author=_AUTHOR,
    author_email="mannargiusepp@gmail.com",
    description=_DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=_LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=_PACKAGES_REQUIRED,
    keywords=["flask", "helper", "flask_extended"]
)

