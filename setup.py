"""
Package zz-tbx installation

This is free and unencumbered software released into the public domain.
For more information, please refer to <http://unlicense.org/>
"""
from tbx import verinfo
import setuptools
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='zz-tbx',
    version=verinfo._v,
    description="Yet another toolbox library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Tom Barron",
    author_email='tusculum@gmail.com',
    url='https://github.com/tbarron/tbx',
    packages=setuptools.find_packages(),
    package_dir={'tbx': 'tbx'},
    data_files=[
        ('pkg_data/tbx/info', ['./LICENSE', './README.md', './CHANGELOG.md']),
    ],
    include_package_data=True,
    install_requires=requirements,
    license="unlicense",
    zip_safe=False,
    keywords='tbx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='test_tbx',
    tests_require=test_requirements,
    python_requires='>=3.5.8',
)
