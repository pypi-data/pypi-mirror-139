from pathlib import Path

from setuptools import find_packages, setup

# description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Packages required for this module to be executed
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

#setup initialization
setup(name='zoofs',
      version='0.1.10',
      url='https://github.com/jaswinder9051998/zoofs',
      author='JaswinderSingh',
      author_email='jaswinder9051998@gmail.com',
      license='Apache License 2.0',
      packages=['zoofs'],
      zip_safe=True,
	  description="zoofs is a Python library for performing feature selection using an variety of nature inspired wrapper algorithms..",
      long_description=long_description  ,
	  long_description_content_type='text/markdown',
	  install_requires=list_reqs(),
      include_package_data=True,

      )
