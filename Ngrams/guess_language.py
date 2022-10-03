# Created by: Acer Jagrup ACJ190005
#   Assignment: Ngrams
#   Class: CS 4395.001
#   Date: October 2, 2022
#


import nltk
import pickle
import numpy

solution_starting_value = 1  # What line number does the solution start counting with?
languages = ['English', 'French', 'Italian']
test_file_name = 'LangId.test'
solution_file_name = 'LangId.sol'
guesses_file_name = 'LangId.guesses'


def main():
    language_ngrams = create_language_ngrams(languages)
    calculate_line_languages(test_file_name, guesses_file_name, language_ngrams)  # Writes to guesses file
    accuracy, incorrect_line_numbers = calculate_accuracy(guesses_file_name, solution_file_name)
    print(f"The model's prediction accuracy is {accuracy}.")
    print(f"The incorrect line numbers are: {incorrect_line_numbers}")


# Assumes "language_name.unigrams.p" and "language_name.bigrams.p" exist
def create_language_ngrams(languages):
    language_ngrams = {}  # key: language_name, value: [unigram_dict, bigram_dict]
    for language_name in languages:
        unigram_dict = pickle.load(open(language_name + '.unigrams.p', 'rb'))
        bigram_dict = pickle.load(open(language_name + '.bigrams.p', 'rb'))
        language_ngrams[language_name] = [unigram_dict, bigram_dict]

    return language_ngrams


def calculate_line_languages(input_file_name, output_file_name, language_ngrams):
    with open(input_file_name, 'r') as f:
        raw_text_lines = f.readlines()

    with open(output_file_name, 'w') as f:
        for line_number, line in enumerate(raw_text_lines):
            guess = guess_language_from_line(line, line_number, language_ngrams)
            f.write(guess + "\n")


def guess_language_from_line(line, line_number, language_ngrams):
    tokens = nltk.word_tokenize(line)

    # Will have a list of lists [token, count] for each token in the sentence by language.
    # Example:
    #   "English": [['the', 1], ['horse', 252], ...]
    #   "French": [['je', 264], ['baguette', 34], ...]
    # After which, compare the counts for each language to get probability

    sentence_unigram_counts_per_language = {language: [] for language in languages}
    sentence_bigram_counts_per_language = {language: [] for language in languages}

    for language in language_ngrams:
        for unigram in tokens:
            try:
                unigram_count = language_ngrams[language][0][unigram]
            except KeyError:
                unigram_count = 0
            sentence_unigram_counts_per_language[language].append([unigram, unigram_count])

        for bigram in nltk.ngrams(tokens, 2):
            bigram = ' '.join(bigram)
            try:
                bigram_count = language_ngrams[language][1][bigram]
            except KeyError:
                bigram_count = 0
            sentence_bigram_counts_per_language[language].append([bigram, bigram_count])

    line_unigram_probabilities = {}
    line_bigram_probabilities = {}
    line_laplace_probabilities = {}

    for language in languages:
        line_unigram_probabilities[language] = calculate_sentence_unigram_probabilities(sentence_unigram_counts_per_language, sentence_bigram_counts_per_language, language_ngrams, language)
        line_bigram_probabilities[language] = calculate_sentence_bigram_probabilities(sentence_unigram_counts_per_language, sentence_bigram_counts_per_language, language_ngrams, language)
        line_laplace_probabilities[language] = calculate_sentence_laplace_probabilities(sentence_unigram_counts_per_language, sentence_bigram_counts_per_language, language_ngrams, language)

    #guess = get_key_of_max_value(line_unigram_probabilities)
    #guess = get_key_of_max_value(line_bigram_probabilities)
    guess = get_key_of_max_value(line_laplace_probabilities)

    # Currently implemented with the laplace probability from the hint, but higher probabilities are gotten from
    # simply counting the unigram or bigram in each language, surprisingly enough

    return f"{line_number + solution_starting_value} {guess}"


# Returns the probability that every unigram of the sentence is of a certain language
def calculate_sentence_unigram_probabilities(sentence_unigram_counts_per_language, sentence_bigram_counts_per_language, language_ngrams, language):
    languages = language_ngrams.keys()
    unigrams_probabilities = {language: [] for language in languages}
    for unigram_index, unigram_data in enumerate(sentence_unigram_counts_per_language[language]):
        unigram, unigram_count = unigram_data
        # Number of times unigram appears in this language / number of times it appears in any language
        # Add 1 to the count in case it's 0 (we don't want to multiply by 0)
        # Add 1 to the denominator in case it's 0 (we don't want to divide by 0)
        unigram_count_all_languages = sum([sentence_unigram_counts_per_language[language][unigram_index][1] for language in languages])
        normalized_unigram_count = (unigram_count + 1) / (unigram_count_all_languages + 1)
        unigrams_probabilities[language].append(normalized_unigram_count)

    # Multiply all probabilities together
    return numpy.prod(unigrams_probabilities[language])  # Multiplies together all probabilities of sentence unigrams


# Returns the probability that every bigram of the sentence is of a certain language
def calculate_sentence_bigram_probabilities(sentence_unigram_counts_per_language, sentence_bigram_counts_per_language, language_ngrams, language):
    languages = language_ngrams.keys()
    bigrams_probabilities = {language: [] for language in languages}
    for bigram_index, bigram_data in enumerate(sentence_bigram_counts_per_language[language]):
        bigram, bigram_count = bigram_data
        # Number of times bigram appears in this language / number of times it appears in any language
        # Add 1 to the count in case it's 0 (we don't want to multiply by 0)
        # Add 1 to the denominator in case it's 0 (we don't want to divide by 0)
        bigram_count_all_languages = sum([sentence_bigram_counts_per_language[language][bigram_index][1] for language in languages])
        normalized_bigram_count = (bigram_count + 1) / (bigram_count_all_languages + 1)

        bigrams_probabilities[language].append(normalized_bigram_count)

    # Multiply all probabilities together
    return numpy.prod(bigrams_probabilities[language])  # Multiplies together all probabilities of sentence bigrams


# Returns the probability that every bigram of the sentence is of a certain language using laplace smoothing
def calculate_sentence_laplace_probabilities(sentence_unigram_counts_per_language, sentence_bigram_counts_per_language, language_ngrams, language):
    languages = language_ngrams.keys()
    language_unigram_counts = language_ngrams[language][0]

    laplace_probabilities = {language: [] for language in languages}
    for bigram_index, bigram_data in enumerate(sentence_bigram_counts_per_language[language]):
        bigram, bigram_count = bigram_data

        try:
            first_unigram_count = language_unigram_counts[bigram.split()[0]]
        except KeyError:  # Unigram doesn't exist in this language
            first_unigram_count = 1

        total_vocabulary_size = sum([len(language_unigram_counts.keys()) for language in languages])
        laplace_bigram_probability = (bigram_count + 1) / (first_unigram_count + total_vocabulary_size)

        laplace_probabilities[language].append(laplace_bigram_probability)

    # Multiply all probabilities together
    return numpy.prod(laplace_probabilities[language])


def get_key_of_max_value(probability_dict):
    return max(probability_dict, key=probability_dict.get)


def calculate_accuracy(guesses_file, solution_file):
    with open(solution_file, 'r') as f:
        solution_list = f.readlines()

    with open(guesses_file, 'r') as f:
        guesses_list = f.readlines()

    correct_guesses_list = [guesses_list[i].strip() == solution_list[i].strip() for i in range(len(solution_list))]
    # Use .strip() to remove '\n' from each line of the solution
    accuracy = sum(correct_guesses_list) / len(correct_guesses_list)

    incorrect_line_numbers = [index + solution_starting_value for index, guess in enumerate(correct_guesses_list) if not guess]
    # Only get line numbers for False guesses
    # Add the starting values to start line numbers at the right number instead of 0

    return accuracy, incorrect_line_numbers


main()
