# import statements
import string
import secrets
from tkinter import *

# This function generates the 8-32 character password using a combination of
# uppercase letters, lowercase letters, special characters and 0-9 digits.
def generatePassword():
    password = ''
    pw_length = secrets.randbelow(25) + 8   # sets length of the password using randbelow() function

    alpha_lc = string.ascii_letters[0:26] # lowercase letters
    alpha_uc = string.ascii_letters[26:52]  # uppercase letters
    special_characters = string.punctuation # special characters

    count = 0
    while count < pw_length:

        # This conditional ensures that each password will have at least one
        # special character, uppercase letter, lowercase letter, and 0-9 digit.
        # After that, the type of a new character is selected at random.
        if count < 4:
            choice = count
        else:
            choice = secrets.randbelow(4) # choice is a random number between 0 and 3 (inclusive)

        new_character = None # character is assigned to a variable before being added to the password string

        # This conditional selects the type based on the random choice variable.
        if choice == 0:
            new_character = str(secrets.randbelow(10))

        elif choice == 1:
            new_character = str(alpha_lc[secrets.randbelow(len(alpha_lc))])

        elif choice == 2:
            new_character = str(alpha_uc[secrets.randbelow(len(alpha_uc))])

        else:
            new_character = str(special_characters[secrets.randbelow(len(special_characters))])


        # If password is at length 2 or longer, its last and second-to-last characters
        # are assigned to variables. Otherwise, those variables are set to None.
        if count >= 2:
            last_character = password[-1]
            second_to_last_character = password[-2]

        else:
            last_character = None
            second_to_last_character = None


        # This conditional checks that the last two characters are different than the
        # new character so that the password will not contain a sequence of 3 or more
        # of the same character at any point. If not, the new character is not added
        # and the count is not increased for that iteration of the loop.
        if not (new_character == last_character and new_character == second_to_last_character):
            password += new_character
            count += 1

    # slices off the first part of the password string (which was created by the conditional
    # to make sure the password has one of each type of character) so that those
    # characters can be redistributed randomly into the password
    pw_substring = password[0:4]
    password = password[4:pw_length]

    count = 0                               # while loop grabs each character of the slice and
    while count < len(pw_substring):        # inserts it randomly back into the password string.

        random_index = secrets.randbelow(len(password)) # picks a random index of the string
        pw_slice_one = password[0:random_index]
        pw_slice_two = password[random_index:len(password)]

        # inserts the currently selected character
        # into the spot designated by the random index
        new_password = pw_slice_one + pw_substring[count] + pw_slice_two

        sample = None

        # creates a slice of characters adjacent to the newly inserted element
        # so that it can be checked for a repeating sequence of three or more
        # characters. This is done to improve password security.
        if random_index <= 1:
            sample = new_password[0: random_index + 3]
        elif random_index >= len(password) - 2:
            sample = new_password[len(new_password) - 4:len(new_password)]
        else:
            sample = new_password[random_index - 2: random_index + 3]

        subcount = 0
        check = True
        last_character = None
        second_to_last_character = None

        # iterates through the sample and checks for the repeating sequence
        # if such a sequence is detected, the while loop stops executing
        while subcount < len(sample) and check != False:

            if subcount >= 2:
                last_character = sample[subcount - 1]
                second_to_last_character = sample[subcount - 2]

            else:
                last_character = None
                second_to_last_character = None

            # if the previous two characters are the same as the currently selected character,
            # the check variable is changed to False
            if sample[subcount] == last_character and sample[subcount] == second_to_last_character:
                check = False

            subcount += 1

        # if the check variable was changed to False in the previous loop,
        # the character is not inserted at the random index that was generated
        # and the count is not increased for that iteration of the loop.
        if check != False:
            password = new_password
            count += 1

    return password

# GUI code
def insertPassword(textbox):
    textbox.delete('1.0', END) # clears contents of the text box
    textbox.insert(END, generatePassword()) # inserts generated password into the text box

def copyPassword(gui_object, textbox): 
    textbox_contents = textbox.get("1.0", END) 
    gui_object.clipboard_clear() # clears previous clipboard contents
    gui_object.clipboard_append(textbox_contents) # copies generated password to the clipboard

gui= Tk(None, None, "password generator") # tkinter Tk() object
gui.geometry('265x72') # sets default window size

textBox = Text(gui, height = 1, width = 32) # Text object where the password goes
generateButton = Button(gui, text = 'Generate', bd = '1', width = 16, command = lambda: insertPassword(textBox)) 
copyButton = Button(gui, text = 'Copy', bd = '1', width = 16, command = lambda: copyPassword(gui, textBox)) 

textBox.pack(side = 'top')
generateButton.pack(side = 'top')
copyButton.pack(side = 'top')

gui.mainloop() # starts the gui
