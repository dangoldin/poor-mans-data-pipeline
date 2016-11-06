# Mostly from http://peterdowns.com/posts/first-time-with-pypi.html

from distutils.core import setup
setup(
  name = 'pmdp',
  packages = ['pmdp'],
  version = '0.2',
  description = 'A poor man\'s data pipeline',
  author = 'Dan Goldin',
  author_email = 'dangoldin@gmail.com',
  url = 'https://github.com/dangoldin/poor-mans-data-pipeline',
  download_url = 'https://github.com/dangoldin/poor-mans-data-pipeline/tarball/0.2',
  keywords = ['data', 'data-pipeline'],
  classifiers = [],
)
