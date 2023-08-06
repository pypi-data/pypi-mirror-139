from setuptools import setup, find_packages

with open('README.md', 'r') as handle:
    long_description = handle.read()

setup(
    name='diskloaf',
    version='0.3.0',
    description='A tool for creating a large file (a loaf) in order to wipe a hard disk '
                'written by someone who knows nothing about security',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Andrew Blomenberg',
    author_email='andrewBlomen@gmail.com',
    url='https://github.com/Yook74/diskloaf',
    packages=['diskloaf'],
    install_requires=['progressbar2'],
    entry_points={
        'console_scripts': ['diskloaf = diskloaf.loaf:main'],
    }
)