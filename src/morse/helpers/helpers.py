"""
Morse Code Arduino Reader.

Author: John Pignato and Jordan Trombly
"""
try:
    import os
    import time
    import pyfirmata
    from gtts import gTTS
except ImportError as e:
    print(e)
    exit(1)


def get_board()->object:
    """
    Gets a Arduino Board object and starts firmata loop.

    Returns:
        object: Arduino Board
    """

    board = pyfirmata.Arduino(os.getenv('PORT_NAME'))
    it = pyfirmata.util.Iterator(board)
    it.start()
    board.digital[int(os.getenv('DIGITAL_INPUT_PIN'))].mode = pyfirmata.INPUT
    return board

def get_configs(config_file: str)->bool:
    if not os.path.exists(config_file):
        return False
    
    with open(config_file, 'r') as fi:
        for config_val in fi.readlines():
            config_val = config_val.strip()
            if config_val != '':
                value = config_val.split("=")
                os.environ[value[0]] = value[1]
    
    return True



def blink_light(number_of_blinks: int, board: object):
    for i in range(number_of_blinks):
        board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(1)
        time.sleep(.2)
        board.digital[int(os.getenv('DIGITAL_OUTPUT_PIN'))].write(0)
        time.sleep(.2)


def text_to_speech(sentence: str):
    tts = gTTS(text=sentence, lang='en', slow=False)
    tts.save("output.mp3")
    # Playing the converted file
    os.system("afplay output.mp3 &")