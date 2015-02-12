import os
from setuptools import setup, find_packages

long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(name='ExpressPigeon',
      version='0.0.3',
      description='ExpressPigeon API',
      long_description=long_description,
      author='Gleb Galkin',
      author_email='gleb@expresspigeon.com',
      license='BSD',
      packages=find_packages('expresspigeon', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
      package_dir={'': 'expresspigeon'},
      keywords=' '.join(['expresspigeon',
                         'api',
                         'email',
                         'marketing',
                         'transactional'
      ]),
      url='https://github.com/expresspigeon/expresspigeon-python',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      tests_require=['pytz'])