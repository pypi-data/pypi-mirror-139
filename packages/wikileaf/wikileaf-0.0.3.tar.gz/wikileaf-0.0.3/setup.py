from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='wikileaf',
    version='0.0.3',
    description='An API Wrapper for the Wikileaf API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/notjawad/wikileaf',
    author='Jawad Abd',
    author_email='jawad.abdulrazzaq@outlook.com',
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ],
    keywords=['wikileaf', 'cannabis', 'weed', 'weedmaps'],
    packages=find_packages(exclude=['docs', 'tests']),
    setup_requires=['pytest-runner', 'setuptools>=38.6.0'],  # >38.6.0 needed for markdown README.md
    tests_require=['pytest', 'pytest-cov'],
    install_requires=["requests"]

)
