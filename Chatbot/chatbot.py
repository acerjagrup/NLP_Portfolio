# Created by: Acer Jagrup ACJ190005 & Silvano Guadalupe Gallegos SGG180002
#   Assignment: Chatbot
#   Class: CS 4395.001
#   Date: November 13, 2022
#

import json
import pickle
import random
import requests
from time import sleep

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('all')

greetings = ["Hello.", "Hello there!", "Nice to meet you!"]
goodbyes = ["It was nice speaking with you.", "See you later.", "Bye bye!"]

prompts_by_intent = {
    "make": {
        "prompt": "What make of car would you like to search for?",
        "examples": ["toyota", "subaru", "mazda"],
        "api_representation": "make"
    },
    "model": {
        "prompt": "What model of car would you like to search for? Don't include the make.",
        "examples": ["camry", "accord"],
        "api_representation": "model"
    },
    "fuel": {
        "prompt": "What type of fuel would you like to search for?",
        "examples": ["gas", "diesel", "electricity"],
        "api_representation": "fuel_type"
    },
    "drive": {
        "prompt": "What drivetrain would you like to search for?",
        "examples": ["fwd", "rwd", "awd", "4wd"],
        "api_representation": "drive"
    },
    "cylinders": {
        "prompt": "How many cylinders are you looking for?",
        "examples": ["2", "4", "6"],
        "api_representation": "cylinders"
    },
    "transmission": {
        "prompt": "Would you like to look for manual or automatic cars?",
        "examples": ["manual", "automatic"],
        "api_representation": "transmission"
    },
    "year": {
        "prompt": "What year would you like to look for?",
        "examples": ["2018", "2006"],
        "api_representation": "year"
    }
}

introduction_statement = "Hi, my name is Autobot. I can provide knowledge on a number of cars.\nPlease type \"exit\" at any time to exit the conversation."
input_pattern = ">>>"
lemmatizer = WordNetLemmatizer()


def ask_for_clarification(some_input, message):
    print(f"{message} {some_input}.")
    answer = ask_question_get_response("Is that correct?")
    if answer is None:
        return None
    return answer.lower().startswith("y")


def ask_question_get_response(question):
    print(question)
    answer = input(input_pattern).strip()
    return answer if "exit" not in answer else None


def get_intent(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    for intent in prompts_by_intent.keys():
        if intent in tokens:
            return intent
    return None


def make_api_call(intent, query):
    api_url = 'https://api.api-ninjas.com/v1/cars'
    api_key = "sSP+krjLeIP0xGsHhLzv1Q==gXBSwzAkgbpnXqMJ"

    url = f"{api_url}?{intent}={query}"
    response = requests.get(url, headers={'X-Api-Key': api_key})
    return response


def question_loop():
    while True:
        request = ask_question_get_response("\nWhat feature of cars would you like to search for?\nIf you're not sure of the categories, just say \"categories\".")

        if request is None:
            break

        if request.lower() == "categories" or request.lower() == "category":
            print("The categories I know about are:")
            [print('\t' + intent) for intent in prompts_by_intent.keys()]
        else:
            intent = get_intent(request)
            if intent is None:
                print("I'm sorry, I didn't understand that category.")
                sleep(1)
            else:
                message = prompts_by_intent[intent]["prompt"] + "\n" + "Some examples are: " + ", ".join(prompts_by_intent[intent]["examples"])
                query = ask_question_get_response(message)
                response = make_api_call(prompts_by_intent[intent]["api_representation"], query)
                if response.ok:
                    json_response = json.loads(response.text)
                    if len(json_response) >= 1:
                        print("Here are some results I found:\n" if len(json_response) > 1 else "Here's a result I found:\n")
                        sleep(1)
                        print(cars_to_string(json_response))
                    else:
                        print("Sorry, I couldn't find any results for that.")
                        sleep(1)
                else:
                    if response.status_code == 400:
                        print("Sorry, I couldn't find any results for that.")
                    else:
                        print("Sorry, I ran into an issue looking that data up.")


def cars_to_string(list_of_cars):
    return '\n'.join([car_to_string(car) for car in list_of_cars])


def car_to_string(car):
    return_string = f'{car["make"].upper()} {car["model"].upper()} {car["year"]}\n'
    if "class" in car.keys():
        return_string += f'Class: {car["class"]}\n'
    if "city_mpg" in car.keys() and "highway_mpg" in car.keys():
        return_string += f'MPG: {car["city_mpg"]} city, {car["highway_mpg"]} highway\n'
    if "transmission" in car.keys():
        return_string += f'Transmission: {"automatic" if car["transmission"] == "a" else "manual"}\n'
    if "drive" in car.keys():
        return_string += f'Drive: {car["drive"].upper()}\n'

    return return_string


def clean_string(user_string):

    tokens = word_tokenize(user_string)
    tokens = [token.lower() for token in tokens]

    extended_stopwords = stopwords.words("english")
    # Specific stopwords because these are used for like/dislike statements
    extended_stopwords.extend(['disapprove', 'approve', 'like', 'dislike', 'love', 'hate', 'enjoy', 'n\'t'])
    clean_tokens = [token for token in tokens if token not in extended_stopwords]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in clean_tokens]

    return " ".join(lemmatized_tokens)


def get_like_statements():
    like_statements = []
    while True:
        like_statement = ask_question_get_response("What's something you like?\nWhen you're done talking about things you like, just say \"done\".")
        if like_statement is None:
            break

        if like_statement.lower() == "done":
            break

        like_statements.append(clean_string(like_statement))

    return like_statements


def get_dislike_statements():
    dislike_statements = []
    while True:
        dislike_statement = ask_question_get_response("What's something you dislike?\nWhen you're done talking about things you don't like, just say \"done\". ")
        if dislike_statement is None:
            break

        if dislike_statement.lower() == "done":
            break

        dislike_statements.append(clean_string(dislike_statement))

    return dislike_statements


def chat():
    try:
        users = retrieve_data('user_data.p')
    except:
        users = {}
    new_user = {}

    print(introduction_statement)
    name = ask_question_get_response("What's your name?")
    if name is None:  # User exited
        return

    is_correct = ask_for_clarification(name, "I have understood that your name is")
    while not is_correct:
        name = ask_question_get_response("What is your name, then?")
        if name is None:  # User exited
            return
        is_correct = ask_for_clarification(name, "I have understood that your name is")
        if is_correct is None:  # User exited
            return
    sleep(1)

    print("Tell me something about yourself.")
    nationality_statement = ask_question_get_response("Where are you from?")
    if nationality_statement is None:
        return
    sleep(1)

    print("That's cool. I'm from Dallas, Texas.")
    sleep(1)

    like_statements = get_like_statements()
    dislike_statements = get_dislike_statements()

    sleep(1)
    print("Interesting...")
    sleep(1)

    print("Personally, the only thing I care about is cars...")
    response = ask_question_get_response("Would you like to talk about them?")
    sleep(1)

    if response is None:
        return

    if response.lower().startswith('n'):
        print("Aw, shucks! That is too bad for you. I don't think we can be friends.")

    else:
        print("You sound very enthusiastic!")
        sleep(1.5)

        print("I know a lot of cars and can help you find some \nbased on a number of parameters.")
        sleep(4)

        question_loop()

    # Save the user's provided information
    new_user['origin'] = nationality_statement
    new_user['likes'] = like_statements if 'likes' not in new_user.keys() else new_user['likes'].extend(like_statements)
    new_user['dislikes'] = dislike_statements if 'dislikes' not in new_user.keys() else new_user['dislikes'].extend(dislike_statements)

    users[name] = new_user
    store_data(users, 'user_data.p')


def store_data(data, file_name):
    pickle.dump(data, open(file_name, 'wb'))


def retrieve_data(file_name):
    data = pickle.load(open(file_name, 'rb'))
    return data


def main():
    chat()
    print(random.choice(goodbyes))
    print("If you have the time, please fill out this online survey so that I can improve my performance.")
    print("https://utdallas.qualtrics.com/jfe/form/SV_5dUMCql3sDOVJ6m")


main()
