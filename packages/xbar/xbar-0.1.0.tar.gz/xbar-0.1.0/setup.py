from setuptools import setup

from xbar import __version__ as pkg


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=pkg.__name__,
    version=pkg.__version__,
    author=pkg.__author__,
    author_email=pkg.__author_email__,
    url=pkg.__url__,
    license=pkg.__license__,
    license_files=('LICENSE',),
    description=pkg.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://xbar.readthedocs.io/en/latest/',
        'Source': pkg.__url__
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    package_data={

    },
    packages=['xbar'],
    install_requires=[
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'xbar=xbzr.__main__:main',
        ]
    }
)
