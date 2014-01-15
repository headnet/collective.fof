import os
import sys

from setuptools import setup, find_packages

def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read()

version = '1.0-dev'

setup(name='collective.fof',
      version=version,
      description="Custom 404 error messages for Plone!",
      long_description='\n'.join([
          read('README.rst'),
          read('CHANGES.rst'),
          ]),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='plone multilingual dexterity',
      author='Bo Simonsen',
      author_email='bo@headnet.dk',
      license="GPLv2+",
      packages=find_packages('.'),
      package_dir={'': '.'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone>=4.1',
          'plone.app.dexterity',
      ],
      extras_require = {
          'test': [
              'plone.testing>=4.0.6',
              'plone.app.testing',
              'lxml',
              ]
          },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
