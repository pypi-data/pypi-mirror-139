
from setuptools import setup, find_packages

setup(
  name='blockchain_users_generator',
  version='0.1',
  license='MIT',
  author="Alexandro Tapia",
  author_email='alexandro@zpace.link',
  packages=find_packages('src'),
  package_dir={'': 'src'},
  url='https://github.com/alexandrotapiaflores/users_generator',
  keywords='users generator blockchain',
  install_requires=[
    "asn1crypto==1.4.0",
    "cffi==1.15.0",
    "coincurve==17.0.0",
    "names==0.3.0",
    "pycparser==2.21",
    "pysha3==1.0.2",
  ],
)