# Created by: Acer Jagrup ACJ190005 & Silvano Guadalupe Gallegos SGG180002
#   Assignment: Web Crawler
#   Class: CS 4395.001
#   Date: October 7, 2022
#

from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer


def main():
    starter_url = "https://en.wikipedia.org/wiki/Lamborghini"
    output_file_name = "urls.txt"
    results_file_name = "Complete_TFreq.txt"

    relevant_urls = get_relevant_urls(starter_url, max_number_of_urls=15)

    save_to_file(relevant_urls, output_file_name)
    url_text_files = scrape_list_of_urls(relevant_urls)
    clean_url_text_files = create_clean_files(url_text_files)  # stores a list of filenames

    combined_text = combine_text_from_files(clean_url_text_files)

    # End of FOR loop

    important_tokens = filter_text(combined_text)
    important_lemmas = lemmatize_tokens(important_tokens)

    print_term_frequency(important_lemmas, number_of_terms=30)


def get_relevant_urls(start_url, max_number_of_urls):
    response = requests.get(start_url)

    data = response.text
    soup = BeautifulSoup(data, features="html.parser")

    relevant_urls = []
    for anchor_element in soup.find_all('a'):  # <a href="https://google.com">aaa</a> is an anchor element in HTML
        if is_relevant(anchor_element) and anchor_element.get('href') not in relevant_urls:  # Don't add duplicates
            relevant_urls.append(anchor_element.get('href'))

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


def save_to_file(lines, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def scrape_list_of_urls(url_list):
    file_names = []

    for url in url_list:
        if url.startswith('/wiki'):
            url = "https://en.wikipedia.org" + url

        text_lines = scrape(url)
        file_name = "texts/Text - " + url.split('/')[-1]  # Get the last term of the link (rudimentary approach)
        save_to_file(text_lines, file_name)
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

    raw_text.replace('\n', ' ')
    raw_text.replace('\t', ' ')

    sentences = nltk.sent_tokenize(raw_text)
    return sentences


def create_clean_files(list_of_files):
    file_names = []
    for file_name in list_of_files:
        sentences = clean_text_from_file(file_name)
        save_to_file(sentences, file_name + ".clean")
        file_names.append(file_name)

    return file_names


def combine_text_from_files(file_names):
    combined_text = ""
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            combined_text = combined_text + text

    return combined_text


def filter_text(text):
    # lower every letter
    text = text.lower()

    tokens = word_tokenize(text)

    # get rid of punctuation and stopwords
    filtered_text = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

    return filtered_text


############ End of filter_text ########################


def lemmatize_tokens(tokens):
    WNL = WordNetLemmatizer()

    lemmas = [WNL.lemmatize(token) for token in tokens]

    # Getting the tags from our token list
    tagged_lemmas = nltk.pos_tag(lemmas)

    important_lemmas = []

    # Separating the Nouns from the rest
    for tagged_lemma in tagged_lemmas:
        # Picking out the Nouns
        if tagged_lemma[1].startswith('N'):
            important_lemmas.append(tagged_lemma[0])

        # Picking out the Verbs
        elif tagged_lemma[1].startswith('V'):
            important_lemmas.append(tagged_lemma[0])

    # Removing words shorter than 3 letters
    important_lemmas = [lemma for lemma in important_lemmas if len(lemma) >= 4]

    return important_lemmas


############ End of lemmatize_tokens ########################


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

    print(f"\n\nHere are the top {number_of_terms} terms from every file:")
    # printing out the tf
    count = 1
    for token in tf_dict.keys():
        print(token, '->', tf_dict[token])
        count += 1
        if count > number_of_terms:
            break


############ End of print_term_frequency ########################


main()
