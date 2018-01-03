# -*- coding: utf-8 -*-


import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'amnesiacms'
]

setup(
    name='amnesiabbpf',
    version='0.0.1',
    description='amnesia bbpf',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Julien Cigar',
    author_email='julien@perdition.city',
    url='https://github.com/silenius/amnesia',
    keywords='web wsgi pyramid cms sqlalchemy',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='amnesiabbpf',
    install_requires=install_requires,
    entry_points={
        'paste.app_factory': [
            'main = amnesiabbpf:main'
        ]
    }

)
