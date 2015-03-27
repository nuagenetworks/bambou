from setuptools  import setup

setup(
    name='bambou',
    version='0.0.1',
    author='Christophe Serafin',
    author_email='christophe.serafin@nuagenetworks.net',
    packages=['bambou', 'bambou.utils', 'bambou.contextual'],
    description='REST Library for Nuage Networks',
    long_description=open('README.md').read(),
    install_requires=[line for line in open('requirements.txt')],
    license='TODO',
    url='https://github.com/nuagenetworks',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: Other/Proprietary License",
        "Environment :: Console",
        "Intended Audience :: Developers"
    ]
)
