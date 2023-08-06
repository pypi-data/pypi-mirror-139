import os
from setuptools import setup, find_packages


setup(
    name="txAMQP3",
    version='0.9.3',
    author="Esteve Fernandez",
    author_email="esteve@apache.org",
    description="Python3 library for communicating with AMQP peers and brokers using Twisted",
    license='Apache License 2.0',
    packages=find_packages(exclude=["tests"]),
    keywords="twisted amq",
    url="https://github.com/jookies/txamqp",
    py_modules=["txAMQP3"],
    include_package_data=True,
    package_data={'txamqp3': ['README.md']},
    install_requires=['Twisted~=22.1.0'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Twisted",
        "Topic :: System :: Networking",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
