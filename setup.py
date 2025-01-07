from setuptools import setup

setup(
    author='Rounak Vyas',
    author_email='itsron143@gmail.com',
    name='es-indexer',
    version='0.1',
    description='A command line tool written in Python to help quickly populate json data into Elasticsearch.',
    url='https://github.com/itsron143/es-indexer',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=['es_indexer'],
    install_requires=[
            'Click', 'elasticsearch',
    ],
    entry_points={
        'console_scripts': [
            'es-indexer=es_indexer.main:main',
        ]
    },
)
