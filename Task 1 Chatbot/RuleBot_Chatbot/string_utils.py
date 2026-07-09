def reverse_string(s):
    return s[::-1]

def is_palindrome(s):
    clean_s = ''.join(c.lower() for c in s if c.isalnum())
    return clean_s == clean_s[::-1]

def count_characters(s):
    return len(s)

def count_words(s):
    return len(s.split())

def count_vowels(s):
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)

def count_consonants(s):
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char.isalpha() and char not in vowels)

def to_uppercase(s):
    return s.upper()

def to_lowercase(s):
    return s.lower()

def capitalize_sentence(s):
    return s.capitalize()

def remove_extra_spaces(s):
    return " ".join(s.split())

def replace_word(s, old_word, new_word):
    return s.replace(old_word, new_word)

def string_length(s):
    return len(s)
