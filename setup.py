from setuptools import setup, find_packages


setup(
    name='picup',
    version='0.1',
    description='PyQt based Picflash upload tool',
    url='https://github.com/Arvedui/picup',
    author='Arvedui',
    author_email='Arvedui@posteo.de',
    license='GPLv2',
    packages=find_packages(),
    install_requires=['picuplib'],
    package_data={
            'picup':['ui_files/*.ui',]
        },
    entry_points={
            'gui_scripts':[
                'picup = picup:main'
            ]
        }
    )
