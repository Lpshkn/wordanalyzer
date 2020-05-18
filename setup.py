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
        'console_scripts': ['wordanalyzer = main:main']
    },
    test_suite="tests",
    install_requires=[
        'pybktree~=1.1',
        'strsim~=0.0.3',
        'numpy~=1.18.4',
        'pyxdameraulevenshtein~=1.6',
        'nltk~=3.5',
        'setuptools~=45.2.0'
    ],
    description="The main goal of this program consists of analyzing a list of words that you can pass to the input. "
                "This program has 4 modes of working and can work in multiple mode at time."
)
