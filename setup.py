#!/usr/bin/env python

import io
import os
from setuptools import setup, find_packages


def read(filename):
    with io.open(
            os.path.join(os.path.dirname(__file__), filename),
            encoding='utf-8') as f:
        return f.read()


setup(
    name='django-flock',
    version=__import__('flock').__version__,
    description='Simple crowdfunding for Django',
    long_description=read('README.rst'),
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='https://github.com/matthiask/django-flock/',
    license='MIT License',
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-mooch',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False,
)
