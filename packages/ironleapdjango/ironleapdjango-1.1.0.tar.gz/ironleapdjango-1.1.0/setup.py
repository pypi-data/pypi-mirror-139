from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = ''
if path.exists('README.md'):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='ironleapdjango',
    author='Iron Leap Inc.',
    author_email='founders@ironleap.io',
    version='1.1.0',
    description='Iron Leap Django SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://ironleap.io',
    packages=find_packages(),
    install_requires=[
        "requests",
        "jsonpickle",
        "python-dateutil",
        "apscheduler"
    ],
)
