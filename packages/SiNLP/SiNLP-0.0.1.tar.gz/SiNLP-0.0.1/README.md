# Ngram Model
This is a basic python module that provides basic nlp algorithms.
This is meant for instructional purposes, but my also be used for smaller 
projects. 

# Python Requirements
Any Python version 3.8 and above is supported.

# Install
Install this pip package by typing the following into the command prompt:

```
pip install SinLP
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
