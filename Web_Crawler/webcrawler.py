# Created by: Acer Jagrup ACJ190005 & Silvano Guadalupe Gallegos SGG180002
#   Assignment: Web Crawler
#   Class: CS 4395.001
#   Date: October 2, 2022
#

from bs4 import BeautifulSoup
import wikipedia
import requests
import nltk


def main():
    starter_url = "https://en.wikipedia.org/wiki/Lamborghini"
    output_file_name = "urls.txt"

    # starts the crawling of url
    relevant_urls = crawl(starter_url)
    save_to_file(relevant_urls, output_file_name)
    url_text_files = scrape_list_of_urls(relevant_urls)
    create_clean_files(url_text_files)


def crawl(start_url):
    response = requests.get(start_url)

    data = response.text
    soup = BeautifulSoup(data, features="html.parser")

    MAX_NUMBER_OF_URLS = 15

    relevant_urls = []
    for anchor_element in soup.find_all('a'):  # <a href="https://google.com">aaa</a> is an anchor element in HTML
        if is_relevant(anchor_element) and anchor_element.get('href') not in relevant_urls:  # Don't add duplicates
            relevant_urls.append(anchor_element.get('href'))

        if len(relevant_urls) >= MAX_NUMBER_OF_URLS:
            break

    else:  # In Python, this means the loop terminated without breaking
        print(f"Only {len(relevant_urls)} relevant urls found out of the maximum {MAX_NUMBER_OF_URLS}")

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

        if "external text" in class_list and "wikipedia" in link:  # Usually links to editing the wiki page and similar stuff
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
        file_name = "texts/Text - " + url.split('/')[-1]
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
    for file_name in list_of_files:
        sentences = clean_text_from_file(file_name)
        save_to_file(sentences, file_name + ".clean")


main()
