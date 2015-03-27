from setuptools  import setup

setup(
    name='bambou',
    version='1.0-a1',
    url='http://www.nuagenetworks.net/',
    author='Christophe Serafin',
    author_email='christophe.serafin@alcatel-lucent.com',
    packages=['bambou', 'bambou.utils', 'bambou.contextual'],
    description='REST Library for Nuage Networks',
    long_description=open('README.md').read(),
    install_requires=[line for line in open('requirements.txt')],
)
