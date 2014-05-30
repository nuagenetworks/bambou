from distutils.core import setup

setup(
    name='restnuage',
    version='0.0.1',
    author='Christophe Serafin',
    author_email='christophe.serafin@alcatel-lucent.com',
    packages=['restnuage', 'restnuage.utils'],
    description='REST Library for Nuage Networks',
    long_description=open('README.txt').read(),
    install_requires=[line for line in open('requirements.txt')],
)
