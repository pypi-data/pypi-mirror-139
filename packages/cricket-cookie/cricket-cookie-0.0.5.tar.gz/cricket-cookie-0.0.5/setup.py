import os

from setuptools import find_packages, setup

PACKAGE_NAME = "cricket-cookie"
DESCRIPTION = 'Cricket Cookie'
URL = 'https://cricket-cookies.com'
EMAIL = 'grid-eng@grid.ai'
AUTHOR = 'Grid.ai'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = os.getenv("VERSION", "0.0.5")

#  What packages are required for this module to be executed?
REQUIRED = []
with open('requirements.txt') as f:
    for line in f.readlines():
        REQUIRED.append(line.replace('\n', ''))

#  Where the magic happens:
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests', 'tests.*')),
    entry_points={
        'console_scripts': ['cricket_cookie=cricket_cookie.cli.__main__:main'],
    },
    long_description="Grid AI Command Line Interface",
    long_description_content_type="text/x-rst",
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
