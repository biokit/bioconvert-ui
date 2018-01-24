# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

_MAJOR = 0
_MINOR = 1
_MICRO = 14
version = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {
        'Brancotte': ('Bryan Brancotte', 'bryan.brancotte@pasteur.fr'),
        },
    'version': version,
    'license': 'BSD',
    'download_url': ['http://pypi.python.org/pypi/bioconvert-ui', ],
    'url': ['https://github.com/biokit/bioconvert-ui', ],
    'description': 'A simple user interface presenting in the browser the conversion proposed by bioconvert.',
    'platforms': ['Linux', 'Unix', 'MacOsX', 'Windows'],
    "keywords": ["django", "REST", "NGS", "bam2bed", "fastq2fasta", "bam2sam"],
    'classifiers': [
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',]
    }


with open('README.rst') as f:
    readme = f.read()

requirements = open("requirements.txt").read().split()

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    # mock, pillow, sphinx, sphinx_rtd_theme installed on RTD
    # but we also need numpydoc and sphinx_gallery
    extra_packages = ["numpydoc", "sphinx_gallery"]
    requirements += extra_packages


setup(
    name='bioconvert-ui',
    version=version,
    maintainer=metainfo['authors']['Brancotte'][0],
    maintainer_email=metainfo['authors']['Brancotte'][1],
    author='The bioconvert Contributors',
    author_email=metainfo['authors']['Brancotte'][1],
    long_description=readme,
    keywords=metainfo['keywords'],
    description=metainfo['description'],
    license=metainfo['license'],
    platforms=metainfo['platforms'],
    url=metainfo['url'][0],
    download_url=metainfo['download_url'][0],
    classifiers=metainfo['classifiers'],
    zip_safe=False,
    packages=find_packages(),
    package_data = {'bioconvert-ui' : ["bioconvertui/*"] },
    #include_package_data=True,
    install_requires=requirements,

    # This is recursive include of data files
    exclude_package_data={"": ["__pycache__"]},

    entry_points={
        'console_scripts': [
           'bioconvert-ui=bioconvertui.manageui:main',
        ]
    },
)
