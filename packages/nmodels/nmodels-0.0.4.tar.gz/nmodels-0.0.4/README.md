# Ngram Model
This is a basic python module that creates and then pads bigrams from a given sentence.

# Python Requirements
Any Python version 3.6 and above is supported.

# Install
Install this pip package by typing the following into the command prompt:

```
pip install ngram
```

# Nmodels
To import the module function, proceed as follows:

```
>>> import ngrams
>>> from nmodels.gram import simple_bigram
>>> string = "Hello world, how are you" 
>>> [('<START>', 'Hello'), ('Hello', 'world,'), ('world,', 'how'),
 ('how', 'are'), ('are', 'you'), ('you', '<END>')]
```
