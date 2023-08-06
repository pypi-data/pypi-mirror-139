from setuptools import setup, find_packages

setup(
    name='grailabsDataCliLib',
    version='1.0.0',
    description='A example Python package',
    url='https://github.com/daniELgrailDev/grailabs-data-cli',
    author='Daniel Zelalem',
    author_email='danielzelalemheru@gmail.com',
    license='BSD 2-clause',
    packages=['grailabsDataCli', 'grailabsDataCli.scripts'],
    install_requires=['requests == 2.27.1'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
