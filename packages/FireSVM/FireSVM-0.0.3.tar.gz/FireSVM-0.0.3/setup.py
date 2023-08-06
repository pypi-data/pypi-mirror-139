#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='FireSVM',
      description='Library containing different variants of the SVM algorithm',
      version = "0.0.3",
      author='Ayman Lafaz',
      author_email='ayman.lafaz@um5r.ac.ma',
      packages=find_packages(where='.'),
     )
