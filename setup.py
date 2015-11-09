import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid-openid',
    'webhelpers',
    'pyramid_mailer',
    'formencode',
    'pyramid_simpleform',
    'pyramid_mailer',
    'pyramid_beaker',
    # 'urllib',
    'urlparse2',
    #    'python_yapps',
    'pyramid_chameleon',
]

setup(name='h2g2m',
      version='0.0',
      description='h2g2m',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='h2g2m crowd',
      author_email='info@h2g2m.com',
      url='http://www.h2g2m.com',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='h2g2m.tests',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = h2g2m:main
      [console_scripts]
      populate_h2g2m = h2g2m.scripts.populate:main
      """,
)

