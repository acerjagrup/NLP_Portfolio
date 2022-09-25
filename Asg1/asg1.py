# Created by: Acer Jagrup ACJ190005
#   Assignment: Assignment #1
#   Class: CS 4395.001
#   Date: September 4, 2022
#

import sys
import os

import re
import pickle


class Person:
    last = ""
    first = ""
    mi = ""
    id = ""
    phone = ""

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def get_id(self):
        return self.id

    def display(self):
        print(f"Employee id: {self.id}\n\t{self.first} {self.mi} {self.last}\n\t{self.phone}")


def main():
    file_lines = get_file_lines()
    if not file_lines:  # File couldn't be read
        return

    file_lines.pop(0)  # Remove the first item (row 1--it is only labels, no data)
    person_dict = convert_to_person_dict(file_lines)
    if not person_dict:  # No dict was made (because an ID was duplicated)
        return

    # Demonstrate pickle
    pickle.dump(person_dict, open('persons.p', 'wb'))
    retrieved_person_dict = pickle.load(open('persons.p', 'rb'))

    display_all_persons(retrieved_person_dict)


def get_file_lines():
    if len(sys.argv) < 2:
        print("Please specify a file to read data from.")
        return None

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        print("Bad filepath.")
        return None

    with open(file_name, "r") as f:
        file_lines = f.readlines()

    return file_lines


def convert_to_person_dict(unprocessed_person_list):
    persons = {}  # Create new dictionary of persons which will include every person in the data
    for person_string in unprocessed_person_list:
        sanitized_person_string = person_string.strip()  # Remove \n and trailing whitespaces
        person_data = sanitized_person_string.split(",")
        new_person = create_person(person_data)
        new_person_id = new_person.get_id()
        if new_person_id in persons.keys():
            print(f"Error: ID {new_person_id} occurs more than once")
            return None
        persons[new_person_id] = new_person

    return persons


def create_person(person_data):
    if len(person_data) != 5:
        raise ValueError("Person data must have 5 elements: last, first, mi, id, phone")

    last = str(person_data[0]).lower().capitalize()
    first = str(person_data[1]).lower().capitalize()
    mi = str(person_data[2]).upper() if (person_data[2] != "") else "X"  # Use X if no initial is specified
    id = str(person_data[3]).upper()
    while not re.search("^[A-Za-z]{2}[0-9]{4}$", id):
        id = input(f"ID invalid: {id}\nID is two letters followed by four digits\nPlease enter a valid ID: ").upper()
    phone = str(person_data[4])

    # Only lets those with consistent delimiter though: 555.555.5555 is fine but not 555.555-5555
    if re.search("^[0-9]{3}.[0-9]{3}.[0-9]{4}$", phone):  # Phone is in the right format with a different delimiter
        phone = phone.replace(phone[3], "-")  # Replace all instances of first delimiter with -

    if re.search("^[0-9]{10}$", phone):
        phone = phone[:3] + "-" + phone[3:6] + "-" + phone[6:10]

    while not re.search("^[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone):  # If it's still not correct, reinput is necessary
        phone = input(f"Phone number invalid: {phone}\nPlease input a phone number of the format 555-555-5555: ")

    return Person(last, first, mi, id, phone)


def display_all_persons(person_dict):
    print("\nEmployee list:")
    for _, person in person_dict.items():
        print()
        person.display()


main()
