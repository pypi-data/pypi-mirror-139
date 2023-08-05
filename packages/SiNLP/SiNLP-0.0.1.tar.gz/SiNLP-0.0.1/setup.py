from setuptools import setup

# Converts readme file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Python set up file
setup(
    name='SiNLP',
    version='0.0.1',
    packages=['nmodels'],
    url='https://github.com/christopher-chandler/ngrams',
    license='MIT',
    author='Christopher Chandler',
    author_email='christopher.chandler@outlook.de',
    description='This is a simple NLP project providing a ngram model package.',
    long_description=long_description,# README
    long_description_content_type="text/markdown"#
    )
