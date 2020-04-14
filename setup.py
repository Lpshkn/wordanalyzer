from setuptools import setup, find_packages
from os.path import join, dirname
import analyzer

setup(
    name='wordanalyzer',
    version=analyzer.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='lpshkn',
    entry_points={
        'console_scripts': ['wordanalyzer = analyzer.main:main']
    },
    install_requires=[
        'pybktree==1.1',
        'strsim==0.0.3'
    ],
    description="""This program analyzes the source set of words was obtained from the file (-s parameter), 
    clear this set from incorrect symbols, split cleared words to lexemes, then correct them by replacing assumed 
    incorrect words to right words and then will create new set of words and save it to the 
    destination file (-d parameter)."""
)
