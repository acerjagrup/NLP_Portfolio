# NLP_Portfolio
Portfolio for Human Language Technologies course
### Overview of NLP
An overview of natural language processing can be found [here](Overview_of_NLP.pdf).
## Assignments
#### Text Processing with Python: [Overview](Text_Processing/Overview_of_Asg_1.pdf), [textprocessing.py](Text_Processing/textprocessing.py)
This project involves creating a Python script to read through a badly-wrangled set of data on people from a .csv file and 
clean it up, converting the data into a dictionary of Person objects which store first names, last names, middle initials, 
IDs, and phone numbers. The program also demonstrates the pickle library by saving the dictionary of Persons to a persons.p 
file and retrieving it.
#### Exploring NLTK: [PDF of Notebook](Exploring_NLTK/Asg2.pdf)
In this notebook I used NLTK to analyze its built-in text1, including lemmatization, stemming, and concordance.
#### Guessing Game: [guessinggame.py](Guessing_Game/guessinggame.py)
This project involves using NLTK to parse a supplied text file to determine the 50 most common nouns. After that, those nouns are used as a list for a hangman or Wheel of Fortune-style game.  
#### WordNet: [PDF of Notebook](WordNet/WordNet.pdf)
In this notebook I explored some capabilities of WordNet including synonym sets, sentiment analysis, and collocations.
#### Ngrams: [Overview](Ngrams/Ngrams.pdf), [create_pickles.py](Ngrams/create_pickles.py), [guess_language.py](Ngrams/guess_language.py)
This project is separated into two scripts. The first one, create_pickles.py, reads some training data for multiple languages and 
creates dictionaries of the counts of each unigram and bigram in that text using NLTK, saving them to files using pickle.
The second file, guess_language.py, uses those pickled dictionaries to calculate the probability that each line of a test
file is of a certain language, then writing those guesses to a file and comparing it to the solution file to determine
the accuracy of the prediction. With a simple guess by unigram, the accuracy is 100% on this test file, and very close to 
that with a simple bigram probability guess. With a bigram guess with laplace smoothing, the accuracy is a bit lower at
around 96%.
#### Web Crawler: [Report](Web_Crawler/Web_Crawler_Report.pdf), [webcrawler.py](Web_Crawler/webcrawler.py)
In this project, my partner Silvano Gallegos and I created a script which, given a link to a website (we chose the Wikipedia link of Lamborghini),
scrapes that website to find related links. It then filters those links by HTML tag data and link content to avoid links 
with no information, such as a link leading to an image of the Wikipedia logo. After procuring those relevant URLs, the script
then scrapes a number of those sites for text, which it stores to files. Each of those texts is cleaned through a filter
and sentence-tokenized by NLTK to create a new text file, a clean version with each sentence taking up its own line. The text
from those clean text files is extracted, stopwords, numbers, and punctuation are removed, and the text is parsed to extract 
the top 30 important terms using term frequency. We then manually chose 10 words which are related to Lamborghini, as some 
top terms were simply a result of Wikipedia formatting, such as the word "article". The script, using those 10 words, creates 
a dictionary corresponding a word to every sentence that contains it, and stores those in a file for each of the 10 words,
where every line is a sentence containing that word. In the future, this will be used as a knowledge base.

The report also contains an overview of the code as well as some sample dialogues for the chatbot.
#### Sentence Parsing: [Report](Sentence_Parsing/Sentence_Parsing.pdf)
This assignment involved writing a complex sentence and performing a phrase structure grammar (PSG) parse, dependency parse, and
semantic role label (SRL) parse on that sentence. I chose the sentence, "Despite having already completed three years of high school, Jack found out that he had to complete two more due to his poor performance"
and performed those parses by hand. Those are included in the report as well as my thoughts on the pros and cons of each parse.

#### Author Attribution: [PDF of Notebook](Author_Attribution/Author_Attribution.pdf)
In this project, I used several models to analyze the text of the Federalist papers to make guesses as to who authored each document.
Some models used include Naïve Bayes, Logistic Regression, and an MLPRegressor neural network.

#### ACL Paper Analysis: [PDF of Summary](ACL/ACL_Paper_Analysis.pdf)
This document is a summary of a paper I chose to read from the Association for Computational Linguistics, "Lower Perplexity is Not Always Human-Like"
by Tatsuki Kuribayashi et al.
I summarize the problem, prior work, unique contributions, self-evaluation, citations of the authors, and importance of the report in the summary document
as a foray into reading academic papers.

#### Chatbot: [Report](Chatbot/Chatbot_Evaluation_and_Report.pdf), [chatbot.py](Chatbot/chatbot.py)
In this project, my partner Silvano Gallegos and I created a rules-based chatbot based off of the API Ninjas' Cars API which
provides lists of cars based on some filter parameters. The bot also has a conversation with the user before that during which it
saves the user's name, place of origin, likes, and dislikes. We also wrote a report on the bot including a detailed description,
flow diagrams, sample dialogues, our evaluation of the bot, appendices for both the API and the user data we collected.