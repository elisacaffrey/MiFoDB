#!/usr/bin/env python

from setuptools import setup, find_packages

from MiFoDB._version import __version__

setup(name='MiFoDB',
      version=__version__,
      description='Profiling of fermented food associated microbes',
      url='https://github.com/elisacaffrey/MiFoDB',
      author='Elisa Caffrey and Matt Olm',
      author_email='ecaffrey@stanford.edu',
      license='MIT',
      package_data={'MiFoDB': ['helper_files/NullModel.txt']},
      #packages=['MiFoDB'],
      packages=find_packages(exclude=["tests"]),
      scripts=['bin/MiFoDB'],
      python_requires='>=3.4.0',
      install_requires=[
          'numpy',
          'pandas>=0.25,!=1.1.3',
          'seaborn',
          'matplotlib',
          'biopython<=1.74',
          'tqdm',
          'pysam>=0.15', # This sets a requirement for python 3.7 for now, but so be it. pysam v0.9 (which works on python 3.8) has a broken iterator (has no stop)
          'networkx',
          'h5py',
          'psutil',
          'lmfit',
          'pytest'
      ],
      zip_safe=False)
