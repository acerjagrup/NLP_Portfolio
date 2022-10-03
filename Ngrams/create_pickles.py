# Created by: Acer Jagrup ACJ190005
#   Assignment: Ngrams
#   Class: CS 4395.001
#   Date: October 2, 2022
#


import nltk
import pickle


def main():
    file_name_list = ['LangId.train.English', 'LangId.train.French', 'LangId.train.Italian']

    for file_name in file_name_list:
        unigram_count, bigram_count = create_count_dictionaries(file_name)
        file_language = file_name.split('.')[-1]  # Should get the language name

        print(f"Creating pickles for {file_language}: {len(unigram_count)} unigrams and {len(bigram_count)} bigrams...")
        pickle.dump(unigram_count, open(file_language + '.unigrams.p', 'wb'))
        pickle.dump(bigram_count, open(file_language + '.bigrams.p', 'wb'))
        print(f"Created two pickles for {file_language}.")


def create_count_dictionaries(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        raw_text = f.read()

    print(f"Processing {file_name}...")
    raw_text.replace("\n", " ")
    tokens = nltk.word_tokenize(raw_text)
    unigrams = nltk.ngrams(tokens, 1)  # Generator object
    bigrams = nltk.ngrams(tokens, 2)  # Generator object

    bigrams = [' '.join(bigram) for bigram in bigrams]  # Convert ("a", "b") to "a b"

    unigram_counts = {unigram: unigrams.count(unigram) for unigram in unigrams}
    bigram_counts = {bigram: bigrams.count(bigram) for bigram in bigrams}

    return unigram_counts, bigram_counts


main()
