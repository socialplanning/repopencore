from setuptools import setup, find_packages
import sys, os

version = '0.2dev'

README = open('README.txt').read()

setup(name='repopencore',
      version=version,
      description="run opencore with repoze.zope2",
      long_description=README,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ethan Jucovy',
      author_email='ejucovy@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      dependency_links=[
        "http://svn.sccs.swarthmore.edu/egj/fake_zope2#egg=zope2-0.0",
        "http://svn.sccs.swarthmore.edu/egj/repoze.zope2_r4571_before_dependency_cleanup#egg=repoze.zope2-2.0repopencore",
        ],
      install_requires=[
        "zope2==0.0",
        "repoze.zope2==2.0repopencore",
      ],
      entry_points="""
      [console_scripts]
      mkopencoreconfig = repopencore:make_config
      run-opencore-wsgi = repopencore:start_server

      [paste.composite_factory]
      wsgifactory = repopencore.wsgi:factory
      """,
      )
