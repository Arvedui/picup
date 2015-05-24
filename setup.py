#!/usr/bin/python

from setuptools import setup, find_packages

import picup

setup(
    name='picup',
    version=picup.__version__,
    description='PyQt based Picflash upload tool',
    url='https://github.com/Arvedui/picup',
    author='Arvedui',
    author_email='Arvedui@posteo.de',
    license='GPLv2',
    packages=find_packages(),
    install_requires=['picuplib', 'requests'],
    package_data={
            'picup':['ui_files/*.ui',]
        },
    entry_points={
            'gui_scripts':[
                'picup = picup:main'
            ]
        },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Environment :: X11 Applications :: Qt',
        ]
    )
