from setuptools import setup

# Converts readme file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Python set up file
setup(
    name='nmodels',
    version='0.0.5',
    packages=['nmodels'],
    url='https://github.com/christopher-chandler/ngrams',
    license='MIT',
    author='Christopher Chandler',
    author_email='christopher.chandler@outlook.de',
    description='This is a simple nlp project providing a ngram model package.',
    long_description=long_description, # ReadMe
    long_description_content_type="text/markdown"#
    )
