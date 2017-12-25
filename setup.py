import version
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# with open('README.md') as readme_file:
#     readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tbx',
    version=version._v,
    description="toolbox",
    # long_description=readme,
    author="Tom Barron",
    author_email='tusculum@gmail.com',
    url='https://github.com/tbarron/tbx',
    packages=[
        'tbx',
    ],
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
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='test_tbx',
    tests_require=test_requirements,
)
