from setuptools import setup

setup(
    name='get_time_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Your Name',
    author_email='email@example.com',
    license='MIT',
    packages=['module_name'],
    namespace_packages=['module_name'],
    install_requires=[
        'requests==2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'get_time=module_name.unix_time_module:main'
        ]
    }
)
