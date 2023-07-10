from setuptools import setup, find_packages

setup(
   name='mini_readability',
   version='0.1',
   description='A useful module',
   author='Alexandr Semenov',
   author_email='semenov84@mail.ru',
   # packages=['mini_readability'],
   packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
   install_requires=['requests', 'beautifulsoup4']
)
