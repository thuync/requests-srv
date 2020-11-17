# encoding: utf8

import setuptools

setuptools.setup(
    name="requests_srv",
    version="0.0.9",
    py_modules=["requests_srv"],
    author=u"Paweł Stiasny",
    author_email="pawelstiasny@gmail.com",
    url="http://github.com/thuync/requests-srv",
    license="Apache 2.0",
    description="A wrapper for Requests supporting DNS SRV records.",
    keywords=['requests'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests',
        'dnspython',
    ],
)
