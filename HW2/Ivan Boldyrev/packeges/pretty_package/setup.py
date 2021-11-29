from setuptools import setup

"""
Вроде все правильно делаю, но выдает ошибку, что нет дирректории
error: package directory 'module_name\package1' does not exist
"""

setup(
    name='get_pretty_time_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Your Name',
    author_email='email@example.com',
    license='MIT',
    namespace_packages=['module_name'],
    packages=['module_name.package1', 'module_name.package2'],
    install_requires=[
        'requests==2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'get_time_pp=module_name.package2.pretty_time_module:main'
        ]
    }
)
