import random
import string




class PasswordGeneratorTools:

    #   the structure to parameters is a dict with this possibilities
    #   params = {'alphabet': 3, 'digits': 3, 'special': 3}
    def __init__(self, parameters = None):
        #   picking random alphabetsfrom ascii, special character and digits choices
        self.alphabets = list(string.ascii_letters)
        self.special_characters = list("!@#$%^&*()")
        self.digits = list(string.digits)
        self.parameters = parameters
        #   picking all random choices
        self.characters = self.alphabets + self.special_characters + self.digits


    def __str__(self):
        #   custom characters random generation
        if self.parameters is not None:
            #   create empty password choices
            password = []
            #   check if key exist in dict and add correponding values from this key to password list
            if 'alphabet' in self.parameters:
                password += self.Alphabet(self.parameters['alphabet'])
            if 'digits' in self.parameters:
                password += self.Digit(self.parameters['digits'])
            if 'special' in self.parameters:
                password += self.Special(self.parameters['special'])

            random.shuffle(password)

            return ''.join(password)


    #   random choose from all Characters list
    def CharactersGenerator(self, length):
        character_choices = []                  #   create choices list empty
        for i in range(length):                 #   random choose length value caracteres in ascii list
            character_choices.append(random.choice(self.characters))

        return character_choices                #   return random alphabet choices


    #   random choose from ASCII Characters list
    def Alphabet(self, length):
        alphabet_choices = []                           #   create choices list empty
        for i in range(length):                         #   random choose length value caracteres in ascii list
            alphabet_choices.append(random.choice(self.alphabets))

        return alphabet_choices                         #   return random alphabet choices


    #   random choose from Digits list
    def Digit(self, length):
        digits_choices = []                         #   create choices list empty
        for i in range(length):                     #   random choose length value digits
            digits_choices.append(random.choice(self.digits))

        return digits_choices                       #   return random digits choices


    #   random choose from SpecialCharacters list
    def Special(self, length):
        special_characters_choices = []                 #   create choices list empty
        for i in range(length):                         #   random choose length value special characters
            special_characters_choices.append(random.choice(self.special_characters))

        return special_characters_choices               #   return random special characters choices