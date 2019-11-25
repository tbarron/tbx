"""
Package zz-tbx installation
Copyright 2019-... Tom Barron
See LICENSE for details
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
    # packages=[
    #     'tbx',
    # ],
    package_dir={'tbx': 'tbx'},
    # package_data={'tbx': './README.md'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
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
    python_requires='>=3.6',
)
