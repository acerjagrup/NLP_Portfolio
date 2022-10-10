# Created by: Acer Jagrup ACJ190005 & Silvano Guadalupe Gallegos SGG180002
#   Assignment: Web Crawler
#   Class: CS 4395.001
#   Date: October 7, 2022
#

import requests
import os

from bs4 import BeautifulSoup

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer


def main():
    starter_url = "https://en.wikipedia.org/wiki/Lamborghini"
    urls_file_name = "urls.txt"
    scraped_files_directory = "texts"
    knowledge_base_directory = "kb"

    print(f'Parsing {starter_url}')
    relevant_urls = get_relevant_urls(starter_url, max_number_of_urls=15)

    save_line_list_to_file(relevant_urls, urls_file_name)
    print(f'Scraping {len(relevant_urls)} sites and creating text files in /{scraped_files_directory}')
    url_text_files = scrape_list_of_urls(relevant_urls, directory=scraped_files_directory)
    print(f'Cleaning text files and saving to /{scraped_files_directory}')
    clean_url_text_files = create_clean_files(url_text_files)  # stores a list of filenames

    print(f'Combining text')
    combined_text_as_lines = combine_lines_from_files(clean_url_text_files)

    print(f'Filtering text')
    important_tokens = filter_text(combined_text_as_lines)
    print(f'Lemmatizing text')
    important_lemmas = lemmatize_tokens(important_tokens, min_length=0)

    print('Calculating term frequencies')
    print_term_frequency(important_lemmas, number_of_terms=30)

    MANUALLY_PICKED_IMPORTANT_WORDS = ["Lamborghini", "sport", "engine", "vehicle", "Volkswagen", "manufacturer",
                                       "business", "subsidiary", "Ducati", "model"]

    print(f'Creating knowledge base from {len(MANUALLY_PICKED_IMPORTANT_WORDS)} important words')
    knowledge_base = create_related_sentences_dict(MANUALLY_PICKED_IMPORTANT_WORDS, combined_text_as_lines)

    print(f'Saving knowledge base')
    save_knowledge_base(knowledge_base, directory=knowledge_base_directory)


def get_relevant_urls(start_url, max_number_of_urls):
    response = requests.get(start_url)

    data = response.text
    soup = BeautifulSoup(data, features="html.parser")

    relevant_urls = []
    for anchor_element in soup.find_all('a'):  # <a href="https://google.com">aaa</a> is an anchor element in HTML
        if is_relevant(anchor_element) and anchor_element.get('href') not in relevant_urls:  # Don't add duplicates
            link = anchor_element.get('href')
            if link.startswith('/wiki/'):  # Account for Wikipedia links being in the form /wiki/...
                link = "https://en.wikipedia.org" + link

            relevant_urls.append(link)

        if len(relevant_urls) >= max_number_of_urls:
            break

    else:  # In Python, this means the loop terminated without breaking
        print(f"Only {len(relevant_urls)} relevant urls found out of the maximum {max_number_of_urls}")

    return relevant_urls


def is_relevant(anchor_element):
    link = anchor_element.get('href')
    if not link:  # If the anchor element has no link, we're not interested in it
        return False

    bad_link_elements = ["Protection_policy", "Help:IPA"]  # Boilerplate wikipedia links, irrelevant to the topic
    if any(item in link for item in bad_link_elements):  # If any of these bad link elements are in the link
        return False

    bad_link_starts = ["#"]  # "#" links to another location on the wikipedia page, category links to unrelated stuff
    if any(link.startswith(start) for start in bad_link_starts):
        return False

    if anchor_element.get('accesskey'):  # Some wikipedia internal stuff
        return False

    class_list = anchor_element.get('class')  # .get('class') returns a list of classes
    if class_list:
        bad_classes = ["image", "mw-jump-link", "mw-disambig", "internal", "interlanguage-link-target", ]
        if any(item in class_list for item in bad_classes):  # If any of these bad_classes strings are in the class
            return False

        if "external text" in class_list and "wikipedia" in link:  # Usually links to editing wiki and similar stuff
            return False

    return True


def save_line_list_to_file(lines, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def scrape_list_of_urls(url_list, directory):
    file_names = []

    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory in case it doesn't exist
    for url in url_list:
        text_lines = scrape(url)
        file_name = f"{directory}/Text - " + url.split('/')[-1]  # Get the last term of the link (rudimentary approach)
        save_line_list_to_file(text_lines, file_name)
        file_names.append(file_name)

    return file_names


def scrape(url):
    response = requests.get(url)
    data = response.text  # This will be HTML
    soup = BeautifulSoup(data, features="html.parser")
    processed_text = soup.get_text(' ')
    split_text = processed_text.split('\n')
    return split_text


def clean_text_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        raw_text = f.read()  # List of lines

    raw_text = raw_text.replace('\t', ' ')
    raw_text = raw_text.replace(' .', '.')
    raw_text = raw_text.replace(' ,', ',')

    sentences = nltk.sent_tokenize(raw_text)
    sentences = [s.strip() for s in sentences]
    return sentences


def create_clean_files(list_of_files):
    file_names = []
    for file_name in list_of_files:
        sentences = clean_text_from_file(file_name)
        clean_file_name = file_name + ".clean"
        save_line_list_to_file(sentences, clean_file_name)
        file_names.append(clean_file_name)

    return file_names


def combine_lines_from_files(file_names):
    combined_lines = []
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            combined_lines += lines

    return combined_lines


def filter_text(lines):
    text = '\n'.join(lines)
    text = text.lower()

    tokens = word_tokenize(text)

    # Get rid of punctuation, numbers, and stopwords
    filtered_text = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

    return filtered_text


def lemmatize_tokens(tokens, min_length):
    WNL = WordNetLemmatizer()

    lemmas = [WNL.lemmatize(token) for token in tokens]

    # Getting the tags from our token list
    tagged_lemmas = nltk.pos_tag(lemmas)

    important_lemmas = []

    for tagged_lemma in tagged_lemmas:
        # Picking out the nouns
        if tagged_lemma[1].startswith('N'):
            important_lemmas.append(tagged_lemma[0])

        # Picking out the verbs
        elif tagged_lemma[1].startswith('V'):
            important_lemmas.append(tagged_lemma[0])

    # Removing words shorter than min_length letters
    important_lemmas = [lemma for lemma in important_lemmas if len(lemma) >= min_length]

    return important_lemmas


def print_term_frequency(tokens, number_of_terms):
    tf_dict = {}

    for token in tokens:
        if token in tf_dict:
            tf_dict[token] += 1
        else:
            tf_dict[token] = 1

    # Normalizing tf by total num of tokens
    for token in tf_dict.keys():
        tf_dict[token] = tf_dict[token] / len(tokens)

    # Largest values first
    tf_dict = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    tf_dict = tf_dict[:number_of_terms]  # Get the first x values

    tf_dict = dict(tf_dict)  # Turns back to a dictionary

    print(f"\n\nHere are the top {number_of_terms} terms from the corpus:")
    # Printing out the tf
    count = 1
    for token in tf_dict.keys():
        print(token, '->', tf_dict[token])
        count += 1
        if count > number_of_terms:
            break

    print('\n')


def create_related_sentences_dict(lemmas, sentences):
    related_sentences = {lemma: [] for lemma in lemmas}  # Dictionary of lemma: ["sent1", "sent2", ...]
    for sentence in sentences:
        for lemma in lemmas:
            if lemma in lemmatize_tokens(nltk.word_tokenize(sentence), min_length=0):  # Must lemmatize sentences to check
                related_sentences[lemma].append(sentence.strip())

    return related_sentences


def save_knowledge_base(knowledge_base, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory in case it doesn't exist
    for lemma, sentences in knowledge_base.items():
        save_line_list_to_file(sentences, f"{directory}/{lemma}")


main()
