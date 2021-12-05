from setuptools import setup

setup(
    name='unixtime_pkg',
    version='0.1',
    packages=['get_time_pkg'],
    install_requires=['requests==2.26.0'],
    # entry_points={
    #     'console_scripts': [
    #         'get_time=get_time_pkg.main:main'
    #     ]
    # }
)
