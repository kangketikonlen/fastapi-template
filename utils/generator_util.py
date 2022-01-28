import random


def password_generator():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password_length = 8
    password = ""

    for i in range(password_length):
        next_index = random.randrange(len(alphabet))
        password = password + alphabet[next_index]
    return password
