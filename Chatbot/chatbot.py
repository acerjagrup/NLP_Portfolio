import pickle
import random
from time import sleep

import nltk

import cars_api as api


# from nltk.stem import WordNetLemmatizer
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import Dense, Dropout

# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download('omw-1.4')
#nltk.download('stopwords')

greetings = ["Hello.", "Hello there!", "Nice to meet you!"]
goodbyes = ["It was nice speaking with you.", "See you later", "Bye bye!"]

intents = {
    # "greeting": ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy"],
    # "goodbye": ["bye", "goodbye", "see ya", "adios", "cya", "see you later", "goodbye now",
    #                      "it was nice talking to you", "I'm gonna go now", "gtg", "g2g"],
    # "question": ["What do you know about", "What is", "How many", "Why", "When", "When did", "Who is", "Who",
    #                      "Whom", "How", "What is", "What", "Where", "Which"]
    "like": ["What are some cars you like?", "Can you name me a Lambo you like", "What would you like to know"],
    "dislike": ["Is there something you hate?", "Are there any Lambos that you dislike?"]
}

introduction_statement = "Hi, my name is Lambot. I can provide any knowledge on Lamborghini.\nPlease type \"exit\" at any time to exit the conversation."
input_pattern = ">>>"

# examples_list = []
# intents_list = []
#
# for intent, examples in intents.items():
#     for example in examples:
#         examples_list.append(example)
#         intents_list.append(intent)
#
# vectorizer = TfidfVectorizer()
#
# vectorized_examples = vectorizer.fit_transform(examples_list)
#
# # intent_enum = {"greeting": 1, "goodbye": 2, "questions": 3}
# # intent_enum_list = ["greeting", "goodbye", "questions"]
# # y = [intent_enum[intent] for intent in intents_list]
#
# X_train, X_test, y_train, y_test = train_test_split(vectorized_examples, intents_list)
#
# intents_model = LogisticRegression()
# intents_model.fit(X_train, y_train)


def ask_for_clarification(some_input, message):
    print(f"{message} {some_input}.")
    answer = ask_question_get_response("Is that correct?")
    return answer.startswith("y")


def ask_question_get_response(question):
    print(question)
    return input(input_pattern).lower().strip()


def get_important_terms(sentence):
    tokens = nltk.word_tokenize(sentence)


def chat():
    try:
        users = retrieve_data('user_data.p')
    except:
        users = {}
    new_user = {}

    print(introduction_statement)
    name = ask_question_get_response("What's your name?")
    is_correct = ask_for_clarification(name, "I have understood that your name is")
    while not is_correct:
        name = ask_question_get_response("What is your name, then?")
        is_correct = ask_for_clarification(name, "I have understood that your name is")

    print("Tell me something about yourself.")
    nationality_statement = ask_question_get_response("Where are you from?")

    print("That's cool. I'm from Dallas, Texas.")
    sleep(1)

    like_statement = ask_question_get_response("What do you like?")

    dislike_statement = ask_question_get_response("What is something you dislike?")

    print("Personally, the only thing I care about is cars...")
    response = ask_question_get_response("Would you like to talk about them?")

    if response.startswith('n'):
        print("Aw, shucks! That is too bad for you. I don't think we can be friends.")
        return

    print("I'll take that as an enthusiastic \"yes\".")

    new_user['personal_info'] = nationality_statement
    new_user['likes'] = like_statement
    new_user['dislikes'] = dislike_statement

    question = ask_question_get_response("What's a question you have about cars or automobiles in general?")

    print(api.get_from_model('camry'))

    important_terms = get_important_terms(question)


    #intent = intents_model.predict(vectorizer.transform([message]))[0]

    # if intent == "question":
    #     print("Very interesting question.")
    # elif intent == "greeting":
    #     print(random.choice(greetings))
    # # elif intent == "goodbye":
    # #     break

    users[name] = new_user
    store_data(users, 'user_data.json')


def store_data(data, file_name):
    pickle.dump(data, open(file_name, 'wb'))


def retrieve_data(file_name):
    data = pickle.load(open(file_name, 'rb'))
    return data


chat()

print(random.choice(goodbyes))

#Stopword custome list
"""
stopwords = stopwords.words('english')
stop_list = ["'s", "too"]
"""


"""
    def bag_of_words (input, vocab):
        bow = [0] * len(vocab)
        
        for word in input:
            for index, Word in enumerate(vocab):
                if Word == word:
                    bow[index] = 1
        return np.array(bow)
    
    def predicate_class(text):
        bow = bag_of_words(,)
        results = model.predict(np.array([bow]))[0]
        thresh = 0.2    
        y_pred = [ [index, res] for index, res in enumerate(result) if res>thresh ]

        y_pred.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in y_pred:
            return_list.append(labels[r[0]])
        return return_list
    def get_responce(intentList, intentDict):
        tag = intentList[0]
        list_of_keys = intentDict.keys()
        
        for reply in list_of_keys:
            if reply == tag:
                if reply["responses"].isEmpty():
                    #google it 
                    result = 
                else:
                    result = random.choice(reply["responses"])
        return result
"""
