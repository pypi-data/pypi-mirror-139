
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name='ImgAlter',
    version='0.1.4',
    author='White.tie',
    author_email='1042798703@qq.com',
    url='https://github.com/tyj-1995',
    description='1.Resize the image, 2.image transfer pdf',
    long_description='1.修改图片大小, 2.图片转成pdf',
    packages=['ImgAlter'],
    install_requires=['requests','pillow'],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 3.6",
        ],
)
