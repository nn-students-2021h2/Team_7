from setuptools import setup

setup(
    name='pp_unixtime_pkg',
    version='0.1',
    packages=['get_pp_time_pkg'],
    install_requires=['unixtime_pkg'],
    entry_points={
        'console_scripts': [
            'get_time=get_pp_time_pkg.main:main',
        ]
    }
)
