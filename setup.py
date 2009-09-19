from setuptools import setup, find_packages
import sys, os

version = '0.3'

README = open('README.txt').read()
CHANGES = open('CHANGES.txt').read()

long_description = """%s
New in this version
===================

%s
""" % (README, CHANGES)

setup(name='repopencore',
      version=version,
      description="run opencore with repoze.zope2",
      long_description=long_description,
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

      install-myghty-fork = repopencore:install_myghty_fork
      install-tasktracker = repopencore:install_tasktracker
      install-deliverance = repopencore:install_deliverance

      mkopencoreconfig-with-tt = repopencore:make_config_with_tt

      [paste.composite_factory]
      wsgifactory = repopencore.wsgi:factory
      """,
      )
