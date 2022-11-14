import json
import pickle
import random
from time import sleep

import nltk
import requests

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

introduction_statement = "Hi, my name is Lambot. I can provide any knowledge on Lamborghini.\nPlease type \"exit\" at any time to exit the conversation."
input_pattern = ">>>"


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

        if "exit" in request.lower():
            break

        if request.lower() == "categories":
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
                        print('\n'.join(parse_api_response(json_response)))
                    else:
                        print("Sorry, I couldn't find any results for that.")
                else:
                    if response.status_code == 400:
                        print("Sorry, I couldn't find any results for that.")
                    else:
                        print("Sorry, I ran into an issue looking that data up.")


def parse_api_response(list_of_cars):
    return [car_to_string(car) for car in list_of_cars]


def car_to_string(car):
    return_string = f'{car["make"].upper()} {car["model"].upper()} {car["year"]}\n'
    if "class" in car.keys():
        return_string += f'Class: {car["class"]}\n'
    if "city_mpg" in car.keys() and "highway_mpg" in car.keys():
        return_string += f'MPG: {car["city_mpg"]} city, {car["highway_mpg"]} highway\n'
    if "transmission" in car.keys():
        return_string += f'Transmission: {"automatic" if car["transmission"] == "a" else "manual"}\n'
    if "drive" in car.keys():
        return_string += f'Drive: {car["drive"]}\n'

    return return_string


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

    like_statement = ask_question_get_response("What do you like?")
    if like_statement is None:
        return

    dislike_statement = ask_question_get_response("What is something you dislike?")
    if dislike_statement is None:
        return
    sleep(1)
    print("Interesting...")
    sleep(1)

    print("Personally, the only thing I care about is cars...")
    response = ask_question_get_response("Would you like to talk about them?")
    sleep(1)

    if response is None:
        return

    if response.startswith('n'):
        print("Aw, shucks! That is too bad for you. I don't think we can be friends.")
        return

    print("You sound very enthusiastic!")
    sleep(1.5)

    new_user['personal_info'] = nationality_statement
    new_user['likes'] = like_statement
    new_user['dislikes'] = dislike_statement

    print("I know a lot about many makes and models of cars and can help you \nfind cars based on some parameter you're looking for.")
    sleep(4)
    question_loop()

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


main()
