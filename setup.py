from distutils.core import setup

setup(
    name='bambou',
    version='0.0.1',
    author='Christophe Serafin',
    author_email='christophe.serafin@alcatel-lucent.com',
    packages=['bambou', 'bambou.utils'],
    description='REST Library for Nuage Networks',
    long_description=open('README.txt').read(),
    install_requires=[line for line in open('requirements.txt')],
)
