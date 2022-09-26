# Created by: Acer Jagrup ACJ190005
#   Assignment: Word Guessing Game
#   Class: CS 4395.001
#   Date: September 25, 2022
#

import random
import sys
import os

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def main():
    raw_text = get_file_text()
    if not raw_text:  # File couldn't be read
        return

    print("The lexical diversity is %.2f." % calculate_lexical_diversity(raw_text))

    tokens, noun_lemmas = pre_process(raw_text)
    noun_dict = create_dict(tokens, noun_lemmas)
    top_fifty_words = list(noun_dict.keys())[:50]
    print("Most common nouns: " + str([(noun, noun_dict[noun]) for noun in top_fifty_words]))

    game = GuessingGame()
    game.play_game(top_fifty_words)


def get_file_text():
    if len(sys.argv) < 2:
        print("Please specify a file to read data from.")
        return None

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        print("Bad filepath.")
        return None

    with open(file_name, "r") as f:
        text = f.read()

    return text


def calculate_lexical_diversity(text):
    tokens = nltk.word_tokenize(text)
    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens)


def pre_process(text):  # Input is list of lines ending in \n
    NOUN_POS_LIST = ['NN', 'NNS', 'NNP', 'NNPS']
    tokens = [word.lower() for word in nltk.word_tokenize(text)
              if word.isalpha() and word not in stopwords.words('english') and len(word) > 5]

    lemmatizer = WordNetLemmatizer()
    lemmas = set([lemmatizer.lemmatize(token) for token in tokens])

    pos_tagged_lemmas = nltk.pos_tag(lemmas)  # Is a list of tuples ('word', 'POS')
    print("First 20 POS-tagged lemmas: " + str(pos_tagged_lemmas))

    noun_lemmas = [lemma[0] for lemma in pos_tagged_lemmas if lemma[1] in NOUN_POS_LIST]
    print(f"There are {len(tokens)} tokens and {len(noun_lemmas)} nouns.")
    return tokens, noun_lemmas


def create_dict(tokens, noun_lemmas):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in
                         tokens]  # Necessary because "muscles" isn't counted as "muscle" if going just by tokens
    unsorted_dict = {}
    for noun_lemma in noun_lemmas:
        unsorted_dict[noun_lemma] = lemmatized_tokens.count(noun_lemma)

    sorted_dict = dict(sorted(unsorted_dict.items(), key=lambda item: item[1], reverse=True))  # Sort by count
    return sorted_dict


class GuessingGame:
    def __init__(self):
        pass

    EMPTY_CHAR = "_"
    QUIT_CHAR = "!"
    word_list = []
    has_quit = False
    score = 5
    current_word = []
    current_word_key = []
    current_word_key_string = ""
    guessed_letters = set()
    word_is_solved = False

    def play_game(self, word_list):
        self.word_list = word_list
        self.print_game_start_message()
        while len(self.word_list) > 0 and not self.has_quit and self.score > 0:
            # Resetting word variables
            self.current_word_key_string = random.choice(self.word_list)
            self.word_list.remove(self.current_word_key_string)

            self.current_word_key = list(self.current_word_key_string)
            self.current_word = list(self.EMPTY_CHAR * len(self.current_word_key))  # A list of underscores

            # Resetting game state variables
            self.word_is_solved = False
            self.guessed_letters = set()

            # Game loop (per word)
            while not self.word_is_solved and self.score > 0:
                self.print_guessed_letters()
                self.print_score()
                self.display_board(self.current_word)
                user_input = self.request_input()
                if len(user_input) == 1:
                    self.process_input_letter(user_input)
                else:
                    self.process_input_word(user_input)

                if not self.current_word:  # Break if user quits
                    break

            if self.word_is_solved:
                self.print_success_message()
                self.print_next_word_message()
            else:
                self.print_failure_message()
                break

    def display_board(self, character_list):
        [print(character, end=" ") for character in character_list]
        print('\n')

    def request_input(self):
        return input("Guess a letter: ").strip().lower()  # Strip input in case of spaces

    def process_input_letter(self, letter):
        if letter == self.QUIT_CHAR:
            self.has_quit = True
            self.current_word = None  # Player has given up
            print("Quitting...")
            return

        elif letter in self.guessed_letters:
            print("This letter has already been guessed.")
            return

        elif letter in self.current_word_key:
            self.score += 1
            print(f"Right!")
            self.guessed_letters.add(letter)
            self.update_word(letter)

        else:  # Letter is wrong
            self.score -= 1
            if self.score > 0:  # Don't print this if the user failed--they won't get a chance to guess again
                print(f"Sorry, guess again.")
            self.guessed_letters.add(letter)

        self.word_is_solved = self.current_word.count(
            self.EMPTY_CHAR) == 0  # Word is solved if there are no empty spots left

    def update_word(self, letter):
        for i in range(0, len(self.current_word)):
            if self.current_word_key[i] == letter:
                self.current_word[i] = letter

    def process_input_word(self, word):
        if word == self.current_word_key_string:
            self.score += self.current_word.count(
                self.EMPTY_CHAR)  # For guessing, user gets +1 score for each empty spot left
            self.current_word = self.current_word_key
            self.word_is_solved = True
        else:
            print("No, that is not the word.")
            self.score -= 1

    def print_guessed_letters(self):
        print("Guessed letters: ", end="")
        [print(letter, end=" ") for letter in self.guessed_letters]
        print()

    def print_game_start_message(self):
        print(f"\nStarted Guessing Game. Guess letters or the whole word. Type {self.QUIT_CHAR} to quit.")

    def print_score(self):
        print(f"Score is {self.score}")

    def print_success_message(self):
        print(f"You got it! The word was: {self.current_word_key_string}.")

    def print_failure_message(self):
        print(f"Better luck next time! The word was: {self.current_word_key_string}.")

    def print_next_word_message(self):
        print("On to the next word!\n")


main()
