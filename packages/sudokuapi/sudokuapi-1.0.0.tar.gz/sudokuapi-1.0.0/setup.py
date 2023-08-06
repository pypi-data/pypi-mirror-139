from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

name = 'sudokuapi'
version = '1.0.0'

setup(
    name=name,
    version=version,
    description='A Python package for solving Sudoku puzzles.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GNU GPL v3',
    author='alotofaxolotl',
    author_email='alottaaxolotl@hotmail.com',
    url='https://github.com/alotofaxolotl/SudokuAPI',
    project_urls={
        'Bug Tracker': 'https://github.com/alotofaxolotl/SudokuAPI/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",

    ],
    package_dir={"": "src"},
    packages=find_packages(where="src")
)