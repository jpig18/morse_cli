"""
Morse Code Arduino Reader.

Author: John Pignato and Jordan Trombly
"""
try:
    import os
    import sys
    import time
    import click
    import pyfirmata
    import morse.helpers.helpers as helpers
    from morse.helpers.binaryTree import MorseTree
    
except ImportError as e:
    print(e)
    exit(1)

board = None
CONFIG_PATH = "{0}/.morse_cli".format(os.getenv("HOME"))

@click.group()
def morse():
    """CLI for Morse Code Reader"""
    global board
    #Load env variables
    if not helpers.get_configs("{0}/{1}".format(CONFIG_PATH, "config.dat")):
        click.secho("error: no configs", fg="red")
        click.echo("Did you run 'morse welcome'?")
    
    try:
        board = helpers.get_board()
    except:
        click.secho("error: board not connected", fg="red")
        click.echo("Did you run 'morse welcome'?")


@morse.command()
def welcome():
    """Welcome and config"""

    welcome_output = """
Welcome to Morse CLI 👋

Quick Start 🚀:
    - Export ardunio code (StandardFirmata/StandardFirmata.ino) to the ardunio board
    - Enter the inputs below to be saved for future executions
    - Use the '--help' options to explore the CLI
    - Happy coding!

About ⚙️:
    Created by John Pignato & Jordan Trombly in 2022 for Saint Anselm College's computer networks class

Suggested Inputs:
    Input pin: 10
    Output pin: 13
    min dash length: 0.55
    port: /dev/cu.usbserial-DN01ADTL
"""

    click.echo(welcome_output)
    input_pin = input("Please enter the number of the input pin: ")
    output_pin = input("Please enter the number of the output pin: ")
    min_dash = input("Please enter the amount of time to wait for a dash: ")
    port = input("Please enter the serial port to read ardunio from: ")

    try:
        input_pin = int(input_pin)
        output_pin = int(output_pin)
        min_dash = float(min_dash)
    except: 
        click.secho("error: invalid inputs", fg='red')
        sys.exit(1)


    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
        
    with open("{0}/{1}".format(CONFIG_PATH, "config.dat"), 'w') as fi:

        output_str = """DIGITAL_INPUT_PIN={0}
DIGITAL_OUTPUT_PIN={1}
MIN_DASH_LENGTH={2}
PORT_NAME={3}""".format(input_pin, output_pin, min_dash, port)

        fi.write(output_str)


@morse.command()
def talk():
    """Text to speech for morse code reader"""
    morse_tree = MorseTree()
    blip_sequence = ''
    translated_char = None
    sentence = ''
    word = ''
    start_wait = None
    wait_time = None
    retry = False #Tests whether char exists
    lines_to_clean = 0
    while True:

        button = board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].read()
        click_flag = False

        click_time = time.time()
        while button is True:
            click_flag = True
            board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(1)
            button = board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].read()
            # Quit program
            if time.time() - click_time > 5:
                click.echo("Goodbye")
                helpers.text_to_speech("Goodbye!")
                helpers.blink_light(10, board)
                sys.exit(0)

        release = time.time()

        if click_flag:
            blip_time = release - click_time
            if blip_time >= float(os.getenv('MIN_DASH_LENGTH')): #is dash
                blip_sequence += '-'
                translated_char = morse_tree.traverse('-')
            else: #is dot
                blip_sequence += '.'
                translated_char = morse_tree.traverse('.')
            start_wait = time.time()

        else:

            # Clean up previous outputs 
            for line in range(lines_to_clean):
                sys.stdout.write("\x1b[1A\x1b[2K")
            lines_to_clean = 0

            if(start_wait != None):
                current_time = time.time()
                wait_time = current_time - start_wait
                # Checking for a wait time of 5secs, this means it is a new sentence
                # If so, reset sentence
                if wait_time >= 5:
                    if sentence != '':
                        click.echo(sentence) # Permanent output
                        helpers.text_to_speech(sentence)
                    sentence = ''
                    morse_tree.reset_traverse()
                # Check for in between word with a wait time of 3 sec
                # if so and the word is not '', then check if the sentence is empty
                # If sentence is empty just add the word, if it is not empty add a space between words
                # echo the sentence and then reset the morse tree
                elif (wait_time >= 3 and word != ''):
                    if sentence != '':
                        sentence = sentence + ' ' + word
                    else:
                        sentence = sentence + word
                    word = ''
                    morse_tree.reset_traverse()
                    click.echo(sentence)
                    lines_to_clean += 1
                # In between each character, theres a wait time of 1 sec
                # Check for that wait time and that there was a character entered
                # Reset translated_char to None, reset the morse tree, and echo the word
                elif(wait_time >= 1 and translated_char):
                    # Checks if encountering invalid morse code
                    if translated_char == -1:
                        if retry:
                            click.secho("error: invalid charecter!", fg='red')
                            lines_to_clean += 1
                            wait_time = time.time() # reset wait time
                            retry = False
                        else:
                            retry = True
                    else:
                        word += translated_char
                        translated_char = None
                        retry = False
                        morse_tree.reset_traverse()
                        click.echo("{0} {1}".format(sentence, word))
                        lines_to_clean += 1

            board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(0)

        time.sleep(0.1)

@morse.command()
def math():
    """Calculator for morse code reader"""
    morse_tree = MorseTree()
    blip_sequence = ''
    translated_char = None
    sentence = ''
    word = ''
    start_wait = None
    wait_time = None
    retry = False #Tests whether char exists
    lines_to_clean = 0
    while True:

        button = board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].read()
        click_flag = False

        click_time = time.time()
        while button is True:
            click_flag = True
            board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(1)
            button = board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].read()
            # Quit program
            if time.time() - click_time > 5:
                click.echo("Goodbye")
                helpers.blink_light(10, board)
                sys.exit(0)

        release = time.time()

        if click_flag:
            blip_time = release - click_time
            if blip_time >= float(os.getenv('MIN_DASH_LENGTH')): #is dash
                blip_sequence += '-'
                translated_char = morse_tree.traverse('-')
            else: #is dot
                blip_sequence += '.'
                translated_char = morse_tree.traverse('.')
            start_wait = time.time()

        else:

            # Clean up previous outputs 
            for line in range(lines_to_clean):
                sys.stdout.write("\x1b[1A\x1b[2K")
            lines_to_clean = 0

            if(start_wait != None):
                current_time = time.time()
                wait_time = current_time - start_wait
                # Checking for a wait time of 5secs, this means it is a new sentence
                # If so, reset sentence
                if wait_time >= 5:
                    if sentence != '':
                        try:
                            value = eval(sentence)
                            click.echo("{0} = {1}".format(sentence, value)) # Permanent output
                        except Exception:
                            click.secho("error: invalid equation", fg='red')     
                            lines_to_clean += 1
                            wait_time = time.time()
                    sentence = ''
                    morse_tree.reset_traverse()
                # Check for in between word with a wait time of 3 sec
                # if so and the word is not '', then check if the sentence is empty
                # If sentence is empty just add the word, if it is not empty add a space between words
                # echo the sentence and then reset the morse tree
                elif (wait_time >= 3 and word != ''):
                    if sentence != '':
                        sentence = sentence + ' ' + word
                    else:
                        sentence = sentence + word
                    word = ''
                    morse_tree.reset_traverse()
                    click.echo(sentence)
                    lines_to_clean += 1
                # In between each character, theres a wait time of 1 sec
                # Check for that wait time and that there was a character entered
                # Reset translated_char to None, reset the morse tree, and echo the word
                elif(wait_time >= 1 and translated_char):
                    # Checks if encountering invalid morse code
                    if translated_char == -1:
                        if retry:
                            click.secho("error: invalid charecter!", fg='red')
                            lines_to_clean += 1
                            wait_time = time.time() # reset wait time
                            retry = False
                        else:
                            retry = True
                    else:
                        word += translated_char
                        translated_char = None
                        retry = False
                        morse_tree.reset_traverse()
                        click.echo("{0} {1}".format(sentence, word))
                        lines_to_clean += 1

            board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(0)

        time.sleep(0.1)



@morse.command()
def read()->str:
    """Convert Morse Code into text"""
    morse_tree = MorseTree()
    blip_sequence = ''
    translated_char = None
    sentence = ''
    word = ''
    start_wait = None
    wait_time = None
    retry = False #Tests whether char exists
    lines_to_clean = 0
    while True:

        button = board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].read()
        click_flag = False

        click_time = time.time()
        while button is True:
            click_flag = True
            board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(1)
            button = board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].read()
            # Quit program
            if time.time() - click_time > 5:
                click.echo("Goodbye")
                helpers.blink_light(10, board)
                sys.exit(0)

        release = time.time()

        if click_flag:
            blip_time = release - click_time
            if blip_time >= float(os.getenv('MIN_DASH_LENGTH')): #is dash
                blip_sequence += '-'
                translated_char = morse_tree.traverse('-')
            else: #is dot
                blip_sequence += '.'
                translated_char = morse_tree.traverse('.')
            start_wait = time.time()

        else:

            # Clean up previous outputs 
            for line in range(lines_to_clean):
                sys.stdout.write("\x1b[1A\x1b[2K")
            lines_to_clean = 0

            if(start_wait != None):
                current_time = time.time()
                wait_time = current_time - start_wait
                # Checking for a wait time of 5secs, this means it is a new sentence
                # If so, reset sentence
                if wait_time >= 5:
                    if sentence != '':
                        click.echo(sentence) # Permanent output
                    sentence = ''
                    morse_tree.reset_traverse()
                # Check for in between word with a wait time of 3 sec
                # if so and the word is not '', then check if the sentence is empty
                # If sentence is empty just add the word, if it is not empty add a space between words
                # echo the sentence and then reset the morse tree
                elif (wait_time >= 3 and word != ''):
                    if sentence != '':
                        sentence = sentence + ' ' + word
                    else:
                        sentence = sentence + word
                    word = ''
                    morse_tree.reset_traverse()
                    click.echo(sentence)
                    lines_to_clean += 1
                # In between each character, theres a wait time of 1 sec
                # Check for that wait time and that there was a character entered
                # Reset translated_char to None, reset the morse tree, and echo the word
                elif(wait_time >= 1 and translated_char):
                    # Checks if encountering invalid morse code
                    if translated_char == -1:
                        if retry:
                            click.secho("error: invalid charecter!", fg='red')
                            lines_to_clean += 1
                            wait_time = time.time() # reset wait time
                            retry = False
                        else:
                            retry = True
                    else:
                        word += translated_char
                        translated_char = None
                        retry = False
                        morse_tree.reset_traverse()
                        click.echo("{0} {1}".format(sentence, word))
                        lines_to_clean += 1

            board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(0)

        time.sleep(0.1)







if __name__ == '__main__':
    #Load env variables
    welcome()
    board = get_board()
    
    read_char(tree)
    # morse()