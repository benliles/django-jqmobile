from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='django-jqmobile',
      version=version,
      description="A Django Application for creating JQuery Mobile websites",
      long_description=open("README").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        #"Development Status :: 6 - Mature",
        ],
      keywords='django jquerymobile',
      author='Texas A&M University Library',
      author_email='webmaster@library.tamu.edu',
      maintainer='Benjamin Liles',
      maintainer_email='benliles@library.tamu.edu',
      url='http://library.tamu.edu',
      license='Apache License 2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ])
