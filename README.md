# NLP_Portfolio
Portfolio for Human Language Technologies course
### Overview of NLP
An overview of natural language processing can be found [here](Overview_of_NLP.pdf).
## Assignments
#### Text Processing with Python: [Overview](Text_Processing/Overview_of_Asg_1.pdf), [Code](Text_Processing/textprocessing.py)
This project involves creating a Python script to read through a badly-wrangled set of data on people from a .csv file and 
clean it up, converting the data into a dictionary of Person objects which store first names, last names, middle initials, 
IDs, and phone numbers. The program also demonstrates the pickle library by saving the dictionary of Persons to a persons.p 
file and retrieving it.
#### Exploring NLTK: [PDF](Exploring_NLTK/Asg2.pdf)
In this notebook I used NLTK to analyze its built-in text1, including lemmatization, stemming, and concordance.
#### Guessing Game: [Code](Guessing_Game/guessinggame.py)
This project involves using NLTK to parse a supplied text file to determine the 50 most common nouns. After that, those nouns are used as a list for a hangman or Wheel of Fortune-style game.  
#### WordNet: [PDF](WordNet/WordNet.pdf)
In this notebook I explored some capabilities of WordNet including synonym sets, sentiment analysis, and collocations.
#### Ngrams: [Pickle Creation Code](Ngrams/create_pickles.py), [Guess Language Code](Ngrams/guess_language.py)
This project is separated into two scripts. The first one, create_pickles.py, reads some training data for multiple languages and 
creates dictionaries of the counts of each unigram and bigram in that text using NLTK, saving them to files using pickle.
The second file, guess_language.py, uses those pickled dictionaries to calculate the probability that each line of a test
file is of a certain language, then writing those guesses to a file and comparing it to the solution file to determine
the accuracy of the prediction. With a simple guess by unigram, the accuracy is 100% on this test file, and very close to 
that with a simple bigram probability guess. With a bigram guess with laplace smoothing, the accuracy is a bit lower at
around 96%.